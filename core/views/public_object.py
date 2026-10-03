"""Minimal anonymous-safe projection of a game object."""

from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from characters.models.changeling.chimera import Chimera
from characters.models.core import CharacterModel, Group
from characters.models.mage.effect import Effect
from characters.models.mage.rote import Rote
from core.constants import ImageStatus
from core.models import CharacterTemplate
from core.permissions import Permission, PermissionManager
from game.security import readable_chronicles
from items.models.core import ItemModel
from locations.models.core import LocationModel


def can_view_public_object(request, obj):
    """Admit a detail card without treating partial roles as full access.

    Full viewers retain access regardless of the discovery setting. Otherwise
    only public objects or objects in a readable chronicle have a card; private,
    legacy custom and unknown values fail closed.
    """
    if PermissionManager.user_has_permission(
        request.user, obj, Permission.VIEW_FULL, request=request
    ):
        return True
    if obj.visibility == "PUB":
        return True
    return bool(
        obj.visibility == "CHR"
        and obj.chronicle_id is not None
        and readable_chronicles(request.user).filter(pk=obj.chronicle_id).exists()
    )


class PublicObjectDetailView(View):
    model_class = None
    resolved_object = None

    def get(self, request, *args, **kwargs):
        obj = self.resolved_object
        if obj is None:
            obj = get_object_or_404(self.model_class, pk=kwargs["pk"])
        if not can_view_public_object(request, obj):
            raise Http404("Object not found")
        image_url = None
        if obj.image and obj.image_status == ImageStatus.APPROVED:
            image_url = obj.image.url
        public_object = {
            "name": obj.name,
            "public_info": obj.public_info,
            "image_url": image_url,
        }
        return render(request, "core/public_object_detail.html", {"public_object": public_object})


def render_public_object_list(request, model_class, extra_context=None):
    """Render only allowlisted public fields from core.Model collections."""
    if issubclass(model_class, Group):
        route = "characters:group"
    elif issubclass(model_class, Chimera):
        route = "characters:changeling:chimera"
    elif issubclass(model_class, Effect):
        route = "characters:mage:effect"
    elif issubclass(model_class, Rote):
        route = "characters:mage:rote"
    elif issubclass(model_class, CharacterModel):
        route = "characters:character"
    elif issubclass(model_class, ItemModel):
        route = "items:item"
    elif issubclass(model_class, LocationModel):
        route = "locations:location"
    elif issubclass(model_class, CharacterTemplate):
        route = "core:character_template_detail"
    else:
        raise ValueError("Unsupported public list model")

    queryset = model_class.objects.order_by("name")
    user = request.user
    if not (user.is_authenticated and (user.is_staff or user.is_superuser)):
        visible = Q(visibility="PUB")
        if issubclass(model_class, CharacterTemplate):
            visible &= Q(is_public=True)
        if user.is_authenticated:
            # Private read/discovery roles and public cards share identities,
            # but public rows always remain an allowlisted projection.
            readable = PermissionManager.filter_queryset_for_user(user, model_class.objects.all())
            visible |= Q(pk__in=readable.values("pk"))
            visible |= Q(
                visibility="CHR",
                chronicle_id__in=readable_chronicles(user).values("pk"),
            )
        queryset = queryset.filter(visible).distinct()

    objects = [
        {
            "name": row["name"],
            "public_info": row["public_info"],
            "image_url": (
                default_storage.url(row["image"])
                if row["image"] and row["image_status"] == ImageStatus.APPROVED
                else None
            ),
            "url": reverse(route, kwargs={"pk": row["pk"]}),
        }
        for row in queryset.values("pk", "name", "public_info", "image", "image_status")[:250]
    ]
    context = {
        "public_objects": objects,
        "title": model_class._meta.verbose_name_plural.title(),
        "nav_active": route.split(":")[0],
    }
    context.update(extra_context or {})
    return render(request, "core/public_object_list.html", context)

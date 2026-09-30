from django.db.models import Q
from django.http import Http404
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.core import CharacterModel
from characters.models.demon import Pact
from core.mixins import MessageMixin
from core.permissions import Permission, PermissionManager


def user_can_view_pact(user, pact, request=None):
    """A pact is private to staff and whoever may fully view its demon or its thrall."""
    if user.is_staff or user.is_superuser:
        return True
    return any(
        character is not None
        and PermissionManager.user_has_permission(
            user, character, Permission.VIEW_FULL, request=request
        )
        for character in (pact.demon, pact.thrall)
    )


class PactDetailView(DetailView):
    """LOGIN route; a pact the user may not view gets the same 404 as a missing one."""

    model = Pact
    template_name = "characters/demon/pact/detail.html"

    def get_queryset(self):
        return Pact.objects.select_related("demon", "thrall")

    def get_object(self, queryset=None):
        pact = super().get_object(queryset)
        if not user_can_view_pact(self.request.user, pact, request=self.request):
            raise Http404("No Pact matches the given query.")
        return pact


class PactCreateView(MessageMixin, CreateView):
    model = Pact
    fields = [
        "demon",
        "thrall",
        "terms",
        "faith_payment",
        "enhancements",
        "active",
    ]
    template_name = "characters/demon/pact/form.html"
    success_message = "Pact created successfully."
    error_message = "There was an error creating the Pact."


class PactUpdateView(MessageMixin, UpdateView):
    model = Pact
    fields = [
        "demon",
        "thrall",
        "terms",
        "faith_payment",
        "enhancements",
        "active",
    ]
    template_name = "characters/demon/pact/form.html"
    success_message = "Pact updated successfully."
    error_message = "There was an error updating the Pact."


class PactListView(ListView):
    """LOGIN route listing only the pacts the user may view."""

    model = Pact
    ordering = ["demon", "thrall"]
    template_name = "characters/demon/pact/list.html"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("demon", "thrall")
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return queryset
        # Narrow in SQL to pacts touching a character the user can read at all, then keep
        # those whose demon or thrall the user may fully view.
        readable = PermissionManager.filter_queryset_for_user(
            user, CharacterModel.objects.all()
        ).values("pk")
        candidates = queryset.filter(Q(demon__in=readable) | Q(thrall__in=readable))
        visible = [
            pact.pk for pact in candidates if user_can_view_pact(user, pact, request=self.request)
        ]
        return queryset.filter(pk__in=visible)

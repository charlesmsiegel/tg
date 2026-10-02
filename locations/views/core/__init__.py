from collections import Counter

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

from core.registries import get_registry
from core.utils import get_gameline_name
from core.views.generic import DictView
from core.views.public_object import PublicObjectDetailView, render_public_object_list
from core.views.registry import RegistryDetailView
from game.models import Chronicle, ObjectType
from locations.forms.core.location_creation import LocationCreationForm
from locations.models.core.location import LocationModel
from locations.views import mage, werewolf

from .city import CityCreateView, CityDetailView, CityListView, CityUpdateView
from .location import LocationCreateView, LocationDetailView, LocationUpdateView


class GenericLocationDetailView(RegistryDetailView):
    registry_app = "locations"
    model_class = LocationModel
    public_view_class = PublicObjectDetailView


class LocationIndexView(View):
    """Staff index (Spread M2): one chronicle's containment tree.

    ``?chronicle=<pk|none>`` picks the chronicle and ``?line=<code>`` narrows the tree to
    one gameline, keeping the ancestors that lead to a match, so every view is a
    bookmarkable URL. Everyone else gets the shared public object list.
    """

    MAX_DEPTH = 8

    def get(self, request, *args, **kwargs):
        if not (
            request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
        ):
            return render_public_object_list(
                request,
                LocationModel,
                (
                    {"location_form": LocationCreationForm(user=request.user)}
                    if request.user.is_authenticated
                    else None
                ),
            )
        context = self.get_context()
        return render(request, "locations/index.html", context)

    def get_context(self):
        # One polymorphic fetch plus one query for the containment links; the old
        # recursive row template queried every location's children.
        locations = list(LocationModel.objects.order_by("name"))
        by_pk = {loc.pk: loc for loc in locations}
        owners = dict(
            LocationModel.objects.filter(owner__isnull=False).values_list("pk", "owner__username")
        )
        children, contained = {}, set()
        links = LocationModel.contained_within.through.objects.values_list(
            "from_locationmodel_id", "to_locationmodel_id"
        )
        for child_pk, container_pk in links:
            contained.add(child_pk)
            if child_pk in by_pk:
                children.setdefault(container_pk, []).append(by_pk[child_pk])
        for kids in children.values():
            kids.sort(key=lambda loc: loc.name.lower())

        by_chronicle = {}
        for loc in locations:
            by_chronicle.setdefault(loc.chronicle_id, []).append(loc)
        chronicles = list(Chronicle.objects.all()) + [None]
        selected = self.selected_chronicle(chronicles, by_chronicle)
        chron_locations = by_chronicle.get(selected.pk if selected else None, [])

        line = self.request.GET.get("line", "")
        if line not in settings.GAMELINES:
            line = ""
        counts = Counter(loc.get_gameline() for loc in chron_locations)

        def build(loc, depth, path):
            path = path | {loc.pk}
            kids = [
                build(child, depth + 1, path)
                for child in children.get(loc.pk, [])
                if child.pk not in path
            ]
            kids = [kid for kid in kids if kid]
            match = not line or loc.get_gameline() == line
            if not (match or kids):
                return None
            return {
                "location": loc,
                "children": kids,
                "depth": min(depth, self.MAX_DEPTH),
                "match": match,
                "owner": owners.get(loc.pk, ""),
            }

        roots = [loc for loc in chron_locations if loc.pk not in contained]
        tree = [node for node in (build(loc, 0, frozenset()) for loc in roots) if node]

        user = self.request.user
        return {
            "objects": get_registry("locations").menu(user),
            "form": LocationCreationForm(user=user),
            "header": user.profile.preferred_heading,
            "selected_chronicle": selected,
            "chronicle_key": str(selected.pk) if selected else "none",
            "chronicle_switch": [
                {"chronicle": chron, "key": str(chron.pk) if chron else "none"}
                for chron in chronicles
                if chron != selected
            ],
            "selected_line": line,
            "line_filter": [{"key": "", "label": "All lines", "count": len(chron_locations)}]
            + [
                {"key": code, "label": data["name"].split(":")[0], "count": counts[code]}
                for code, data in settings.GAMELINES.items()
                if counts[code]
            ],
            "place_count": len(chron_locations),
            "location_tree": tree,
        }

    def selected_chronicle(self, chronicles, by_chronicle):
        """The requested chronicle, else the first one with places, else the first one."""
        keys = {str(chron.pk) if chron else "none": chron for chron in chronicles}
        requested = self.request.GET.get("chronicle")
        if requested in keys:
            return keys[requested]
        return next(
            (chron for chron in chronicles if by_chronicle.get(chron.pk if chron else None)),
            chronicles[0],
        )


__all__ = [
    "Http404",
    "redirect",
    "render",
    "View",
    "get_gameline_name",
    "DictView",
    "Chronicle",
    "ObjectType",
    "LocationCreationForm",
    "LocationModel",
    "mage",
    "werewolf",
    "CityCreateView",
    "CityDetailView",
    "CityListView",
    "CityUpdateView",
    "LocationCreateView",
    "LocationDetailView",
    "LocationUpdateView",
]

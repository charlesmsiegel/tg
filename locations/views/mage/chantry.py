from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from characters.forms.core.linked_npc import LinkedNPCForm
from characters.models.core.background_block import Background
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ViewPermissionMixin,
    launch_chronicle,
)
from core.permissions import PermissionManager
from core.views.generic import DictView
from game.models import Chronicle
from locations.forms.mage.chantry import (
    ChantryCreateForm,
    ChantryEffectsForm,
    ChantryPointForm,
)
from locations.forms.mage.library import LibraryForm
from locations.forms.mage.node import NodeForm
from locations.forms.mage.sanctum import SanctumForm
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.registry import registry
from locations.services.chantry_points import apply_type_grants

# Every field of the direct (ST) forms; chantry/form.html renders exactly these.
DIRECT_FORM_FIELDS = [
    "name",
    "contained_within",
    "gauntlet",
    "shroud",
    "dimension_barrier",
    "description",
    "faction",
    "leadership_type",
    "season",
    "chantry_type",
    "total_points",
    "integrated_effects",
    "leaders",
    "members",
    "cabals",
    "ambassador",
    "node_tender",
    "investigator",
    "guardian",
    "teacher",
]


def direct_create_chronicles(user):
    """Chronicles in which user may create a chantry with the direct form.

    Mirrors PermissionManager.can_manage_scope for the Mage gameline: staff get
    every chronicle; otherwise the chronicles the user heads or is a Mage ST of.
    """
    if not user.is_authenticated:
        return Chronicle.objects.none()
    if user.is_staff or user.is_superuser:
        return Chronicle.objects.all()
    mage = settings.GAMELINES["mta"]["name"]
    return Chronicle.objects.filter(
        Q(head_st=user) | Q(st_relationships__user=user, st_relationships__gameline__name=mage)
    ).distinct()


class _ChantryDetailView(ViewPermissionMixin, DetailView):

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        factions = []
        f = self.object.faction
        while f is not None:
            factions.append(f)
            f = f.parent
        factions.reverse()
        factions = [f'<a href="{x.get_absolute_url()}">{x}</a>' for x in factions]
        factions = "/".join(factions)
        context["factions"] = factions
        return context


ChantryDetailView = registry.view("locations.Chantry", "detail")


class _ChantryListView(ListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_create_directly"] = direct_create_chronicles(self.request.user).exists()
        return context


ChantryListView = registry.view("locations.Chantry", "list")


class _ChantryCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    """All-fields create form for Mage STs of the chosen chronicle, and staff."""

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get("chronicle"):
            initial.pop("chronicle", None)
            chronicle = launch_chronicle(self.request)
            if chronicle and direct_create_chronicles(self.request.user).filter(pk=chronicle.pk).exists():
                initial["chronicle"] = chronicle
        return initial

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not direct_create_chronicles(request.user).exists():
            raise PermissionDenied("Only storytellers can create a chantry directly")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["chronicle"].queryset = direct_create_chronicles(self.request.user)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        return form

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if not PermissionManager.user_can_manage_creation(request.user, form, request=request):
            raise PermissionDenied("Choose a chronicle you are a storyteller for")
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        apply_type_grants(self.object)
        return response


ChantryCreateView = registry.view("locations.Chantry", "create")


class _ChantryUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    """Direct edit form; the route policy (OBJECT_ST_WRITE) limits it to scoped STs and staff."""

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        if "chantry_type" in form.changed_data:
            apply_type_grants(self.object)
        return response


ChantryUpdateView = registry.view("locations.Chantry", "update")


class LoadExamplesView(View):
    def get(self, request, *args, **kwargs):
        from core.ajax import dropdown_options_response

        category_choice = request.GET.get("category")
        object_id = request.GET.get("object")
        m = get_object_or_404(Chantry, pk=object_id)

        category_choice = request.GET.get("category")
        if category_choice == "New Background":
            examples = Background.objects.filter(property_name__in=m.allowed_backgrounds).order_by(
                "name"
            )
            if m.points < 5:
                examples = examples.exclude(property_name__in=["sanctum"])
            if m.points < 4:
                examples = examples.exclude(property_name__in=["enhancement", "requisitions"])
            if m.points < 3:
                examples = examples.exclude(property_name__in=["node", "resources"])
            if m.points < 2:
                examples = examples.exclude(
                    property_name__in=[
                        "allies",
                        "arcane",
                        "backup",
                        "cult",
                        "elders",
                        "library",
                        "retainers",
                        "spies",
                    ]
                )
        elif category_choice == "Existing Background":
            examples = ChantryBackgroundRating.objects.filter(chantry=m, rating__lt=5)
            if m.points < 5:
                examples = examples.exclude(bg__property_name__in=["sanctum"])
            if m.points < 4:
                examples = examples.exclude(bg__property_name__in=["enhancement", "requisitions"])
            if m.points < 3:
                examples = examples.exclude(bg__property_name__in=["node", "resources"])
            if m.points < 2:
                examples = examples.exclude(
                    bg__property_name__in=[
                        "allies",
                        "arcane",
                        "backup",
                        "cult",
                        "elders",
                        "library",
                        "retainers",
                        "spies",
                    ]
                )
        else:
            examples = []

        return dropdown_options_response(examples, label_attr="__str__")


class ChantryBasicsView(LoginRequiredMixin, CreateView):
    """Wizard entry: the player names the chantry and chooses its total points."""

    model = Chantry
    form_class = ChantryCreateForm
    template_name = "locations/mage/chantry/basics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_create_directly"] = direct_create_chronicles(self.request.user).exists()
        return context

    def form_valid(self, form):
        chantry = form.save(commit=False)
        chantry.owner = self.request.user
        chantry.status = "Un"
        chantry.creation_status = 1
        chantry.save()
        form.save_m2m()
        apply_type_grants(chantry)
        self.object = chantry
        return HttpResponseRedirect(chantry.get_absolute_url())


class ChantryObjectMixin:
    """Wizard steps 1-2 are FormViews; resolve the chantry for permission checks."""

    def get_object(self, queryset=None):
        return get_object_or_404(Chantry, pk=self.kwargs["pk"])


class ChantryPointsView(EditPermissionMixin, ChantryObjectMixin, FormView):
    form_class = ChantryPointForm
    template_name = "locations/mage/chantry/locgen.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["pk"] = self.kwargs.get("pk")
        self.object = get_object_or_404(Chantry, pk=self.kwargs["pk"])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.object
        context["is_approved_user"] = True  # If we got here, user has permission
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Chantry, pk=kwargs.get("pk"))
        if obj.points < 2:
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().post(request, *args, **kwargs)


class ChantryIntegratedEffectsView(EditPermissionMixin, ChantryObjectMixin, FormView):
    form_class = ChantryEffectsForm
    template_name = "locations/mage/chantry/locgen.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["pk"] = self.kwargs.get("pk")
        self.object = get_object_or_404(Chantry, pk=self.kwargs["pk"])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.object
        context["is_approved_user"] = True  # If we got here, user has permission
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Chantry, pk=kwargs.get("pk"))
        if obj.current_ie_points() == 0:
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().post(request, *args, **kwargs)


class ChantryBackgroundView(EditPermissionMixin, ChantryObjectMixin, FormView):
    """Wizard steps 3-6: detail the chantry's next unfinished rating of one background.

    The character wizards' GenericBackgroundView resolves a Character and advances the
    character workflow, so it cannot serve a chantry. Here the new node, library, ally or
    sanctum takes the chantry's owner and chronicle; once no rating of the background is
    left unfinished the chantry moves to the next step. With nothing to detail, GET shows
    the step without a form and POST skips it.
    """

    background_name = ""
    template_name = "locations/mage/chantry/locgen.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.current_background = self.object.backgrounds.filter(
            bg__property_name=self.background_name, complete=False
        ).first()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if issubclass(self.get_form_class(), LinkedNPCForm):
            kwargs["obj"] = self.object
            kwargs["npc_role"] = self.background_name
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if "rank" in form.fields and self.current_background is not None:
            rating = self.current_background.rating
            form.fields["rank"].initial = rating
            form.fields["rank"].widget.attrs.update({"min": rating, "max": rating})
        return form

    def get_context_data(self, **kwargs):
        if self.current_background is None:
            kwargs["form"] = None
        context = super().get_context_data(**kwargs)
        context["object"] = self.object
        context["current_background"] = self.current_background
        return context

    def post(self, request, *args, **kwargs):
        if self.current_background is None:
            return self.next_step()
        return super().post(request, *args, **kwargs)

    def next_step(self):
        self.object.creation_status += 1
        self.object.save(update_fields=["creation_status"])
        return HttpResponseRedirect(self.object.get_absolute_url())

    def form_valid(self, form):
        background_object = form.save()
        background_object.owner = self.object.owner
        background_object.chronicle = self.object.chronicle
        background_object.status = "Sub"
        background_object.save()
        self.current_background.note = background_object.name
        self.current_background.url = background_object.get_absolute_url()
        self.current_background.linked_object = background_object
        self.current_background.complete = True
        self.current_background.save()
        if not self.object.backgrounds.filter(
            bg__property_name=self.background_name, complete=False
        ).exists():
            return self.next_step()
        return HttpResponseRedirect(self.object.get_absolute_url())


class ChantryNodeView(ChantryBackgroundView):
    background_name = "node"
    form_class = NodeForm


class ChantryLibrarysView(ChantryBackgroundView):
    background_name = "library"
    form_class = LibraryForm


class ChantryAlliesView(ChantryBackgroundView):
    background_name = "allies"
    form_class = LinkedNPCForm


class ChantrySanctumView(ChantryBackgroundView):
    background_name = "sanctum"
    form_class = SanctumForm


class ChantryCreationView(DictView):
    chargen_router = True
    view_mapping = {
        1: ChantryPointsView,  # Backgrounds
        2: ChantryIntegratedEffectsView,  # effects
        3: ChantryNodeView,  # Nodes
        4: ChantryLibrarysView,  # Libraries
        5: ChantryAlliesView,  # allies
        6: ChantrySanctumView,  # sanctum
    }
    model_class = Chantry
    key_property = "creation_status"
    default_redirect = ChantryDetailView

    def is_valid_key(self, obj, key):
        return key in self.view_mapping and obj.status in {"Un", "Rev"}

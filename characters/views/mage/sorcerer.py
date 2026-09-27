from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, FormView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.chargen.transitions import advance
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.mage.familiar import FamiliarForm
from characters.forms.mage.freebies import SorcererFreebiesForm
from characters.forms.mage.numina import (
    NuminaPathRatingFormSet,
    NuminaRitualForm,
    PsychicPathRatingFormSet,
)
from characters.forms.mage.sorcerer import SorcererBasicsForm, SorcererForm
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.human import Human
from characters.models.mage.fellowship import SorcererFellowship
from characters.models.mage.focus import Practice
from characters.models.mage.sorcerer import (
    LinearMagicPath,
    LinearMagicRitual,
    PathRating,
    Sorcerer,
)
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.chargen_mixins import ChargenStepMixin
from characters.views.core.extras import CharacterExtrasView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanDetailView,
    HumanFreebiesView,
    HumanLanguagesView,
    HumanSpecialtiesView,
)
from characters.views.mage.background_views import (
    CharacterChantryBackgroundView,
    MtAEnhancementView,
)
from characters.views.mage.mtahuman import MtAHumanAbilityView
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ScopedCreationFormMixin,
    ScopedEditFormMixin,
    SpecialUserMixin,
    SpendFreebiesPermissionMixin,
    XPApprovalMixin,
)
from core.permissions import PermissionManager
from core.views.generic import MultipleFormsetsMixin
from items.forms.mage.sorcerer_artifact import ArtifactCreateOrSelectForm
from locations.forms.mage.library import LibraryForm
from locations.forms.mage.node import NodeForm
from locations.forms.mage.sanctum import SanctumForm


class SorcererBasicsView(ScopedCreationFormMixin, MessageMixin, LoginRequiredMixin, CreateView):
    model = Sorcerer
    form_class = SorcererBasicsForm
    success_message = "Sorcerer created successfully."
    error_message = "Error creating sorcerer."
    template_name = "characters/mage/sorcerer/basics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["storyteller"] = PermissionManager.user_can_manage_creation(
            self.request.user, context["form"], request=self.request
        )
        return context

    def form_invalid(self, form):
        errors = form.errors
        if "casting_attribute" in errors:
            del errors["casting_attribute"]
        if "affinity_path" in errors:
            del errors["affinity_path"]

        if not errors:
            return self.form_valid(form)
        return super().form_invalid(form)

    def form_valid(self, form):
        # Handle foreign key fields from ChainedChoiceField string values
        casting_attr_pk = form.data.get("casting_attribute")
        affinity_path_pk = form.data.get("affinity_path")
        fellowship_pk = form.data.get("fellowship")

        if casting_attr_pk:
            form.instance.casting_attribute = get_object_or_404(Attribute, pk=casting_attr_pk)
        if affinity_path_pk:
            form.instance.affinity_path = get_object_or_404(LinearMagicPath, pk=affinity_path_pk)
        if fellowship_pk:
            form.instance.fellowship = get_object_or_404(SorcererFellowship, pk=fellowship_pk)
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SorcererUpdateView(ScopedEditFormMixin, EditPermissionMixin, MessageMixin, UpdateView):
    model = Sorcerer
    form_class = SorcererForm
    template_name = "characters/mage/sorcerer/form.html"
    success_message = "Sorcerer '{name}' updated successfully."
    error_message = "Error updating sorcerer."

    limited_form_class = LimitedHumanEditForm


class SorcererDetailView(XPApprovalMixin, HumanDetailView):
    model = Sorcerer
    template_name = "characters/mage/sorcerer/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SorcererAttributeView(HumanAttributeView):
    model = Sorcerer
    template_name = "characters/mage/sorcerer/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SorcererAbilityView(MtAHumanAbilityView):
    model = Sorcerer
    template_name = "characters/mage/sorcerer/chargen.html"

    primary = 11
    secondary = 7
    tertiary = 4


class SorcererBackgroundsView(HumanBackgroundsView):
    template_name = "characters/mage/sorcerer/chargen.html"


class SorcererPsychicView(ChargenStepMixin, SpecialUserMixin, MultipleFormsetsMixin, UpdateView):
    model = Sorcerer
    fields = []
    template_name = "characters/mage/sorcerer/chargen.html"
    formsets = {
        "numina_form": PsychicPathRatingFormSet,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        self.object.willpower = 5
        context = self.get_context_data()
        sorcerer = context["object"]
        numina_data = self.get_form_data("numina_form")
        for numina in numina_data:
            numina["path"] = get_object_or_404(LinearMagicPath, id=numina["path"])
            numina["rating"] = int(numina["rating"])
            if numina["rating"] > sorcerer.willpower // 2:
                pass
        total_numina = sum(x["rating"] for x in numina_data)
        if total_numina != 5:
            form.add_error(None, "Must choose exactly five levels of Numina")
            return self.form_invalid(form)
        for numina in numina_data:
            PathRating.objects.create(
                character=sorcerer,
                path=numina["path"],
                rating=numina["rating"],
                practice=None,
                ability=None,
            )
        advance(self.object, user=self.request.user)
        self.object.freebies = 21
        self.object.save()
        return super().form_valid(form)


class SorcererPathView(ChargenStepMixin, SpecialUserMixin, MultipleFormsetsMixin, UpdateView):
    model = Sorcerer
    fields = []
    template_name = "characters/mage/sorcerer/chargen.html"
    formsets = {
        "numina_form": NuminaPathRatingFormSet,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        sorcerer = context["object"]
        numina_data = self.get_form_data("numina_form")
        for numina in numina_data:
            numina["path"] = get_object_or_404(LinearMagicPath, id=numina["path"])
            numina["rating"] = int(numina["rating"])
            numina["practice"] = get_object_or_404(Practice, id=numina["practice"])
            numina["ability"] = get_object_or_404(Ability, id=numina["ability"])
        total_numina = sum(x["rating"] for x in numina_data)
        if total_numina != 5:
            form.add_error(None, "Must choose exactly five levels of Numina")
            return self.form_invalid(form)
        for numina in numina_data:
            PathRating.objects.create(
                character=sorcerer,
                path=numina["path"],
                rating=numina["rating"],
                practice=numina["practice"],
                ability=numina["ability"],
            )
        advance(self.object, user=self.request.user)
        self.object.willpower = 5
        self.object.freebies = 21
        self.object.save()
        return super().form_valid(form)


class SorcererRitualView(ChargenStepMixin, SpendFreebiesPermissionMixin, FormView):
    form_class = NuminaRitualForm
    template_name = "characters/mage/sorcerer/chargen.html"

    def get_object(self):
        """Return the Sorcerer object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Sorcerer, pk=self.kwargs.get("pk"))
        return self.object

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        human_pk = self.kwargs.get("pk")
        kwargs.update({"pk": human_pk})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        sorcerer = context["object"]
        if form.cleaned_data["select_or_create"]:
            # Create
            if (
                form.cleaned_data["name"] == ""
                or form.cleaned_data["description"] == ""
                or form.cleaned_data["path"] is None
            ):
                form.add_error(
                    None,
                    "Must select or create ritual",
                )
                return self.form_invalid(form)
            r = LinearMagicRitual.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                path=form.cleaned_data["path"],
                level=form.cleaned_data["level"],
            )
        else:
            # Select
            r = form.cleaned_data["select_ritual"]
            if r is None:
                form.add_error(
                    None,
                    "Must select or create ritual",
                )
                return self.form_invalid(form)
        p = r.path
        path_rating = sorcerer.path_rating(p)
        if r.level > path_rating:
            form.add_error(
                None,
                "Cannot learn ritual higher than path rating",
            )
            return self.form_invalid(form)
        if sorcerer.rituals.filter(path=p).count() >= path_rating:
            form.add_error(
                None,
                "One ritual per path dot at this stage",
            )
            return self.form_invalid(form)
        if r.level != 1 and not sorcerer.rituals.filter(path=p, level=r.level - 1).exists():
            form.add_error(
                None,
                "Must learn rituals in ascending level",
            )
            return self.form_invalid(form)
        sorcerer.rituals.add(r)
        if all(
            [
                sorcerer.rituals.filter(path=x).count() == sorcerer.path_rating(x)
                for x in sorcerer.paths.all()
            ]
        ):
            advance(sorcerer, user=self.request.user)
            sorcerer.save()
        return HttpResponseRedirect(context["object"].get_absolute_url())


class SorcererExtrasView(CharacterExtrasView):
    model = Sorcerer
    fields = [
        "date_of_birth",
        "apparent_age",
        "age",
        "description",
        "history",
        "goals",
        "notes",
        "public_info",
    ]
    template_name = "characters/mage/sorcerer/chargen.html"
    field_widget_attrs = {
        "public_info": {
            "placeholder": "This will be displayed to all players who look at your character, include Fame and anything else that would be publicly seen beyond physical description"
        }
    }


class SorcererFreebiesView(HumanFreebiesView):
    model = Sorcerer
    form_class = SorcererFreebiesForm
    template_name = "characters/mage/sorcerer/chargen.html"
    example_models = {
        **HumanFreebiesView.example_models,
        "Path": LinearMagicPath,
        "Select Ritual": LinearMagicRitual,
    }
    category_aliases = {"New Path": "Path", "Existing Path": "Path"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ritual_form"] = NuminaRitualForm(pk=self.object.id)
        return context

    def get_spending_kwargs(self, form):
        kwargs = super().get_spending_kwargs(form)
        if kwargs["category"] == "Path":
            for key, model in (("practice", Practice), ("ability", Ability)):
                value = form.cleaned_data.get(key)
                kwargs[key] = self.resolve_choice(model, value) if value else None
        elif kwargs["category"] == "Create Ritual":
            ritual_form = NuminaRitualForm(form.data, pk=self.object.pk)
            if not ritual_form.is_valid():
                raise ValidationError("Invalid ritual details")
            data = ritual_form.cleaned_data
            kwargs.update(
                ritual_name=data.get("name", ""),
                ritual_path=data.get("path"),
                ritual_level=data.get("level") or 1,
                ritual_description=data.get("description", ""),
            )
        return kwargs


class SorcererLanguagesView(HumanLanguagesView):
    model = Sorcerer
    template_name = "characters/mage/sorcerer/chargen.html"


class SorcererSpecialtiesView(HumanSpecialtiesView):
    model = Sorcerer
    template_name = "characters/mage/sorcerer/chargen.html"

    def get_specialties_needed(self):
        character = self.get_object()
        stats = list(Attribute.objects.all()) + list(
            Ability.objects.all().exclude(property_name="rituals")
        )
        stats = [x for x in stats if getattr(character, x.property_name, 0) >= 4] + [
            x
            for x in stats
            if getattr(character, x.property_name, 0) >= 1
            and x.property_name
            in [
                "arts",
                "athletics",
                "crafts",
                "firearms",
                "larceny",
                "melee",
                "academics",
                "esoterica",
                "lore",
                "politics",
                "science",
            ]
        ]
        stats.extend([x for x in LinearMagicPath.objects.all() if character.path_rating(x) >= 4])
        return [x.property_name for x in stats]


class SorcererAlliesView(GenericBackgroundView):
    primary_object_class = Sorcerer
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/mage/sorcerer/chargen.html"


class SorcererEnhancementView(MtAEnhancementView):
    template_name = "characters/mage/sorcerer/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["flaw"].required = True
        return form


class SorcererFamiliarView(GenericBackgroundView):
    primary_object_class = Sorcerer
    background_name = "familiar"
    form_class = FamiliarForm
    template_name = "characters/mage/sorcerer/chargen.html"

    def special_valid_action(self, background_object):
        background_object.freebies = 10 * self.current_background.rating
        background_object.status = "Un"
        background_object.save()
        return background_object


class SorcererLibraryView(GenericBackgroundView):
    primary_object_class = Sorcerer
    background_name = "library"
    form_class = LibraryForm
    template_name = "characters/mage/sorcerer/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        obj = get_object_or_404(self.primary_object_class, pk=self.kwargs.get("pk"))
        form.fields["name"].initial = self.current_background.note or f"{obj.name}'s Library"
        return form


class SorcererNodeView(GenericBackgroundView):
    primary_object_class = Sorcerer
    background_name = "node"
    form_class = NodeForm
    template_name = "characters/mage/sorcerer/chargen.html"


class SorcererArtifactView(ChargenStepMixin, EditPermissionMixin, FormView):
    form_class = ArtifactCreateOrSelectForm
    template_name = "characters/mage/sorcerer/chargen.html"

    def get_object(self):
        """Return the Sorcerer object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Sorcerer, pk=self.kwargs.get("pk"))
        return self.object

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Human, id=self.kwargs["pk"])
        context["current_artifact"] = (
            context["object"]
            .backgrounds.filter(bg__property_name="artifact", complete=False)
            .first()
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        a = form.save()
        obj = context["object"]
        a.owned_by.add(obj)
        a.owner = context["object"].owner
        a.chronicle = context["object"].chronicle
        a.status = "Sub"
        a.save()

        self.current_artifact.note = a.name
        self.current_artifact.url = a.get_absolute_url()
        self.current_artifact.complete = True
        self.current_artifact.save()

        if (
            context["object"]
            .backgrounds.filter(bg__property_name="artifact", complete=False)
            .count()
            == 0
        ):
            advance(context["object"], user=self.request.user)
        return HttpResponseRedirect(context["object"].get_absolute_url())

    def get_form(self, form_class=None):
        obj = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        self.current_artifact = obj.backgrounds.filter(
            bg__property_name="artifact", complete=False
        ).first()
        form = super().get_form(form_class)

        form.fields["name"].initial = self.current_artifact.note
        form.fields["rank"].widget.attrs.update(
            {
                "min": self.current_artifact.rating,
                "max": self.current_artifact.rating,
                "initial": self.current_artifact.rating,
            }
        )
        return form


class SorcererSanctumView(GenericBackgroundView):
    primary_object_class = Sorcerer
    background_name = "sanctum"
    form_class = SanctumForm
    template_name = "characters/mage/sorcerer/chargen.html"


class SorcererChantryView(CharacterChantryBackgroundView):
    primary_object_class = Sorcerer
    template_name = "characters/mage/sorcerer/chargen.html"


class SorcererCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()

    model_class = Sorcerer
    key_property = "creation_status"
    default_redirect = SorcererDetailView

from typing import Any

from characters.forms.core.backgroundform import BackgroundRatingFormSet
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.mage.familiar import FamiliarForm
from characters.forms.mage.freebies import SorcererFreebiesForm
from characters.forms.mage.numina import (
    NuminaPathRatingFormSet,
    NuminaRitualForm,
    PsychicPathRatingFormSet,
)
from characters.models.core.ability_block import Ability
from characters.models.core.archetype import Archetype
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.core.specialty import Specialty
from characters.models.mage.companion import Advantage
from characters.models.mage.fellowship import SorcererFellowship
from characters.models.mage.focus import Practice
from characters.models.mage.sorcerer import (
    LinearMagicPath,
    LinearMagicRitual,
    PathRating,
    Sorcerer,
)
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanDetailView,
)
from characters.views.mage.background_views import MtAEnhancementView
from characters.views.mage.mtahuman import MtAHumanAbilityView
from core.forms.language import HumanLanguageForm
from core.mixins import (
    DropdownOptionsView,
    EditPermissionMixin,
    JsonListView,
    MessageMixin,
    SpecialUserMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
)
from core.models import Language
from core.views.generic import MultipleFormsetsMixin
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView
from game.models import ObjectType
from items.forms.mage.sorcerer_artifact import ArtifactCreateOrSelectForm
from locations.forms.mage.chantry import ChantrySelectOrCreateForm
from locations.forms.mage.library import LibraryForm
from locations.forms.mage.node import NodeForm
from locations.forms.mage.sanctum import SanctumForm


class SorcererBasicsView(MessageMixin, LoginRequiredMixin, CreateView):
    model = Sorcerer
    success_message = "Sorcerer created successfully."
    error_message = "Error creating sorcerer."
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "fellowship",
        "affinity_path",
        "casting_attribute",
        "sorcerer_type",
        "chronicle",
        "image",
        "npc",
    ]
    template_name = "characters/mage/sorcerer/basics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storyteller"] = False
        if self.request.user.profile.is_st():
            context["storyteller"] = True
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["nature"].queryset = Archetype.objects.all().order_by("name")
        form.fields["demeanor"].queryset = Archetype.objects.all().order_by("name")
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["concept"].widget.attrs.update({"placeholder": "Enter concept here"})
        form.fields["image"].required = False
        form.fields["casting_attribute"].queryset = Attribute.objects.none()
        form.fields["affinity_path"].queryset = LinearMagicPath.objects.none()
        return form

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
        if form.data["casting_attribute"]:
            form.instance.casting_attribute = get_object_or_404(
                Attribute, pk=form.data["casting_attribute"]
            )
        if form.data["affinity_path"]:
            form.instance.affinity_path = get_object_or_404(
                LinearMagicPath, pk=form.data["affinity_path"]
            )
        form.instance.owner = self.request.user
        return super().form_valid(form)


class LoadAttributesView(DropdownOptionsView):
    """AJAX view to load favored attributes for a sorcerer fellowship."""

    def get_queryset(self):
        fellowship_id = self.request.GET.get("fellowship")
        sf = get_object_or_404(SorcererFellowship, id=fellowship_id)
        return sf.favored_attributes.all()


class LoadAffinitiesView(DropdownOptionsView):
    """AJAX view to load favored paths (affinities) for a sorcerer fellowship."""

    def get_queryset(self):
        fellowship_id = self.request.GET.get("fellowship")
        sf = get_object_or_404(SorcererFellowship, id=fellowship_id)
        return sf.favored_paths.all()


class SorcererUpdateView(EditPermissionMixin, UpdateView):
    model = Sorcerer
    fields = "__all__"
    template_name = "characters/mage/sorcerer/form.html"
    success_message = "Sorcerer updated successfully."
    error_message = "Error updating sorcerer."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SorcererDetailView(HumanDetailView):
    model = Sorcerer
    template_name = "characters/mage/sorcerer/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoadExamplesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        from core.ajax import dropdown_options_response

        category_choice = request.GET.get("category")
        object_id = request.GET.get("object")
        m = get_object_or_404(Sorcerer, pk=object_id)

        category_choice = request.GET.get("category")
        if category_choice == "Attribute":
            examples = Attribute.objects.all()
            examples = [x for x in examples if getattr(m, x.property_name, 0) < 5]
        elif category_choice == "Ability":
            examples = Ability.objects.order_by("name")
            examples = [x for x in examples if hasattr(m, x.property_name)]
            examples = [x for x in examples if isinstance(getattr(m, x.property_name), int)]
            examples = [x for x in examples if getattr(m, x.property_name, 0) < 4]
        elif category_choice == "New Background":
            examples = Background.objects.filter(property_name__in=m.allowed_backgrounds).order_by(
                "name"
            )
        elif category_choice == "Existing Background":
            examples = [x for x in BackgroundRating.objects.filter(char=m, rating__lt=4)]
        elif category_choice == "MeritFlaw":
            companion, _ = ObjectType.objects.get_or_create(
                name="companion", defaults={"type": "char", "gameline": "mta"}
            )
            examples = MeritFlaw.objects.filter(allowed_types=companion)
            if m.total_flaws() <= 0:
                examples = examples.exclude(max_rating__lt=min(0, -7 - m.total_flaws()))
            examples = examples.exclude(min_rating__gt=m.freebies)
        elif category_choice == "New Path":
            if m.sorcerer_type == "hedge_mage":
                examples = LinearMagicPath.objects.filter(numina_type="hedge_magic")
            else:
                examples = LinearMagicPath.objects.filter(numina_type="psychic")
            examples = examples.exclude(id__in=[x.id for x in m.paths.all()])
        elif category_choice == "Existing Path":
            if m.sorcerer_type == "hedge_mage":
                examples = LinearMagicPath.objects.filter(numina_type="hedge_magic")
            else:
                examples = LinearMagicPath.objects.filter(numina_type="psychic")
            examples = examples.filter(id__in=[x.id for x in examples if 5 > m.path_rating(x) > 0])
        elif category_choice == "Select Ritual":
            rituals = Q()

            for path in m.pathrating_set.all():
                ritual_levels = list(
                    m.rituals.filter(path=path.path).values_list("level", flat=True)
                )
                if ritual_levels:
                    maximum_level_ritual = max(ritual_levels)
                else:
                    maximum_level_ritual = 0

                rituals |= Q(
                    **{
                        "path": path.path,
                        "level__lte": min([path.rating, maximum_level_ritual + 1]),
                    }
                )

            examples = LinearMagicRitual.objects.filter(rituals).exclude(
                id__in=[x.id for x in m.rituals.all()]
            )
        else:
            examples = []

        return dropdown_options_response(examples, label_attr="__str__")


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


class GetPracticeAbilitiesView(JsonListView):
    """AJAX view to get abilities for a practice."""

    def get_items(self):
        practice_id = self.request.GET.get("practice_id")
        prac = get_object_or_404(Practice, id=practice_id)
        abilities = prac.abilities.all().order_by("name")
        return [{"id": ability.id, "name": ability.name} for ability in abilities]


class SorcererPsychicView(SpecialUserMixin, MultipleFormsetsMixin, UpdateView):
    model = Sorcerer
    fields = []
    template_name = "characters/mage/sorcerer/chargen.html"
    formsets = {
        "numina_form": PsychicPathRatingFormSet,
    }

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Sorcerer, pk=kwargs.get("pk"))
        if obj.sorcerer_type == "hedge_mage":
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

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
        self.object.creation_status += 3
        self.object.freebies = 21
        self.object.save()
        return super().form_valid(form)


class SorcererPathView(SpecialUserMixin, MultipleFormsetsMixin, UpdateView):
    model = Sorcerer
    fields = []
    template_name = "characters/mage/sorcerer/chargen.html"
    formsets = {
        "numina_form": NuminaPathRatingFormSet,
    }

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Sorcerer, pk=kwargs.get("pk"))
        if obj.sorcerer_type != "hedge_mage":
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

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
        self.object.creation_status += 1
        if self.object.sorcerer_type != "hedge_mage":
            self.object.creation_status += 1
        self.object.willpower = 5
        self.object.freebies = 21
        self.object.save()
        return super().form_valid(form)


class SorcererRitualView(EditPermissionMixin, FormView):
    form_class = NuminaRitualForm
    template_name = "characters/mage/sorcerer/chargen.html"

    def get_object(self):
        """Return the Sorcerer object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Sorcerer, pk=self.kwargs.get("pk"))
        return self.object

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Sorcerer, pk=kwargs.get("pk"))
        if obj.sorcerer_type != "hedge_mage":
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

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
        if r.level != 1 and sorcerer.rituals.filter(path=p, level=r.level - 1).count() == 0:
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
            sorcerer.creation_status += 1
            sorcerer.save()
        return HttpResponseRedirect(context["object"].get_absolute_url())


class SorcererExtrasView(SpecialUserMixin, UpdateView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date_of_birth"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["description"].widget.attrs.update(
            {
                "placeholder": "Describe your character's physical appeareance. Be detailed, this will be visible to other players."
            }
        )
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe character history/backstory. Include information about their childhood, when and how they Awakened, and how they've interacted with mage society since, particularly mentioning important backgrounds."
            }
        )
        form.fields["goals"].widget.attrs.update(
            {
                "placeholder": "Describe your character's long and short term goals, whether personal, professional, or magical."
            }
        )
        form.fields["notes"].widget.attrs.update({"placeholder": "Notes"})
        form.fields["public_info"].widget.attrs.update(
            {
                "placeholder": "This will be displayed to all players who look at your character, include Fame and anything else that would be publicly seen beyond physical description"
            }
        )
        return form


class SorcererFreebiesView(SpecialUserMixin, UpdateView):
    model = Sorcerer
    form_class = SorcererFreebiesForm
    template_name = "characters/mage/sorcerer/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ritual_form"] = NuminaRitualForm(pk=self.object.id)
        return context

    def form_valid(self, form):
        if form.data["category"] == "-----":
            form.add_error(None, "Must Choose Freebie Expenditure Type")
            return super().form_invalid(form)
        elif form.data["category"] == "MeritFlaw" and (
            form.data["example"] == "" or form.data["value"] == ""
        ):
            form.add_error(None, "Must Choose Merit/Flaw and rating")
            return super().form_invalid(form)
        elif (
            form.data["category"]
            in [
                "Attribute",
                "Ability",
                "New Background",
                "Existing Background",
                "Path",
                "Ritual",
            ]
            and form.data["example"] == ""
        ):
            form.add_error(None, "Must Choose Trait")
            return super().form_invalid(form)
        trait_type = form.data["category"].lower()
        if "background" in trait_type:
            trait_type = "background"
        if "path" in trait_type:
            trait_type = "path"
        if "ritual" in trait_type:
            trait_type = "ritual"
        cost = self.object.freebie_cost(trait_type)
        if cost == "rating":
            cost = int(form.data["value"])
        if cost > self.object.freebies:
            form.add_error(None, f"Not Enough Freebies! {trait_type} costs {cost}")
            return super().form_invalid(form)
        if form.data["category"] == "Attribute":
            trait = get_object_or_404(Attribute, pk=form.data["example"])
            value = getattr(self.object, trait.property_name) + 1
            self.object.add_attribute(trait.property_name)
            self.object.freebies -= cost
            trait = trait.name
        elif form.data["category"] == "Ability":
            trait = get_object_or_404(Ability, pk=form.data["example"])
            value = getattr(self.object, trait.property_name) + 1
            self.object.add_ability(trait.property_name)
            self.object.freebies -= cost
            trait = trait.name
        elif form.data["category"] == "New Background":
            trait = get_object_or_404(Background, pk=form.data["example"])
            cost *= trait.multiplier
            value = 1
            BackgroundRating.objects.create(
                bg=trait, rating=1, char=self.object, note=form.data["note"]
            )
            self.object.freebies -= cost
            trait = str(trait)
            if form.data["note"]:
                trait += f" ({form.data['note']})"
        elif form.data["category"] == "Existing Background":
            trait = get_object_or_404(BackgroundRating, pk=form.data["example"])
            cost *= trait.bg.multiplier
            value = trait.rating + 1
            trait.rating += 1
            trait.save()
            self.object.freebies -= cost
            trait = str(trait)
        elif form.data["category"] == "Willpower":
            trait = "Willpower"
            value = self.object.willpower + 1
            self.object.add_willpower()
            self.object.freebies -= cost
        elif form.data["category"] == "MeritFlaw":
            trait = get_object_or_404(MeritFlaw, pk=form.data["example"])
            value = int(form.data["value"])
            self.object.add_mf(trait, value)
            self.object.freebies -= cost
            trait = trait.name
        elif "Path" in form.data["category"]:
            trait = get_object_or_404(LinearMagicPath, pk=form.data["example"])
            value = self.object.path_rating(trait) + 1
            prac = form.data.get("practice", None)
            if prac != "":
                prac = get_object_or_404(Practice, pk=prac)
            else:
                prac = None
            ability = form.data.get("ability", None)
            if ability != "":
                ability = get_object_or_404(Ability, pk=ability)
            else:
                ability = None
            self.object.add_path(trait, prac, ability)
            self.object.freebies -= cost
            trait = trait.name
            if prac is not None:
                trait += f"({prac.name}, {ability.name})"
        elif form.data["category"] == "Create Ritual":
            name = form.data["name"]
            path = get_object_or_404(LinearMagicPath, pk=int(form.data["path"]))
            level = int(form.data["level"])
            description = form.data["description"]
            trait = LinearMagicRitual.objects.create(
                name=name, path=path, level=level, description=description
            )
            value = cost
            self.object.add_ritual(trait)
            self.object.freebies -= cost
            trait = trait.name
        elif form.data["category"] == "Select Ritual":
            trait = get_object_or_404(LinearMagicRitual, pk=form.data["example"])
            value = cost
            self.object.add_ritual(trait)
            self.object.freebies -= cost
            trait = trait.name
        if form.data["category"] != "MeritFlaw":
            self.object.spent_freebies.append(
                self.object.freebie_spend_record(trait, trait_type, value, cost=cost)
            )
        else:
            self.object.spent_freebies.append(
                self.object.freebie_spend_record(trait, trait_type, value, cost=cost)
            )
        if self.object.freebies == 0:
            self.object.creation_status += 1
            if "Language" not in self.object.merits_and_flaws.values_list("name", flat=True):
                self.object.creation_status += 1
                english, _ = Language.objects.get_or_create(name="English")
                self.object.languages.add(english)
                for step in [
                    "node",
                    "library",
                    "familiar",
                    "artifact",
                    "enhancement",
                    "sanctum",
                    "allies",
                ]:
                    bg, _ = Background.objects.get_or_create(
                        property_name=step,
                        defaults={"name": step.replace("_", " ").title()},
                    )
                    if (
                        BackgroundRating.objects.filter(
                            bg=bg,
                            char=self.object,
                            complete=False,
                        ).count()
                        == 0
                    ):
                        self.object.creation_status += 1
                    else:
                        self.object.save()
                        break
                    self.object.save()
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.data["category"] == "-----":
            form.add_error(None, "Must Choose Freebie Expenditure Type")
            return super().form_invalid(form)
        elif form.data["category"] == "MeritFlaw" and (
            form.data["example"] == "" or form.data["value"] == ""
        ):
            form.add_error(None, "Must Choose Merit/Flaw and rating")
            return super().form_invalid(form)
        elif (
            form.data["category"] in ["Attribute", "Ability", "Background"]
            and form.data["example"] == ""
        ):
            form.add_error(None, "Must Choose Trait")
            return super().form_invalid(form)
        return self.form_valid(form)


class SorcererLanguagesView(EditPermissionMixin, FormView):
    form_class = HumanLanguageForm
    template_name = "characters/mage/sorcerer/chargen.html"

    def get_object(self):
        """Return the Human object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        return self.object

    # Overriding `get_form_kwargs` to pass custom arguments to the form
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        human_pk = self.kwargs.get("pk")
        human = get_object_or_404(Human, pk=human_pk)
        num_languages = human.num_languages()
        kwargs.update({"pk": human_pk, "num_languages": int(num_languages)})
        return kwargs

    # Overriding `form_valid` to handle saving the data
    def form_valid(self, form):
        # Get the human instance from the pased `pk`
        human_pk = self.kwargs.get("pk")
        human = get_object_or_404(Human, pk=human_pk)

        for key, value in form.cleaned_data.items():
            if key.startswith("language_"):
                language_name = value
                if language_name:
                    language, _ = Language.objects.get_or_create(name=language_name)
                    human.languages.add(language)
        human.creation_status += 1
        human.save()
        return HttpResponseRedirect(human.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context


class SorcererSpecialtiesView(EditPermissionMixin, FormView):
    form_class = SpecialtiesForm
    template_name = "characters/mage/sorcerer/chargen.html"

    def get_object(self):
        """Return the Sorcerer object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Sorcerer, id=self.kwargs["pk"])
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        companion = get_object_or_404(Sorcerer, id=self.kwargs["pk"])
        kwargs["object"] = companion
        stats = list(Attribute.objects.all()) + list(
            Ability.objects.all().exclude(property_name="rituals")
        )
        stats = [x for x in stats if getattr(companion, x.property_name, 0) >= 4] + [
            x
            for x in stats
            if getattr(companion, x.property_name, 0) >= 1
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
        stats.extend([x for x in LinearMagicPath.objects.all() if companion.path_rating(x) >= 4])
        kwargs["specialties_needed"] = [x.property_name for x in stats]
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        companion = context["object"]
        for field in form.fields:
            spec = Specialty.objects.get_or_create(name=form.data[field], stat=field)[0]
            companion.specialties.add(spec)
        companion.status = "Sub"
        companion.save()
        return HttpResponseRedirect(companion.get_absolute_url())


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


class SorcererArtifactView(EditPermissionMixin, FormView):
    form_class = ArtifactCreateOrSelectForm
    template_name = "characters/mage/sorcerer/chargen.html"

    potential_skip = [
        "enhancement",
        "sanctum",
        "allies",
    ]

    def get_object(self):
        """Return the Sorcerer object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Sorcerer, pk=self.kwargs.get("pk"))
        return self.object

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Sorcerer, pk=kwargs.get("pk"))
        if not obj.backgrounds.filter(bg__property_name="artifact", complete=False).exists():
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = Human.objects.get(id=self.kwargs["pk"])
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
            context["object"].creation_status += 1
            context["object"].save()
            for step in self.potential_skip:
                if (
                    context["object"]
                    .backgrounds.filter(bg__property_name=step, complete=False)
                    .count()
                    == 0
                ):
                    context["object"].creation_status += 1
                else:
                    context["object"].save()
                    break
            context["object"].save()
        return HttpResponseRedirect(context["object"].get_absolute_url())

    def get_form(self, form_class=None):
        obj = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        self.current_artifact = obj.backgrounds.filter(
            bg__property_name="artifact", complete=False
        ).first()
        form = super().get_form(form_class)

        form.artifact_form.fields["name"].initial = self.current_artifact.note
        form.artifact_form.fields["rank"].widget.attrs.update(
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


class SorcererChantryView(GenericBackgroundView):
    primary_object_class = Sorcerer
    background_name = "chantry"
    form_class = ChantrySelectOrCreateForm
    template_name = "characters/mage/sorcerer/chargen.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = get_object_or_404(self.primary_object_class, pk=self.kwargs["pk"])
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.chantry_creation_form.fields["total_points"].initial = self.current_background.rating
        form.chantry_creation_form.fields["total_points"].widget.attrs.update(
            {
                "min": self.current_background.rating,
                "max": self.current_background.rating,
            }
        )
        return form


class SorcererCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: SorcererAttributeView,
        2: SorcererAbilityView,
        3: SorcererBackgroundsView,
        4: SorcererPsychicView,
        5: SorcererPathView,
        6: SorcererRitualView,
        7: SorcererExtrasView,
        8: SorcererFreebiesView,
        9: SorcererLanguagesView,
        10: SorcererNodeView,
        11: SorcererLibraryView,
        12: SorcererFamiliarView,
        13: SorcererArtifactView,
        14: SorcererEnhancementView,
        15: SorcererSanctumView,
        16: SorcererAlliesView,
        17: SorcererChantryView,
        18: SorcererSpecialtiesView,
    }

    model_class = Sorcerer
    key_property = "creation_status"
    default_redirect = SorcererDetailView

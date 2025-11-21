from typing import Any

from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db import transaction

from characters.forms.core.ally import AllyForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.forms.mage.familiar import FamiliarForm
from characters.forms.mage.freebies import MageFreebiesForm
from characters.forms.mage.mage import MageCreationForm
from characters.forms.mage.practiceform import PracticeRatingFormSet
from characters.forms.mage.rote import RoteCreationForm
from characters.forms.mage.xp import MageXPForm
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.core.specialty import Specialty
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Practice, SpecializedPractice, Tenet
from characters.models.mage.mage import Mage, PracticeRating, ResRating
from characters.models.mage.resonance import Resonance
from characters.models.mage.rote import Rote
from characters.models.mage.sphere import Sphere
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanDetailView,
    HumanFreebieFormPopulationView,
    HumanFreebiesView,
    HumanLanguagesView,
    HumanSpecialtiesView,
)
from characters.views.mage.background_views import MtAEnhancementView
from characters.views.mage.mtahuman import MtAHumanAbilityView
from core.forms.language import HumanLanguageForm
from core.models import Language
from core.mixins import ViewPermissionMixin, EditPermissionMixin, SpendFreebiesPermissionMixin, SpendXPPermissionMixin
from core.views.approved_user_mixin import SpecialUserMixin
from core.views.message_mixin import MessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from core.widgets import AutocompleteTextInput
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import ValidationError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView
from game.models import ObjectType
from items.forms.mage.wonder import WonderForm
from items.models.core.item import ItemModel
from locations.forms.mage.chantry import ChantrySelectOrCreateForm
from locations.forms.mage.library import LibraryForm
from locations.forms.mage.node import NodeForm
from locations.forms.mage.sanctum import SanctumForm


def load_factions(request):
    affiliation_id = request.GET.get("affiliation")
    factions = MageFaction.objects.filter(parent=affiliation_id).order_by("name")
    return render(
        request,
        "characters/mage/mage/load_faction_dropdown_list.html",
        {"factions": factions},
    )


def load_subfactions(request):
    faction_id = request.GET.get("faction")
    subfactions = MageFaction.objects.filter(parent=faction_id).order_by("name")
    return render(
        request,
        "characters/mage/mage/load_subfaction_dropdown_list.html",
        {"subfactions": subfactions},
    )


def load_mf_ratings(request):
    mf_id = request.GET.get("mf")
    ratings = MeritFlaw.objects.get(pk=mf_id).ratings
    return render(
        request,
        "characters/mage/mage/load_mf_rating_dropdown_list.html",
        {"ratings": ratings},
    )


class MageFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Mage
    template_name = "characters/core/human/load_examples_dropdown_list.html"

    def category_method_map(self):
        d = super().category_method_map()
        d.update(
            {
                "Sphere": self.sphere_options,
                "Resonance": self.resonance_options,
                "Tenet": self.tenet_options,
                "Practice": self.practice_options,
                "Arete": self.practice_options,
            }
        )
        return d

    def sphere_options(self):
        return [
            x
            for x in Sphere.objects.all().order_by("name")
            if getattr(self.character, x.property_name, 0) < self.character.arete
            and hasattr(self.character, x.property_name)
        ]

    def resonance_options(self):
        return Resonance.objects.all()

    def tenet_options(self):
        metaphysical_tenet_q = (
            Q(id=self.character.metaphysical_tenet.id)
            if self.character.metaphysical_tenet
            else Q()
        )
        personal_tenet_q = (
            Q(id=self.character.personal_tenet.id)
            if self.character.personal_tenet
            else Q()
        )
        ascension_tenet_q = (
            Q(id=self.character.ascension_tenet.id)
            if self.character.ascension_tenet
            else Q()
        )
        other_tenets_q = Q(
            id__in=self.character.other_tenets.all().values_list("id", flat=True)
        )
        related_tenets_q = (
            metaphysical_tenet_q | personal_tenet_q | ascension_tenet_q | other_tenets_q
        )
        return Tenet.objects.exclude(related_tenets_q)

    def practice_options(self):
        examples = Practice.objects.exclude(
            polymorphic_ctype__model="specializedpractice"
        ).exclude(polymorphic_ctype__model="corruptedpractice")
        spec = SpecializedPractice.objects.filter(faction=self.character.faction)
        if spec.count() > 0:
            examples = examples.exclude(
                id__in=[x.parent_practice.id for x in spec]
            ) | Practice.objects.filter(id__in=[x.id for x in spec])
        ids = PracticeRating.objects.filter(mage=self.character, rating=5).values_list(
            "practice__id", flat=True
        )
        examples = examples.exclude(pk__in=ids).order_by("name")
        return [
            x
            for x in examples
            if (
                sum(
                    [
                        getattr(self.character, abb.property_name)
                        for abb in x.abilities.all()
                    ]
                )
                / 2
                >= self.character.practice_rating(x) + 1
            )
        ]


class LoadXPExamplesView(View):
    template_name = "characters/core/human/load_examples_dropdown_list.html"

    def get(self, request, *args, **kwargs):
        category_choice = request.GET.get("category")
        object_id = request.GET.get("object")
        self.character = Mage.objects.get(pk=object_id)
        examples = []

        if category_choice == "Attribute":
            filtered_attributes = [
                attribute
                for attribute in Attribute.objects.all()
                if getattr(self.character, attribute.property_name) < 5
            ]
            filtered_for_xp_cost = [
                x
                for x in filtered_attributes
                if self.character.xp_cost(
                    "attribute",
                    getattr(self.character, x.property_name),
                )
                <= self.character.xp
            ]
            examples = filtered_for_xp_cost
        elif category_choice == "Ability":
            filtered_abilities = [
                ability
                for ability in Ability.objects.filter(
                    property_name__in=self.character.talents
                    + self.character.skills
                    + self.character.knowledges
                )
                if getattr(self.character, ability.property_name) < 5
            ]
            filtered_for_xp_cost = [
                x
                for x in filtered_abilities
                if self.character.xp_cost(
                    "ability",
                    getattr(self.character, x.property_name),
                )
                <= self.character.xp
            ]
            examples = filtered_for_xp_cost
        elif category_choice == "New Background":
            examples = Background.objects.filter(
                property_name__in=self.character.allowed_backgrounds
            ).order_by("name")
        elif category_choice == "Existing Background":
            bgs = self.character.backgrounds.filter(rating__lt=5)
            filtered_for_xp_cost = [
                x
                for x in bgs
                if self.character.xp_cost(
                    "background",
                    x.rating,
                )
                <= self.character.xp
            ]
            examples = filtered_for_xp_cost
        elif category_choice == "MeritFlaw":
            mage = ObjectType.objects.get(name="mage")
            examples = MeritFlaw.objects.filter(allowed_types=mage, max_rating__gte=0)
            examples = [
                x for x in examples if self.character.mf_rating(x) != x.max_rating
            ]
            examples = [
                x
                for x in examples
                if (
                    min([y for y in x.get_ratings() if y > self.character.mf_rating(x)])
                    - self.character.mf_rating(x)
                )
                * 3
                <= self.character.xp
            ]
        elif category_choice == "Sphere":
            filtered_spheres = [
                sphere
                for sphere in Sphere.objects.all()
                if getattr(self.character, sphere.property_name) < self.character.arete
            ]
            filtered_for_xp_cost = [
                x
                for x in filtered_spheres
                if self.character.xp_cost(
                    self.character.sphere_to_trait_type(x.property_name),
                    getattr(self.character, x.property_name),
                )
                <= self.character.xp
            ]
            examples = filtered_for_xp_cost
        elif category_choice == "Tenet":
            examples = Tenet.objects.exclude(
                id__in=[
                    self.character.metaphysical_tenet.id,
                    self.character.personal_tenet.id,
                    self.character.ascension_tenet.id,
                ]
            )
            examples = examples.exclude(
                id__in=[x.id for x in self.character.other_tenets.all()]
            )
        elif category_choice == "Remove Tenet":
            examples = self.character.other_tenets.all()
            types = [x.tenet_type for x in examples]
            if "met" in types:
                examples |= Tenet.objects.filter(
                    id__in=[self.character.metaphysical_tenet.id]
                )
            if "asc" in types:
                examples |= Tenet.objects.filter(
                    id__in=[self.character.ascension_tenet.id]
                )
            if "per" in types:
                examples |= Tenet.objects.filter(
                    id__in=[self.character.personal_tenet.id]
                )
        elif category_choice == "Practice":
            examples = Practice.objects.exclude(
                polymorphic_ctype__model="specializedpractice"
            ).exclude(polymorphic_ctype__model="corruptedpractice")
            spec = SpecializedPractice.objects.filter(faction=self.character.faction)
            if spec.count() > 0:
                examples = examples.exclude(
                    id__in=[x.parent_practice.id for x in spec]
                ) | Practice.objects.filter(id__in=[x.id for x in spec])

            ids = PracticeRating.objects.filter(
                mage=self.character, rating=5
            ).values_list("practice__id", flat=True)

            filtered_practices = examples.exclude(pk__in=ids).order_by("name")
            examples = [
                x
                for x in filtered_practices
                if self.character.xp_cost(
                    "practice",
                    self.character.practice_rating(x),
                )
                <= self.character.xp
            ]
            examples = [
                x
                for x in examples
                if (
                    sum(
                        [
                            getattr(self.character, abb.property_name)
                            for abb in x.abilities.all()
                        ]
                    )
                    / 2
                    > self.character.practice_rating(x) + 1
                )
            ]
        return render(request, self.template_name, {"examples": examples})


def get_abilities(request):
    object_id = request.GET.get("object")
    object = Human.objects.get(id=object_id)
    practice_id = request.GET.get("practice_id")
    prac = Practice.objects.get(id=practice_id)
    abilities = prac.abilities.all().order_by("name")
    abilities = [x for x in abilities if getattr(object, x.property_name) > 0]
    abilities_list = [{"id": "", "name": "--------"}]  # Empty option
    abilities_list += [
        {"id": ability.id, "name": ability.name} for ability in abilities
    ]
    return JsonResponse(abilities_list, safe=False)


class MageDetailView(HumanDetailView):
    model = Mage
    template_name = "characters/mage/mage/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["items_owned"] = ItemModel.objects.filter(owned_by=self.object)
        context["is_approved_user"] = True  # If we got here, user has permission
        if "form" not in context:
            context["form"] = MageXPForm(character=self.object)
        context["rote_form"] = RoteCreationForm(instance=self.object)
        context["spec_form"] = SpecialtiesForm(
            object=self.object, specialties_needed=self.object.needed_specialties()
        )
        context["resonance"] = ResRating.objects.filter(mage=self.object).order_by(
            "resonance__name"
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        form = MageXPForm(request.POST, request.FILES, character=self.object)
        rote_form = RoteCreationForm(request.POST, instance=self.object)
        form_errors = False
        if "spend_xp" in form.data.keys():
            if form.is_valid():
                category = form.cleaned_data["category"]
                example = form.cleaned_data["example"]
                value = form.cleaned_data["value"]
                note = form.cleaned_data["note"]
                pooled = form.cleaned_data["pooled"]
                image_field = form.cleaned_data["image_field"]
                resonance = form.cleaned_data["resonance"]
                if category == "Image":
                    self.object.image = image_field
                    self.object.save()
                if category not in ["Image", "Rote"]:
                    if category == "Attribute":
                        trait = example.name
                        trait_type = "attribute"
                        value = getattr(self.object, example.property_name)
                        cost = self.object.xp_cost("attribute", value)
                        d = self.object.xp_spend_record(
                            trait, trait_type, value + 1, cost=cost
                        )
                    elif category == "Ability":
                        trait = example.name
                        trait_type = "ability"
                        value = getattr(self.object, example.property_name)
                        cost = self.object.xp_cost("ability", value)
                        d = self.object.xp_spend_record(
                            trait, trait_type, value + 1, cost=cost
                        )
                    elif category == "New Background":
                        if note:
                            trait = example.name + f" ({note})"
                        else:
                            trait = example.name
                        trait_type = "new background"
                        value = 1
                        cost = self.object.xp_cost("new background", value)
                        d = self.object.xp_spend_record(
                            trait, trait_type, value, cost=cost
                        )
                    elif category == "Existing Background":
                        trait = example.bg.name + f" ({example.note})"
                        trait_type = "background"
                        value = example.rating
                        cost = self.object.xp_cost("background", value)
                        d = self.object.xp_spend_record(
                            trait, trait_type, value + 1, cost=cost
                        )
                    elif category == "Willpower":
                        trait = "Willpower"
                        trait_type = "willpower"
                        value = self.object.willpower
                        cost = self.object.xp_cost("willpower", value)
                        d = self.object.xp_spend_record(
                            trait, trait_type, value + 1, cost=cost
                        )
                    elif category == "MeritFlaw":
                        current_rating = self.object.mf_rating(example)
                        trait = example.name
                        trait_type = "meritflaw"
                        cost = self.object.xp_cost("meritflaw", value - current_rating)
                        d = self.object.xp_spend_record(
                            trait, trait_type, value, cost=cost
                        )
                    elif category == "Sphere":
                        trait = example.name
                        trait_type = "sphere"
                        value = getattr(self.object, example.property_name) + 1
                        cost = self.object.xp_cost(
                            self.object.sphere_to_trait_type(example.property_name),
                            getattr(self.object, example.property_name),
                        )
                        d = self.object.xp_spend_record(
                            trait, trait_type, value, cost=cost
                        )
                    elif category == "Rote Points":
                        trait = "Rote Points"
                        trait_type = "rotes"
                        cost = self.object.xp_cost("rotes", 1)
                        value = (
                            self.object.total_effects() + self.object.rote_points + 3
                        )
                        d = self.object.xp_spend_record(
                            trait, trait_type, value, cost=cost
                        )
                    elif category == "Resonance":
                        trait = f"Resonance ({resonance})"
                        r = Resonance.objects.get_or_create(name=resonance)[0]
                        trait_type = "resonance"
                        value = self.object.resonance_rating(r)
                        cost = self.object.xp_cost("resonance", value)
                        # Use atomic transaction method to prevent race conditions
                        try:
                            d = self.object.spend_xp(
                                trait_name=trait,
                                trait_display=trait,
                                cost=cost,
                                category=trait_type
                            )
                        except ValidationError as e:
                            messages.error(request, str(e))
                            context["form"] = form
                            form_errors = True
                    elif category == "Tenet":
                        trait = example.name
                        trait_type = "tenet"
                        cost = self.object.xp_cost("tenet", 1)
                        d = self.object.xp_spend_record(trait, trait_type, 0, cost=cost)
                    elif category == "Remove Tenet":
                        trait = "Remove " + example.name
                        trait_type = "remove tenet"
                        cost = self.object.xp_cost(
                            "remove tenet", self.object.other_tenets.count() + 3
                        )
                        d = self.object.xp_spend_record(
                            trait, trait_type, None, cost=cost
                        )
                    elif category == "Practice":
                        trait = example.name
                        trait_type = "practice"
                        value = self.object.practice_rating(example)
                        cost = self.object.xp_cost("practice", value)
                        d = self.object.xp_spend_record(
                            trait, trait_type, value + 1, cost=cost
                        )
                    elif category == "Arete":
                        trait = "Arete"
                        trait_type = "arete"
                        value = self.object.arete
                        cost = self.object.xp_cost("arete", value)
                        d = self.object.xp_spend_record(
                            trait, trait_type, value + 1, cost=cost
                        )
                    if d not in self.object.spent_xp:
                        # Use atomic transaction method to prevent race conditions
                        try:
                            # Recreate the record using spend_xp for atomicity
                            d = self.object.spend_xp(
                                trait_name=d['value'],
                                trait_display=d['trait'],
                                cost=cost,
                                category=trait_type
                            )
                        except ValidationError as e:
                            messages.error(request, str(e))
                            context["form"] = form
                            form_errors = True
                    else:
                        form.add_error(
                            None, "Wait for trait to be approved before buying again!"
                        )
                        context["form"] = form
                        form_errors = True
                elif category == "Rote":
                    if rote_form.is_valid():
                        if (
                            not rote_form.cleaned_data["select_or_create_rote"]
                            and not rote_form.cleaned_data["rote_options"]
                        ):
                            rote_form.add_error(None, "Must create or select a rote")
                            return render(
                                request, self.template_name, self.get_context_data()
                            )
                        if rote_form.cleaned_data["select_or_create_rote"]:
                            if (
                                not rote_form.cleaned_data["select_or_create_effect"]
                                and not rote_form.cleaned_data["effect_options"]
                            ):
                                rote_form.add_error(
                                    None, "Must create or select an effect"
                                )
                                return render(
                                    request, self.template_name, self.get_context_data()
                                )
                            if not rote_form.cleaned_data["name"]:
                                rote_form.add_error(None, "Must choose rote name")
                                return render(
                                    request, self.template_name, self.get_context_data()
                                )
                            if not rote_form.cleaned_data["practice"]:
                                rote_form.add_error(None, "Must choose rote Practice")
                                return render(
                                    request, self.template_name, self.get_context_data()
                                )
                            if not rote_form.cleaned_data["attribute"]:
                                rote_form.add_error(None, "Must choose rote Attribute")
                                return render(
                                    request, self.template_name, self.get_context_data()
                                )
                            if not rote_form.cleaned_data["ability"]:
                                rote_form.add_error(None, "Must choose rote Ability")
                                return render(
                                    request, self.template_name, self.get_context_data()
                                )
                            if not rote_form.cleaned_data["description"]:
                                rote_form.add_error(
                                    None, "Must choose rote description"
                                )
                                return render(
                                    request, self.template_name, self.get_context_data()
                                )
                            if rote_form.cleaned_data["select_or_create_effect"]:
                                if not rote_form.cleaned_data["systems"]:
                                    rote_form.add_error(
                                        None, "Must choose rote systems"
                                    )
                                    return render(
                                        request,
                                        self.template_name,
                                        self.get_context_data(),
                                    )
                                if (
                                    rote_form.cleaned_data["correspondence"]
                                    + rote_form.cleaned_data["entropy"]
                                    + rote_form.cleaned_data["forces"]
                                    + rote_form.cleaned_data["life"]
                                    + rote_form.cleaned_data["matter"]
                                    + rote_form.cleaned_data["mind"]
                                    + rote_form.cleaned_data["prime"]
                                    + rote_form.cleaned_data["spirit"]
                                    + rote_form.cleaned_data["time"]
                                    == 0
                                ):
                                    rote_form.add_error(
                                        None, "Effects must have sphere ratings"
                                    )
                                    return render(
                                        request,
                                        self.template_name,
                                        self.get_context_data(),
                                    )
                        try:
                            rote_form.save(self.object)
                        except forms.ValidationError:
                            return render(
                                request, self.template_name, self.get_context_data()
                            )
            else:
                print("errors", form.errors)
        if "Approve" in form.data.values():
            xp_index = [x for x in form.data.keys() if form.data[x] == "Approve"][0]
            index = "_".join(xp_index.split("_")[:-1])
            d = [x for x in self.object.spent_xp if x["index"] == index][0]
            i = self.object.spent_xp.index(d)
            char_id, trait_type, trait, value = index.split("_")
            value = int(value)

            # Use atomic approval for attributes and abilities
            if trait_type == "attribute":
                att = Attribute.objects.get(name=trait)
                try:
                    self.object.approve_xp_spend(i, att.property_name, value)
                    messages.success(request, f"Approved {att.name} increase to {value}")
                except ValidationError as e:
                    messages.error(request, str(e))
            elif trait_type == "ability":
                abb = Ability.objects.get(name=trait)
                try:
                    self.object.approve_xp_spend(i, abb.property_name, value)
                    messages.success(request, f"Approved {abb.name} increase to {value}")
                except ValidationError as e:
                    messages.error(request, str(e))
            elif trait_type == "background":
                # Wrap in transaction for atomicity
                with transaction.atomic():
                    trait, note = trait.replace("-", " ").split(" (")
                    note = note[:-1]
                    bgr = self.object.backgrounds.filter(bg__name=trait, note=note).first()
                    bgr.rating += 1
                    bgr.save()
                    self.object.spent_xp[i]["approved"] = "Approved"
                    self.object.save()
            elif trait_type == "new-background":
                # Wrap in transaction for atomicity
                with transaction.atomic():
                    trait = trait.replace("-", " ")
                    if "(" not in trait:
                        note = ""
                        trait = trait
                    else:
                        trait, note = trait.split("(")
                        note = note[:-1]
                    trait = trait.strip()
                    note = note.strip()
                    BackgroundRating.objects.create(
                        bg=Background.objects.get(name=trait),
                        rating=1,
                        char=self.object,
                        note=note,
                    )
                    self.object.spent_xp[i]["approved"] = "Approved"
                    self.object.save()
            elif trait_type == "willpower":
                # Use atomic approval method
                try:
                    self.object.approve_xp_spend(i, 'willpower', value)
                    messages.success(request, f"Approved Willpower increase to {value}")
                except ValidationError as e:
                    messages.error(request, str(e))
            elif trait_type == "meritflaw":
                # Wrap in transaction for atomicity
                with transaction.atomic():
                    trait = trait.replace("-", " ")
                    value = int(value)
                    mf = MeritFlaw.objects.get(name=trait)
                    self.object.add_mf(mf, value)
                    self.object.spent_xp[i]["approved"] = "Approved"
                    self.object.save()
            elif trait_type == "sphere":
                # Wrap in transaction for atomicity
                with transaction.atomic():
                    s = Sphere.objects.get(name=trait)
                    setattr(self.object, s.property_name, value)
                    self.object.spent_xp[i]["approved"] = "Approved"
                    self.object.save()
            elif trait_type == "arete":
                # Use atomic approval method
                try:
                    self.object.approve_xp_spend(i, 'arete', value)
                    messages.success(request, f"Approved Arete increase to {value}")
                except ValidationError as e:
                    messages.error(request, str(e))
            elif trait_type == "tenet":
                # Wrap in transaction for atomicity
                with transaction.atomic():
                    t = Tenet.objects.get(name=trait.replace("-", " "))
                    self.object.other_tenets.add(t)
                    self.object.spent_xp[i]["approved"] = "Approved"
                    self.object.save()
            elif trait_type == "remove-tenet":
                # Wrap in transaction for atomicity
                with transaction.atomic():
                    trait = " ".join(trait.split("-")[1:])
                    tenet = Tenet.objects.get(name=trait)
                    if tenet in self.object.other_tenets.all():
                        self.object.other_tenets.remove(tenet)
                    else:
                        replacement = self.object.other_tenets.filter(
                            tenet_type=tenet.tenet_type
                        ).first()
                        if tenet.tenet_type == "met":
                            self.object.metaphysical_tenet = replacement
                        elif tenet.tenet_type == "per":
                            self.object.personal_tenet = replacement
                        elif tenet.tenet_type == "asc":
                            self.object.ascension_tenet = replacement
                        self.object.other_tenets.remove(replacement)
                    self.object.spent_xp[i]["approved"] = "Approved"
                    self.object.save()
            elif trait_type == "practice":
                # Wrap in transaction for atomicity
                with transaction.atomic():
                    trait = trait.replace("-", " ")
                    practice = Practice.objects.get(name=trait)
                    self.object.add_practice(practice)
                    self.object.spent_xp[i]["approved"] = "Approved"
                    self.object.save()
            elif trait_type == "rotes":
                # Wrap in transaction for atomicity
                with transaction.atomic():
                    self.object.rote_points += 3
                    self.object.spent_xp[i]["approved"] = "Approved"
                    self.object.save()
            elif trait_type == "resonance":
                # Wrap in transaction for atomicity
                with transaction.atomic():
                    t = trait.split("-")
                    detail = " ".join(t[1:])[1:-1]
                    trait = t[0]
                    self.object.add_resonance(detail)
                    self.object.spent_xp[i]["approved"] = "Approved"
                    self.object.save()
        if "Reject" in form.data.values():
            # Wrap rejection in transaction to prevent partial refunds
            with transaction.atomic():
                xp_index = [x for x in form.data.keys() if form.data[x] == "Reject"][0]
                index = "_".join(xp_index.split("_")[:-1])
                spends = [x for x in self.object.spent_xp if x["index"] == index]
                for spend in spends:
                    self.object.xp += spend["cost"]
                self.object.spent_xp = [
                    x
                    for x in self.object.spent_xp
                    if x["index"] != index
                    or not (x["index"] == index and x["approved"] == "Pending")
                ]
                self.object.save()
                messages.success(request, f"Rejected XP spend and refunded {sum(s['cost'] for s in spends)} XP")
        if "specialties" in form.data.keys():
            specs = {
                k: v
                for k, v in form.data.items()
                if k not in ["csrfmiddlewaretoken", "specialties"]
            }
            for stat, spec in specs.items():
                spec = Specialty.objects.get_or_create(name=spec, stat=stat)[0]
                self.object.specialties.add(spec)
            self.object.save()
        if "retire" in form.data.keys():
            self.object.status = "Ret"
            self.object.save()
        if "decease" in form.data.keys():
            self.object.status = "Dec"
            self.object.save()
        if form_errors:
            return self.render_to_response(context)
        return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))


class MageCreateView(MessageMixin, CreateView):
    model = Mage
    fields = [
        "name",
        "owner",
        "description",
        "nature",
        "demeanor",
        "specialties",
        "willpower",
        "derangements",
        "age",
        "apparent_age",
        "date_of_birth",
        "merits_and_flaws",
        "history",
        "goals",
        "notes",
        "strength",
        "dexterity",
        "stamina",
        "perception",
        "intelligence",
        "wits",
        "charisma",
        "manipulation",
        "appearance",
        "awareness",
        "art",
        "leadership",
        "animal_kinship",
        "blatancy",
        "carousing",
        "flying",
        "high_ritual",
        "lucid_dreaming",
        "search",
        "seduction",
        "larceny",
        "meditation",
        "research",
        "survival",
        "technology",
        "acrobatics",
        "archery",
        "biotech",
        "energy_weapons",
        "jetpack",
        "riding",
        "torture",
        "cosmology",
        "enigmas",
        "finance",
        "law",
        "occult",
        "politics",
        "area_knowledge",
        "belief_systems",
        "cryptography",
        "demolitions",
        "lore",
        "media",
        "pharmacopeia",
        "cooking",
        "diplomacy",
        "instruction",
        "intrigue",
        "intuition",
        "mimicry",
        "negotiation",
        "newspeak",
        "scan",
        "scrounging",
        "style",
        "blind_fighting",
        "climbing",
        "disguise",
        "elusion",
        "escapology",
        "fast_draw",
        "fast_talk",
        "fencing",
        "fortune_telling",
        "gambling",
        "gunsmith",
        "heavy_weapons",
        "hunting",
        "hypnotism",
        "jury_rigging",
        "microgravity_operations",
        "misdirection",
        "networking",
        "pilot",
        "psychology",
        "security",
        "speed_reading",
        "swimming",
        "conspiracy_theory",
        "chantry_politics",
        "covert_culture",
        "cultural_savvy",
        "helmsman",
        "history_knowledge",
        "power_brokering",
        "propaganda",
        "theology",
        "unconventional_warface",
        "vice",
        "essence",
        "correspondence",
        "time",
        "spirit",
        "mind",
        "entropy",
        "time",
        "forces",
        "matter",
        "life",
        "arete",
        "affinity_sphere",
        "corr_name",
        "prime_name",
        "spirit_name",
        "age_of_awakening",
        "avatar_description",
        "rote_points",
        "quintessence",
        "paradox",
        "quiet",
        "quiet_type",
        "affiliation",
        "faction",
        "subfaction",
        "public_info",
    ]
    template_name = "characters/mage/mage/form.html"
    success_message = "Mage '{name}' created successfully!"
    error_message = "Failed to create mage. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["affiliation"].queryset = MageFaction.objects.top_level()
        form.fields["faction"].queryset = MageFaction.objects.none()
        form.fields["subfaction"].queryset = MageFaction.objects.none()
        return form


class MageUpdateView(EditPermissionMixin, UpdateView):
    model = Mage
    fields = [
        "name",
        "owner",
        "description",
        "nature",
        "demeanor",
        "specialties",
        "willpower",
        "derangements",
        "age",
        "apparent_age",
        "date_of_birth",
        "merits_and_flaws",
        "history",
        "goals",
        "notes",
        "strength",
        "dexterity",
        "stamina",
        "perception",
        "intelligence",
        "wits",
        "charisma",
        "manipulation",
        "appearance",
        "awareness",
        "art",
        "leadership",
        "animal_kinship",
        "blatancy",
        "carousing",
        "flying",
        "high_ritual",
        "lucid_dreaming",
        "search",
        "seduction",
        "larceny",
        "meditation",
        "research",
        "survival",
        "technology",
        "acrobatics",
        "archery",
        "biotech",
        "energy_weapons",
        "jetpack",
        "riding",
        "torture",
        "cosmology",
        "enigmas",
        "finance",
        "law",
        "occult",
        "politics",
        "area_knowledge",
        "belief_systems",
        "cryptography",
        "demolitions",
        "lore",
        "media",
        "pharmacopeia",
        "cooking",
        "diplomacy",
        "instruction",
        "intrigue",
        "intuition",
        "mimicry",
        "negotiation",
        "newspeak",
        "scan",
        "scrounging",
        "style",
        "blind_fighting",
        "climbing",
        "disguise",
        "elusion",
        "escapology",
        "fast_draw",
        "fast_talk",
        "fencing",
        "fortune_telling",
        "gambling",
        "gunsmith",
        "heavy_weapons",
        "hunting",
        "hypnotism",
        "jury_rigging",
        "microgravity_operations",
        "misdirection",
        "networking",
        "pilot",
        "psychology",
        "security",
        "speed_reading",
        "swimming",
        "conspiracy_theory",
        "chantry_politics",
        "covert_culture",
        "cultural_savvy",
        "helmsman",
        "history_knowledge",
        "power_brokering",
        "propaganda",
        "theology",
        "unconventional_warface",
        "vice",
        "essence",
        "correspondence",
        "time",
        "spirit",
        "mind",
        "entropy",
        "prime",
        "forces",
        "matter",
        "life",
        "arete",
        "affinity_sphere",
        "corr_name",
        "prime_name",
        "spirit_name",
        "age_of_awakening",
        "avatar_description",
        "rote_points",
        "quintessence",
        "paradox",
        "quiet",
        "quiet_type",
        "affiliation",
        "faction",
        "subfaction",
        "public_info",
    ]
    template_name = "characters/mage/mage/form.html"
    success_message = "Mage '{name}' updated successfully!"
    error_message = "Failed to update mage. Please correct the errors below."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = True  # If we got here, user has permission
        return context


class MageBasicsView(LoginRequiredMixin, FormView):
    form_class = MageCreationForm
    template_name = "characters/mage/mage/magebasics.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storyteller"] = False
        if self.request.user.profile.is_st():
            context["storyteller"] = True
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.willpower = 5
        self.object.save()
        messages.success(
            self.request,
            f"Mage '{self.object.name}' created successfully! Continue with character creation."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Please correct the errors in the form below."
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class MageAttributeView(HumanAttributeView):
    model = Mage
    template_name = "characters/mage/mage/chargen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = True  # If we got here, user has permission
        return context


class MageAbilityView(MtAHumanAbilityView):
    model = Mage
    template_name = "characters/mage/mage/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5


class MageBackgroundsView(HumanBackgroundsView):
    template_name = "characters/mage/mage/chargen.html"


class MageFocusView(SpecialUserMixin, UpdateView):
    model = Mage
    fields = [
        "metaphysical_tenet",
        "personal_tenet",
        "ascension_tenet",
        "other_tenets",
    ]
    template_name = "characters/mage/mage/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["metaphysical_tenet"].queryset = Tenet.objects.filter(
            tenet_type="met"
        )
        form.fields["personal_tenet"].queryset = Tenet.objects.filter(tenet_type="per")
        form.fields["ascension_tenet"].queryset = Tenet.objects.filter(tenet_type="asc")
        form.fields["other_tenets"].queryset = Tenet.objects.filter(tenet_type="oth")
        form.fields["personal_tenet"].empty_label = "Choose Personal Tenet"
        form.fields["ascension_tenet"].empty_label = "Choose Ascension Tenet"
        form.fields["metaphysical_tenet"].empty_label = "Choose Metaphysical Tenet"
        return form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["practice_formset"] = PracticeRatingFormSet(
                self.request.POST, instance=self.object, mage=self.object
            )
        else:
            context["practice_formset"] = PracticeRatingFormSet(
                instance=self.object, mage=self.object
            )
        context["is_approved_user"] = True  # If we got here, user has permission
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context["form"].full_clean()
        if context["form"].cleaned_data["metaphysical_tenet"] is None:
            context["form"].add_error(None, "Must include Metaphysical Tenet")
            return self.form_invalid(context["form"])
        if context["form"].cleaned_data["personal_tenet"] is None:
            context["form"].add_error(None, "Must include Personal Tenet")
            return self.form_invalid(context["form"])
        if context["form"].cleaned_data["ascension_tenet"] is None:
            context["form"].add_error(None, "Must include Ascension Tenet")
            return self.form_invalid(context["form"])
        practice_formset = context["practice_formset"]

        if practice_formset.is_valid():
            self.object = form.save()
            ratings = [x.cleaned_data.get("rating") for x in practice_formset]
            ratings = [x for x in ratings if x is not None]
            practice_total = sum(ratings)
            if practice_total != self.object.arete:
                form.add_error(None, "Starting Practices must add up to Arete rating")
                return self.form_invalid(form)
            for practice_form in practice_formset:
                practice = practice_form.cleaned_data.get("practice")
                rating = practice_form.cleaned_data.get("rating")
                if practice is not None:
                    ability_total = 0
                    for ability in practice.abilities.all():
                        ability_total += getattr(self.object, ability.property_name, 0)
                    if (
                        practice is not None
                        and rating is not None
                        and rating <= ability_total / 2
                    ):
                        pr = PracticeRating.objects.create(
                            mage=self.object, practice=practice, rating=rating
                        )
                    else:
                        form.add_error(
                            None,
                            "You must have at least 2 dots in associated abilities for each dot of a Practice",
                        )
                        return self.form_invalid(form)
            self.object.creation_status += 1
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response


class MageSpheresView(SpecialUserMixin, UpdateView):
    model = Mage
    fields = [
        "arete",
        "correspondence",
        "time",
        "spirit",
        "forces",
        "matter",
        "life",
        "entropy",
        "mind",
        "prime",
        "affinity_sphere",
        "corr_name",
        "prime_name",
        "spirit_name",
        "resonance",
    ]
    template_name = "characters/mage/mage/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields[
            "affinity_sphere"
        ].queryset = self.object.get_affinity_sphere_options().order_by("name")
        form.fields["affinity_sphere"].empty_label = "Choose an Affinity"
        form.fields["resonance"].widget = AutocompleteTextInput(
            suggestions=[x.name.title() for x in Resonance.objects.order_by("name")]
        )
        form.fields["affinity_sphere"].required = True
        return form

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial["arete"] = 1
        initial["resonance"] = ""
        return initial

    def form_valid(self, form):
        arete = form.cleaned_data.get("arete", 1)
        correspondence = form.cleaned_data.get("correspondence", 0)
        time = form.cleaned_data.get("time", 0)
        spirit = form.cleaned_data.get("spirit", 0)
        forces = form.cleaned_data.get("forces", 0)
        matter = form.cleaned_data.get("matter", 0)
        life = form.cleaned_data.get("life", 0)
        entropy = form.cleaned_data.get("entropy", 0)
        mind = form.cleaned_data.get("mind", 0)
        prime = form.cleaned_data.get("prime", 0)
        affinity_sphere = form.cleaned_data.get("affinity_sphere")
        if affinity_sphere is None:  # This will catch the 'empty_label' selection
            raise ValidationError("You must select a valid affinity sphere.")
        corr_name = form.cleaned_data.get("corr_name")
        prime_name = form.cleaned_data.get("prime_name")
        spirit_name = form.cleaned_data.get("spirit_name")
        resonance = form.data.get("resonance")
        self.object.add_resonance(resonance)

        if arete > 3:
            form.add_error(None, "Arete may not exceed 3 at character creation")
            return self.form_invalid(form)

        for sphere in [
            correspondence,
            time,
            spirit,
            forces,
            matter,
            life,
            entropy,
            mind,
            prime,
        ]:
            if (
                sphere < 0
                or sphere > arete
                or getattr(self.object, self.object.affinity_sphere.property_name) == 0
            ):
                form.add_error(
                    None,
                    "Spheres must range from 0-Arete Rating and Affinity Sphere must be nonzero",
                )
                return self.form_invalid(form)

        tot_spheres = sum(
            [correspondence, time, spirit, forces, matter, life, entropy, mind, prime]
        )
        if tot_spheres != 6:
            form.add_error(None, "Spheres must total 6")
            return self.form_invalid(form)
        self.object.creation_status += 1
        for i in range(arete - 1):
            self.object.freebies -= 4
            self.object.spent_freebies.append(
                self.object.freebie_spend_record("Arete", "arete", i + 2)
            )
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = form.errors
        if "resonance" in errors and "resonance" in form.data:
            del errors["resonance"]
        if not errors:
            return self.form_valid(form)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = True  # If we got here, user has permission
        return context


class MageExtrasView(SpecialUserMixin, UpdateView):
    model = Mage
    fields = [
        "date_of_birth",
        "apparent_age",
        "age_of_awakening",
        "age",
        "description",
        "history",
        "avatar_description",
        "goals",
        "notes",
        "public_info",
    ]
    template_name = "characters/mage/mage/chargen.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = True  # If we got here, user has permission
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
        form.fields["avatar_description"].widget.attrs.update(
            {
                "placeholder": "Describe your Avatar. Both how it appears to you, how you relate to it, and anything it is, in particular, pushing you towards."
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


class MageFreebiesView(HumanFreebiesView):
    model = Mage
    form_class = MageFreebiesForm
    template_name = "characters/mage/mage/chargen.html"

    def get_category_functions(self):
        d = super().get_category_functions()
        d.update(
            {
                "sphere": self.object.sphere_freebies,
                "arete": self.object.arete_freebies,
                "rotes": self.object.rotes_freebies,
                "resonance": self.object.resonance_freebies,
                "tenet": self.object.tenet_freebies,
                "practice": self.object.practice_freebies,
                "quintessence": self.object.quintessence_freebies,
            }
        )
        return d


class MageLanguagesView(HumanLanguagesView):
    template_name = "characters/mage/mage/chargen.html"


class MageRoteView(SpecialUserMixin, CreateView):
    model = Rote
    form_class = RoteCreationForm
    template_name = "characters/mage/mage/chargen.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        mage_id = self.kwargs.get("pk")
        context["object"] = Mage.objects.get(id=mage_id)
        context["is_approved_user"] = self.check_if_special_user(
            context["object"], self.request.user
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        mage_id = self.kwargs.get("pk")
        mage = Mage.objects.get(pk=mage_id)
        kwargs["instance"] = mage
        return kwargs

    def form_invalid(self, form):
        errors = form.errors
        print(errors)
        # if "ability" in errors:
        #     del errors["ability"]
        if not errors:
            return self.form_valid(form)
        return super().form_invalid(form)

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        mage = context["object"]
        if (
            not form.cleaned_data["select_or_create_rote"]
            and not form.cleaned_data["rote_options"]
        ):
            form.add_error(None, "Must create or select a rote")
            return super().form_invalid(form)
        if form.cleaned_data["select_or_create_rote"]:
            if (
                not form.cleaned_data["select_or_create_effect"]
                and not form.cleaned_data["effect_options"]
            ):
                form.add_error(None, "Must create or select an effect")
                return super().form_invalid(form)
            if not form.cleaned_data["name"]:
                form.add_error(None, "Must choose rote name")
                return super().form_invalid(form)
            if not form.cleaned_data["practice"]:
                form.add_error(None, "Must choose rote Practice")
                return super().form_invalid(form)
            if not form.cleaned_data["attribute"]:
                form.add_error(None, "Must choose rote Attribute")
                return super().form_invalid(form)
            if not form.cleaned_data["ability"]:
                form.add_error(None, "Must choose rote Ability")
                return super().form_invalid(form)
            if not form.cleaned_data["description"]:
                form.add_error(None, "Must choose rote description")
                return super().form_invalid(form)
            if form.cleaned_data["select_or_create_effect"]:
                if not form.cleaned_data["systems"]:
                    form.add_error(None, "Must choose rote systems")
                    return super().form_invalid(form)
                if (
                    form.cleaned_data["correspondence"]
                    + form.cleaned_data["entropy"]
                    + form.cleaned_data["forces"]
                    + form.cleaned_data["life"]
                    + form.cleaned_data["matter"]
                    + form.cleaned_data["mind"]
                    + form.cleaned_data["prime"]
                    + form.cleaned_data["spirit"]
                    + form.cleaned_data["time"]
                    == 0
                ):
                    form.add_error(None, "Effects must have sphere ratings")
                    return super().form_invalid(form)

        if form.save(mage):
            if mage.rote_points == 0:
                mage.creation_status += 1
                mage.save()
                for step in [
                    "node",
                    "library",
                    "familiar",
                    "wonder",
                    "enhancement",
                    "sanctum",
                    "allies",
                ]:
                    if (
                        BackgroundRating.objects.filter(
                            bg=Background.objects.get(property_name=step),
                            char=mage,
                            complete=False,
                        ).count()
                        == 0
                    ):
                        mage.creation_status += 1
                    else:
                        mage.save()
                        break
                    mage.save()
            return HttpResponseRedirect(mage.get_absolute_url())
        return super().form_invalid(form)


class MageAlliesView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "allies"
    form_class = AllyForm
    template_name = "characters/mage/mage/chargen.html"


class MageEnhancementView(MtAEnhancementView):
    template_name = "characters/mage/mage/chargen.html"


class MageFamiliarView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "familiar"
    form_class = FamiliarForm
    template_name = "characters/mage/mage/chargen.html"

    def special_valid_action(self, background_object):
        background_object.freebies = 10 * self.current_background.rating
        background_object.status = "Un"
        background_object.save()
        return background_object


class MageLibraryView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "library"
    form_class = LibraryForm
    template_name = "characters/mage/mage/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        obj = get_object_or_404(self.primary_object_class, pk=self.kwargs.get("pk"))
        form.fields["name"].initial = (
            self.current_background.note or f"{obj.name}'s Library"
        )
        tmp = [obj.affiliation, obj.faction, obj.subfaction]
        tmp = [x.pk for x in tmp if hasattr(x, "pk")]
        form.fields["faction"].queryset = MageFaction.objects.filter(pk__in=tmp)
        return form


class MageNodeView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "node"
    form_class = NodeForm
    template_name = "characters/mage/mage/chargen.html"


class MageSpecialtiesView(HumanSpecialtiesView):
    template_name = "characters/mage/mage/chargen.html"


class MageWonderView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "wonder"
    potential_skip = [
        "enhancement",
        "sanctum",
        "allies",
    ]
    form_class = WonderForm
    template_name = "characters/mage/mage/chargen.html"
    multiple_ownership = True


class MageSanctumView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "sanctum"
    potential_skip = [
        "allies",
    ]
    form_class = SanctumForm
    template_name = "characters/mage/mage/chargen.html"


class MageChantryView(GenericBackgroundView):
    primary_object_class = Mage
    background_name = "chantry"
    form_class = ChantrySelectOrCreateForm
    template_name = "characters/mage/mage/chargen.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = self.primary_object_class.objects.get(
            pk=self.kwargs["pk"]
        )
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.chantry_creation_form.fields[
            "total_points"
        ].initial = self.current_background.rating
        form.chantry_creation_form.fields["total_points"].widget.attrs.update(
            {
                "min": self.current_background.rating,
                "max": self.current_background.rating,
            }
        )
        return form


class MageCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: MageAttributeView,
        2: MageAbilityView,
        3: MageBackgroundsView,
        4: MageSpheresView,
        5: MageFocusView,
        6: MageExtrasView,
        7: MageFreebiesView,
        8: MageLanguagesView,
        9: MageRoteView,
        10: MageNodeView,
        11: MageLibraryView,
        12: MageFamiliarView,
        13: MageWonderView,
        14: MageEnhancementView,
        15: MageSanctumView,
        16: MageAlliesView,
        17: MageChantryView,
        18: MageSpecialtiesView,
    }
    model_class = Mage
    key_property = "creation_status"
    default_redirect = MageDetailView

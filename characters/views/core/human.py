from typing import Any

from characters.forms.core.freebies import HumanFreebiesForm
from characters.forms.core.specialty import SpecialtiesForm
from characters.models.core import Human
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.core.specialty import Specialty
from characters.services.freebie_spending import FreebieSpendingServiceFactory
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.character import CharacterDetailView
from core.forms.language import HumanLanguageForm
from core.mixins import (
    DropdownOptionsView,
    EditPermissionMixin,
    MessageMixin,
    SimpleValuesView,
    SpendFreebiesPermissionMixin,
)
from core.models import Language
from core.views.generic import DictView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView
from game.models import ObjectType


class HumanDetailView(CharacterDetailView):
    """Detail view for Human characters. Inherits permissions from CharacterDetailView."""

    model = Human
    template_name = "characters/core/human/detail.html"


class HumanCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    """Create view for Human characters."""

    model = Human
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
    ]
    template_name = "characters/core/human/form.html"
    success_message = "Human created successfully."
    error_message = "Error creating Human."

    def form_valid(self, form):
        if not form.instance.owner:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class HumanUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    """
    Update view for Human characters.
    Only STs and Admins can directly edit character fields.
    Owners should use the character creation workflow or XP spending.
    """

    model = Human
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
    ]
    template_name = "characters/core/human/form.html"
    success_message = "Human updated successfully."
    error_message = "Error updating Human."


class HumanBasicsView(LoginRequiredMixin, CreateView):
    """First step of character creation."""

    model = Human
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
    ]
    template_name = "characters/core/human/humanbasics.html"

    def form_valid(self, form):
        if not form.instance.owner:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class HumanAttributeView(SpendFreebiesPermissionMixin, UpdateView):
    """
    Character creation step: allocating attribute points.
    Uses SpendFreebiesPermissionMixin - only owners of unfinished characters can access.
    """

    model = Human
    fields = [
        "strength",
        "dexterity",
        "stamina",
        "perception",
        "intelligence",
        "wits",
        "charisma",
        "manipulation",
        "appearance",
    ]
    template_name = "characters/core/human/attributes.html"

    primary = 7
    secondary = 5
    tertiary = 3

    def form_valid(self, form):
        strength = form.cleaned_data.get("strength")
        dexterity = form.cleaned_data.get("dexterity")
        stamina = form.cleaned_data.get("stamina")
        perception = form.cleaned_data.get("perception")
        intelligence = form.cleaned_data.get("intelligence")
        wits = form.cleaned_data.get("wits")
        charisma = form.cleaned_data.get("charisma")
        manipulation = form.cleaned_data.get("manipulation")
        appearance = form.cleaned_data.get("appearance")

        for attribute in [
            strength,
            dexterity,
            stamina,
            perception,
            intelligence,
            wits,
            charisma,
            manipulation,
            appearance,
        ]:
            if attribute < 1 or attribute > 5:
                form.add_error(None, "Attributes must range from 1-5")
                return self.form_invalid(form)

        triple = [
            strength + dexterity + stamina,
            perception + intelligence + wits,
            charisma + manipulation + appearance,
        ]
        triple.sort()
        if triple != [3 + self.tertiary, 3 + self.secondary, 3 + self.primary]:
            form.add_error(
                None,
                f"Attributes must be distributed {self.primary}/{self.secondary}/{self.tertiary}",
            )
            return self.form_invalid(form)
        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["primary"] = self.primary
        context["secondary"] = self.secondary
        context["tertiary"] = self.tertiary
        return context


class HumanAbilityView(SpendFreebiesPermissionMixin, UpdateView):
    model = Human
    fields = Human.primary_abilities
    template_name = "characters/wraith/wtohuman/chargen.html"

    primary = 11
    secondary = 7
    tertiary = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["primary"] = self.primary
        context["secondary"] = self.secondary
        context["tertiary"] = self.tertiary
        return context

    def form_valid(self, form):
        for ability in self.model.primary_abilities:
            if form.cleaned_data.get(ability) < 0 or form.cleaned_data.get(ability) > 3:
                form.add_error(None, "Abilities must range from 0-3")
                return self.form_invalid(form)

        talents = sum([form.cleaned_data.get(ability) for ability in self.model.talents])
        skills = sum([form.cleaned_data.get(ability) for ability in self.model.skills])
        knowledges = sum([form.cleaned_data.get(ability) for ability in self.model.knowledges])

        triple = [talents, skills, knowledges]
        triple.sort()
        if triple != [self.tertiary, self.secondary, self.primary]:
            form.add_error(
                None,
                f"Abilities must be distributed {self.primary}/{self.secondary}/{self.tertiary}",
            )
            return self.form_invalid(form)
        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class HumanBiographicalInformation(SpendFreebiesPermissionMixin, UpdateView):
    model = Human
    fields = [
        "age",
        "apparent_age",
        "date_of_birth",
        "history",
        "goals",
        "notes",
    ]
    template_name = "characters/core/human/bio.html"

    def form_valid(self, form):
        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class LoadExamplesView(DropdownOptionsView):
    """AJAX view to load examples for dropdown options (Attribute, Ability, Background, MeritFlaw)."""

    label_attr = "__str__"

    def get_options(self):
        category_choice = self.request.GET.get("category")
        if category_choice == "Attribute":
            return Attribute.objects.all()
        elif category_choice == "Ability":
            return Ability.objects.all()
        elif category_choice == "Background":
            return Background.objects.all()
        elif category_choice == "MeritFlaw":
            return MeritFlaw.objects.all()
        return []


class LoadValuesView(SimpleValuesView):
    """AJAX view to load merit/flaw rating values filtered by affordability."""

    def get_values(self):
        mf = get_object_or_404(MeritFlaw, pk=self.request.GET.get("example"))
        character_id = self.request.GET.get("object")
        is_xp = self.request.GET.get("xp", "false").lower() == "true"

        ratings = [x.value for x in mf.ratings.all()]
        ratings.sort()

        # Filter ratings based on character's available freebies/XP and flaw limit
        if character_id:
            character = get_object_or_404(Human, pk=character_id)
            current_rating = character.mf_rating(mf)

            affordable_ratings = []

            if is_xp:
                # For XP spending: cost = 3 × |new_rating - current_rating|
                available_xp = character.xp
                for rating in ratings:
                    cost = 3 * abs(rating - current_rating)
                    if cost <= available_xp and rating != current_rating:
                        affordable_ratings.append(rating)
            else:
                # For freebie spending: cost = rating value
                current_flaws = character.total_flaws()
                available_freebies = character.freebies

                for rating in ratings:
                    # Flaws (negative ratings) are affordable if they don't exceed the -7 limit
                    if rating < 0:
                        if current_flaws + rating >= -7:
                            affordable_ratings.append(rating)
                    # Merits and neutral (0) ratings are affordable if we have enough freebies
                    else:
                        if rating <= available_freebies:
                            affordable_ratings.append(rating)

            ratings = affordable_ratings

        return ratings


class HumanFreebieFormPopulationView(View):
    primary_class = Human

    def get(self, request, *args, **kwargs):
        from django.http import JsonResponse

        category_choice = request.GET.get("category")
        self.character = get_object_or_404(self.primary_class, pk=request.GET.get("object"))

        if category_choice == "Background":
            # Return combined Background and BackgroundRating objects with prefixed values
            return self._get_combined_backgrounds()

        from core.ajax import dropdown_options_response

        examples = []
        if category_choice in self.category_method_map().keys():
            examples = self.category_method_map()[category_choice]()
        else:
            examples = []

        return dropdown_options_response(examples, label_attr="__str__")

    def _get_combined_backgrounds(self):
        """Return combined new and existing backgrounds with prefixed values."""
        from django.http import JsonResponse

        options = []

        # New backgrounds (Background objects) - prefixed with "bg_"
        new_backgrounds = Background.objects.filter(
            property_name__in=self.character.allowed_backgrounds
        ).order_by("name")
        for bg in new_backgrounds:
            options.append(
                {
                    "value": f"bg_{bg.pk}",
                    "label": f"{bg.name} (new)",
                    "poolable": bg.poolable if hasattr(bg, "poolable") else False,
                    "is_new": True,
                }
            )

        # Existing backgrounds (BackgroundRating objects) - prefixed with "br_"
        existing_backgrounds = BackgroundRating.objects.filter(char=self.character, rating__lt=5)
        for br in existing_backgrounds:
            label = str(br)
            options.append(
                {
                    "value": f"br_{br.pk}",
                    "label": label,
                    "poolable": False,  # Existing backgrounds don't change poolable status
                    "is_new": False,
                }
            )

        return JsonResponse({"options": options})

    def category_method_map(self):
        return {
            "Attribute": self.attribute_options,
            "Ability": self.ability_options,
            "Background": self.background_options,
            "MeritFlaw": self.meritflaw_options,
        }

    def attribute_options(self):
        return [
            x for x in Attribute.objects.all() if getattr(self.character, x.property_name, 0) < 5
        ]

    def ability_options(self):
        return [
            x
            for x in Ability.objects.order_by("name")
            if getattr(self.character, x.property_name, 0) < 5
            and hasattr(self.character, x.property_name)
        ]

    def background_options(self):
        """Return combined backgrounds - handled specially in get() method."""
        # This is handled by _get_combined_backgrounds() but we need the method
        # to exist for the category_method_map
        return []

    def meritflaw_options(self):
        char_type = self.primary_class.type
        if "human" in char_type:
            char_type = "human"
        chartype, _ = ObjectType.objects.get_or_create(
            name=char_type, defaults={"type": "char", "gameline": "wod"}
        )
        examples = MeritFlaw.objects.filter(allowed_types=chartype)

        # Filter to only show merit/flaws with at least one affordable rating
        affordable_mfs = []
        current_flaws = self.character.total_flaws()
        available_freebies = self.character.freebies

        for mf in examples:
            ratings = mf.get_ratings()
            has_affordable = False

            for rating in ratings:
                # Flaws (negative ratings) are affordable if they don't exceed the -7 limit
                if rating < 0:
                    if current_flaws + rating >= -7:
                        has_affordable = True
                        break
                # Merits and neutral (0) ratings are affordable if we have enough freebies
                else:
                    if rating <= available_freebies:
                        has_affordable = True
                        break

            if has_affordable:
                affordable_mfs.append(mf.id)

        return examples.filter(id__in=affordable_mfs)


class HumanFreebiesView(SpendFreebiesPermissionMixin, UpdateView):
    """View for spending freebie points during character creation.

    Uses FreebieSpendingServiceFactory to get the appropriate service
    for the character type and delegates all spending logic to the service.
    """

    model = Human
    form_class = HumanFreebiesForm
    template_name = "characters/human/human/chargen.html"

    def form_valid(self, form):
        if form.is_valid():
            # Get the spending service for this character type
            service = FreebieSpendingServiceFactory.get_service(self.object)

            # Extract form data
            category = form.data["category"]
            example = form.cleaned_data.get("example")
            value = form.cleaned_data.get("value")
            note = form.cleaned_data.get("note", "")
            pooled = form.cleaned_data.get("pooled", False)

            # Handle Background with prefixed values (bg_123 or br_456)
            if category == "Background":
                example_value = form.data.get("example", "")
                if example_value.startswith("bg_"):
                    # New background - load Background object
                    bg_pk = example_value[3:]  # Remove "bg_" prefix
                    example = get_object_or_404(Background, pk=bg_pk)
                elif example_value.startswith("br_"):
                    # Existing background - load BackgroundRating object
                    br_pk = example_value[3:]  # Remove "br_" prefix
                    example = get_object_or_404(BackgroundRating, pk=br_pk)
                else:
                    form.add_error(None, "Invalid background selection")
                    return super().form_invalid(form)

            # Convert value to int if present (for MeritFlaw ratings)
            if value and value != "":
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    pass

            # Use the service to handle the spending
            result = service.spend(
                category=category,
                example=example,
                value=value,
                note=note,
                pooled=pooled,
            )

            if result.success:
                return HttpResponseRedirect(self.get_success_url())
            else:
                form.add_error(None, result.error)
                return super().form_invalid(form)

        return super().form_invalid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        return response

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Human, pk=kwargs.get("pk"))
        if obj.freebies == 0:
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)


class HumanLanguagesView(SpendFreebiesPermissionMixin, FormView):
    form_class = HumanLanguageForm
    template_name = "characters/core/human/chargen.html"

    def get_object(self):
        """Return the Human object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        return self.object

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Human, pk=kwargs.get("pk"))
        if "Language" not in obj.merits_and_flaws.values_list("name", flat=True):
            english, _ = Language.objects.get_or_create(name="English")
            obj.languages.add(english)
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

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
        num_languages = human.num_languages()
        english, _ = Language.objects.get_or_create(name="English")
        human.languages.add(english)
        for i in range(num_languages):
            language_name = form.cleaned_data.get(f"language_{i+1}")
            if language_name:
                language, created = Language.objects.get_or_create(name=language_name)
                human.languages.add(language)
        human.creation_status += 1
        human.save()
        return HttpResponseRedirect(human.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context


class HumanSpecialtiesView(SpendFreebiesPermissionMixin, FormView):
    form_class = SpecialtiesForm
    template_name = "characters/core/human/chargen.html"

    def get_object(self):
        """Return the Human object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Human, id=self.kwargs["pk"])
        return self.object

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        obj = self.get_object()
        kwargs["object"] = obj
        kwargs["specialties_needed"] = obj.needed_specialties()
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        mage = context["object"]
        for field in form.fields:
            spec = Specialty.objects.get_or_create(name=form.data[field], stat=field)[0]
            mage.specialties.add(spec)
        mage.status = "Sub"
        mage.save()
        return HttpResponseRedirect(mage.get_absolute_url())


class HumanCharacterCreationView(DictView):
    view_mapping = {
        1: HumanAttributeView,
        2: HumanAbilityView,
        3: HumanBackgroundsView,
        4: HumanBiographicalInformation,
        5: HumanFreebiesView,
        6: HumanLanguagesView,
        7: HumanSpecialtiesView,
    }
    model_class = Human
    key_property = "creation_status"
    default_redirect = HumanDetailView

    def is_valid_key(self, obj, key):
        return key in self.view_mapping and obj.status == "Un"

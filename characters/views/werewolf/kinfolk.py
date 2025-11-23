from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.werewolf.kinfolk import KinfolkCreationForm
from characters.models.core.merit_flaw_block import MeritFlawRating
from characters.models.werewolf.kinfolk import Kinfolk
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanFreebieFormPopulationView,
)
from characters.views.werewolf.wtahuman import (
    WtAHumanAbilityView,
    WtAHumanAlliesView,
    WtAHumanExtrasView,
    WtAHumanFreebieFormPopulationView,
    WtAHumanFreebiesView,
    WtAHumanLanguagesView,
    WtAHumanSpecialtiesView,
)
from core.mixins import (
    ApprovedUserContextMixin,
    EditPermissionMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
)
from core.views.message_mixin import MessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, FormView, UpdateView
from game.models import ObjectType


class KinfolkDetailView(ApprovedUserContextMixin, ViewPermissionMixin, DetailView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        specialties = {}
        for attribute in self.object.get_attributes():
            specialties[attribute] = ", ".join(
                [x.name for x in self.object.specialties.filter(stat=attribute)]
            )
        for ability in self.object.get_abilities():
            specialties[ability] = ", ".join(
                [x.name for x in self.object.specialties.filter(stat=ability)]
            )
        for key, value in specialties.items():
            context[f"{key}_spec"] = value

        context["merits_and_flaws"] = MeritFlawRating.objects.order_by(
            "mf__name"
        ).filter(character=self.object)
        all_gifts = list(context["object"].gifts.all())
        row_length = 3
        all_gifts = [
            all_gifts[i : i + row_length] for i in range(0, len(all_gifts), row_length)
        ]
        context["gifts"] = all_gifts
        return context


class KinfolkCreateView(MessageMixin, CreateView):
    model = Kinfolk
    success_message = "Kinfolk created successfully."
    error_message = "Error creating kinfolk."
    fields = [
        "name",
        "description",
        "concept",
        "nature",
        "demeanor",
        "strength",
        "dexterity",
        "stamina",
        "perception",
        "intelligence",
        "wits",
        "charisma",
        "manipulation",
        "appearance",
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "specialties",
        "languages",
        "willpower",
        "derangements",
        "age",
        "apparent_age",
        "date_of_birth",
        "merits_and_flaws",
        "history",
        "goals",
        "notes",
        "leadership",
        "primal_urge",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "enigmas",
        "law",
        "occult",
        "rituals",
        "technology",
        "breed",
        "tribe",
        "relation",
        "gifts",
        "gnosis",
        "fetishes_owned",
        "glory",
        "temporary_glory",
        "wisdom",
        "temporary_wisdom",
        "honor",
        "temporary_honor",
    ]
    template_name = "characters/werewolf/kinfolk/form.html"


class KinfolkUpdateView(ApprovedUserContextMixin, EditPermissionMixin, UpdateView):
    model = Kinfolk
    success_message = "Kinfolk updated successfully."
    error_message = "Error updating kinfolk."
    fields = [
        "name",
        "description",
        "concept",
        "nature",
        "demeanor",
        "strength",
        "dexterity",
        "stamina",
        "perception",
        "intelligence",
        "wits",
        "charisma",
        "manipulation",
        "appearance",
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "specialties",
        "languages",
        "willpower",
        "derangements",
        "age",
        "apparent_age",
        "date_of_birth",
        "merits_and_flaws",
        "history",
        "goals",
        "notes",
        "leadership",
        "primal_urge",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "enigmas",
        "law",
        "occult",
        "rituals",
        "technology",
        "breed",
        "tribe",
        "relation",
        "gifts",
        "gnosis",
        "fetishes_owned",
        "glory",
        "temporary_glory",
        "wisdom",
        "temporary_wisdom",
        "honor",
        "temporary_honor",
    ]
    template_name = "characters/werewolf/kinfolk/form.html"


class KinfolkBasicsView(LoginRequiredMixin, FormView):
    form_class = KinfolkCreationForm
    template_name = "characters/werewolf/kinfolk/basics.html"

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
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class KinfolkAttributeView(HumanAttributeView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class KinfolkAbilityView(WtAHumanAbilityView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkBackgroundsView(HumanBackgroundsView):
    template_name = "characters/werewolf/kinfolk/chargen.html"

    def form_valid(self, form):
        """Validate tribal restrictions on backgrounds before saving."""
        self.get_context_data()

        # Get the character
        character = self.object

        # If no tribe is set, use parent validation
        if not character.tribe:
            return super().form_valid(form)

        tribe_name = character.tribe.name

        # Track background totals for resource-capped tribes
        resources_total = 0

        # Validate each background form
        for f in form:
            if "bg" not in f.cleaned_data or "rating" not in f.cleaned_data:
                continue

            bg = f.cleaned_data["bg"]
            rating = f.cleaned_data["rating"]

            if rating == 0:  # Skip backgrounds with 0 rating
                continue

            bg_name = bg.property_name

            # Track resources for tribes with caps
            if bg_name == "resources":
                resources_total = rating

            # Bone Gnawers: No Pure Breed, Resources capped at 3
            if tribe_name == "Bone Gnawers":
                if bg_name == "pure_breed":
                    f.add_error("bg", "Bone Gnawers may not purchase Pure Breed")
                    return super().form_invalid(form)
                if bg_name == "resources" and rating > 3:
                    f.add_error("rating", "Bone Gnawers may not purchase more than 3 dots of Resources")
                    return super().form_invalid(form)

            # Glass Walkers: No Pure Breed or Mentor
            if tribe_name == "Glass Walkers":
                if bg_name in ["pure_breed", "mentor"]:
                    f.add_error("bg", f"Glass Walkers may not purchase {bg.name}")
                    return super().form_invalid(form)

            # Red Talons: No Resources, Allies, or Contacts
            if tribe_name == "Red Talons":
                if bg_name in ["resources", "allies", "contacts"]:
                    f.add_error("bg", f"Red Talons may not purchase {bg.name}")
                    return super().form_invalid(form)

            # Shadow Lords: No Mentor
            if tribe_name == "Shadow Lords":
                if bg_name == "mentor":
                    f.add_error("bg", "Shadow Lords may not purchase Mentor")
                    return super().form_invalid(form)

            # Silent Striders: Resources capped at 3
            if tribe_name == "Silent Striders":
                if bg_name == "resources" and rating > 3:
                    f.add_error("rating", "Silent Striders may not purchase more than 3 dots of Resources")
                    return super().form_invalid(form)

            # Stargazers: Resources capped at 3
            if tribe_name == "Stargazers":
                if bg_name == "resources" and rating > 3:
                    f.add_error("rating", "Stargazers may not purchase more than 3 dots of Resources")
                    return super().form_invalid(form)

            # Wendigo: Resources capped at 3
            if tribe_name == "Wendigo":
                if bg_name == "resources" and rating > 3:
                    f.add_error("rating", "Wendigo may not purchase more than 3 dots of Resources")
                    return super().form_invalid(form)

        # Silver Fangs: Must have at least 1 Pure Breed
        # Check after all forms have been validated
        if tribe_name == "Silver Fangs":
            pure_breed_found = any(
                form_item.cleaned_data.get("bg") and
                form_item.cleaned_data["bg"].property_name == "pure_breed" and
                form_item.cleaned_data.get("rating", 0) >= 1
                for form_item in form
                if "bg" in form_item.cleaned_data and "rating" in form_item.cleaned_data
            )
            if not pure_breed_found:
                # Add error to the first form in the formset
                if len(form.forms) > 0:
                    form.forms[0].add_error(None, "Silver Fangs must purchase at least 1 dot of Pure Breed")
                return super().form_invalid(form)

        # All tribal restrictions passed, use parent validation
        return super().form_valid(form)


class KinfolkExtrasView(WtAHumanExtrasView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkFreebiesView(WtAHumanFreebiesView):
    model = Kinfolk
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Kinfolk


class KinfolkLanguagesView(WtAHumanLanguagesView):
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkAlliesView(GenericBackgroundView):
    primary_object_class = Kinfolk
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkSpecialtiesView(WtAHumanSpecialtiesView):
    template_name = "characters/werewolf/kinfolk/chargen.html"


class KinfolkCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: KinfolkAttributeView,
        2: KinfolkAbilityView,
        3: KinfolkBackgroundsView,
        4: KinfolkExtrasView,
        5: KinfolkFreebiesView,
        6: KinfolkLanguagesView,
        7: KinfolkAlliesView,
        8: KinfolkSpecialtiesView,
    }
    model_class = Kinfolk
    key_property = "creation_status"
    default_redirect = KinfolkDetailView

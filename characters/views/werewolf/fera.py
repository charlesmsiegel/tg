from typing import Any

from characters.forms.core.freebies import HumanFreebiesForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.werewolf.fera import FeraCreationForm
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.werewolf.ajaba import Ajaba
from characters.models.werewolf.ananasi import Ananasi
from characters.models.werewolf.bastet import Bastet
from characters.models.werewolf.corax import Corax
from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import Gift, GiftPermission
from characters.models.werewolf.grondr import Grondr
from characters.models.werewolf.gurahl import Gurahl
from characters.models.werewolf.kitsune import Kitsune
from characters.models.werewolf.mokole import Mokole
from characters.models.werewolf.nagah import Nagah
from characters.models.werewolf.nuwisha import Nuwisha
from characters.models.werewolf.ratkin import Ratkin
from characters.models.werewolf.rokea import Rokea
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanFreebieFormPopulationView,
    HumanFreebiesView,
    HumanLanguagesView,
    HumanSpecialtiesView,
)
from characters.views.werewolf.wtahuman import WtAHumanAbilityView
from core.mixins import (
    EditPermissionMixin,
    SpecialUserMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
    XPApprovalMixin,
)
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, UpdateView
from items.models.werewolf.fetish import Fetish


class FeraDetailView(XPApprovalMixin, ViewPermissionMixin, DetailView):
    model = Fera
    template_name = "characters/werewolf/fera/detail.html"


class FeraUpdateView(EditPermissionMixin, UpdateView):
    model = Fera
    success_message = "Fera updated successfully."
    error_message = "Error updating fera."
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
        "faction",
        "gnosis",
        "rage",
        "renown",
        "temporary_renown",
        "gifts",
        "rites_known",
        "fetishes_owned",
        "first_change",
        "age_of_first_change",
    ]
    template_name = "characters/werewolf/fera/form.html"


class FeraBasicsView(LoginRequiredMixin, FormView):
    form_class = FeraCreationForm
    template_name = "characters/werewolf/fera/basics.html"

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


class FeraBreedFactionView(SpecialUserMixin, UpdateView):
    """
    Stage for setting breed and faction-specific choices.
    This handles the different structures for each Fera type.
    """

    model = Fera
    template_name = "characters/werewolf/fera/chargen.html"

    def get_form_class(self):
        """Return a dynamic form based on the Fera type."""
        obj = self.get_object()

        # Determine which fields to show based on the type
        if isinstance(obj, Ratkin):
            fields = ["breed", "aspect"]
        elif isinstance(obj, Mokole):
            fields = ["breed", "stream", "auspice"]
        elif isinstance(obj, Bastet):
            fields = ["breed", "tribe", "pryio"]
        elif isinstance(obj, Corax):
            fields = ["breed"]
        elif isinstance(obj, Nuwisha):
            fields = ["breed", "role"]
        elif isinstance(obj, Gurahl):
            fields = ["breed", "auspice"]
        elif isinstance(obj, Ananasi):
            fields = ["breed", "aspect"]
        elif isinstance(obj, Rokea):
            fields = ["breed", "auspice"]
        elif isinstance(obj, Kitsune):
            fields = ["breed", "path"]
        elif isinstance(obj, Nagah):
            fields = ["breed", "auspice"]
        elif isinstance(obj, Ajaba):
            fields = ["breed", "auspice"]
        elif isinstance(obj, Grondr):
            fields = ["breed", "auspice"]
        else:
            # Generic Fera
            fields = ["breed", "faction"]

        # Create a dynamic form class
        class FeraBreedFactionForm(forms.ModelForm):
            class Meta:
                model = type(obj)
                fields = fields

        return FeraBreedFactionForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        obj = self.get_object()

        # Add help text based on Fera type
        if "breed" in form.fields:
            form.fields["breed"].help_text = "Choose your breed (birth form)."

        if isinstance(obj, Ratkin):
            if "aspect" in form.fields:
                form.fields["aspect"].help_text = (
                    "Choose your aspect (similar to auspice for Garou)."
                )
        elif isinstance(obj, Mokole):
            if "stream" in form.fields:
                form.fields["stream"].help_text = "Choose your stream (cultural/regional grouping)."
            if "auspice" in form.fields:
                form.fields["auspice"].help_text = (
                    "Choose your auspice (based on sun position at birth)."
                )
        elif isinstance(obj, Bastet):
            if "tribe" in form.fields:
                form.fields["tribe"].help_text = "Choose your tribe (cat species)."
            if "pryio" in form.fields:
                form.fields["pryio"].help_text = "Choose your Pryio (moon-based role)."
        elif isinstance(obj, Nuwisha):
            if "role" in form.fields:
                form.fields["role"].help_text = "Choose your role (optional, loose affiliation)."
                form.fields["role"].required = False
        elif isinstance(obj, Gurahl):
            if "auspice" in form.fields:
                form.fields["auspice"].help_text = "Choose your auspice (seasonal role)."
        elif isinstance(obj, Ananasi):
            if "aspect" in form.fields:
                form.fields["aspect"].help_text = "Choose your aspect (role among the Ananasi)."
        elif isinstance(obj, Rokea):
            if "auspice" in form.fields:
                form.fields["auspice"].help_text = "Choose your auspice (time of birth)."
        elif isinstance(obj, Kitsune):
            if "path" in form.fields:
                form.fields["path"].help_text = "Choose your path (role in society)."
        elif isinstance(obj, Nagah):
            if "auspice" in form.fields:
                form.fields["auspice"].help_text = "Choose your auspice (role as assassin)."
        elif isinstance(obj, Ajaba):
            if "auspice" in form.fields:
                form.fields["auspice"].help_text = "Choose your auspice (lunar cycle)."
        elif isinstance(obj, Grondr):
            if "auspice" in form.fields:
                form.fields["auspice"].help_text = "Choose your auspice (seasonal role)."

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fera_type"] = type(self.object).__name__
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)

        # Call the appropriate setter methods based on Fera type
        if "breed" in form.changed_data:
            obj.set_breed(form.cleaned_data["breed"])

        if isinstance(obj, Ratkin):
            if "aspect" in form.changed_data:
                obj.set_aspect(form.cleaned_data["aspect"])
        elif isinstance(obj, Mokole):
            if "stream" in form.changed_data:
                obj.set_stream(form.cleaned_data["stream"])
            if "auspice" in form.changed_data:
                obj.set_auspice(form.cleaned_data["auspice"])
        elif isinstance(obj, Bastet):
            if "tribe" in form.changed_data:
                obj.set_tribe(form.cleaned_data["tribe"])
            if "pryio" in form.changed_data:
                obj.set_pryio(form.cleaned_data["pryio"])
        elif isinstance(obj, Nuwisha):
            if "role" in form.changed_data and form.cleaned_data.get("role"):
                obj.set_role(form.cleaned_data["role"])
        elif isinstance(obj, Gurahl):
            if "auspice" in form.changed_data:
                obj.set_auspice(form.cleaned_data["auspice"])
        elif isinstance(obj, Ananasi):
            if "aspect" in form.changed_data:
                obj.set_aspect(form.cleaned_data["aspect"])
        elif isinstance(obj, Rokea):
            if "auspice" in form.changed_data:
                obj.set_auspice(form.cleaned_data["auspice"])
        elif isinstance(obj, Kitsune):
            if "path" in form.changed_data:
                obj.set_path(form.cleaned_data["path"])
        elif isinstance(obj, Nagah):
            if "auspice" in form.changed_data:
                obj.set_auspice(form.cleaned_data["auspice"])
        elif isinstance(obj, Ajaba):
            if "auspice" in form.changed_data:
                obj.set_auspice(form.cleaned_data["auspice"])
        elif isinstance(obj, Grondr):
            if "auspice" in form.changed_data:
                obj.set_auspice(form.cleaned_data["auspice"])

        obj.creation_status += 1
        obj.save()
        return super().form_valid(form)


class FeraAttributeView(HumanAttributeView):
    model = Fera
    template_name = "characters/werewolf/fera/chargen.html"


class FeraAbilityView(WtAHumanAbilityView):
    model = Fera
    template_name = "characters/werewolf/fera/chargen.html"

    primary = 13
    secondary = 9
    tertiary = 5


class FeraBackgroundsView(HumanBackgroundsView):
    template_name = "characters/werewolf/fera/chargen.html"


class FeraGiftsView(SpecialUserMixin, UpdateView):
    model = Fera
    fields = ["gifts"]
    template_name = "characters/werewolf/fera/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter gifts to only show rank 1 gifts with appropriate permissions
        form.fields["gifts"].queryset = Gift.objects.filter(
            rank=1, allowed__in=self.object.gift_permissions.all()
        ).order_by("name")

        # Customize help text based on Fera type
        if isinstance(self.object, Corax):
            form.fields["gifts"].help_text = (
                "Choose 3 starting Gifts: all from the Corax gift list."
            )
        elif isinstance(self.object, Nuwisha):
            form.fields["gifts"].help_text = (
                "Choose 3 starting Gifts: from your Breed and general Nuwisha gifts."
            )
        else:
            form.fields["gifts"].help_text = (
                "Choose 3 starting Gifts from your breed and faction/aspect/tribe."
            )

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get gift categories based on type
        obj = self.object

        # Breed gifts (all Fera have this)
        if obj.breed:
            breed_perm = GiftPermission.objects.filter(
                shifter=obj.type, condition=obj.breed
            ).first()
            if breed_perm:
                context["breed_gifts"] = Gift.objects.filter(rank=1, allowed=breed_perm).order_by(
                    "name"
                )

        # Type-specific gift categories
        if isinstance(obj, Ratkin) and obj.aspect:
            aspect_perm = GiftPermission.objects.filter(
                shifter="ratkin", condition=obj.aspect
            ).first()
            if aspect_perm:
                context["aspect_gifts"] = Gift.objects.filter(rank=1, allowed=aspect_perm).order_by(
                    "name"
                )
        elif isinstance(obj, Mokole):
            if obj.stream:
                stream_perm = GiftPermission.objects.filter(
                    shifter="mokole", condition=obj.stream
                ).first()
                if stream_perm:
                    context["stream_gifts"] = Gift.objects.filter(
                        rank=1, allowed=stream_perm
                    ).order_by("name")
            if obj.auspice:
                auspice_perm = GiftPermission.objects.filter(
                    shifter="mokole", condition=obj.auspice
                ).first()
                if auspice_perm:
                    context["auspice_gifts"] = Gift.objects.filter(
                        rank=1, allowed=auspice_perm
                    ).order_by("name")
        elif isinstance(obj, Bastet):
            if obj.tribe:
                tribe_perm = GiftPermission.objects.filter(
                    shifter="bastet", condition=obj.tribe
                ).first()
                if tribe_perm:
                    context["tribe_gifts"] = Gift.objects.filter(
                        rank=1, allowed=tribe_perm
                    ).order_by("name")
            if obj.pryio:
                pryio_perm = GiftPermission.objects.filter(
                    shifter="bastet", condition=obj.pryio
                ).first()
                if pryio_perm:
                    context["pryio_gifts"] = Gift.objects.filter(
                        rank=1, allowed=pryio_perm
                    ).order_by("name")
        elif isinstance(obj, Corax):
            # Corax have a single gift list
            corax_perm = GiftPermission.objects.filter(shifter="corax", condition="corax").first()
            if corax_perm:
                context["corax_gifts"] = Gift.objects.filter(rank=1, allowed=corax_perm).order_by(
                    "name"
                )
        elif isinstance(obj, Nuwisha):
            # Nuwisha have general gifts and optional role gifts
            nuwisha_perm = GiftPermission.objects.filter(
                shifter="nuwisha", condition="nuwisha"
            ).first()
            if nuwisha_perm:
                context["nuwisha_gifts"] = Gift.objects.filter(
                    rank=1, allowed=nuwisha_perm
                ).order_by("name")
            if obj.role:
                role_perm = GiftPermission.objects.filter(
                    shifter="nuwisha", condition=obj.role
                ).first()
                if role_perm:
                    context["role_gifts"] = Gift.objects.filter(rank=1, allowed=role_perm).order_by(
                        "name"
                    )
        elif isinstance(obj, Gurahl) and obj.auspice:
            auspice_perm = GiftPermission.objects.filter(
                shifter="gurahl", condition=obj.auspice
            ).first()
            if auspice_perm:
                context["auspice_gifts"] = Gift.objects.filter(
                    rank=1, allowed=auspice_perm
                ).order_by("name")
        elif isinstance(obj, Ananasi) and obj.aspect:
            aspect_perm = GiftPermission.objects.filter(
                shifter="ananasi", condition=obj.aspect
            ).first()
            if aspect_perm:
                context["aspect_gifts"] = Gift.objects.filter(rank=1, allowed=aspect_perm).order_by(
                    "name"
                )
        elif isinstance(obj, Rokea) and obj.auspice:
            auspice_perm = GiftPermission.objects.filter(
                shifter="rokea", condition=obj.auspice
            ).first()
            if auspice_perm:
                context["auspice_gifts"] = Gift.objects.filter(
                    rank=1, allowed=auspice_perm
                ).order_by("name")
        elif isinstance(obj, Kitsune) and obj.path:
            path_perm = GiftPermission.objects.filter(shifter="kitsune", condition=obj.path).first()
            if path_perm:
                context["path_gifts"] = Gift.objects.filter(rank=1, allowed=path_perm).order_by(
                    "name"
                )
        elif isinstance(obj, Nagah) and obj.auspice:
            auspice_perm = GiftPermission.objects.filter(
                shifter="nagah", condition=obj.auspice
            ).first()
            if auspice_perm:
                context["auspice_gifts"] = Gift.objects.filter(
                    rank=1, allowed=auspice_perm
                ).order_by("name")
        elif isinstance(obj, Ajaba) and obj.auspice:
            auspice_perm = GiftPermission.objects.filter(
                shifter="ajaba", condition=obj.auspice
            ).first()
            if auspice_perm:
                context["auspice_gifts"] = Gift.objects.filter(
                    rank=1, allowed=auspice_perm
                ).order_by("name")
        elif isinstance(obj, Grondr) and obj.auspice:
            auspice_perm = GiftPermission.objects.filter(
                shifter="grondr", condition=obj.auspice
            ).first()
            if auspice_perm:
                context["auspice_gifts"] = Gift.objects.filter(
                    rank=1, allowed=auspice_perm
                ).order_by("name")

        return context

    def form_valid(self, form):
        gifts = form.cleaned_data.get("gifts")
        if gifts.count() != 3:
            form.add_error("gifts", "You must select exactly 3 starting Gifts.")
            return self.form_invalid(form)

        # Validate gift selections are appropriate for the character
        # (Simplified validation - could be more specific per type)
        valid_gifts = Gift.objects.filter(rank=1, allowed__in=self.object.gift_permissions.all())
        for gift in gifts:
            if gift not in valid_gifts:
                form.add_error("gifts", f"{gift.name} is not available to your character.")
                return self.form_invalid(form)

        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class FeraHistoryView(SpecialUserMixin, UpdateView):
    model = Fera
    fields = [
        "first_change",
        "age_of_first_change",
    ]
    template_name = "characters/werewolf/fera/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["first_change"].widget.attrs.update(
            {
                "placeholder": f"Describe your character's First Change. Include where they were, what triggered it, and how they dealt with the immediate aftermath."
            }
        )
        form.fields["first_change"].help_text = (
            "This is a pivotal moment in every shapeshifter's life."
        )
        form.fields["age_of_first_change"].help_text = (
            "The age at which the character first changed forms."
        )
        return form

    def form_valid(self, form):
        first_change = form.cleaned_data.get("first_change")
        age_of_first_change = form.cleaned_data.get("age_of_first_change")

        if not first_change or first_change.strip() == "":
            form.add_error("first_change", "You must describe your First Change.")
            return self.form_invalid(form)

        if age_of_first_change <= 0:
            form.add_error(
                "age_of_first_change",
                "Age of First Change must be greater than 0.",
            )
            return self.form_invalid(form)

        if age_of_first_change >= self.object.age:
            form.add_error(
                "age_of_first_change",
                "Age of First Change must be less than current age.",
            )
            return self.form_invalid(form)

        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)


class FeraExtrasView(SpecialUserMixin, UpdateView):
    model = Fera
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
    template_name = "characters/werewolf/fera/chargen.html"

    def form_valid(self, form):
        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date_of_birth"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["description"].widget.attrs.update(
            {
                "placeholder": "Describe your character's physical appearance in all forms. Be detailed, this will be visible to other players."
            }
        )
        form.fields["history"].widget.attrs.update(
            {
                "placeholder": "Describe character history/backstory. Include information about their upbringing, their First Change (already detailed above), and their role among their kind."
            }
        )
        form.fields["goals"].widget.attrs.update(
            {
                "placeholder": "Describe your character's long and short term goals, whether personal or related to Gaia's war."
            }
        )
        form.fields["notes"].widget.attrs.update({"placeholder": "Notes"})
        form.fields["public_info"].widget.attrs.update(
            {
                "placeholder": "This will be displayed to all players who look at your character. Include Renown, deeds, and anything else that would be publicly known."
            }
        )
        return form


class FeraFreebieFormPopulationView(HumanFreebieFormPopulationView):
    primary_class = Fera


class FeraFreebiesView(HumanFreebiesView):
    model = Fera
    form_class = HumanFreebiesForm
    template_name = "characters/werewolf/fera/chargen.html"


class FeraLanguagesView(HumanLanguagesView):
    template_name = "characters/werewolf/fera/chargen.html"


class FeraAlliesView(GenericBackgroundView):
    primary_object_class = Fera
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/werewolf/fera/chargen.html"


class FeraFetishView(GenericBackgroundView):
    primary_object_class = Fera
    background_name = "fetish"
    form_class = None  # We'll handle this specially
    template_name = "characters/werewolf/fera/chargen.html"
    multiple_ownership = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the current background rating for fetish
        fetish_bg, _ = Background.objects.get_or_create(
            property_name="fetish", defaults={"name": "Fetish"}
        )
        fetish_rating = BackgroundRating.objects.filter(char=self.object, bg=fetish_bg).first()
        if fetish_rating:
            context["max_fetish_rating"] = fetish_rating.rating
            context["current_fetish_total"] = self.object.total_fetish_rating()
        else:
            context["max_fetish_rating"] = 0
            context["current_fetish_total"] = 0
        context["available_fetishes"] = self.object.filter_fetishes(
            min_rating=0,
            max_rating=(fetish_rating.rating if fetish_rating else 0),
        )
        return context


class FeraSpecialtiesView(HumanSpecialtiesView):
    template_name = "characters/werewolf/fera/chargen.html"


class FeraCharacterCreationView(HumanCharacterCreationView):
    view_mapping = {
        1: FeraBreedFactionView,
        2: FeraAttributeView,
        3: FeraAbilityView,
        4: FeraBackgroundsView,
        5: FeraGiftsView,
        6: FeraHistoryView,
        7: FeraExtrasView,
        8: FeraFreebiesView,
        9: FeraLanguagesView,
        10: FeraAlliesView,
        11: FeraSpecialtiesView,
    }
    model_class = Fera
    key_property = "creation_status"
    default_redirect = FeraDetailView

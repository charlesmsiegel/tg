from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView

from characters.chargen.registry import WorkflowViews
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.mage.freebies import CompanionFreebiesForm
from characters.models.core.ability_block import Ability
from characters.models.core.archetype import Archetype
from characters.models.core.attribute_block import Attribute
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.mage.companion import Advantage, Companion
from characters.models.mage.faction import MageFaction
from characters.models.werewolf.charm import SpiritCharm
from characters.views.core.backgrounds import HumanBackgroundsView
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
    XPApprovalMixin,
    prepare_created_object,
)
from core.permissions import Permission, PermissionManager
from items.forms.mage.wonder import WonderForm
from locations.forms.mage.library import LibraryForm
from locations.forms.mage.node import NodeForm
from locations.forms.mage.sanctum import SanctumForm


class CompanionDetailView(XPApprovalMixin, HumanDetailView):
    model = Companion
    template_name = "characters/mage/companion/detail.html"


class CompanionCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    """
    Create view for companions (Mage: The Ascension).

    Security: Uses explicit field whitelist to prevent mass assignment of
    sensitive fields like status, xp, owner, freebies_approved, etc.

    Note: For character creation workflow, use CompanionBasicsView instead.
    """

    model = Companion
    fields = [
        "name",
        "concept",
        "description",
        "public_info",
        "chronicle",
        "companion_type",
        "companion_of",
        "npc",
        "nature",
        "demeanor",
    ]
    template_name = "characters/mage/companion/form.html"
    success_message = "Companion created successfully."
    error_message = "There was an error creating the Companion."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form

    def form_valid(self, form):
        # Set owner to current user - authentication enforced by LoginRequiredMixin
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CompanionUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    """
    Update view for companions.

    - Chronicle Head STs can edit everything (via ST_EDIT_FIELDS)
    - Owners can only edit limited fields (enforced by LimitedHumanEditForm)

    Security: Uses explicit field whitelist to prevent mass assignment attacks.
    """

    model = Companion
    # Fields available to STs with full edit permission
    # Note: owners get LimitedHumanEditForm via get_form_class()
    ST_EDIT_FIELDS = [
        "name",
        "concept",
        "description",
        "public_info",
        "notes",
        "history",
        "goals",
        "chronicle",
        "npc",
        "status",
        "xp",
        "image",
        "st_notes",
        "freebies_approved",
        "display",
        "visibility",
        "nature",
        "demeanor",
        "companion_type",
        "companion_of",
        "willpower",
        "age",
        "apparent_age",
        "date_of_birth",
    ]
    fields = ST_EDIT_FIELDS
    template_name = "characters/mage/companion/form.html"
    success_message = "Companion updated successfully."
    error_message = "There was an error updating the Companion."

    limited_form_class = LimitedHumanEditForm


class CompanionBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, CreateView):
    model = Companion
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "companion_type",
        "chronicle",
        "image",
        "companion_of",
        "npc",
    ]
    template_name = "characters/mage/companion/basics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["storyteller"] = PermissionManager.user_can_manage_creation(
            self.request.user, context["form"], request=self.request
        )
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["nature"].queryset = Archetype.objects.all().order_by("name")
        form.fields["demeanor"].queryset = Archetype.objects.all().order_by("name")
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["concept"].widget.attrs.update({"placeholder": "Enter concept here"})
        form.fields["image"].required = False
        return form

    def form_valid(self, form):
        linked_character = form.instance.companion_of
        if linked_character is not None and (
            linked_character.chronicle_id != form.instance.chronicle_id
            or not (
                linked_character.owner_id == self.request.user.pk
                or PermissionManager.user_has_permission(
                    self.request.user,
                    linked_character,
                    Permission.EDIT_FULL,
                    request=self.request,
                )
            )
        ):
            raise PermissionDenied("Cannot attach a companion to this character")

        prepare_created_object(form, self.request)
        return super().form_valid(form)


class CompanionAttributeView(HumanAttributeView):
    model = Companion
    template_name = "characters/mage/companion/chargen.html"

    primary = 6
    secondary = 4
    tertiary = 3


class CompanionAbilityView(MtAHumanAbilityView):
    model = Companion
    template_name = "characters/mage/companion/chargen.html"

    primary = 11
    secondary = 7
    tertiary = 4


class CompanionBackgroundsView(HumanBackgroundsView):
    template_name = "characters/mage/companion/chargen.html"


class CompanionExtrasView(CharacterExtrasView):
    model = Companion
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
    template_name = "characters/mage/companion/chargen.html"
    field_widget_attrs = {
        "public_info": {
            "placeholder": "This will be displayed to all players who look at your character, include Fame and anything else that would be publicly seen beyond physical description"
        }
    }

    def prepare_character(self, form):
        if self.object.companion_type in ["acoylte", "backup"]:
            self.object.freebies = 15
        elif self.object.companion_type in ["consor", "ally"]:
            self.object.freebies = 21
        elif self.object.companion_type in ["familiar"]:
            if self.object.npc == False:
                self.object.freebies = 25
            thaumivore = get_object_or_404(MeritFlaw, name="Thaumivore")
            bond_sharing = get_object_or_404(Advantage, name="Bond-Sharing")
            paradox_nullification = get_object_or_404(Advantage, name="Paradox Nullification")
            self.object.add_mf(thaumivore, -5)
            self.object.spent_freebies.append(
                self.object.freebie_spend_record(thaumivore.name, "meritflaw", -5, cost=-5)
            )
            self.object.add_advantage(bond_sharing, 4)
            self.object.spent_freebies.append(
                self.object.freebie_spend_record(bond_sharing.name, "advantage", 4, cost=4)
            )
            self.object.add_advantage(paradox_nullification, 2)
            self.object.spent_freebies.append(
                self.object.freebie_spend_record(paradox_nullification.name, "advantage", 2, cost=2)
            )
            self.object.add_charm(get_object_or_404(SpiritCharm, name="Airt Sense"))
            self.object.freebies -= 1


class CompanionFreebiesView(HumanFreebiesView):
    model = Companion
    form_class = CompanionFreebiesForm
    template_name = "characters/mage/companion/chargen.html"
    example_models = {
        **HumanFreebiesView.example_models,
        "Advantage": Advantage,
        "Charm": SpiritCharm,
    }
    category_aliases = {"Charms": "Charm"}


class CompanionLanguagesView(HumanLanguagesView):
    model = Companion
    template_name = "characters/mage/companion/chargen.html"


class CompanionSpecialtiesView(HumanSpecialtiesView):
    model = Companion
    template_name = "characters/mage/companion/chargen.html"

    def get_specialties_needed(self):
        character = self.get_object()
        stats = list(Attribute.objects.all()) + list(Ability.objects.all())
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
        return [x.property_name for x in stats]


class CompanionAlliesView(GenericBackgroundView):
    primary_object_class = Companion
    background_name = "allies"
    form_class = LinkedNPCForm
    template_name = "characters/mage/companion/chargen.html"


class CompanionEnhancementView(MtAEnhancementView):
    template_name = "characters/mage/companion/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["flaw"].required = True
        return form


class CompanionLibraryView(GenericBackgroundView):
    primary_object_class = Companion
    background_name = "library"
    form_class = LibraryForm
    template_name = "characters/mage/companion/chargen.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        obj = get_object_or_404(self.primary_object_class, pk=self.kwargs.get("pk"))
        form.fields["name"].initial = self.current_background.note or f"{obj.name}'s Library"
        form.fields["faction"].queryset = MageFaction.objects.all()
        return form


class CompanionNodeView(GenericBackgroundView):
    primary_object_class = Companion
    background_name = "node"
    form_class = NodeForm
    template_name = "characters/mage/companion/chargen.html"


class CompanionWonderView(GenericBackgroundView):
    primary_object_class = Companion
    background_name = "wonder"
    form_class = WonderForm
    template_name = "characters/mage/companion/chargen.html"
    multiple_ownership = True


class CompanionSanctumView(GenericBackgroundView):
    primary_object_class = Companion
    background_name = "sanctum"
    form_class = SanctumForm
    template_name = "characters/mage/companion/chargen.html"


class CompanionChantryView(CharacterChantryBackgroundView):
    primary_object_class = Companion
    template_name = "characters/mage/companion/chargen.html"


class CopanionCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()

    model_class = Companion
    key_property = "creation_status"
    default_redirect = CompanionDetailView

from characters.forms.core.limited_edit import LimitedEarthboundEditForm
from characters.models.demon import Earthbound
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ViewPermissionMixin,
    VisibilityFilterMixin,
    XPApprovalMixin,
)
from core.permissions import Permission, PermissionManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class EarthboundDetailView(XPApprovalMixin, ViewPermissionMixin, DetailView):
    model = Earthbound
    template_name = "characters/demon/earthbound/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EarthboundCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Earthbound
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
        "awareness",
        "intuition",
        "leadership",
        "seduction",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "performance",
        "security",
        "survival",
        "technology",
        "animal_ken",
        "demolitions",
        "academics",
        "computer",
        "finance",
        "investigation",
        "law",
        "enigmas",
        "medicine",
        "occult",
        "politics",
        "religion",
        "research",
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
        "house",
        "urge_flesh",
        "urge_thought",
        "urge_emotion",
        "faith",
        "temporary_faith",
        "max_faith",
        "torment",
        "temporary_torment",
        "conviction",
        "courage",
        "conscience",
        "reliquary_type",
        "reliquary_description",
        "reliquary_materials",
        "reliquary_max_health",
        "reliquary_current_health",
        "reliquary_soak",
        "can_manifest",
        "manifestation_range",
        "cult_size",
        "worship_ritual_frequency",
        "known_celestial_names",
        "known_true_names",
        "mastery_rating",
        "indoctrination",
        "recall",
        "tactics",
        "torture",
        "celestial_name",
        "date_summoned",
        "time_in_stasis",
    ]
    template_name = "characters/demon/earthbound/form.html"
    success_message = "Earthbound '{name}' created successfully!"
    error_message = "Failed to create earthbound. Please correct the errors below."


class EarthboundUpdateView(EditPermissionMixin, UpdateView):
    model = Earthbound
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
        "awareness",
        "intuition",
        "leadership",
        "seduction",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "performance",
        "security",
        "survival",
        "technology",
        "animal_ken",
        "demolitions",
        "academics",
        "computer",
        "finance",
        "investigation",
        "law",
        "enigmas",
        "medicine",
        "occult",
        "politics",
        "religion",
        "research",
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
        "house",
        "urge_flesh",
        "urge_thought",
        "urge_emotion",
        "faith",
        "temporary_faith",
        "max_faith",
        "torment",
        "temporary_torment",
        "conviction",
        "courage",
        "conscience",
        "reliquary_type",
        "reliquary_description",
        "reliquary_materials",
        "reliquary_max_health",
        "reliquary_current_health",
        "reliquary_soak",
        "can_manifest",
        "manifestation_range",
        "cult_size",
        "worship_ritual_frequency",
        "known_celestial_names",
        "known_true_names",
        "mastery_rating",
        "indoctrination",
        "recall",
        "tactics",
        "torture",
        "celestial_name",
        "date_summoned",
        "time_in_stasis",
    ]
    template_name = "characters/demon/earthbound/form.html"
    success_message = "Earthbound '{name}' updated successfully!"
    error_message = "Failed to update earthbound. Please correct the errors below."

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields (notes, description, etc.) via LimitedEarthboundEditForm.
        STs and admins get full access to all fields via the default form.
        """
        # Check if user has full edit permission
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )

        if has_full_edit:
            # STs and admins get all fields
            return super().get_form_class()
        else:
            # Owners get limited fields (notes, description, public_info, image, history, goals)
            return LimitedEarthboundEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EarthboundListView(VisibilityFilterMixin, ListView):
    model = Earthbound
    template_name = "characters/demon/earthbound/list.html"
    context_object_name = "earthbounds"
    paginate_by = 25

    def get_queryset(self):
        """Get filtered queryset based on permissions."""
        qs = super().get_queryset()
        return qs.select_related("owner", "house", "chronicle").order_by("name")

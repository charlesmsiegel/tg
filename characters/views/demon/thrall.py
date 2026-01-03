from characters.forms.core.limited_edit import LimitedThrallEditForm
from characters.models.demon import Thrall
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
    VisibilityFilterMixin,
    XPApprovalMixin,
)
from core.permissions import Permission, PermissionManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class ThrallDetailView(XPApprovalMixin, ViewPermissionMixin, DetailView):
    model = Thrall
    template_name = "characters/demon/thrall/detail.html"


class ThrallCreateView(MessageMixin, CreateView):
    model = Thrall
    success_message = "Thrall created successfully."
    error_message = "Error creating thrall."
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
        "faith_potential",
        "daily_faith_offered",
        "master",
        "enhancements",
        "conviction",
        "courage",
        "conscience",
    ]
    template_name = "characters/demon/thrall/form.html"


class ThrallUpdateView(EditPermissionMixin, UpdateView):
    model = Thrall
    success_message = "Thrall updated successfully."
    error_message = "Error updating thrall."
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
        "faith_potential",
        "daily_faith_offered",
        "master",
        "enhancements",
        "conviction",
        "courage",
        "conscience",
    ]
    template_name = "characters/demon/thrall/form.html"

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields (notes, description, etc.) via LimitedThrallEditForm.
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
            return LimitedThrallEditForm


class ThrallListView(VisibilityFilterMixin, ListView):
    model = Thrall
    template_name = "characters/demon/thrall/list.html"
    context_object_name = "thralls"
    paginate_by = 25

    def get_queryset(self):
        """Get filtered queryset based on permissions."""
        qs = super().get_queryset()
        return qs.select_related("owner", "master", "chronicle").order_by("name")

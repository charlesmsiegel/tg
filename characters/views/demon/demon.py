from characters.forms.core.limited_edit import LimitedDemonEditForm
from characters.models.demon import Demon
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


class DemonDetailView(XPApprovalMixin, ViewPermissionMixin, DetailView):
    model = Demon
    template_name = "characters/demon/demon/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DemonCreateView(MessageMixin, CreateView):
    model = Demon
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
        "faction",
        "visage",
        "faith",
        "temporary_faith",
        "torment",
        "temporary_torment",
        "conviction",
        "courage",
        "conscience",
        "apocalyptic_form",
        "days_until_consumption",
        "celestial_name",
        "age_of_fall",
        "abyss_duration",
    ]
    template_name = "characters/demon/demon/form.html"
    success_message = "Demon '{name}' created successfully!"
    error_message = "Failed to create demon. Please correct the errors below."

    def get_success_url(self):
        return self.object.get_absolute_url()


class DemonUpdateView(EditPermissionMixin, UpdateView):
    model = Demon
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
        "faction",
        "visage",
        "faith",
        "temporary_faith",
        "torment",
        "temporary_torment",
        "conviction",
        "courage",
        "conscience",
        "apocalyptic_form",
        "days_until_consumption",
        "celestial_name",
        "age_of_fall",
        "abyss_duration",
    ]
    template_name = "characters/demon/demon/form.html"
    success_message = "Demon '{name}' updated successfully!"
    error_message = "Failed to update demon. Please correct the errors below."

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields (notes, description, etc.) via LimitedDemonEditForm.
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
            return LimitedDemonEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DemonListView(VisibilityFilterMixin, ListView):
    model = Demon
    template_name = "characters/demon/demon/list.html"
    context_object_name = "demons"
    paginate_by = 25

    def get_queryset(self):
        """Get filtered queryset based on permissions."""
        qs = super().get_queryset()
        return qs.select_related("owner", "house", "faction", "chronicle").order_by("name")

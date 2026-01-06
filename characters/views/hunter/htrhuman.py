from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.hunter import HtRHuman
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ViewPermissionMixin,
    VisibilityFilterMixin,
    XPApprovalMixin,
)
from core.permissions import Permission, PermissionManager
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class HtRHumanDetailView(XPApprovalMixin, ViewPermissionMixin, DetailView):
    model = HtRHuman
    template_name = "characters/hunter/htrhuman/detail.html"


class HtRHumanCreateView(MessageMixin, CreateView):
    model = HtRHuman
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
        "leadership",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "animal_ken",
        "larceny",
        "performance",
        "repair",
        "survival",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "finance",
        "law",
        "occult",
        "politics",
        "technology",
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
        "allies",
        "influence",
        "resources",
        "status_background",
    ]
    template_name = "characters/hunter/htrhuman/form.html"
    success_message = "Human (Hunter) '{name}' created successfully!"
    error_message = "Failed to create human. Please correct the errors below."

    def get_success_url(self):
        return self.object.get_absolute_url()


class HtRHumanUpdateView(EditPermissionMixin, UpdateView):
    model = HtRHuman
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
        "leadership",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "animal_ken",
        "larceny",
        "performance",
        "repair",
        "survival",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "finance",
        "law",
        "occult",
        "politics",
        "technology",
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
        "allies",
        "influence",
        "resources",
        "status_background",
    ]
    template_name = "characters/hunter/htrhuman/form.html"
    success_message = "Human (Hunter) '{name}' updated successfully!"
    error_message = "Failed to update human. Please correct the errors below."

    def get_form_class(self):
        """Return different form based on user permissions."""
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )
        if has_full_edit:
            return super().get_form_class()
        else:
            return LimitedHumanEditForm


class HtRHumanListView(VisibilityFilterMixin, ListView):
    model = HtRHuman
    template_name = "characters/hunter/htrhuman/list.html"
    context_object_name = "humans"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("owner", "chronicle").order_by("name")

from characters.forms.core.limited_edit import LimitedHunterEditForm
from characters.models.hunter import Hunter
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ViewPermissionMixin,
    VisibilityFilterMixin,
)
from core.permissions import Permission, PermissionManager
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class HunterDetailView(ViewPermissionMixin, DetailView):
    model = Hunter
    template_name = "characters/hunter/hunter/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edges"] = self.object.get_edges()
        return context


class HunterCreateView(MessageMixin, CreateView):
    model = Hunter
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
        "creed",
        "conviction",
        "vision",
        "zeal",
        "temporary_conviction",
        "temporary_vision",
        "temporary_zeal",
        "primary_virtue",
        "imbuing_date",
        "safehouse",
        "discern",
        "burden",
        "balance",
        "expose",
        "investigate",
        "witness",
        "prosecute",
        "illuminate",
        "ward",
        "cleave",
        "hide",
        "blaze",
        "radiate",
        "vengeance",
        "demand",
        "confront",
        "donate",
        "becalm",
        "respire",
        "rejuvenate",
        "redeem",
    ]
    template_name = "characters/hunter/hunter/form.html"
    success_message = "Hunter '{name}' created successfully!"
    error_message = "Failed to create hunter. Please correct the errors below."


class HunterUpdateView(EditPermissionMixin, UpdateView):
    model = Hunter
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
        "creed",
        "conviction",
        "vision",
        "zeal",
        "temporary_conviction",
        "temporary_vision",
        "temporary_zeal",
        "primary_virtue",
        "imbuing_date",
        "safehouse",
        "discern",
        "burden",
        "balance",
        "expose",
        "investigate",
        "witness",
        "prosecute",
        "illuminate",
        "ward",
        "cleave",
        "hide",
        "blaze",
        "radiate",
        "vengeance",
        "demand",
        "confront",
        "donate",
        "becalm",
        "respire",
        "rejuvenate",
        "redeem",
    ]
    template_name = "characters/hunter/hunter/form.html"
    success_message = "Hunter '{name}' updated successfully!"
    error_message = "Failed to update hunter. Please correct the errors below."

    def get_form_class(self):
        """Return different form based on user permissions."""
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )
        if has_full_edit:
            return super().get_form_class()
        else:
            return LimitedHunterEditForm


class HunterListView(VisibilityFilterMixin, ListView):
    model = Hunter
    template_name = "characters/hunter/hunter/list.html"
    context_object_name = "hunters"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("owner", "creed", "chronicle").order_by("name")

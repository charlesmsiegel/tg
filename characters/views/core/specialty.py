from characters.models.core import Specialty
from characters.models.core.statistic import Statistic
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class SpecialtyDetailView(DetailView):
    model = Specialty
    template_name = "characters/core/specialty/detail.html"


class SpecialtyCreateView(MessageMixin, CreateView):
    model = Specialty
    fields = ["name", "stat"]
    template_name = "characters/core/specialty/form.html"
    success_message = "Specialty '{name}' created successfully!"
    error_message = "Failed to create Specialty. Please correct the errors below."


class SpecialtyUpdateView(MessageMixin, UpdateView):
    model = Specialty
    fields = ["name", "stat"]
    template_name = "characters/core/specialty/form.html"
    success_message = "Specialty '{name}' updated successfully!"
    error_message = "Failed to update Specialty. Please correct the errors below."


class SpecialtyListView(ListView):
    model = Specialty
    ordering = ["name"]
    template_name = "characters/core/specialty/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by stat type (Ability, Attribute, Background)
        stat_type = self.request.GET.get("stat_type", "")
        if stat_type:
            # Get all property_names for the selected stat type
            if stat_type == "ability":
                stat_property_names = list(Ability.objects.values_list("property_name", flat=True))
            elif stat_type == "attribute":
                stat_property_names = list(Attribute.objects.values_list("property_name", flat=True))
            elif stat_type == "background":
                stat_property_names = list(Background.objects.values_list("property_name", flat=True))
            else:
                stat_property_names = []

            if stat_property_names:
                queryset = queryset.filter(stat__in=stat_property_names)

        # Filter by specific statistic
        specific_stat = self.request.GET.get("stat", "")
        if specific_stat:
            queryset = queryset.filter(stat=specific_stat)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all stat types for the filter dropdown
        context["stat_types"] = [
            ("ability", "Ability"),
            ("attribute", "Attribute"),
            ("background", "Background"),
        ]

        # Get all unique stats from specialties for the specific stat filter
        all_stats = Specialty.objects.values_list("stat", flat=True).distinct().order_by("stat")

        # Map stat property_names to their display names
        stat_choices = []
        for stat_prop in all_stats:
            stat_obj = Statistic.objects.filter(property_name=stat_prop).first()
            if stat_obj:
                stat_choices.append((stat_prop, stat_obj.name))
            else:
                stat_choices.append((stat_prop, stat_prop.replace("_", " ").title()))

        context["stat_choices"] = sorted(stat_choices, key=lambda x: x[1])

        # Preserve current filter selections
        context["current_stat_type"] = self.request.GET.get("stat_type", "")
        context["current_stat"] = self.request.GET.get("stat", "")

        return context

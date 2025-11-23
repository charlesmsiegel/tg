from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.demon.relic import Relic


class RelicDetailView(DetailView):
    model = Relic
    template_name = "items/demon/relic/detail.html"


class RelicListView(ListView):
    model = Relic
    ordering = ["name"]
    template_name = "items/demon/relic/list.html"


class RelicCreateView(MessageMixin, CreateView):
    model = Relic
    fields = [
        "name",
        "description",
        "relic_type",
        "complexity",
        "lore_used",
        "power",
        "material",
        "house",
        "is_permanent",
        "difficulty",
        "dice_pool",
    ]
    template_name = "items/demon/relic/form.html"
    success_message = "Relic '{name}' created successfully!"
    error_message = "Failed to create relic. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class RelicUpdateView(MessageMixin, UpdateView):
    model = Relic
    fields = [
        "name",
        "description",
        "relic_type",
        "complexity",
        "lore_used",
        "power",
        "material",
        "house",
        "is_permanent",
        "difficulty",
        "dice_pool",
    ]
    template_name = "items/demon/relic/form.html"
    success_message = "Relic '{name}' updated successfully!"
    error_message = "Failed to update relic. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form

from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.core import City


class CityDetailView(DetailView):
    model = City
    template_name = "locations/core/city/detail.html"


class CityListView(ListView):
    model = City
    ordering = ["name"]
    template_name = "locations/core/city/list.html"


class CityCreateView(MessageMixin, CreateView):
    model = City
    fields = [
        "name",
        "description",
        "parent",
        "gauntlet",
        "shroud",
        "dimension_barrier",
        "description",
        "population",
        "mood",
        "theme",
        "media",
        "politicians",
        "characters",
    ]
    template_name = "locations/core/city/form.html"
    success_message = "City '{name}' created successfully!"
    error_message = "Failed to create city. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["mood"].widget.attrs.update({"placeholder": "Enter mood here"})
        form.fields["theme"].widget.attrs.update({"placeholder": "Enter theme here"})
        form.fields["media"].widget.attrs.update({"placeholder": "Enter media here"})
        form.fields["politicians"].widget.attrs.update(
            {"placeholder": "Enter politicians here"}
        )
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form


class CityUpdateView(MessageMixin, UpdateView):
    model = City
    fields = [
        "name",
        "description",
        "parent",
        "gauntlet",
        "shroud",
        "dimension_barrier",
        "description",
        "population",
        "mood",
        "theme",
        "media",
        "politicians",
        "characters",
    ]
    template_name = "locations/core/city/form.html"
    success_message = "City '{name}' updated successfully!"
    error_message = "Failed to update city. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["mood"].widget.attrs.update({"placeholder": "Enter mood here"})
        form.fields["theme"].widget.attrs.update({"placeholder": "Enter theme here"})
        form.fields["media"].widget.attrs.update({"placeholder": "Enter media here"})
        form.fields["politicians"].widget.attrs.update(
            {"placeholder": "Enter politicians here"}
        )
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form

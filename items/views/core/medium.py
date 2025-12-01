from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.core import Medium


class MediumDetailView(DetailView):
    model = Medium
    template_name = "items/core/medium/detail.html"


class MediumCreateView(MessageMixin, CreateView):
    model = Medium
    fields = "__all__"
    template_name = "items/core/medium/form.html"
    success_message = "Medium '{name}' created successfully!"
    error_message = "Failed to create Medium. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here", "rows": 1})
        return form


class MediumUpdateView(MessageMixin, UpdateView):
    model = Medium
    fields = "__all__"
    template_name = "items/core/medium/form.html"
    success_message = "Medium '{name}' updated successfully!"
    error_message = "Failed to update Medium. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here", "rows": 1})
        return form


class MediumListView(ListView):
    model = Medium
    ordering = ["name"]
    template_name = "items/core/medium/list.html"

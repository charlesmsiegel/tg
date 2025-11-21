from django.views.generic import CreateView, DetailView, UpdateView

from core.views.message_mixin import MessageMixin
from items.models.core import ItemModel


class ItemDetailView(DetailView):
    model = ItemModel
    template_name = "items/core/item/detail.html"


class ItemCreateView(MessageMixin, CreateView):
    model = ItemModel
    fields = ["name", "description"]
    template_name = "items/core/item/form.html"
    success_message = "Item '{name}' created successfully!"
    error_message = "Failed to create Item. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class ItemUpdateView(MessageMixin, UpdateView):
    model = ItemModel
    fields = ["name", "description"]
    template_name = "items/core/item/form.html"
    success_message = "Item '{name}' updated successfully!"
    error_message = "Failed to update Item. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form

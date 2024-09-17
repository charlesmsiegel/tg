from django.views.generic import CreateView, DetailView, UpdateView
from items.models.core import ItemModel


class ItemDetailView(DetailView):
    model = ItemModel
    template_name = "items/core/item/detail.html"


class ItemCreateView(CreateView):
    model = ItemModel
    fields = ["name", "description"]
    template_name = "items/core/item/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class ItemUpdateView(UpdateView):
    model = ItemModel
    fields = ["name", "description"]
    template_name = "items/core/item/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form

from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.core import Weapon


class WeaponDetailView(DetailView):
    model = Weapon
    template_name = "items/core/weapon/detail.html"


class WeaponListView(ListView):
    model = Weapon
    ordering = ["name"]
    template_name = "items/core/weapon/list.html"


class WeaponCreateView(MessageMixin, CreateView):
    model = Weapon
    fields = ["name", "description", "difficulty", "damage", "damage_type", "conceal"]
    template_name = "items/core/weapon/form.html"
    success_message = "Weapon '{name}' created successfully!"
    error_message = "Failed to create Weapon. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class WeaponUpdateView(MessageMixin, UpdateView):
    model = Weapon
    fields = ["name", "description", "difficulty", "damage", "damage_type", "conceal"]
    template_name = "items/core/weapon/form.html"
    success_message = "Weapon '{name}' updated successfully!"
    error_message = "Failed to update Weapon. Please correct the errors below."

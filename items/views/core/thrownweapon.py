from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.core import ThrownWeapon


class ThrownWeaponDetailView(DetailView):
    model = ThrownWeapon
    template_name = "items/core/thrownweapon/detail.html"


class ThrownWeaponListView(ListView):
    model = ThrownWeapon
    ordering = ["name"]
    template_name = "items/core/thrownweapon/list.html"


class ThrownWeaponCreateView(MessageMixin, CreateView):
    model = ThrownWeapon
    fields = ["name", "description", "difficulty", "damage", "damage_type", "conceal"]
    template_name = "items/core/thrownweapon/form.html"
    success_message = "Thrown Weapon '{name}' created successfully!"
    error_message = "Failed to create Thrown Weapon. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class ThrownWeaponUpdateView(MessageMixin, UpdateView):
    model = ThrownWeapon
    fields = ["name", "description", "difficulty", "damage", "damage_type", "conceal"]
    template_name = "items/core/thrownweapon/form.html"
    success_message = "Thrown Weapon '{name}' updated successfully!"
    error_message = "Failed to update Thrown Weapon. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form

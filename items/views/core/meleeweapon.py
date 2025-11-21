from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.views.message_mixin import MessageMixin
from items.models.core import MeleeWeapon


class MeleeWeaponDetailView(DetailView):
    model = MeleeWeapon
    template_name = "items/core/meleeweapon/detail.html"


class MeleeWeaponListView(ListView):
    model = MeleeWeapon
    ordering = ["name"]
    template_name = "items/core/meleeweapon/list.html"


class MeleeWeaponCreateView(MessageMixin, CreateView):
    model = MeleeWeapon
    fields = ["name", "description", "difficulty", "damage", "damage_type", "conceal"]
    template_name = "items/core/meleeweapon/form.html"
    success_message = "Melee Weapon '{name}' created successfully!"
    error_message = "Failed to create Melee Weapon. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class MeleeWeaponUpdateView(MessageMixin, UpdateView):
    model = MeleeWeapon
    fields = ["name", "description", "difficulty", "damage", "damage_type", "conceal"]
    template_name = "items/core/meleeweapon/form.html"
    success_message = "Melee Weapon '{name}' updated successfully!"
    error_message = "Failed to update Melee Weapon. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form

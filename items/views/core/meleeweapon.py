from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.core import MeleeWeapon


class MeleeWeaponDetailView(DetailView):
    model = MeleeWeapon
    template_name = "items/core/meleeweapon/detail.html"


class MeleeWeaponListView(ListView):
    model = MeleeWeapon
    ordering = ["name"]
    template_name = "items/core/meleeweapon/list.html"


class MeleeWeaponCreateView(CreateView):
    model = MeleeWeapon
    fields = ["name", "description", "difficulty", "damage", "damage_type", "conceal"]
    template_name = "items/core/meleeweapon/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class MeleeWeaponUpdateView(UpdateView):
    model = MeleeWeapon
    fields = ["name", "description", "difficulty", "damage", "damage_type", "conceal"]
    template_name = "items/core/meleeweapon/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form

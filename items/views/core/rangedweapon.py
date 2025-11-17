from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.core import RangedWeapon


class RangedWeaponDetailView(DetailView):
    model = RangedWeapon
    template_name = "items/core/rangedweapon/detail.html"


class RangedWeaponListView(ListView):
    model = RangedWeapon
    ordering = ["name"]
    template_name = "items/core/rangedweapon/list.html"


class RangedWeaponCreateView(CreateView):
    model = RangedWeapon
    fields = [
        "name",
        "description",
        "difficulty",
        "damage",
        "damage_type",
        "conceal",
        "range",
        "rate",
        "clip",
    ]
    template_name = "items/core/rangedweapon/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class RangedWeaponUpdateView(UpdateView):
    model = RangedWeapon
    fields = [
        "name",
        "description",
        "difficulty",
        "damage",
        "damage_type",
        "conceal",
        "range",
        "rate",
        "clip",
    ]
    template_name = "items/core/rangedweapon/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form

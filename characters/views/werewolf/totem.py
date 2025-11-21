from characters.models.werewolf.totem import Totem
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class TotemDetailView(DetailView):
    model = Totem
    template_name = "characters/werewolf/totem/detail.html"


class TotemCreateView(MessageMixin, CreateView):
    model = Totem
    fields = [
        "name",
        "description",
        "cost",
        "totem_type",
        "individual_traits",
        "pack_traits",
        "ban",
    ]
    template_name = "characters/werewolf/totem/form.html"
    success_message = "Totem created successfully."
    error_message = "There was an error creating the Totem."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["individual_traits"].widget.attrs.update(
            {"placeholder": "Enter individual traits here"}
        )
        form.fields["pack_traits"].widget.attrs.update(
            {"placeholder": "Enter pack traits here"}
        )
        form.fields["ban"].widget.attrs.update({"placeholder": "Enter ban here"})
        return form


class TotemUpdateView(MessageMixin, UpdateView):
    model = Totem
    fields = [
        "name",
        "description",
        "cost",
        "totem_type",
        "individual_traits",
        "pack_traits",
        "ban",
    ]
    template_name = "characters/werewolf/totem/form.html"
    success_message = "Totem updated successfully."
    error_message = "There was an error updating the Totem."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["individual_traits"].widget.attrs.update(
            {"placeholder": "Enter individual traits here"}
        )
        form.fields["pack_traits"].widget.attrs.update(
            {"placeholder": "Enter pack traits here"}
        )
        form.fields["ban"].widget.attrs.update({"placeholder": "Enter ban here"})
        return form


class TotemListView(ListView):
    model = Totem
    ordering = ["name"]
    template_name = "characters/werewolf/totem/list.html"

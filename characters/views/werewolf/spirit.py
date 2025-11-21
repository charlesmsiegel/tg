from characters.models.werewolf.spirit_character import SpiritCharacter
from core.mixins import ViewPermissionMixin, EditPermissionMixin, SpendFreebiesPermissionMixin, SpendXPPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView


class SpiritDetailView(ViewPermissionMixin, DetailView):
    model = SpiritCharacter
    template_name = "characters/werewolf/spirit/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = True  # If we got here, user has permission
        return context


class SpiritCreateView(MessageMixin, CreateView):
    model = SpiritCharacter
    fields = ["name", "description", "willpower", "rage", "gnosis", "essence", "owner"]
    template_name = "characters/werewolf/spirit/form.html"
    success_message = "Spirit created successfully."
    error_message = "There was an error creating the Spirit."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class SpiritUpdateView(EditPermissionMixin, UpdateView):
    model = SpiritCharacter
    fields = ["name", "description", "willpower", "rage", "gnosis", "essence", "owner"]
    template_name = "characters/werewolf/spirit/form.html"
    success_message = "Spirit updated successfully."
    error_message = "There was an error updating the Spirit."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = True  # If we got here, user has permission
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form

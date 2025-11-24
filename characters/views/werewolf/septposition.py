from characters.forms.werewolf.septposition import SeptPositionForm
from characters.models.werewolf.septposition import SeptPosition
from core.mixins import MessageMixin, ViewPermissionMixin
from django.views.generic import CreateView, DetailView, UpdateView


class SeptPositionDetailView(ViewPermissionMixin, DetailView):
    model = SeptPosition
    template_name = "characters/werewolf/septposition/detail.html"


class SeptPositionCreateView(MessageMixin, CreateView):
    model = SeptPosition
    form_class = SeptPositionForm
    template_name = "characters/werewolf/septposition/form.html"
    success_message = "Sept Position created successfully."


class SeptPositionUpdateView(MessageMixin, UpdateView):
    model = SeptPosition
    form_class = SeptPositionForm
    template_name = "characters/werewolf/septposition/form.html"
    success_message = "Sept Position updated successfully."

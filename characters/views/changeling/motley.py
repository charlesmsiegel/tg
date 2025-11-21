from characters.models.changeling.motley import Motley
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, UpdateView


class MotleyDetailView(DetailView):
    model = Motley
    template_name = "characters/changeling/motley/detail.html"


class MotleyCreateView(MessageMixin, CreateView):
    model = Motley
    fields = ["name", "description", "members", "leader"]
    template_name = "characters/changeling/motley/form.html"
    success_message = "Motley created successfully."
    error_message = "There was an error creating the Motley."


class MotleyUpdateView(MessageMixin, UpdateView):
    model = Motley
    fields = ["name", "description", "members", "leader"]
    template_name = "characters/changeling/motley/form.html"
    success_message = "Motley updated successfully."
    error_message = "There was an error updating the Motley."

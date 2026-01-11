from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.werewolf.camp import Camp
from core.mixins import MessageMixin


class CampDetailView(DetailView):
    model = Camp
    template_name = "characters/werewolf/camp/detail.html"


class CampCreateView(MessageMixin, CreateView):
    model = Camp
    fields = ["name", "description", "tribe", "camp_type"]
    template_name = "characters/werewolf/camp/form.html"
    success_message = "Camp created successfully."
    error_message = "There was an error creating the Camp."


class CampUpdateView(MessageMixin, UpdateView):
    model = Camp
    fields = ["name", "description", "tribe", "camp_type"]
    template_name = "characters/werewolf/camp/form.html"
    success_message = "Camp updated successfully."
    error_message = "There was an error updating the Camp."


class CampListView(ListView):
    model = Camp
    ordering = ["name"]
    template_name = "characters/werewolf/camp/list.html"

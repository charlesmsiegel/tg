from characters.models.changeling.nunnehi import Nunnehi
from characters.views.core.human import HumanDetailView
from core.mixins import EditPermissionMixin, MessageMixin
from django.views.generic import CreateView, UpdateView


class NunnehiDetailView(HumanDetailView):
    model = Nunnehi
    template_name = "characters/changeling/nunnehi/detail.html"


class NunnehiCreateView(MessageMixin, CreateView):
    model = Nunnehi
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "family",
        "nunnehi_seeming",
        "camp",
    ]
    template_name = "characters/changeling/nunnehi/form.html"
    success_message = "Nunnehi '{name}' created successfully!"
    error_message = "Failed to create nunnehi. Please correct the errors below."


class NunnehiUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Nunnehi
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "family",
        "nunnehi_seeming",
        "camp",
        "spirit_medicine",
        "sacred_place",
        "tribal_duty",
    ]
    template_name = "characters/changeling/nunnehi/form.html"
    success_message = "Nunnehi '{name}' updated successfully!"
    error_message = "Failed to update nunnehi. Please correct the errors below."

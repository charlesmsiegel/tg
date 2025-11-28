from characters.models.changeling.autumn_person import AutumnPerson
from characters.views.core.human import HumanDetailView
from core.mixins import EditPermissionMixin, MessageMixin
from django.views.generic import CreateView, UpdateView


class AutumnPersonDetailView(HumanDetailView):
    model = AutumnPerson
    template_name = "characters/changeling/autumn_person/detail.html"


class AutumnPersonCreateView(MessageMixin, CreateView):
    model = AutumnPerson
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "archetype",
        "awareness",
        "banality_rating",
    ]
    template_name = "characters/changeling/autumn_person/form.html"
    success_message = "Autumn Person '{name}' created successfully!"
    error_message = "Failed to create autumn person. Please correct the errors below."


class AutumnPersonUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = AutumnPerson
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "archetype",
        "awareness",
        "banality_rating",
        "organization",
        "motivation",
        "sphere_of_influence",
        "is_dauntain",
        "former_kith",
    ]
    template_name = "characters/changeling/autumn_person/form.html"
    success_message = "Autumn Person '{name}' updated successfully!"
    error_message = "Failed to update autumn person. Please correct the errors below."

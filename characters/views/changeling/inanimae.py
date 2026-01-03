from characters.models.changeling.inanimae import Inanimae
from characters.views.core.human import HumanDetailView
from core.mixins import EditPermissionMixin, MessageMixin, XPApprovalMixin
from django.views.generic import CreateView, UpdateView


class InanimaeDetailView(XPApprovalMixin, HumanDetailView):
    model = Inanimae
    template_name = "characters/changeling/inanimae/detail.html"


class InanimaeCreateView(MessageMixin, CreateView):
    model = Inanimae
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "kingdom",
        "inanimae_seeming",
        "season",
    ]
    template_name = "characters/changeling/inanimae/form.html"
    success_message = "Inanimae '{name}' created successfully!"
    error_message = "Failed to create inanimae. Please correct the errors below."


class InanimaeUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Inanimae
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "kingdom",
        "inanimae_seeming",
        "season",
        "mana",
        "anchor_description",
        "elemental_strength",
        "elemental_weakness",
    ]
    template_name = "characters/changeling/inanimae/form.html"
    success_message = "Inanimae '{name}' updated successfully!"
    error_message = "Failed to update inanimae. Please correct the errors below."

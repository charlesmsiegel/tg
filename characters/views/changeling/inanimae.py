from django.views.generic import CreateView, UpdateView

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.changeling.inanimae import Inanimae
from characters.views.core.human import HumanDetailView
from core.mixins import EditPermissionMixin, MessageMixin, XPApprovalMixin
from core.permissions import Permission, PermissionManager


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

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields via LimitedHumanEditForm.
        STs and admins get full access via the default form.
        """
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )
        if has_full_edit:
            return super().get_form_class()
        else:
            return LimitedHumanEditForm

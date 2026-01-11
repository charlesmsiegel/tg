from django.views.generic import CreateView, UpdateView

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.changeling.nunnehi import Nunnehi
from characters.views.core.human import HumanDetailView
from core.mixins import EditPermissionMixin, MessageMixin, XPApprovalMixin
from core.permissions import Permission, PermissionManager


class NunnehiDetailView(XPApprovalMixin, HumanDetailView):
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
        "tribe",
        "nunnehi_seeming",
        "path",
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
        "tribe",
        "nunnehi_seeming",
        "path",
        "spirit_medicine",
        "sacred_place",
        "spirit_guide",
        "tribal_duty",
    ]
    template_name = "characters/changeling/nunnehi/form.html"
    success_message = "Nunnehi '{name}' updated successfully!"
    error_message = "Failed to update nunnehi. Please correct the errors below."

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

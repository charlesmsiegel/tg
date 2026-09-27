"""Character sheet actions: one URL, permission and service call each."""

from django.contrib import messages
from django.shortcuts import redirect

from characters.forms.core.specialty import SpecialtiesForm
from characters.models.core import Character
from characters.models.core.human import Human
from characters.services.specialties import record_specialties
from characters.services.status import change_character_status
from core.actions import ActionFailed, ObjectActionView
from core.permissions import Permission, PermissionManager
from game.models import XPSpendingRequest
from game.spending_approval import (
    SpendingAlreadyDecided,
    SpendingDecisionError,
    can_approve_spending,
    decide_spending_request,
)


class XPRequestDecisionView(ObjectActionView):
    """Approve or deny one pending XP spending request of this character."""

    model = Character
    decision = None

    def has_permission(self, subject):
        return can_approve_spending(self.request.user, subject, request=self.request)

    def perform(self, form):
        try:
            return decide_spending_request(
                XPSpendingRequest,
                self.object,
                self.kwargs["request_pk"],
                self.request.user,
                self.decision,
            )
        except SpendingAlreadyDecided:
            raise
        except SpendingDecisionError as exc:
            raise ActionFailed(str(exc)) from exc

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except SpendingAlreadyDecided as exc:
            # A double submit or a concurrent decision: nothing to do.
            messages.warning(request, str(exc))
            return redirect(self.get_success_url())


class XPRequestApproveView(XPRequestDecisionView):
    decision = "approve"


class XPRequestRejectView(XPRequestDecisionView):
    decision = "deny"


class CharacterStatusView(ObjectActionView):
    """Move the character to ``target_status`` under a row lock."""

    model = Character
    lock = True
    target_status = None

    def perform(self, form):
        return change_character_status(self.object, self.target_status)


class CharacterRetireView(CharacterStatusView):
    """The owner, or a storyteller for this chronicle and gameline, retires a character."""

    target_status = "Ret"

    def has_permission(self, subject):
        return subject.owner_id == self.request.user.pk or (
            PermissionManager.user_has_scoped_editor_role(
                self.request.user, subject, request=self.request
            )
        )


class CharacterDeceaseView(CharacterStatusView):
    """Only a storyteller for this chronicle and gameline marks a character deceased."""

    target_status = "Dec"

    def has_permission(self, subject):
        return PermissionManager.user_has_scoped_editor_role(
            self.request.user, subject, request=self.request
        )


class CharacterSpecialtiesView(ObjectActionView):
    """Record the specialties the character's ratings call for."""

    model = Human
    permission = Permission.EDIT_FULL
    form_class = SpecialtiesForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop("files")
        kwargs["object"] = self.object
        kwargs["specialties_needed"] = self.object.needed_specialties()
        return kwargs

    def get_form(self):
        form = super().get_form()
        # A player may fill in only some of the needed specialties at a time.
        for field in form.fields.values():
            field.required = False
        return form

    def perform(self, form):
        return record_specialties(self.object, form.cleaned_data)

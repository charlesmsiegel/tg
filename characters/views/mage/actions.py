"""Mage sheet actions."""

from characters.forms.mage.rote import RoteCreationForm
from characters.forms.mage.xp import MageXPForm
from characters.models.mage.mage import Mage
from characters.services.mage_xp import spend_mage_xp
from characters.views.mage.mage import MageDetailView
from core.actions import ObjectActionView
from core.permissions import Permission


class MageXPSpendView(ObjectActionView):
    """Spend XP or rote points from the Mage sheet; errors re-render the sheet."""

    model = Mage
    permission = Permission.SPEND_XP
    form_class = MageXPForm
    host_view_class = MageDetailView
    rote_form = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = self.object
        return kwargs

    def is_valid(self, form):
        if not form.is_valid():
            return False
        if form.cleaned_data["category"] == "Rote":
            self.rote_form = RoteCreationForm(self.request.POST, instance=self.object)
            return self.rote_form.is_valid()
        return True

    def perform(self, form):
        rote_data = self.rote_form.cleaned_data if self.rote_form is not None else None
        return spend_mage_xp(self.object, form.cleaned_data, rote_data)

    def action_failed(self, error, form=None):
        # A refused rote belongs on the rote form, where the old sheet showed it.
        if self.rote_form is not None and self.fragment_response(form=form, error=error) is None:
            self.rote_form.add_error(None, error)
            return self.render_host(form)
        return super().action_failed(error, form)

    def get_host_context(self, form):
        context = super().get_host_context(form)
        if self.rote_form is not None:
            context["rote_form"] = self.rote_form
        return context

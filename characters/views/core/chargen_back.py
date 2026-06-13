"""View for going back one step in character creation."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from characters.models.core import Character
from characters.models.core.human import Human


class ChargenBackView(LoginRequiredMixin, View):
    """Go back one step in character creation. POST only."""

    http_method_names = ["post"]

    def post(self, request, pk):
        with transaction.atomic():
            char = get_object_or_404(Character, pk=pk)
            if char.owner != request.user:
                raise PermissionDenied
            # Redirect through the generic character router, not
            # get_absolute_url: several subclasses (Vampire, Ghoul, Wraith,
            # Demon, Thrall, ...) override get_absolute_url to a plain detail
            # route, which would drop the user out of chargen. The router
            # dispatches Un characters to the step matching creation_status.
            destination = redirect("characters:character", pk=char.pk)
            # Lock and refresh BEFORE the state checks so concurrent Back POSTs
            # (and a concurrent ST freebie approval) serialize: otherwise two
            # requests from the same step could both pass the lower-bound check
            # and decrement twice. Human.objects locks both the Human and
            # Character rows (the latter holding creation_status); non-Human
            # characters lock the Character row. freebies_approved is also on
            # the Human row, matching award_backstory_freebies's lock.
            if isinstance(char, Human):
                char = Human.objects.select_for_update().get(pk=char.pk)
            else:
                char = Character.objects.select_for_update().get(pk=char.pk)
            if char.status != "Un":
                messages.warning(
                    request,
                    "Cannot change creation steps once a character is submitted.",
                )
                return destination
            if char.creation_status <= 1:
                return destination
            # Once freebies are approved, block back navigation entirely: any
            # earlier step could invalidate the locked allocation. We do not
            # key this on freebie_step — that class attribute diverges from the
            # real per-gameline freebie step in several creation routers.
            if getattr(char, "freebies_approved", False):
                messages.warning(
                    request, "Cannot navigate back once freebies are approved."
                )
                return destination
            char.prev_stage()
        return destination

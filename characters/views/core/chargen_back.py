"""View for going back one step in character creation."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from characters.models.core import Character


class ChargenBackView(LoginRequiredMixin, View):
    """Go back one step in character creation. POST only."""

    http_method_names = ["post"]

    def post(self, request, pk):
        char = get_object_or_404(Character, pk=pk)
        if char.owner != request.user:
            raise PermissionDenied
        # Redirect through the generic character router, not get_absolute_url:
        # several subclasses (Vampire, Ghoul, Wraith, Demon, Thrall, ...)
        # override get_absolute_url to a plain detail route, which would drop
        # the user out of chargen. The router dispatches Un characters to the
        # creation step matching the (decremented) creation_status.
        destination = redirect("characters:character", pk=char.pk)
        if char.status != "Un":
            messages.warning(
                request, "Cannot change creation steps once a character is submitted."
            )
            return destination
        if char.creation_status <= 1:
            return destination
        # Once freebies are approved, block back navigation entirely: any
        # earlier step could invalidate the locked allocation. We do not key
        # this on freebie_step — that class attribute diverges from the real
        # per-gameline freebie step in several creation routers.
        if getattr(char, "freebies_approved", False):
            messages.warning(
                request, "Cannot navigate back once freebies are approved."
            )
            return destination
        char.prev_stage()
        return destination

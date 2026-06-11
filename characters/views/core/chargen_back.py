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
        if char.status != "Un":
            messages.warning(
                request, "Cannot change creation steps once a character is submitted."
            )
            return redirect(char.get_absolute_url())
        if char.creation_status <= 1:
            return redirect(char.get_absolute_url())
        # Once freebies are approved, block navigation to the freebie step
        # AND any step before it (target <= freebie_step), since earlier
        # steps could invalidate the approved freebie allocation.
        target = char.creation_status - 1
        freebie_step = getattr(char, "freebie_step", -1)
        if freebie_step > 0 and target <= freebie_step:
            if getattr(char, "freebies_approved", False):
                messages.warning(
                    request,
                    "Cannot go back past the freebie step once freebies are approved.",
                )
                return redirect(char.get_absolute_url())
        char.prev_stage()
        return redirect(char.get_absolute_url())

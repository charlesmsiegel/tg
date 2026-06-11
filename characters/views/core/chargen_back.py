"""View for going back one step in character creation."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from characters.models.core import Character


class ChargenBackView(LoginRequiredMixin, View):
    """Go back one step in character creation. POST only."""

    def post(self, request, pk):
        char = get_object_or_404(Character, pk=pk)
        if char.owner != request.user:
            raise PermissionDenied
        if char.status != "Un":
            return redirect(char.get_absolute_url())
        if char.creation_status <= 1:
            return redirect(char.get_absolute_url())
        # Prevent going back into the freebie step once freebies are locked in
        target = char.creation_status - 1
        freebie_step = getattr(char, "freebie_step", -1)
        if freebie_step > 0 and target <= freebie_step:
            if getattr(char, "freebies_approved", False):
                return redirect(char.get_absolute_url())
        char.prev_stage()
        return redirect(char.get_absolute_url())

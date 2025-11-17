from characters.forms.core.npc_profile import NPCProfileForm
from characters.models.core import Character
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View


class NPCProfileCreateView(LoginRequiredMixin, View):
    """
    View for creating NPC profiles of any character type.
    Provides a unified interface for creating mentors, contacts, allies, and other NPCs.
    """

    template_name = "characters/core/npc/create.html"

    def get(self, request, pk=None):
        """Display the NPC profile creation form."""
        related_character = None
        if pk:
            related_character = get_object_or_404(Character, pk=pk)

        form = NPCProfileForm(user=request.user, related_character=related_character)

        context = {
            "form": form,
            "related_character": related_character,
        }

        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        """Handle NPC profile creation."""
        related_character = None
        if pk:
            related_character = get_object_or_404(Character, pk=pk)

        form = NPCProfileForm(
            request.POST,
            request.FILES,
            user=request.user,
            related_character=related_character,
        )

        if form.is_valid():
            npc = form.save()
            messages.success(
                request, f'NPC "{npc.name}" has been created successfully.'
            )
            return redirect(npc.get_absolute_url())

        context = {
            "form": form,
            "related_character": related_character,
        }

        return render(request, self.template_name, context)

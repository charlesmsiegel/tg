from typing import Any

from characters.models.core import Character
from core.views.approved_user_mixin import SpecialUserMixin
from core.views.message_mixin import MessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from game.models import Scene


class CharacterDetailView(SpecialUserMixin, DetailView):
    model = Character
    template_name = "characters/core/character/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["scenes"] = Scene.objects.filter(characters=context["object"]).order_by(
            "-date_of_scene"
        )
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Handle retirement and death status changes
        if "retire" in request.POST:
            self.object.status = "Ret"
            self.object.save()
        if "decease" in request.POST:
            self.object.status = "Dec"
            self.object.save()
        return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))


class CharacterCreateView(MessageMixin, CreateView):
    model = Character
    fields = "__all__"
    template_name = "characters/core/character/form.html"
    success_message = "Character '{name}' created successfully!"
    error_message = "Failed to create Character. Please correct the errors below."


class CharacterUpdateView(MessageMixin, SpecialUserMixin, UpdateView):
    model = Character
    fields = "__all__"
    template_name = "characters/core/character/form.html"
    success_message = "Character '{name}' updated successfully!"
    error_message = "Failed to update Character. Please correct the errors below."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context

from typing import Any

from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from characters.chargen.transitions import advance
from characters.forms.mage.enhancements import EnhancementForm
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from characters.views.core.chargen_mixins import ChargenStepMixin
from characters.views.core.generic_background import GenericBackgroundView
from core.mixins import (
    SpendFreebiesPermissionMixin,
)
from locations.forms.mage.chantry import ChantrySelectOrCreateForm


class MtAEnhancementView(ChargenStepMixin, SpendFreebiesPermissionMixin, FormView):
    form_class = EnhancementForm
    template_name = "characters/mage/mage/chargen.html"

    def get_object(self):
        """Return the Human object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        return self.object

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        obj = Human.objects.get(id=self.kwargs["pk"])
        enhancement_bg = Background.objects.get(property_name="enhancement")
        self.current_enhancement = BackgroundRating.objects.filter(
            char=obj,
            bg=enhancement_bg,
            complete=False,
        ).first()
        kwargs["rank"] = self.current_enhancement.rating
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        obj = get_object_or_404(Human, pk=self.kwargs.get("pk"))
        enhancement_bg = Background.objects.get(property_name="enhancement")
        self.current_enhancement = BackgroundRating.objects.filter(
            char=obj,
            bg=enhancement_bg,
            complete=False,
        ).first()
        return form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        context["current_enhancement"] = self.current_enhancement
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        obj = context["object"]
        # Save the form data
        form.save(char=obj)

        # Check if there are more enhancements to complete
        enhancement_bg, _ = Background.objects.get_or_create(
            property_name="enhancement", defaults={"name": "Enhancement"}
        )
        if (
            BackgroundRating.objects.filter(
                char=obj,
                bg=enhancement_bg,
                complete=False,
            ).count()
            == 0
        ):
            advance(obj, user=self.request.user)
        return HttpResponseRedirect(obj.get_absolute_url())


class CharacterChantryBackgroundView(GenericBackgroundView):
    """Chantry background step shared by the Mage-family character wizards.

    Subclasses set only ``primary_object_class`` and ``template_name``.
    ``form_valid`` replaces the generic version, which would overwrite the
    owner, chronicle and status of a chantry the character merely joins.
    """

    background_name = "chantry"
    form_class = ChantrySelectOrCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = self.get_object()
        rating = getattr(self, "current_background", None)
        kwargs["points"] = rating.rating if rating is not None else 0
        return kwargs

    def form_valid(self, form):
        character = self.get_object()
        rating_model = type(self.current_background)
        with transaction.atomic():
            # Claim the rating before saving anything else, so a second near-simultaneous
            # POST that also passed GenericBackgroundView's pre-check finds it already
            # complete and backs off instead of double-adding points or double-creating.
            claimed = rating_model.objects.filter(
                pk=self.current_background.pk, complete=False
            ).update(complete=True)
            if not claimed:
                return HttpResponseRedirect(character.get_absolute_url())
            chantry = form.save()
            chantry.members.add(character)
            self.current_background.note = chantry.name
            self.current_background.url = chantry.get_absolute_url()
            self.current_background.complete = True
            self.current_background.save()
            if not character.backgrounds.filter(
                bg__property_name=self.background_name, complete=False
            ).exists():
                advance(character, user=self.request.user)
                character.save()
        return HttpResponseRedirect(character.get_absolute_url())

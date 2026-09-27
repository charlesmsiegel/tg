import json

from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from characters.chargen.transitions import advance
from characters.forms.core.backgroundform import BackgroundRatingFormSet
from characters.models.core.background_block import Background
from characters.models.core.human import Human
from characters.views.core.chargen_mixins import ChargenStepMixin
from core.mixins import (
    SpendFreebiesPermissionMixin,
)


class HumanBackgroundsView(ChargenStepMixin, SpendFreebiesPermissionMixin, FormView):
    form_class = BackgroundRatingFormSet
    template_name = "characters/core/human/chargen.html"
    live_validation = True

    def validation_totals(self, form):
        return [form.allocation_status()]

    def get_object(self):
        """Return the Human object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Human, pk=self.kwargs["pk"])
        return self.object

    def get_success_url(self):
        return get_object_or_404(Human, pk=self.kwargs["pk"]).get_absolute_url()

    def form_valid(self, form):
        form.save()
        advance(self.object, user=self.request.user)
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.object = get_object_or_404(Human, pk=self.kwargs["pk"])
        kwargs["character"] = self.object
        kwargs["enforce_allocation"] = True
        kwargs["instance"] = self.object  # Required for inline formset
        return kwargs

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure self.object is set (it's set in get_form_kwargs during POST/GET)
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Human, pk=self.kwargs["pk"])
        context["object"] = self.object
        for form in context["form"]:
            form.fields["bg"].queryset = Background.objects.filter(
                property_name__in=self.object.allowed_backgrounds
            )

        empty_form = context["form"].empty_form
        empty_form.fields["bg"].queryset = Background.objects.filter(
            property_name__in=self.object.allowed_backgrounds
        )
        context["empty_form"] = empty_form
        # Multiplier map (pk -> cost multiplier) for the client points counter.
        # It must cover EVERY selectable background, not just the allowed set:
        # the formset's add-row rebuilds empty_form with add_fields(), which
        # resets the bg queryset to all backgrounds, so a dynamically added row
        # can select one outside allowed_backgrounds and the server still
        # applies its real multiplier. Rendered via json.dumps to avoid a
        # hand-built template loop; pk/multiplier are integers (no XSS).
        context["background_multipliers_json"] = json.dumps(
            dict(Background.objects.values_list("pk", "multiplier"))
        )
        return context

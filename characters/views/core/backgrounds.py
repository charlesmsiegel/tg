from characters.forms.core.backgroundform import BackgroundRatingFormSet
from characters.models.core.background_block import Background
from characters.models.core.human import Human
from core.mixins import (
    EditPermissionMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    ViewPermissionMixin,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import FormView


class HumanBackgroundsView(EditPermissionMixin, FormView):
    form_class = BackgroundRatingFormSet
    template_name = "characters/core/human/chargen.html"

    def get_object(self):
        """Return the Human object for permission checking."""
        if not hasattr(self, "object") or self.object is None:
            self.object = get_object_or_404(Human, pk=self.kwargs["pk"])
        return self.object

    def get_success_url(self):
        return get_object_or_404(Human, pk=self.kwargs["pk"]).get_absolute_url()

    def form_valid(self, form):
        self.get_context_data()
        total_bg = sum(
            [
                f.cleaned_data["rating"] * f.cleaned_data["bg"].multiplier
                for f in form
                if "rating" in f.cleaned_data.keys() and "bg" in f.cleaned_data.keys()
            ]
        )
        if total_bg != self.object.background_points:
            for f in form:
                f.add_error(
                    None,
                    f"Backgrounds must total {self.object.background_points} points",
                )
            return super().form_invalid(form)
        form.save()
        self.object.creation_status += 1
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.object = get_object_or_404(Human, pk=self.kwargs["pk"])
        kwargs["character"] = self.object
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
        return context

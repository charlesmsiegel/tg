"""The optional template entry point precedes the numbered chargen workflow."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView


class CharacterTemplateSelectView(LoginRequiredMixin, FormView):
    model = None
    creation_route = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.object = get_object_or_404(self.model, pk=kwargs["pk"], owner_id=request.user.pk)
        if self.object.creation_status > 0:
            return redirect(self.creation_route, pk=self.object.pk)
        if self.object.status not in {"Un", "Rev"}:
            raise PermissionDenied("Cannot select a template for a locked character")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = self.object
        context["available_templates"] = context["form"].fields["template"].queryset
        return context

    @transaction.atomic
    def form_valid(self, form):
        template = form.cleaned_data.get("template")
        if template:
            template.apply_to_character(self.object)
            messages.success(
                self.request,
                f"Applied template '{template.name}'. You can now customize the character further.",
            )
        else:
            messages.info(self.request, "Starting with blank character. Fill in all attributes.")
        # Position zero is the optional entry point, outside the numbered registry.
        self.object.creation_status = 1
        self.object.save()
        return redirect(self.creation_route, pk=self.object.pk)

"""Shared bounded allocation lifecycle for record-backed chargen pools."""

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from characters.chargen.transitions import advance
from characters.views.core.chargen_mixins import ChargenStepMixin
from core.mixins import SpecialUserMixin, SpendFreebiesPermissionMixin


class PointAllocationView(
    ChargenStepMixin, SpendFreebiesPermissionMixin, SpecialUserMixin, FormView
):
    """Adapters name the pool and supply the existing model's add-record hook."""

    model = None
    allocation_name = ""
    total_attribute = ""
    spent_method = ""
    complete_method = ""
    completion_message = ""

    def get_object(self):
        if getattr(self, "object", None) is None:
            self.object = get_object_or_404(self.model, pk=self.kwargs["pk"])
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["object"] = obj
        context["is_approved_user"] = self.check_if_special_user(obj, self.request.user)
        total = getattr(obj, self.total_attribute)
        spent = getattr(obj, self.spent_method)()
        prefix = f"{self.allocation_name}_points"
        context.update(
            {
                f"{prefix}_total": total,
                f"{prefix}_spent": spent,
                f"{prefix}_remaining": total - spent,
            }
        )
        return context

    def add_record(self, obj, data):
        raise NotImplementedError

    def form_valid(self, form):
        obj = self.get_object()
        total = getattr(obj, self.total_attribute)
        spent = getattr(obj, self.spent_method)()
        if spent + form.cleaned_data["rating"] > total:
            error = (
                f"Cannot exceed {total} total {self.allocation_name} points. "
                f"You have {total - spent} remaining."
            )
            form.add_error("rating", error)
            messages.error(self.request, error)
            return self.form_invalid(form)
        self.add_record(obj, form.cleaned_data)
        if getattr(obj, self.complete_method)():
            advance(obj, user=self.request.user)
            obj.save()
            messages.success(self.request, self.completion_message)
        else:
            remaining = total - getattr(obj, self.spent_method)()
            messages.success(
                self.request,
                f"{self.allocation_name.title()} added successfully! {remaining} points remaining.",
            )
        return HttpResponseRedirect(obj.get_absolute_url())

    def form_invalid(self, form):
        if not self.request._messages._queued_messages:
            messages.error(self.request, "Please correct the errors in the form below.")
        return super().form_invalid(form)

"""Shared allocation lifecycles for chargen steps.

``AllocationStepMixin`` hands ``characters.rules`` limits to a form whose
``clean()`` enforces them; ``PointAllocationView`` adds one record at a time
to a bounded pool.
"""

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from characters.chargen.transitions import advance
from characters.forms.core.allocation import (
    allocation_modelform,
    priority_columns,
    rating_values,
)
from characters.rules.allocation import PriorityRule
from characters.views.core.chargen_mixins import ChargenStepMixin
from core.mixins import SpecialUserMixin, SpendFreebiesPermissionMixin


class AllocationStepMixin:
    """Bind a rule-enforcing form; flash any rule messages when it is invalid.

    Views describe limits with ``get_allocation_rules()`` (and optionally
    ``get_extra_clean()`` for a character-dependent check); they never sum or
    compare ratings themselves.
    """

    allocation_rules = ()
    live_validation = True
    infer_priority = False

    def get_allocation_rules(self):
        return self.allocation_rules

    def get_extra_clean(self):
        return None

    def get_form_class(self):
        if self.form_class is not None:
            return self.form_class
        model = self.model if self.model is not None else type(self.object)
        return allocation_modelform(model, tuple(self.fields))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["allocation_rules"] = self.get_allocation_rules()
        kwargs["extra_clean"] = self.get_extra_clean()
        kwargs["infer_priority"] = self.infer_priority
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rules = self.get_allocation_rules()
        context["allocation_rules"] = [rule.client_data() for rule in rules]
        # The PRI / SEC / TER picker and per-column counts (Attributes, Abilities).
        priority = next((rule for rule in rules if isinstance(rule, PriorityRule)), None)
        if priority is not None and "form" in context:
            context["priority"] = priority_columns(context["form"], priority)
        return context

    def validation_totals(self, form):
        values = rating_values(form)
        return [rule.status(values) for rule in self.get_allocation_rules()]

    def form_invalid(self, form):
        for text in getattr(form, "flash_errors", ()):
            messages.error(self.request, text)
        return super().form_invalid(form)


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

"""Mixins for character creation views."""

import time
from itertools import zip_longest

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import NON_FIELD_ERRORS, PermissionDenied
from django.forms.formsets import BaseFormSet
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from characters.chargen import get_workflow
from core.access_policy import authorize_route
from core.htmx import hx_redirect, is_fragment_request, mark_fragment, trigger, vary_on_htmx
from widgets.fields.chained import ChainedChoiceField

VALIDATE_PARAM = "_validate"
OPTIONS_PARAM = "_options"


class ChargenStepMixin:
    """Authorize before applicability checks and render the registered fragment.

    On an interactive workflow the same URL also serves htmx partials: the step
    fragment (``HX-Request``), validate-only feedback (``POST _validate=1``) and
    chained-select options (``GET _options=<field>``). See
    docs/superpowers/specs/2026-09-25-htmx-chargen-design.md.
    """

    # Steps whose template renders the live validator (feedback and totals).
    live_validation = False
    fragment_template = "characters/core/chargen/step_fragment.html"
    feedback_template = "characters/core/chargen/feedback.html"
    options_template = "characters/core/chargen/options.html"
    interactive_scripts = ("characters/js/chargen.js", "characters/js/chargen-components.js")

    def dispatch(self, request, *args, **kwargs):
        from characters.models.core import Character

        character = get_object_or_404(Character, pk=kwargs["pk"])
        denial = authorize_route(request, type(self), args, kwargs, subject=character)
        if denial is not None:
            return denial
        workflow = get_workflow(character.type)
        self.chargen_interactive = bool(workflow and workflow.interactive)
        fragment = self.chargen_interactive and is_fragment_request(request)
        step = None
        if workflow and 1 <= character.creation_status <= len(workflow.steps):
            step = workflow.step(character.creation_status)
        waiting = step is not None and step.key == "freebies" and not character.freebies_approved
        skipping = step is not None and step.should_skip(character)
        partial = self.partial_mode(request) if fragment else None
        if partial is not None:
            # Partials never advance, skip or save. An unavailable step has
            # nothing to validate or offer; htmx ignores 204 responses.
            if step is None or waiting or skipping or self.partial_throttled(request, character):
                return HttpResponse(status=204)
            self.chargen_step = step
            if partial == "validate":
                return self.render_validation()
            return self.render_options()
        if waiting:
            if request.method == "POST":
                raise PermissionDenied("Freebie allocation is awaiting approval")
            if request.method in {"GET", "HEAD"}:
                return self.render_to_response({"object": character})
        if skipping:
            if request.method == "POST":
                from characters.chargen.transitions import advance

                advance(character, user=request.user)
                return redirect("characters:character", pk=character.pk)
            if request.method in {"GET", "HEAD"}:
                return self.render_to_response({"object": character, "skip_step": True})
        response = super().dispatch(request, *args, **kwargs)
        wizard_url = reverse("characters:character", kwargs={"pk": character.pk})
        # Several models' canonical URLs are plain detail views. Keep unfinished
        # POSTs inside the wizard, including handlers with explicit redirects.
        if response.status_code == 302 and response.get("Location") == character.get_absolute_url():
            character.refresh_from_db(fields=["status"])
            if character.status in {"Un", "Rev"}:
                response = redirect(wizard_url)
        # Inside the wizard the XHR follows the redirect and receives the next
        # step's fragment. Anywhere else (the terminal step submits) htmx must
        # navigate the whole page instead of nesting that page in the form.
        if fragment and response.status_code in {301, 302, 303}:
            if response["Location"] != wizard_url:
                return vary_on_htmx(hx_redirect(response["Location"]))
        return response

    # -- htmx partials -------------------------------------------------------

    @staticmethod
    def partial_mode(request):
        if request.method == "POST" and request.POST.get(VALIDATE_PARAM):
            return "validate"
        if request.method == "GET" and request.GET.get(OPTIONS_PARAM):
            return "options"
        return None

    def partial_throttled(self, request, character):
        """Cap partial requests per user and character; a runaway client gets 204s."""
        limit = getattr(settings, "CHARGEN_PARTIAL_LIMIT", 60)
        key = f"chargen-partial:{request.user.pk}:{character.pk}:{int(time.time() // 60)}"
        cache.add(key, 0, 120)
        try:
            return cache.incr(key) > limit
        except ValueError:  # expired between add and incr
            return False

    def _partial_object(self):
        if getattr(self, "object", None) is None:
            self.object = self.get_object()
        return self.object

    def _partial_response(self, template, context, kind):
        response = TemplateResponse(self.request, template, context)
        response["TG-Step"] = self.chargen_step.key
        return vary_on_htmx(mark_fragment(response, kind))

    def render_validation(self):
        """Run the step's own form checks without saving (no form_valid, no service)."""
        character = self._partial_object()
        form = self.get_form()
        valid = form.is_valid()
        return self._partial_response(
            self.feedback_template,
            {
                "object": character,
                "step": self.chargen_step,
                "valid": valid,
                "errors": form_error_messages(form),
                "totals": self.validation_totals(form),
            },
            "chargen-feedback",
        )

    def validation_totals(self, form):
        """Authoritative running totals for the feedback fragment; steps override."""
        return []

    def render_options(self):
        """``<option>`` elements for one chained child, from the step's own form."""
        self._partial_object()
        form = self.get_form()
        name = self.request.GET[OPTIONS_PARAM]
        field = form.fields.get(name)
        if not (
            isinstance(field, ChainedChoiceField)
            and field.parent_field in form.fields
            and hasattr(form, "chain_for")
        ):
            return HttpResponseBadRequest("Unknown chained field")
        chain = form.chain_for(name)
        values = {chained: self.request.GET.get(chained, "") for chained in chain}
        position = chain.index(name)
        # A new parent value invalidates this field and everything below it.
        for reset in chain[position:]:
            values[reset] = ""
        choices = field.get_choices_for_parent(values[field.parent_field])
        response = self._partial_response(
            self.options_template,
            {
                "choices": [(str(choice[0]), choice[1]) for choice in choices],
                "resets": [
                    (form[below].auto_id, form.fields[below].empty_label)
                    for below in chain[position + 1 :]
                ],
            },
            "chargen-options",
        )
        if hasattr(form, "field_visibility"):
            trigger(response, "tg-visibility", form.field_visibility(values))
        return response

    # -- rendering -----------------------------------------------------------

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if getattr(self, "chargen_interactive", False):
            use_dot_widgets(form, self.dot_bounds())
            if hasattr(form, "enable_htmx_chains"):
                form.enable_htmx_chains(self.request.path)
        return form

    def dot_bounds(self):
        """``{field: (min, max)}`` for fields rendered as clickable dots."""
        bounds = {}
        for rule in getattr(self, "get_allocation_rules", lambda: ())():
            data = rule.client_data()
            for name in rule.fields:
                bounds[name] = (data.get("min", 0), data.get("max", 5))
        return bounds

    def render_to_response(self, context, **response_kwargs):
        character = context.get("object") or getattr(self, "object", None)
        interactive = getattr(self, "chargen_interactive", False)
        if character is not None:
            workflow = get_workflow(character.type)
            if workflow and 1 <= character.creation_status <= len(workflow.steps):
                context["step"] = workflow.step(character.creation_status)
                context["chargen_steps"] = workflow.progress(character.creation_status)
                if context["step"].key == "abilities" and "form" in context:
                    form = context["form"]
                    groups = [
                        [form[name] for name in getattr(character, group) if name in form.fields]
                        for group in ("talents", "skills", "knowledges")
                    ]
                    context["ability_rows"] = list(zip_longest(*groups))
                context["chargen_formsets"] = {
                    key: value
                    for key, value in context.items()
                    if key.endswith("_context") and isinstance(value, dict) and "formset" in value
                }
        context["chargen_interactive"] = interactive
        if interactive:
            context["component_scripts"] = self.interactive_scripts
            context["live_validation"] = (
                self.live_validation and "form" in context and not context.get("skip_step")
            )
        response = super().render_to_response(context, **response_kwargs)
        if interactive:
            vary_on_htmx(response)
            if is_fragment_request(self.request):
                mark_fragment(response, "chargen-step")
        return response

    def get_template_names(self):
        if getattr(self, "chargen_interactive", False) and is_fragment_request(self.request):
            return [self.fragment_template]
        if self.template_name.endswith("/chargen.html"):
            return [self.template_name]
        return ["characters/core/chargen.html"]


def use_dot_widgets(form, bounds):
    """Render bounded number fields as clickable dots (the input stays the control)."""
    from widgets.widgets.dots import DotRatingInput

    for name, (minimum, maximum) in bounds.items():
        field = form.fields.get(name)
        if field is not None and type(field.widget) is forms.NumberInput:
            field.widget = DotRatingInput(
                minimum=minimum,
                maximum=maximum,
                label=field.label or name,
                attrs=field.widget.attrs,
            )


def form_error_messages(form):
    """Every error of a form or formset as ``(label, message)``, non-field first."""
    if isinstance(form, BaseFormSet):
        messages = [(None, error) for error in form.non_form_errors()]
        for subform in form.forms:
            messages += form_error_messages(subform)
        return messages
    messages = [(None, error) for error in form.non_field_errors()]
    for name, errors in form.errors.items():
        if name == NON_FIELD_ERRORS:
            continue
        label = form.fields[name].label if name in form.fields else name
        messages += [(label or name.replace("_", " ").title(), error) for error in errors]
    return messages


class ChargenProgressMixin:
    """Mixin that provides chargen_steps context for the progress bar.

    Subclasses define `chargen_step_labels` as a list of (start_status, label)
    tuples. Example: [(1, "Stats"), (3, "Powers"), (6, "Details"), (7, "Freebies")]

    Note on MRO: This mixin accesses `self.object`, which is set by
    UpdateView.get() before get_context_data is called. For FormView-based
    step views where self.object may not exist, the guard
    `getattr(self, "object", None)` prevents AttributeError.
    """

    chargen_step_labels = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = getattr(self, "object", None)
        if self.chargen_step_labels and obj is not None and hasattr(obj, "creation_status"):
            steps = []
            current = obj.creation_status
            for i, (start, label) in enumerate(self.chargen_step_labels):
                if i + 1 < len(self.chargen_step_labels):
                    # A group of statuses ends where the next group starts.
                    next_start = self.chargen_step_labels[i + 1][0]
                    if current >= next_start:
                        status = "completed"
                    elif current >= start:
                        status = "current"
                    else:
                        status = "pending"
                else:
                    # The final group has no defined endpoint, so it stays
                    # current for every status at or above its start rather
                    # than flipping to completed after its first status.
                    status = "current" if current >= start else "pending"
                steps.append({"label": label, "status": status})
            context["chargen_steps"] = steps
        return context

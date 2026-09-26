"""Mixins for character creation views."""

from itertools import zip_longest

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect

from characters.chargen import get_workflow
from core.access_policy import authorize_route


class ChargenStepMixin:
    """Authorize before applicability checks and render the registered fragment."""

    def dispatch(self, request, *args, **kwargs):
        from characters.models.core import Character

        character = get_object_or_404(Character, pk=kwargs["pk"])
        denial = authorize_route(request, type(self), args, kwargs, subject=character)
        if denial is not None:
            return denial
        workflow = get_workflow(character.type)
        if workflow and 1 <= character.creation_status <= len(workflow.steps):
            step = workflow.step(character.creation_status)
            if step.key == "freebies" and not character.freebies_approved:
                if request.method == "POST":
                    raise PermissionDenied("Freebie allocation is awaiting approval")
                if request.method in {"GET", "HEAD"}:
                    return self.render_to_response({"object": character})
            if step.should_skip(character):
                if request.method == "POST":
                    from characters.chargen.transitions import advance

                    advance(character, user=request.user)
                    return redirect("characters:character", pk=character.pk)
                if request.method in {"GET", "HEAD"}:
                    return self.render_to_response({"object": character, "skip_step": True})
        response = super().dispatch(request, *args, **kwargs)
        # Several models' canonical URLs are plain detail views. Keep unfinished
        # POSTs inside the wizard, including handlers with explicit redirects.
        if response.status_code == 302 and response.get("Location") == character.get_absolute_url():
            character.refresh_from_db(fields=["status"])
            if character.status in {"Un", "Rev"}:
                return redirect("characters:character", pk=character.pk)
        return response

    def render_to_response(self, context, **response_kwargs):
        character = context.get("object") or getattr(self, "object", None)
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
        return super().render_to_response(context, **response_kwargs)

    def get_template_names(self):
        if self.template_name.endswith("/chargen.html"):
            return [self.template_name]
        return ["characters/core/chargen.html"]


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

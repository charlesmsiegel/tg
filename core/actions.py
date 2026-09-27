"""Dedicated POST endpoints: one action on one object per URL (Step 5).

An action view loads its subject, authorizes it, binds its form, runs exactly
one service call inside a transaction, flashes the outcome and redirects.
Detail views render pages and never handle POST.

The route policy ``ACTION`` (``core.access_policy``) rejects non-POST methods
(405) and anonymous callers (401) before the view runs; the object rule lives
on the action itself as ``permission`` or ``has_permission``.
"""

from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views import View

from core.permissions import Permission, PermissionManager


class ActionFailed(Exception):
    """A service refused the action; the message is shown to the user."""


def _error_text(exc):
    if isinstance(exc, ValidationError):
        return "; ".join(exc.messages)
    return str(exc)


class ObjectActionView(View):
    """Load, authorize, validate, perform in a transaction, flash, redirect.

    Order matters: a caller who may not see the subject gets the same 404 as
    for a missing one, before any form validation or side effect (Step 0).
    """

    http_method_names = ["post"]
    model = None
    pk_url_kwarg = "pk"
    permission = None
    form_class = None
    lock = False
    success_message = ""
    host_view_class = None
    host_form_context_name = "form"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.authorize()
        form = self.get_form()
        if form is not None and not self.is_valid(form):
            return self.form_invalid(form)
        try:
            with transaction.atomic():
                if self.lock:
                    self.object = self.lock_object(self.object)
                result = self.perform(form)
                if getattr(result, "success", True) is False:
                    raise ActionFailed(getattr(result, "error", None) or "Action failed")
        except (ActionFailed, ValidationError) as exc:
            return self.action_failed(_error_text(exc), form)
        return self.action_succeeded(result)

    # Subject -----------------------------------------------------------

    def get_queryset(self):
        return self.model._default_manager.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs[self.pk_url_kwarg])

    def lock_object(self, obj):
        return type(obj)._default_manager.select_for_update().get(pk=obj.pk)

    def get_permission_subject(self):
        return self.object

    # Authorization -----------------------------------------------------

    def authorize(self):
        subject = self.get_permission_subject()
        if not self.can_see(subject):
            raise Http404("Object not found")
        if not self.has_permission(subject):
            raise PermissionDenied("You cannot perform this action")

    def can_see(self, subject):
        return PermissionManager.user_has_permission(
            self.request.user, subject, Permission.VIEW_FULL, request=self.request
        )

    def has_permission(self, subject):
        if self.permission is None:
            raise NotImplementedError("Set permission or override has_permission()")
        return PermissionManager.user_has_permission(
            self.request.user, subject, self.permission, request=self.request
        )

    # Form --------------------------------------------------------------

    def get_form_kwargs(self):
        return {"data": self.request.POST, "files": self.request.FILES}

    def get_form(self):
        if self.form_class is None:
            return None
        return self.form_class(**self.get_form_kwargs())

    def is_valid(self, form):
        return form.is_valid()

    # Work --------------------------------------------------------------

    def perform(self, form):
        """Make exactly one service or model call and return its result."""
        raise NotImplementedError

    # Responses ---------------------------------------------------------

    def get_success_url(self, result=None):
        return self.object.get_absolute_url()

    def get_failure_url(self):
        return self.get_success_url()

    def get_success_message(self, result):
        message = getattr(result, "message", "") if result is not None else ""
        return message or self.success_message.format(object=self.object)

    def fragment_response(self, result=None, form=None, error=None):
        """Step 10 hook: return a partial response (e.g. for htmx) or None.

        Called first on the success, failure and invalid-form paths, after
        authorization and validation, so a fragment never skips a check.
        """
        return None

    def action_succeeded(self, result):
        fragment = self.fragment_response(result=result)
        if fragment is not None:
            return fragment
        message = self.get_success_message(result)
        if message:
            messages.success(self.request, message)
        return redirect(self.get_success_url(result))

    def action_failed(self, error, form=None):
        fragment = self.fragment_response(form=form, error=error)
        if fragment is not None:
            return fragment
        if form is not None and self.host_view_class is not None:
            form.add_error(None, error)
            return self.render_host(form)
        messages.error(self.request, error)
        return redirect(self.get_failure_url())

    def form_invalid(self, form):
        fragment = self.fragment_response(form=form)
        if fragment is not None:
            return fragment
        if self.host_view_class is not None:
            return self.render_host(form)
        for field, errors in form.errors.items():
            for error in errors:
                label = form.fields[field].label if field in form.fields else None
                messages.error(self.request, f"{label}: {error}" if label else error)
        return redirect(self.get_failure_url())

    def get_host_context(self, form):
        return {self.host_form_context_name: form}

    def render_host(self, form):
        """Re-render the page the form came from, with the bound form."""
        host = self.host_view_class()
        host.setup(self.request, *self.args, **self.kwargs)
        host.object = self.object
        context = host.get_context_data(object=self.object, **self.get_host_context(form))
        return TemplateResponse(self.request, host.get_template_names(), context)

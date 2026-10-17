"""Dedicated bounded journal actions, reusing native owner/APPROVE policies."""

import sqlite3

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import OperationalError
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from characters.models.core import CharacterModel
from core.api.scene_journal import MAX_NATIVE_ID, GameReadView, entry_projection, hidden_get
from core.permissions import PermissionManager
from game.actions import JournalEntryCreateView, JournalResponseView
from game.journal_api import JournalWriteError, append_prose, first_response
from game.models import Chronicle, Journal, JournalEntry, STRelationship
from game.security import can_read_private_record


def complete_entry(entry):
    return entry_projection(entry) | {"st_message": entry.st_message}


def sqlite_lock_conflict(exc):
    cause = exc.__cause__
    if not isinstance(cause, sqlite3.OperationalError):
        return False
    code = getattr(cause, "sqlite_errorcode", None)
    if code is not None:
        # Stable SQLite C base codes: BUSY=5, LOCKED=6 (including extensions).
        return code & 0xFF in {5, 6}
    # Python 3.10 exposes neither sqlite_errorcode nor SQLite error constants.
    # Exact engine messages, scoped to a real sqlite3 cause, preserve its support.
    return str(cause).split(":", 1)[0] in {
        "database is locked",
        "database table is locked",
        "database schema is locked",
    }


class JournalWriteMixin:
    lock = True
    form_class = None
    success_status = 200

    def dispatch(self, request, *args, **kwargs):
        try:
            if any(not 1 <= value <= MAX_NATIVE_ID for value in kwargs.values()):
                raise Http404
            response = super().dispatch(request, *args, **kwargs)
        except Http404:
            response = JsonResponse({"error": "Not found."}, status=404)
        except PermissionDenied:
            response = JsonResponse({"error": "Forbidden."}, status=403)
        except JournalWriteError as exc:
            response = JsonResponse({"errors": exc.errors}, status=exc.status)
        except OperationalError as exc:
            if not sqlite_lock_conflict(exc):
                raise
            # ObjectActionView has exited/rolled back its atomic block. SQLite
            # read-to-write upgrades can conflict despite select_for_update().
            response = JsonResponse(
                {
                    "errors": {
                        "non_field_errors": [
                            {
                                "message": "Concurrent journal change. Refresh before retrying.",
                                "code": "write_conflict",
                            }
                        ]
                    }
                },
                status=409,
            )
        response["Cache-Control"] = "private, no-store"
        return response

    def lock_object(self, obj):
        journal = get_object_or_404(Journal.objects.select_for_update(), pk=obj.pk)
        if journal.character_id != obj.character_id:
            raise Http404
        # Do not carry pre-lock relation caches or stale actor flags into writes.
        character = get_object_or_404(
            CharacterModel.objects.select_for_update(), pk=journal.character_id
        )
        self.request.user = get_object_or_404(
            get_user_model().objects.select_for_update(), pk=self.request.user.pk
        )
        if not self.request.user.is_active:
            raise Http404
        if character.chronicle_id is not None:
            character.chronicle = get_object_or_404(
                Chronicle.objects.select_for_update(), pk=character.chronicle_id
            )
            # Protect current scoped-role rows against revocation during this action.
            list(
                STRelationship.objects.select_for_update().filter(
                    user_id=self.request.user.pk, chronicle_id=character.chronicle_id
                )
            )
        journal.character = character
        return journal

    def reauthorize(self):
        PermissionManager.invalidate_request_cache(self.request)
        self.authorize()

    def action_succeeded(self, result):
        return JsonResponse(complete_entry(result), status=self.success_status)


class JournalAppendView(JournalWriteMixin, JournalEntryCreateView):
    success_status = 201

    def perform(self, form):
        self.reauthorize()
        return append_prose(self.object, self.request)


class JournalFirstResponseView(JournalWriteMixin, JournalResponseView):
    def perform(self, form):
        self.reauthorize()
        entry = get_object_or_404(
            JournalEntry.objects.select_for_update(),
            pk=self.kwargs["entry_pk"],
            journal_id=self.object.pk,
        )
        return first_response(entry, self.request)


class JournalEntryDetailView(GameReadView):
    def get(self, request, pk, entry_pk):
        if not 1 <= entry_pk <= MAX_NATIVE_ID:
            raise NotFound("Not found.")
        journal = self.journal(pk=pk)
        entry = hidden_get(JournalEntry.objects.all(), pk=entry_pk, journal_id=journal.pk)
        # Repeat canonical native visibility after lookup; a response is visible
        # to the same readers as the native journal, never an ST-only secret.
        self.journal(pk=pk)
        if not JournalEntry.objects.filter(pk=entry.pk, journal_id=journal.pk).exists():
            raise NotFound("Not found.")
        if not can_read_private_record(request.user, entry):
            raise NotFound("Not found.")
        return Response(complete_entry(entry))

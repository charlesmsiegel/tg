"""Bounded prose append and first response; no journal command execution or edits."""

import json
import re
from datetime import datetime, time

from django.utils.timezone import make_aware

from game.forms import JournalEntryForm, STResponseForm
from game.models import JournalEntry

MAX_TEXT = 10_000
MAX_BODY = 65_536
# Native process_message recognizes these substrings anywhere, not just at start.
# Reject case variants too instead of silently changing future/native interpretation.
RESERVED = re.compile(r"#(?:WP|Q-?\d+|P-?\d+|-?\d+[BLA])|/(?:extended|rolls|roll|stat)", re.I)


class JournalWriteError(Exception):
    def __init__(self, errors, status=400):
        self.errors = errors
        self.status = status
        super().__init__("Journal write refused")


def refuse(field, message, code, status=400):
    raise JournalWriteError({field: [{"message": message, "code": code}]}, status)


def unique_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            refuse(key, "Duplicate field.", "duplicate")
        result[key] = value
    return result


def bounded_payload(request, fields):
    if request.content_type != "application/json":
        refuse("non_field_errors", "Content-Type must be application/json.", "media_type", 415)
    if len(request.body) > MAX_BODY:
        refuse("non_field_errors", "Request is too large.", "max_size")
    try:
        data = json.loads(request.body.decode("utf-8"), object_pairs_hook=unique_fields)
    except (ValueError, UnicodeDecodeError, RecursionError) as exc:
        raise JournalWriteError(
            {"non_field_errors": [{"message": "Malformed JSON.", "code": "invalid"}]}
        ) from exc
    if not isinstance(data, dict):
        refuse("non_field_errors", "Expected a JSON object.", "invalid")
    for key, value in data.items():
        if key not in fields:
            refuse(key, "Unsupported field.", "unsupported")
        if not isinstance(value, str):
            refuse(key, "Expected text.", "invalid")
        try:
            value.encode("utf-8")
        except UnicodeEncodeError:
            refuse(key, "Expected valid Unicode text.", "invalid")
        if len(value) > MAX_TEXT:
            refuse(key, f"Use at most {MAX_TEXT} characters.", "max_length")
    return data


def append_prose(journal, request):
    data = bounded_payload(request, {"date", "message"})
    if "date" in data and not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", data["date"]):
        refuse("date", "Use YYYY-MM-DD.", "invalid")
    form = JournalEntryForm(data=data, instance=journal)
    if not form.is_valid():
        raise JournalWriteError(form.errors.get_json_data())
    message = form.cleaned_data["message"]
    if RESERVED.search(message):
        refuse(
            "message", "Dice commands and resource tags are not supported.", "unsupported_command"
        )
    # Same native form stripping/date conversion, deliberately no add_post/parser.
    date = make_aware(datetime.combine(form.cleaned_data["date"], time.min))
    return JournalEntry.objects.create(journal=journal, date=date, message=message)


def first_response(entry, request):
    data = bounded_payload(request, {"st_message"})
    form = STResponseForm(data=data, entry=entry)
    if not form.is_valid():
        raise JournalWriteError(form.errors.get_json_data())
    message = form.cleaned_data["st_message"]
    # A first answer only: never overwrite player prose, a changed parent or a
    # competing/native response. Updating just this field avoids stale row saves.
    changed = JournalEntry.objects.filter(
        pk=entry.pk, journal_id=entry.journal_id, st_message=""
    ).update(st_message=message)
    if changed != 1:
        refuse("st_message", "This entry already has a response.", "already_answered", 409)
    entry.st_message = message
    return entry

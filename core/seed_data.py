"""Validated, explicitly configured reference catalogues; no executable data."""

import json
import keyword
import re
from pathlib import Path

from django.core.exceptions import FieldDoesNotExist
from django.db import models, transaction

KEY_PATTERN = re.compile(r"[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+")
RECORD_PROPERTIES = {"key", "export", "legacy_lookup", "fields"}


class SeedDataError(ValueError):
    """A catalogue cannot be interpreted or safely adopted."""


def _unique_properties(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise SeedDataError(f"duplicate JSON property {key!r}")
        result[key] = value
    return result


def _validate_configuration(model, names):
    for name in names:
        try:
            field = model._meta.get_field(name)
        except FieldDoesNotExist as error:
            raise SeedDataError(f"unknown configured field {name!r}") from error
        if not field.concrete or field.is_relation or field.primary_key or name == "seed_key":
            raise SeedDataError(f"disallowed configured field {name!r}")


def _validate_record(record, allowed_fields, legacy_fields):
    if not isinstance(record, dict) or set(record) != RECORD_PROPERTIES:
        raise SeedDataError(f"record must contain exactly {sorted(RECORD_PROPERTIES)}")
    key, export = record["key"], record["export"]
    if not isinstance(key, str) or len(key) > 150 or not KEY_PATTERN.fullmatch(key):
        raise SeedDataError("invalid seed key (expected dotted lowercase identifier, <=150 chars)")
    if not isinstance(export, str) or not export.isidentifier() or keyword.iskeyword(export):
        raise SeedDataError("invalid Python export identifier")
    fields, lookup = record["fields"], record["legacy_lookup"]
    if not isinstance(fields, dict) or set(fields) != allowed_fields:
        raise SeedDataError(f"fields must contain exactly {sorted(allowed_fields)}")
    if not isinstance(lookup, dict) or not lookup or not set(lookup) <= legacy_fields:
        raise SeedDataError("legacy_lookup must be a nonempty subset of configured legacy fields")


def read_seed_records(
    model, path: Path, *, allowed_fields: frozenset[str], legacy_fields: frozenset[str]
) -> list[dict]:
    """Validate a complete input contract without querying or writing the database."""
    path = Path(path)
    try:
        if not allowed_fields or not legacy_fields:
            raise SeedDataError("allowed_fields and legacy_fields must not be empty")
        _validate_configuration(model, allowed_fields | legacy_fields)
        with path.open(encoding="utf-8") as source:
            records = json.load(source, object_pairs_hook=_unique_properties)
        if not isinstance(records, list):
            raise SeedDataError("catalogue must be a list")
        keys, exports = set(), set()
        for index, record in enumerate(records):
            try:
                _validate_record(record, allowed_fields, legacy_fields)
                if record["key"] in keys or record["export"] in exports:
                    raise SeedDataError("duplicate seed key or export")
                keys.add(record["key"])
                exports.add(record["export"])
            except SeedDataError as error:
                raise SeedDataError(f"record {index + 1}: {error}") from error
        return records
    except (OSError, UnicodeError, ValueError) as error:
        raise SeedDataError(f"{path}: {error}") from error


def load_seed_records(
    model, path: Path, *, allowed_fields: frozenset[str], legacy_fields: frozenset[str]
) -> dict[str, "models.Model"]:
    """Adopt or update a catalogue atomically, retaining database identities.

    Declared content fields are authoritative. Removed records are not deleted.
    Conflicting concurrent loads may fail; callers can retry the whole catalogue.
    """
    records = read_seed_records(
        model, path, allowed_fields=allowed_fields, legacy_fields=legacy_fields
    )
    exports = {}
    with transaction.atomic():
        for record in records:
            key, lookup = record["key"], record["legacy_lookup"]
            locked = model.objects.select_for_update()
            obj = locked.filter(seed_key=key).first()
            if obj is None:
                matches = list(locked.filter(**lookup)[:2])
                if len(matches) > 1 or (matches and matches[0].seed_key is not None):
                    raise SeedDataError(f"{path}: cannot adopt {key!r} with {lookup!r}")
                obj = matches[0] if matches else model()
                obj.seed_key = key
            for name, value in record["fields"].items():
                setattr(obj, name, value)
            obj.full_clean()
            if obj.pk is None:
                obj.save()
            else:
                obj.save(update_fields=allowed_fields | {"seed_key"})
            exports[record["export"]] = obj
    return exports

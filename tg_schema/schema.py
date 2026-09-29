"""Helpers for tg_schema migrations: guarded patches for legacy databases.

Local apps (game, characters, locations...) have no migration history: a fresh
database gets their tables from the current models, and these migrations bring an
older database up to date, each change exactly once. They look models and fields
up by name when they run, never at import: a model or field that a later release
renames or removes is skipped (that release's migration owns it), so an old
migration can't crash every ``migrate`` after such a change.
"""

from django.apps import apps
from django.core.exceptions import FieldDoesNotExist


def live_model(label):
    """The model ``app_label.ModelName`` as the code defines it now, or None."""
    try:
        return apps.get_model(label)
    except LookupError:
        return None


def live_field(model, name):
    """``model``'s field ``name`` as the code defines it now, or None."""
    if model is None:
        return None
    try:
        return model._meta.get_field(name)
    except FieldDoesNotExist:
        return None


def table_names(connection):
    with connection.cursor() as cursor:
        return set(connection.introspection.table_names(cursor))


def table_columns(connection, table):
    with connection.cursor() as cursor:
        return {
            column.name for column in connection.introspection.get_table_description(cursor, table)
        }


def add_missing_columns(schema_editor, label, names):
    """Add each field in ``names`` of model ``label`` whose column the table lacks.

    Test and fresh databases already have the columns (their tables come from the
    current models); older ones get the DDL exactly once. Returns the names added.
    """
    model = live_model(label)
    connection = schema_editor.connection
    if model is None or model._meta.db_table not in table_names(connection):
        return set()
    columns = table_columns(connection, model._meta.db_table)
    added = set()
    for name in names:
        field = live_field(model, name)
        if field is not None and field.column not in columns:
            schema_editor.add_field(model, field)
            added.add(name)
    return added

"""Widen Human age checks for long-lived characters on existing databases.

Fresh databases take these checks from the live model. Legacy databases can
still have the older age and apparent-age limits, so replace the named checks
without depending on local character migration files (which are gitignored).
The model and its fields are looked up by name when this runs: a later release
that renames or removes them owns the change, so this migration skips them.
"""

from django.db import migrations, models

from tg_schema.schema import live_field, live_model, table_names

CHECKS = (
    ("age", "characters_human_reasonable_age"),
    ("apparent_age", "characters_human_reasonable_apparent_age"),
)


def widen_age_limits(apps, schema_editor):
    Human = live_model("characters.Human")
    connection = schema_editor.connection
    if Human is None or Human._meta.db_table not in table_names(connection):
        return
    with connection.cursor() as cursor:
        existing = connection.introspection.get_constraints(cursor, Human._meta.db_table)
    for field, name in CHECKS:
        if live_field(Human, field) is None:
            continue
        constraint = models.CheckConstraint(
            condition=models.Q(**{f"{field}__isnull": True})
            | (models.Q(**{f"{field}__gte": 0}) & models.Q(**{f"{field}__lte": 65535})),
            name=name,
            violation_error_message=f"{field.replace('_', ' ').title()} must be between 0 and 65535",
        )
        if name in existing:
            schema_editor.remove_constraint(Human, constraint)
        schema_editor.add_constraint(Human, constraint)


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0008_unique_scene_read_status")]
    operations = [migrations.RunPython(widen_age_limits, migrations.RunPython.noop)]

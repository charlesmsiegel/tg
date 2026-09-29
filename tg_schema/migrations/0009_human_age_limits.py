"""Widen Human age checks for long-lived characters on existing databases.

Fresh databases take these checks from the live model. Legacy databases can
still have the older age and apparent-age limits, so replace the named checks
without depending on local character migration files (which are gitignored).
"""

from django.db import migrations, models


def widen_age_limits(apps, schema_editor):
    from characters.models.core.human import Human

    checks = (
        ("age", "characters_human_reasonable_age"),
        ("apparent_age", "characters_human_reasonable_apparent_age"),
    )
    table = Human._meta.db_table
    with schema_editor.connection.cursor() as cursor:
        existing = schema_editor.connection.introspection.get_constraints(cursor, table)
    for field, name in checks:
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

"""Replace database-local Lore IDs with durable property names in ritual requirements.

Only old entries with resolvable IDs change. Dangling IDs are retained and logged for
manual repair or a reference-data reload; dropping them would erase requirements.
Removed models, fields, tables and columns are skipped. Reversal retains durable keys.
"""

import logging

from django.db import migrations

from tg_schema.schema import live_field, live_model, table_columns, table_names

logger = logging.getLogger(__name__)


def convert_ritual_lore_keys(apps, schema_editor):
    ritual = live_model("characters.Ritual")
    lore = live_model("characters.Lore")
    required = ((ritual, ("secondary_lore_requirements",)), (lore, ("property_name",)))
    for model, names in required:
        if model is None or any(live_field(model, name) is None for name in names):
            return
    connection = schema_editor.connection
    tables = table_names(connection)
    for model, names in required:
        table = model._meta.db_table
        if table not in tables:
            return
        fields = [model._meta.pk, *(live_field(model, name) for name in names)]
        if not {field.column for field in fields} <= table_columns(connection, table):
            return
    keys = dict(lore.objects.using(connection.alias).values_list("pk", "property_name"))
    rows = ritual.objects.using(connection.alias)
    for pk, requirements in rows.values_list("pk", "secondary_lore_requirements").iterator():
        if not isinstance(requirements, list):
            continue
        converted = []
        for requirement in requirements:
            if (
                isinstance(requirement, dict)
                and "lore_id" in requirement
                and "lore" not in requirement
            ):
                old_id = requirement["lore_id"]
                key = (
                    keys.get(old_id)
                    if isinstance(old_id, int) and not isinstance(old_id, bool)
                    else None
                )
                if key:
                    requirement = {k: v for k, v in requirement.items() if k != "lore_id"}
                    requirement["lore"] = key
                else:
                    logger.warning("Ritual %s retains unresolved legacy Lore ID %r", pk, old_id)
            converted.append(requirement)
        if converted != requirements:
            rows.filter(pk=pk).update(secondary_lore_requirements=converted)


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0014_dynasty_seed_key")]
    operations = [migrations.RunPython(convert_ritual_lore_keys, migrations.RunPython.noop)]

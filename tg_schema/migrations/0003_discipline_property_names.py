"""Link legacy Vampire Discipline reference rows to character trait fields."""

from django.db import migrations

from tg_schema.schema import live_field, live_model

DISCIPLINE_FIELDS = (
    "celerity",
    "fortitude",
    "potence",
    "auspex",
    "dominate",
    "dementation",
    "presence",
    "animalism",
    "protean",
    "obfuscate",
    "chimerstry",
    "necromancy",
    "obtenebration",
    "quietus",
    "serpentis",
    "thaumaturgy",
    "vicissitude",
    "daimoinon",
    "melpominee",
    "mytherceria",
    "obeah",
    "temporis",
    "thanatosis",
    "valeren",
    "visceratika",
)


def backfill_discipline_property_names(apps, schema_editor):
    # Looked up when it runs, so a later rename can't break it (see tg_schema.schema).
    Discipline = live_model("characters.Discipline")
    if live_field(Discipline, "property_name") is None:
        return
    disciplines = Discipline.objects.using(schema_editor.connection.alias)
    for field_name in DISCIPLINE_FIELDS:
        disciplines.filter(name__iexact=field_name, property_name="").update(
            property_name=field_name
        )


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0002_chantry_rating_linked_object")]
    operations = [
        migrations.RunPython(backfill_discipline_property_names, migrations.RunPython.noop)
    ]

"""Retire the unsupported Custom visibility choice without widening access.

Every CUS value becomes PRI; detail cards remain limited to full viewers, and existing
owner, storyteller and observer grants are untouched. PermissionMixin and Model are
abstract, so their visibility field lives in many unrelated concrete table roots,
not one core table. The frozen list below includes every current owning table,
including reference-data roots and CharacterTemplate, once per physical column.
Keep this historical list frozen; later schema changes need their own migrations,
not edits to this snapshot to satisfy a current-model coverage audit.

Only the old value changes. A missing/renamed model, field, table or column is
skipped so later releases remain migratable. Reversing never restores the retired
choice or broadens public visibility.
"""

from django.db import migrations

from tg_schema.schema import live_field, live_model, table_columns, table_names

VISIBILITY_TABLES = (
    ("characters.Advantage", "characters_advantage"),
    ("characters.ApocalypticForm", "characters_apocalypticform"),
    ("characters.ApocalypticFormTrait", "characters_apocalypticformtrait"),
    ("characters.Arcanos", "characters_arcanos"),
    ("characters.Archetype", "characters_archetype"),
    ("characters.BattleScar", "characters_battlescar"),
    ("characters.Camp", "characters_camp"),
    ("characters.Cantrip", "characters_cantrip"),
    ("characters.CharacterModel", "characters_charactermodel"),
    ("characters.Chimera", "characters_chimera"),
    ("characters.DemonFaction", "characters_demonfaction"),
    ("characters.DemonHouse", "characters_demonhouse"),
    ("characters.Derangement", "characters_derangement"),
    ("characters.Effect", "characters_effect"),
    ("characters.FomoriPower", "characters_fomoripower"),
    ("characters.Gift", "characters_gift"),
    ("characters.Group", "characters_group"),
    ("characters.Guild", "characters_guild"),
    ("characters.House", "characters_house"),
    ("characters.HouseFaction", "characters_housefaction"),
    ("characters.Instrument", "characters_instrument"),
    ("characters.Kith", "characters_kith"),
    ("characters.Legacy", "characters_legacy"),
    ("characters.LinearMagicPath", "characters_linearmagicpath"),
    ("characters.LinearMagicRitual", "characters_linearmagicritual"),
    ("characters.Lore", "characters_lore"),
    ("characters.MageFaction", "characters_magefaction"),
    ("characters.MeritFlaw", "characters_meritflaw"),
    ("characters.Paradigm", "characters_paradigm"),
    ("characters.Path", "characters_path"),
    ("characters.Practice", "characters_practice"),
    ("characters.RenownIncident", "characters_renownincident"),
    ("characters.Resonance", "characters_resonance"),
    ("characters.Rite", "characters_rite"),
    ("characters.Ritual", "characters_ritual"),
    ("characters.Rote", "characters_rote"),
    ("characters.SeptPosition", "characters_septposition"),
    ("characters.ShadowArchetype", "characters_shadowarchetype"),
    ("characters.SorcererFellowship", "characters_sorcererfellowship"),
    ("characters.Specialty", "characters_specialty"),
    ("characters.SpiritCharm", "characters_spiritcharm"),
    ("characters.Tenet", "characters_tenet"),
    ("characters.Thorn", "characters_thorn"),
    ("characters.Totem", "characters_totem"),
    ("characters.Tribe", "characters_tribe"),
    ("characters.VampireClan", "characters_vampireclan"),
    ("characters.VampireSect", "characters_vampiresect"),
    ("characters.VampireTitle", "characters_vampiretitle"),
    ("characters.Visage", "characters_visage"),
    ("characters.WraithFaction", "characters_wraithfaction"),
    ("core.CharacterTemplate", "core_charactertemplate"),
    ("items.ItemModel", "items_itemmodel"),
    ("locations.LocationModel", "locations_locationmodel"),
)
COLUMN = "visibility"


def retire_custom_visibility(apps, schema_editor):
    connection = schema_editor.connection
    tables = table_names(connection)
    q = connection.ops.quote_name
    for label, table in VISIBILITY_TABLES:
        model = live_model(label)
        if model is None or model._meta.db_table != table or table not in tables:
            continue
        field = live_field(model, COLUMN)
        if field is None or field.column != COLUMN or field not in model._meta.local_fields:
            continue
        if COLUMN not in table_columns(connection, table):
            continue
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {q(table)} SET {q(COLUMN)} = %s WHERE {q(COLUMN)} = %s",
                ["PRI", "CUS"],
            )


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0010_unique_weekly_xp_request")]
    operations = [migrations.RunPython(retire_custom_visibility, migrations.RunPython.noop)]

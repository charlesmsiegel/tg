"""Character-creation limits: one source for forms, views and client hints.

Costs live in ``characters.costs``; this module holds the point pools,
per-trait bounds and restriction tables that chargen steps enforce. Per-type
Attribute and Ability priorities remain view adapter configuration
(``primary``/``secondary``/``tertiary``) and are turned into rules by
``attribute_rule`` and ``ability_rule``.
"""

from dataclasses import replace

from characters.rules.allocation import AllocationRule, PriorityRule

ATTRIBUTE_GROUPS = (
    ("physical", ("strength", "dexterity", "stamina")),
    ("social", ("charisma", "manipulation", "appearance")),
    ("mental", ("perception", "intelligence", "wits")),
)

ABILITY_GROUP_NAMES = ("talents", "skills", "knowledges")
CHARGEN_ABILITY_MAXIMUM = 3


def attribute_rule(primary, secondary, tertiary):
    return PriorityRule(
        name="attributes",
        groups=ATTRIBUTE_GROUPS,
        points=(primary, secondary, tertiary),
        base=1,
        minimum=1,
        maximum=5,
        range_message="Attributes must range from 1-5",
        message="Attributes must be distributed {primary}/{secondary}/{tertiary}",
    )


def ability_rule(
    model, form_fields, primary, secondary, tertiary, range_flash=None, flash=None
):
    """Abilities rated 0-3, talents/skills/knowledges summed over the form's fields.

    Mage ability groups include secondary abilities that are not allocated on
    this step, so each group only counts names the form actually offers.
    """
    return PriorityRule(
        name="abilities",
        groups=tuple(
            (group, tuple(name for name in getattr(model, group) if name in form_fields))
            for group in ABILITY_GROUP_NAMES
        ),
        points=(primary, secondary, tertiary),
        minimum=0,
        maximum=CHARGEN_ABILITY_MAXIMUM,
        range_fields=tuple(model.primary_abilities),
        range_message=f"Abilities must range from 0-{CHARGEN_ABILITY_MAXIMUM}",
        range_flash=range_flash or None,
        message="Abilities must be distributed {primary}/{secondary}/{tertiary}",
        flash=flash or None,
    )


CHANGELING_ARTS = AllocationRule(
    name="arts",
    fields=(
        "autumn",
        "chicanery",
        "chronos",
        "contract",
        "dragons_ire",
        "legerdemain",
        "metamorphosis",
        "naming",
        "oneiromancy",
        "primal",
        "pyretics",
        "skycraft",
        "soothsay",
        "sovereign",
        "spring",
        "summer",
        "wayfare",
        "winter",
    ),
    total=3,
    message="Arts must total {total} dots (currently {current})",
    flash="Arts allocation error: You must spend exactly {total} dots. You have {current}.",
    maximum=5,
    maximum_flash="{label} cannot exceed {maximum} dots.",
)

CHANGELING_REALMS = AllocationRule(
    name="realms",
    fields=("actor", "fae", "nature_realm", "prop", "scene", "time"),
    total=5,
    message="Realms must total {total} dots (currently {current})",
    flash="Realms allocation error: You must spend exactly {total} dots. You have {current}.",
    maximum=5,
    maximum_flash="{label} cannot exceed {maximum} dots.",
)

WRAITH_ARCANOI = AllocationRule(
    name="arcanoi",
    fields=(
        "argos",
        "castigate",
        "embody",
        "fatalism",
        "flux",
        "inhabit",
        "keening",
        "lifeweb",
        "moliate",
        "mnemosynis",
        "outrage",
        "pandemonium",
        "phantasm",
        "usury",
        "intimation",
    ),
    total=5,
    message="Arcanoi must total exactly {total} dots (currently {current})",
    flash="Arcanoi allocation error: You must spend exactly {total} dots. You have {current}.",
    maximum=5,
    maximum_message="Arcanoi cannot exceed {maximum} dots",
    maximum_flash="Each Arcanos cannot exceed {maximum} dots.",
)

DEMON_LORES = AllocationRule(
    name="lores",
    fields=(
        "lore_of_the_celestials",
        "lore_of_the_earth",
        "lore_of_the_firmament",
        "lore_of_humanity",
        "lore_of_the_wild",
        "lore_of_light",
        "lore_of_radiance",
        "lore_of_awakening",
        "lore_of_the_fundament",
        "lore_of_patterns",
        "lore_of_portals",
        "lore_of_the_forge",
        "lore_of_longing",
        "lore_of_storms",
        "lore_of_transfiguration",
        "lore_of_the_flesh",
        "lore_of_death",
        "lore_of_the_spirit",
        "lore_of_the_winds",
        "lore_of_flame",
        "lore_of_paths",
    ),
    total=3,
    message="You must spend exactly {total} dots on Lores. Currently: {current}",
)

FALLEN_VIRTUES = AllocationRule(
    name="virtues",
    fields=("conviction", "courage", "conscience"),
    total=6,
    message="Virtues must total {total} dots. Currently: {current}",
)

VAMPIRE_DISCIPLINES = AllocationRule(
    name="disciplines",
    fields=(
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
    ),
    total=3,
    message="You must spend exactly {total} dots on Disciplines. Currently: {current}",
    flash=(
        "Discipline allocation error: You must spend exactly {total} dots. You have {current}."
    ),
    allowed_message="You can only spend starting dots on clan Disciplines.",
    allowed_flash="You can only allocate starting dots to your clan's Disciplines.",
)

# Potence is the fixed first dot every ghoul has; it is not part of the pool.
GHOUL_FIXED_DISCIPLINES = ("potence",)
GHOUL_DISCIPLINES = AllocationRule(
    name="disciplines",
    fields=("celerity", "fortitude", "auspex", "dominate", "obfuscate", "presence"),
    total=2,
    comparison="at_most",
    message="You can spend up to {total} dots on additional Disciplines. Currently: {current}",
    allowed_message=(
        "You can only learn disciplines available from your domitor or physical "
        "disciplines if independent."
    ),
)

VAMPIRE_VIRTUES = AllocationRule(
    name="virtues",
    fields=("conscience", "self_control", "courage"),
    total=7,
    message="Virtues must total {total} dots. Currently: {current}",
    flash="Virtue allocation error: You must spend exactly {total} dots. You have {current}.",
)


def vampire_virtue_rule(vampire):
    """The virtues a vampire actually rates: its Path decides the first two."""
    return replace(VAMPIRE_VIRTUES, fields=vampire.active_virtue_fields())


# Tribal background restrictions for Kinfolk (W20 Kinfolk: A Breed Apart).
# Keyed on Tribe.name because Tribe has no stable slug; one table replaces the
# former view and Kinfolk.add_background if-chains.
KINFOLK_TRIBE_BACKGROUND_LIMITS = {
    "Bone Gnawers": {"forbidden": ("pure_breed",), "max": {"resources": 3}},
    "Glass Walkers": {"forbidden": ("pure_breed", "mentor")},
    "Red Talons": {"forbidden": ("resources", "allies", "contacts")},
    "Shadow Lords": {"forbidden": ("mentor",)},
    "Silent Striders": {"max": {"resources": 3}},
    "Stargazers": {"max": {"resources": 3}},
    "Wendigo": {"max": {"resources": 3}},
    "Silver Fangs": {"required": ("pure_breed",)},
}

# Demon Apocalyptic Form: four traits per Torment state within a point budget.
APOCALYPTIC_FORM_TRAITS_PER_STATE = 4
APOCALYPTIC_FORM_POINT_BUDGET = 16

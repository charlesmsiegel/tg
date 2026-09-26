"""Ordered workflows. Shared tasks compose; bindings keep existing view identities."""

from dataclasses import replace

from .predicates import (
    background,
    completed_fetters,
    completed_passions,
    exhausted_freebies,
    hedge_mage,
    no_languages,
    no_rotes,
    psychic,
)
from .registry import Step, Workflow

# These types currently have detail pages but no creation router. Preserve their
# existing freebie eligibility without inventing a wizard or inheriting its order.
DETAIL_ONLY_FREEBIE_POSITIONS = {
    "autumn_person": 5,
    "inanimae": 5,
    "nunnehi": 5,
    "earthbound": 7,
    "htr_human": 5,
    "hunter": 7,
    "mtr_human": 5,
    "mummy": 7,
    "revenant": 6,
}


def bind(tasks, module, prefix, *, templates=None, views=None):
    templates, views = templates or {}, views or {}
    return Workflow(
        tuple(
            replace(
                task,
                view_path=f"{module}.{views.get(task.key, prefix + task.view_path + 'View')}",
                template=templates.get(task.key, task.template),
            )
            for task in tasks
        )
    )


ATTRIBUTE = Step(
    "attributes", "Attributes", "Attribute", "characters/core/attribute_block/form.html"
)
ABILITY = Step("abilities", "Abilities", "Ability", "characters/core/chargen/abilities.html")
BACKGROUNDS = Step(
    "backgrounds", "Backgrounds", "Backgrounds", "characters/core/background_block/form.html"
)
EXTRAS = Step("biography", "Biography", "Extras", "characters/core/chargen/form.html")
FREEBIES = Step(
    "freebies",
    "Freebies",
    "Freebies",
    "characters/core/chargen/freebies.html",
    skip_if=exhausted_freebies,
)
LANGUAGES = Step(
    "languages",
    "Languages",
    "Languages",
    "characters/core/human/human_language_block_form.html",
    skip_if=no_languages,
)
SPECIALTIES = Step(
    "specialties", "Specialties", "Specialties", "characters/core/chargen/specialties.html"
)
ALLIES = Step(
    "allies", "Allies", "Allies", "characters/core/chargen/form.html", skip_if=background("allies")
)
DISCIPLINES = Step("disciplines", "Disciplines", "Disciplines", "characters/core/chargen/form.html")
VIRTUES = Step("virtues", "Virtues", "Virtues", "characters/core/chargen/form.html")
MENTOR = Step(
    "mentor", "Mentor", "Mentor", "characters/core/chargen/form.html", skip_if=background("mentor")
)
CONTACTS = Step(
    "contacts",
    "Contacts",
    "Contacts",
    "characters/core/chargen/form.html",
    skip_if=background("contacts"),
)
RETAINERS = Step(
    "retainers",
    "Retainers",
    "Retainers",
    "characters/core/chargen/form.html",
    skip_if=background("retainers"),
)
GIFTS = Step("gifts", "Gifts", "Gifts", "characters/core/chargen/form.html")
HISTORY = Step("history", "History", "History", "characters/core/chargen/form.html")
POWERS = Step("powers", "Powers", "Powers", "characters/core/chargen/form.html")
BREEDFACTION = Step(
    "breed_faction", "Breed Faction", "BreedFaction", "characters/core/chargen/form.html"
)
NODE = Step("node", "Node", "Node", "characters/core/chargen/form.html", skip_if=background("node"))
LIBRARY = Step(
    "library",
    "Library",
    "Library",
    "characters/core/chargen/form.html",
    skip_if=background("library"),
)
WONDER = Step(
    "wonder", "Wonder", "Wonder", "characters/core/chargen/form.html", skip_if=background("wonder")
)
ENHANCEMENT = Step(
    "enhancement",
    "Enhancement",
    "Enhancement",
    "characters/core/chargen/form.html",
    skip_if=background("enhancement"),
)
SANCTUM = Step(
    "sanctum",
    "Sanctum",
    "Sanctum",
    "characters/core/chargen/form.html",
    skip_if=background("sanctum"),
)
CHANTRY = Step(
    "chantry",
    "Chantry",
    "Chantry",
    "characters/core/chargen/form.html",
    skip_if=background("chantry"),
)
SPHERES = Step("spheres", "Spheres", "Spheres", "characters/core/chargen/form.html")
FOCUS = Step("focus", "Focus", "Focus", "characters/core/chargen/form.html")
ROTE = Step("rote", "Rote", "Rote", "characters/core/chargen/form.html", skip_if=no_rotes)
FAMILIAR = Step(
    "familiar",
    "Familiar",
    "Familiar",
    "characters/core/chargen/form.html",
    skip_if=background("familiar"),
)
PSYCHIC = Step(
    "psychic", "Psychic", "Psychic", "characters/core/chargen/form.html", skip_if=hedge_mage
)
PATH = Step("path", "Path", "Path", "characters/core/chargen/form.html", skip_if=psychic)
RITUAL = Step("ritual", "Ritual", "Ritual", "characters/core/chargen/form.html", skip_if=psychic)
ARTIFACT = Step(
    "artifact",
    "Artifact",
    "Artifact",
    "characters/core/chargen/form.html",
    skip_if=background("artifact"),
)
ARTSREALMS = Step("arts_realms", "Arts Realms", "ArtsRealms", "characters/core/chargen/form.html")
ARCANOS = Step("arcanos", "Arcanos", "Arcanos", "characters/core/chargen/form.html")
SHADOW = Step("shadow", "Shadow", "Shadow", "characters/core/chargen/form.html")
PASSIONS = Step("passions", "Passions", "Passions", skip_if=completed_passions)
FETTERS = Step("fetters", "Fetters", "Fetters", skip_if=completed_fetters)
LORES = Step("lores", "Lores", "Lores", "characters/core/chargen/form.html")
APOCALYPTICFORM = Step(
    "apocalyptic_form", "Apocalyptic Form", "ApocalypticForm", "characters/core/chargen/form.html"
)
FOLLOWERS = Step(
    "followers",
    "Followers",
    "Followers",
    "characters/core/chargen/form.html",
    skip_if=background("followers"),
)

STATS = (ATTRIBUTE, ABILITY, BACKGROUNDS)
MORTAL = STATS + (EXTRAS, FREEBIES, LANGUAGES)
MAGE_BACKGROUNDS = (NODE, LIBRARY, WONDER, ENHANCEMENT, SANCTUM, ALLIES, CHANTRY, SPECIALTIES)

HUMAN = bind(
    MORTAL + (SPECIALTIES,),
    "characters.views.core.human",
    "Human",
    views={
        "attributes": "HumanAttributeChargenView",
        "abilities": "HumanAbilityChargenView",
        "backgrounds": "HumanBackgroundsChargenView",
        "biography": "HumanBiographicalInformationChargenView",
        "freebies": "HumanFreebiesChargenView",
        "languages": "HumanLanguagesChargenView",
        "specialties": "HumanSpecialtiesChargenView",
    },
)

VTM_HUMAN = bind(
    MORTAL
    + (
        ALLIES,
        SPECIALTIES,
    ),
    "characters.views.vampire.vtmhuman",
    "VtMHuman",
    templates={
        "abilities": "characters/vampire/vtmhuman/ability_block_form.html",
        "allies": "characters/core/chargen/form.html",
    },
)

VAMPIRE = bind(
    STATS
    + (
        DISCIPLINES,
        VIRTUES,
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        ALLIES,
        MENTOR,
        CONTACTS,
        RETAINERS,
        SPECIALTIES,
    ),
    "characters.views.vampire.vampire_chargen",
    "Vampire",
    templates={
        "abilities": "characters/vampire/vtmhuman/ability_block_form.html",
        "disciplines": "characters/vampire/vampire/steps/disciplines.html",
        "virtues": "characters/vampire/vampire/steps/virtues.html",
        "allies": "characters/core/chargen/form.html",
    },
)

GHOUL = bind(
    STATS
    + (
        DISCIPLINES,
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        ALLIES,
        SPECIALTIES,
    ),
    "characters.views.vampire.ghoul_chargen",
    "Ghoul",
    templates={
        "abilities": "characters/vampire/vtmhuman/ability_block_form.html",
        "disciplines": "characters/vampire/ghoul/steps/disciplines.html",
        "allies": "characters/core/chargen/form.html",
    },
)

WTA_HUMAN = bind(
    MORTAL
    + (
        ALLIES,
        SPECIALTIES,
    ),
    "characters.views.werewolf.wtahuman",
    "WtAHuman",
    templates={
        "abilities": "characters/werewolf/wtahuman/ability_block_form.html",
        "allies": "characters/core/chargen/form.html",
    },
)

WEREWOLF = bind(
    STATS
    + (
        GIFTS,
        HISTORY,
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        ALLIES,
        MENTOR,
        CONTACTS,
        SPECIALTIES,
    ),
    "characters.views.werewolf.garou",
    "Werewolf",
    templates={"abilities": "characters/werewolf/wtahuman/ability_block_form.html"},
)

KINFOLK = bind(
    MORTAL
    + (
        ALLIES,
        SPECIALTIES,
    ),
    "characters.views.werewolf.kinfolk",
    "Kinfolk",
    templates={
        "abilities": "characters/werewolf/wtahuman/ability_block_form.html",
        "allies": "characters/core/chargen/form.html",
    },
)

FOMOR = bind(
    STATS
    + (
        POWERS,
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        ALLIES,
        CONTACTS,
        SPECIALTIES,
    ),
    "characters.views.werewolf.fomor",
    "Fomor",
    templates={
        "abilities": "characters/werewolf/wtahuman/ability_block_form.html",
        "powers": "characters/werewolf/fomor/steps/powers.html",
        "allies": "characters/core/chargen/form.html",
    },
)

DRONE = bind(
    MORTAL + (SPECIALTIES,),
    "characters.views.werewolf.drone",
    "Drone",
    templates={"abilities": "characters/werewolf/wtahuman/ability_block_form.html"},
)

FERA = bind(
    (
        BREEDFACTION,
        ATTRIBUTE,
        ABILITY,
        BACKGROUNDS,
        GIFTS,
        HISTORY,
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        ALLIES,
        SPECIALTIES,
    ),
    "characters.views.werewolf.fera",
    "Fera",
    templates={
        "breed_faction": "characters/werewolf/fera/breed_faction_form.html",
        "abilities": "characters/werewolf/wtahuman/ability_block_form.html",
        "gifts": "characters/werewolf/fera/gifts_form.html",
        "history": "characters/werewolf/fera/history_form.html",
        "allies": "characters/core/chargen/form.html",
    },
)

MTA_HUMAN = bind(
    MORTAL + MAGE_BACKGROUNDS,
    "characters.views.mage.mtahuman",
    "MtAHuman",
    templates={
        "abilities": "characters/mage/mtahuman/ability_block_form.html",
        "node": "locations/mage/node/form_include.html",
        "library": "locations/mage/library/form_include.html",
        "wonder": "items/mage/wonder/form_include.html",
        "enhancement": "characters/mage/mage/mage_enhancements_form.html",
        "sanctum": "locations/mage/sanctum/form_include.html",
        "allies": "characters/core/chargen/form.html",
        "chantry": "locations/mage/chantry/select_or_create_form.html",
    },
)

MAGE = bind(
    STATS
    + (
        SPHERES,
        FOCUS,
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        ROTE,
        NODE,
        LIBRARY,
        FAMILIAR,
        WONDER,
        ENHANCEMENT,
        SANCTUM,
        ALLIES,
        MENTOR,
        CONTACTS,
        RETAINERS,
        CHANTRY,
        SPECIALTIES,
    ),
    "characters.views.mage.mage",
    "Mage",
    templates={
        "abilities": "characters/mage/mtahuman/ability_block_form.html",
        "spheres": "characters/mage/mage/mage_powers_block_form.html",
        "focus": "characters/mage/mage/mage_focus_block_form.html",
        "rote": "characters/mage/mage/mage_rote_form_block.html",
        "node": "locations/mage/node/form_include.html",
        "library": "locations/mage/library/form_include.html",
        "familiar": "characters/mage/mage/familiar_form.html",
        "wonder": "items/mage/wonder/form_include.html",
        "enhancement": "characters/mage/mage/mage_enhancements_form.html",
        "sanctum": "locations/mage/sanctum/form_include.html",
        "allies": "characters/core/chargen/form.html",
        "chantry": "locations/mage/chantry/select_or_create_form.html",
    },
)

COMPANION = bind(
    MORTAL + MAGE_BACKGROUNDS,
    "characters.views.mage.companion",
    "Companion",
    templates={
        "abilities": "characters/mage/mtahuman/ability_block_form.html",
        "node": "locations/mage/node/form_include.html",
        "library": "locations/mage/library/form_include.html",
        "wonder": "items/mage/wonder/form_include.html",
        "enhancement": "characters/mage/mage/mage_enhancements_form.html",
        "sanctum": "locations/mage/sanctum/form_include.html",
        "allies": "characters/core/chargen/form.html",
        "chantry": "locations/mage/chantry/select_or_create_form.html",
    },
)

SORCERER = bind(
    STATS
    + (
        PSYCHIC,
        PATH,
        RITUAL,
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        NODE,
        LIBRARY,
        FAMILIAR,
        ARTIFACT,
        ENHANCEMENT,
        SANCTUM,
        ALLIES,
        CHANTRY,
        SPECIALTIES,
    ),
    "characters.views.mage.sorcerer",
    "Sorcerer",
    templates={
        "abilities": "characters/mage/mtahuman/ability_block_form.html",
        "psychic": "characters/mage/sorcerer/sorcerer_psychic_block_form.html",
        "freebies": "characters/mage/sorcerer/steps/freebies.html",
        "path": "characters/mage/sorcerer/sorcerer_path_block_form.html",
        "ritual": "characters/mage/sorcerer/sorcerer_ritual_block_form.html",
        "node": "locations/mage/node/form_include.html",
        "library": "locations/mage/library/form_include.html",
        "familiar": "characters/mage/mage/familiar_form.html",
        "artifact": "items/mage/artifact/form_include.html",
        "enhancement": "characters/mage/mage/mage_enhancements_form.html",
        "sanctum": "locations/mage/sanctum/form_include.html",
        "allies": "characters/core/chargen/form.html",
        "chantry": "locations/mage/chantry/select_or_create_form.html",
    },
)

CTD_HUMAN = bind(
    MORTAL
    + (
        ALLIES,
        SPECIALTIES,
    ),
    "characters.views.changeling.ctdhuman",
    "CtDHuman",
    templates={
        "abilities": "characters/changeling/ctdhuman/ability_block_form.html",
        "allies": "characters/core/chargen/form.html",
    },
)

CHANGELING = bind(
    STATS
    + (
        ARTSREALMS,
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        ALLIES,
        SPECIALTIES,
    ),
    "characters.views.changeling.changeling",
    "Changeling",
    templates={
        "abilities": "characters/changeling/ctdhuman/ability_block_form.html",
        "arts_realms": "characters/changeling/changeling/arts_realms_form.html",
        "allies": "characters/core/chargen/form.html",
    },
)

WTO_HUMAN = bind(
    MORTAL
    + (
        ALLIES,
        SPECIALTIES,
    ),
    "characters.views.wraith.wtohuman",
    "WtOHuman",
    templates={
        "abilities": "characters/wraith/wtohuman/ability_block_form.html",
        "allies": "characters/core/chargen/form.html",
    },
)

WRAITH = bind(
    STATS
    + (
        ARCANOS,
        SHADOW,
        PASSIONS,
        FETTERS,
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        ALLIES,
        MENTOR,
        CONTACTS,
        SPECIALTIES,
    ),
    "characters.views.wraith.wraith_chargen",
    "Wraith",
    templates={
        "abilities": "characters/wraith/wtohuman/ability_block_form.html",
        "arcanos": "characters/wraith/wraith/steps/arcanos.html",
        "shadow": "characters/wraith/wraith/steps/shadow.html",
        "passions": "characters/wraith/wraith/steps/passions.html",
        "fetters": "characters/wraith/wraith/steps/fetters.html",
        "allies": "characters/core/chargen/form.html",
        "mentor": "characters/core/chargen/form.html",
    },
)

DTF_HUMAN = bind(
    MORTAL
    + (
        ALLIES,
        SPECIALTIES,
    ),
    "characters.views.demon.dtfhuman_chargen",
    "DtFHuman",
)

DEMON = bind(
    STATS
    + (
        LORES,
        APOCALYPTICFORM,
        VIRTUES,
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        ALLIES,
        MENTOR,
        CONTACTS,
        RETAINERS,
        FOLLOWERS,
        SPECIALTIES,
    ),
    "characters.views.demon.demon_chargen",
    "Demon",
)

THRALL = bind(
    STATS
    + (
        VIRTUES,
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        ALLIES,
        SPECIALTIES,
    ),
    "characters.views.demon.thrall_chargen",
    "Thrall",
)

WORKFLOWS = {
    "human": HUMAN,
    "vtm_human": VTM_HUMAN,
    "vampire": VAMPIRE,
    "ghoul": GHOUL,
    "wta_human": WTA_HUMAN,
    "werewolf": WEREWOLF,
    "kinfolk": KINFOLK,
    "fomor": FOMOR,
    "drone": DRONE,
    "fera": FERA,
    "ajaba": FERA,
    "ananasi": FERA,
    "bastet": FERA,
    "corax": FERA,
    "grondr": FERA,
    "gurahl": FERA,
    "kitsune": FERA,
    "mokole": FERA,
    "nagah": FERA,
    "nuwisha": FERA,
    "ratkin": FERA,
    "rokea": FERA,
    "mta_human": MTA_HUMAN,
    "mage": MAGE,
    "companion": COMPANION,
    "sorcerer": SORCERER,
    "ctd_human": CTD_HUMAN,
    "changeling": CHANGELING,
    "wto_human": WTO_HUMAN,
    "wraith": WRAITH,
    "dtf_human": DTF_HUMAN,
    "demon": DEMON,
    "thrall": THRALL,
}

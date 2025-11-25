"""Constants and choices used across the application."""


class GameLine:
    """Game line constants for World of Darkness games."""

    WOD = "wod"
    VTM = "vtm"
    WTA = "wta"
    MTA = "mta"
    WTO = "wto"
    CTD = "ctd"
    DTF = "dtf"
    MTR = "mtr"

    CHOICES = [
        (WOD, "World of Darkness"),
        (VTM, "Vampire: the Masquerade"),
        (WTA, "Werewolf: the Apocalypse"),
        (MTA, "Mage: the Ascension"),
        (WTO, "Wraith: the Oblivion"),
        (CTD, "Changeling: the Dreaming"),
        (DTF, "Demon: the Fallen"),
        (MTR, "Mummy: the Resurrection"),
    ]

    # URL path mappings for gamelines
    # Format: (url_path, module_name, namespace)
    # This is the single source of truth for all gameline URL routing.
    # Each app's URL config will attempt to load these modules; missing modules
    # are gracefully handled via exception catching.
    URL_PATTERNS = [
        ("vampire", "vampire", "vampire"),
        ("werewolf", "werewolf", "werewolf"),
        ("mage", "mage", "mage"),
        ("wraith", "wraith", "wraith"),
        ("changeling", "changeling", "changeling"),
        ("demon", "demon", "demon"),
        ("mummy", "mummy", "mummy"),
    ]


class ObjectTypeChoices:
    """Object type constants."""

    CHAR = "char"
    LOC = "loc"
    OBJ = "obj"

    CHOICES = [
        (CHAR, "Character"),
        (LOC, "Location"),
        (OBJ, "Item"),
    ]


class HeadingChoices:
    """Heading/theme style choices."""

    VTM = "vtm_heading"
    WTA = "wta_heading"
    MTA = "mta_heading"
    CTD = "ctd_heading"
    WTO = "wto_heading"
    DTF = "dtf_heading"
    WOD = "wod_heading"

    CHOICES = [
        (VTM, "Vampire: the Masquerade"),
        (WTA, "Werewolf: the Apocalypse"),
        (MTA, "Mage: the Ascension"),
        (CTD, "Changeling: the Dreaming"),
        (WTO, "Wraith: the Oblivion"),
        (DTF, "Demon: the Fallen"),
        (WOD, "World of Darkness"),
    ]


class ThemeChoices:
    """Theme/color scheme choices."""

    LIGHT = "light"
    DARK = "dark"

    CHOICES = [
        (LIGHT, "Light"),
        (DARK, "Dark"),
    ]


class CharacterStatus:
    """Character status choices."""

    UNAPPROVED = "Un"
    SUBMITTED = "Sub"
    APPROVED = "App"
    DECEASED = "Dec"
    RETIRED = "Ret"

    CHOICES = [
        (UNAPPROVED, "Unapproved"),
        (SUBMITTED, "Submitted"),
        (APPROVED, "Approved"),
        (DECEASED, "Deceased"),
        (RETIRED, "Retired"),
    ]


class ImageStatus:
    """Image approval status choices."""

    UNAPPROVED = "un"
    SUBMITTED = "sub"
    APPROVED = "app"

    CHOICES = [
        (UNAPPROVED, "Unapproved"),
        (SUBMITTED, "Submitted"),
        (APPROVED, "Approved"),
    ]


class AbilityFields:
    """Ability field definitions for World of Darkness characters.

    This serves as the single source of truth for ability categorization,
    eliminating duplication in model field definitions.
    """

    TALENTS = [
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
    ]

    SKILLS = [
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
    ]

    KNOWLEDGES = [
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
    ]

    # Combined list of all primary abilities (talents + skills + knowledges)
    PRIMARY_ABILITIES = TALENTS + SKILLS + KNOWLEDGES

class XPApprovalStatus:
    """XP spending approval status choices."""

    PENDING = "Pending"
    APPROVED = "Approved"
    DENIED = "Denied"

    CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (DENIED, "Denied"),
    ]

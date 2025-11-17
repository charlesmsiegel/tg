"""Constants and choices used across the application."""


class GameLine:
    """Game line constants for World of Darkness games."""

    WOD = "wod"
    VTM = "vtm"
    WTA = "wta"
    MTA = "mta"
    WTO = "wto"
    CTD = "ctd"

    CHOICES = [
        (WOD, "World of Darkness"),
        (VTM, "Vampire: the Masquerade"),
        (WTA, "Werewolf: the Apocalypse"),
        (MTA, "Mage: the Ascension"),
        (WTO, "Wraith: the Oblivion"),
        (CTD, "Changeling: the Dreaming"),
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
    WOD = "wod_heading"

    CHOICES = [
        (WOD, "World of Darkness"),
        (VTM, "Vampire: the Masquerade"),
        (WTA, "Werewolf: the Apocalypse"),
        (MTA, "Mage: the Ascension"),
        (CTD, "Changeling: the Dreaming"),
        (WTO, "Wraith: the Oblivion"),
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

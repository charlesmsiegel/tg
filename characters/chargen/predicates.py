"""Read-only applicability checks; GET can evaluate these without side effects."""

from functools import partial


def exhausted_freebies(character):
    return character.freebies_approved and character.freebies == 0


def no_languages(character):
    return not character.merits_and_flaws.filter(name="Language").exists()


def no_background(character, *, name):
    return not character.backgrounds.filter(bg__property_name=name, complete=False).exists()


def background(name):
    return partial(no_background, name=name)


def hedge_mage(character):
    return character.sorcerer_type == "hedge_mage"


def psychic(character):
    return not hedge_mage(character)


def no_rotes(character):
    return character.rote_points == 0


def completed_passions(character):
    return character.has_passions()


def completed_fetters(character):
    return character.has_fetters()

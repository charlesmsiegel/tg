"""Parsing of the display names that spending records store for backgrounds.

An XP or freebie spending record keeps only a display string such as
``"Contacts (Police (Vice))"``: the background name, then the rating's note in
parentheses when it has one. The appliers that approve or revert such a record
have to recover the name and note from that string to find the
``BackgroundRating`` it refers to.
"""


def split_background_trait_name(trait_name: str) -> tuple[str, str]:
    """Return ``(background name, note)`` for a stored background trait name.

    The note starts at the first ``" ("`` and runs to the end of the string
    minus one closing parenthesis, so a note that itself contains parentheses
    round-trips. A name without a note gives an empty note.
    """
    trait_name = trait_name.strip()
    bg_name, separator, rest = trait_name.partition(" (")
    if not separator:
        return trait_name, ""
    note = rest[:-1] if rest.endswith(")") else rest
    return bg_name.strip(), note.strip()

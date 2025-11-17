from characters.models.wraith.faction import WraithFaction

# Major Legions
WraithFaction.objects.get_or_create(
    name="Skeletal Army",
    defaults={
        "faction_type": "legion",
        "description": "Legion of Death, military enforcement",
    }
)[0]

WraithFaction.objects.get_or_create(
    name="Fate Legion",
    defaults={
        "faction_type": "legion",
        "description": "Legion of Destiny",
    }
)[0]

WraithFaction.objects.get_or_create(
    name="Penitent Legion",
    defaults={
        "faction_type": "legion",
        "description": "Legion of Redemption",
    }
)[0]

WraithFaction.objects.get_or_create(
    name="Silent Legion",
    defaults={
        "faction_type": "legion",
        "description": "Legion of Introspection",
    }
)[0]

WraithFaction.objects.get_or_create(
    name="Grim Legion",
    defaults={
        "faction_type": "legion",
        "description": "Legion of Justice",
    }
)[0]

WraithFaction.objects.get_or_create(
    name="Iron Legion",
    defaults={
        "faction_type": "legion",
        "description": "Military Legion",
    }
)[0]

WraithFaction.objects.get_or_create(
    name="Emerald Legion",
    defaults={
        "faction_type": "legion",
        "description": "Regional Legion",
    }
)[0]

# Heretic Groups
WraithFaction.objects.get_or_create(
    name="Renegades",
    defaults={
        "faction_type": "heretic",
        "description": "Anti-hierarchy rebels",
    }
)[0]

WraithFaction.objects.get_or_create(
    name="Freewraiths",
    defaults={
        "faction_type": "heretic",
        "description": "Independent operators",
    }
)[0]

WraithFaction.objects.get_or_create(
    name="Helldivers",
    defaults={
        "faction_type": "heretic",
        "description": "Labyrinth explorers and Spectre hunters",
    }
)[0]

# Spectre Organizations
WraithFaction.objects.get_or_create(
    name="The Hive",
    defaults={
        "faction_type": "spectre",
        "description": "Coordinated Spectre collectives",
    }
)[0]

WraithFaction.objects.get_or_create(
    name="Mortwrights",
    defaults={
        "faction_type": "spectre",
        "description": "Spectre collective consciousness units",
    }
)[0]

# Other Factions
WraithFaction.objects.get_or_create(
    name="Darksiders",
    defaults={
        "faction_type": "other",
        "description": "Order of Redemption researchers",
    }
)[0]

WraithFaction.objects.get_or_create(
    name="Doomslayers",
    defaults={
        "faction_type": "other",
        "description": "Combat specialists and recovery teams",
    }
)[0]

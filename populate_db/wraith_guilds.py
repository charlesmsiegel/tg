from characters.models.wraith.guild import Guild

# 13 Greater Guilds
Guild.objects.get_or_create(
    name="Artificers",
    defaults={
        "guild_type": "greater",
        "willpower": 5,
        "description": "Soulforging and crafting masters, monopoly on Inhabit Arcanos",
    }
)[0]

Guild.objects.get_or_create(
    name="Chanteurs",
    defaults={
        "guild_type": "greater",
        "willpower": 5,
        "description": "Emotion manipulation through sound and music, masters of Keening",
    }
)[0]

Guild.objects.get_or_create(
    name="Harbingers",
    defaults={
        "guild_type": "greater",
        "willpower": 5,
        "description": "Perception, prophecy, and future sight specialists, masters of Argos",
    }
)[0]

Guild.objects.get_or_create(
    name="Masquers",
    defaults={
        "guild_type": "greater",
        "willpower": 5,
        "description": "Body and form modification experts, masters of Moliate",
    }
)[0]

Guild.objects.get_or_create(
    name="Mnemoi",
    defaults={
        "guild_type": "greater",
        "willpower": 5,
        "description": "Memory manipulation and recall specialists, masters of Mnemosynis",
    }
)[0]

Guild.objects.get_or_create(
    name="Monitors",
    defaults={
        "guild_type": "greater",
        "willpower": 5,
        "description": "Connection and network manipulation, masters of Lifeweb",
    }
)[0]

Guild.objects.get_or_create(
    name="Oracles",
    defaults={
        "guild_type": "greater",
        "willpower": 5,
        "description": "Fate and destiny manipulation, masters of Fatalism",
    }
)[0]

Guild.objects.get_or_create(
    name="Pardoners",
    defaults={
        "guild_type": "greater",
        "willpower": 5,
        "description": "Shadow purification and guilt removal, masters of Castigate",
    }
)[0]

Guild.objects.get_or_create(
    name="Proctors",
    defaults={
        "guild_type": "greater",
        "willpower": 5,
        "description": "Manifestation in Skinlands, masters of Embody",
    }
)[0]

Guild.objects.get_or_create(
    name="Sandmen",
    defaults={
        "guild_type": "greater",
        "willpower": 5,
        "description": "Illusion and sensory manipulation, masters of Phantasm",
    }
)[0]

Guild.objects.get_or_create(
    name="Solicitors",
    defaults={
        "guild_type": "banned",
        "willpower": 5,
        "description": "Desire and temptation manipulation, masters of Intimation - BANNED by Dictum Mortuum",
    }
)[0]

Guild.objects.get_or_create(
    name="Spooks",
    defaults={
        "guild_type": "greater",
        "willpower": 5,
        "description": "Rage and violence amplification, masters of Outrage",
    }
)[0]

Guild.objects.get_or_create(
    name="Usurers",
    defaults={
        "guild_type": "greater",
        "willpower": 5,
        "description": "Debt and obligation binding, masters of Usury",
    }
)[0]

# 3 Lesser Guilds
Guild.objects.get_or_create(
    name="Alchemists",
    defaults={
        "guild_type": "banned",
        "willpower": 5,
        "description": "Entropy and decay manipulation, masters of Flux - Officially banned",
    }
)[0]

Guild.objects.get_or_create(
    name="Emissaries",
    defaults={
        "guild_type": "lesser",
        "willpower": 5,
        "description": "Lesser Guild, independent operations",
    }
)[0]

Guild.objects.get_or_create(
    name="Haunters",
    defaults={
        "guild_type": "lesser",
        "willpower": 5,
        "description": "Apparition and nightmare specialists, masters of Pandemonium",
    }
)[0]

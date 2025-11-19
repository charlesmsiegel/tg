from game.models import ObjectType

# WoD Character Objects
ObjectType.objects.get_or_create(name="statistic", type="char", gameline="wod")
ObjectType.objects.get_or_create(name="specialty", type="char", gameline="wod")
ObjectType.objects.get_or_create(name="attribute", type="char", gameline="wod")
ObjectType.objects.get_or_create(name="merit_flaw", type="char", gameline="wod")
human = ObjectType.objects.get_or_create(name="human", type="char", gameline="wod")[0]
ObjectType.objects.get_or_create(name="group", type="char", gameline="wod")
ObjectType.objects.get_or_create(name="derangement", type="char", gameline="wod")
ObjectType.objects.get_or_create(name="character", type="char", gameline="wod")
ObjectType.objects.get_or_create(name="archetype", type="char", gameline="wod")
ObjectType.objects.get_or_create(name="ability", type="char", gameline="wod")
ObjectType.objects.get_or_create(name="background", type="char", gameline="wod")
ObjectType.objects.get_or_create(name="gameline", type="char", gameline="wod")
ObjectType.objects.get_or_create(name="house_rule", type="char", gameline="wod")

# WoD Item Objects
ObjectType.objects.get_or_create(name="weapon", type="obj", gameline="wod")
ObjectType.objects.get_or_create(name="noun", type="obj", gameline="wod")
ObjectType.objects.get_or_create(name="language", type="obj", gameline="wod")
ObjectType.objects.get_or_create(name="medium", type="obj", gameline="wod")
ObjectType.objects.get_or_create(name="material", type="obj", gameline="wod")
ObjectType.objects.get_or_create(name="item", type="obj", gameline="wod")

# WoD Location Objects
ObjectType.objects.get_or_create(name="city", type="loc", gameline="wod")
ObjectType.objects.get_or_create(name="location", type="loc", gameline="wod")

# VtM Character Objects
ObjectType.objects.get_or_create(name="discipline", type="char", gameline="vtm")
ObjectType.objects.get_or_create(name="path", type="char", gameline="vtm")
ObjectType.objects.get_or_create(name="vampire_clan", type="char", gameline="vtm")
ObjectType.objects.get_or_create(name="vampire_sect", type="char", gameline="vtm")
ObjectType.objects.get_or_create(name="vampire", type="char", gameline="vtm")
ObjectType.objects.get_or_create(name="vtm_human", type="char", gameline="vtm")

# WtA Character Objects
werewolf = ObjectType.objects.get_or_create(
    name="werewolf", type="char", gameline="wta"
)[0]
ObjectType.objects.get_or_create(name="battle_scar", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="camp", type="char", gameline="wta")
kinfolk = ObjectType.objects.get_or_create(name="kinfolk", type="char", gameline="wta")[
    0
]
ObjectType.objects.get_or_create(name="fomor", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="wta_human", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="totem", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="spirit", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="spirit_character", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="spirit_charm", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="tribe", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="renown_incident", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="rite", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="gift", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="gift_permission", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="fomori_power", type="char", gameline="wta")

# WtA Item Objects
ObjectType.objects.get_or_create(name="fetish", type="obj", gameline="wta")
ObjectType.objects.get_or_create(name="talen", type="obj", gameline="wta")

# WtA Location Objects
ObjectType.objects.get_or_create(name="caern", type="loc", gameline="wta")

# MtA Character Objects
ObjectType.objects.get_or_create(name="sphere", type="char", gameline="mta")
ObjectType.objects.get_or_create(name="rote", type="char", gameline="mta")
ObjectType.objects.get_or_create(name="resonance", type="char", gameline="mta")
ObjectType.objects.get_or_create(name="instrument", type="char", gameline="mta")
ObjectType.objects.get_or_create(name="practice", type="char", gameline="mta")
ObjectType.objects.get_or_create(
    name="specialized_practice", type="char", gameline="mta"
)
ObjectType.objects.get_or_create(name="corrupted_practice", type="char", gameline="mta")
ObjectType.objects.get_or_create(name="tenet", type="char", gameline="mta")
ObjectType.objects.get_or_create(name="paradigm", type="char", gameline="mta")
ObjectType.objects.get_or_create(name="mage_faction", type="char", gameline="mta")
ObjectType.objects.get_or_create(name="effect", type="char", gameline="mta")
ObjectType.objects.get_or_create(name="advantage", type="char", gameline="mta")
mage = ObjectType.objects.get_or_create(name="mage", type="char", gameline="mta")[0]
ObjectType.objects.get_or_create(name="mta_human", type="char", gameline="mta")
companion = ObjectType.objects.get_or_create(
    name="companion", type="char", gameline="mta"
)[0]
ObjectType.objects.get_or_create(name="cabal", type="char", gameline="mta")
sorcerer = ObjectType.objects.get_or_create(
    name="sorcerer", type="char", gameline="mta"
)[0]

ObjectType.objects.get_or_create(name="wonder", type="obj", gameline="mta")
ObjectType.objects.get_or_create(name="artifact", type="obj", gameline="mta")
ObjectType.objects.get_or_create(name="charm", type="obj", gameline="mta")
ObjectType.objects.get_or_create(name="grimoire", type="obj", gameline="mta")
ObjectType.objects.get_or_create(name="talisman", type="obj", gameline="mta")
ObjectType.objects.get_or_create(name="sorcerer_artifact", type="obj", gameline="mta")

ObjectType.objects.get_or_create(name="chantry", type="loc", gameline="mta")
ObjectType.objects.get_or_create(name="library", type="loc", gameline="mta")
node = ObjectType.objects.get_or_create(name="node", type="loc", gameline="mta")[0]
ObjectType.objects.get_or_create(name="sector", type="loc", gameline="mta")
ObjectType.objects.get_or_create(name="horizon_realm", type="loc", gameline="mta")
ObjectType.objects.get_or_create(name="sanctum", type="loc", gameline="mta")[0]
ObjectType.objects.get_or_create(name="reality_zone", type="loc", gameline="mta")[0]

changeling = ObjectType.objects.get_or_create(
    name="changeling", type="char", gameline="ctd"
)[0]
ObjectType.objects.get_or_create(name="ctd_human", type="char", gameline="ctd")
ObjectType.objects.get_or_create(name="motley", type="char", gameline="ctd")

# WtO Character Objects
ObjectType.objects.get_or_create(name="wto_human", type="char", gameline="wto")

# DtF Character Objects
demon = ObjectType.objects.get_or_create(name="demon", type="char", gameline="dtf")[0]
thrall = ObjectType.objects.get_or_create(name="thrall", type="char", gameline="dtf")[0]
dtfhuman = ObjectType.objects.get_or_create(name="dtf_human", type="char", gameline="dtf")[0]

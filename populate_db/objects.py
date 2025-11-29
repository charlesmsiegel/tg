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
ObjectType.objects.get_or_create(name="vampire_title", type="char", gameline="vtm")
ObjectType.objects.get_or_create(name="vampire", type="char", gameline="vtm")
ObjectType.objects.get_or_create(name="ghoul", type="char", gameline="vtm")
ObjectType.objects.get_or_create(name="revenant", type="char", gameline="vtm")
ObjectType.objects.get_or_create(name="revenant_family", type="char", gameline="vtm")
ObjectType.objects.get_or_create(name="vtm_human", type="char", gameline="vtm")
ObjectType.objects.get_or_create(name="coterie", type="char", gameline="vtm")

# VtM Item Objects
ObjectType.objects.get_or_create(name="vampire_artifact", type="obj", gameline="vtm")
ObjectType.objects.get_or_create(name="bloodstone", type="obj", gameline="vtm")

# VtM Location Objects
ObjectType.objects.get_or_create(name="domain", type="loc", gameline="vtm")
ObjectType.objects.get_or_create(name="elysium", type="loc", gameline="vtm")
ObjectType.objects.get_or_create(name="haven", type="loc", gameline="vtm")
ObjectType.objects.get_or_create(name="rack", type="loc", gameline="vtm")
ObjectType.objects.get_or_create(name="tremere_chantry", type="loc", gameline="vtm")
ObjectType.objects.get_or_create(name="barrens", type="loc", gameline="vtm")

# WtA Character Objects
werewolf = ObjectType.objects.get_or_create(
    name="werewolf", type="char", gameline="wta"
)[0]
ObjectType.objects.get_or_create(name="fera", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="ajaba", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="ananasi", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="bastet", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="corax", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="grondr", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="gurahl", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="kitsune", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="mokole", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="nagah", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="nuwisha", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="ratkin", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="rokea", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="battle_scar", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="camp", type="char", gameline="wta")
kinfolk = ObjectType.objects.get_or_create(name="kinfolk", type="char", gameline="wta")[
    0
]
ObjectType.objects.get_or_create(name="fomor", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="drone", type="char", gameline="wta")
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
ObjectType.objects.get_or_create(name="sept_position", type="char", gameline="wta")
ObjectType.objects.get_or_create(name="pack", type="char", gameline="wta")

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
ObjectType.objects.get_or_create(name="sorcerer_fellowship", type="char", gameline="mta")
ObjectType.objects.get_or_create(name="linear_magic_path", type="char", gameline="mta")
ObjectType.objects.get_or_create(name="linear_magic_ritual", type="char", gameline="mta")

# MtA Item Objects
ObjectType.objects.get_or_create(name="wonder", type="obj", gameline="mta")
ObjectType.objects.get_or_create(name="artifact", type="obj", gameline="mta")
ObjectType.objects.get_or_create(name="charm", type="obj", gameline="mta")
ObjectType.objects.get_or_create(name="grimoire", type="obj", gameline="mta")
ObjectType.objects.get_or_create(name="talisman", type="obj", gameline="mta")
ObjectType.objects.get_or_create(name="sorcerer_artifact", type="obj", gameline="mta")
ObjectType.objects.get_or_create(name="periapt", type="obj", gameline="mta")

# MtA Location Objects
ObjectType.objects.get_or_create(name="chantry", type="loc", gameline="mta")
ObjectType.objects.get_or_create(name="library", type="loc", gameline="mta")
node = ObjectType.objects.get_or_create(name="node", type="loc", gameline="mta")[0]
ObjectType.objects.get_or_create(name="sector", type="loc", gameline="mta")
ObjectType.objects.get_or_create(name="horizon_realm", type="loc", gameline="mta")
ObjectType.objects.get_or_create(name="paradox_realm", type="loc", gameline="mta")
ObjectType.objects.get_or_create(name="sanctum", type="loc", gameline="mta")[0]
ObjectType.objects.get_or_create(name="reality_zone", type="loc", gameline="mta")[0]
ObjectType.objects.get_or_create(name="demesne", type="loc", gameline="mta")

# CtD Character Objects
changeling = ObjectType.objects.get_or_create(
    name="changeling", type="char", gameline="ctd"
)[0]
ObjectType.objects.get_or_create(name="ctd_human", type="char", gameline="ctd")
ObjectType.objects.get_or_create(name="autumn_person", type="char", gameline="ctd")
ObjectType.objects.get_or_create(name="inanimae", type="char", gameline="ctd")
ObjectType.objects.get_or_create(name="nunnehi", type="char", gameline="ctd")
ObjectType.objects.get_or_create(name="motley", type="char", gameline="ctd")
ObjectType.objects.get_or_create(name="kith", type="char", gameline="ctd")
ObjectType.objects.get_or_create(name="house", type="char", gameline="ctd")
ObjectType.objects.get_or_create(name="house_faction", type="char", gameline="ctd")
ObjectType.objects.get_or_create(name="legacy", type="char", gameline="ctd")
ObjectType.objects.get_or_create(name="cantrip", type="char", gameline="ctd")
ObjectType.objects.get_or_create(name="chimera", type="char", gameline="ctd")

# CtD Item Objects
ObjectType.objects.get_or_create(name="treasure", type="obj", gameline="ctd")
ObjectType.objects.get_or_create(name="dross", type="obj", gameline="ctd")

# CtD Location Objects
ObjectType.objects.get_or_create(name="freehold", type="loc", gameline="ctd")
ObjectType.objects.get_or_create(name="dream_realm", type="loc", gameline="ctd")
ObjectType.objects.get_or_create(name="trod", type="loc", gameline="ctd")
ObjectType.objects.get_or_create(name="holding", type="loc", gameline="ctd")

# WtO Character Objects
ObjectType.objects.get_or_create(name="wraith", type="char", gameline="wto")
ObjectType.objects.get_or_create(name="wto_human", type="char", gameline="wto")
ObjectType.objects.get_or_create(name="circle", type="char", gameline="wto")
ObjectType.objects.get_or_create(name="wraith_faction", type="char", gameline="wto")
ObjectType.objects.get_or_create(name="guild", type="char", gameline="wto")
ObjectType.objects.get_or_create(name="arcanos", type="char", gameline="wto")
ObjectType.objects.get_or_create(name="thorn", type="char", gameline="wto")
ObjectType.objects.get_or_create(name="shadow_archetype", type="char", gameline="wto")

# WtO Item Objects
ObjectType.objects.get_or_create(name="wraith_artifact", type="obj", gameline="wto")
ObjectType.objects.get_or_create(name="wraith_relic", type="obj", gameline="wto")

# WtO Location Objects
ObjectType.objects.get_or_create(name="byway", type="loc", gameline="wto")
ObjectType.objects.get_or_create(name="citadel", type="loc", gameline="wto")
ObjectType.objects.get_or_create(name="haunt", type="loc", gameline="wto")
ObjectType.objects.get_or_create(name="necropolis", type="loc", gameline="wto")
ObjectType.objects.get_or_create(name="nihil", type="loc", gameline="wto")
ObjectType.objects.get_or_create(name="wraith_freehold", type="loc", gameline="wto")

# DtF Character Objects
demon = ObjectType.objects.get_or_create(name="demon", type="char", gameline="dtf")[0]
thrall = ObjectType.objects.get_or_create(name="thrall", type="char", gameline="dtf")[0]
earthbound = ObjectType.objects.get_or_create(
    name="earthbound", type="char", gameline="dtf"
)[0]
dtfhuman = ObjectType.objects.get_or_create(
    name="dtf_human", type="char", gameline="dtf"
)[0]
ObjectType.objects.get_or_create(name="conclave", type="char", gameline="dtf")
ObjectType.objects.get_or_create(name="demon_faction", type="char", gameline="dtf")
ObjectType.objects.get_or_create(name="demon_house", type="char", gameline="dtf")
ObjectType.objects.get_or_create(name="lore", type="char", gameline="dtf")
ObjectType.objects.get_or_create(name="visage", type="char", gameline="dtf")
ObjectType.objects.get_or_create(name="pact", type="char", gameline="dtf")
ObjectType.objects.get_or_create(name="demon_ritual", type="char", gameline="dtf")
ObjectType.objects.get_or_create(name="apocalyptic_form_trait", type="char", gameline="dtf")

# DtF Item Objects
ObjectType.objects.get_or_create(name="demon_relic", type="obj", gameline="dtf")

# DtF Location Objects
ObjectType.objects.get_or_create(name="bastion", type="loc", gameline="dtf")
ObjectType.objects.get_or_create(name="reliquary", type="loc", gameline="dtf")

# HtR Character Objects
ObjectType.objects.get_or_create(name="htr_human", type="char", gameline="htr")
ObjectType.objects.get_or_create(name="hunter", type="char", gameline="htr")
ObjectType.objects.get_or_create(name="creed", type="char", gameline="htr")
ObjectType.objects.get_or_create(name="edge", type="char", gameline="htr")
ObjectType.objects.get_or_create(name="hunter_organization", type="char", gameline="htr")

# HtR Item Objects
ObjectType.objects.get_or_create(name="hunter_relic", type="obj", gameline="htr")
ObjectType.objects.get_or_create(name="hunter_gear", type="obj", gameline="htr")

# HtR Location Objects
ObjectType.objects.get_or_create(name="hunting_ground", type="loc", gameline="htr")
ObjectType.objects.get_or_create(name="safehouse", type="loc", gameline="htr")

# MtR Character Objects
ObjectType.objects.get_or_create(name="mtr_human", type="char", gameline="mtr")
ObjectType.objects.get_or_create(name="mummy", type="char", gameline="mtr")
ObjectType.objects.get_or_create(name="dynasty", type="char", gameline="mtr")
ObjectType.objects.get_or_create(name="mummy_title", type="char", gameline="mtr")

# MtR Item Objects
ObjectType.objects.get_or_create(name="mummy_relic", type="obj", gameline="mtr")
ObjectType.objects.get_or_create(name="vessel", type="obj", gameline="mtr")
ObjectType.objects.get_or_create(name="ushabti", type="obj", gameline="mtr")

# MtR Location Objects
ObjectType.objects.get_or_create(name="tomb", type="loc", gameline="mtr")
ObjectType.objects.get_or_create(name="cult_temple", type="loc", gameline="mtr")
ObjectType.objects.get_or_create(name="underground_sanctuary", type="loc", gameline="mtr")

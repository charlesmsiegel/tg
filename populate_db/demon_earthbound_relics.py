"""
Populate database with Earthbound Relics from Demon: Earthbound Chapter 4.

The Earthbound create powerful relics that serve various purposes, usually bestowed
upon their mortal servants. These relics are more powerful than typical fallen
artifacts due to ages of experience in shaping mortal tools.
"""

from items.models.demon.relic import Relic

# EARTHBOUND ENHANCED ITEMS

altar_knife = Relic.objects.get_or_create(
    name="Altar Knife (Earthbound Enhanced)",
    relic_type="enhanced",
    lore_used="Lore of Contamination",
    power="Enhancement must be activated with wielder's own blood (1 health level lethal). Inflicts Strength + 4 lethal damage, difficulty to hit reduced by 4 (min 3)",
    material="Ancient sacrificial knife",
    dice_pool=0,
    difficulty=0,
)[0]
altar_knife.add_source("Demon: Earthbound", 105)

enhanced_body_armor = Relic.objects.get_or_create(
    name="Enhanced Body Armor (Earthbound)",
    relic_type="enhanced",
    lore_used="Lore of Contamination",
    power="Requires activation (call Earthbound's name, spend 1 Willpower). Armor rating 8, no movement penalties when activated",
    material="Modern body armor or ancient mail",
    dice_pool=0,
    difficulty=0,
)[0]
enhanced_body_armor.add_source("Demon: Earthbound", 106)

false_id = Relic.objects.get_or_create(
    name="False ID (Earthbound Enhanced)",
    relic_type="enhanced",
    lore_used="Lore of Contamination",
    power="Provides +4 dice for Subterfuge rolls to convince others of identity, difficulty -1",
    material="Falsified identification documents",
    dice_pool=4,
    difficulty=0,
)[0]
false_id.add_source("Demon: Earthbound", 107)

unscaled_eyes = Relic.objects.get_or_create(
    name="Unscaled Eyes",
    relic_type="enhanced",
    lore_used="Lore of Contamination",
    power="Spectacles that reveal truth from lies. +4 dice for Perception rolls to detect/resist Subterfuge, difficulty -1",
    material="Finely made spectacles or sunglasses",
    dice_pool=4,
    difficulty=0,
)[0]
unscaled_eyes.add_source("Demon: Earthbound", 107)

# EARTHBOUND ENCHANTED ITEMS

celestial_gauntlets = Relic.objects.get_or_create(
    name="Celestial Gauntlets",
    relic_type="enchanted",
    lore_used="Lore of the Flesh",
    power="Red/black leather gloves that improve physical capabilities. Roll 5 dice (diff 6), each success adds 1 to a Physical Attribute (can exceed 5). Excess successes over Wits cost Willpower/inflict bashing damage",
    material="Fine leather gloves (often human skin)",
    dice_pool=5,
    difficulty=6,
)[0]
celestial_gauntlets.add_source("Demon: Earthbound", 108)

veil_of_secrets = Relic.objects.get_or_create(
    name="Veil of Secrets",
    relic_type="enchanted",
    lore_used="Lore of Portals",
    power="Braided rope/chain creating mystical barrier. Roll 10 dice (diff 6), protects 5-yard radius (can trade successes for +5 yards each). Blocks doorways, seals windows, prevents external evocations",
    material="Braided rope of hide/hair, chain, or paneled screen",
    dice_pool=10,
    difficulty=6,
)[0]
veil_of_secrets.add_source("Demon: Earthbound", 108)

pain_of_the_ages = Relic.objects.get_or_create(
    name="Pain of the Ages",
    relic_type="enchanted",
    lore_used="Lore of the Flesh, Lore of Longing",
    power="Torture device inflicting pure agony. Roll 7 dice (diff 6), each success = 1 die wound penalty. If penalty exceeds Stamina+5, victim passes out. Excess over Stamina inflicts lethal damage",
    material="Gleaming tool with flanges, points, ridges, serrated edges",
    dice_pool=7,
    difficulty=6,
)[0]
pain_of_the_ages.add_source("Demon: Earthbound", 109)

press_of_voices = Relic.objects.get_or_create(
    name="Press of Voices",
    relic_type="enchanted",
    lore_used="Lore of Humanity",
    power="Newspaper printing press that makes stories seem credible. Affects 5% of papers printed. Roll 8 dice vs reader's Willpower - success means absolute belief. Created by Hedammu's enslaved demon",
    material="Modern newspaper printing press (massive)",
    dice_pool=8,
    difficulty=0,
)[0]
press_of_voices.add_source("Demon: Earthbound", 109)

# EARTHBOUND DEMONIC ITEMS

black_whip_of_ruin = Relic.objects.get_or_create(
    name="Black Whip of Ruin",
    relic_type="demonic",
    lore_used="Lore of Contamination",
    power="Whip with trapped demon soul. When activated: +2 Initiative, +3 Dexterity+Melee, disarm/sweep at normal difficulty, ignores mundane armor, inflicts aggravated damage. Wounds are ragged and suppurating",
    material="Vicious whip",
    dice_pool=0,
    difficulty=0,
)[0]
black_whip_of_ruin.add_source("Demon: Earthbound", 110)

infernal_grimoire_limited = Relic.objects.get_or_create(
    name="Infernal Grimoire (Limited)",
    relic_type="demonic",
    lore_used="Lore of the Spirit",
    power="Book with trapped demon spirit. Describes single Ability/lore path. Roll 7 dice (diff 6) to extract information. Can teach like mentor. Spirit compelled but may mislead with incomplete info",
    material="Finely wrought tome",
    dice_pool=7,
    difficulty=6,
)[0]
infernal_grimoire_limited.add_source("Demon: Earthbound", 110)

infernal_grimoire_informative = Relic.objects.get_or_create(
    name="Infernal Grimoire (Informative)",
    relic_type="demonic",
    lore_used="Lore of the Spirit, Lore of Patterns",
    power="Book describing all Abilities and lore of trapped spirit, plus memories and rituals. Roll 9 dice (diff 6). Can teach like mentor. Book moves independently to suit owner's needs",
    material="Finely wrought tome with precious ornamentation",
    dice_pool=9,
    difficulty=6,
)[0]
infernal_grimoire_informative.add_source("Demon: Earthbound", 111)

infernal_grimoire_comprehensive = Relic.objects.get_or_create(
    name="Infernal Grimoire (Comprehensive)",
    relic_type="demonic",
    lore_used="Lore of the Spirit, Lore of Patterns",
    power="Book containing everything demon has ever known. All Abilities, lore, rituals, memories including pre-banishment history. Roll 12 dice (diff 6). Ultimate reference, but spirit may mislead",
    material="Baroque tome adorned with gems and precious metals",
    dice_pool=12,
    difficulty=6,
)[0]
infernal_grimoire_comprehensive.add_source("Demon: Earthbound", 111)

childs_companion = Relic.objects.get_or_create(
    name="Child's Companion",
    relic_type="demonic",
    lore_used="Lore of Longing, Lore of the Celestials",
    power="Toy with malicious demon whispering to sleeping children. Roll 6 dice vs Willpower. Success = disturbing visions. After 14 nights of visions, victim loses 1 temp Willpower. At 0 Willpower, gains permanent derangement and is indoctrinated",
    material="Child's toy (teddy bear, doll, etc.)",
    dice_pool=6,
    difficulty=0,
)[0]
childs_companion.add_source("Demon: Earthbound", 111)

ghost_coin = Relic.objects.get_or_create(
    name="Ghost Coin",
    relic_type="demonic",
    lore_used="Lore of Humanity, Lore of Longing, Lore of the Spirit",
    power="Item with trapped mortal soul that whispers to loved ones in dreams. Roll 10 dice vs Willpower. Success = victim listens to conversion attempts. After successes = Willpower, victim is indoctrinated to Earthbound worship",
    material="Jewelry or sentimental trinket of deceased",
    dice_pool=10,
    difficulty=0,
)[0]
ghost_coin.add_source("Demon: Earthbound", 113)

print("Earthbound Relics created successfully!")
print("Enhanced Items: Altar Knife, Body Armor, False ID, Unscaled Eyes")
print("Enchanted Items: Celestial Gauntlets, Veil of Secrets, Pain of the Ages, Press of Voices")
print("Demonic Items: Black Whip, Infernal Grimoires (3 types), Child's Companion, Ghost Coin")

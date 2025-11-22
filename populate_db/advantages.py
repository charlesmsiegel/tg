from characters.models.mage.companion import Advantage

alacrity = Advantage.objects.get_or_create(name="Alacrity")[0].add_source(
    "Gods and Monsters", 201
)
alacrity.add_ratings([2, 4, 6])
armor = Advantage.objects.get_or_create(name="Armor")[0].add_source(
    "Gods and Monsters", 201
)
armor.add_ratings([1, 2, 3, 4, 5])
armor_soak_aggravated = Advantage.objects.get_or_create(name="Armor (Soak Aggravated)")[
    0
].add_source("Gods and Monsters", 201)
armor_soak_aggravated.add_ratings([2, 4, 6, 8, 10])
aura = Advantage.objects.get_or_create(name="Aura")[0].add_source(
    "Gods and Monsters", 202
)
aura.add_ratings([3])
aww = Advantage.objects.get_or_create(name="Aww!")[0].add_source(
    "Gods and Monsters", 202
)
aww.add_ratings([1, 2, 3, 4])
bare_necessities = Advantage.objects.get_or_create(name="Bare Necessities")[0].add_source("Gods and Monsters", 202)
bare_necessities.add_ratings([1, 3])
bioluminescence = Advantage.objects.get_or_create(name="Bioluminescence")[0].add_source("Gods and Monsters", 202)
bioluminescence.add_ratings([1, 2, 3])
blending = Advantage.objects.get_or_create(name="Blending")[0].add_source(
    "Gods and Monsters", 203
)
blending.add_ratings([1])
bond_sharing = Advantage.objects.get_or_create(name="Bond-Sharing")[0].add_source(
    "Gods and Monsters", 203
)
bond_sharing.add_ratings([4, 5, 6])
claws_fangs_or_horns = Advantage.objects.get_or_create(name="Claws, Fangs, or Horns")[
    0
].add_source("Gods and Monsters", 203)
claws_fangs_or_horns.add_ratings([3, 5, 7])
cause_insanity = Advantage.objects.get_or_create(name="Cause Insanity")[0].add_source("Gods and Monsters", 203)
cause_insanity.add_ratings([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
deadly_demise = Advantage.objects.get_or_create(name="Deadly Demise")[0].add_source(
    "Gods and Monsters", 204
)
deadly_demise.add_ratings([2, 4, 6])
elemental_touch = Advantage.objects.get_or_create(name="Elemental Touch")[0].add_source("Gods and Monsters", 204)
elemental_touch.add_ratings([3, 5, 7, 10, 15])
empathic_bond = Advantage.objects.get_or_create(name="Empathic Bond")[0].add_source(
    "Gods and Monsters", 205
)
empathic_bond.add_ratings([2])
extra_heads = Advantage.objects.get_or_create(name="Extra Heads")[0].add_source(
    "Gods and Monsters", 205
)
extra_heads.add_ratings([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
extra_limbs = Advantage.objects.get_or_create(name="Extra Limbs")[0].add_source(
    "Gods and Monsters", 205
)
extra_limbs.add_ratings([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
ferocity = Advantage.objects.get_or_create(name="Ferocity")[0].add_source(
    "Gods and Monsters", 205
)
ferocity.add_ratings([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
flexibility = Advantage.objects.get_or_create(name="Flexibility")[0].add_source(
    "Gods and Monsters", 206
)
flexibility.add_ratings([2])
dominance = Advantage.objects.get_or_create(name="Dominance")[0].add_source(
    "Gods and Monsters", 204
)
dominance.add_ratings([1])
earthbond = Advantage.objects.get_or_create(name="Earthbond")[0].add_source(
    "Gods and Monsters", 204
)
earthbond.add_ratings([2])
hazardous_breath = Advantage.objects.get_or_create(name="Hazardous Breath")[0].add_source("Gods and Monsters", 206)
hazardous_breath.add_ratings([5, 10, 15, 20, 25, 30])
hazardous_breath_aggravated = Advantage.objects.get_or_create(
    name="Hazardous Breath (Aggravated)"
)[0].add_source("Gods and Monsters", 206)
hazardous_breath_aggravated.add_ratings([10, 20, 30, 40, 50, 60])
hazardous_breath_caustic = Advantage.objects.get_or_create(
    name="Hazardous Breath (Caustic)"
)[0].add_source("Gods and Monsters", 206)
hazardous_breath_caustic.add_ratings([7, 14, 21, 28, 35, 42])
hazardous_breath_caustic_aggravated = Advantage.objects.get_or_create(
    name="Hazardous Breath (Caustic, Aggravated)"
)[0].add_source("Gods and Monsters", 206)
hazardous_breath_caustic_aggravated.add_ratings([14, 28, 42, 56, 70, 84])
healing_lick = Advantage.objects.get_or_create(name="Healing Lick")[0].add_source(
    "Gods and Monsters", 206
)
healing_lick.add_ratings([3, 6])
homing_instinct = Advantage.objects.get_or_create(name="Homing Instinct")[0].add_source("Gods and Monsters", 206)
homing_instinct.add_ratings([2, 4])
human_guise = Advantage.objects.get_or_create(name="Human Guise")[0].add_source(
    "Gods and Monsters", 206
)
human_guise.add_ratings([2, 4])
human_speech = Advantage.objects.get_or_create(name="Human Speech")[0].add_source(
    "Gods and Monsters", 207
)
human_speech.add_ratings([1])
information_fount = Advantage.objects.get_or_create(name="Information Fount")[0].add_source("Gods and Monsters", 207)
information_fount.add_ratings([5])
intangibility = Advantage.objects.get_or_create(name="Intangibility")[0].add_source(
    "Gods and Monsters", 207
)
intangibility.add_ratings([8, 10])
mesemerism = Advantage.objects.get_or_create(name="Mesemerism")[0].add_source(
    "Gods and Monsters", 207
)
mesemerism.add_ratings([3, 6])
musical_influence = Advantage.objects.get_or_create(name="Musical Influence")[0].add_source("Gods and Monsters", 208)
musical_influence.add_ratings([6])
musk = Advantage.objects.get_or_create(name="Musk")[0].add_source(
    "Gods and Monsters", 208
)
musk.add_ratings([3])
mystic_shield = Advantage.objects.get_or_create(name="Mystic Shield")[0].add_source(
    "Gods and Monsters", 208
)
mystic_shield.add_ratings([2, 4, 6, 8, 10])
needleteeth = Advantage.objects.get_or_create(name="Needleteeth")[0].add_source(
    "Gods and Monsters", 209
)
needleteeth.add_ratings([3])
nightsight = Advantage.objects.get_or_create(name="Nightsight")[0].add_source(
    "Gods and Monsters", 209
)
nightsight.add_ratings([3])
omega_status = Advantage.objects.get_or_create(name="Omega Status")[0].add_source(
    "Gods and Monsters", 209
)
omega_status.add_ratings([4])
paradox_nullification = Advantage.objects.get_or_create(name="Paradox Nullification")[
    0
].add_source("Gods and Monsters", 209)
paradox_nullification.add_ratings([2, 3, 4, 5, 6])
quills = Advantage.objects.get_or_create(name="Quills")[0].add_source(
    "Gods and Monsters", 209
)
quills.add_ratings([2, 4])
rapid_healing = Advantage.objects.get_or_create(name="Rapid Healing")[0].add_source(
    "Gods and Monsters", 210
)
rapid_healing.add_ratings([2, 4, 6, 8, 10])
razorskin = Advantage.objects.get_or_create(name="Razorskin")[0].add_source(
    "Gods and Monsters", 210
)
razorskin.add_ratings([3])
read_and_write = Advantage.objects.get_or_create(name="Read and Write")[0].add_source("Gods and Monsters", 210)
read_and_write.add_ratings([1])
regrowth = Advantage.objects.get_or_create(name="Regrowth")[0].add_source(
    "Gods and Monsters", 210
)
regrowth.add_ratings([2, 4, 6])
shapechanger = Advantage.objects.get_or_create(name="Shapechanger")[0].add_source(
    "Gods and Monsters", 210
)
shapechanger.add_ratings([3, 5, 8])
size = Advantage.objects.get_or_create(name="Size")[0].add_source(
    "Gods and Monsters", 34
)
size.add_ratings([3, 5, 8])
soak_lethal_damage = Advantage.objects.get_or_create(name="Soak Lethal Damage")[0].add_source("Gods and Monsters", 211)
soak_lethal_damage.add_ratings([3])
soak_aggravated_damage = Advantage.objects.get_or_create(name="Soak Aggravated Damage")[
    0
].add_source("Gods and Monsters", 211)
soak_aggravated_damage.add_ratings([5])
soul_sense_or_death_sense = Advantage.objects.get_or_create(
    name="Soul-Sense/Death-Sense"
)[0].add_source("Gods and Monsters", 211)
soul_sense_or_death_sense.add_ratings([2, 3])
speed = Advantage.objects.get_or_create(name="Speed")[0].add_source(
    "Gods and Monsters", 211
)
speed.add_ratings([2, 4, 6, 8, 10])
spirit_vision = Advantage.objects.get_or_create(name="Spirit Vision")[0].add_source(
    "Gods and Monsters", 212
)
spirit_vision.add_ratings([3])
spirit_travel = Advantage.objects.get_or_create(name="Spirit Travel")[0].add_source(
    "Gods and Monsters", 211
)
spirit_travel.add_ratings([8, 10, 16])
telepathy = Advantage.objects.get_or_create(name="Telepathy")[0].add_source(
    "Gods and Monsters", 212
)
telepathy.add_ratings([2, 4, 6])
telekinesis = Advantage.objects.get_or_create(name="Telekinesis")[0].add_source(
    "Gods and Monsters", 212
)
telekinesis.add_ratings([3, 5, 8, 12])
tides_of_fortune = Advantage.objects.get_or_create(name="Tides of Fortune")[0].add_source("Gods and Monsters", 213)
tides_of_fortune.add_ratings([5])
tunneling = Advantage.objects.get_or_create(name="Tunneling")[0].add_source(
    "Gods and Monsters", 213
)
tunneling.add_ratings([3])
unaging = Advantage.objects.get_or_create(name="Unaging")[0].add_source(
    "Gods and Monsters", 213
)
unaging.add_ratings([5])
universal_translator = Advantage.objects.get_or_create(name="Universal Translator")[0].add_source("Gods and Monsters", 213)
universal_translator.add_ratings([5])
venom_injury = Advantage.objects.get_or_create(name="Venom (Injury)")[0].add_source(
    "Gods and Monsters", 213
)
venom_injury.add_ratings([3, 6, 9, 12, 15, 18, 21])
venom_contact = Advantage.objects.get_or_create(name="Venom (Contact)")[0].add_source("Gods and Monsters", 213)
venom_contact.add_ratings([5, 10, 15, 20, 25, 30])
wall_crawling = Advantage.objects.get_or_create(name="Wall-Crawling")[0].add_source(
    "Gods and Monsters", 213
)
wall_crawling.add_ratings([3])
water_breathing = Advantage.objects.get_or_create(name="Water-Breathing")[0].add_source("Gods and Monsters", 214)
water_breathing.add_ratings([2, 5])
webbing = Advantage.objects.get_or_create(name="Webbing")[0].add_source(
    "Gods and Monsters", 214
)
webbing.add_ratings([5])
wings = Advantage.objects.get_or_create(name="Wings")[0].add_source(
    "Gods and Monsters", 214
)
wings.add_ratings([3, 5])

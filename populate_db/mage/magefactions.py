from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Paradigm, Practice
from characters.models.mage.sphere import Sphere
from populate_db.languages import (
    afghan,
    algonquin,
    anguthimri,
    arabic,
    aramaic,
    chinese,
    egyptian,
    farsi,
    french,
    gaelic,
    greek,
    hebrew,
    hindi,
    irish,
    iroquois,
    japanese,
    koine_greek,
    korean,
    latin,
    mayan,
    nahuatl,
    navaho,
    oromo,
    quechua,
    sanskrit,
    sioux,
    spanish,
    swahili,
    thai,
    vietnamese,
    welsh,
    yoruba,
)
from populate_db.materials import (
    bone,
    cloth,
    iron,
    leather,
    paper,
    parchment,
    steel,
    vellum,
    wood,
)
from populate_db.mediums import book, ebook, flash_drive, scrolls, software, tablets
from populate_db.paradigms_INC import (
    a_mechanistic_cosmos,
    bring_back_the_golden_age,
    divine_and_alive,
    divine_order_earthly_chaos,
    everything_is_an_illusion,
    everything_is_chaos,
    everything_is_data,
    gods_and_monsters,
    have_faith,
    might_is_right,
    one_way_trip_to_oblivion,
    tech_holds_all_answers,
)
from populate_db.practices_INC import (
    alchemy,
    artofdesire,
    bardism,
    chaosmagick,
    craftwork,
    crazywisdom,
    cybernetics,
    dominion,
    faith,
    guttermagick,
    highritualmagick,
    hypertech,
    maleficia,
    martialarts,
    medicinework,
    qi_manipulation,
    realityhacking,
    shamanism,
    voudoun,
    weirdscience,
    witchcraft,
    yoga,
)
from populate_db.spheres import (
    correspondence,
    entropy,
    forces,
    life,
    matter,
    mind,
    prime,
    spirit,
    time,
)

traditions = MageFaction.objects.get_or_create(name="Traditions")[0]
ab = MageFaction.objects.get_or_create(
    name="Akashayana", parent=traditions, founded=-3000
)[0]
ab.paradigms.add(
    bring_back_the_golden_age, everything_is_an_illusion, have_faith, might_is_right
)
ab.affinities.add(life, mind)
ab.practices.add(
    alchemy, craftwork, faith, yoga, dominion, martialarts, qi_manipulation
)
ab.languages.add(chinese, japanese, korean, vietnamese, thai)
ab.materials.add(paper, vellum, parchment, leather, cloth, wood, steel)
ab.media.add(book, scrolls)
ab.save()
MageFaction.objects.get_or_create(name="Shi-Ren", parent=ab)[0]
MageFaction.objects.get_or_create(name="Li-Hai", parent=ab)[0]
MageFaction.objects.get_or_create(name="Kannagara", parent=ab)[0]
MageFaction.objects.get_or_create(name="Jnani", parent=ab)[0]
MageFaction.objects.get_or_create(name="Vajrapani", parent=ab)[0]
MageFaction.objects.get_or_create(name="Wulong", parent=ab)[0]
cc = MageFaction.objects.get_or_create(
    name="Celestial Chorus",
    parent=traditions,
    founded=-1500,
)[0]
cc.affinities.add(forces, prime, spirit)
cc.paradigms.add(divine_and_alive, divine_order_earthly_chaos, have_faith)
cc.practices.add(faith, highritualmagick, bardism)
cc.languages.add(arabic, hebrew, aramaic, latin, koine_greek)
cc.materials.add(paper, vellum, parchment, leather, cloth, wood, steel)
cc.media.add(book, tablets, scrolls)
cc.save()
MageFaction.objects.get_or_create(name="Latitudinarians", parent=cc)[0]
MageFaction.objects.get_or_create(name="Monists", parent=cc)[0]
MageFaction.objects.get_or_create(name="Anchorites", parent=cc)[0]
MageFaction.objects.get_or_create(name="The Alexandrian Society", parent=cc)[0]

cox = MageFaction.objects.get_or_create(
    name="Cult of Ecstasy",
    parent=traditions,
    founded=0,
)[0]
cox.affinities.add(life, mind, time)
cox.paradigms.add(
    divine_and_alive, everything_is_data, everything_is_an_illusion, have_faith
)
cox.practices.add(crazywisdom, guttermagick, yoga, cybernetics, hypertech, bardism)
cox.languages.add(farsi, hindi, afghan, french)
cox.materials.add(paper, vellum, parchment, leather, cloth, wood, steel)
cox.media.add(book, scrolls)
cox.save()
MageFaction.objects.get_or_create(name="Children's Crusade", parent=cox)[0]
MageFaction.objects.get_or_create(name="Cult of Acceptance", parent=cox)[0]
MageFaction.objects.get_or_create(name="Dissonance Society", parent=cox)[0]
MageFaction.objects.get_or_create(name="Erzuli Jingo", parent=cox)[0]
MageFaction.objects.get_or_create(name="Fellowship of Pan", parent=cox)[0]
MageFaction.objects.get_or_create(name="The Joybringers", parent=cox)[0]
MageFaction.objects.get_or_create(name="K'an Lu", parent=cox)[0]
MageFaction.objects.get_or_create(name="Los Sabios Locos", parent=cox)[0]
MageFaction.objects.get_or_create(name="Los Sangradores", parent=cox)[0]
MageFaction.objects.get_or_create(name="Silver Bridges", parent=cox)[0]
MageFaction.objects.get_or_create(name="Vratyas", parent=cox)[0]
MageFaction.objects.get_or_create(name="Hagalaz", parent=cox)[0]
MageFaction.objects.get_or_create(name="Ka'a Klubwerks", parent=cox)[0]
MageFaction.objects.get_or_create(name="Khlysty Flagellants", parent=cox)[0]
MageFaction.objects.get_or_create(name="Studiosi", parent=cox)[0]
MageFaction.objects.get_or_create(name="Umilyenye", parent=cox)[0]

ds = MageFaction.objects.get_or_create(
    name="Dreamspeakers",
    parent=traditions,
    founded=-4000,
)[0]
ds.affinities.add(forces, life, matter, spirit)
ds.paradigms.add(
    gods_and_monsters, bring_back_the_golden_age, divine_and_alive, might_is_right
)
ds.practices.add(medicinework, craftwork, shamanism, crazywisdom, faith)
ds.languages.add(
    quechua,
    spanish,
    swahili,
    yoruba,
    oromo,
    nahuatl,
    mayan,
    algonquin,
    iroquois,
    navaho,
    sioux,
    anguthimri,
)
ds.materials.add(paper, vellum, parchment, leather, cloth, wood, steel)
ds.media.add(book, tablets, scrolls)
ds.save()
MageFaction.objects.get_or_create(name="Baruti", parent=ds)[0]
MageFaction.objects.get_or_create(name="Ghost Wheel Society", parent=ds)[0]
MageFaction.objects.get_or_create(name="Keepers of the Sacred Flame", parent=ds)[0]
MageFaction.objects.get_or_create(name="Red Spear Society", parent=ds)[0]
MageFaction.objects.get_or_create(name="Spirit Smiths", parent=ds)[0]
eu = MageFaction.objects.get_or_create(
    name="Euthanatos",
    parent=traditions,
    founded=-3000,
)[0]
eu.affinities.add(entropy, life, spirit)
eu.paradigms.add(
    divine_and_alive, divine_order_earthly_chaos, everything_is_an_illusion, have_faith
)
eu.practices.add(
    crazywisdom,
    faith,
    highritualmagick,
    medicinework,
    realityhacking,
    martialarts,
    shamanism,
    voudoun,
    yoga,
)
eu.languages.add(hindi, sanskrit, greek)
eu.materials.add(paper, vellum, parchment, leather, cloth, wood, steel)
eu.media.add(book, scrolls)
eu.save()
MageFaction.objects.get_or_create(name="Chakravanti", parent=eu)[0]
MageFaction.objects.get_or_create(name="Madzimbabwe", parent=eu)[0]
MageFaction.objects.get_or_create(name="Vrati", parent=eu)[0]
MageFaction.objects.get_or_create(name="Aided", parent=eu)[0]
MageFaction.objects.get_or_create(name="Hierchthonoi", parent=eu)[0]
ooh = MageFaction.objects.get_or_create(
    name="Order of Hermes", parent=traditions, founded=750
)[0]
ooh.affinities.add(forces)
ooh.paradigms.add(
    a_mechanistic_cosmos,
    bring_back_the_golden_age,
    divine_order_earthly_chaos,
    might_is_right,
    tech_holds_all_answers,
)
ooh.practices.add(alchemy, dominion, highritualmagick)
ooh.languages.add(hebrew, arabic, latin, greek, aramaic, egyptian)
ooh.materials.add(paper, vellum, parchment, leather, cloth, wood, steel, iron)
ooh.media.add(book, scrolls)
ooh.save()
bonisagus = MageFaction.objects.get_or_create(name="House Bonisagus", parent=ooh)[0]
bonisagus.affinities.add(prime)
bonisagus.save()
MageFaction.objects.get_or_create(name="House Ex Miscellanea", parent=ooh)[0]
MageFaction.objects.get_or_create(name="House Criamon", parent=ooh)[0]
MageFaction.objects.get_or_create(name="House Merinita", parent=ooh)[0]
MageFaction.objects.get_or_create(name="House Jerbiton", parent=ooh)[0]
MageFaction.objects.get_or_create(name="House Flambeau", parent=ooh)[0]
fortunae = MageFaction.objects.get_or_create(name="House Fortunae", parent=ooh)[0]
fortunae.affinities.add(entropy)
fortunae.save()
quaesitor = MageFaction.objects.get_or_create(name="House Quaesitor", parent=ooh)[0]
quaesitor.affinities.add(mind, spirit)
quaesitor.save()
shaea = MageFaction.objects.get_or_create(name="House Shaea", parent=ooh)[0]
shaea.affinities.add(time)
shaea.save()
hsolificati = MageFaction.objects.get_or_create(name="House Solificati", parent=ooh)[0]
hsolificati.affinities.add(matter)
hsolificati.save()
tytalus = MageFaction.objects.get_or_create(name="House Tytalus", parent=ooh)[0]
tytalus.affinities.add(mind)
tytalus.save()
verditius = MageFaction.objects.get_or_create(name="House Verditius", parent=ooh)[0]
verditius.affinities.add(matter, correspondence)
verditius.save()
MageFaction.objects.get_or_create(name="House Hong Lei", parent=ooh)[0]
MageFaction.objects.get_or_create(name="House Ngoma", parent=ooh)[0]
MageFaction.objects.get_or_create(name="House Skopos", parent=ooh)[0]
MageFaction.objects.get_or_create(name="House Xaos", parent=ooh)[0]

soe = MageFaction.objects.get_or_create(
    name="Society of Ether",
    parent=traditions,
    founded=1200,
)[0]
soe.affinities.add(forces, matter, prime)
soe.paradigms.add(
    a_mechanistic_cosmos,
    everything_is_data,
    everything_is_an_illusion,
    might_is_right,
    tech_holds_all_answers,
)
soe.practices.add(
    alchemy, craftwork, cybernetics, hypertech, realityhacking, weirdscience
)
soe.languages.add(french, latin)
soe.materials.add(leather, cloth, wood, steel, bone)
soe.media.add(book, flash_drive, ebook, software)
soe.save()
MageFaction.objects.get_or_create(name="The Royal Ethernautical Society", parent=soe)[0]
MageFaction.objects.get_or_create(name="The Cybernetic Research Institute", parent=soe)[
    0
]
MageFaction.objects.get_or_create(name="Progressivists", parent=soe)[0]
MageFaction.objects.get_or_create(name="Utopians", parent=soe)[0]
MageFaction.objects.get_or_create(name="Adventurers", parent=soe)[0]
MageFaction.objects.get_or_create(name="Aquanauts", parent=soe)[0]
MageFaction.objects.get_or_create(name="Dissidents", parent=soe)[0]
verb = MageFaction.objects.get_or_create(
    name="Verbena", parent=traditions, founded=-2000
)[0]
verb.affinities.add(forces, life)
verb.paradigms.add(
    gods_and_monsters,
    bring_back_the_golden_age,
    divine_and_alive,
    everything_is_chaos,
    might_is_right,
)
verb.practices.add(
    witchcraft,
    voudoun,
    dominion,
    weirdscience,
    chaosmagick,
    yoga,
    martialarts,
    highritualmagick,
    cybernetics,
    artofdesire,
    craftwork,
    medicinework,
    hypertech,
)
verb.languages.add(irish, gaelic, welsh)
verb.materials.add(paper, vellum, parchment, leather, cloth, wood, steel)
verb.media.add(book, tablets)
verb.save()
MageFaction.objects.get_or_create(name="Moon-Seekers", parent=verb)[0]
MageFaction.objects.get_or_create(name="Gardeners of the Tree", parent=verb)[0]
MageFaction.objects.get_or_create(name="Life Weavers", parent=verb)[0]
MageFaction.objects.get_or_create(name="Twisters of Fate", parent=verb)[0]
va = MageFaction.objects.get_or_create(
    name="Virtual Adepts",
    parent=traditions,
    founded=1880,
)[0]
va.affinities.add(correspondence, forces)
va.paradigms.add(a_mechanistic_cosmos, everything_is_data)
va.practices.add(
    realityhacking,
    cybernetics,
    hypertech,
    weirdscience,
    martialarts,
    chaosmagick,
    guttermagick,
)
va.languages.add()
va.materials.add(leather, cloth, steel)
va.media.add(book, ebook, software, flash_drive)
va.save()
MageFaction.objects.get_or_create(name="Reality Coders", parent=va)[0]
MageFaction.objects.get_or_create(name="Cyberpunks", parent=va)[0]
MageFaction.objects.get_or_create(name="Chaoticians", parent=va)[0]
MageFaction.objects.get_or_create(name="Cypherpunks", parent=va)[0]
MageFaction.objects.get_or_create(name="Nexplorers", parent=va)[0]

da = MageFaction.objects.get_or_create(name="The Disparate Alliance")[0]
hollow_ones = MageFaction.objects.get_or_create(
    name="Hollow Ones",
    parent=da,
)[0]
hollow_ones.affinities.add(*list(Sphere.objects.all()))
hollow_ones.paradigms.add(
    everything_is_chaos,
    everything_is_an_illusion,
    one_way_trip_to_oblivion,
    have_faith,
)
hollow_ones.practices.add(chaosmagick, guttermagick)
hollow_ones.save()
orphans = MageFaction.objects.get_or_create(
    name="Orphans",
    parent=da,
)[0]
orphans.affinities.add(*list(Sphere.objects.all()))
orphans.paradigms.add(*list(Paradigm.objects.all()))
orphans.practices.add(*list(Practice.objects.all()))
orphans.save()


MageFaction.objects.get_or_create(name="Chevra Kedisha", parent=da)[0]
MageFaction.objects.get_or_create(
    name="Knights of St. George and the Dragon", parent=da
)[0]


kopa_loei = MageFaction.objects.get_or_create(
    name="Kopa Loei",
    parent=da,
)[0]
kopa_loei.affinities.add(*list(Sphere.objects.all()))
kopa_loei.paradigms.add(divine_and_alive, divine_order_earthly_chaos)
kopa_loei.practices.add(shamanism, witchcraft, highritualmagick)
kopa_loei.save()
taftani = MageFaction.objects.get_or_create(name="Taftani", parent=da)[0]
taftani.affinities.add(forces, matter, prime, spirit)
taftani.paradigms.add(divine_order_earthly_chaos, might_is_right)
taftani.practices.add(
    alchemy,
    craftwork,
    highritualmagick,
    crazywisdom,
    artofdesire,
    dominion,
    hypertech,
)
taftani.save()
wulung = MageFaction.objects.get_or_create(name="Wu Lung", parent=da)[0]
wulung.affinities.add(spirit, forces, matter, life)
wulung.paradigms.add(divine_order_earthly_chaos, bring_back_the_golden_age)
wulung.practices.add(highritualmagick, alchemy, martialarts)
wulung.save()
ngoma = MageFaction.objects.get_or_create(name="Ngoma", parent=da)[0]
ngoma.affinities.add(life, mind, prime, spirit)
ngoma.paradigms.add(divine_order_earthly_chaos, tech_holds_all_answers)
ngoma.practices.add(
    highritualmagick,
    alchemy,
    hypertech,
    medicinework,
    craftwork,
    realityhacking,
    artofdesire,
)
ngoma.save()
ahl_i_batin = MageFaction.objects.get_or_create(name="Ahl-i-Batin", parent=da)[0]
ahl_i_batin.affinities.add(correspondence, mind)
ahl_i_batin.paradigms.add(
    divine_order_earthly_chaos, have_faith, everything_is_an_illusion
)
ahl_i_batin.practices.add(
    faith,
    crazywisdom,
    alchemy,
    highritualmagick,
    yoga,
    guttermagick,
    realityhacking,
    chaosmagick,
)
ahl_i_batin.save()
bataa = MageFaction.objects.get_or_create(name="Bata'a", parent=da)[0]
bataa.affinities.add(spirit, life)
bataa.paradigms.add(divine_and_alive, everything_is_chaos, gods_and_monsters)
bataa.practices.add(
    voudoun,
    faith,
    medicinework,
    craftwork,
    guttermagick,
    shamanism,
    weirdscience,
    dominion,
    maleficia,
    martialarts,
)
bataa.save()
cok = MageFaction.objects.get_or_create(
    name="Children of Knowledge",
    parent=da,
)[0]
cok.affinities.add(matter, forces, prime, entropy)
cok.paradigms.add(everything_is_chaos, everything_is_data, everything_is_an_illusion)
cok.practices.add(alchemy, craftwork, crazywisdom, artofdesire, chaosmagick, hypertech)
cok.save()

soh = MageFaction.objects.get_or_create(name="Sisters of Hippolyta", parent=da)[0]
soh.affinities.add(life, mind)
soh.paradigms.add(divine_and_alive, might_is_right, have_faith)
soh.practices.add(
    medicinework, witchcraft, shamanism, highritualmagick, craftwork, martialarts
)
soh.save()
templars = MageFaction.objects.get_or_create(name="Templar Knights", parent=da)[0]
templars.affinities.add(forces, life, mind, prime)
templars.paradigms.add(gods_and_monsters, divine_order_earthly_chaos, might_is_right)
templars.practices.add(faith, martialarts, dominion, craftwork, hypertech)
templars.save()

MageFaction.objects.get_or_create(
    name="The Brothers of St. Christopher", parent=templars
)[0]
MageFaction.objects.get_or_create(name="The Order of St. Michael", parent=templars)[0]
MageFaction.objects.get_or_create(name="Sisters of Gabrielle", parent=templars)[0]

tu = MageFaction.objects.get_or_create(
    name="Technocratic Union",
)[0]
itx = MageFaction.objects.get_or_create(name="Iteration X", parent=tu)[0]
itx.affinities.add(forces, matter, time)
itx.paradigms.add(a_mechanistic_cosmos, tech_holds_all_answers, everything_is_data)
itx.practices.add(
    cybernetics,
    hypertech,
    craftwork,
    martialarts,
    dominion,
    artofdesire,
    realityhacking,
)
itx.save()
nwo = MageFaction.objects.get_or_create(name="New World Order", parent=tu)[0]
nwo.affinities.add(mind, correspondence)
nwo.paradigms.add(gods_and_monsters, might_is_right, tech_holds_all_answers)
nwo.practices.add(dominion, martialarts, hypertech, bardism)
nwo.save()
syn = MageFaction.objects.get_or_create(name="The Syndicate", parent=tu)[0]
syn.affinities.add(entropy, mind, prime)
syn.paradigms.add(might_is_right, one_way_trip_to_oblivion)
syn.practices.add(artofdesire, martialarts, dominion, bardism)
syn.save()
prog = MageFaction.objects.get_or_create(name="Progenitors", parent=tu)[0]
prog.affinities.add(life, entropy, mind)
prog.paradigms.add(might_is_right, divine_and_alive)
prog.practices.add(weirdscience, medicinework, cybernetics, hypertech)
prog.save()
ve = MageFaction.objects.get_or_create(name="Void Engineers", parent=tu)[0]
ve.affinities.add(spirit, correspondence, forces)
ve.paradigms.add(tech_holds_all_answers, gods_and_monsters, everything_is_chaos)
ve.practices.add(hypertech, cybernetics, craftwork, realityhacking, weirdscience)
ve.save()
MageFaction.objects.get_or_create(name="BioMechanics", parent=itx)[0]
MageFaction.objects.get_or_create(name="Statisticians", parent=itx)[0]
MageFaction.objects.get_or_create(name="Time-Motion Managers", parent=itx)[0]
MageFaction.objects.get_or_create(name="Macrotechnicians", parent=itx)[0]
MageFaction.objects.get_or_create(name="Ivory Tower", parent=nwo)[0]
MageFaction.objects.get_or_create(name="The Operatives", parent=nwo)[0]
MageFaction.objects.get_or_create(name="The Watchers", parent=nwo)[0]
MageFaction.objects.get_or_create(name="The Feed", parent=nwo)[0]
MageFaction.objects.get_or_create(name="Division Q", parent=nwo)[0]
MageFaction.objects.get_or_create(name="Media Control", parent=syn)[0]
MageFaction.objects.get_or_create(name="Financiers", parent=syn)[0]
MageFaction.objects.get_or_create(name="Enforcers", parent=syn)[0]
MageFaction.objects.get_or_create(name="Disbursements", parent=syn)[0]
MageFaction.objects.get_or_create(name="Pharmacopoeists", parent=prog)[0]
MageFaction.objects.get_or_create(name="Damage Control", parent=prog)[0]
MageFaction.objects.get_or_create(name="Applied Science", parent=prog)[0]
MageFaction.objects.get_or_create(name="FACADE Engineers", parent=prog)[0]
MageFaction.objects.get_or_create(name="Genegineers", parent=prog)[0]
MageFaction.objects.get_or_create(name="Earth Frontier Division", parent=ve)[0]
MageFaction.objects.get_or_create(name="Research and Execution", parent=ve)[0]
MageFaction.objects.get_or_create(
    name="Neutralization Specialization Corps", parent=ve
)[0]
MageFaction.objects.get_or_create(name="Border Corps Division", parent=ve)[0]
MageFaction.objects.get_or_create(name="Pan-Dimension Corps", parent=ve)[0]

nephandi = MageFaction.objects.get_or_create(name="Nephandi")[0]
kllashaa = MageFaction.objects.get_or_create(name="The K'llashsaa", parent=nephandi)[
    0
].add_source("Book of the Fallen", 71)

malfeans = MageFaction.objects.get_or_create(name="Malfeans", parent=nephandi)[
    0
].add_source("Book of the Fallen", 74)
malfeans.affinities.add(entropy)
malfeans.save()

infernalist = MageFaction.objects.get_or_create(name="Infernalists", parent=nephandi)[
    0
].add_source("Book of the Fallen", 68)
infernalist.practices.add(highritualmagick, witchcraft)
infernalist.save()
MageFaction.objects.get_or_create(name="The New Rite Church", parent=infernalist)[
    0
].add_source("Book of the Fallen", 69)
MageFaction.objects.get_or_create(name="The Cauldron of Banjoko", parent=infernalist)[
    0
].add_source("Book of the Fallen", 69)
MageFaction.objects.get_or_create(
    name="The Lodge of the Crimson Goat", parent=infernalist
)[0].add_source("Book of the Fallen", 69)

baphie = MageFaction.objects.get_or_create(name="Baphies", parent=nephandi)[
    0
].add_source("Book of the Fallen", 76)

exie = MageFaction.objects.get_or_create(name="Obliviates", parent=nephandi)[
    0
].add_source("Book of the Fallen", 79)

hob = MageFaction.objects.get_or_create(name="Heralds of Basilisk", parent=nephandi)[
    0
].add_source("Book of the Fallen", 82)

ironhands = MageFaction.objects.get_or_create(name="Ironhands", parent=nephandi)[
    0
].add_source("Book of the Fallen", 85)
ironhands.practices.add(weirdscience, hypertech, craftwork)
ironhands.save()
MageFaction.objects.get_or_create(name="Hammer Security Response", parent=ironhands)[
    0
].add_source("Book of the Fallen", 86)
MageFaction.objects.get_or_create(
    name="Secure Armaments for Autonomy", parent=ironhands
)[0].add_source("Book of the Fallen", 86)
MageFaction.objects.get_or_create(
    name="The Golem Research and Innovation Project", parent=ironhands
)[0].add_source("Book of the Fallen", 86)
MageFaction.objects.get_or_create(name="The Pipers", parent=ironhands)[0].add_source(
    "Book of the Fallen", 87
)
MageFaction.objects.get_or_create(
    name="Oil Refinement Capacity Advancement Association", parent=ironhands
)[0].add_source("Book of the Fallen", 87)

mammonites = MageFaction.objects.get_or_create(name="Mammonites", parent=nephandi)[
    0
].add_source("Book of the Fallen", 89)

marauders = MageFaction.objects.get_or_create(name="Marauders")[0]
MageFaction.objects.get_or_create(name="Bai Dai", parent=marauders)[0]
uu = MageFaction.objects.get_or_create(name="Umbral Underground", parent=marauders)[0]
MageFaction.objects.get_or_create(name="Numpa Kachpa", parent=uu)[0]
MageFaction.objects.get_or_create(name="Independent", parent=marauders)[0]
MageFaction.objects.get_or_create(name="Butcher Street Regulars", parent=uu)[0]
MageFaction.objects.get_or_create(name="The Railroad", parent=uu)[0]
glh = MageFaction.objects.get_or_create(name="God's Left Hand", parent=marauders)[0]
MageFaction.objects.get_or_create(name="The Sitrin", parent=glh)[0]
MageFaction.objects.get_or_create(name="The P'o Chun", parent=glh)[0]
MageFaction.objects.get_or_create(name="Team 23", parent=glh)[0]

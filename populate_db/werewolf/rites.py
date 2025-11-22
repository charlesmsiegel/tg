from characters.models.werewolf.rite import Rite

Rite.objects.get_or_create(name="Rite of Cleansing", level=1, rite_type="accord")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 203)
Rite.objects.get_or_create(name="Rite of Contrition", level=1, rite_type="accord")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 204)
Rite.objects.get_or_create(name="Rite of Renunciation", level=2, rite_type="accord")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 204)
Rite.objects.get_or_create(name="Rite of the Loyal PAck", level=3, rite_type="accord")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 205)
Rite.objects.get_or_create(name="Enchant the Forest", level=4, rite_type="accord")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 205)
Rite.objects.get_or_create(name="Rite of the Opened Sky", level=4, rite_type="accord")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 205)
moot_rite = Rite.objects.get_or_create(name="Moot Rite", level=1, rite_type="caern")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 206)
Rite.objects.get_or_create(name="Rite of the Opened Caern", level=1, rite_type="caern")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 206)
Rite.objects.get_or_create(
    name="Rite of the Glorious Past", level=3, rite_type="caern"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 206)
Rite.objects.get_or_create(name="The Badger's Burrow", level=4, rite_type="caern")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 206)
Rite.objects.get_or_create(
    name="Rite of the Opened Bridge", level=4, rite_type="caern"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 207)
Rite.objects.get_or_create(
    name="Rite of the Shrouded Glen", level=4, rite_type="caern"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 207)
rite_of_caern_building = Rite.objects.get_or_create(
    name="Rite of Caern Building", level=5, rite_type="caern"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 208)
Rite.objects.get_or_create(
    name="Gathering for the Departed", level=1, rite_type="death"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 209)
Rite.objects.get_or_create(name="Last Blessing", level=1, rite_type="death")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 209)
Rite.objects.get_or_create(name="Rite of the Winter Wolf", level=3, rite_type="death")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 209)
Rite.objects.get_or_create(name="Baptism of Fire", level=1, rite_type="mystic")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 210)
Rite.objects.get_or_create(name="Rite of Binding", level=1, rite_type="mystic")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 210)
Rite.objects.get_or_create(name="Rite of Growth", level=1, rite_type="mystic")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 210)
Rite.objects.get_or_create(name="Rite of Heritage", level=1, rite_type="mystic")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 211)
Rite.objects.get_or_create(
    name="Rite of the Cardboard Palace", level=1, rite_type="mystic"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 211)
Rite.objects.get_or_create(
    name="Rite of the Questing Stone", level=1, rite_type="mystic"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 211)
Rite.objects.get_or_create(
    name="Rite of Talisman Dedication", level=1, rite_type="mystic"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 211)
Rite.objects.get_or_create(name="Rite of Becoming", level=2, rite_type="mystic")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 211)
Rite.objects.get_or_create(
    name="Rite of Spirit Awakening", level=2, rite_type="mystic"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 212)
Rite.objects.get_or_create(name="Rite of Summoning", level=2, rite_type="mystic")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 212)
Rite.objects.get_or_create(name="Rite of Sacred Rebirth", level=5, rite_type="mystic")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 212)
Rite.objects.get_or_create(
    name="Descent Into the Underworld", level=3, rite_type="mystic"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 213)
Rite.objects.get_or_create(name="Rite of the Fetish", level=3, rite_type="mystic")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 213)
Rite.objects.get_or_create(name="Rite of the Totem", level=3, rite_type="mystic")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 213)
Rite.objects.get_or_create(name="Rite of the Jackdaw", level=1, rite_type="punishment")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 214)
rite_of_ostracism = Rite.objects.get_or_create(
    name="Rite of Ostracism", level=2, rite_type="punishment"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 214)
stone_of_scorn = Rite.objects.get_or_create(
    name="Stone of Scorn", level=2, rite_type="punishment"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 214)
rite_of_the_jackal = Rite.objects.get_or_create(
    name="Voice of the Jackal", level=2, rite_type="punishment"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 214)
Rite.objects.get_or_create(name="The Hunt", level=3, rite_type="punishment")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 215)
Rite.objects.get_or_create(
    name="Rite of the Omega Wolf", level=3, rite_type="punishment"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 215)
Rite.objects.get_or_create(name="Satire Rite", level=3, rite_type="punishment")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 215)
Rite.objects.get_or_create(
    name="The Rending of the Veil", level=4, rite_type="punishment"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 216)
Rite.objects.get_or_create(
    name="Gaia's Vengeful Teeth", level=5, rite_type="punishment"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 216)
Rite.objects.get_or_create(name="Rite of Boasting", level=1, rite_type="renown")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 216)
rite_of_wounding = Rite.objects.get_or_create(
    name="Rite of Wounding", level=1, rite_type="renown"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 217)
Rite.objects.get_or_create(name="Rite of Accomplishment", level=2, rite_type="renown")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 217)
rite_of_passage = Rite.objects.get_or_create(
    name="Rite of Passage", level=2, rite_type="renown"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 217)
Rite.objects.get_or_create(name="Rite of Praise", level=2, rite_type="renown")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 217)
Rite.objects.get_or_create(
    name="Rite of the Winter Winds", level=2, rite_type="seasonal"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 218)
Rite.objects.get_or_create(name="Rite of Reawakening", level=2, rite_type="seasonal")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 218)
Rite.objects.get_or_create(name="The Great Hunt", level=2, rite_type="seasonal")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 218)
Rite.objects.get_or_create(name="The Long Vigil", level=3, rite_type="seasonal")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 219)
Rite.objects.get_or_create(name="Bone Rhythms", level=0, rite_type="minor")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 220)
Rite.objects.get_or_create(name="Breath of Gaia", level=0, rite_type="minor")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 220)
Rite.objects.get_or_create(name="Greet the Moon", level=0, rite_type="minor")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 220)
Rite.objects.get_or_create(name="Greet the Sun", level=0, rite_type="minor")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 220)
Rite.objects.get_or_create(name="Hunting Prayer", level=0, rite_type="minor")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 220)
Rite.objects.get_or_create(name="Prayer for the Prey", level=0, rite_type="minor")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 220)

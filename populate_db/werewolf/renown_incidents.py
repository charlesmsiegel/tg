from characters.models.werewolf.renownincident import RenownIncident
from populate_db.werewolf.rites import (
    moot_rite,
    rite_of_caern_building,
    rite_of_ostracism,
    rite_of_passage,
    rite_of_the_jackal,
    rite_of_wounding,
    stone_of_scorn,
)

RenownIncident.objects.get_or_create(
    name="Besting someone (including a spirit) in a riddle contest",
    glory=0,
    honor=0,
    wisdom=3,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 246)
RenownIncident.objects.get_or_create(
    name="Showing restriant in the face of certain death", glory=0, honor=1, wisdom=3
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 246)
RenownIncident.objects.get_or_create(
    name="Ending a threat without serious harm to any Garou", glory=0, honor=0, wisdom=5
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 246)
RenownIncident.objects.get_or_create(
    name="Surviving an Incapacitating wound", glory=2, honor=0, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 246)
RenownIncident.objects.get_or_create(
    name="Surviving any toxic waste attack", glory=2, honor=0, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 246)
RenownIncident.objects.get_or_create(
    name="Attacking a much more powerful force without aid", glory=0, honor=0, wisdom=-3
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 246)
RenownIncident.objects.get_or_create(
    name="Attacking a minion of the Wyrm without regard to personal safety",
    glory=3,
    honor=0,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 246)
RenownIncident.objects.get_or_create(
    name="Defeating a formidable supernatural threat not of the Wyrm (strand spider, master mage, fae warrior, Fera, etc.)",
    glory=2,
    honor=0,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 246)

RenownIncident.objects.get_or_create(
    name="Defeating a very powerful supernatual threat not of the Wyrm (archmage, fae sorcerer, etc.)",
    glory=3,
    honor=0,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Defeating a minor Wyrm threat (Kalus, a Bane-infested animal, young vampire, etc.)",
    glory=2,
    honor=0,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Defeating an average Wyrm threat (Blight Child, fomori, etc.)",
    glory=3,
    honor=0,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Defeating a strong Wyrm threat (Psychomachie, Black Spiral Dancer pack, etc.)",
    glory=5,
    honor=0,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Defeating a very powerful Wyrm threat (Nexus Crawler, elder vampires, etc.)",
    glory=7,
    honor=0,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
# We are currently ignoring the four modifiers on 247 for killing, no other Garou harmed, not being hurt, and enemy with silver
RenownIncident.objects.get_or_create(
    name='Revealing, with certain proof, that a human or Kinfolk is "of the Wyrm"',
    glory=0,
    honor=0,
    wisdom=2,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name='Falsely accusing a Kinfolk of being "of the Wyrm"',
    glory=0,
    honor=-2,
    wisdom=-3,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name='Revealing, with certain proof, that an area or object is "of the Wyrm"',
    glory=0,
    honor=0,
    wisdom=3,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name='Revealing, with certain proof, that a Garou is "of the Wyrm"',
    glory=0,
    honor=0,
    wisdom=6,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name='Falsely accusing a Garou of being "of the Wyrm"', glory=0, honor=-5, wisdom=-4
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Purifying a Wyrm-tainted object, person, or place", glory=0, honor=0, wisdom=2
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Summoning an Incarna avatar", glory=0, honor=0, wisdom=2
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Traveling to any of the Umbral Realms and surviving",
    glory=3,
    honor=0,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Successfully completing a spirit quest in the Umbra",
    glory=0,
    honor=0,
    wisdom=3,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Failing to succeed in a spirit quest in the Umbra",
    glory=0,
    honor=0,
    wisdom=-3,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Having and properly following a prophetic dream", glory=0, honor=0, wisdom=5
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Giving a prophetic warning that later comes true", glory=0, honor=0, wisdom=5
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Ignoring omens, dreams, and the like for no good reason (i.e., suspecting they may be of the Wyrm)",
    glory=0,
    honor=0,
    wisdom=-3,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name='Binding "inappropriate" items to oneself through the Rite of Talisman Dedication',
    glory=0,
    honor=0,
    wisdom=-2,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Spending a year in ritualistic seclusion (fasting, meditation, etc.)",
    glory=0,
    honor=0,
    wisdom=5,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(name="Discovering a talen", glory=0, honor=0, wisdom=1)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(name="Discovering a fetish", glory=0, honor=0, wisdom=2)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Discovering ancient Garou lore", glory=0, honor=0, wisdom=3
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(name="Discovering a Pathstone", glory=0, honor=0, wisdom=4)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Discovering an ancient caern that was lost", glory=0, honor=0, wisdom=7
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Perfomring a Moot Rite", glory=0, honor=2, wisdom=0, rite=moot_rite
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)
RenownIncident.objects.get_or_create(
    name="Refusing to perform a Moot Rite when asked",
    glory=0,
    honor=-3,
    wisdom=0,
    rite=moot_rite,
)[0]
RenownIncident.objects.get_or_create(name="Missing a Moot Rite", glory=0, honor=0, wisdom=-1)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 247)

RenownIncident.objects.get_or_create(
    name="Performing a Rite of Passage",
    glory=0,
    honor=2,
    wisdom=1,
    rite=rite_of_passage,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Receiving a Rite of Wounding",
    glory=2,
    honor=0,
    wisdom=0,
    rite=rite_of_wounding,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Performing a Rite of Caern Building",
    glory=3,
    honor=5,
    wisdom=7,
    rite=rite_of_caern_building,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Participating in a Rite of Caern Building", glory=0, honor=5, wisdom=3
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Participating in a successful Great Hunt rite", glory=3, honor=0, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Participating in a failed Great Hunt rite", glory=-2, honor=0, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Suffering the Rite of Ostracism",
    glory=-1,
    honor=-7,
    wisdom=-1,
    rite=rite_of_ostracism,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Suffering the Stone of Scorn",
    glory=0,
    honor=-8,
    wisdom=-2,
    rite=stone_of_scorn,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Suffering the Rite of the Jackal",
    glory=-2,
    honor=-7,
    wisdom=0,
    rite=rite_of_the_jackal,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
# No test currently for "has a punishment rite"
RenownIncident.objects.get_or_create(
    name="Performing a Punishment Rite", glory=0, honor=2, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Performing a Punishment Rite unjustly", glory=0, honor=-5, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Refusing to participate in a rite", glory=0, honor=0, wisdom=-1
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Giggling, joking, or otherwise being disrespectful during a rite",
    glory=0,
    honor=0,
    wisdom=-3,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(name="Learning a new rite", glory=0, honor=0, wisdom=1)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Discovering/creating a new rite", glory=0, honor=0, wisdom=5
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Discovering/creating a new gift", glory=0, honor=0, wisdom=7
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(name="Creating a talen", glory=0, honor=0, wisdom=1)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Using a fetish for the good of the sept or tribe", glory=0, honor=0, wisdom=2
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Using a fetish for selfish reasons only", glory=0, honor=0, wisdom=-1
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(name="Creating a fetish", glory=0, honor=0, wisdom=4)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Owning a klaive (awarded once, only after three moons of use)",
    glory=2,
    honor=1,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Owning a grand klaive (awarded once, only after three moons of use)",
    glory=3,
    honor=2,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Sacrificing a fetish for the good of the sept or tribe",
    glory=0,
    honor=0,
    wisdom=4,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Accidentally breaking a fetish or talen", glory=0, honor=0, wisdom=-3
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Accidentally breaking or losing a klaive", glory=0, honor=-3, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(name="Helping guard a caern", glory=0, honor=1, wisdom=0)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Staying at your post when on caern watch, even when tempted not to",
    glory=0,
    honor=2,
    wisdom=1,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Not staying at your post when on watch", glory=0, honor=-3, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Not helping guard a caern, even when asked to", glory=0, honor=-3, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Keeping a caern safe from humans through trickery or negotiation",
    glory=0,
    honor=0,
    wisdom=4,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Helping to prevent a caern from being overrun by the Wyrm",
    glory=3,
    honor=4,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Not prevenitng a caern from being overrun by the Wyrm",
    glory=-3,
    honor=-7,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Dying while defending a caern (posthumous)",
    glory=5,
    honor=8,
    wisdom=0,
    posthumous=True,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Single-handedly preventing a caern from being taken by the Wyrm",
    glory=5,
    honor=8,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Teaching other Garou (depends on the depth of study)",
    glory=0,
    honor=3,
    wisdom=4,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="Learning the complete Silver Record (a lifetime's work)",
    glory=0,
    honor=7,
    wisdom=8,
    only_once=True,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="For a homid Garou, surviving to age 75",
    glory=0,
    honor=8,
    wisdom=10,
    breed="homid",
    only_once=True,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)
RenownIncident.objects.get_or_create(
    name="For a lupus Garou, surviving to age 65",
    glory=0,
    honor=8,
    wisdom=10,
    breed="lupus",
    only_once=True,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 248)

RenownIncident.objects.get_or_create(
    name="For a homid, ignoring one's wold nature for too long",
    glory=0,
    honor=0,
    wisdom=-3,
    breed="homid",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="For a metis, attempting to hide one's deformity",
    glory=0,
    honor=0,
    wisdom=-3,
    breed="metis",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="For a lupus, using too many human tools and other Weaver things",
    glory=0,
    honor=0,
    wisdom=-1,
    breed="lupus",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Gaining the position of Pack leader", glory=0, honor=3, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Living alone, without one's pack, except for ritual reasons",
    glory=0,
    honor=0,
    wisdom=-3,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Performing regular duties and chores for the sept (gained at monthly Moot Rite)",
    glory=0,
    honor=1,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Failing to perform regular duties and chores for the sept (subtracted at monthly Moot Rite)",
    glory=0,
    honor=0,
    wisdom=-3,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Disobeying a caern officer without good reason", glory=0, honor=-2, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Serving in any sept position for a year", glory=1, honor=3, wisdom=1
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Refusing any sept position", glory=-1, honor=-2, wisdom=-1
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Maintaining loyal service to a sept for a year", glory=1, honor=2, wisdom=1
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Maintaining loyal service to a tribe for a year", glory=1, honor=3, wisdom=1
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(name="Upholding the Litany", glory=0, honor=3, wisdom=2)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(name="Breaking the Litany", glory=0, honor=-6, wisdom=-3)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Participating in a just challenge", glory=1, honor=2, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Participating in an unjust challenge", glory=0, honor=-3, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Challenging someone too far above or too far below your Rank",
    glory=0,
    honor=-3,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(name="Giving good advice", glory=0, honor=0, wisdom=2)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(name="Giving bad advice", glory=0, honor=0, wisdom=-2)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(name="Mediating a dispute fairly", glory=0, honor=3, wisdom=0)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Mediating a dispute unfairly", glory=0, honor=-4, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(name="Keeping one's promises", glory=0, honor=2, wisdom=0)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Failing to keep one's promises", glory=0, honor=-3, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(name="Being truthful", glory=0, honor=2, wisdom=0)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Being truthful in the face of extreme adversity", glory=0, honor=5, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(name="Being deceptive", glory=0, honor=-3, wisdom=0)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Being deceptive in the face of extreme adversity", glory=0, honor=-1, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Having your trickery backfire", glory=0, honor=0, wisdom=-2
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Attempting to openly act outside one's auspice", glory=1, honor=-3, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Telling a good story at a moot", glory=2, honor=0, wisdom=2
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Telling a true epic at a moot that is later retorld by others",
    glory=3,
    honor=1,
    wisdom=3,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Telling an epic that is entered into the Silver Record",
    glory=0,
    honor=4,
    wisdom=6,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Speaking dishonorably to one's elders", glory=0, honor=-3, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Speaking without permission at a moot", glory=0, honor=-1, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Speaking poorly of the Garou as a whole", glory=0, honor=-2, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Speaking poorly of one's auspice", glory=0, honor=-4, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Speaking poorly of one's tribe", glory=0, honor=-4, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)
RenownIncident.objects.get_or_create(
    name="Speaking poorly of one's pack", glory=0, honor=-6, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 249)

RenownIncident.objects.get_or_create(
    name="Speaking poorly of another tribe (except Bone Gnawers)",
    glory=0,
    honor=-1,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Summoning help when there is no real danger present",
    glory=0,
    honor=-5,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Healing a fellow Garou (non-pack member) unselifishly",
    glory=0,
    honor=0,
    wisdom=1,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Showing mercy to a wayward Garou", glory=0, honor=0, wisdom=3
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Protecting a helpless Garou", glory=0, honor=4, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Not protecting a helpless Garou", glory=0, honor=-5, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Protecting a helpless human", glory=0, honor=2, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Not protecting a helpless human", glory=0, honor=-1, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(name="Protecting a helpless wolf", glory=0, honor=5, wisdom=0)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Not protecting a helpless wolf", glory=0, honor=-6, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Supporting an innocent being accused of a crime (who is later proven innocent)",
    glory=0,
    honor=5,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Supporting an innocent being accused of a crime (who is later proven guilty)",
    glory=0,
    honor=-4,
    wisdom=0,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Dying while defending your pack (posthumous)",
    glory=4,
    honor=6,
    wisdom=0,
    posthumous=True,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Dying in defense of Gaia (posthumous)",
    glory=7,
    honor=7,
    wisdom=0,
    posthumous=True,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Succumbing to a berserk frenzy", glory=0, honor=0, wisdom=-1
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Succumbing to a fox frenzy", glory=-1, honor=0, wisdom=-1
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Succumbing to a fox frenzy and abandoning your pack in time of need",
    glory=0,
    honor=-1,
    wisdom=-2,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Succumbing to a berserk frenzy and injuring fellow Garou",
    glory=0,
    honor=0,
    wisdom=-3,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Succumbing to the thrall of the Wyrm", glory=0, honor=0, wisdom=-4
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Performing a heinous act while in the thrall of the Wyrm (cannibalism, perversion, attacking your own packmates, etc.)",
    glory=0,
    honor=-3,
    wisdom=-1,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Maintaining good relations with nearby Kinfolk", glory=0, honor=0, wisdom=2
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Having poor relations with nearby Kinfolk", glory=0, honor=0, wisdom=-3
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Choosing a mate and breeding", glory=0, honor=0, wisdom=3
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Choosing a mate, but not breeding", glory=0, honor=0, wisdom=-1
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Staying honorably mated for a year", glory=0, honor=2, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(name="Protecting the Veil", glory=0, honor=4, wisdom=0)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(
    name="Harming or rending the Veil", glory=0, honor=-5, wisdom=0
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)
RenownIncident.objects.get_or_create(name="Repairing the Veil", glory=0, honor=3, wisdom=1)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 250)

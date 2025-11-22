from characters.models.werewolf.totem import Totem

Totem.objects.get_or_create(
    name="Falcon",
    cost=5,
    totem_type="respect",
    individual_traits="2 points of Honor Renown",
    pack_traits="Three Dots of Leadership and 4 Willpower points per story",
    ban="Death before Dishonor",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 373)
Totem.objects.get_or_create(
    name="Grandfather Thunder",
    cost=7,
    totem_type="respect",
    individual_traits="1 point of Honor Renown, 2 dice on intimidate rolls when invoking Thunder's name",
    pack_traits="3 dots of Etiquette, 5 points of Willpower per Story, interest of the Shadow Lords",
    ban="Must not show unearned respect",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 373)
Totem.objects.get_or_create(
    name="Pegasus",
    cost=4,
    totem_type="respect",
    individual_traits="2 points of Honor Renown",
    pack_traits="3 dots of Animal Ken and 3 points of Willpower per story, friendship of the Black Furies",
    ban="Cannot refuse to help females of any species",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 373)
Totem.objects.get_or_create(
    name="Stag",
    cost=6,
    totem_type="respect",
    individual_traits="3 points of Honor Renown, 1 point of Stamina only for long-distance running",
    pack_traits="3 dots of Survival and 3 points of Willpower per story, Fianne and the Fae are well-disposed towards the pack",
    ban="Cannot refuse to aid the Fae and must always respect their prey",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 373)
Totem.objects.get_or_create(
    name="Bear",
    cost=5,
    totem_type="war",
    individual_traits="1 dot of Strength, can use Mother's Touch once per day, hibernate for three months, lose 5 points of temporary Honor Renown and reduce all Honor Renown rewards by 1",
    pack_traits="3 dots of Medicine, friendship with Gurahl",
    ban="",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 374)
Totem.objects.get_or_create(
    name="Boar",
    cost=5,
    totem_type="war",
    individual_traits="1 dot of Stamina",
    pack_traits="2 dots of Brawl",
    ban="Never hunt or eat wild boars",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 374)
Totem.objects.get_or_create(
    name="Fenris",
    cost=5,
    totem_type="war",
    individual_traits="2 points of Glory Renown, increase 1 Physical Attribute by 1 dot",
    pack_traits="Respect of the Get of Fenris",
    ban="Never pass up a worthy fight",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 374)
Totem.objects.get_or_create(
    name="Griffin",
    cost=4,
    totem_type="war",
    individual_traits="Communicate with birds of prey, gain 2 dots of Glory Renown",
    pack_traits="3 dots of Alertness and respect of Red Talons",
    ban="Cannot associate with humans, has never accepted a pack with a homid",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 374)
Totem.objects.get_or_create(
    name="Rat",
    cost=5,
    totem_type="war",
    individual_traits="-1 difficulty on all bite rolls and rolls involving stealth or quiet",
    pack_traits="5 Willpower points per story, friendship of Bone Gnawers and some Ratkin",
    ban="Never kill vermin of any kind",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 374)
Totem.objects.get_or_create(
    name="Wendigo",
    cost=7,
    totem_type="war",
    individual_traits="Start each story with +5 points of Rage, gain two dots of Glory Renown",
    pack_traits="Respect of the Wendigo tribe",
    ban="Must aid animists in need",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 374)
Totem.objects.get_or_create(
    name="Chimera",
    cost=7,
    totem_type="wisdom",
    individual_traits="-2 difficulty to solve riddles, interpret dreams, or enigmas, and gain 2 points of Wisdom Renown. They can also disguise themselves as something else in the Umbra with a Gnosis roll at difficulty 7",
    pack_traits="3 dots of Enigmas and 1 dot of Perception",
    ban="Must seek enlightenment",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 375)
Totem.objects.get_or_create(
    name="Cockroach",
    cost=6,
    totem_type="wisdom",
    individual_traits="-2 to all difficulties involving computers, electricity, and applied science. May perceive data streams in the Umbra, parsing it with Gnosis (difficulty 6)",
    pack_traits="3 dice to activate any Gift involving technology",
    ban="Never kill a cockroach",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 375)
Totem.objects.get_or_create(
    name="Owl",
    cost=5,
    totem_type="wisdom",
    individual_traits="Wings in the Umbra, -2 difficulty for stealth and silence, and 2 points of Wisdom Renown",
    pack_traits="Premonitions and prophetic dreams, 3 dice for any Gift that uses air travel, movement, or darkness. May be aided by Silent Striders but will have the enmity of followers of Rat",
    ban="Must leave small rodents tied and helpless in the woods for Owl and his kind",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 375)
Totem.objects.get_or_create(
    name="Raven",
    cost=5,
    totem_type="wisdom",
    individual_traits="One point of Wisdom Renown",
    pack_traits="3 dots of Survival, 1 of Subterfuge, 1 of Enigmas, friendship of Wereravens",
    ban="Cannot carry wealth",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 376)
Totem.objects.get_or_create(
    name="Uktena",
    cost=7,
    totem_type="wisdom",
    individual_traits="3 dice to soak in the Umbra, 2 XP per story to be spent on Enigmas, Occult, Rituals, Gifts, or other mystical knowledge. Two points of Wisdom Renown. +1 difficulty on interacting with werewolves who are not Uktena or Wendigo",
    pack_traits="Treated by the Uktena as brothers",
    ban="Must recover mystical lore, objects, places, and animals from the minions of the Wyrm",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 376)
Totem.objects.get_or_create(
    name="Unicorn",
    cost=7,
    totem_type="wisdom",
    individual_traits="Move at double speed in the Umbra, -2 to all difficulties on healing and empathy, +2 difficulty to attempts to harm Garou who are not Wyrm-tainted, gain 3 points of Wisdom Renown",
    pack_traits="3 dice when using Gifts of healing, strength, and protection. Children of Gaia will aid the pack.",
    ban="Must protect and aid the weak and exploited.",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 376)
Totem.objects.get_or_create(
    name="Coyote",
    cost=7,
    totem_type="cunning",
    individual_traits="-1 from all temporary Wisdowm Renown awards",
    pack_traits="3 dots of stealth, 3 dots of streetwise, 1 dot of subterfuge, 1 dot of survival. Coyote's avatars can always find the pack.",
    ban="",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 376)
Totem.objects.get_or_create(
    name="Cuckoo",
    cost=6,
    totem_type="cunning",
    individual_traits="-2 from awards of temporary Honor Renown",
    pack_traits="1 dot of Manipulation, 2 dots of Subterfuge, the ability to be overlooked",
    ban="Never pass up a chance to improve pack's position at the expense of others",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 376)
Totem.objects.get_or_create(
    name="Fox",
    cost=7,
    totem_type="cunning",
    individual_traits="1 dot of Manipulation, -1 from awards of temporary Honor Renown",
    pack_traits="2 dots of Stealth, 2 dots of Streetwise, and 3 dots of Subterfuge",
    ban="May never participate in a fox hunt and must sabotage any they find",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 377)

"""
Populate database with Earthbound Backgrounds from Demon: Earthbound Chapter 3.

These Backgrounds are available for all Earthbound characters.
Normal Demon characters cannot take these Backgrounds unless they become
Earthbound over the course of a chronicle.
"""

from characters.models.core.background_block import Background

# Codex
codex = Background.objects.get_or_create(name="Codex", property_name="codex")[0]
codex.description = """Over the course of centuries and millennia, the Earthbound have sought desperately after two invaluable commodities. The first is, of course, a cult of worshippers to do the monster's bidding and provide it with Faith. The second is the Celestial and True Names of other demons - not just those of Earthbound who oppose the character, but those of demons who are still in Hell. With the True Name of another demon, the Earthbound can have it summoned from Hell, enslave it or destroy it and devour its soul.

The Codex Background determines how successful the Earthbound has been in learning the True or Celestial Names of other demons. When the character encounters another demon - one who is Earthbound or inhabiting a mortal body - the player may make an Intelligence + Codex roll (difficulty 8). With two successes, the Earthbound knows the Celestial Name of the demon, gaining a slight advantage. With four or more successes, the Earthbound knows the True Name of the demon and can use it against this new rival or potential slave. Only one Codex roll can be made for any demon the Earthbound encounters. If the roll doesn't receive enough successes, the Earthbound has simply never learned the spiritual identity of the newcomer.

A Codex roll can only be made when the Earthbound is in the presence of another demon. The Earthbound cannot simply sit around in its reliquary, trying to remember True Names and setting its worshippers off to summon demons. There are simply too many demons in Hell and on Earth, and the risks are too great to try contacting and controlling a random demon for no reason.

Note: Fallen who become Earthbound over the course of a chronicle cannot purchase this Background. Codex represents an accumulation of knowledge gained over hundreds of years of scrutiny - a luxury not available to newly formed Earthbound.

X You have never paid attention to others of your kind, so you have learned a scant handful of True Names over the millennia of your existence.
• You're aware of the Names of a few of your former brethren, but you haven't actively sought out further Names.
•• Your agents and slaves have searched Creation for clues and information on other demons, and you know the Names of a significant number of them.
••• Finding out the True Names of other demons has been an important priority for you, and you know the spiritual identities of hundreds of them.
•••• You know the True Names of perhaps thousands of demons, and you can identify and control almost any demon you encounter.
••••• Legends tell of a great book, older than any mortal can imagine, that records the True Name of every demon and angel. You are its author."""
codex.save()
codex.add_source("Demon: Earthbound", 75)

# Cult
cult_bg = Background.objects.get_or_create(name="Cult", property_name="cult")[0]
# Note: Cult already exists, but we'll update it with Earthbound-specific info
if not cult_bg.description or len(cult_bg.description) < 100:
    cult_bg.description = """There is power in worship, power both mundane and mystical. Every Earthbound strives to amass a thriving cult of worshippers, and each actively seeks new members and believers for two reasons. First, dedicated worshippers provide the Earthbound with a horde of agents who are able to perform the tasks that it cannot while trapped inside its reliquary. Secondly, the size of the Earthbound's cult determines how often its disciples can meet and perform their black masses. You gain Faith only when your worshippers perform a worship ritual, and such a ritual normally occurs on one of the specific days that is unholy to your cult. See the Worship Background to determine how much Faith you gain with each ritual.

Fallen characters who become Earthbound may purchase this Background with experience points as normal, but the Storyteller should require that any increase be justified by active recruitment efforts during play. Characters must actively work to increase their cults before additional dots can be purchased in this Background.

X You have no worshippers, or perhaps just a handful of dedicated thralls. You have no source of Faith to draw upon, and you risk falling into stasis.
• You have a small cult - perhaps three or four priests and a few dozen worshippers. The group is able to perform a ritual in your service only once a month.
•• Your cult is not large, but it is of a manageable and controllable size - perhaps 10 priests and 20 or 30 followers. The cult is able to perform rituals in your honor twice a month.
••• Your cult is large and probably has branches in several different cities, with more than 100 members. The cult is large enough so that a ritual is performed in your name once a week.
•••• Your cult is huge, with tentacles of control in several different countries. Several hundred mortals obey your every whim. A ritual is performed for you twice a week.
••••• Your followers are everywhere, and temples to your unholy power are hidden in almost every nation. More than 1,000 mortals live and die for your name, and black rituals are performed for your glory almost every day. Not a day goes by without your worshippers performing rituals, and you gain Faith thus once per day."""
    cult_bg.save()
cult_bg.add_source("Demon: Earthbound", 75)

# Hoard
hoard = Background.objects.get_or_create(name="Hoard", property_name="hoard")[0]
hoard.description = """Mortal bodies can hold only so much divine (or infernal) power, and they can channel only a small amount of spiritual energy. Inanimate objects have the capacity to hold much more Faith in reserve, giving even minor Earthbound a vast wellspring of Faith to draw upon for evocations and black miracles.

The character's Hoard Background measures how much temporary Faith its reliquary can hold at any one time. The higher the reliquary's quality is, the more attuned it is to the Earthbound's spirit, and the larger the reliquary is, the more Faith it can contain. Small reliquaries of highly valuable or appropriate materials can hold a great deal of Faith, as can large reliquaries, and those few vessels that are both large and of high quality can hold enormous amounts. Due to their spiritually unattuned nature, improvised reliquaries are poor vessels for Faith. Characters who are bound to improvised reliquaries cannot have more than three dots in Hoard.

X Your reliquary is small and particularly shoddy, and you have not honed its spiritual properties. You can hold a maximum of 10 points of temporary Faith.
• Your reliquary is small, and formed of simple materials, such as iron, stone, glass or plastic. You can hold a maximum of 15 points of temporary Faith.
•• Your reliquary is larger, perhaps the size of a chest or casket. It is made from fine but not exceptional materials with only minor affinities to your nature - perhaps crude crystals, steel, marble and obsidian. You can hold a maximum of 20 points of temporary Faith.
••• Your reliquary is either quite large, made of particularly fine materials or composed of material well attuned to your nature - perhaps rubies and volcanic stone to align with your mastery of fire. You can hold a maximum of 25 points of temporary Faith. This is the maximum Hoard rating possible for Earthbound in improvised reliquaries.
•••• Your reliquary is both large and valuable, a finely crafted object of precious and appropriate materials nearly the size of a man. You can hold a maximum of 30 points of temporary Faith.
••••• Enormous and jaw-droppingly valuable, a king's ransom of precious materials have gone into making your reliquary, an object larger than a man that is worth a fortune in its own right. You can hold a maximum of 35 points of temporary Faith."""
hoard.save()
hoard.add_source("Demon: Earthbound", 76)

# Mastery
mastery = Background.objects.get_or_create(name="Mastery", property_name="mastery")[0]
mastery.description = """The Earthbound are perhaps the greatest masters of lore that Creation has ever seen - even though their lore is a twisted and corrupt thing that can only destroy. While the evocations of other demons are often limited in power and range, the evocations of the Earthbound - powered by staggering expenditures of Faith - can reach across a continent, strike down dozens of victims or set a city afire. The Mastery Background measures how much extra Faith the character can spend on enhancing its evocations. For full details of how the Earthbound enhance their evocations, see "That Hideous Strength" (Demon: Earthbound p. 79).

X Your character has not mastered his lore, so he cannot spend any Faith on enhancing evocations.
• You can spend one point of extra Faith to enhance an aspect of an evocation.
•• You can spend two points of extra Faith to enhance an aspect of an evocation.
••• You can spend three points of extra Faith to enhance an aspect of an evocation.
•••• You can spend four points of extra Faith to enhance an aspect of an evocation.
••••• You can spend five points of extra Faith to enhance an aspect of an evocation."""
mastery.save()
mastery.add_source("Demon: Earthbound", 76)

# Thralls
thralls = Background.objects.get_or_create(name="Thralls", property_name="thralls")[0]
thralls.description = """As well as the devoted followers that worship them, the Earthbound also have need of stronger, more capable agents - ones who are still loyal unto death to their dark master. These thralls might be mortals who have accepted the black gift of the Earthbound's power, or they could be infernal slaves, demons bound to the Earthbound through its knowledge of their True Names. With Storyteller permission, you might even have other supernatural beings as thralls (for more information on the effects of thralldom on other supernatural beings, see the Demon Storytellers Companion).

The Thralls Background replaces the Followers Background, which is available to normal Demon characters. It functions in a very similar way, but while the agents of the Followers Background are normal mortals, those provided by the Thralls Background are much more competent and powerful. They are still insects compared to the power of their Earthbound master, but they are a match for any skilled mortal or even for the average demon. The Storyteller and player should work together to decide on the capabilities of the character's Thralls. Infernal slaves are roughly equal to a starting Demon character, while empowered mortals are skilled examples of their kind. See "Damned Souls" (Demon: Earthbound p. 98) for more details.

X You have no thralls, mortal or supernatural, and you can work only through normal agents and followers.
• You have one thrall.
•• You have two thralls.
••• You have three thralls.
•••• You have four thralls.
••••• You have five thralls."""
thralls.save()
thralls.add_source("Demon: Earthbound", 77)

# Worship
worship = Background.objects.get_or_create(name="Worship", property_name="worship")[0]
worship.description = """It's not enough to merely have a cult of followers and servants. Such pawns might be useful, but they don't provide the Earthbound with what it desperately needs - Faith. The Earthbound gains Faith only if its followers perform a long, complex and symbolic worship ritual, which culminates in the Earthbound gaining Faith equal to the number of participants. The Worship Background determines how many worshippers of the Earthbound participate in each ritual. Other members might be involved, but only on the periphery, and their Faith does not flow to the demon.

Worship also measures how powerful the veneration rituals of the cult are - the shorter, less powerful rites that can grant the Earthbound's player extra dice for evocation rolls. For more details on veneration rituals, see Demon: Earthbound p. 69.

X Your followers have yet to create any worship or veneration rituals, and they cannot offer their Faith to you or assist your evocations.
• Two followers at a time perform private, relatively short rituals. You gain two points of Faith from each ritual. Veneration rituals can last up to two hours and provide up to two extra dice.
•• Four cultists perform a longer ritual that lasts several hours. You gain four points of Faith from each ritual. Veneration rituals can last up to four hours and provide up to four extra dice.
••• Six cultists form the core of a ritual that lasts many hours. You gain six points of Faith from each ritual. Veneration rituals can last up to six hours and provide up to six extra dice.
•••• Eight cultists take turns performing complex rites over the course of more than a day. You gain eight points of Faith from each ritual. Veneration rituals can last up to eight hours and provide up to eight extra dice.
••••• Ten supplicants engage in a long, incredibly complex ritual that goes on for many days. You gain 10 points of Faith from each ritual. Veneration rituals can last up to 10 hours and provide up to 10 extra dice."""
worship.save()
worship.add_source("Demon: Earthbound", 77)

print("Earthbound Backgrounds created successfully!")

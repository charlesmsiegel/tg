"""
Demon: The Fallen Merits and Flaws
Source: Demon Players Guide
"""

from characters.models.core.merit_flaw_block import MeritFlaw
from populate_db.objects import demon, thrall, dtfhuman

# INFERNAL MERITS - Specific to demon nature and celestial heritage

mf = MeritFlaw.objects.get_or_create(name="Angelic Aura")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.description = "Your character exudes the nobility and grace of a Celestial even in her unaltered mortal state. Despite her physical appearance, she radiates an aura of wisdom, confidence and transcendent authority that belies her mortal condition, even as her Torment begins to weigh heavily on her soul. The difficulty of all Charisma and Appearance rolls decreases by one when your character interacts with mortals."
mf.source = "Demon Players Guide, p. 76"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Angelic Gaze")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.description = "The eyes are the windows to the soul, and the act of possession has altered the eyes of your character's mortal host to reflect his celestial nature. A Devil's eyes might be the color of the golden sun or the sullen red of banked embers; a Devourer's eyes might be the lantern yellow of a wolf or lion. The difficulty of all Leadership, Intimidation or Empathy rolls decreases by one."
mf.source = "Demon Players Guide, p. 76"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Debt of Gratitude")[0]
mf.add_ratings([1, 2, 3])
mf.allowed_types.add(demon)
mf.description = "Another demon owes your character a debt of gratitude because of something either he or his liege did for her during the war. The depth of gratitude the demon owes depends on how many points you wish to spend. One point might mean that the demon owes your character a favor; three points might mean that she owes your character her life."
mf.source = "Demon Players Guide, p. 76"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Atavistic Form")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.description = "Upon their return to the mortal world, the fallen have discovered that many of their past exploits have lived on in human legend. Although time and the interpretations of human minds distort these legends, demons are nevertheless able to tap into these atavistic memories through the appearance of their apocalyptic form. Your character's revelatory form is an iconic image in human myth, be it a visage of a dragon, a fire giant or a winsome siren. The difficulty of all Social rolls decreases by one when interacting with mortals when the demon is in apocalyptic form. Additionally, the difficulty to resist the effects of Revelation increases by one."
mf.source = "Demon Players Guide, p. 76"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Dreams of the Past")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.description = "When dreaming, your character is able to recall especially vivid memories of the Age of Wrath, dredging the recollections from deep in her host body's subconscious. Your character has no conscious control over what memories she revisits while she is asleep, but many pertain specifically to the situations and challenges that your character is dealing with at the moment. The Storyteller can use this Merit to impart useful information to your character that she might not otherwise know. Additionally, if your character has the Legacy Background, this Merit reduces the difficulty of all Legacy rolls by one."
mf.source = "Demon Players Guide, p. 76"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Famous Liege")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.description = "Your character is the vassal of a legendary lord of the infernal host, which grants your character an aura of authority and influence beyond her own accomplishments. Most low-ranking demons will be eager to curry your character's favor, hoping to be remembered later when her dark lord has returned in triumph. Upon learning your character's identity, most low-ranking demons will treat you with a certain degree of deference and respect, giving you the benefit of the doubt in most questionable situations. Note that this Merit is separate and in addition to the Eminence Background, which reflects your character's personal rank and influence. The character who possesses both is able to open doors and gain respect in any growing demonic court by virtue of their identity. The Storyteller is the final arbiter as to how much influence and respect your character can command based on the needs of her chronicle."
mf.source = "Demon Players Guide, p. 76-77"
mf.save()

# PHYSICAL MERITS - Related to the mortal host's physical capabilities

mf = MeritFlaw.objects.get_or_create(name="Acute Sense")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "One of your character's senses, be it sight, smell, taste, touch or hearing is exceptionally keen. The difficulty of any roll involving this sense decreases by two."
mf.source = "Demon Players Guide, p. 77"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Good Right Hook")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "The power of your character's punch belies her actual strength. Maybe she took up boxing at the gym, or perhaps she's just been in a lot of fights. Regardless, people tend to fall over when your character hits them. Add two dice to your damage roll for any Brawl-based attack."
mf.source = "Demon Players Guide, p. 77"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Hollow Leg")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character can drink like a fish. The amount of alcohol she can put away during a binge is truly phenomenal. What's more aggravating to her buddies is how little she suffers for it. Anyone who gets in a drinking competition with your character quickly regrets it. Halve any penalties your character suffers for consuming alcohol."
mf.source = "Demon Players Guide, p. 77"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Light Sleeper")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Although your character sleeps well, she is awakened quickly by a commotion. Any disturbance, from an exorcist picking the lock of your character's apartment to a cat getting amorous on a neighboring roof, wakes your character immediately."
mf.source = "Demon Players Guide, p. 77"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Natural Runner")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal host enjoyed running ever since she was a kid. While most people wheeze and complain about exercising, running has always been an absolute pleasure for her. As a result, your character can run like the wind when the occasion demands it. Your character's Dexterity counts as one point higher than it actually is for purposes of determining movement rates."
mf.source = "Demon Players Guide, p. 77"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Perfect Balance")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's sense of balance is superb. Not even the narrowest of ledges scares her because she has such a good command of her physical equilibrium. She's probably a good dancer, too. This Merit allows you to reduce the difficulty of all balance-related rolls by two."
mf.source = "Demon Players Guide, p. 77"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Robust Health")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has the constitution of an ox. She rarely gets ill, if at all, and food poisoning is a stranger to her. Reduce the difficulty of any roll to resist illness or poisoning — including alcohol poisoning — by two."
mf.source = "Demon Players Guide, p. 77"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Sea Legs")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is no landlubber, but a salty sea dog at heart. She's at home on a boat even when traveling rough seas. She suffers no penalty incurred due to rough seas or unpredictable ship motion on any actions performed while aboard."
mf.source = "Demon Players Guide, p. 77"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Bundle of Energy")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is full of energy. She can subsist on five or six hours of sleep a night, being unable to stay in bed any longer. Her days are full of physical activity, and she can work long into the night without penalty."
mf.source = "Demon Players Guide, p. 77"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Catnapper")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "While your character needs six to eight hours of sleep per night, she doesn't need it all at once. She can catch her Zs as and when she can. As long as her naps total six to eight hours in a 24-hour period — and they usually do unless she's forcibly denied naps — she can function as normal."
mf.source = "Demon Players Guide, p. 77"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Forgettable")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "It's not that your character is ugly. It's just that, well, people's eyes tend to slide over her. She's of average height and build, unremarkable looks and run-of-the-mill dress. People have problems remembering her appearance after they meet her, unless she has talked with them for a long time. Certainly, people won't be able to give a useful description of her if they only see her briefly. Your character must have an Appearance of 2 or 3 and a Charisma no higher than 3 to take this Merit. If either of those Attributes moves outside that range through play, you lose this Merit. This Merit applies solely to your character's physical appearance. She might have a dreadful credit rating, a police file as thick as the phone book and a sexual history that would make a porn star blush, but people just don't remember her on the street."
mf.source = "Demon Players Guide, p. 77-78"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Good Night Vision")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Maybe your character's mortal host spent a lot of time camping. Maybe she's just a fisherman who's used to getting up before dawn. For whatever reason, your character's night vision is excellent. The difficulty of Perception rolls decreases by two at night."
mf.source = "Demon Players Guide, p. 78"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Sexy")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's one sexy mutha. She might not necessarily be that classically good looking, but there's something about the way she moves and acts that exudes sexuality. As a result, she draws in members of the opposite sex, or homosexual members of her own sex, with raw animal magnetism. You may reduce the difficulty of any Social roll by two when dealing with a character who is attracted to your character. If you actively attempt to use your character's charms against someone, you may reduce the difficulty by three."
mf.source = "Demon Players Guide, p. 78"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Daredevil")[0]
mf.add_ratings([3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character loves taking risks, and the adrenaline rush she gets helps her succeed at stunts. Whether it's leaping from a moving train or taking on a Devourer in face-to-face combat, your character lives for danger. When attempting such a dangerous action, you can add three dice to your roll and ignore one botch die that results. In general, the action attempted must be at least difficulty 8 and have the potential to inflict three health levels of lethal damage or six levels of bashing damage if you fail. The Storyteller is the final arbiter of when this Merit applies, and he may impose a cap of one hair-raising feat per game session."
mf.source = "Demon Players Guide, p. 78"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Huge Size")[0]
mf.add_ratings([3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is one big individual. He's at least 6'10\" in size and 300 pounds in weight, making his physical presence nearly impossible to ignore. Because of his sheer bulk, your character gains an extra bruised health level. Your Storyteller might also award bonuses for attempts to push objects, break down doors or resist being knocked down."
mf.source = "Demon Players Guide, p. 78"
mf.save()

# SOCIAL MERITS - Part 1 (1-20)

mf = MeritFlaw.objects.get_or_create(name="Approachable")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "There's something very approachable and non-threatening about your character's mortal persona. People find it very easy to start a conversation with her. Reduce the difficulty of any Empathy rolls involving other people or demons by one."
mf.source = "Demon Players Guide, p. 78"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Early Adopter")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "\"Wow! Look at that new palmtop computer. I just got to have one.\" Your character's mortal host was the kind of person who wanted to have the latest gadgets and technology. It's a drain on your character's cash, and her apartment is cluttered with some neat-seeming technology that turned out to be crap, but you have a solid sense of how to use the latest gadgets. You quickly understand and use most new consumer-level technology. Add two dice to any Technology roll when trying to figure out how to use a new gadget."
mf.source = "Demon Players Guide, p. 78"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Funny")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character can make people laugh. Her timing and sense of the absurd is second to none. She's always being invited to parties because she's so much fun. Most importantly, your character is also very good at judging the appropriateness of her humor. Sometimes the right joke can lift the spirits of people when everything seems to be going against them. Therefore, she does what she can to make life more bearable for her friends and compatriots, even when the situation seems darkest. Reduce by two the difficulty of any Social roll that is intended to boost morale."
mf.source = "Demon Players Guide, p. 78"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Good Listener")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has a keen interest in people. She enjoys hearing what they have to say and is prepared to take the time to hear them out without interrupting with her own opinion. Others can sense this, and they open up to your character without really meaning to. The difficulty of all apparently friendly Social rolls that involve people talking to your character decreases by two."
mf.source = "Demon Players Guide, p. 78"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Good Taste")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has a knack for choosing the right food from the menu, telling the right anecdotes and giving the right presents. She's seen the right films for discussion in cultured company, and she wouldn't know who starred in Dumb and Dumber, let alone have the first clue about the plot. Her taste makes forging social contacts among the upper classes much easier, whatever her origins. Reduce the difficulty by two for any Social roll intended to gain acceptance or to impress in a high-society or business situation."
mf.source = "Demon Players Guide, p. 78"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Gossip")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is an incurable gossip, and other gossips recognize a kindred spirit in her. She's more than happy to spend hours shooting the breeze with complete strangers, all the while discussing the minutiae of other people's lives. Reduce the difficulty by two for any Interrogation rolls made in a social situation, without bullying or intimidation."
mf.source = "Demon Players Guide, p. 78"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="In Love")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has fallen for someone (or her mortal host had), and the feeling is reciprocated. The world seems a better place. Colors are brighter, music is more enchanting, and life just seems less desperate. Even the slightest success boosts your confidence. Regain two Willpower instead of one when your character wakes up each morning."
mf.source = "Demon Players Guide, p. 78-79"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Media Junkie")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "TV, radio, newspaper, magazine, film — your character can't get enough. She's a voracious consumer of pop culture and is always up on the latest movies, music and current affairs. Reduce the difficulty by two on any Social or Research roll that involves pop culture."
mf.source = "Demon Players Guide, p. 79"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Natural Leader")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has been gifted with a certain bearing and personality that naturally makes people defer to her opinion or orders. You receive two extra dice on Leadership rolls. Your character must have a Charisma of 3 or greater to purchase this Merit."
mf.source = "Demon Players Guide, p. 79"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Natural Politician")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is right at home among the devious minds of the political world. Whether it's the cut and thrust of office jockeying or the showboating of regional politics, she knows how to get what she wants. You receive two extra dice on Manipulation rolls in social situations that involve an element of politics, such as an office or gun-club meeting. Your character must have a Manipulation of 3 or more to have this Merit. The Politics Ability has no bearing because this Merit represents raw talent, not the knowledge gained through long experience."
mf.source = "Demon Players Guide, p. 79"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Punctual")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is a master of the virtually lost art of turning up on time. If she has a meeting at 10:00 AM, she's sitting in the reception room at 9:59. If she has an 8:00 PM dinner date with her inamorato, she'll be in the restaurant at 8:00 on the dot, so he doesn't end up waiting. Barring deliberate interference in her plans, your character almost always manages things so that she turns up on time. It makes her a great organizer, assuming her allies come through for her."
mf.source = "Demon Players Guide, p. 79"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Smooth")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character might come from the wrong side of the tracks. She might not have known the proper etiquette in every situation. She probably don't have a clue which fork to use when eating out. Yet none of that matters. She presents herself with such an easy grace and carefree attitude that people forgive her most errors. They might not like her much, but they enjoy her company so much that her rougher edges are quickly forgiven and forgotten. Reduce the difficulty of any Manipulation rolls by two."
mf.source = "Demon Players Guide, p. 79"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Way with Words")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Language is a finely honed tool, not a blunt instrument. Your character is able to create exactly the effect she wants by choosing her words carefully, in both written and verbal communication. Gain two dice on any Expression roll that involves words."
mf.source = "Demon Players Guide, p. 79"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Best Friend")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has the good fortune to have a best mate. He stands with your character through thick and thin. They've shared jokes, tragedies and all the highs and lows of life over the years, all of which has forged a bond between them that some married couples never achieve. Perhaps they were at school or worked together. While your character might not be able to share the truth of her real nature with her friend, she can rely on him to back her up to the best of his abilities without asking too many difficult questions. A best friend is closer to you and more committed to helping you than an ally (see the Allies Background on page 153 of the Demon core rules), but he demands far more in return. He goes that extra mile to get her out of trouble that an ally wouldn't, but he counts on her to do the same for him."
mf.source = "Demon Players Guide, p. 79"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Enchanting Voice")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has the most incredible voice. It has a quality that makes people unable to ignore it. If she whispers seductive words in someone's ear, his heart melts. If she demands that someone do something, he springs into action at her behest. The difficulty of all rolls involving the use of your character's voice to persuade, seduce, charm or give orders decreases by two."
mf.source = "Demon Players Guide, p. 79"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Fashion Sense")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character doesn't just dress well, she has an innate sense of what sort of clothes suit a particular occasion. This sense isn't a case of slavishly following the latest trends from the hottest designers either, it's a matter of knowing when to dress smart and when to be casual and having the know-how to carry it off on a limited budget. Subtract one from the difficulty of Social rolls in situations where dressing appropriately is important, such as in a business meeting, chatting at a club or attending an upper-crust function."
mf.source = "Demon Players Guide, p. 79"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Flirt")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal friends claim that she's a terrible flirt, but that quite manifestly isn't true. She's great at it. She's an absolute master at all the subtle signals that give off that particular combination of promise and denial that makes teasing so much fun. At her best, she can make members of the opposite sex, or members of the same sex, putty in her hands. Add two dice to all Social rolls in such circumstances."
mf.source = "Demon Players Guide, p. 79"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Good Sense of Character")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has an innate instinct for reading a person. She can make an appraisal of the kind of person someone is after meeting him for a few seconds, based on little more than gut instinct. She is rarely wrong. Decrease the difficulty by two on any Perception roll based on assessing a person or demon."
mf.source = "Demon Players Guide, p. 80"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Great Liar")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Lying comes naturally to your character. Even the most involved deception sounds like God's own truth when it comes tripping off her honeyed tongue. Gain two dice on any Social roll that involves lying to or deceiving another person or demon."
mf.source = "Demon Players Guide, p. 80"
mf.save()

# SOCIAL MERITS - Part 2 (21-37)

mf = MeritFlaw.objects.get_or_create(name="Laid-Back Friends")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Everyone needs good buddies, and your character has a particularly good bunch. They're pretty cool about when they see her; they don't get all uptight if she's not in contact for a while. They're also great at not interfering with her life. Sure, she's gone through some changes of late, but that's her choice. They'll be there if she wants to talk or needs help, but they'll otherwise keep the hell out of her hair. If these guys are also your character's allies (as per the Background), they'll help her without asking too many difficult questions. Hey, that's her business, right?"
mf.source = "Demon Players Guide, p. 80"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="People Person")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is a social animal. She just likes being around others. Hell, they like being around her. Her open and gregarious nature makes people warm to her quickly. The difficulty decreases by two on any Social roll to create a good impression on another."
mf.source = "Demon Players Guide, p. 80"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Pillar of the Community")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is a fine, upstanding person, respected by those around her. Through participation in local events, helping out with community groups or helping others, she's become well liked and trusted by those who live around her. When she brings them a warning of potential danger or offers an explanation of strange, miraculous events, they're likely to believe her. She might even be able to call upon their aid in a pinch, but she shouldn't count on help every time things go sour."
mf.source = "Demon Players Guide, p. 80"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Seasoned Traveler")[0]
mf.add_ratings([2, 4])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is adept at finding accommodation, supplies and local help wherever she goes in her home country. With the 4-pt. version, the same applies to foreign countries. She might not speak the language well, or at all, but she knows how to go about obtaining things and learning about the local culture without offending the natives, through a combination of prior research and general street smarts."
mf.source = "Demon Players Guide, p. 80"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Socially Aware")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Social interplay is an open book to your character. She's the first to spot the hidden relationships between people after only a few minutes of observation. Such subtle clues as body language and position, voice tone and choice of words speak volumes to her about the underlying connections between people. Gain two dice on any Perception roll involving interaction between other people."
mf.source = "Demon Players Guide, p. 80"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Trivia Champ")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Where does your character come up with this stuff? Whether it's through plenty of reading, too much TV or just an eclectic bunch of friends, she has the oddest collection of facts stored way in her skull. Once in a while, at the Storyteller's discretion, one of them turns out to be just the piece of information she needs. Your character might not actually be very bright, but the sheer amount of anecdotal knowledge she's picked up makes her appear to be."
mf.source = "Demon Players Guide, p. 80"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Upright Citizen")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Up until the moment of possession, your character's mortal host was a model citizen. Not even a whiff of scandal has ever tainted her. Her working life has been good without being extraordinary. Her friends would be hard-pressed to come up with any embarrassing secrets about her, and even her ex-lovers are complimentary about her most of the time. Your character just doesn't have any dirty secrets to come back to haunt her, and people who know her have a hard time believing anything bad about her."
mf.source = "Demon Players Guide, p. 80"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Vibrant Neighborhood")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character lives in a part of the city where everything goes, and does so most of the time. The streets are fairly busy late at night, and the inhabitants are up to all sorts of strange things. If anything odd happens, people tend to dismiss it as just another part of the local routine."
mf.source = "Demon Players Guide, p. 80"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Corporate Savvy")[0]
mf.add_ratings([3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal host has been a warrior of the cube battlefields for a long time and now your character knows how the corporate mind works. She understands the dynamics of money, business, information and power that make up companies, and she can manipulate them for her own ends to a limited degree. Add two dice to any roll involving manipulating a corporate structure or a corporate employee."
mf.source = "Demon Players Guide, p. 80"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Media Savvy")[0]
mf.add_ratings([3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "There's a knack to dealing with the media, and your character has it. She's learned what journalists want, and she does her best to provide it in a way that best suits her. She can create, suppress and redirect stories with a fair amount of effectiveness, just by the spin she puts on them. Most of the time, she tries to set up situations so the media reads them the way she wants. Add two dice to any Social rolls in which your character deals with journalists or reporters."
mf.source = "Demon Players Guide, p. 80-81"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Supportive Family")[0]
mf.add_ratings([3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Sure, your character's acting strange these days. There's something going on that she can't or won't tell them about, but it's important to her. That much is clear. They're her family, they love her, and they'll be there for her. They're sure she'll get around to telling them the whole truth sooner or later. Until then, they have no choice but to trust her. Unless you have also taken the Allies Background for your character, her family won't go out of the way to help her. They just don't ask the questions that she can't answer."
mf.source = "Demon Players Guide, p. 81"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Lucky")[0]
mf.add_ratings([4])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal host was normally a very lucky sort of person. Since she was a kid, things always worked out her way. Maybe she took a job with a small firm just before the business went through the roof, leading to her rapid promotion. Once per chapter (game session), the Storyteller may decrease the difficulty of a critical roll you make by two. If you succeed, it's because some random factor makes things easier for your character."
mf.source = "Demon Players Guide, p. 81"
mf.save()

# MENTAL MERITS - Cognitive abilities and mental characteristics

mf = MeritFlaw.objects.get_or_create(name="Common Sense")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has been gifted with practical, everyday wisdom that allows her to avoid making stupid, obvious mistakes. Whenever she's about to act in a way that's contrary to common sense, the Storyteller can make a suggestion as to the likely outcome of the action, possibly warning you off. Unlike Demon's Intuition Ability, this Merit doesn't allow you to make good guesses, nor does it offer you any particular insight. It just helps you avoid doing especially dumb things."
mf.source = "Demon Players Guide, p. 81"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Concentration")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is rather good at shutting distractions out and focusing on the task at hand. She's unaffected by disturbances — such as screaming kids, loud noises, hanging upside down or DJs playing really terrible music — when she focuses on a particular action."
mf.source = "Demon Players Guide, p. 81"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Good Map Reader")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is the Holy Grail of drivers everywhere: someone who can read a map well. Whether it's using an old map and a road atlas to locate an Earthbound's lair, or the New York subway plan and a street atlas, she can find her way to where she needs to be."
mf.source = "Demon Players Guide, p. 81"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Fast Reader")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character can read and understand a piece of writing far faster than most people can. While this Merit can make long train or plane journeys expensive propositions due to the number of books and magazines she goes through, it allows her to quickly extract useful information from anything written in her mortal host's native language."
mf.source = "Demon Players Guide, p. 82"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Good Recognition")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is great at remembering people's names and places she's been. She can call to mind the name of somebody she met briefly at a party three months ago, while a bit drunk, as clearly as if she met them only yesterday. She can also remember the streets she staggered down on the way home. She's even good at remembering the names of people mentioned in newspaper stories and TV reports, as well as locations glimpsed in photographs or on TV."
mf.source = "Demon Players Guide, p. 82"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Healthy Cynicism")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is good at separating truth from fiction, and someone has to be up pretty damn early to catch her off guard. She rarely takes what people say at face value until she's able to check the details herself. This Merit allows you to reduce the difficulty by two on any roll to perceive a lie. It should also be roleplayed as much as possible."
mf.source = "Demon Players Guide, p. 82"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Time Sense")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has an almost uncanny sense of time. She can estimate the amount of time that has passed, as well as the approximate time of day, without using a clock or any other means of measuring time."
mf.source = "Demon Players Guide, p. 82"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Code of Honor")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has a personal code of ethics to which she adheres strictly. This code might be related to her experiences in the war or something of a legacy from her mortal host. You should work out the details of your code with the Storyteller before play begins. You gain two additional dice to all Willpower rolls when accomplishing a major feat in accordance with that code."
mf.source = "Demon Players Guide, p. 82"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Determined")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is one tenacious bitch, determined to go her own way. It can be really difficult for people to persuade her otherwise. Gain two dice in any resisted roll in which someone tries to persuade her to do something. You might also have the Stubborn Flaw (see p. 82)."
mf.source = "Demon Players Guide, p. 82"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Eidetic Memory")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has a photographic memory. As a result, she can remember things she's seen, heard or read in perfect detail. Entire conversations, documents or pictures can be committed to memory with only minor concentration. Should she attempt the same feat under stressful conditions, such as trying to memorize a long list of names while three Earthbound thralls pound at the door, you must make a Perception + Alertness roll (difficulty 6) for her to summon enough concentration to finish the job (unless your character also has the Concentration Merit, which allows her to commit information to memory flawlessly)."
mf.source = "Demon Players Guide, p. 82"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Internet Savvy")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "The Internet is becoming increasingly common, but it is far from universal. Many users never progress beyond the basic email/simple surfing to \"sites whose address you know\" stage. Characters with this Merit are adept at using the Internet in all its vast, rambling confusion — no small feat for the technologically challenged fallen."
mf.source = "Demon Players Guide, p. 82"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Natural Linguist")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal host had a gift for other languages, reading and speaking them with the fluency of a native. When your character learns a language, reflected by increases in her Linguistics Ability, she learns it in more depth and with greater fluency than most do. You may add three dice to any roll involving writing, reading or speaking a language your character knows, barring her native tongue."
mf.source = "Demon Players Guide, p. 82"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Fast Learner")[0]
mf.add_ratings([3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character learns the basics of a subject very quickly indeed. She can cram simple information about virtually any subject into her head quickly and easily. It takes the normal time to develop a deeper knowledge, of course, but your character starts getting the hang of things very quickly. The cost to gain a new Ability is one experience point instead of three. The costs for higher levels are normal, however."
mf.source = "Demon Players Guide, p. 82"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Natural Aptitude")[0]
mf.add_ratings([3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has a particular Ability at which she excels. She's just a natural or has studied it so extensively that the Ability comes easily to her. You pay fewer than normal experience points to gain dots in the Ability, and each level is achieved as if it were one lower. The first point of the Ability costs only one experience point to gain if your character learns it after play begins. You also gain one extra die on any roll involving that Ability."
mf.source = "Demon Players Guide, p. 82"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Unflappable")[0]
mf.add_ratings([3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal host was a naturally placid person who took most things in stride. She was almost hit by a car? That was close. Her husband ran off with the kids? Ah, well. While she feels emotions like everyone else, she doesn't let them affect her the way others do. You gain two extra dice on any Willpower roll that involves staying clam or not overreacting to mundane experiences."
mf.source = "Demon Players Guide, p. 83"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Direction Sense")[0]
mf.add_ratings([4])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has an innate sense of where she is and the distance she's traveled. She can make a good guess at which way is north, even without clues like the position of the sun. She rarely gets lost and can estimate the distance between two points pretty well. She might even be able to navigate her way through London's one-way systems. Maybe."
mf.source = "Demon Players Guide, p. 83"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Optimistic")[0]
mf.add_ratings([4])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Despite everything that has happened to your character, she refuses to accept the fact that life cannot and will not ultimately change for the better. Regain two Willpower when you wake up each morning, rather than the usual one."
mf.source = "Demon Players Guide, p. 83"
mf.save()

# LEGAL MERITS - Special licenses and legal statuses

mf = MeritFlaw.objects.get_or_create(name="Drivers License")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's driving repertoire extends far beyond the SUV or sports car. She is qualified to drive trucks, farm vehicles or some other specialized form of vehicular transportation."
mf.source = "Demon Players Guide, p. 83"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Dual Nationality")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Thanks to being born from parents of different countries, your character's mortal host has dual nationality. She might even have two passports. This makes it easy for her to operate in two different places and even hide out in another country if things get too hot in her normal place of residence."
mf.source = "Demon Players Guide, p. 83"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Firearms License")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "The effect of this Merit depends on the country in which your game is set. In some countries (such as the UK) it indicates that your character is allowed to carry weapons. Without this Merit, possession of a firearm is illegal. In countries where individuals have a right to bear arms, it indicates that your character has a license to carry unusual or powerful firearms such as automatic weapons."
mf.source = "Demon Players Guide, p. 83"
mf.save()

# ECONOMIC MERITS - Wealth and financial advantages

mf = MeritFlaw.objects.get_or_create(name="Alimony Recipient")[0]
mf.add_ratings([1, 2, 3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's host's marriage has failed, but at least that cheating bastard has to pay for it. The level of Merit you buy indicates the number of Resources points your character can have (that must be purchased separately) for which she doesn't have to work. Her rating also suggests how wealthy her ex was or how badly he was beaten in court. Chances are she has the Children Flaw, too."
mf.source = "Demon Players Guide, p. 83"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Eye for a Bargain")[0]
mf.add_ratings([1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal host had a knack for getting things cheaply. Sometimes she gets the goods she needs in sales. Sometimes she gets them through wholesalers. Other times, she just hunts around until she finds a bargain. However she does it, the difficulty of any Resources roll you make decreases by two."
mf.source = "Demon Players Guide, p. 83"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Independent Income")[0]
mf.add_ratings([1, 2, 3, 4, 5])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Through hard work, heredity or phenomenal good fortune, your character's Resources rating is an independent income for which she doesn't have to work. The level of Merit you buy indicates how many dots of Resources (which must be purchased separately) your character has that do not require her to work."
mf.source = "Demon Players Guide, p. 83"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Good Credit Rating")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal host always paid off her debts on time and built up enough financial security to keep the most cynical banker happy. She can access a decent amount of credit as a result. Your character must have a Resources rating of 3 or more to purchase this Merit."
mf.source = "Demon Players Guide, p. 83"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Wealthy Partner")[0]
mf.add_ratings([2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's \"other half\" is pulling in a fortune, at least by her earning standards, and he's happy to be the breadwinner. With him covering the bills and living expenses, she can get away with a part-time job that allows her time to fulfill her obligations to allies, superiors at court and so on."
mf.source = "Demon Players Guide, p. 83"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Flexible Job")[0]
mf.add_ratings([3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's job allows her to work flexible hours or allows her to travel a lot. Or perhaps she's effectively her own boss, with no one monitoring her activities. However she does it, she can earn her Resources rating through a job that doesn't significantly restrict her infernal activities."
mf.source = "Demon Players Guide, p. 83"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Paid Mortgage")[0]
mf.add_ratings([3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's house is her own. She's paid off the bank, so mortgage repayments are no longer an issue, nor is repossession a threat. No matter what happens, she at least has a roof over her head."
mf.source = "Demon Players Guide, p. 83"
mf.save()

# ========== FLAWS ==========

# INFERNAL FLAWS - Specific to demons and their fallen nature

mf = MeritFlaw.objects.get_or_create(name="Ancient Animosity")[0]
mf.add_ratings([-1, -2, -3])
mf.allowed_types.add(demon)
mf.description = "Your character still holds to an ancient feud with another demon that dates from the War of Wrath. Even if the object of her animosity remains in the Abyss, he will make every attempt to even the score against her through allies and proxies. The amount of points spent on this Flaw indicates how far your character's foe is willing to go to strike back at her. One point indicates a minor or largely forgotten feud; the other demon will take steps to make your character's life difficult only when it is convenient for him to do so. Two points indicate that your character's enemy is actively working on plans to make your character's existence as difficult as possible, enlisting the aid of friends and allies to strike at her whenever the opportunity arises. Three points indicate that your character has gained an implacable foe that thinks of nothing else but your character's demise. He bends all of his energies and resources to make her life a living Hell."
mf.source = "Demon Players Guide, p. 84"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Cursed By God")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(demon)
mf.description = "Your character has been especially cursed by the Creator for actions taken during the War of Wrath. The strength and pervasiveness of the curse depends upon how many points you wish to gain. Examples: If your character passes on a secret she is entrusted with, her betrayal will come back to harm her in some way (1 pt.). Your character stutters uncontrollably when she tries to describe what she has seen or heard (2 pts.). Tools break or malfunction when your character tries to use them (3 pts.). Your character is doomed to make enemies of those whom she most loves or admire (4 pts.). Every one of your character's accomplishments or triumphs will eventually become soiled or fail in some way (5 pts.). Your character might or might not have a way to atone for her actions and free herself of this curse, at the Storyteller's discretion."
mf.source = "Demon Players Guide, p. 84"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="True Reflection")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.description = "It was once believed that mirrors reflected not one's physical appearance, but the true nature of one's soul. Your character's reflection reveals her actual celestial nature. When she looks in the mirror, she sees her apocalyptic form rather than her mortal guise. This reflection changes as her Torment increases or decreases. Mortals who see this reflected image are not subject to Revelation (see page 253 of the Demon core rules for details), but they will react with shock, amazement or alarm."
mf.source = "Demon Players Guide, p. 84"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Infamy")[0]
mf.add_ratings([-2])
mf.allowed_types.add(demon)
mf.description = "Your character's actions in the War of Wrath have earned her a degree of ill repute and hostility among her fellow demons. The difficulty of all Social rolls increases by one when your character is interacting with other fallen."
mf.source = "Demon Players Guide, p. 84"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Nightmares")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.description = "Your character's sleep is plagued by visions of the horrors she saw during the war. You must make a Willpower roll (difficulty 7) in order for the character to sleep through the night without being tormented. The day after, add two to the difficulty of the first Ability or Attribute roll you make to deal with other demons."
mf.source = "Demon Players Guide, p. 84"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="War Wound")[0]
mf.add_ratings([-2])
mf.allowed_types.add(demon)
mf.description = "Your character endured a terrible wound during the war that scarred the very essence of her being, manifesting itself even to this day when she reveals her Celestial nature. When your character adopts her apocalyptic form, she automatically suffers one health level of aggravated damage above and beyond any damage she currently suffers. This damage cannot be healed by any means."
mf.source = "Demon Players Guide, p. 84"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Cannot Enter Holy Ground")[0]
mf.add_ratings([-3])
mf.allowed_types.add(demon)
mf.description = "Your character's intense regret and guilt following her rebellion against God is so great that she cannot bear to enter holy ground or handle holy objects without suffering intense pain. No matter what her Torment level is, your character still suffers damage from holy ground and sanctified items such as crosses and holy water."
mf.source = "Demon Players Guide, p. 84"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Flashbacks")[0]
mf.add_ratings([-3])
mf.allowed_types.add(demon)
mf.description = "Like veterans of many mortal wars, the sights your character witnessed during the War of Wrath haunt her still, filling her dreams with visions of horror and destruction and occasionally overtaking her during moments of stress. When the character is under intense pressure or involved in combat, your character might experience powerful flashbacks of ancient battles. The Storyteller can call for a Willpower roll (difficulty 8) at appropriate moments. If the roll fails, the character thinks she's back in the war as she is caught up in a hallucinatory episode of incredible vividness and detail. As soon as the threat or source of stress is gone, you may begin making Willpower rolls (difficulty 7) for the character each turn to see if she can emerge from the visions of the past."
mf.source = "Demon Players Guide, p. 84-85"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Hunted")[0]
mf.add_ratings([-4])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.description = "Your character is pursued by a fanatical demon-hunter who believes (perhaps correctly) that she is a danger to humanity. Everyone with whom your character associates, be they mortal or fallen, might be hunted as well."
mf.source = "Demon Players Guide, p. 85"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Probationary Faction Member")[0]
mf.add_ratings([-4])
mf.allowed_types.add(demon)
mf.description = "Your character is a defector. She turned her back on her prior faction and still has much to prove before she is accepted by the demons to whom she has defected. Other demons who are members of her current faction treat her with distrust and even hostility, and her reputation might even sully those demons with whom she regularly associates."
mf.source = "Demon Players Guide, p. 85"
mf.save()

# PHYSICAL FLAWS - Part 1 (1-17) - Related to the mortal host's physical limitations

mf = MeritFlaw.objects.get_or_create(name="Allergies")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal body is allergic to a rather common substance such as cat hair that causes coughing, watery eyes and other distracting symptoms. The difficulty of all actions increases by one when exposed to whatever triggers her allergy."
mf.source = "Demon Players Guide, p. 85"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Arthritic")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's joints, especially her hands, are tender and often swollen. When she attempts anything that requires fine and careful touch, such as sewing or repairing a watch, increase the difficulty of your roll by one."
mf.source = "Demon Players Guide, p. 85"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Color Blind")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has trouble distinguishing between hues. You must make a Perception roll (difficulty 6) for your character to accurately determine the color of a given object."
mf.source = "Demon Players Guide, p. 85"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Distinguishing Characteristic")[0]
mf.add_ratings([-1, -2])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal body has a physical feature that makes her very easy to pick out in crowds, such as elaborate tattoos, a scar or an obvious birthmark. This Flaw is worth one point if the characteristic is hidden easily under clothes, two points if it is not."
mf.source = "Demon Players Guide, p. 85"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Heavy Sleeper")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character tends to sleep right through most disturbances, from the loud stereo playing next door to the exorcists laying a binding sigil around her bed. You must make a successful Willpower roll (difficulty 6) for the character to wake up quickly. Failure means she spends the equivalent of a combat turn waking up. A botch means she sleeps right through the disturbance, pending the Storyteller's judgment on the situation."
mf.source = "Demon Players Guide, p. 86"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Lazy")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has trouble motivating herself to do anything. She'd rather sit around the house watching TV and thinking of doing something with her life than actually getting up and doing it. She tends to complain loudly when there's work to do, and she likes to let things slide until the last possible moment. You must make a Willpower roll (difficulty 6) to take care of any routine tasks not directly related to your character's demonic activities, such as paying the electricity bill or getting the car's tires rotated."
mf.source = "Demon Players Guide, p. 86"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Low Alcohol Tolerance")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Alcohol goes straight to your character's head. While this can be an advantage when she tries to enjoy a night out on the cheap, it can be deadly when hunted by exorcists or worse. Double any penalties your character suffers for consuming alcohol."
mf.source = "Demon Players Guide, p. 86"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Medicated")[0]
mf.add_ratings([-1, -5])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal body requires daily medication to stay in good health. As a one-point flaw, her medication is important for her long-term health but has little effect on her day-to-day well being, as with prescription drugs that keep your cholesterol down. The five-point version represents insulin shots or something else that is necessary to keep your character alive. If she should miss a day's worth of medicine, she automatically suffers a bashing or lethal level of damage for every 12 hours that pass without her medicine, as determined by the Storyteller. This damage heals at a rate of one level per 12 hours that pass once you resume your regular medication schedule. Time spent in apocalyptic form is not counted toward the total time without medication."
mf.source = "Demon Players Guide, p. 86"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Motion Sickness")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character becomes queasy and nauseated on boats, when traveling long distances by car or on amusement-park rides. Increase the difficulty by two on all actions your character takes when dealing with these conditions."
mf.source = "Demon Players Guide, p. 86"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="No Sense of Smell")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character has no sense of smell. Her mortal host might have simply been born without it, or she lost it due to some freak accident. She can't smell anything, no matter how strong the odor is. Food tastes somewhat bland to her. On the good side, she isn't bothered by the stench of sewers, rotting flesh or other nastiness."
mf.source = "Demon Players Guide, p. 86"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="No Sense of Taste")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's taste buds simply do not function. She cannot appreciate a fine meal, and she has trouble gauging the difference between good and bad food and drink."
mf.source = "Demon Players Guide, p. 86"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Non-Swimmer")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character never learned how to swim, and she has no natural talent for it. If she ever finds herself in a position where she has to try to swim, she can manage a pitiable doggie paddle. Increase the difficulty by two for any Athletics rolls involving swimming."
mf.source = "Demon Players Guide, p. 86"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Poor Eyesight")[0]
mf.add_ratings([-1, -3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal host is either severely nearsighted or farsighted. Increase the difficulty by two for any rolls that involve visual acuity. The one-point version is correctable with glasses or contact lenses. The three-point version is not."
mf.source = "Demon Players Guide, p. 86"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Poor Hearing")[0]
mf.add_ratings([-1, -3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's hearing is exceptionally bad. Increase the difficulty by two on any roll involving hearing. This Flaw is worth one point if it is correctable with a hearing aid or similar device, three points if it is not."
mf.source = "Demon Players Guide, p. 86"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Sickly")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is constantly coughing and wheezing, and she has trouble shaking colds. Her mortal host suffered almost every childhood illness imaginable, and she's only become worse as an adult. When checking to avoid catching a disease or developing an infection, increase the difficulty of the roll by two."
mf.source = "Demon Players Guide, p. 86"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Vice")[0]
mf.add_ratings([-1, -2, -3])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character is addicted to some sort of substance. The one-point version of this Flaw represents an addiction to a substance that is legal and easy to satisfy, such as cigarettes. The two-point version represents a legal or mildly illegal substance that inhibits her abilities to a serious degree, such as alcohol or marijuana. The three-point version represents an addiction to a highly illegal or highly dangerous \"hard\" drug such as heroin. Your character is always under the effects of your chosen vice unless she assumes her apocalyptic form."
mf.source = "Demon Players Guide, p. 86"
mf.save()

mf = MeritFlaw.objects.get_or_create(name="Youthful Appearance")[0]
mf.add_ratings([-1])
mf.allowed_types.add(demon)
mf.allowed_types.add(thrall)
mf.allowed_types.add(dtfhuman)
mf.description = "Your character's mortal host looks like she did in high school. She always gets carded at bars and often has to produce identification to buy even cigarettes. In order to gain entry to clubs, concerts and bars, or to purchase alcohol, your character needs to present a valid-looking ID."
mf.source = "Demon Players Guide, p. 86-87"
mf.save()

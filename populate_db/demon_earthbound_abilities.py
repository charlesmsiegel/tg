"""
Populate database with Earthbound Abilities from Demon: Earthbound Chapter 3.

These Abilities are available for Earthbound characters, with some restricted
to Earthbound only (like Recall).
"""

from characters.models.core.ability_block import Ability

# Indoctrination (Skill)
indoctrination = Ability.objects.get_or_create(
    name="Indoctrination", property_name="indoctrination"
)[0]
indoctrination.description = """This Skill represents the capability to change the heartfelt convictions and attitudes of others through brainwashing and psychological conditioning. More than simply lying or persuading another, Indoctrination allows the practitioner to permanently alter another person's personality, loyalty and beliefs. The Skill involves knowledge of effective psychological techniques, as well as familiarity with the medications, drugs and equipment useful to the brainwashing process.

Using this Skill on a subject requires an extended roll. The player must gain more successes than the subject's Willpower score to successfully indoctrinate her with a new set of beliefs. The frequency of the Indoctrination rolls depends on the circumstances. If the indoctrinator can isolate the subject from outside influences and work on her 24 hours a day, the Storyteller may allow a roll once per day. If the indoctrinator is forced to take a more subtle approach and can work on her subject for only an hour or so per day, the Storyteller may allow an Indoctrination roll only once per week.

The difficulty of the roll depends on how isolated the subject is from outside influences that could reinforce her normal beliefs. Complete isolation (the subject is locked in a cell) would present a difficulty of 6. Partial isolation (the subject is removed from her normal surroundings and subjected to a culture sympathetic to the indoctrinator) would present a difficulty of 7. Limited isolation (the indoctrinator can only isolate the subject for brief periods of time) would present a difficulty of 8 or higher. Willpower points can be spent to gain automatic successes on this roll.

Once a subject has been successfully indoctrinated, her beliefs will remain altered until she can be de-programmed - using the Indoctrination process again to restore her prior beliefs.

• Novice: You can sometimes encourage others to fall in with the party line.
•• Practiced: You usually have no problem convincing others to accept your version of "truth."
••• Competent: You can turn friend against friend, husband against wife, or brother against brother with enough time.
•••• Expert: You can easily mold others' emotions, ideas and faith into whatever form you desire.
••••• Master: What label do you prefer - Big Brother or God?

Possessed by: Cult Leaders, Deprogrammers, Earthbound, Generals, Psychological Warfare Experts, Psychologists
Specialties: Chemical Aids, Harsh Methods, Hate, Love, Worship"""
indoctrination.save()

# Recall (Talent) - Earthbound only
recall = Ability.objects.get_or_create(name="Recall", property_name="recall")[0]
recall.description = """This Talent is available only to the Earthbound who escaped to Earth before the breaking of the Abyss; recently Earthbound demons may not possess it.

Ancient Earthbound do not suffer from the same clouding of memory that other demons have, so their memories of the Fall and the Age of Wrath are detailed and full. What's more problematic, though, is remembering the details of the Earthbound's time in Creation after being summoned from Hell. The Earthbound do not perceive time the same way mortals do, they occasionally ignore meaningless events like wars and the rise of civilization, and they spend time in dreaming stasis when they run low on Faith. Therefore, the memory of an Earthbound can be patchy - not hazy like that of a normal demon, but simply unfocused.

The Recall Talent measures how extensive and focused the Earthbound's memories are on a particular subject or topic relating to mortal history. Roll Intelligence or Wits (Storyteller's choice) + Recall against a difficulty of 6. Remembering simple facts requires only one success; obscure details or hidden secrets require more. Once it's determined that the Earthbound does know about a specific fact, the player doesn't need to make further Recall rolls to revisit the topic.

It's important to note that Recall is not the same as the Legacy Background. Legacy measures how well a demon remembers the Time of Babel, the Time of Atrocities and other periods leading up to its imprisonment in Hell. The Earthbound remember this time clearly. Their memories are not clouded by the limitations of a mortal host's brain, so they have no need of the Legacy Background. Recall, on the other hand, measures the character's memories and experiences of life and mortal society after it was summoned from Hell.

• Novice: The lives of insects mean nothing to you, so you paid little attention to the events of the mortal world.
•• Practiced: You possess sound recollection of human history - at least for those periods you found interesting.
••• Competent: You kept a careful eye on mortal society throughout your existence, wary for signs of rivals and enemies.
•••• Expert: Human history is an open book to you, and few details have ever slipped your memory or evaded your notice.
••••• Master: No detail has ever escaped your unblinking eye. No fact has ever fled your memory. No secret has ever been hidden from your sight.

Possessed by: Earthbound
Specialties: Cults, Empires, Lost Cities, Rivals, Wars"""
recall.save()

# Tactics (Skill)
tactics = Ability.objects.get_or_create(name="Tactics", property_name="tactics")[0]
tactics.description = """The Earthbound have witnessed countless wars and millennia of conflict, and they have learned the secrets of battle. Tactics is a Skill measuring the character's grasp of military strategy and the best way to fight a battle, regardless of the odds. A skilled tactician can hold back an army with a dozen soldiers or pierce a stronghold's defenses with perfectly timed attacks. Tactics is useless for a lone warrior, though, who survives only through raw skill and power. Tactics is based on leadership and teamwork, and it requires the character to command a group of warriors or followers.

Successful Intelligence or Wits + Tactics rolls allow the player to ask the Storyteller questions about the forces opposing her followers before the battle begins. Each success yields a piece of information that the player can use to form battle plans. Alternatively, the Storyteller might award the player a pool of automatic successes equal to the successes of the Tactics roll. These successes can be applied to any roll or rolls made in the ensuing battle, representing the planning and teamwork employed by the Earthbound's forces. Once used, these automatic successes are lost. Only one Tactics roll may be made per scene.

• Novice: "Be careful out there, okay."
•• Practiced: "Protect your flank, and watch out for automatic fire."
••• Competent: "Jackson, you take point. Henderson, you're on overwatch, and remember to stick to controlled bursts."
•••• Expert: "There's a high chance that their commander will call for a pincer movement - in which case, you need to..."
••••• Master: "Execute maneuver #46 after precisely 127 seconds have elapsed, which will remove their tertiary fire support..."

Possessed by: Earthbound, Generals, Mercenaries, Military Historians, Soldiers
Specialties: Defense, First Strikes, Offense, Teamwork, Weapons"""
tactics.save()

# Torture (Skill)
torture = Ability.objects.get_or_create(name="Torture", property_name="torture")[0]
torture.description = """Torture is a dark and hideous Skill, made all the more insidious because the Earthbound learned it from their mortal followers. It took a mortal to invent murder, and it took a mortal to invent the notion of hurting someone until that someone cooperates. Torture allows the character to wrest information from an unwilling victim, usually through physical means - beatings, red-hot pokers, drops of water falling constantly on the victim's skull. Psychological torture can also be effective, using methods such as sensory deprivation, sleep deprivation and constant questioning that leaves the victim on the edge of madness.

Torturing a victim requires an extended, resisted roll. Roll Manipulation + Torture versus the victim's Willpower - the difficulty for both rolls is 7. If the Torture roll wins, the victim suffers one health level of lethal damage (for physical torture) or loses one point of temporary Willpower (for psychological torture). Once the torturer accumulates successes equal to the victim's permanent Willpower, the victim breaks and tells the torturer what she wants. If the victim's resistance roll botches, the character loses a point of permanent Willpower; if the Torture roll botches, the victim resists all further attempts at interrogation. Note that the victim can cease resistance at any time to spare further damage or loss of Willpower and confess what she knows.

• Novice: You're prepared to beat an answer out of someone.
•• Practiced: With the right tools and a few weeks, you can coax answers out of most people.
••• Competent: You mix a strong grasp of psychology with an inhuman gift for causing pain, and you can apply these skills to the strongest spy.
•••• Expert: You could break saints and martyrs into screaming pieces, given enough time.
••••• Master: Nothing that lives can withstand your clinical, brutal interrogation.

Possessed by: Black Ops Agents, Earthbound, "Military Advisors," Serial Killers
Specialties: Improvised, Physical, Psychological, Rapid, Resisting Torture"""
torture.save()

print("Earthbound Abilities created successfully!")

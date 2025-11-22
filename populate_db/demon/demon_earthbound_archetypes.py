"""
Populate database with Earthbound Archetypes from Demon: Earthbound Chapter 3.

These extreme Archetypes are available for all Earthbound characters.
Normal Demon characters can also have these Archetypes, but indulging them
can lead to corruption, rage and rapid accumulation of Torment.
"""

from characters.models.core.archetype import Archetype

# Destroyer
destroyer = Archetype.objects.get_or_create(
    name="Destroyer",
    description="The mere existence of this world is an affront, a mocking gesture from a Creator who thinks Himself your superior. Well, if God loves His creation so much, let's see what He thinks when you burn it to ashes. Nothing pleases your twisted soul as much as the mindless act of destruction - except for the deliberate destruction of something precious to another being. Seeing the loss in the soul of another makes the carnage you wreak that much more exquisite. You regain Willpower when you completely destroy a precious or useful thing, be it a priceless artifact or a loving relationship.",
)[0]
destroyer.add_source("Demon: Earthbound", 71)

# Enslaver
enslaver = Archetype.objects.get_or_create(
    name="Enslaver",
    description="Other beings are no more than illusions, puppets that exist solely to dance to your whim. If they resist your commands, it just makes their eventual enslavement all the sweeter. Seeing the dying flicker of free will and rebellion in the eyes of another is the closest you come to joy. You surround yourself with mortal servitors, but even demons and other supernatural beings will submit to your will soon enough. You regain Willpower when you subvert another's will to your own.",
)[0]
enslaver.add_source("Demon: Earthbound", 72)

# Sadist
sadist = Archetype.objects.get_or_create(
    name="Sadist",
    description="The screams of the damned and the dying is the sweetest music your tormented soul can imagine. To inflict pain on others, and to see them writhe in agony, is all you live for, all that makes your corrupted existence meaningful. You kill without a second thought if necessary, but you prefer to let your victims live so that they can heal - then you can hurt them all over again. You regain Willpower whenever you deliberately cause great pain to another being - be it physical or spiritual, mental or emotional.",
)[0]
sadist.add_source("Demon: Earthbound", 72)

# Tyrant
tyrant = Archetype.objects.get_or_create(
    name="Tyrant",
    description="There are fools in this world who oppose your will, and they must be destroyed. All that matters to you is the unstoppable advance of your plans and the dominance of your will. Other beings exist only to serve you without question or to act as obstacles - and all obstacles must be crushed without mercy. Your word is Law. All shall obey. You regain Willpower whenever you destroy an obstacle to your will.",
)[0]
tyrant.add_source("Demon: Earthbound", 72)

# Vivisectionist
vivisectionist = Archetype.objects.get_or_create(
    name="Vivisectionist",
    description="Nothing in this world is as important as knowledge and the gathering of information - certainly not the lives of others or the foolishness of morality and ethics. How can you know the intricacies of the human nervous system if you don't flay open an experimental subject and tinker with her muscles? How can you learn the limits of human Faith without pushing a human past those limits - and recording the way in which he died? Experiments require subjects, and if those subjects suffer for your knowledge, that's not so inconvenient. You regain Willpower whenever your twisted experiments grant you new and meaningful information.",
)[0]
vivisectionist.add_source("Demon: Earthbound", 72)


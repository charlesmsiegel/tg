"""
Populate database with Earthbound Rituals from Demon: Earthbound Chapter 4.

Earthbound rituals are ancient and powerful, focused on subtly affecting the minds
of potential worshippers, causing chaos and terror, and protecting the Earthbound.
Unlike normal demon rituals, Earthbound rituals do not have low-Torment effects.
"""

from characters.models.demon.ritual import Ritual
from populate_db.demon.demon_earthbound_lores import lore_of_chaos as lore_chaos
from populate_db.demon.demon_earthbound_lores import (
    lore_of_contamination as lore_contamination,
)
from populate_db.demon.demon_earthbound_lores import lore_of_violation as lore_violation
from populate_db.demon.demon_lores import lore_of_awakening as lore_awakening
from populate_db.demon.demon_lores import lore_of_flame, lore_of_humanity
from populate_db.demon.demon_lores import lore_of_patterns as lore_patterns
from populate_db.demon.demon_lores import lore_of_the_beast as lore_beast
from populate_db.demon.demon_lores import lore_of_the_celestials as lore_celestials
from populate_db.demon.demon_lores import lore_of_the_firmament as lore_firmament
from populate_db.demon.demon_lores import lore_of_the_flesh as lore_flesh
from populate_db.demon.demon_lores import lore_of_the_forge as lore_forge
from populate_db.demon.demon_lores import lore_of_the_spirit as lore_spirit

# ============================================================================
# EARTHBOUND RITUALS
# ============================================================================

# Undying Fire
undying_fire = Ritual.objects.get_or_create(
    name="Undying Fire",
    house=None,  # Earthbound ritual, not house-specific
)[0]
undying_fire.primary_lore = lore_flesh
undying_fire.primary_lore_rating = 4
undying_fire.secondary_lore_requirements = [
    {"lore_id": lore_of_flame.id, "rating": 2},
]
undying_fire.base_cost = 12
undying_fire.minimum_casting_time = 36
undying_fire.restrictions = (
    "The ritual must be cast in sunlight, and the target must be within sight of the Ankida."
)
undying_fire.system = """Roll Stamina + Survival. The target suffers dice pool penalties as if he had taken a number of health levels of damage equal to the successes rolled. A Willpower point may be spent per health level of penalty to ignore its effects for the duration of a single turn. The target does not take any physical damage from the flames.

The flames are not just illusory, however - the target really is on fire. Any inflammable articles on the target's body will catch fire as well. This may cause damage to the target if he is carrying ammunition, aerosol cans or the like.

The effects of this ritual last for the duration of a scene. Once its effects expire, make a Willpower roll for the victim against a difficulty of 8. If the roll fails, the victim loses a point of permanent Willpower. If the roll botches, the target also gains a temporary derangement."""
undying_fire.torment_effect = "Earthbound rituals do not have low-Torment effects. Fallen participants automatically gain a temporary point of Torment."
undying_fire.variations = ""
undying_fire.flavor_text = "Originally developed from the Devils' ritual Resist Fire as a tool for punishment, this ritual sets the victim on fire, inflicting hideous agony without the release of unconsciousness or death."
undying_fire.source_page = "Earthbound 113-114"
undying_fire.save()

# Unholy Geas
unholy_geas = Ritual.objects.get_or_create(
    name="Unholy Geas",
    house=None,
)[0]
unholy_geas.primary_lore = lore_violation
unholy_geas.primary_lore_rating = 4
unholy_geas.secondary_lore_requirements = [
    {"lore_id": lore_celestials.id, "rating": 2},
]
unholy_geas.base_cost = 12
unholy_geas.minimum_casting_time = 36
unholy_geas.restrictions = "The sigil must be drawn in human blood and bile, and the Ankida must know the name of the mortal she wishes to affect. The victim does not have to be present at the ritual site to be affected. The Ankida can affect a victim up to a number of miles away equal to her Faith score."
unholy_geas.system = """Roll Manipulation + Leadership; the target resists with a Willpower roll (difficulty 8). If the Earthbound succeeds, the geas takes effect. The target also suffers one level of bashing damage for every extra success the Earthbound gets, as the mortal's mind is crushed beneath the weight of the Dread King's will.

The geas can be a number of discrete commands equal to the unresisted successes gained by the ritual effect roll. A valid command can be communicated in a single, simple sentence. (Rob a bank. Kill your husband. Go to 1251 Main Street.) The more unresisted successes the roll garners, the more complex the instruction set can be. If the ritual effect roll generated three unresisted successes, a valid set of commands might read as follows: Rob a bank, take the money to 1251 Main Street, and leave the money in the mailbox.

The victim may attempt to resist the geas each day with a successful Willpower roll (difficulty 9), or by spending a Willpower point. If successful, the victim can resist the geas for the rest of the day. Otherwise the victim will attempt to fulfill the geas to the best of her capability and regardless of the risk to herself or others.

The ritual's compulsion lasts for a number of days equal to the Ankida's Willpower. If the mortal fulfills the compulsion or performs the task demanded of him before this time, the effects cease. When the ritual's monstrous sendings end, make a Willpower roll (difficulty 8) for the victim. If the roll fails, the mortal gains a temporary derangement. If the roll botches, the derangement becomes permanent. A mortal can be subject to only one geas at any given time."""
unholy_geas.torment_effect = "Earthbound rituals do not have low-Torment effects. Fallen participants automatically gain a temporary point of Torment."
unholy_geas.variations = ""
unholy_geas.flavor_text = "This ritual inflicts a long-lasting and irresistible compulsion to obey the will of the Earthbound. The geas manifests as whispered voices, hallucinations and near-uncontrollable urges to follow commands."
unholy_geas.source_page = "Earthbound 114-115"
unholy_geas.save()

# Song of Sinuous Questioning
song_of_sinuous_questioning = Ritual.objects.get_or_create(
    name="Song of Sinuous Questioning",
    house=None,
)[0]
song_of_sinuous_questioning.primary_lore = lore_spirit
song_of_sinuous_questioning.primary_lore_rating = 5
song_of_sinuous_questioning.secondary_lore_requirements = [
    {"lore_id": lore_violation.id, "rating": 2},
]
song_of_sinuous_questioning.base_cost = 14
song_of_sinuous_questioning.minimum_casting_time = 49
song_of_sinuous_questioning.restrictions = "The demon must be within the ritual sigil, and the Ankida must know the demon's Celestial or True Name."
song_of_sinuous_questioning.system = """The Song of Sinuous Questioning was first developed by the Earthbound Agashunakzar for use against other, weaker Earthbound, but it can be employed against the fallen as well. The ritual requires a Manipulation + Awareness roll resisted by the target's Willpower.

The number of unresisted successes determines how much information the Earthbound gleans from the target. One success allows trivial acquaintance with the subject's mind - superficial recollections of the target's thoughts and recent history. Three successes grant access to deeper memories and information about the demon's supernatural abilities - particularly lore paths and rituals. Five successes allow an Earthbound to rummage through every compartment of the demon's mind, perhaps even accessing memories the fallen no longer remembers (including those of times before the banishment to the Abyss).

If the ritual does not reveal enough information for the Earthbound's satisfaction, it can be repeated. It is less efficacious each time, however, and each repetition against the same demon after the first casting increases the difficulty of the Manipulation + Awareness roll by one."""
song_of_sinuous_questioning.torment_effect = "Earthbound rituals do not have low-Torment effects. Fallen participants automatically gain a temporary point of Torment."
song_of_sinuous_questioning.variations = ""
song_of_sinuous_questioning.flavor_text = "This ritual uses seduction and corruption to overcome the will of trapped demons, forcing the truth from them. It paralyzes the demon's spirit rather than its physical form."
song_of_sinuous_questioning.source_page = "Earthbound 115"
song_of_sinuous_questioning.save()

# Soul Cascade
soul_cascade = Ritual.objects.get_or_create(
    name="Soul Cascade",
    house=None,
)[0]
soul_cascade.primary_lore = lore_forge
soul_cascade.primary_lore_rating = 5
soul_cascade.secondary_lore_requirements = [
    {"lore_id": lore_patterns.id, "rating": 3},
]
soul_cascade.base_cost = 16
soul_cascade.minimum_casting_time = 64
soul_cascade.restrictions = "The sigil must surround the intended backup reliquary and must be performed on a night with no moon."
soul_cascade.system = """This ritual provides an emergency escape route for an Earthbound demon should its existing resting-place be destroyed. The reliquary-to-be can be prepared for only one Earthbound; other demons gain no benefit from inhabiting it. The ritual is performed when the spare reliquary is prepared, while the Earthbound is still safely ensconced in her original idol. The effects of the ritual last for a number of months equal to the Ankida's Faith score before it must be renewed to maintain the link to the Earthbound. Each Earthbound may have only one such backup reliquary.

Roll Intelligence + Occult against a difficulty equal to the Earthbound's Willpower. If it succeeds, a channel is opened from the Earthbound to the backup reliquary. This channel can be detected like other manifestations of demonic powers, but the difficulty to detect it is 9.

If the ritual is successful and the Earthbound's existing reliquary is destroyed while the ritual is still in effect, the demon becomes subject to the same system for discarnate demons detailed on p. 259 of the Demon core rulebook. The channel to the new reliquary anchors her to this world somewhat. The difficulty of the Willpower roll to avoid being dragged back into the Abyss decreases by one as a result.

The new reliquary item automatically counts as attuned for a disembodied soul, so the Willpower roll to inhabit it is made against a difficulty of only 6. The link from the Earthbound also eases the trauma of discorporation somewhat, so the demon does not lose the point of Faith rating she otherwise would. These effects apply only to the Earthbound demon for which it has been prepared. Other demons attempting to inhabit it find the difficulty increased by one, as the Earthbound's lingering resonance is an obstacle to successful possession.

Before it is inhabited, however, the potential reliquary can make the Earthbound somewhat vulnerable. The relic is linked with its essential nature, and it resonates with this link. Should it fall into the hands of the demon's enemies, they might be able to glean some or all of the Earthbound's True Name from it over time (Demon, p. 256). Therefore, most Earthbound guard such items jealously, if they ever create them at all."""
soul_cascade.torment_effect = "Earthbound rituals do not have low-Torment effects. Fallen participants automatically gain a temporary point of Torment."
soul_cascade.variations = ""
soul_cascade.flavor_text = "This ritual creates a backup reliquary that serves as an emergency vessel should the Earthbound's primary reliquary be destroyed."
soul_cascade.source_page = "Earthbound 115-116"
soul_cascade.save()

# Plague Tide
plague_tide = Ritual.objects.get_or_create(
    name="Plague Tide",
    house=None,
)[0]
plague_tide.primary_lore = lore_beast
plague_tide.primary_lore_rating = 3
plague_tide.secondary_lore_requirements = [
    {"lore_id": lore_awakening.id, "rating": 2},
    {"lore_id": lore_contamination.id, "rating": 2},
]
plague_tide.base_cost = 21
plague_tide.minimum_casting_time = 49
plague_tide.restrictions = "The creatures to be affected must all be gathered within the sigil."
plague_tide.system = """Roll Manipulation + Animal Ken. This ritual allows the Earthbound to possess and control a number of animals, equal to 10 times the number of successes rolled, although it works only on animals the size of a cat or smaller. The Earthbound often use rats, mice, bats, snakes, crows, eels and insects as their instruments of contagion. The possession lasts for a number of hours equal to the Ankida's Faith score.

For more information on animal swarms and their capabilities, please see page 72 of the Demon Storytellers Companion.

The horde of creatures spreads disease throughout human communities. In addition to the usual damage from a creature of that type, a bite or claw from an infected animal inflicts a wasting disease on its victims. Make a Stamina roll each time a victim suffers a health level of damage from a member of the swarm. If the roll fails, the victim suffers an additional level of unsoakable bashing damage and becomes infected by the disease.

Every day thereafter, the victim suffers an additional level of bashing damage and loses one temporary Willpower point until the disease has run its course. The sickness afflicts sufferers for a number of days equal to the Earthbound's Faith score, and it cannot be cured with medical attention. If another demon attempts to cure the disease with the Lore of Awakening, the evocation roll becomes a resisted roll versus the Ankida's Willpower. If the fallen loses the contest, the victim cannot be cured."""
plague_tide.torment_effect = "Earthbound rituals do not have low-Torment effects. Fallen participants automatically gain a temporary point of Torment."
plague_tide.variations = ""
plague_tide.flavor_text = "Previous uses of this ritual have been responsible for awful contagions and plagues throughout history. The Earthbound commands hordes of vile beasts to spread disease and misery."
plague_tide.source_page = "Earthbound 116"
plague_tide.save()

# Networking
networking = Ritual.objects.get_or_create(
    name="Networking",
    house=None,
)[0]
networking.primary_lore = lore_firmament
networking.primary_lore_rating = 4
networking.secondary_lore_requirements = [
    {"lore_id": lore_of_humanity.id, "rating": 3},
    {"lore_id": lore_forge.id, "rating": 3},
]
networking.base_cost = 30
networking.minimum_casting_time = 100
networking.restrictions = "The ritual must be cast during the hours of darkness, and it requires a computer connected to the Internet to be placed within the sigil. This computer must remain there as long as the ritual effect continues."
networking.system = """Roll Manipulation + Technology. The ritual allows the demon to interact with the Internet as if it were sitting at a computer using it directly. Messages sent to the demon require a Perception + Technology check to notice them, unless he's paying attention to the Internet at the time.

To affect other Internet users with the online persona, roll Manipulation + Empathy - targets may resist with Willpower (difficulty 7). The demon can affect a number of individuals equal to the successes rolled for the ritual effect. If the targets fail their Willpower roll - or choose not to resist, whether knowingly or not - they trust the demon and will talk honestly with him. The difficulty of all future Manipulation-based rolls against an affected target decreases by one.

Though seemingly benign, this ritual allows an Earthbound to interact with and influence mortals on an even broader scope than would be possible using only its thralls and infernal servants. Used imaginatively, it can provide the demon with useful information or sow discord and chaos. Innocent victims can be lured from the safety of their homes and into the arms of waiting cultists, or vulnerable mortals can be indoctrinated to the worship of the demon over a period of time.

The effects of the ritual last for a number of weeks equal to the Ankida's Faith score."""
networking.torment_effect = "Earthbound rituals do not have low-Torment effects. Fallen participants automatically gain a temporary point of Torment."
networking.variations = ""
networking.flavor_text = "This newly developed ritual creates an Internet presence for the demon, an online persona who is witty, charming and interesting, preying upon the honesty and trust of naïve souls."
networking.source_page = "Earthbound 116"
networking.save()

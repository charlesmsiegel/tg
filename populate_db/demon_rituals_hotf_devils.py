"""
Populate database with Devil (Namaru) rituals from Houses of the Fallen.
"""

from characters.models.demon.ritual import Ritual

from populate_db.demon_houses import devils
from populate_db.demon_lores import (
    lore_of_the_celestials as lore_celestials,
    lore_of_flame as lore_flame,
    lore_of_the_firmament as lore_firmament,
    lore_of_humanity,
    lore_of_light,
    lore_of_longing,
    lore_of_radiance,
    lore_of_the_realms as lore_realms,
    lore_of_the_fundament as lore_fundament,
)

# =============================================================================
# DEVIL RITUALS - HOUSES OF THE FALLEN
# =============================================================================

dawns_light = Ritual.objects.get_or_create(
    name="Dawn's Light",
    house=devils,
)[0]
dawns_light.primary_lore = lore_celestials
dawns_light.primary_lore_rating = 3
dawns_light.secondary_lore_requirements = [
    {"lore_id": lore_humanity.id, "rating": 2},
    {"lore_id": lore_light.id, "rating": 1},
]
dawns_light.base_cost = 18
dawns_light.minimum_casting_time = 36
dawns_light.restrictions = "The ritual must be performed at night."
dawns_light.system = """Roll Charisma + Leadership. For a number of minutes equal to the successes rolled, the surrounding area is filled by bright (but not blinding) sunlight, for a radius in miles equal to the Ankida's permanent Faith. The sunlight radiates from the ritual's sigil, but the sigil does not become overly bright. The light casts shadows away from the sigil, but permeates the whole area so that almost all locations within the radius of effect are illuminated as if it were the first few minutes of dawn.

Both mortals and demons within the ritual's radius of effect may be revitalized and inspired by the dawn's light, which is both physically and spiritually illuminating. All mortals within the area regain a point of temporary Willpower, if they had less than their normal maximum number of points. They also heal a level of bashing damage if they were injured.

Make a Faith roll for every demon within the area of effect against a difficulty equal to their permanent Torment ratings. For every success, they regain a point of Willpower (up to their maximum rating). If the roll fails the demon is too wracked with anguish and hate to gain determination from the kiss of morning. If the roll botches, the demon gains a permanent point of Torment.

The light created by this ritual is true sunlight, with all the spiritual and physical properties of the sun. Any creatures affected by sunlight in some way, such as vampires or other supernatural creatures, will be fully affected by the dawn light created by the ritual, for as long as the sigil shines or until they find shelter."""
dawns_light.torment_effect = """The high-Torment version of this ritual creates a dark, brooding light the color of rust, like the glow of a dying star. Mortals touched by this corrupt glow are plagued by despair, madness and nightmares, and they lose a point of temporary Willpower. Mortal thralls may try to resist this effect with a successful Willpower roll (difficulty 8).

Any demons in the area of effect can draw strength from the bloody light, but only if they give in to their inner darkness. Make a Torment roll, with a difficulty equal to the demon's permanent Faith. For each success, the character regains a point of temporary Willpower and a point of temporary Torment."""
dawns_light.variations = "None"
dawns_light.flavor_text = "The Heralds were light itself in the first days of Creation, as well as being the stars that shone in the sky. Most importantly, the Heralds governed the sun, and brought the divine spark of the Creator to humanity when morning first broke across Creation and stirred Adam and Eve from sleep. With this ritual, the Namaru can re-create that first dawn in the middle of the night."
dawns_light.source_page = "Houses of the Fallen, p. 29"
dawns_light.save()

ghostly_inferno = Ritual.objects.get_or_create(
    name="Ghostly Inferno",
    house=devils,
)[0]
ghostly_inferno.primary_lore = lore_flame
ghostly_inferno.primary_lore_rating = 3
ghostly_inferno.secondary_lore_requirements = [
    {"lore_id": lore_realms.id, "rating": 2},
]
ghostly_inferno.base_cost = 10
ghostly_inferno.minimum_casting_time = 25
ghostly_inferno.restrictions = "The ritual requires that a burnt offering of flesh be placed in the center of the sigil."
ghostly_inferno.system = """Roll Manipulation + Survival. The flames fill an area in the spirit world with a radius equal to the successes in yards, out to a range equal to 10 times the Ankida's permanent Faith in yards. The fire's intensity is equal to the number of successes rolled, and it burns for a number of minutes equal to the Ankida's Faith.

The flames are invisible to the normal eye, but the Ankida can vaguely perceive a patch of shimmering haze where the blaze lies, and he can attempt to control it while the ritual persists. Make a Faith roll for the Ankida each turn to control the flames. Each success increases or decreases the blaze's radius by a yard or moves the blaze a yard in any chosen direction.

Within the area of the blaze, mortals and demons take one health level of lethal damage each round for each level of the fire's intensity. This damage can be soaked, but since it is a spiritual flame instead of a physical one, each character rolls Wits instead of Stamina to soak. Physical armor does not add to the soak roll. Characters who are immune to normal fire are also immune to spiritual flame. If the intensity of the fire is enough to ignite objects (see page 177 of the Demon core rules for more details), the items lose one structural level each turn until destroyed or until the fire dies out.

In the spirit world, ghosts (see page 54 of the Demon Storytellers Companion for details) and demons in spirit form that are trapped in the flames take damage, but they may soak with their Stamina and armor as normal."""
ghostly_inferno.torment_effect = """The high-Torment version of this ritual sets the very substance of the spirit realm aflame, feeding on dead souls and the malevolent energies of the realm. The flames of this ritual cannot be controlled by the Ankida, but they are more powerful and cover a greater area. Add half the number of successes rolled (round down) to both the radius and the intensity of the blaze.

While the flames remain invisible, ghastly moans and screams emanate from the affected region. Make a Willpower roll (difficulty 7) for each mortal within the area of effect. If the roll fails, the mortal loses a point of Willpower. If the roll botches, the mortal also gains a temporary derangement (see page 260 of the Demon core rules for details)."""
ghostly_inferno.variations = "Some versions of this ritual allow the creation of flames far from the sigil and performers — the ghostly blaze erupting around a chosen victim anywhere in the world. To perform this variation, add Lore of the Firmament •• to the secondary lore, the sigil must contain a personal item belonging to the target or a piece of her body, and the Ankida cannot control the movements of the flames."
ghostly_inferno.flavor_text = "This ritual allows a Devil to summon a raging inferno not in the mortal world, but in the spirit realm. While the flames do not exist in this world, the effects of the blaze are still felt here — objects and people in the area of effect are burned by cold, invisible flames."
ghostly_inferno.source_page = "Houses of the Fallen, p. 29"
ghostly_inferno.save()

reshape_soul = Ritual.objects.get_or_create(
    name="Reshape the Soul",
    house=devils,
)[0]
reshape_soul.primary_lore = lore_radiance
reshape_soul.primary_lore_rating = 5
reshape_soul.secondary_lore_requirements = [
    {"lore_id": lore_humanity.id, "rating": 5},
    {"lore_id": lore_longing.id, "rating": 2},
]
reshape_soul.base_cost = 36
reshape_soul.minimum_casting_time = 144
reshape_soul.restrictions = "The mortal being affected by the ritual must remain in the center of the sigil throughout. If she is an unwilling participant, she must be restrained or incapacitated so that she cannot leave."
reshape_soul.system = """Roll Manipulation + Subterfuge; the target resists with a Willpower roll (difficulty 8). If the Ankida gains more successes, the mortal's mind and soul can be remade as she sees fit. The Ankida can alter the human's personality any way she likes, replacing his Nature and Demeanor with any Archetypes she wishes. She can also alter the mortal's memories — one significant memory or chain of memories for each success gained on the ritual — change his opinions, make him loyal to the Ankida (or to someone else) and so on. The ritual cannot increase the mortal's Faith potential. That requires a personal journey for the mortal that cannot be tampered with by demonic powers.

If the Ankida wishes to make the mortal into an undercover agent, she can implant post-hypnotic suggestions into his subconscious. Every success gained on the evocation roll provides a suggestion that can be implanted, with a predetermined trigger and outcome of the Ankida's choosing. When the trigger condition is activated, the mortal will follow his orders, then return to normal with no memory of what he has done. Some suggestions might be reusable on an ongoing basis, such as, "Report on what Manishtusu has done in the last week." Others, such as, "Kill Matthew Wallace," will expire once completed and pass from the mortal's programming. The Storyteller is the final arbiter as to whether or not an implanted suggestion is reusable over a period of time.

The effects of this ritual are permanent unless they are undone by another demon. The Revelation evocation of the Lore of Radiance can negate the programming, though the difficulty of the evocation roll increases by two. Before this can be done, though, the demon must realize that the mortal has been affected by Reshape the Soul, which can only be determined through observation and deduction."""
reshape_soul.torment_effect = """The high-Torment version of this ritual reprograms a mortal as normal, but at the cost of his sanity. The psyche and very soul of the human are damaged, and he is doomed to madness. If the ritual succeeds, the mortal gains a permanent derangement. For every success gained on the ritual after the first, he also loses a point of permanent Willpower (down to a minimum of one point). Furthermore, he will lose a point of temporary Willpower each time a post-hypnotic suggestion is activated."""
reshape_soul.variations = "None"
reshape_soul.flavor_text = "This powerful, terrible ritual is a product of the dark days of the Time of Atrocities, when both angels and demons made use of mortal worshippers or followers to strike at their enemies. With this ritual, demons would 'reprogram' a mortal's personality, shaping her into a perfect spy — or weapon."
reshape_soul.source_page = "Houses of the Fallen, p. 30"
reshape_soul.save()

print("Devil (Namaru) rituals from Houses of the Fallen loaded successfully")

"""
Populate database with Devourer (Rabisu) rituals from Houses of the Fallen.
"""

from characters.models.demon.ritual import Ritual
from populate_db.demon.demon_houses import devourers
from populate_db.demon.demon_lores import lore_of_humanity
from populate_db.demon.demon_lores import lore_of_paths as lore_paths
from populate_db.demon.demon_lores import lore_of_the_beast as lore_beast
from populate_db.demon.demon_lores import lore_of_the_wild as lore_wild

# =============================================================================
# DEVOURER RITUALS - HOUSES OF THE FALLEN
# =============================================================================

animated_plant = Ritual.objects.get_or_create(
    name="Animated Plant",
    house=devourers,
)[0]
animated_plant.primary_lore = lore_wild
animated_plant.primary_lore_rating = 5
animated_plant.secondary_lore_requirements = [
    {"lore_id": lore_beast.id, "rating": 4},
]
animated_plant.base_cost = 18
animated_plant.minimum_casting_time = 81
animated_plant.restrictions = "The plants to be enchanted must be placed within the sigil and targeted with the ritual when they are only seedlings."
animated_plant.system = """Spend a Faith point and roll Intelligence + Survival. The seedlings can be planted and nurtured like any other flora once the ritual has been cast on them; they are affected by the Devourer's Lore of the Wild like normal plants. The affected plants are far more than mere vegetation, however. They have rudimentary intelligence equivalent to that of an animal. The effect on the plants is permanent once the ritual has been completed. As they grow, they develop their intelligence just as a wild animal does.

The plant also develops natural weapons it can use for hunting or combat. The plant's attack and damage dice pools are equal to the Ankida's Faith rating. The damage the plant inflicts is lethal.

Devourers who wish to command these animated plants must use evocations such as Command the Wild (Wild •••) to do so. Without this control, the plants are as wild and feral as any untamed animal."""
animated_plant.torment_effect = """If the ritual is affected by Torment, controlling these plants — which develop a vicious and bloodthirsty will of their own — requires a demon using Command the Wild to also succeed on a Willpower roll with a difficulty equal to the Ankida's Torment score. In addition, when the plants successfully cause damage to someone, they also inflict an additional lethal health level of damage. Their sap is caustic and toxic, highly dangerous to mortal, animal and demon alike."""
animated_plant.variations = "Unconfirmed rumors told of plants that could speak with men, created by incorporating the Lore of Humanity • into the ritual."
animated_plant.flavor_text = "In time, the most senior Rabisu mastered plants and animals alike, and under their watchful gaze the two began to blur. With this ritual and others like it, the Devourers created intelligent and active plants that were far more than mere vegetation."
animated_plant.source_page = "Houses of the Fallen, p. 161"
animated_plant.save()

beast_tongue = Ritual.objects.get_or_create(
    name="Beast Tongue",
    house=devourers,
)[0]
beast_tongue.primary_lore = lore_beast
beast_tongue.primary_lore_rating = 2
beast_tongue.secondary_lore_requirements = [
    {"lore_id": lore_of_humanity.id, "rating": 1},
]
beast_tongue.base_cost = 6
beast_tongue.minimum_casting_time = 9
beast_tongue.restrictions = (
    "The sigil must be drawn with a solution infused with woodbine and robin."
)
beast_tongue.system = """Roll Manipulation + Empathy. The ritual can affect a number of mortals (or demons) equal to the Ankida's Faith score multiplied by the number of successes rolled. Once it takes effect, the subjects can converse with any natural animal that is ordinarily capable of communicating with others of its kind. The animal will perceive the ritual subjects to be communicating with it as others of its kind would. The ritual's effects last for a number of hours equal to the Ankida's Faith score."""
beast_tongue.torment_effect = """The ritual's subjects can still communicate with animals, but their "speech" comes out hostile and aggressive. Animals will react as if threatened to anything the subjects say while affected by the ritual. A mortal or demon must rely on a Manipulation + Animal Ken roll against a difficulty equal to the Ankida's Torment score to overcome this effect and be understood normally."""
beast_tongue.variations = "Increasing the Humanity rating to •• causes animals who are being spoken to by a ritual subject to be naturally predisposed in her favor, regardless of whether they have been previously commanded by a Devourer to be friendly."
beast_tongue.flavor_text = "The demons of the Sixth House had easy access to the minds and hearts of the animals with which they worked, but their human allies had no such advantage. The ability to converse with animals in tactical situations was invaluable to the Rabisu, and the Beast Tongue ritual was developed to extend this ability to the mortals who aided them."
beast_tongue.source_page = "Houses of the Fallen, p. 161"
beast_tongue.save()

wild_path = Ritual.objects.get_or_create(
    name="Wild Path",
    house=devourers,
)[0]
wild_path.primary_lore = lore_wild
wild_path.primary_lore_rating = 4
wild_path.secondary_lore_requirements = [
    {"lore_id": lore_paths.id, "rating": 2},
]
wild_path.base_cost = 12
wild_path.minimum_casting_time = 36
wild_path.restrictions = "The subjects must stand within the sigil, which must be inscribed in a natural clearing in a copse of trees or forest."
wild_path.system = """Spend one Faith point and roll Stamina + Survival. The ritual affects a number of subjects — mortal or demon — up to the number of successes rolled. The ritual lasts for 12 hours, and during that period the affected subjects can step into one tree and emerge from another just as if they had traversed a path. This effect works anywhere within the Ankida's Faith score in miles from the ritual's sigil.

In effect, the ritual spontaneously creates paths for the beneficiaries of the ritual between the trees in the ritual's area of effect, as and when the paths are needed. If a subject tries to step out of a tree that is outside the area of the ritual's influence, she is automatically diverted to the nearest tree that is within the Ankida's Faith in miles of the ritual sigil.

Identifying the correct tree to step out of requires a Perception + Survival roll (difficulty 7). If the roll fails, the person steps out of a random tree in the ritual's area of effect."""
wild_path.torment_effect = """If the ritual is affected by Torment, the demons' taint irritates the trees and provokes resistance. Stepping into a tree requires a Willpower roll against the Ankida's Torment score, to push one's way past the Torment-induced barrier."""
wild_path.variations = "None"
wild_path.flavor_text = "Speed and mobility on the field of war were essential for victory. Where others used their wings, many Ninurtu used the plants they had nurtured from infancy to burgeoning adulthood. Using the Wild Path ritual, Devourers could step into a stand of trees and step out a mile away, an unpleasant surprise to the enemy with their backs turned."
wild_path.source_page = "Houses of the Fallen, p. 161"
wild_path.save()


"""
Populate database with Defiler (Lammasu) rituals from Houses of the Fallen.
"""

from characters.models.demon.ritual import Ritual
from populate_db.demon.demon_houses import defilers
from populate_db.demon.demon_lores import lore_of_awakening as lore_awakening
from populate_db.demon.demon_lores import (
    lore_of_longing,
    lore_of_patterns,
    lore_of_storms,
)
from populate_db.demon.demon_lores import lore_of_the_flesh as lore_flesh
from populate_db.demon.demon_lores import lore_of_the_fundament as lore_fundament
from populate_db.demon.demon_lores import lore_of_transfiguration

# =============================================================================
# DEFILER RITUALS - HOUSES OF THE FALLEN
# =============================================================================

horn_of_truesight = Ritual.objects.get_or_create(
    name="Horn of Truesight",
    house=defilers,
)[0]
horn_of_truesight.primary_lore = lore_of_longing
horn_of_truesight.primary_lore_rating = 2
horn_of_truesight.secondary_lore_requirements = [
    {"lore_id": lore_of_patterns.id, "rating": 1},
]
horn_of_truesight.base_cost = 6
horn_of_truesight.minimum_casting_time = 9
horn_of_truesight.restrictions = "The recipient must be within sight of the Ankida for the duration of casting. Traditionally this ritual was bound into a circlet of horn taken from a creature of the oceans to make a permanent enchanted item, but since no suitable creatures currently exist, its use is strictly temporary."
horn_of_truesight.system = """A roll is necessary for this ritual only if an external force tries to implant false dreams into the recipient. If such is the case, roll the Ankida's Manipulation + Intuition in the same way that Perception + Alertness is used to resist illusions (see the core rulebook, page 171). If this roll is successful, it indicates that the dream could not break the barrier.

Otherwise, the ritual's effects are such that hidden truths about the dreamer's own personality are revealed, allowing her to gain greater insight into herself and possibly restore lost confidence or conviction. At the Storyteller's discretion, the recipient of this ritual might regain one or more lost Willpower points upon awaking and may overcome a temporary derangement.

The protective aspect of this ritual is effective for as many nights as the Ankida has points of Faith."""
horn_of_truesight.torment_effect = """Instead of filtering natural dreams, the ritual creates its own — dreams of fear and paranoia that make it impossible to rest. The effects of the ritual last for a number of days equal to the Ankida's Torment. Each time the recipient awakens from sleep within that time frame, he loses one die from all Mental dice pools, though no dice pool may be reduced below one die. The recipient can attempt to avoid this erosion of mental faculties by remaining awake, requiring Stamina or Willpower rolls as the Storyteller deems appropriate. Once the ritual effect ends and the recipient gains a full night of undisturbed sleep, his mental faculties return to normal."""
horn_of_truesight.variations = "Another version of the ritual, with the same components, filters out true dreams, instead of the opposite. It is easier to create an enchanted object with this version, since it requires ivory from a sea creature — the tusks of a walrus or narwhal will suffice."
horn_of_truesight.flavor_text = "This ritual influences the dreams of the recipient, but only as a filter. Only things that are true will appear in dreams, but the ritual does not influence what those dreams might be. If the recipient was to have had false dreams, they simply would not occur, and nothing would take their place."
horn_of_truesight.source_page = "Houses of the Fallen, p. 130"
horn_of_truesight.save()

liquid_assassin = Ritual.objects.get_or_create(
    name="Liquid Assassin",
    house=defilers,
)[0]
liquid_assassin.primary_lore = lore_of_storms
liquid_assassin.primary_lore_rating = 2
liquid_assassin.secondary_lore_requirements = [
    {"lore_id": lore_fundament.id, "rating": 2},
]
liquid_assassin.base_cost = 8
liquid_assassin.minimum_casting_time = 16
liquid_assassin.restrictions = "The Ankida must hold a vial of quicksilver in her hand during the casting of the ritual, and the target must be within the Ankida's line of sight at the ritual's culmination."
liquid_assassin.system = """Roll Manipulation + Science (difficulty 7). Each success represents a quantity of moisture drawn from the victim's surrounding environment that condenses on the victim's skin and slowly flows into his mouth and nostrils. The victim can attempt to fling the water from his skin with a Strength + Dodge roll (difficulty 7), with each success canceling one of the Ankida's successes. Each unsaved success inflicts one health level of lethal damage per turn for a number of turns equal to the Ankida's Faith score.

Using towels or other absorbent material has no effect on the water, but high temperatures will evaporate it. Every 10 degrees of heat above 90 degrees Fahrenheit cancels one of the Ankida's successes each turn.

Within the area of the blaze, mortals and demons take one health level of lethal damage each round for each level of the fire's intensity."""
liquid_assassin.torment_effect = """All the water between the Ankida and the victim (and a yard on either side of that line), acts in a similar manner, trying to kill every mortal in the affected area."""
liquid_assassin.variations = "If Lore of the Winds •• is used instead of Fundament, then the ritual becomes far more beneficial, allowing the recipients (either a single individual, or all the members participating in the ritual) to breathe beneath water for one hour per success rolled on Constitution + Science. Adding Fundament • to the Winds •• version allows the recipients to resist water pressure as well."
liquid_assassin.flavor_text = "This simple but potentially lethal ritual literally forces water into a victim's lungs, drowning him far from the presence of any large body of water."
liquid_assassin.source_page = "Houses of the Fallen, p. 131"
liquid_assassin.save()

prenatal_guardian = Ritual.objects.get_or_create(
    name="Prenatal Guardian",
    house=defilers,
)[0]
prenatal_guardian.primary_lore = lore_of_transfiguration
prenatal_guardian.primary_lore_rating = 3
prenatal_guardian.secondary_lore_requirements = [
    {"lore_id": lore_of_storms.id, "rating": 2},
    {"lore_id": lore_flesh.id, "rating": 1},
]
prenatal_guardian.base_cost = 18
prenatal_guardian.minimum_casting_time = 36
prenatal_guardian.restrictions = (
    "Must be cast upon a pregnant woman within one week of conception."
)
prenatal_guardian.system = """Roll Stamina + Medicine (difficulty 8). Each success protects against a negative influence on the growing fetus. Such an influence might be the transmission of a disease or poison from the mother's body, the development of a congenital disease or even miscarriage. When the baby is born, any remaining successes not used will increase the baby's potential Attributes at the Storyteller's discretion.

These rituals can create child prodigies whose talents far exceed those of their peers, creating a potential resource for unscrupulous fallen. There are rumors that monstrous demons and even Earthbound continue to refine this ritual as a means of creating superhuman vessels for themselves or their still-imprisoned superiors, sometimes using isolated villages to breed scores of altered children for their experimentations.

This ritual can be cast more than once during the one-week period after conception, but the successes do not stack. Instead, the roll with the highest number of successes is used. It can be cast only once per day per woman. If the woman is bearing more than one child, then each is affected, but the number of children is subtracted from the number of successes."""
prenatal_guardian.torment_effect = """The high-Torment version of this ritual creates a soulless twin of the unborn child. Instead of shielding the child from disease or malformation, these evils are passed onto the twin, yet the power of the ritual ensures that the twin will survive its deformities and be born as a feral, bloodthirsty monster. Like the low-Torment version of this ritual, extra successes increase this twin's Attributes, so it is possible that the infant can emerge fully formed (and lethally capable) from the womb."""
prenatal_guardian.variations = "One form of punishment inflicted on human women was to curse them with bearing an animal (usually a goat). Replace Flesh • with Lore of the Beast •. Note that the animal grows at the same rate and to the same size as a human baby, making it a (very slow) way to produce giant-sized animals. The animal chosen may create other complications, at Storyteller discretion."
prenatal_guardian.flavor_text = "Before the war, one of the functions of the Angels of the Deep was to protect children growing in the womb. Few, however, had the time or even desire to do so during the darker days of the war. This ritual was developed to provide a similar function, in order to assuage the guilt felt by some Defilers (though others used it as a tool of propaganda and control over the human population)."
prenatal_guardian.source_page = "Houses of the Fallen, p. 132"
prenatal_guardian.save()

song_of_ecstatic_battle = Ritual.objects.get_or_create(
    name="Song of Ecstatic Battle",
    house=defilers,
)[0]
song_of_ecstatic_battle.primary_lore = lore_of_longing
song_of_ecstatic_battle.primary_lore_rating = 3
song_of_ecstatic_battle.secondary_lore_requirements = [
    {"lore_id": lore_of_transfiguration.id, "rating": 2},
    {"lore_id": lore_awakening.id, "rating": 2},
]
song_of_ecstatic_battle.base_cost = 21
song_of_ecstatic_battle.minimum_casting_time = 49
song_of_ecstatic_battle.restrictions = (
    "A drop of blood from every human potentially affected."
)
song_of_ecstatic_battle.system = """Roll Charisma + Leadership. For each success, three troops can be affected. When they have taken between two (Hurt) and five (Mauled) health levels of damage, they add one die to any pool based on a Physical Attribute, rather than subtracting anything.

Once they reach six levels (Crippled), however, the entire effect catches up with them. In addition, each level of lethal damage taken while under the effect of the ritual creates an extra level of bashing damage (that cannot be soaked) once the effect dissipates. The duration is 10 minutes per point of Faith."""
song_of_ecstatic_battle.torment_effect = """An attempt to relieve anyone of the ability to feel pain is anathema to a tormented soul. This version adds an extra die to every Physical dice pool, but the pain from any attack is such that wound penalties are doubled. (Once Hurt they are at -1, Wounded is -3, and Crippled is -9.)"""
song_of_ecstatic_battle.variations = """A strange version of this ritual replaces the Lore of Awakening with the Lore of Humanity •••. Each wound sustained under this ritual makes the character less likely to be attacked if he wishes to retreat (or move to a more strategic location). Each time a recipient is wounded, he can decide to step back, in which case the wound penalty acts as if that many dice were rolled on a use of the Fade evocation (Humanity •••). For example, if an affected soldier is Mauled (with a -2 wound penalty), any opponent would have to make a Willpower roll and get more than two successes to continue the attack on that individual (and in a pitched battle is more likely to just focus on a different target). If the soldier continued attacking, however, this chance is lost until he is wounded again. If the recipient was to attack after the person who injured him in the turn, then he must abort his action to keep from doing so (see the core rulebook, page 240). The effects of the Fade on each individual so affected lasts one minute per point of Faith in the ritual."""
song_of_ecstatic_battle.flavor_text = "This ritual enables human troops to more effectively fight on while injured. Under its effects, each feels no pain from wounds, but only a surge of adrenaline and power that makes them redouble their attack."
song_of_ecstatic_battle.source_page = "Houses of the Fallen, p. 132"
song_of_ecstatic_battle.save()

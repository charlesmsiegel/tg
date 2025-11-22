from characters.models.demon.apocalyptic_form import ApocalypticFormTrait
from characters.models.demon.house import DemonHouse
from characters.models.demon.visage import Visage

# Get the houses
from populate_db.demon_houses import (
    defilers,
    devils,
    devourers,
    fiends,
    malefactors,
    scourges,
    slayers,
)

# =============================================================================
# APOCALYPTIC FORM TRAIT DEFINITIONS
# =============================================================================

trait_affirm_devils_cost3 = ApocalypticFormTrait.objects.get_or_create(
    name="Affirm", cost=3, house=devils
)[0]
trait_alter_size_defilers_cost3 = ApocalypticFormTrait.objects.get_or_create(
    name="Alter Size", cost=3, house=defilers
)[0]
trait_alter_size_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Alter Size", house=malefactors
)[0]
trait_armor = ApocalypticFormTrait.objects.get_or_create(name="Armor", house=None)[0]
trait_armor_cost4 = ApocalypticFormTrait.objects.get_or_create(
    name="Armor", cost=4, house=None
)[0]
trait_aura_of_dread_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Aura of Dread", house=slayers
)[0]
trait_aura_of_entropy_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Aura of Entropy", house=slayers
)[0]
trait_aura_of_misfortune_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Aura of Misfortune", house=fiends
)[0]
trait_aura_of_vitality_scourges = ApocalypticFormTrait.objects.get_or_create(
    name="Aura of Vitality", house=scourges
)[0]
trait_beckon_devils_cost2 = ApocalypticFormTrait.objects.get_or_create(
    name="Beckon", cost=2, house=devils
)[0]
trait_blades_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Blades", house=malefactors
)[0]
trait_casts_no_reflection = ApocalypticFormTrait.objects.get_or_create(
    name="Casts No Reflection", house=None
)[0]
trait_caustic_bile_scourges = ApocalypticFormTrait.objects.get_or_create(
    name="Caustic Bile", house=scourges
)[0]
trait_chameleon_skin_devourers = ApocalypticFormTrait.objects.get_or_create(
    name="Chameleon Skin", house=devourers
)[0]
trait_chimerical_attack_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Chimerical Attack", house=fiends
)[0]
trait_chimerical_aura_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Chimerical Aura", house=fiends
)[0]
trait_claws_teeth = ApocalypticFormTrait.objects.get_or_create(
    name="Claws/Teeth", house=None
)[0]
trait_cloak_of_shadows_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Cloak of Shadows", house=fiends
)[0]
trait_cloak_of_shadows_scourges = ApocalypticFormTrait.objects.get_or_create(
    name="Cloak of Shadows", house=scourges
)[0]
trait_cloak_of_shadows_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Cloak of Shadows", house=slayers
)[0]
trait_conjuration_slayers_cost2 = ApocalypticFormTrait.objects.get_or_create(
    name="Conjuration", cost=2, house=slayers
)[0]
trait_conjure_from_nothing_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Conjure from Nothing", house=slayers
)[0]
trait_corrosive_spit_devils = ApocalypticFormTrait.objects.get_or_create(
    name="Corrosive Spit", house=devils
)[0]
trait_damage_resistance = ApocalypticFormTrait.objects.get_or_create(
    name="Damage Resistance", house=None
)[0]
trait_dead_reckoning_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Dead Reckoning", house=malefactors
)[0]
trait_dead_reckoning_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Dead Reckoning", house=slayers
)[0]
trait_death_grip_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Death-Grip", house=slayers
)[0]
trait_death_grip_slayers_cost4 = ApocalypticFormTrait.objects.get_or_create(
    name="Death-Grip", cost=4, house=slayers
)[0]
trait_distortion_defilers_cost3 = ApocalypticFormTrait.objects.get_or_create(
    name="Distortion", cost=3, house=defilers
)[0]
trait_dread_gaze_devils = ApocalypticFormTrait.objects.get_or_create(
    name="Dread Gaze", house=devils
)[0]
trait_dread_gaze_devils_cost4 = ApocalypticFormTrait.objects.get_or_create(
    name="Dread Gaze", cost=4, house=devils
)[0]
trait_dread_gaze_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Dread Gaze", house=slayers
)[0]
trait_dread_gaze_slayers_cost4 = ApocalypticFormTrait.objects.get_or_create(
    name="Dread Gaze", cost=4, house=slayers
)[0]
trait_dread_mien_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Dread Mien", house=fiends
)[0]
trait_dread_mien_fiends_cost1 = ApocalypticFormTrait.objects.get_or_create(
    name="Dread Mien", cost=1, house=fiends
)[0]
trait_enhanced_ability_cost3 = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Ability", cost=3, house=None
)[0]
trait_enhanced_awareness_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Awareness", house=slayers
)[0]
trait_enhanced_dodge_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Dodge", house=fiends
)[0]
trait_enhanced_dodge_fiends_cost1 = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Dodge", cost=1, house=fiends
)[0]
trait_enhanced_dodge_scourges = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Dodge", house=scourges
)[0]
trait_enhanced_empathy_defilers = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Empathy", house=defilers
)[0]
trait_enhanced_intuition_defilers = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Intuition", house=defilers
)[0]
trait_enhanced_intuition_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Intuition", house=fiends
)[0]
trait_enhanced_intuition_scourges = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Intuition", house=scourges
)[0]
trait_enhanced_mental_acuity_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Mental Acuity", house=fiends
)[0]
trait_enhanced_perception_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Perception", house=malefactors
)[0]
trait_enhanced_senses = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Senses", house=None
)[0]
trait_enhanced_senses_cost3 = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Senses", cost=3, house=None
)[0]
trait_enhanced_social_traits_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Social Traits", house=slayers
)[0]
trait_extra_actions = ApocalypticFormTrait.objects.get_or_create(
    name="Extra Actions", house=None
)[0]
trait_extra_actions_cost3 = ApocalypticFormTrait.objects.get_or_create(
    name="Extra Actions", cost=3, house=None
)[0]
trait_extra_health_levels = ApocalypticFormTrait.objects.get_or_create(
    name="Extra Health Levels", house=None
)[0]
trait_extra_limbs = ApocalypticFormTrait.objects.get_or_create(
    name="Extra Limbs", house=None
)[0]
trait_eyes_of_fate_fiends_cost4 = ApocalypticFormTrait.objects.get_or_create(
    name="Eyes of Fate", cost=4, house=fiends
)[0]
trait_fiery_blood_devils = ApocalypticFormTrait.objects.get_or_create(
    name="Fiery Blood", house=devils
)[0]
trait_flashing_fingers_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Flashing Fingers", house=malefactors
)[0]
trait_gaping_maw = ApocalypticFormTrait.objects.get_or_create(
    name="Gaping Maw", house=None
)[0]
trait_ghost_sight_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Ghost Sight", house=slayers
)[0]
trait_ghost_sight_slayers_cost2 = ApocalypticFormTrait.objects.get_or_create(
    name="Ghost Sight", cost=2, house=slayers
)[0]
trait_horns = ApocalypticFormTrait.objects.get_or_create(name="Horns", house=None)[0]
trait_howl_of_the_damned_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Howl of the Damned", house=slayers
)[0]
trait_hypnotic_visions_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Hypnotic Visions", house=fiends
)[0]
trait_ichor_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Ichor", house=malefactors
)[0]
trait_immune_to_electricity_defilers = ApocalypticFormTrait.objects.get_or_create(
    name="Immune to Electricity", house=defilers
)[0]
trait_immune_to_fire_devils_cost3 = ApocalypticFormTrait.objects.get_or_create(
    name="Immune to Fire", cost=3, house=devils
)[0]
trait_immune_to_fire_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Immune to Fire", house=malefactors
)[0]
trait_immune_to_poisons_devourers = ApocalypticFormTrait.objects.get_or_create(
    name="Immune to Poisons", house=devourers
)[0]
trait_immunity_to_fire_devils = ApocalypticFormTrait.objects.get_or_create(
    name="Immunity to Fire", house=devils
)[0]
trait_improved_dexterity_defilers = ApocalypticFormTrait.objects.get_or_create(
    name="Improved Dexterity", house=defilers
)[0]
trait_improved_initiative = ApocalypticFormTrait.objects.get_or_create(
    name="Improved Initiative", house=None
)[0]
trait_increased_awareness_devils = ApocalypticFormTrait.objects.get_or_create(
    name="Increased Awareness", house=devils
)[0]
trait_increased_awareness_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Increased Awareness", house=fiends
)[0]
trait_increased_size = ApocalypticFormTrait.objects.get_or_create(
    name="Increased Size", house=None
)[0]
trait_increased_size_cost3 = ApocalypticFormTrait.objects.get_or_create(
    name="Increased Size", cost=3, house=None
)[0]
trait_inhuman_allure_devils = ApocalypticFormTrait.objects.get_or_create(
    name="Inhuman Allure", house=devils
)[0]
trait_inhuman_allure_devils_cost2 = ApocalypticFormTrait.objects.get_or_create(
    name="Inhuman Allure", cost=2, house=devils
)[0]
trait_ink_cloud_defilers = ApocalypticFormTrait.objects.get_or_create(
    name="Ink Cloud", house=defilers
)[0]
trait_ink_cloud_defilers_cost2 = ApocalypticFormTrait.objects.get_or_create(
    name="Ink Cloud", cost=2, house=defilers
)[0]
trait_iron_skin_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Iron Skin", house=malefactors
)[0]
trait_iron_skin_malefactors_cost3 = ApocalypticFormTrait.objects.get_or_create(
    name="Iron Skin", cost=3, house=malefactors
)[0]
trait_irresistible_force_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Irresistible Force", house=malefactors
)[0]
trait_lashing_tail = ApocalypticFormTrait.objects.get_or_create(
    name="Lashing Tail", house=None
)[0]
trait_lordly_mien_devils = ApocalypticFormTrait.objects.get_or_create(
    name="Lordly Mien", house=devils
)[0]
trait_lordly_mien_devils_cost2 = ApocalypticFormTrait.objects.get_or_create(
    name="Lordly Mien", cost=2, house=devils
)[0]
trait_lyrical_voice_defilers = ApocalypticFormTrait.objects.get_or_create(
    name="Lyrical Voice", house=defilers
)[0]
trait_magnetic_field_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Magnetic Field", house=malefactors
)[0]
trait_master_artisan_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Master Artisan", house=malefactors
)[0]
trait_miasma_scourges = ApocalypticFormTrait.objects.get_or_create(
    name="Miasma", house=scourges
)[0]
trait_mirage_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Mirage", house=malefactors
)[0]
trait_mirage_malefactors_cost2 = ApocalypticFormTrait.objects.get_or_create(
    name="Mirage", cost=2, house=malefactors
)[0]
trait_mist_scourges_cost4 = ApocalypticFormTrait.objects.get_or_create(
    name="Mist", cost=4, house=scourges
)[0]
trait_multiple_eyes_scourges = ApocalypticFormTrait.objects.get_or_create(
    name="Multiple Eyes", house=scourges
)[0]
trait_night_sight_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Night Sight", house=fiends
)[0]
trait_night_sight_fiends_cost2 = ApocalypticFormTrait.objects.get_or_create(
    name="Night Sight", cost=2, house=fiends
)[0]
trait_night_sight_slayers_cost1 = ApocalypticFormTrait.objects.get_or_create(
    name="Night Sight", cost=1, house=slayers
)[0]
trait_night_vision_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Night Vision", house=malefactors
)[0]
trait_pass_without_trace = ApocalypticFormTrait.objects.get_or_create(
    name="Pass Without Trace", house=None
)[0]
trait_perfect_balance_scourges = ApocalypticFormTrait.objects.get_or_create(
    name="Perfect Balance", house=scourges
)[0]
trait_quills_scourges = ApocalypticFormTrait.objects.get_or_create(
    name="Quills", house=scourges
)[0]
trait_radiant_aura_devils = ApocalypticFormTrait.objects.get_or_create(
    name="Radiant Aura", house=devils
)[0]
trait_radiant_aura_devils_cost1 = ApocalypticFormTrait.objects.get_or_create(
    name="Radiant Aura", cost=1, house=devils
)[0]
trait_regeneration = ApocalypticFormTrait.objects.get_or_create(
    name="Regeneration", house=None
)[0]
trait_regeneration_cost4 = ApocalypticFormTrait.objects.get_or_create(
    name="Regeneration", cost=4, house=None
)[0]
trait_relentless_devourers_cost1 = ApocalypticFormTrait.objects.get_or_create(
    name="Relentless", cost=1, house=devourers
)[0]
trait_relentless_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Relentless", house=malefactors
)[0]
trait_relentless_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Relentless", house=slayers
)[0]
trait_relentless_slayers_cost1 = ApocalypticFormTrait.objects.get_or_create(
    name="Relentless", cost=1, house=slayers
)[0]
trait_scales_devils = ApocalypticFormTrait.objects.get_or_create(
    name="Scales", house=devils
)[0]
trait_seas_beauty_defilers_cost3 = ApocalypticFormTrait.objects.get_or_create(
    name="Sea's Beauty", cost=3, house=defilers
)[0]
trait_sense_the_hidden_devils = ApocalypticFormTrait.objects.get_or_create(
    name="Sense the Hidden", house=devils
)[0]
trait_shark_hide_defilers = ApocalypticFormTrait.objects.get_or_create(
    name="Shark Hide", house=defilers
)[0]
trait_shocking_touch_defilers = ApocalypticFormTrait.objects.get_or_create(
    name="Shocking Touch", house=defilers
)[0]
trait_shroud_of_flames_devils = ApocalypticFormTrait.objects.get_or_create(
    name="Shroud of Flames", house=devils
)[0]
trait_sibilant_whispers_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Sibilant Whispers", house=fiends
)[0]
trait_spark_of_faith_devils_cost3 = ApocalypticFormTrait.objects.get_or_create(
    name="Spark of Faith", cost=3, house=devils
)[0]
trait_spikes_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Spikes", house=malefactors
)[0]
trait_spines_defilers = ApocalypticFormTrait.objects.get_or_create(
    name="Spines", house=defilers
)[0]
trait_spines_defilers_cost2 = ApocalypticFormTrait.objects.get_or_create(
    name="Spines", cost=2, house=defilers
)[0]
trait_supernatural_vision_scourges = ApocalypticFormTrait.objects.get_or_create(
    name="Supernatural Vision", house=scourges
)[0]
trait_thick_hide_devourers = ApocalypticFormTrait.objects.get_or_create(
    name="Thick Hide", house=devourers
)[0]
trait_thick_hide_devourers_cost2 = ApocalypticFormTrait.objects.get_or_create(
    name="Thick Hide", cost=2, house=devourers
)[0]
trait_thorns_devourers = ApocalypticFormTrait.objects.get_or_create(
    name="Thorns", house=devourers
)[0]
trait_thorns_devourers_cost1 = ApocalypticFormTrait.objects.get_or_create(
    name="Thorns", cost=1, house=devourers
)[0]
trait_thunderous_voice_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Thunderous Voice", house=malefactors
)[0]
trait_toxins_devourers = ApocalypticFormTrait.objects.get_or_create(
    name="Toxins", house=devourers
)[0]
trait_unearthly_glamour_fiends = ApocalypticFormTrait.objects.get_or_create(
    name="Unearthly Glamour", house=fiends
)[0]
trait_venom_defilers = ApocalypticFormTrait.objects.get_or_create(
    name="Venom", house=defilers
)[0]
trait_viscous_flesh_scourges = ApocalypticFormTrait.objects.get_or_create(
    name="Viscous Flesh", house=scourges
)[0]
trait_voice_of_the_damned_devils = ApocalypticFormTrait.objects.get_or_create(
    name="Voice of the Damned", house=devils
)[0]
trait_voice_of_the_grave_slayers = ApocalypticFormTrait.objects.get_or_create(
    name="Voice of the Grave", house=slayers
)[0]
trait_weather_sense_defilers = ApocalypticFormTrait.objects.get_or_create(
    name="Weather Sense", house=defilers
)[0]
trait_wings = ApocalypticFormTrait.objects.get_or_create(name="Wings", house=None)[0]
trait_wings_cost3 = ApocalypticFormTrait.objects.get_or_create(
    name="Wings", cost=3, house=None
)[0]

# Additional traits for specific visages
trait_enhanced_social_traits_devourers = ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Social Traits", house=devourers
)[0]
trait_immune_to_bashing_damage_malefactors = ApocalypticFormTrait.objects.get_or_create(
    name="Immune to Bashing Damage", house=malefactors
)[0]
trait_immune_to_falling_damage_scourges = ApocalypticFormTrait.objects.get_or_create(
    name="Immune to Falling Damage", house=scourges
)[0]
trait_improved_physical_capabilities_scourges = (
    ApocalypticFormTrait.objects.get_or_create(
        name="Improved Physical Capabilities", house=scourges
    )[0]
)

# =============================================================================
# VISAGE DEFINITIONS
# =============================================================================

# DEVIL VISAGES
# Bel, the Visage of the Celestials
bel = Visage.objects.get_or_create(
    name="Bel",
    house=devils,
    defaults={
        "description": "The apocalyptic form of the Lore of the Celestials reveals the fallen as a luminous, lordly angel, radiating divine grandeur and authority. Her skin literally glows, wreathing her in an aura of golden light that shifts in intensity depending on her mood. Her eyes blaze with the cold light of the stars. Despite her actual physical appearance, the fallen seems to tower over everyone around her."
    },
)[0]
bel.add_source("Demon: The Fallen", 176)
bel.low_torment_traits.set(
    [
        trait_wings,
        trait_lordly_mien_devils,
        trait_enhanced_senses,
        trait_increased_awareness_devils,
    ]
)
bel.high_torment_traits.set(
    [
        trait_claws_teeth,
        trait_scales_devils,
        trait_increased_size,
        trait_dread_gaze_devils,
    ]
)

# Nusku, the Visage of the Flames
nusku = Visage.objects.get_or_create(
    name="Nusku",
    house=devils,
    defaults={
        "description": "These demons reveal themselves in a blaze of yellow-orange light. Their skin glows with the seething brilliance of the sun, and their image shimmers like a mirage. Their eyes take on the color of burnished gold, and when angered, the Nusku radiate palpable waves of heat. An angel's hair becomes a deep red or reddish-gold and thickens into a leonine mane. Open flames flare brightly in his presence, seeming to bow toward their master as the tongues of flame are drawn to the divinity in their midst."
    },
)[0]
nusku.add_source("Demon: The Fallen", 178)
nusku.low_torment_traits.set(
    [
        trait_shroud_of_flames_devils,
        trait_immunity_to_fire_devils,
        trait_extra_actions,
        trait_improved_initiative,
    ]
)
nusku.high_torment_traits.set(
    [
        trait_claws_teeth,
        trait_lashing_tail,
        trait_increased_size,
        trait_fiery_blood_devils,
    ]
)

# Qingu, the Visage of Radiance
qingu = Visage.objects.get_or_create(
    name="Qingu",
    house=devils,
    defaults={
        "description": "The apocalyptic form of the masters of Radiance is an incandescent figure wreathed in a corona of jewel-like color. Their physical features have more in common with the smooth perfection of marble than with human skin. Their voices are pure as crystal, and they cut through the petty din of the mortal world like a razor."
    },
)[0]
qingu.add_source("Demon: The Fallen", 180)
qingu.low_torment_traits.set(
    [
        trait_wings,
        trait_inhuman_allure_devils,
        trait_radiant_aura_devils,
        trait_sense_the_hidden_devils,
    ]
)
qingu.high_torment_traits.set(
    [
        trait_voice_of_the_damned_devils,
        trait_casts_no_reflection,
        trait_corrosive_spit_devils,
        trait_horns,
    ]
)

# SCOURGE VISAGES
# Dagan, the Visage of Awakenings
dagan = Visage.objects.get_or_create(
    name="Dagan",
    house=scourges,
    defaults={
        "description": "The apocalyptic form of the masters of animation infuses the angel's mortal body with the blush of youth and vibrant health - even the oldest mortal vessel appears to be in the prime of life and moves with inhuman grace, speed and strength. This aura of life and vitality radiates as a palpable sense of warmth, like a beam of sunlight, and every living being touched is temporarily suffused with its power. Wilted flowers return to full bloom, the injured gain strength and the old forget their afflictions."
    },
)[0]
dagan.add_source("Demon: The Fallen", 182)
dagan.low_torment_traits.set(
    [
        trait_aura_of_vitality_scourges,
        trait_pass_without_trace,
        trait_improved_physical_capabilities_scourges,
        trait_wings,
    ]
)
dagan.high_torment_traits.set(
    [
        trait_miasma_scourges,
        trait_extra_health_levels,
        trait_viscous_flesh_scourges,
        trait_extra_limbs,
    ]
)

# Anshar, the Visage of the Firmament
anshar = Visage.objects.get_or_create(
    name="Anshar",
    house=scourges,
    defaults={
        "description": "These Angels of the Firmament reveal themselves as lithe, ethereal figures with pale skin and large gray eyes. When they speak, their voice echoes faintly, as if from a great distance, and they alternate between bouts of quiet distraction and periods of intense, disquieting scrutiny."
    },
)[0]
anshar.add_source("Demon: The Fallen", 184)
anshar.low_torment_traits.set(
    [
        trait_enhanced_senses,
        trait_wings,
        trait_enhanced_intuition_scourges,
        trait_enhanced_dodge_scourges,
    ]
)
anshar.high_torment_traits.set(
    [
        trait_cloak_of_shadows_scourges,
        trait_multiple_eyes_scourges,
        trait_improved_initiative,
        trait_claws_teeth,
    ]
)

# Ellil, the Visage of the Winds
ellil = Visage.objects.get_or_create(
    name="Ellil",
    house=scourges,
    defaults={
        "description": "The monarchs of the air reveal themselves as tall and lithe, with large eyes and swift, graceful movements. When in revelatory form, the Ellil are constantly surrounded by shifting winds that ebb and flow with the intensity of their emotions. Any smoke or steam in the area is often sucked by these winds into a swirling vortex that circles their heads and shoulders like an ominous halo."
    },
)[0]
ellil.add_source("Demon: The Fallen", 185)
ellil.low_torment_traits.set(
    [
        trait_supernatural_vision_scourges,
        trait_wings,
        trait_perfect_balance_scourges,
        trait_immune_to_falling_damage_scourges,
    ]
)
ellil.high_torment_traits.set(
    [
        trait_claws_teeth,
        trait_extra_actions,
        trait_quills_scourges,
        trait_caustic_bile_scourges,
    ]
)

# MALEFACTOR VISAGES
# Kishar, the Visage of the Earth
kishar = Visage.objects.get_or_create(
    name="Kishar",
    house=malefactors,
    defaults={
        "description": "These angels manifest as towering figures with dark skin that ranges from a creamy brown to utter black, and their bodies appear as though hewn from stone, with muscle and bone etched in sharp relief on a frame devoid of soft flesh or fat. The Kishar are hairless, and the irises of their eyes have the clarity and color of gemstones: ruby, sapphire, emerald, garnet, topaz and diamond. The air about them smells of freshly turned earth, rich with the promise of life."
    },
)[0]
kishar.add_source("Demon: The Fallen", 188)
kishar.low_torment_traits.set(
    [
        trait_increased_size,
        trait_immune_to_bashing_damage_malefactors,
        trait_irresistible_force_malefactors,
        trait_night_vision_malefactors,
    ]
)
kishar.high_torment_traits.set(
    [
        trait_extra_limbs,
        trait_gaping_maw,
        trait_spikes_malefactors,
        trait_ichor_malefactors,
    ]
)

# Antu, the Visage of the Paths
antu = Visage.objects.get_or_create(
    name="Antu",
    house=malefactors,
    defaults={
        "description": "The angels of the pathways closely resemble mortals at first glance. Their skin is deeply tanned, as though they'd spent a lifetime in the sun, and the skin around their dark eyes are deeply lined, casting their orbits in permanent shadow. It is only on closer inspection that the worry lines are revealed as intricate patterns that radiate from the angel's eyes and continue to run across the planes of her face, disappearing into her scalp and circling her throat in intricate tattoos. At night these lines reflect the moonlight in ghostly traceries that seem to shift and realign themselves as the angel speaks."
    },
)[0]
antu.add_source("Demon: The Fallen", 189)
antu.low_torment_traits.set(
    [
        trait_dead_reckoning_malefactors,
        trait_enhanced_perception_malefactors,
        trait_improved_initiative,
        trait_flashing_fingers_malefactors,
    ]
)
antu.high_torment_traits.set(
    [
        trait_pass_without_trace,
        trait_alter_size_malefactors,
        trait_mirage_malefactors,
        trait_relentless_malefactors,
    ]
)

# Mummu, the Visage of the Forge
mummu = Visage.objects.get_or_create(
    name="Mummu",
    house=malefactors,
    defaults={
        "description": "The angels of the forge appear as giants hammered from the black iron of the earth, their powerfully muscled forms lit with veins of hot magma, and their eyes shining like disks of burnished brass. Their voices are deep and thunderous, like the roar of a furnace. When in their apocalyptic form, these fallen are immune to extremes of temperature and pressure. They can handle hot coals as mortals do ice cubes."
    },
)[0]
mummu.add_source("Demon: The Fallen", 191)
mummu.low_torment_traits.set(
    [
        trait_master_artisan_malefactors,
        trait_increased_size,
        trait_thunderous_voice_malefactors,
        trait_immune_to_fire_malefactors,
    ]
)
mummu.high_torment_traits.set(
    [
        trait_blades_malefactors,
        trait_extra_limbs,
        trait_magnetic_field_malefactors,
        trait_iron_skin_malefactors,
    ]
)

# FIEND VISAGES
# Ninsun, the Visage of Patterns
ninsun = Visage.objects.get_or_create(
    name="Ninsun",
    house=fiends,
    defaults={
        "description": "The angels of the great pattern have skins of indigo. Their hairless bodies are covered with intricate lines and patterns etched in silvery blue light that shifts and realigns depending on the angle of light and the intensity of the angel's mood. Their eyes are like bright sapphires, casting the cold light of the stars."
    },
)[0]
ninsun.add_source("Demon: The Fallen", 194)
ninsun.low_torment_traits.set(
    [
        trait_wings,
        trait_improved_initiative,
        trait_enhanced_intuition_fiends,
        trait_enhanced_mental_acuity_fiends,
    ]
)
ninsun.high_torment_traits.set(
    [
        trait_aura_of_misfortune_fiends,
        trait_extra_actions,
        trait_extra_limbs,
        trait_sibilant_whispers_fiends,
    ]
)

# Nedu, the Visage of Portals
nedu = Visage.objects.get_or_create(
    name="Nedu",
    house=fiends,
    defaults={
        "description": "The angels of the threshold are tall, ethereal figures, their long limbs and lean bodies wreathed in a veil of shifting shadow. Their movements are as fluid as they are soundless, and their feet leave no impression to mark their passing. When they pass into deep shadow, their eyes shine with a cold, blue light."
    },
)[0]
nedu.add_source("Demon: The Fallen", 196)
nedu.low_torment_traits.set(
    [
        trait_pass_without_trace,
        trait_enhanced_senses,
        trait_increased_awareness_fiends,
        trait_wings,
    ]
)
nedu.high_torment_traits.set(
    [
        trait_cloak_of_shadows_fiends,
        trait_improved_initiative,
        trait_enhanced_dodge_fiends,
        trait_casts_no_reflection,
    ]
)

# Shamash, the Visage of Light
shamash = Visage.objects.get_or_create(
    name="Shamash",
    house=fiends,
    defaults={
        "description": "The apocalyptic form of the masters of this lore paints a demon in shifting patterns of shadow and pale, silvery starlight. These hypnotic images draw the eye and beguile the senses, at times hinting at subtle flashes that reflect the demon's inner thoughts. The Shamash are alluring, chimerical, deceptive, terrifying or achingly beautiful, often from moment to moment."
    },
)[0]
shamash.add_source("Demon: The Fallen", 198)
shamash.low_torment_traits.set(
    [
        trait_enhanced_mental_acuity_fiends,
        trait_night_sight_fiends,
        trait_chimerical_aura_fiends,
        trait_unearthly_glamour_fiends,
    ]
)
shamash.high_torment_traits.set(
    [
        trait_hypnotic_visions_fiends,
        trait_dread_mien_fiends,
        trait_chimerical_attack_fiends,
        trait_casts_no_reflection,
    ]
)

# DEFILER VISAGES
# Ishhara, the Visage of Longing
ishhara = Visage.objects.get_or_create(
    name="Ishhara",
    house=defilers,
    defaults={
        "description": "The angels of inspiration are visions of beauty, compared to whom even the radiant angels of the Namaru pale. Their golden hair and perfectly sculpted features are the romantic ideal spoken of in mortal poetry and prose, and their honeyed voices melt even the hardest hearts."
    },
)[0]
ishhara.add_source("Demon: The Fallen", 199)
ishhara.low_torment_traits.set(
    [
        trait_enhanced_social_traits_devourers,
        trait_lyrical_voice_defilers,
        trait_enhanced_senses,
        trait_enhanced_intuition_defilers,
    ]
)
ishhara.high_torment_traits.set(
    [
        trait_claws_teeth,
        trait_venom_defilers,
        trait_extra_limbs,
        trait_casts_no_reflection,
    ]
)

# Adad, the Visage of Storms
adad = Visage.objects.get_or_create(
    name="Adad",
    house=defilers,
    defaults={
        "description": "The angels of the storm are tall, statuesque figures, their skins glistening like opal and their dark hair tinged with the deep green of the ocean depths. Blue flickers of ball lightning writhe and dance across their bodies, forming an angry nimbus surrounding their head and shoulders when their fury is aroused."
    },
)[0]
adad.add_source("Demon: The Fallen", 201)
adad.low_torment_traits.set(
    [
        trait_weather_sense_defilers,
        trait_immune_to_electricity_defilers,
        trait_improved_initiative,
        trait_shocking_touch_defilers,
    ]
)
adad.high_torment_traits.set(
    [
        trait_claws_teeth,
        trait_spines_defilers,
        trait_shark_hide_defilers,
        trait_ink_cloud_defilers,
    ]
)

# Mammetum, the Visage of Transfiguration
mammetum = Visage.objects.get_or_create(
    name="Mammetum",
    house=defilers,
    defaults={
        "description": "The angels of transfiguration reveal themselves as luminescent figures devoid of identifying feature or expression, haunting in their silence and deliberate grace. Their entire body is a mirror reflecting the moods and thoughts of those around them, shifting like quicksilver amid a riot of conflicting feelings and expressions."
    },
)[0]
mammetum.add_source("Demon: The Fallen", 203)
mammetum.low_torment_traits.set(
    [
        trait_enhanced_empathy_defilers,
        trait_casts_no_reflection,
        trait_pass_without_trace,
        trait_improved_dexterity_defilers,
    ]
)
mammetum.high_torment_traits.set(
    [
        trait_claws_teeth,
        trait_improved_initiative,
        trait_venom_defilers,
        trait_extra_actions,
    ]
)

# DEVOURER VISAGES
# Zaltu, the Visage of the Beast
zaltu = Visage.objects.get_or_create(
    name="Zaltu",
    house=devourers,
    defaults={
        "description": "The angels of the hunt are fearsome in their strength and majesty, stalking invisibly through the darkness with panther-like strength and supple grace. The physical appearances of these fallen are many and varied, but most are powerfully muscled and covered in a pelt of fur, with large, golden eyes that glow like coals in the moonlight. They speak in a low, liquid rumble, and their howls chill the blood for miles when they hunt."
    },
)[0]
zaltu.add_source("Demon: The Fallen", 205)
zaltu.low_torment_traits.set(
    [
        trait_increased_size,
        trait_enhanced_senses,
        trait_claws_teeth,
        trait_extra_actions,
    ]
)
zaltu.high_torment_traits.set(
    [
        trait_thick_hide_devourers,
        trait_gaping_maw,
        trait_extra_limbs,
        trait_chameleon_skin_devourers,
    ]
)

# Ninurtu, the Visage of the Wild
ninurtu = Visage.objects.get_or_create(
    name="Ninurtu",
    house=devourers,
    defaults={
        "description": "The angels of the wilderness manifest as an amalgam of the flora they command and the fauna that thrive beneath their aegis. Their skin is commonly covered by a fine pelt similar to a deer's, and they often possess hooves instead of feet. Their bodies are powerfully muscled, and their eyes change colors like the seasons, ranging from pale gray to deep summer green."
    },
)[0]
ninurtu.add_source("Demon: The Fallen", 207)
ninurtu.low_torment_traits.set(
    [
        trait_enhanced_senses,
        trait_chameleon_skin_devourers,
        trait_pass_without_trace,
        trait_extra_health_levels,
    ]
)
ninurtu.high_torment_traits.set(
    [
        trait_thorns_devourers,
        trait_increased_size,
        trait_extra_limbs,
        trait_toxins_devourers,
    ]
)

# Aruru, the Visage of Flesh
aruru = Visage.objects.get_or_create(
    name="Aruru",
    house=devourers,
    defaults={
        "description": "The angels of the flesh, who can alter their forms more completely than even the Defilers, manifest themselves as idealized versions of their own mortal forms. Their power exalts the mortal shells that they inhabit, removing any blemishes or deformities and refining their original features to perfection. In a way, this makes their appearance just as alien and wondrous as the shimmering apparitions of their Celestial kin."
    },
)[0]
aruru.add_source("Demon: The Fallen", 209)
aruru.low_torment_traits.set(
    [
        trait_enhanced_social_traits_devourers,
        trait_immune_to_poisons_devourers,
        trait_improved_initiative,
        trait_casts_no_reflection,
    ]
)
aruru.high_torment_traits.set(
    [
        trait_extra_health_levels,
        trait_armor,
        trait_gaping_maw,
        trait_regeneration,
    ]
)

# SLAYER VISAGES
# Namtar, the Visage of Death
namtar = Visage.objects.get_or_create(
    name="Namtar",
    house=slayers,
    defaults={
        "description": "These angels manifest as shadowy figures wreathed in tendrils of ghostly mist that shift and writhe from moment to moment, occasionally reflecting the angels' thoughts in strange, symbolic forms. A pall of silence surrounds these figures, and their feet never seem to touch the ground. Their skin is as pale as alabaster, and their faces are constantly hidden in deep shadow."
    },
)[0]
namtar.add_source("Demon: The Fallen", 211)
namtar.low_torment_traits.set(
    [
        trait_wings,
        trait_improved_initiative,
        trait_pass_without_trace,
        trait_casts_no_reflection,
    ]
)
namtar.high_torment_traits.set(
    [
        trait_cloak_of_shadows_slayers,
        trait_death_grip_slayers,
        trait_aura_of_entropy_slayers,
        trait_damage_resistance,
    ]
)

# Nergal, the Visage of the Spirit
nergal = Visage.objects.get_or_create(
    name="Nergal",
    house=slayers,
    defaults={
        "description": "The angels of the spirit world appear as pale, serene figures reminiscent of the images of human saints, beautiful, silent and remote. Like others of their House, the Nergal move without noise or effort, seeming to glide along the ground as they move. Only their eyes, colored in shifting patterns of gray and black, hint at the bleak world beyond the mortal realm."
    },
)[0]
nergal.add_source("Demon: The Fallen", 213)
nergal.low_torment_traits.set(
    [
        trait_ghost_sight_slayers,
        trait_enhanced_social_traits_slayers,
        trait_pass_without_trace,
        trait_wings,
    ]
)
nergal.high_torment_traits.set(
    [
        trait_cloak_of_shadows_slayers,
        trait_howl_of_the_damned_slayers,
        trait_aura_of_dread_slayers,
        trait_damage_resistance,
    ]
)

# Ereshkigal, the Visage of the Realms
ereshkigal = Visage.objects.get_or_create(
    name="Ereshkigal",
    house=slayers,
    defaults={
        "description": "Angels of the Second World manifest as shadowy figures whose features are hidden in perpetual darkness. The air itself seems to wrap about them like a robe of night, conjuring the image of the cowled ferryman of human myth. Their hands are white and bony, like a skeleton's, and they move without effort or sound."
    },
)[0]
ereshkigal.add_source("Demon: The Fallen", 215)
ereshkigal.low_torment_traits.set(
    [
        trait_dead_reckoning_slayers,
        trait_pass_without_trace,
        trait_enhanced_awareness_slayers,
        trait_conjure_from_nothing_slayers,
    ]
)
ereshkigal.high_torment_traits.set(
    [
        trait_cloak_of_shadows_slayers,
        trait_relentless_slayers,
        trait_voice_of_the_grave_slayers,
        trait_dread_gaze_slayers,
    ]
)

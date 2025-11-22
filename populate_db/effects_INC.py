# M20 Jumpstart Common Magickal Effects
from characters.models.mage.effect import Effect

effect_adapt_to_environment_self = Effect.objects.get_or_create(
    name="Adapt to Environment (Self)", life=2
)
effect_adapt_to_environment_other = Effect.objects.get_or_create(
    name="Adapt to Environment (Other)", life=3
)
effect_animate_corpse_or_parts = Effect.objects.get_or_create(
    name="Animate Corpse or Parts", life=2, prime=2
)
effect_cause_disease_self = Effect.objects.get_or_create(
    name="Cause Disease (Self)", life=2
)
effect_cure_disease_self = Effect.objects.get_or_create(
    name="Cure Disease (Self)", life=2
)
effect_cause_disease_other = Effect.objects.get_or_create(
    name="Cause Disease (Other)", life=3
)
effect_cure_disease_other = Effect.objects.get_or_create(
    name="Cure Disease (Other)", life=3
)
effect_cosmetic_alteration = Effect.objects.get_or_create(
    name="Cosmetic Alteration", life=3
)
effect_create_body_simple = Effect.objects.get_or_create(
    name="Create Body (Simple)", life=2, prime=2
)
effect_create_body_complex = Effect.objects.get_or_create(
    name="Create Body (Complex)", life=5, prime=2
)
effect_duplicate_body = Effect.objects.get_or_create(
    name="Duplicate Body", life=5, prime=2
)
effect_grow_new_limbs_or_other_features_self = Effect.objects.get_or_create(
    name="Grow New Limbs or Other Features (Self)", life=3
)
effect_grow_new_limbs_or_other_features_other = Effect.objects.get_or_create(
    name="Grow New Limbs or Other Features (Other)", life=4
)
effect_harm_living_being_simple = Effect.objects.get_or_create(
    name="Harm Living Being (Simple)", life=2
)
effect_heal_living_being_simple = Effect.objects.get_or_create(
    name="Heal Living Being (Simple)", life=2
)
effect_harm_living_being_complex = Effect.objects.get_or_create(
    name="Harm Living Being (Complex)", life=3
)
effect_heal_living_being_complex = Effect.objects.get_or_create(
    name="Heal Living Being (Complex)", life=3
)
effect_heal_fae = Effect.objects.get_or_create(name="Heal Fae", life=3, mind=3)
effect_harm_fae = Effect.objects.get_or_create(name="Harm Fae", life=3, mind=3)
effect_heal_vampire = Effect.objects.get_or_create(
    name="Heal Vampire", life=3, matter=2
)
effect_harm_vampire = Effect.objects.get_or_create(
    name="Harm Vampire", life=3, matter=2
)
effect_heal_werecreature = Effect.objects.get_or_create(
    name="Heal Werecreature", life=3, spirit=2
)
effect_harm_werecreature = Effect.objects.get_or_create(
    name="Harm Werecreature", life=3, spirit=2
)
effect_increase_physique_traits_self = Effect.objects.get_or_create(
    name="Increase Physique/Traits (Self)", life=3
)
effect_increase_physique_traits_other = Effect.objects.get_or_create(
    name="Increase Physique/Traits (Other)", life=4
)
effect_increase_speed = Effect.objects.get_or_create(name="Increase Speed", time=3)
effect_reduce_speed = Effect.objects.get_or_create(name="Reduce Speed", time=3)
effect_revive_recently_dead = Effect.objects.get_or_create(
    name="Revive Recently Dead", life=4, spirit=4, prime=3
)
effect_rot_body_entropy = Effect.objects.get_or_create(
    name="Rot Body (Entropy)", entropy=4
)
effect_rot_body_life = Effect.objects.get_or_create(name="Rot Body (Life)", life=4)
effect_shapeshift_self = Effect.objects.get_or_create(name="Shapeshift (Self)", life=4)
effect_shapeshift_other = Effect.objects.get_or_create(
    name="Shapeshift (Other)", life=5
)
effect_soak_aggravated_damage = Effect.objects.get_or_create(
    name="Soak Aggravated Damage", life=3
)
effect_transform_into_element_earth_metal_water = Effect.objects.get_or_create(
    name="Transform into Element (Earth, Metal, Water)", life=3, matter=3
)[0]
effect_transform_into_element_wood = Effect.objects.get_or_create(
    name="Transform into Element (Wood)", life=3
)
effect_transform_into_element_air_fire = Effect.objects.get_or_create(
    name="Transform into Element (Air, Fire)", life=3, forces=3
)
effect_alter_probability = Effect.objects.get_or_create(
    name="Alter Probability", entropy=2
)
effect_bless = Effect.objects.get_or_create(name="Bless", entropy=3, life=3)
effect_curse = Effect.objects.get_or_create(name="Curse", entropy=3, life=3)
effect_cause_decay = Effect.objects.get_or_create(name="Cause Decay", entropy=3)[
    0
]  # entropy 3+ variants
effect, _ = Effect.objects.get_or_create(name="Spot Flaws", entropy=1)
effect.description = "Basic Entropy senses allow the mage to find the most disordered point in a structure, effectively finding the weakest spot to attack it."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 192)
effect.add_source("Mage: The Ascension (Second Edition)", 193)
effect.add_source("Mage: The Ascension (Revised)", 162)
effect_call_storm = Effect.objects.get_or_create(name="Call Storm", forces=4, prime=2)
effect_conjure_element_fire_wind = Effect.objects.get_or_create(
    name="Conjure Element (Fire, Wind)", forces=3, prime=2
)
effect_conjure_element_earth_metal_water = Effect.objects.get_or_create(
    name="Conjure Element (Earth, Metal, Water)", matter=3, prime=2
)
effect_conjure_element_wood = Effect.objects.get_or_create(
    name="Conjure Element (Wood)", life=3, prime=2
)
effect_conjure_new_object = Effect.objects.get_or_create(
    name="Conjure New Object", matter=3, prime=2
)[
    0
]  # matter 3+ variants
Effect.objects.get_or_create(name='Conjure "Physical" Illusion', forces=2, prime=2)[
    0
]  # forces 2+ variants
effect_direct_existing_elements = Effect.objects.get_or_create(
    name="Direct Existing Elements", forces=2
)[
    0
]  # forces 2+ variants
effect_disintegrate_object_matter = Effect.objects.get_or_create(
    name="Disintegrate Object (Matter)", matter=3
)
effect_disintegrate_object_entropy_time = Effect.objects.get_or_create(
    name="Disintegrate Object (Entropy/Time)", entropy=3, time=3
)
effect_invisibility_field = Effect.objects.get_or_create(
    name="Invisibility Field", forces=2
)
effect_silence_field = Effect.objects.get_or_create(name="Silence Field", forces=2)
effect_invisibility_on_living_being = Effect.objects.get_or_create(
    name="Invisibility on Living Being", forces=2, life=2
)
effect_levitation_forces = Effect.objects.get_or_create(
    name="Levitation (Forces)", forces=2
)
effect_levitation_correspondence = Effect.objects.get_or_create(
    name="Levitation (Correspondence)", correspondence=3, matter=2
)
effect_flying_forces = Effect.objects.get_or_create(name="Flying (Forces)", forces=2)
effect_flying_correspondence = Effect.objects.get_or_create(
    name="Flying (Correspondence)", correspondence=3, life=2
)
effect_speed_velocity = Effect.objects.get_or_create(name="Speed Velocity", forces=2)[
    0
]  # forces 2+ variants
effect_slow_velocity = Effect.objects.get_or_create(name="Slow Velocity", forces=2)[
    0
]  # forces 2+ variants
effect_transform_objects = Effect.objects.get_or_create(
    name="Transform Objects", matter=2
)[
    0
]  # matter 2+ variants and other target thing spheres
effect_transform_forces = Effect.objects.get_or_create(
    name="Transform Forces", forces=3
)[
    0
]  # forces 3+ variants and other target thing spheres
effect, _ = Effect.objects.get_or_create(name="Astral Projection", mind=4)
effect.description = "Astral Projection releases the mage's mind, free of the body. When Astral Projecting, the mage can access the Astral Umbra. They can also move around the material world as an insubstantial being that can travel anywhere so long as they think about it."
effect.save()
effect.add_source("Dead Magic 2", 103)
effect.add_source("Mage: The Ascension (Revised)", 178)
effect_clairvoyance = Effect.objects.get_or_create(
    name="Clairvoyance", correspondence=2
)[
    0
]  # Mind 3/Corr 2 variant, why?
effect_conceal_aura_mind = Effect.objects.get_or_create(
    name="Conceal Aura (Mind)", mind=1
)
effect_conceal_aura_prime = Effect.objects.get_or_create(
    name="Conceal Aura (Prime)", mind=2
)
effect_alter_aura_mind = Effect.objects.get_or_create(name="Alter Aura (Mind)", mind=1)
effect_alter_aura_prime = Effect.objects.get_or_create(
    name="Alter Aura (Prime)", mind=2
)
effect_conceal_avatar = Effect.objects.get_or_create(
    name="Conceal Avatar", spirit=2, mind=1
)
effect_conceal_thoughts = Effect.objects.get_or_create(name="Conceal Thoughts", mind=1)
effect_conjure_mental_illusions = Effect.objects.get_or_create(
    name="Conjure Mental Illusions", mind=2
)[
    0
]  # Mind 2+ variants
effect_influence_mood = Effect.objects.get_or_create(name="Influence Mood", mind=2)
effect_influence_subconscious = Effect.objects.get_or_create(
    name="Influence Subconscious", mind=3
)[
    0
]  # Mind 3+ variants
effect_mind_control = Effect.objects.get_or_create(name="Mind Control", mind=4)
effect_prophecy = Effect.objects.get_or_create(name="Prophecy", time=2)[
    0
]  # why mind 2/time 2?
effect_hindsight = Effect.objects.get_or_create(name="Hindsight", time=2)[
    0
]  # why mind 2/time 2?
effect_scramble_thoughts = Effect.objects.get_or_create(
    name="Scramble Thoughts", mind=3
)
effect_see_through_another_s_eyes = Effect.objects.get_or_create(
    name="See Through Another's Eyes", mind=3
)
effect_sense_energies_correspondence = Effect.objects.get_or_create(
    name="Sense Energies (Correspondence)", correspondence=1
)
effect_sense_energies_time = Effect.objects.get_or_create(
    name="Sense Energies (Time)", time=1
)
effect_sense_energies_spirit = Effect.objects.get_or_create(
    name="Sense Energies (Spirit)", spirit=1
)
effect_sense_energies_matter = Effect.objects.get_or_create(
    name="Sense Energies (Matter)", matter=1
)
effect_sense_energies_forces = Effect.objects.get_or_create(
    name="Sense Energies (Forces)", forces=1
)
effect_sense_energies_life = Effect.objects.get_or_create(
    name="Sense Energies (Life)", life=1
)
effect_sense_energies_entropy = Effect.objects.get_or_create(
    name="Sense Energies (Entropy)", entropy=1
)
effect_sense_energies_mind = Effect.objects.get_or_create(
    name="Sense Energies (Mind)", mind=1
)
effect_sense_energies_prime = Effect.objects.get_or_create(
    name="Sense Energies (Prime)", prime=1
)
effect_share_perception = Effect.objects.get_or_create(name="Share Perception", mind=1)[
    0
]  # separate variants for other spheres?
effect_shield_mind_other = Effect.objects.get_or_create(
    name="Shield Mind (Other)", mind=2
)
effect_tear_mind_apart = Effect.objects.get_or_create(name="Tear Mind Apart", mind=3)
effect_tear_mind_apart_aggravated = Effect.objects.get_or_create(
    name="Tear Mind Apart (Aggravated)", mind=3, life=3
)
effect, _ = Effect.objects.get_or_create(name="Telepathy", mind=3)
effect.description = (
    "The mage is able to communicate directly with the target, mind-to-mind."
)
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 206)
effect.add_source("Mage: The Ascension (Second Edition)", 210)
effect.add_source("Mage: The Ascension (Revised)", 178)
effect_telekinesis = Effect.objects.get_or_create(name="Telekinesis", forces=2)[
    0
]  # forces 2+ variants
effect_translate_languages = Effect.objects.get_or_create(
    name="Translate Languages", mind=3
)
effect_translate_languages_group = Effect.objects.get_or_create(
    name="Translate Languages (Group)", mind=3, forces=2
)
effect_absorb_quintessence = Effect.objects.get_or_create(
    name="Absorb Quintessence", prime=3
)
effect_channel_quintessence = Effect.objects.get_or_create(
    name="Channel Quintessence", prime=3
)
effect_destroy_by_draining_quintessence_object = Effect.objects.get_or_create(
    name="Destroy by Draining Quintessence (Object)", prime=4
)
effect_destroy_by_draining_quintessence_creature = Effect.objects.get_or_create(
    name="Destroy by Draining Quintessence (Creature)", prime=5
)
effect_drain_node = Effect.objects.get_or_create(name="Drain Node", prime=4)
effect_drain_quintessence = Effect.objects.get_or_create(
    name="Drain Quintessence", prime=3
)
effect_fuel_new_pattern = Effect.objects.get_or_create(
    name="Fuel New Pattern", prime=2
)[
    0
]  # variants add appropriate spheres
effect_share_exchange_quintessence = Effect.objects.get_or_create(
    name="Share/Exchange Quintessence", prime=3
)
effect_command_spirit = Effect.objects.get_or_create(
    name="Command Spirit", mind=4, spirit=4
)
effect_conjure_spirit = Effect.objects.get_or_create(name="Conjure Spirit", spirit=3)
effect_drain_spirit_s_essence = Effect.objects.get_or_create(
    name="Drain Spirit's Essence", prime=4, spirit=4
)
effect_harm_spirit_wraith = Effect.objects.get_or_create(
    name="Harm Spirit/Wraith", spirit=3
)
effect_open_gateway = Effect.objects.get_or_create(name="Open Gateway", spirit=4)
effect_close_gateway = Effect.objects.get_or_create(name="Close Gateway", spirit=4)
effect_see_spirits = Effect.objects.get_or_create(name="See Spirits", spirit=1)
effect_speak_to_spirits = Effect.objects.get_or_create(
    name="Speak to Spirits", spirit=2
)
effect_step_sideways = Effect.objects.get_or_create(name="Step Sideways", spirit=3)
effect_touch_spirit = Effect.objects.get_or_create(name="Touch Spirit", spirit=2)
effect_affect_distant_object_being = Effect.objects.get_or_create(
    name="Affect Distant Object/Being", correspondence=2
)[
    0
]  # Correspondence 2+ variants
effect_aging_living_being = Effect.objects.get_or_create(
    name="Aging (Living Being)", time=3, life=4
)[
    0
]  # Time 3+ variants
effect_reversing_age_living_being = Effect.objects.get_or_create(
    name="Reversing Age (Living Being)", time=3, life=4
)[
    0
]  # Time 3+ variants
effect_aging_object = Effect.objects.get_or_create(
    name="Aging (Object)", time=3, matter=2
)[
    0
]  # Time 3+ variants
effect_reversing_age_object = Effect.objects.get_or_create(
    name="Reversing Age (Object)", time=3, matter=2
)[
    0
]  # Time 3+ variants
effect_conjure_earthly_being = Effect.objects.get_or_create(
    name="Conjure Earthly Being", correspondence=4, life=2
)
effect_create_multiple_images_correspondence = Effect.objects.get_or_create(
    name="Create Multiple Images (Correspondence)", correspondence=3, prime=2
)[0]
effect_create_multiple_images_forces = Effect.objects.get_or_create(
    name="Create Multiple Images (Forces)", forces=2, prime=2
)[
    0
]  # forces 2+ variants
effect_create_multiple_objects = Effect.objects.get_or_create(
    name="Create Multiple Objects", correspondence=5, matter=3, prime=2
)[0]
effect_open_gateway_between_locations = Effect.objects.get_or_create(
    name="Open Gateway Between Locations", correspondence=4
)
effect_rewind_time = Effect.objects.get_or_create(name="Rewind Time", time=3)
effect_set_time_trigger = Effect.objects.get_or_create(name="Set Time Trigger", time=4)
effect_teleport_self = Effect.objects.get_or_create(
    name="Teleport (Self)", correspondence=3
)
effect_teleport_other = Effect.objects.get_or_create(
    name="Teleport (Other)", correspondence=4
)
effect_time_travel = Effect.objects.get_or_create(name="Time Travel", time=5)

# M20 Effects
effect_bullet_catch = Effect.objects.get_or_create(
    name="Bullet-Catch", time=3, forces=2, life=2
)
effect_astral_sojourn = Effect.objects.get_or_create(
    name="Astral Sojourn", mind=4, spirit=3, prime=2
)
effect_agama_re = Effect.objects.get_or_create(
    name="Agama Re", entropy=4, life=2, spirit=3
)
effect_agama_te = Effect.objects.get_or_create(
    name="Agama Te", entropy=4, life=3, spirit=4
)
effect_astral_agama = Effect.objects.get_or_create(
    name="Astral Agama", entropy=5, mind=5, spirit=3
)
effect_suggest_sleep = Effect.objects.get_or_create(name="Suggest Sleep", mind=2)
effect_compel_sleep = Effect.objects.get_or_create(name="Compel Sleep", mind=4)
effect_make_tired = Effect.objects.get_or_create(name="Make Tired", life=3)
effect_create_wonder = Effect.objects.get_or_create(name="Create Wonder", prime=4)
effect_create_fetish_willing = Effect.objects.get_or_create(
    name="Create Fetish (Willing)", prime=4
)
effect_create_fetish_unwilling = Effect.objects.get_or_create(
    name="Create Fetish (Unwilling)", spirit=4
)
effect_create_periapt = Effect.objects.get_or_create(name="Create Periapt", matter=4)
effect_create_souflower = Effect.objects.get_or_create(
    name="Create Souflower", life=5, prime=3
)
effect_creat_trinket = Effect.objects.get_or_create(name="Creat Trinket", prime=2)
effect_mental_illusions_that_inflict_damage = Effect.objects.get_or_create(
    name="Mental Illusions that Inflict Damage", mind=3
)
effect_immersive_illusions = Effect.objects.get_or_create(
    name="Immersive Illusions", forces=4, mind=4, prime=4
)
effect_awaken_object_s_spirit = Effect.objects.get_or_create(
    name="Awaken Object's Spirit", spirit=3
)
effect_harm_ghost = Effect.objects.get_or_create(name="Harm Ghost", entropy=3, prime=2)
effect_perfect_object = Effect.objects.get_or_create(name="Perfect Object", matter=3)
effect_consecrate = Effect.objects.get_or_create(name="Consecrate", prime=2)
effect_ward_ban = Effect.objects.get_or_create(
    name="Ward/Ban", correspondence=2, prime=2
)[
    0
]  # Corr/PRime 2+ variant, plus appropriate spheres at 2+
effect_astral_body_of_light = Effect.objects.get_or_create(
    name="Astral Body of Light", mind=4, spirit=3, prime=2
)
effect_enter_a_dream = Effect.objects.get_or_create(name="Enter a Dream", mind=3)
effect_see_avatar = Effect.objects.get_or_create(
    name="See Avatar", mind=3, prime=2, spirit=1
)
effect_see_through_mental_illusions = Effect.objects.get_or_create(
    name="See Through Mental Illusions", mind=4
)
effect_shield_mind_self = Effect.objects.get_or_create(
    name="Shield Mind (Self)", mind=1
)
effect_create_new_node = Effect.objects.get_or_create(name="Create New Node", prime=5)
effect_create_quintessence_weapon = Effect.objects.get_or_create(
    name="Create Quintessence Weapon", prime=3
)
effect_employ_periapt = Effect.objects.get_or_create(name="Employ Periapt", prime=2)
effect_enchant_object = Effect.objects.get_or_create(name="Enchant Object", prime=2)
effect_energize_periapt = Effect.objects.get_or_create(name="Energize Periapt", prime=3)
effect_nullify_paradox = Effect.objects.get_or_create(name="Nullify Paradox", prime=5)
effect_refine_tass = Effect.objects.get_or_create(name="Refine Tass", prime=4)
effect_tap_wellspring = Effect.objects.get_or_create(name="Tap Wellspring", prime=4)
effect_body_of_light = Effect.objects.get_or_create(name="Body of Light", prime=2)

# How Do You DO That?
# Book of Secrets
effect_the_branding_effect = Effect.objects.get_or_create(
    name="The Branding Effect", spirit=3, life=3, mind=2, prime=3
)
effect_the_branding_effect_expirating = Effect.objects.get_or_create(
    name="The Branding Effect (Expirating)", spirit=3, life=3, mind=2, prime=3, time=4
)[0]
effect_the_branding_effect_avatar_brand = Effect.objects.get_or_create(
    name="The Branding Effect (Avatar Brand)", spirit=4, life=3, mind=2, prime=3
)[0]
effect_the_branding_effect_glowing = Effect.objects.get_or_create(
    name="The Branding Effect (Glowing)", spirit=3, life=3, mind=2, prime=3, forces=3
)[0]

effect_gilgul = Effect.objects.get_or_create(
    name="Gilgul", spirit=5, entropy=5, mind=5, prime=5
)
effect_gilgul_aggravated_damage = Effect.objects.get_or_create(
    name="Gilgul (Aggravated Damage)", spirit=5, entropy=5, mind=5, prime=5, life=3
)[0]
effect_gilgul_body_to_dust = Effect.objects.get_or_create(
    name="Gilgul (Body to Dust)", spirit=5, entropy=5, mind=5, prime=5, life=5
)[0]
effect_gilgul_scattered_body_to_dust = Effect.objects.get_or_create(
    name="Gilgul (Scattered Body to Dust)",
    spirit=5,
    entropy=5,
    mind=5,
    prime=5,
    life=5,
    forces=3,
    correspondence=5,
)[0]

# Gods and Monsters
# Book of the Fallen
# Technocracy: Reloaded
# Rich Bastard's Guide to Magick
# T:R Quickstart
# Operative's Dossier
# Lore of the Traditions
# M20 Victorian Age
# Le Prix à Payer
# Rouen Brûle t elle

# Enlightend Grimoire
effect, _ = Effect.objects.get_or_create(name="Balance the Scales", matter=2, entropy=2)
effect.description = "With this, the Euthanatos can cause small accidents or fortunes, the Entropy 2 version works once, Entropy 3 lasts for a duration. The Pattern sphere dictates the sort of coincidences to occur."
effect.save()
effect.add_source("Tradition Book: Euthanatos", 67)
effect, _ = Effect.objects.get_or_create(name="Blight/Farmer's Favor", time=3, life=3)
effect.description = "This rote can be used to affect the state of crops or stored food. Life 3 and Time 3 accelerate either growth or decay of crops in the field, whereas Correspondence 2 and Matter 2 can preserve or destroy stored crops. Spirit can add an unpredictable element by requesting help from the local spirits with whichever version is being used, and Prime 2 preserves the soil from the rapid draw of nutrients."
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 271)
effect, _ = Effect.objects.get_or_create(
    name="Luck's Blessing/Curse", spirit=3, entropy=2
)
effect.description = "The shaman awakens the spirit of a location (size determines number of successes required) and leaves some kind of object or symbol for the spirit. This object causes the spirit to either help or hinder those who are there for the duration of the effect. For a longer duration, the spirit must be negotiated with directly."
effect.save()
effect.add_source("The Spirit Ways", 90)
effect, _ = Effect.objects.get_or_create(name="Luck of the Lotus", entropy=3, mind=2)
effect.description = "The Wu-Keng can paint pictures of people and their intentions for them, and in doing so twist their luck and grant them either a good feeling aura or a bad one. When the luck invoked is bad, this rote is called 'The Crippled Lotus Curse.'"
effect.save()
effect.add_source("Book of Crafts", 119)
effect, _ = Effect.objects.get_or_create(
    name="Nanburbu", correspondence=2, spirit=3, life=2, entropy=4, prime=3
)
effect.description = "This ritual doesn't read the omens like Adad, Istar, Samas, Sin and Anunnaku. Instead, it allows the mage to reduce the severity of bad fates. First, the mage and any assistants must seclude themselves from the world, either literally or symbolically (in a Magic Circle). Then, everyone involved must shave and wash while inhaling tamarisk incense to become pure. Then the leader sacrifices a goat and rings a copper bell. Finally, food and incense are offered to the gods as the participants request help preventing the omen from coming true."
effect.save()
effect.add_source("Dead Magic", 54)
effect, _ = Effect.objects.get_or_create(name="Threefold Return", time=4, entropy=4)
effect.description = "By creating a small charm to be worn or carried (most often a small mirror), the Verbena can bring the Law of Threefold Return on those they interact with. When expended, the person who acted towards the mage will receive a benefit or harm proportional to the number of successes on this effect."
effect.save()
effect.add_source("Tradition Book: Verbena", 68)
effect, _ = Effect.objects.get_or_create(name="Ansu Ishten", matter=3, entropy=3)
effect.description = "The mage invokes a protective god and then recites a list of the harms they want to protect an object or person from, in rhyming couplets. This list is quite specific, and every harm must be fully mundane. Each success adds one to the difficulty of attempts to cause the fates on this list, but there is no protection whatsoever for harm not on this list."
effect.save()
effect.add_source("Dead Magic", 56)
effect, _ = Effect.objects.get_or_create(name="Banishing Blessing", entropy=2, mind=2)
effect.description = "With three successes lasting a day and further successes extending the duration, a mage can make someone go away. Something will come up in their lives that causes them to want to leave, whether it's a free vacation, a job opportunity, or long-lost relatives."
effect.save()
effect.add_source("Tradition Book: Verbena (First Edition)", 64)
effect.add_source("Tradition Book: Verbena (Revised)", 65)
effect, _ = Effect.objects.get_or_create(name="Baptism Rune", entropy=4)
effect.description = "This rune is used to bless a newborn child, ensuring that they do not die in combat, or at least, are less likely to."
effect.save()
effect.add_source("Dead Magic 2", 100)
effect, _ = Effect.objects.get_or_create(name="Beginner's Luck", entropy=2)
effect.description = "The first time trying some feat, the mage gets automatic successes on their ability roll for each success on this rote."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 194)
effect.add_source("Mage: The Ascension (Revised)", 163)
effect, _ = Effect.objects.get_or_create(
    name="Bless the Heavenly Flower", spirit=4, life=4, entropy=5
)
effect.description = "The Wu-Keng are tightly bound to the families in the communities they serve. By entering a deep trance, the mage may travel to the Heavenly Flower Garden and cultivate the flowers of benevolence for the family of a ghost. Once they have bloomed sufficiently, that family will give birth to a baby for whom that ghost will act as a guardian. In extreme cases, that baby will in fact be that ghost reborn."
effect.save()
effect.add_source("Dragons of the East", 68)
effect, _ = Effect.objects.get_or_create(
    name="Bum a Dollar From the Universe", matter=2, entropy=2
)
effect.description = "The Hollow One who uses this rote will just happen to come across money. Not a lot of it, but just enough for what they need."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 61)
effect, _ = Effect.objects.get_or_create(name="Buzzwords", entropy=3, mind=2)
effect.description = "Using corporate and business buzzwords, the Technocrat can add successes to a roll related to the success of a business enterprise."
effect.save()
effect.add_source("Guide to the Technocracy", 209)
effect, _ = Effect.objects.get_or_create(
    name="Caesar's Due", correspondence=3, entropy=2, prime=2
)
effect.description = "It's a rare thing for a Hermetic to be able to hold down a day job, so they tend to come up with creative ways to pay the bills. The Hermetic sets up a circle of seven bank cards (that don't need to be active or even theirs), with Enochian sigils inscribed on them, and puts their monthly bills in the center. Prime creates an aetheric matrix for insubstantial things to pass through (namely electronic money), and then Correspondence covers an area for Entropy to move the money around in. The Forces 3 version is more brute force, and directly sends signals that the bills have been paid. It is much riskier, but possible, to use this to make money rather than just to pay bills."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="Epiphany of the Muse", mind=2)
effect.description = "This is a formal prayer to the Muses for inspiration. By sacrificing something of value to them, good, jewelry, an artifact, the mage is gifted with insight. Mind 2 is essential, but Spirit 2 gains the insight from a spirit, Prime 1 helps create a thought from nothing, and with Entropy the mage lucks into it."
effect.save()
effect.add_source("Dead Magic", 105)
effect, _ = Effect.objects.get_or_create(name="Games of Luck", entropy=2)
effect.description = "This rote can be used to influence the outcome of a game of chance, the mage getting more exactly the outcome they want with more successes."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 192)
effect.add_source("Technocracy: Syndicate", 47)
effect.add_source("Mage: The Ascension (Second Edition)", 194)
effect.add_source("Mage: The Ascension (Revised)", 163)
effect, _ = Effect.objects.get_or_create(
    name="Luck Be a Lady Tonight", spirit=2, entropy=1
)
effect.description = "Summons a spirit of luck to assist the mage."
effect.save()
effect.add_source("Fallen Tower: Las Vegas", 120)
effect, _ = Effect.objects.get_or_create(name="Masquerade to Adulthood", spirit=3)
effect.description = "A coming-of-age ritual that allows the mage to keep the initiation involved a secret from spiritual eavesdroppers or weakens the ties of the subject to things connected to their childhood."
effect.save()
effect.add_source("Dead Magic", 29)
effect, _ = Effect.objects.get_or_create(name="Midwife's Blessing", entropy=4)
effect.description = "Only able to be used on a pregnant woman or a newborn, this rote grants the child an easier life, preventing misfortunes and causing good luck to follow them. This can incline the child towards specific, beneficial Resonance, prevent birth defects or fatal diseases, and other benefits, though they can't be specified precisely, only in general terms."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 195)
effect.add_source("Mage: The Ascension (Revised)", 164)
effect, _ = Effect.objects.get_or_create(
    name="Nobody Dies in Vegas", correspondence=4, entropy=4
)
effect.description = "There is an unspoken rule that any trouble stays out of Las Vegas to avoid disrupting business. So, if a mage is actively leaving Las Vegas, this rote gives a +1 penalty to difficulty per success to all attempts to stop them from escaping. This protection lasts until the user escapes from the geographic boundary that is important to their pursuit, whether it be the city limits, the county line or the state of Nevada."
effect.save()
effect.add_source("Fallen Tower: Las Vegas", 119)
effect, _ = Effect.objects.get_or_create(name="Reflecting Bane", spirit=3)
effect.description = "With a proper reflective surface, a malevolent spirit can be tricked into looking at its reflection, scaring it off. This effect can also reflect malignant thoughts with Mind. With Life, in addition to being a guard against evil influence, the subject's healing is accelerated."
effect.save()
effect.add_source("Dead Magic", 30)
effect, _ = Effect.objects.get_or_create(name="Shishipat's Favor", life=1)
effect.description = "By eating goose boiled in caribou fat, the mage ensures that the subject will have a successful hunt, giving decreased difficulty to their next Survival or Athletics rolls for the duration of their next hunt."
effect.save()
effect.add_source("Dead Magic", 132)
effect, _ = Effect.objects.get_or_create(name="Waiting to Exhale", spirit=2, entropy=3)
effect.description = "A group of women contribute blood to this ritual. The mage then offers the blood to the gods as a burnt offering, and in exchange the gods protect the women's homes, preventing misfortunes. One specific effect is that harmful Coincidental Entropy effects are at higher difficulty."
effect.save()
effect.add_source("Dead Magic", 77)
effect, _ = Effect.objects.get_or_create(name="Weeping for Tammuz", entropy=3)
effect.description = "The Babylonians have a story about the goddess Ereshkigal who fell in love with a mortal named Tammuz. When the mortal died, she sacrificed herself, staying in the underworld, that he could live, and eventually a bargain was struck where Tammuz's sister would take his place for half the year. By making this sacrifice, and by making symbolic sacrifices of a similar nature, the priests of Babylon were able to guarantee good fortune. This rote allows the mage to burn an object of personal significance (or a person) and in exchange adds automatic successes to a task in the future."
effect.save()
effect.add_source("Dead Magic", 52)
effect, _ = Effect.objects.get_or_create(name="Wurnan Blessing", spirit=2, entropy=2)
effect.description = "This rote is used by the Law Woman of an Aboriginal tribe on a new baby. It briefly connects the child to the inter-relationship between all members of the tribe and ensures that minor accidents are avoided during the first days of the baby's life."
effect.save()
effect.add_source("Dead Magic 2", 66)
effect, _ = Effect.objects.get_or_create(name="Ace of Diamonds", entropy=3, prime=1)
effect.description = "Largely regarded as an unlucky card, Ace of Diamonds allows a Technocrat to cause their target to become extremely unlucky. This is so severe that for every two successes, the target loses on success for all rolls for the duration of the effect."
effect.save()
effect.add_source("Guide to the Technocracy", 209)
effect, _ = Effect.objects.get_or_create(name="Actively Actuarial", entropy=2)
effect.description = "Like Beginner's Luck, it causes unlikely events to happen. While Beginner's Luck applies to a single action of the user, this causes an unlikely but bad fate to befall the chosen target. More successes (minimum 1, maximum 20) are required for both the severity of the event and the unlikeliness."
effect.save()
effect.add_source("Guide to the Technocracy", 208)
effect, _ = Effect.objects.get_or_create(name="Death Curse", spirit=2, life=3)
effect.description = "The shaman conducts a ritual to cause harm to a target. When finished, the target experiences a serious illness, which may be as quick as a sudden heart attack or as slow as a wasting fever. The shaman needs at least the target's Stamina + Health levels successes. Correspondence is needed unless they directly confront the target."
effect.save()
effect.add_source("The Spirit Ways", 90)
effect, _ = Effect.objects.get_or_create(name="Death Wish", correspondence=2, life=2)
effect.description = "The most basic version causes things to go wrong, giving the victim bad luck. The second version is much deadlier and causes aggravated damage via Life to the target according to what is most appropriate for the caster. The Correspondence 2/Life 3/Entropy 3 variant combines the two effects. The deadliest version is the final one, which causes the victim to burst into flames."
effect.save()
effect.add_source("Orphan's Survival Guide", 127)
effect, _ = Effect.objects.get_or_create(
    name="Learn-It", correspondence=2, time=2, entropy=2, prime=3
)
effect.description = "An instructional rote, of sorts, it's also a stealth weapon against the Technocracy. The Virtual Adept using it tags the target and this causes enemies and challenges 'appropriate to the target's current power level.' Every success causes the target to become a magnet for one skill-appropriate challenge per session. This number can be modified by the original user, or by someone with Prime 2, though they cannot reduce it below one. To negate it completely requires Prime 3 and Entropy 3."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 62)
effect, _ = Effect.objects.get_or_create(
    name="Rival's Curse", correspondence=2, entropy=4
)
effect.description = "A long-distance Entropy-based attack on an enemy. This attack usually takes the form of such bad luck that it seems that everything is out to kill the target, doing damage based on the number of successes."
effect.save()
effect.add_source("Order of Reason", 108)
effect, _ = Effect.objects.get_or_create(
    name="Sha'ir's Sentence", life=2, entropy=3, mind=2
)
effect.description = "The Taftani first composes a poem about the target which evokes their weaknesses and then recites the poem at the target. This concludes with giving the target a nickname which captures these weaknesses. This rote then causes the nickname to stick and for it to become increasingly true over time. This can be very slow, often a gradual change over the course of years, but it can cause 'Camel Face' to lose Appearance and 'Stumblefoot' to lose Dexterity. The same technique works in the other direction: a poem highlighting strengths can emphasize strengths. Giving someone the title 'the Clever' can gain them Mental Attributes, for instance. A new nickname given with this rote will override an old one."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 90)
effect, _ = Effect.objects.get_or_create(name="Spoiling", life=2, entropy=2)
effect.description = "This rote brings bad luck to a target, and with Life that bad luck extends to their crops and livestock."
effect.save()
effect.add_source("Dead Magic 2", 128)
effect, _ = Effect.objects.get_or_create(name="Statistical Mechanics", entropy=2)
effect.description = "Iteration X's Statisticians have all sorts of statistics at their fingertips. With this procedure, by reminding the target of a fact regarding their action, they can shift the odds in their favor or against them."
effect.save()
effect.add_source("Technocracy: Iteration X", 47)
effect, _ = Effect.objects.get_or_create(name="Vext", time=3, entropy=2)
effect.description = "Used on enemies of the Hollow Ones (and NEVER on another Hollow One), this causes that target to have a series of minor setbacks and annoyances, just bad luck, for a number of days equal to the number of successes."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 64)
effect, _ = Effect.objects.get_or_create(
    name="Brand (the Rawhide Effect)", forces=2, entropy=2, prime=2
)
effect.description = "A method of branding a Digital Web icon so that the brand stays visible despite any changes of form. Adding Time guarantees that the Brand lasts until the punishment is over."
effect.save()
effect.add_source("Digital Web 2.0", 112)
effect, _ = Effect.objects.get_or_create(
    name="Create Virtual Object/Create Daemon", forces=3, prime=2
)
effect.description = "This rote can create an inanimate object inside the Digital Web. The advanced version, Create Daemon, allows the mage to create a simple AI rather than an inanimate object."
effect.save()
effect.add_source("Digital Web", 98)
effect.add_source("Digital Web", 99)
effect.add_source("Digital Web 2.0", 114)
effect, _ = Effect.objects.get_or_create(name="Digital Disruption", forces=2, prime=2)
effect.description = "A basic online attack rote. With just Forces and Prime, it will soft de-rez the target, with Entropy it will inflict a hard de-rez."
effect.save()
effect.add_source("Digital Web", 98)
effect.add_source("Digital Web 2.0", 112)
effect, _ = Effect.objects.get_or_create(name="Doe's Password", entropy=2, mind=3)
effect.description = "This rote uses Mind to link to a Restricted program and Entropy to find a way in, giving any mage access to Restricted sectors."
effect.save()
effect.add_source("Digital Web", 98)
effect, _ = Effect.objects.get_or_create(
    name="Encode", correspondence=2, life=2, prime=2
)
effect.description = (
    "This rote allows a Cyberpunk to store an object in virtual space for later use."
)
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 65)
effect, _ = Effect.objects.get_or_create(
    name="Energy Transformation", correspondence=1, life=4, forces=4
)
effect.description = "This allows a mage to physically enter the Digital Web."
effect.save()
effect.add_source("Digital Web", 98)
effect, _ = Effect.objects.get_or_create(name="Feedback", forces=2, mind=3)
effect.description = "For a user who is either using sensory immersion or astral immersion into the Digital Web, but not physical immersion, this rote creates a feedback loop to overload the target's equipment. The simplest form uses raw static information to create the loop and causes intense pain and disorientation (standard Mind sphere attack), whereas the more advanced Life-based version and Forces 3 version cause physical damage to the target."
effect.save()
effect.add_source("Digital Web 2.0", 115)
effect, _ = Effect.objects.get_or_create(
    name="FIRP", life=3, forces=3, entropy=4, mind=5, prime=2
)
effect.description = "FIRP, or Fractal Interference Removal Procedure, is one of the more brutal rotes that can be found among Digital Web users, it blasts energy or projectiles in a fractal pattern, fracturing the target's consciousness, scattering their icon and energy, and then using Life to bring the attack into the physical world. Effectively this causes a Chaos Dump, splitting the target's consciousness between their body and their broken icon, and largely considered a fate worse than death."
effect.save()
effect.add_source("Digital Web 2.0", 155)
effect, _ = Effect.objects.get_or_create(
    name="Fractal Encryption", forces=2, entropy=3, prime=2
)
effect.description = "This rote encrypts data as a three-dimensional fractal sculpture in the Digital Web. It can only be decrypted with the same rote. Failure on either the encryption or decryption side destroys the information."
effect.save()
effect.add_source("Digital Web 2.0", 115)
effect, _ = Effect.objects.get_or_create(name="Hardware Entry", correspondence=1)
effect.description = "With a VR Rig, allows the mage to enter the Digital Web with Sensory or Astral Immersion. Many mages still prefer to use this rote, but it is no longer necessary to use any magic for Sensory Immersion. It is necessary to couple this with Astral Projection to enter the Digital Web astrally."
effect.save()
effect.add_source("Digital Web", 98)
effect, _ = Effect.objects.get_or_create(
    name="Information Superhighway", correspondence=2, time=3
)
effect.description = "Using this, the mage can travel more quickly along routes within the Digital Web, with Time speeding up time around them and Correspondence allowing them to follow the natural conduits and routes."
effect.save()
effect.add_source("Digital Web", 99)
effect, _ = Effect.objects.get_or_create(
    name="Instant Offline", correspondence=3, forces=2
)
effect.description = "Soft de-razzes the user, getting them out of the Digital Web instantly. Usually, this is used as a sort of 'panic button.'"
effect.save()
effect.add_source("Digital Web", 98)
effect.add_source("Digital Web 2.0", 115)
effect, _ = Effect.objects.get_or_create(
    name="Online Virus Transmitter Program", correspondence=2, life=2, forces=2, prime=2
)
effect.description = "This rote allows a mage to craft a virus that infects another user's icon and then uses that connection to infect the user with a disease."
effect.save()
effect.add_source("Digital Web 2.0", 112)
effect, _ = Effect.objects.get_or_create(name="Overwrite", forces=3, entropy=3, prime=4)
effect.description = "The rote permits the mage to alter parameters and is always vulgar as it involves pushing against the nature of the Digital Web itself. Five successes are necessary to fully remove a parameter."
effect.save()
effect.add_source("Digital Web", 99)
effect, _ = Effect.objects.get_or_create(
    name="Parallax", correspondence=4, forces=2, mind=1
)
effect.description = "Powerful Virtual Adepts often need to be in multiple places at once, and when online, this rote handle that. The digital version of Polyappearance, with Forces 2 and Mind 1 added in the mage can not only be in several places simultaneously but can act independently in each of them."
effect.save()
effect.add_source("Digital Web 2.0", 115)
effect, _ = Effect.objects.get_or_create(name="Restrict Sector", mind=4, prime=3)
effect.description = "This permanently seals off a sector as Restricted. When used, the mage chooses some parameters that determine who can enter, and the restrictions last until destroyed."
effect.save()
effect.add_source("Digital Web", 99)
effect, _ = Effect.objects.get_or_create(
    name="TechnoVision", correspondence=1, forces=1, entropy=1, mind=1, prime=1
)
effect.description = "Pulling up a readout window, the Digital Web user has a running basic analysis and scan of their surroundings."
effect.save()
effect.add_source("Digital Web", 98)
effect.add_source("Digital Web 2.0", 112)
effect, _ = Effect.objects.get_or_create(
    name="Virtual Talisman Transmogrification", matter=3, forces=2, prime=3
)
effect.description = "This allows the mage to transfer a Talisman into the Digital Web just as a person can physically enter it."
effect.save()
effect.add_source("Digital Web", 98)
effect, _ = Effect.objects.get_or_create(
    name="Webcrawlers", correspondence=3, forces=3, prime=2
)
effect.description = "Nexplorers use this rote to create energy-arachnids in virtual space that can follow simple commands. Most often, they act as information retrieval systems, or defensive walls of force. A Webcrawler is created with 3 health levels and the ability to follow simple commands. More successes create more Webcrawlers rather than more powerful ones. There is an alternate version of this rote using Spirit instead of Prime, which leads to speculation as to whether it is creating the Webcrawlers or calling them from another place."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 66)
effect, _ = Effect.objects.get_or_create(name="Boot Buzzer", correspondence=2, forces=2)
effect.description = "A Virtual Adept prank/attack rote, they can connect to any computer on a network they have access to and cause it to electrocute its user. With Forces 2, it takes time to build the charge and it is weaker, only doing one level of damage per success. With Forces 3/Prime 2, it builds instantly and causes normal damage."
effect.save()
effect.add_source("Hidden Lore", 20)
effect, _ = Effect.objects.get_or_create(name="Burn Out", forces=2, entropy=1)
effect.description = "This rote lets the mage fry circuitry by directing electricity at its weakest point, disabling mundane electronics easily. This is such a surgical strike, that it only disables the device for one turn per success, not permanently."
effect.save()
effect.add_source("Book of Shadows", 145)
effect, _ = Effect.objects.get_or_create(
    name="FOR NEXT Loop", correspondence=4, life=4, forces=2
)
effect.description = "This Virtual Adept technique converts the target to energy and puts them into a computer and then breaks them by pushing them through various circuit boards. The victim rolls Willpower (difficulty 10-Intelligence) to escape. Each success causes the victim to lose a point of Willpower, but a failure gives them another chance to escape."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 220)
effect, _ = Effect.objects.get_or_create(
    name="Red Button", forces=3, entropy=3, prime=2
)
effect.description = "When raiding the laboratories of rogue Technomages, this allows the New World Order to find the weaknesses in their machinery and use them to destroy the equipment."
effect.save()
effect.add_source("Technocracy: New World Order", 49)
effect, _ = Effect.objects.get_or_create(
    name="System Crash", correspondence=2, forces=2, prime=2
)
effect.description = "A mage who is on the Digital Web can crash a Sleeper system. Successes go towards defeating security and the size of the system."
effect.save()
effect.add_source("Digital Web 2.0", 113)
effect, _ = Effect.objects.get_or_create(name="System Havoc", forces=2)
effect.description = "This rote causes a spike of electrical energy into a system, causing electronics that aren't properly shielded to fry."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 195)
effect.add_source("Mage: The Ascension (Second Edition)", 198)
effect, _ = Effect.objects.get_or_create(
    name="That Rascal Puff", correspondence=2, life=3, forces=3, prime=2
)
effect.description = "A Marauder encountered by Dante detonated a room full of computers by breathing fire on one after connecting them. Correspondence links them, and Life allows the Marauder to breathe the fireball from Forces 3 and Prime 2, which travels through the connection causing a larger detonation."
effect.save()
effect.add_source("Hidden Lore", 51)
effect, _ = Effect.objects.get_or_create(
    name="Black Card/Little Black Box", correspondence=2, forces=2, mind=2
)
effect.description = "Using some kind of black box or security card, the mage can attempt to hack a system that they normally could never reach. The controls must be networked to the system they are attaching the box to."
effect.save()
effect.add_source("Mage: The Ascension 20th Anniversary Edition", 601)
effect, _ = Effect.objects.get_or_create(name="Captain's Treasure", entropy=2, prime=4)
effect.description = "The mage locates a conduit containing financial data (usually near a Syndicate sector) and shifts it so that the streams pass through the mage's accounts on the way to their primary goal. Entropy prevents accounting programs from noticing as money is skimmed from the stream."
effect.save()
effect.add_source("Digital Web", 99)
effect, _ = Effect.objects.get_or_create(
    name="Core Dump", correspondence=2, time=2, forces=3
)
effect.description = "This allows the Virtual Adept to load a massive amount of useless data into a computer via Forces or a person via Mind. This overwhelms them to the point where they are unable to initiate an action for three rounds. If more successes than target's Willpower, the computer will crash, or the person will enter a temporary coma (they will recover after a successful Willpower roll, rolled once a day)."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 64)
effect, _ = Effect.objects.get_or_create(
    name="Disk-Doctor", forces=1, entropy=3, mind=2
)
effect.description = "This rote has been essential for maintaining the secrecy of the Knights Templar. With it, a Templar can scan any piece of computer storage media for given data and delete it."
effect.save()
effect.add_source("Book of Crafts", 103)
effect, _ = Effect.objects.get_or_create(name="DRM", correspondence=3, mind=1, prime=2)
effect.description = "Marks a piece of data with custom code as a booby trap. It pulls identifying information from an intruder and sends it to the Technocrat, as well as providing countermagick against attempts to obtain the data illegitimately."
effect.save()
effect.add_source("Convention Book: New World Order (Revised)", 85)
effect, _ = Effect.objects.get_or_create(name="Encrypt", time=3, forces=3)
effect.description = "This rote scrambles a person's (or computer's) memory so that if they are coerced to speak, they will respond only with nonsense. What they are doing is responding fully with everything they remember, but in a randomized configuration that makes no sense to outsiders. Every success on this effect decreases the opponent's Interrogation or Investigation skills by one, with Decrypt being the inverse effect which increases them."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 65)
effect, _ = Effect.objects.get_or_create(name="Graphic Transmission", mind=3)
effect.description = "A Virtual Adept illusion effect, it produces computer graphics, and then transmits them to the target's mind. The number of successes determines how complex the illusion is partial successes may look like CGI to the viewer."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 206)
effect.add_source("Mage: The Ascension (Second Edition)", 210)
effect, _ = Effect.objects.get_or_create(
    name="Hacker's Glance", correspondence=1, entropy=2
)
effect.description = "This rote analyzes massive amounts of data to increase the odds that the mage will find what they are looking for. Successes add to a subsequent data retrieval roll."
effect.save()
effect.add_source("Digital Web", 98)
effect, _ = Effect.objects.get_or_create(name="Intel", correspondence=3, mind=1)
effect.description = "Virtually every piece of information that anyone could want is stored on a computer somewhere. With this procedure, a Technocrat can find and download the information that they seek. More difficult and better hidden information requires more successes."
effect.save()
effect.add_source("Guide to the Technocracy", 206)
effect, _ = Effect.objects.get_or_create(
    name="Mental Interface", correspondence=2, forces=2, mind=2
)
effect.description = "This rote allows the Virtual Adept to use their computer to see what is being actively done on another. This rote doesn't allow the mage to control the system."
effect.save()
effect.add_source("Hidden Lore", 19)
effect, _ = Effect.objects.get_or_create(
    name="Remote Access", correspondence=2, forces=2
)
effect.description = "Allows the mage to access a network from a distance."
effect.save()
effect.add_source("Digital Web 2.0", 113)
effect, _ = Effect.objects.get_or_create(
    name="Virtual Lockpick", correspondence=1, time=3, forces=2, mind=1
)
effect.description = "This rote compresses time inside the computer and makes many, many educated guesses about what the password may be. To use this, the mage needs to already know a login ID."
effect.save()
effect.add_source("Digital Web", 99)
effect, _ = Effect.objects.get_or_create(name="AI (Artificial Intelligence)", mind=5)
effect.description = "With this rote, a Technomage can create a full artificial intelligence. It can live in a computer, be transferred to the Digital Web or, with Life, given a living body. The AI will have a personality and is capable of growing and changing over time. The most powerful computers tend to have AIs but they come with a risk. They can develop complex relationships with their users, ranging all the way from hate to love...and there is no consensus of which of the two is more dangerous: a spurned AI lover is the sort of thing that Virtual Adepts have nightmares about."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 211)
effect, _ = Effect.objects.get_or_create(
    name="Audience of Inanna", correspondence=2, time=1, matter=2
)
effect.description = "Originally used to prevent impotence by placing a figurine of Inanna, a fertility goddess, at the head of a bed, Virtual Adepts have adapted it to avoid obsolescence: old hardware can run as effectively as new, and with enough successes, can convert a laptop into a supercomputer."
effect.save()
effect.add_source("Dead Magic", 57)
effect, _ = Effect.objects.get_or_create(
    name="Personal Assistant Software", mind=5, prime=2
)
effect.description = "This procedure creates a digital assistant based on the Technocrat's personality. The assistant controls their phone or computer's operation, assisting the agent in using it efficiently."
effect.save()
effect.add_source("Convention Book: New World Order (Revised)", 86)
effect, _ = Effect.objects.get_or_create(
    name="Psychic Interface", correspondence=2, forces=2, mind=3
)
effect.description = "In short, this effect allows a mage to access their computers remotely, directly from their minds. When this is active, meditation may be used in place of computers and IT gear as an instrument. This often still involves some sort of technological instrument, such as implants, glass-tech or the like, though those with cybernetics can work directly."
effect.save()
effect.add_source("Mage: The Ascension 20th Anniversary Edition", 608)
effect, _ = Effect.objects.get_or_create(name="Remote Programming", forces=2)
effect.description = "It can be far more efficient to program a computer or a robot directly, rather than via a keyboard. An Iterator with mental implants can use this procedure to directly connect their implants to the target and program it directly. To do so from far away, however, requires Correspondence."
effect.save()
effect.add_source("Technocracy: Iteration X", 47)
effect, _ = Effect.objects.get_or_create(
    name="Book of Whispers", time=3, matter=3, mind=2
)
effect.description = "A common rote among the Bonisagus, this rote binds a blank book to a person. Then, the book fills with the person's surface thoughts. The book must be in the subject's immediate vicinity to work, but it doesn't need to be obvious (it may be disguised among other books)."
effect.save()
effect.add_source("Blood Treachery", 88)
effect, _ = Effect.objects.get_or_create(name="Crowd Surfing", mind=4)
effect.description = "In a large crowd interacting with each other, like at a concert or a party, the Hollow One can erect a facade of coolness and mingle, and come away with a sense of who's who, who feels what for whom, and the like."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 62)
effect, _ = Effect.objects.get_or_create(
    name="Eavesdropper", correspondence=2, forces=2
)
effect.description = "A Technomage using this rote picks up a phone, dials a long sequence of digits, and can listen in on anything said near another working telephone."
effect.save()
effect.add_source("Hidden Lore", 19)
effect, _ = Effect.objects.get_or_create(
    name="High-Definition", correspondence=2, mind=2
)
effect.description = "By accessing a communication line, generally cable TV or Internet, this allows the Agent to see through any modern (LCD, plasma, etc.) television."
effect.save()
effect.add_source("Convention Book: New World Order (Revised)", 85)
effect, _ = Effect.objects.get_or_create(name="Monitor Communications", forces=1)
effect.description = "The New World Order's Watchers use this effect to spy on electronic communications. It is still defeated by encryption, but any open electronic communication can be eavesdropped upon with this procedure."
effect.save()
effect.add_source("Technocracy: New World Order", 45)
effect, _ = Effect.objects.get_or_create(
    name="Nearest and Dearest", correspondence=2, time=2, mind=3
)
effect.description = "By going through a wallet or a database, a Syndicate Enforcer can find out detailed information about their target's family and loved ones."
effect.save()
effect.add_source("Hidden Lore", 54)
effect, _ = Effect.objects.get_or_create(name="Phone Tap", correspondence=2, forces=2)
effect.description = "The New World Order is skilled in communication and can both send secure messages and intercept the messages of others with this procedure."
effect.save()
effect.add_source("Technocracy: New World Order", 49)
effect, _ = Effect.objects.get_or_create(
    name="PIN Drop", correspondence=2, time=2, forces=2, mind=2
)
effect.description = "By hacking an ATM or similar device, a Syndicate Agent can acquire a target's personal identification number, and use it to obtain all linked information, usually including social security number, address, bank account numbers, etc."
effect.save()
effect.add_source("Technocracy: Syndicate", 47)
effect, _ = Effect.objects.get_or_create(
    name="Squaring the Circle", correspondence=2, mind=1
)
effect.description = "A mage can use this rote to spy on conversations occurring in a place where the mage cannot go. Correspondence is used to access the location and Mind to discern the conversations. It is more difficult depending on how vigilant against spies the targets are."
effect.save()
effect.add_source("Order of Reason", 88)
effect, _ = Effect.objects.get_or_create(name="Surveillance", correspondence=2)
effect.description = "A Technocrat can use this procedure to access the feed from any video camera, microphone or other device that can pick up a signal. With Forces, the end-device is unnecessary, as variations in energy can be detected directly."
effect.save()
effect.add_source("Guide to the Technocracy", 204)
effect, _ = Effect.objects.get_or_create(name="Telescreen", correspondence=2, mind=2)
effect.description = "The New World Order is quite adept at watching people through their television screens. With this Procedure, they can not only do that, but if they have more successes than the target's Willpower, they can analyze psychic defenses."
effect.save()
effect.add_source("Guide to the Technocracy", 205)
effect, _ = Effect.objects.get_or_create(name="Tracking Device", correspondence=2)
effect.description = "Marks an object so that it can be detected and found later, particularly useful if the Agent can arrange for it to be picked up by someone they want to track."
effect.save()
effect.add_source("Guide to the Technocracy", 205)
effect, _ = Effect.objects.get_or_create(
    name="Adad", correspondence=2, spirit=1, entropy=2
)
effect.description = "By reading in the stars, Babylonian mages could determine the general fate of an area and the people within. Very detailed readings are almost impossible with this rote, but general things like 'prosperity' or even 'a break in the walls' for a major event can be determined with varying numbers of successes."
effect.save()
effect.add_source("Dead Magic", 53)
effect, _ = Effect.objects.get_or_create(
    name="Chaos Butterfly", spirit=2, entropy=2, prime=2
)
effect.description = "Houses Thig and Fortunae use this rote by inscribing a sigil and focusing their intent on some larger effect they wish to cause. This summons a minor Umbrood, a butterfly with wings of fire. The mage then must forget about the desired effect and let the butterfly flutter away. At some point in the future, likely in a very unexpected way, the effect that the mage desired comes to pass. In fact, this effect should always take the character (and the player) by surprise."
effect.save()
effect.add_source("Blood Treachery", 91)
effect, _ = Effect.objects.get_or_create(name="Contemplation", spirit=2)
effect.description = "Celestial Masters can gain insight from the stars, as they align with the world on the Spirit planes. This can give the user a vague insight, though never anything particularly big nor that circumvents an aspect of the story."
effect.save()
effect.add_source("Order of Reason", 84)
effect, _ = Effect.objects.get_or_create(name="Dogon Divination", time=2, entropy=1)
effect.description = "Like other forms of Time Sight, this variant allows the mage to perceive the patterns that are emerging, and which actions might prevent bad fates in the future, rather than seeing the future itself."
effect.save()
effect.add_source("Dead Magic", 27)
effect, _ = Effect.objects.get_or_create(
    name="Find the Lost", correspondence=1, entropy=2
)
effect.description = "Choristers often use this rote to find people who are troubled and in need of help. Correspondence 2 is needed if searching for someone beyond line of sight. Mind detects them based on their thoughts and emotions; Entropy manipulates luck to bring the mage to the person."
effect.save()
effect.add_source("Tradition Book: Celestial Chorus (Revised)", 57)
effect, _ = Effect.objects.get_or_create(
    name="Istar", correspondence=3, spirit=3, entropy=4
)
effect.description = "By reading the signs of Istar in the sky, the mage may gain insight into the fates of nations and their leaders. The results of reading these fates are very metaphorical and broad, rarely are individual events predicted, but the general sense of what will happen can be determined."
effect.save()
effect.add_source("Dead Magic", 54)
effect, _ = Effect.objects.get_or_create(
    name="Laying on of Hands", time=2, life=1, entropy=1
)
effect.description = "The mage touches the subject and can see which wounds they are likely to take during an upcoming battle. This is useful for attempting to avoid those wounds, with armor, magick or other means."
effect.save()
effect.add_source("Dead Magic 2", 102)
effect, _ = Effect.objects.get_or_create(name="Lighting the Path", correspondence=2)
effect.description = "A Chorister who seeks a specific person, place or thing uses the Correspondence version of this rote, where the number of successes determines how much detail they learn about the road to it. The Entropy version is useful for vague requests, such as when the character needs direction."
effect.save()
effect.add_source("Tradition Book: Celestial Chorus (Revised)", 58)
effect, _ = Effect.objects.get_or_create(name="Read the Lightning", time=2, forces=2)
effect.description = "Etruscan mages could read the future in the patterns of lightning strikes and thunderclaps. In fact, the mage calls down lightning to do so. This requires only Forces 2 in stormy weather, but Forces 4 can do it in any weather."
effect.save()
effect.add_source("Dead Magic 2", 143)
effect, _ = Effect.objects.get_or_create(name="Samas", correspondence=2, forces=2)
effect.description = "Samas is the sun, and its signs involve the path it takes through the sky, which changes every day. By reading these omens, the fates of crops, weather and other things that depend on the sun can be divined."
effect.save()
effect.add_source("Dead Magic", 54)
effect, _ = Effect.objects.get_or_create(
    name="Search Engine", correspondence=2, entropy=1, prime=1
)
effect.description = "This rote puts the Virtual Adept in touch with someone who matches their needs, or someone who knows someone who does. Each success gives a 20% chance of finding a person of the type they need."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 63)
effect, _ = Effect.objects.get_or_create(
    name="Silent Promise of the Spring Tortoise", entropy=1
)
effect.description = "By adopting a turtle and raising it for a week, and then boiling and eating it, a Wu-Keng may divine the odds of their next undertaking from the way the shell cracks."
effect.save()
effect.add_source("Book of Crafts", 119)
effect, _ = Effect.objects.get_or_create(name="Sin", spirit=2, entropy=2, prime=1)
effect.description = "Moon phases and paths are one of the most complex sets of omens that Babylonian mages had access to. The readings from Sin are as broad as those from Samas, though usually much more straightforward. With the greater version, huge changes and calamities can be predicted."
effect.save()
effect.add_source("Dead Magic", 54)
effect, _ = Effect.objects.get_or_create(
    name="Wyrd Visions", correspondence=2, time=2, entropy=1
)
effect.description = "The mage attunes themselves to the threads of fate, seeking an understanding of the past, present and future."
effect.save()
effect.add_source("Dead Magic 2", 102)
effect, _ = Effect.objects.get_or_create(name="Binding Oath", entropy=5)
effect.description = "Binds an oath or contract to fate itself. If the oath is broken, disaster will befall the oathbreaker, and anyone who looks at them with Entropy senses can see that that's what they are."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 195)
effect.add_source("Mage: The Ascension (Revised)", 164)
effect, _ = Effect.objects.get_or_create(name="Fate Mark", entropy=4)
effect.description = "Simpler than a Binding Oath, a Fate Mark is detectable to anyone with Entropy senses, and can be customized, for instance, to mark someone as a Tradition Herald or a messenger."
effect.save()
effect.add_source("Guide to the Traditions", 280)
effect, _ = Effect.objects.get_or_create(name="Geasa", entropy=5)
effect.description = "A Master can read Fate well enough that they can request Fate give an individual attention. Often Geasa are laid at birth, but not always. Every two successes allow the mage to give a level of Geasa, up to five levels. Five additional successes are needed to make it permanent. For each level, the character may gain an additional Freebie point, as at character creation. However, the consequences of violating the Geasa are dire and up to the ST. A Geasa is identical to the 'Paranormal Prohibition or Imperative' Flaw on Page 83 of the Book of Secrets."
effect.save()
effect.add_source("Tradition Book: Euthanatos (Revised)", 62)
effect, _ = Effect.objects.get_or_create(name="Major Geas", entropy=5, mind=5)
effect.description = (
    "Like Binding Oath, though Mind allows the mage to force it upon the target."
)
effect.save()
effect.add_source("Dead Magic 2", 118)
effect, _ = Effect.objects.get_or_create(name="Minor Geas", entropy=2, mind=2)
effect.description = "The mage voluntarily swears a binding oath, which overrules all other concerns for them. Mind binds the target's honor code into upholding the geas, and Entropy causes bad luck if it is broken."
effect.save()
effect.add_source("Dead Magic 2", 118)
effect, _ = Effect.objects.get_or_create(name="Secret Rune", entropy=5)
effect.description = "The mage uses this rune when sharing a secret with a trusted person. The trusted person swears an oath to keep the information secret, and the Secret Rune binds them to that oath. If they break the trust, they gain a flaw worth one point per two successes on this spell."
effect.save()
effect.add_source("Dead Magic 2", 101)
effect, _ = Effect.objects.get_or_create(
    name="Sparrow's Fall", time=4, entropy=3, prime=2
)
effect.description = "Like The Branding Rote, Sparrow's Fall marks someone with a forbidden act and attacks them if they commit it, for instance, marking a suspected Vampire to be harmed if it drinks blood. Three successes are needed to create the mark, and successes beyond that are used for damage. The three variants use Prime 2, Life 3 and Mind 4 to cause the damage."
effect.save()
effect.add_source("Order of Reason", 110)
effect, _ = Effect.objects.get_or_create(name="All Tomorrow's Parties", time=2, mind=3)
effect.description = "By asking the right questions of the right people, the mage can find out about upcoming events, scanning nearby minds to determine if there's something being planned and using Time, looking ahead slightly. This gives hunches and inclinations that guide the mage to an event even if they cannot get people to directly tell them about it."
effect.save()
effect.add_source("Orphan's Survival Guide", 127)
effect, _ = Effect.objects.get_or_create(name="Anunnaku", spirit=3, entropy=3, prime=3)
effect.description = "This set of omens are one of the most immediately useful: the ability to read the present and future of supernatural forces. It's particularly effective at reading the fates of malevolent forces and is one of the most effective techniques for determining the plans of the Nephandi."
effect.save()
effect.add_source("Dead Magic", 54)
effect, _ = Effect.objects.get_or_create(
    name="Biometric Holographic Recreation", time=2, forces=2
)
effect.description = "With a half hour spent scanning and detailed investigation of the scene of an incident, the Progenitor investigator can create a perfect holographic replica of it down to the last speck of dust."
effect.save()
effect.add_source("Convention Book: Progenitors (Revised)", 72)
effect, _ = Effect.objects.get_or_create(name="Celestial Prediction", time=2)
effect.description = "A Celestial Master may study the stars and use them to deduce something that has happened in the past or will happen in the future."
effect.save()
effect.add_source("Order of Reason", 86)
effect, _ = Effect.objects.get_or_create(name="Chronopathy", time=2, mind=3)
effect.description = "Combining Telepathy and Past or Future Sight, the mage can experience the past or future from the perspective of a denizen of that time. With Time 4, they can even send brief thoughts and impulses to the target."
effect.save()
effect.add_source("Hidden Lore", 16)
effect, _ = Effect.objects.get_or_create(name="Crime and Consequences", time=2, mind=2)
effect.description = "The Cultist looks forward in time and causes the target to feel all the consequences of their actions in advance, all at once."
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (Revised)", 72)
effect, _ = Effect.objects.get_or_create(name="Divinations", time=2)
effect.description = "The mage can investigate the past or future, with successes spent on both the duration of the vision and how far away it is. The further back or forward, of course, the less accurate the divination."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 192)
effect, _ = Effect.objects.get_or_create(
    name="Don't Cross the Streams", correspondence=2, time=2
)
effect.description = "This rote developed by Chaoticians gives a warning about a specific place, and the more successes the more specific the warning about a potential danger will be."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 64)
effect, _ = Effect.objects.get_or_create(name="Forecasting", time=2, entropy=2)
effect.description = "The Technocrat creates a simulation and spends a turn inputting data, after which the agent can spend one success to roll their next action in advance, with each additional success allowing a roll for another distinct action."
effect.save()
effect.add_source("Convention Book: Syndicate (Revised)", 74)
effect, _ = Effect.objects.get_or_create(name="The Geometry of Trade", time=2)
effect.description = "A technique developed by the High Guild, by gathering information about trade and prices in an area. Time gives information about the future, Correspondence allows it to target the trade in a different place, Mind gives insight into what people want, and Entropy helps to make the predictions more accurate."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 91)
effect, _ = Effect.objects.get_or_create(name="Hepatoscopy", time=2)
effect.description = (
    "The mage slaughters an animal and can read the future in its liver."
)
effect.save()
effect.add_source("Dead Magic 2", 143)
effect, _ = Effect.objects.get_or_create(name="Jung's Trick", correspondence=2, mind=3)
effect.description = "By researching the subject's dreams, the Technocrat can create an algorithm to analyze the subject's subconscious. Then, the Agent can analyze dreams in progress and predict what the subject intends to do in the next day."
effect.save()
effect.add_source("Convention Book: New World Order (Revised)", 86)
effect, _ = Effect.objects.get_or_create(
    name="Long-Range Eyes", correspondence=2, time=2, mind=1
)
effect.description = "The mage can look at any given place or time and follow a given target forward or backwards."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (First Edition)", 62)
effect, _ = Effect.objects.get_or_create(name="Manipulate Time Fragment", time=2)
effect.description = "With the proper apparatus, a Void Engineer Chrononaut can see ten minutes into the future or the past, albeit not necessarily clearly."
effect.save()
effect.add_source("Technocracy: Void Engineers", 46)
effect, _ = Effect.objects.get_or_create(name="Nonlinear Prediction", entropy=2)
effect.description = "The Technocrat can use a complex statistical model to predict the probable outcome of one action. More successes are needed for the more complex the action being predicted is."
effect.save()
effect.add_source("Guide to the Technocracy", 208)
effect, _ = Effect.objects.get_or_create(name="Peeping Tom", correspondence=2, time=2)
effect.description = "The mage can look backwards in time at any location, whether they are there or not."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 228)
effect, _ = Effect.objects.get_or_create(name="Planned Projection", time=2)
effect.description = "Using complex statistics, the Iterator can predict the future (to reasonable accuracy) of a single person, place, or thing."
effect.save()
effect.add_source("Technocracy: Iteration X", 49)
effect, _ = Effect.objects.get_or_create(name="Play Back", correspondence=2, time=2)
effect.description = "A Virtual Adept technique that allows them to obtain recordings and other data, even if it has been damaged or attempts have been made to destroy it."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 221)
effect, _ = Effect.objects.get_or_create(name="Postcognition", time=2)
effect.description = "This allows the mage to view a location and look backwards in time, as though rewinding."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 218)
effect.add_source("Mage: The Ascension (Second Edition)", 223)
effect, _ = Effect.objects.get_or_create(name="Psychometry", time=2, matter=1)
effect.description = "By touching an object, the mage can get a sense of its background and important events that occurred near it during its history."
effect.save()
effect.add_source("Hidden Lore", 14)
effect, _ = Effect.objects.get_or_create(
    name="Quo Vadis? (Whither Goest Thou?)", correspondence=2, time=2, mind=2
)
effect.description = "This rote gives a Templar an approximate idea of the target's planned route, where they will be going in the near future."
effect.save()
effect.add_source("Book of Crafts", 103)
effect, _ = Effect.objects.get_or_create(
    name="Reading the Umbral Skein", time=2, spirit=2, mind=1
)
effect.description = "Functionally identical to usual Time magic scrying, this rote gives access to the history (not the future!) of a portion of the Umbra corresponding to the user's location (or elsewhere with Correspondence). The temporal distance that can be seen is 21 times the usual amount, allowing the mage to see into the deep past of the Umbra, and Mind is used to allow the mage to remember every bit of the often-bizarre information gained this way."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (Revised)", 70)
effect, _ = Effect.objects.get_or_create(
    name="Running Scenarios", time=2, entropy=2, mind=4
)
effect.description = "This rote requires at least one level of the Dream background. Using the information available from the Dream background and the flexibility of dreams, the mage runs through huge numbers of scenarios and possibilities. When they wake up, they will have an accurate assessment of the probabilities of various actions related to the problem they were dreaming about, and some relevant skills (as per Dream)."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 68)
effect, _ = Effect.objects.get_or_create(name="Salmon of Wisdom", time=2, mind=3)
effect.description = "The mage enters a dreamlike trance that reveals a portion of the future. Mind ensures that the mage can enter the trance while awake and remember what occurs. Spirit allows the mage to contact the salmon of wisdom themselves and speak to them."
effect.save()
effect.add_source("Dead Magic 2", 120)
effect, _ = Effect.objects.get_or_create(name="The Scented Handkerchief", time=2)
effect.description = "The mage can discern facts about recent events from disparate environmental clues. With more successes, more clues are pulled together and a more detailed description of what occurred can be inferred."
effect.save()
effect.add_source("Order of Reason", 86)
effect, _ = Effect.objects.get_or_create(name="Songs of Future Days", time=2)
effect.description = (
    "Like Postcognition, but it involves viewing the future rather than the past."
)
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 218)
effect.add_source("Mage: The Ascension (Second Edition)", 223)
effect, _ = Effect.objects.get_or_create(
    name="Strategic Inefficiency Analysis", time=2, entropy=2
)
effect.description = "Via precise statistical modeling, a Technocrat can predict what a given organization is planning, though several successes are needed to determine anything other than the absolute basics."
effect.save()
effect.add_source("Guide to the Technocracy", 209)
effect, _ = Effect.objects.get_or_create(name="Sugar Magnolias", time=2, mind=3)
effect.description = "This rote allows a mage to experience past events via the subject's memories. This is not just viewing the memories, however, but rather reconstructing the event with the help of the memories, but able to experience it independently."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 228)
effect, _ = Effect.objects.get_or_create(
    name="Turning the Wheel of Ages", time=2, spirit=1, mind=3
)
effect.description = "This rote allows an Akashic to experience the past of other mages, including their past lives. Mind 3 suffices for willing targets and other Akashics, Mind 4 is necessary otherwise."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 77)
effect, _ = Effect.objects.get_or_create(
    name="View the Scattered Lotus Petals", time=2, entropy=1
)
effect.description = "Using Entropy, the Euthanatos can follow several threads of fate and see multiple possible futures, with each success revealing one possibility."
effect.save()
effect.add_source("Tradition Book: Euthanatos (Revised)", 60)
effect, _ = Effect.objects.get_or_create(name="Area Scan", correspondence=3)
effect.description = "The Void Engineer can perceive several places at once."
effect.save()
effect.add_source("Technocracy: Void Engineers", 41)
effect, _ = Effect.objects.get_or_create(
    name="Auric Trail", correspondence=1, spirit=1, prime=1
)
effect.description = "This rote allows a mage to track a mage or spirit (with Spirit 2) wherever they go, on Earth or in the Umbra. This tracks the target by its resonance and is easier if the target has particularly strong resonance. The rote is much harder on Earth as resonance fades more quickly there than in the Umbra. Correspondence 2 is required if the target reforms elsewhere (spirits) or teleports (mages)."
effect.save()
effect.add_source("Infinite Tapestry", 181)
effect, _ = Effect.objects.get_or_create(name="Check the Corners", correspondence=2)
effect.description = "Via parabolic microphones, thermal detectors and motion sensors, a New World Order Agent can see around corners and through walls."
effect.save()
effect.add_source("Technocracy: New World Order", 43)
effect, _ = Effect.objects.get_or_create(
    name="Correspondence Sensing", correspondence=2
)
effect.description = "This rote allows the mage to build a connection between their senses and a desired location. This can take the form of scrying: where the mage can view a location remotely. It can also take the form of an active defense, where the mage watches for others attempting to build connections to the location and prepares to counter their efforts."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 185)
effect.add_source("Mage: The Ascension (Revised)", 159)
effect, _ = Effect.objects.get_or_create(name="Distant Sight", correspondence=2)
effect.description = "This rote allows the user to scry a distant location. With Time added in, the mage can also see the past or future of the distant location."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 91)
effect, _ = Effect.objects.get_or_create(name="Divided Sight", correspondence=3)
effect.description = "Though true co-location is still beyond them, the mage can perceive multiple locations at the same time."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 186)
effect.add_source("Mage: The Ascension (Second Edition)", 190)
effect, _ = Effect.objects.get_or_create(name="Filter All-Space", correspondence=3)
effect.description = "At this level of Correspondence, a mage can search the universe for an object or creature, scanning everywhere simultaneously rather than having to search manually. Without Mind 1, the mage may have trouble understanding what they see."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 186)
effect.add_source("Technocracy: New World Order", 44)
effect.add_source("Mage: The Ascension (Second Edition)", 190)
effect.add_source("Mage: The Ascension (Revised)", 160)
effect, _ = Effect.objects.get_or_create(name="Geometric Jars", correspondence=2)
effect.description = "By setting up a collection of jars filled with water in an area and watching the ripples on the surface, the mage can derive information about the subject area. With Forces, the echoes that cause the ripples can be heard."
effect.save()
effect.add_source("Artisan's Handbook", 51)
effect, _ = Effect.objects.get_or_create(
    name="Heat Seeking", correspondence=2, life=1, forces=1
)
effect.description = "With the aid of surveillance devices that can track people by temperature, the New World Order can track people inside a building, determine the number of individuals in the group."
effect.save()
effect.add_source("Technocracy: New World Order", 48)
effect, _ = Effect.objects.get_or_create(name="Heat Trace", time=2, forces=1)
effect.description = "This rote uses the path of warm air left in the wake of a person moving around to track their past movements."
effect.save()
effect.add_source("Hidden Lore", 17)
effect, _ = Effect.objects.get_or_create(
    name="Map the True Way", correspondence=2, matter=2
)
effect.description = "By entering a trance and drawing a map, an Ahl-i-Batin mage can find a person, place, or object."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 43)
effect, _ = Effect.objects.get_or_create(name="Open/Close Window", correspondence=2)
effect.description = "Allows the mage to scry on a distant location."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 189)
effect, _ = Effect.objects.get_or_create(
    name="Scan Non-Local Universe", correspondence=2, spirit=2
)
effect.description = (
    "This allows the Void Engineers to perceive any location in the Umbra."
)
effect.save()
effect.add_source("Technocracy: Void Engineers", 42)
effect, _ = Effect.objects.get_or_create(name="Scrying", correspondence=2, spirit=1)
effect.description = "During a drumming frenzy, the Dreamspeaker can see other places, both in the physical and the spirit worlds. Though normally limited to places the Dreamspeaker has been or knows somewhat, they can smoothly move perceptions to investigate new locations."
effect.save()
effect.add_source("Book of Shadows", 140)
effect, _ = Effect.objects.get_or_create(name="Seizing the Forgotten", correspondence=2)
effect.description = "Originating among the Gabrielites and Craftmasons, the mage investigates an area where an object has disappeared and turns up evidence (at least evidence that mages will recognize) if an object has been disturbed via Correspondence magick. That tampering occurred can be proven with two successes, more may give hints about who did it or where they are."
effect.save()
effect.add_source("Order of Reason", 66)
effect, _ = Effect.objects.get_or_create(name="Stalking the Void", correspondence=3)
effect.description = "An advanced form of Open/Close Window, this allows the mage to track any irregularity back to its source."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 188)
effect.add_source("Mage: The Ascension (Second Edition)", 190)
effect, _ = Effect.objects.get_or_create(name="Anger in the Land", spirit=3, matter=3)
effect.description = "This rote allows a Kopa Loei to summon forth an elemental by chanting near a large volume of the element in question. Matter is needed for an Earth elemental, Forces for a Fire, Water or Air elemental. Spirit 4 allows the mage to call a more powerful elemental spirit to inhabit the material."
effect.save()
effect.add_source("Book of Crafts", 74)
effect, _ = Effect.objects.get_or_create(name="Banish Elemental", spirit=2, forces=2)
effect.description = "This rote is a direct attack that only works against elemental spirits. It deals aggravated damage to materialized elementals and reduces Power for those in the Umbra. It cannot actually destroy them, only force them to stop manifesting or send them into Slumber."
effect.save()
effect.add_source("Hidden Lore", 17)
effect, _ = Effect.objects.get_or_create(
    name="Cycle of the Five Agents", matter=2, forces=3, prime=2
)
effect.description = "The Wu Lung can create or destroy any of the five elements according to their cycle. A flame can be converted to soil, for example. This allows general elemental transmutation, though in the Wu Lung paradigm, only along the cycle of creation or destruction."
effect.save()
effect.add_source("Dragons of the East", 59)
effect, _ = Effect.objects.get_or_create(name="Time Lock", time=4, forces=2)
effect.description = "A Hermetic Adept of Time can pre-set a force to be infused to be removed from an area in advance. Forces 2 for simple forces, Forces 3 for more complex ones, and Prime 2 if it must be created."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (First Edition)", 66)
effect, _ = Effect.objects.get_or_create(name="No Surrender", entropy=4, prime=2)
effect.description = "A last-ditch rite to prevent any group of Sisters of Hippolyta from being conquered, this unleashes earthquakes, firestorms, plagues, or explosions that demolish their conclave and kill everyone in it."
effect.save()
effect.add_source("Book of Crafts", 89)
effect, _ = Effect.objects.get_or_create(
    name="Rouse the Dragon", spirit=4, matter=5, forces=5, prime=4
)
effect.description = "By burning hundreds of charms and appeasing their ancestors with a feast, a Wu Lung creates a dragon of jade, paper, or gold. They paint red dots on the eyes to awaken it. This turns the very landscape against the Wu Lung's enemies, it may cause a tidal wave, earthquake, volcanic eruption, or hurricane, depending on the dragon being awoken, not just the figuring, but the sleeping dragon inhabiting the geography of the area."
effect.save()
effect.add_source("Dragons of the East", 58)
effect, _ = Effect.objects.get_or_create(
    name="Yao Su Dragon Thunder", spirit=2, forces=3, prime=2
)
effect.description = "This rote allows a Wu Lung to make a direct attack at anything, physical or ephemera, using some element, such as a fireball, a thunderbolt, a shower of molten metal, etc."
effect.save()
effect.add_source("Book of Crafts", 135)
effect, _ = Effect.objects.get_or_create(name="Cuicuilco's Demise", matter=4, forces=5)
effect.description = "The great city of Cuicuilco was the most powerful in Mexican Central Highlands until it was destroyed by a volcano in 150. The mage must sacrifice a human being, either slaughtering them near the volcano or throwing them in, to cause a volcanic eruption to occur. This requires at least 20 successes. Fewer can cause Earthquakes and smaller lava flows, however."
effect.save()
effect.add_source("Dead Magic", 74)
effect, _ = Effect.objects.get_or_create(name="Embracing the Earth Mother", forces=4)
effect.description = "This rote focuses gravity against a target, making them feel as though they weigh significantly more, multiplied by the number of successes plus one."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 196)
effect.add_source("Mage: The Ascension (Second Edition)", 199)
effect.add_source("Mage: The Ascension (Revised)", 167)
effect, _ = Effect.objects.get_or_create(
    name="Pele Wai'ula (Pele's Blood)", correspondence=3, matter=2, forces=3
)
effect.description = "Polynesian mages have a deep familiarity with the forces of volcanism. With Forces 3, they can open a volcanic fissure, while Forces 4 allows them to cause a full-scale volcanic eruption."
effect.save()
effect.add_source("Dead Magic 2", 29)
effect, _ = Effect.objects.get_or_create(name="Pele's Wrath", forces=4)
effect.description = "A powerful Kopa Loei can use a chunk of lava to redirect the power of a volcano into a smaller eruption."
effect.save()
effect.add_source("Book of Crafts", 74)
effect, _ = Effect.objects.get_or_create(
    name="TWACI", correspondence=3, forces=3, mind=2
)
effect.description = "Short for 'The Walls Are Closing In' and pronounced 'th-whacky,' the Reality Coder uses this rote to warp gravity and space, and to create a sense of creeping doom in the target. This rote paralyzes the target with fear, makes the walls appear to literally be closing in, and causes cumulative damage of one die of bashing damage up to a maximum of 10 dice."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 66)
effect, _ = Effect.objects.get_or_create(name="Arc", correspondence=2, forces=2)
effect.description = "Cyberpunks are rarely without weapons in modern cities, and this rote is why. It allows them to draw electricity from the power grid and turn it into an arc of electricity attacking their target."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 65)
effect, _ = Effect.objects.get_or_create(name="Call Lightning", forces=3)
effect.description = "During a thunderstorm, a mage can use this rote to route a lightning bolt from the clouds to a target."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 195)
effect.add_source("Mage: The Ascension (Second Edition)", 199)
effect, _ = Effect.objects.get_or_create(name="Discharge Static", forces=2)
effect.description = "This rote causes the static electricity in the air to discharge, attacking a target."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 195)
effect.add_source("Mage: The Ascension (Second Edition)", 198)
effect, _ = Effect.objects.get_or_create(name="Electrical Chaos", forces=2)
effect.description = "Diverts the usual flow of electricity into a target. If living, it is a damaging attack, if not, then the device takes electrical damage."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 166)
effect, _ = Effect.objects.get_or_create(
    name="Lightning Gateway", correspondence=2, forces=3, prime=2
)
effect.description = "This rote is similar to Ignis, it conjures a Forces attack from nothing, but it also can ignore barriers, striking hidden targets."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (First Edition)", 65)
effect, _ = Effect.objects.get_or_create(
    name="Pulse of the Electro-Stream", forces=3, prime=2
)
effect.description = "This rote creates a strong electrical pulse and directs it at the target. Humans take standard damage, electronics overload."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 223)
effect, _ = Effect.objects.get_or_create(
    name="Akua Kumu Haka (Guided Fireball)", spirit=3, forces=3, prime=2
)
effect.description = "Summons a fire spirit and a fireball for it to inhabit. The spirit guides the fireball to its target at high speed."
effect.save()
effect.add_source("Dead Magic 2", 26)
effect, _ = Effect.objects.get_or_create(name="Awaken Flame", spirit=3, forces=2)
effect.description = "Awakens the spirit of a flame. These spirits are usually talkative, hungry, and volatile. With Prime and Forces 3, the fire can be created and awakened, otherwise the shaman needs pre-existing flame large enough to support a spirit of the power level they want."
effect.save()
effect.add_source("The Spirit Ways", 87)
effect, _ = Effect.objects.get_or_create(name="Balefire", spirit=3, forces=3, prime=2)
effect.description = "Not actually fire, but rather a scalding blob of ephemera from something resembling a literal hell. When it encounters living flesh, it burns like fire, but cannot be soaked without Life 3/Prime 2. The flames burn until all fuel is consumed, and any injuries take twice as long as usual to heal and leave nasty scars."
effect.save()
effect.add_source("Infernalism: The Path of Screams", 86)
effect, _ = Effect.objects.get_or_create(
    name="Ball of Abysmal Flames", time=4, matter=3, forces=5, prime=4
)
effect.description = "One of the most powerful combat rotes in the Hermetic arsenal, Ball of Abysmal Flames leeches Quintessence from the surrounding area and ignites it, fueling a flame that sucks in the air surrounding it and grows stronger until it explodes in a firestorm. Prime 5 allows it to draw fuel from living beings, not just inanimate objects as with Prime 4, Matter compresses it into a small ball of flames and Time releases that ball's destructive capacity at a chosen time, hopefully allowing the mage time to get to safety. It was not an exaggeration when certain modern Hermetics nicknamed this rote 'The Nuke.'"
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 223)
effect.add_source("Tradition Book: Order of Hermes (First Edition)", 67)
effect, _ = Effect.objects.get_or_create(
    name="Betrayal of the Burning Arrow", correspondence=1, forces=3
)
effect.description = "By breaking a glass or crystal arrowhead inscribed with the Enochian symbol for the number 8, an ill-omened number according to many Hermetics, a Hermetic mage chooses a bullet in a gun within line of sight and converts kinetic energy to heat. When the bullet is fired, it explodes turning into a Forces attack on the holder of the gun."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (Revised)", 66)
effect, _ = Effect.objects.get_or_create(
    name="Devouring Gullet of Flame", forces=4, prime=2
)
effect.description = "The Taftani most often trigger this effect by forging a ring of copper and brass and then throwing it at their enemies while speaking the trigger word. This causes the ring itself to turn into a tunnel of flame, sucking the Taftani's enemies into it. Evading this tunnel without magick requires a difficulty 9 Dexterity+Athletics roll. Forces damage is assessed each turn that the target is within the tunnel, which for each success is five feet in diameter and five feet deep."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 87)
effect, _ = Effect.objects.get_or_create(name="Dragonstorm", forces=4, prime=4)
effect.description = "A refined version of Greek fire, Dragonstorm is a fire that can consume anything and everything. Forces creates a super hot flame while Prime draws the quintessence out of everything in the area to fuel it. Forces 5 doubles the blast radius. The Prime 4 version does successes x 3 aggravated damage and the Prime 5 version does x 4 and can overwhelm flame resistance, such as that possessed by dragons."
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 273)
effect, _ = Effect.objects.get_or_create(name="Eternal Flame", forces=2, prime=3)
effect.description = "With at least 10 successes, this rote allows a Chorister to pass a Quintessence stream (such as from a Node) through a flame to keep it burning. The Quintessence is not consumed, and may be used for other things, but if the flow stops, the flame does as well."
effect.save()
effect.add_source("Tradition Book: Celestial Chorus", 65)
effect, _ = Effect.objects.get_or_create(name="Fire Rune", forces=3)
effect.description = "This rune douses a flame."
effect.save()
effect.add_source("Dead Magic 2", 99)
effect, _ = Effect.objects.get_or_create(name="Friction Curse", forces=3)
effect.description = "Converts kinetic energy to heat, so that the faster an object goes, the hotter it becomes and the more damage it takes."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 166)
effect, _ = Effect.objects.get_or_create(
    name="Gabriel's Embrace", correspondence=2, matter=2, forces=3, prime=2
)
effect.description = "This rote converts the air around the target (Matter) or the target's flesh itself (Life) into a burning flame. The mage calls upon Gabriel, the Archangel of Fire, and keys the pentacle of Mercury to the victim (via some Correspondence connection)."
effect.save()
effect.add_source("Blood Treachery", 88)
effect, _ = Effect.objects.get_or_create(
    name="Hermes' Brand", time=4, forces=3, entropy=1, prime=2
)
effect.description = "A Hermetic uses Entropy 1 and Time 4 to enchant their (or another's) blood creating a hanging Prime 2/Forces 3 effect which takes place a fixed amount of time after the blood is ingested by a Vampire. Each blood point consumed from the target of this rote bursts into flame inside the Vampire for two health levels of aggravated damage, and if the Vampire survives, they lose a blood point for each point that exploded (and those are also lost)."
effect.save()
effect.add_source("Blood Treachery", 89)
effect, _ = Effect.objects.get_or_create(name="Ignis", forces=3, prime=2)
effect.description = "An effect beloved of House Flambeau, Ignis conjures flames from nothing at the target."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (First Edition)", 65)
effect, _ = Effect.objects.get_or_create(name="Inferno", forces=5)
effect.description = "Converts all the light and sound in an area into heat, causing it to burst into flame."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 167)
effect, _ = Effect.objects.get_or_create(name="Lotus Bloom", forces=3)
effect.description = "This requires the Footbind rote has been performed. This vulgar Wu-Keng rote causes a lotus to blossom from the caster's bound feet, and then explode, immolating the mage's foes."
effect.save()
effect.add_source("Book of Crafts", 119)
effect, _ = Effect.objects.get_or_create(
    name="Phlogiston Manipulation", life=3, forces=3, prime=2
)
effect.description = "Though phlogiston has been discredited by mainstream scientists, Hermetics can manipulate it in the living (with Life) and in inanimate objects (with Matter) to either ignite an object (extracting the phlogiston) or to restore something that has been burned (inserting new phlogiston)."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (First Edition)", 66)
effect_phlogiston_flux = Effect.objects.get_or_create(name="Phlogiston Flux", matter=2)[
    0
]
effect, _ = Effect.objects.get_or_create(
    name="Pop Goes the Weasel", life=3, forces=2, prime=2
)
effect.description = "The mage immobilizes the victim and makes an extended roll. The target suffers extreme pain as their body is heated up. At the end of the effect, all the damage is applied as aggravated damage, usually killing the victim in a burst of flame."
effect.save()
effect.add_source("Orphan's Survival Guide", 129)
effect, _ = Effect.objects.get_or_create(name="Possess Flame", forces=2, mind=4)
effect.description = "The shaman can take control of a fire (or create one that they are in control of with Prime and Forces 4). During this time, the shaman's consciousness inhabits the flame, and their body lies in a trance. Larger flames, the side of buildings, require Forces 4. If still inside the fire when it is extinguished, the mage loses a point of Willpower."
effect.save()
effect.add_source("The Spirit Ways", 88)
effect, _ = Effect.objects.get_or_create(
    name="Proof Against Immolation", matter=3, prime=2
)
effect.description = "An alchemist can develop a smoke they can inhale which protects their body from flame and heat."
effect.save()
effect.add_source("Book of Crafts", 42)
effect, _ = Effect.objects.get_or_create(
    name="Shih-Huang-Ti's Marvelous Game", life=3, forces=2
)
effect.description = "The Wu-Keng usually reserve this attack for their enemies, the Wu Lung, but sometimes use it on others. This rote boils the victim alive in their skin."
effect.save()
effect.add_source("Book of Crafts", 119)
effect, _ = Effect.objects.get_or_create(name="Wildfire", forces=2, entropy=2)
effect.description = "By lighting a fire at the intersection of two interlocked pentacles, for Mars and Pluto, the mage warps probability to make everything just happen to break correctly for the flame to grow out of control."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (Revised)", 68)
effect, _ = Effect.objects.get_or_create(name="Wrath of Heaven", forces=4, prime=2)
effect.description = "This Chorister rote is traditionally used in extreme combat situations. It can create nearly any manifestation of Forces traditionally associated with the divine, the most common of which are ball lightning and a pillar of fire."
effect.save()
effect.add_source("Tradition Book: Celestial Chorus", 65)
effect, _ = Effect.objects.get_or_create(name="Fiat Lux", forces=2, prime=2)
effect.description = "Arguably one of the oldest rotes in existence, the weaker version enhances a light source and the strong creates one."
effect.save()
effect.add_source("Tradition Book: Celestial Chorus (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(name="Filter'd Lantern-Light", forces=2)
effect.description = "Can create various forms of light from a lantern. Among the effects possible are a diffuse, colored light with an obvious origin, a strong colored beam of light, or even burning hot but dull, so that little illumination is offered but the lantern acts as a heat source."
effect.save()
effect.add_source("Artisan's Handbook", 49)
effect, _ = Effect.objects.get_or_create(name="Flash", forces=3)
effect.description = "An Artificer rote, the user prepares a piece of paper to ignite rapidly creating a bright flash of light from a fire. This burst of light can blind anyone caught unaware (Stamina diff 8 to avoid) and under the right circumstances, may trigger panic in Vampires."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (First Edition)", 62)
effect.add_source("Order of Reason", 72)
effect, _ = Effect.objects.get_or_create(
    name="Glorious Sword of Heaven", correspondence=2, forces=2
)
effect.description = "From the minor and odd House Castrovinci, this rote uses an Enochian supplication to Michael the warrior Archangel and patron of the Sun, along with pentacles of Mars, to direct a lance of sunlight from somewhere on Earth to a Vampire. The rank 2 version of this rote summons a focused beam of sunlight that must target a Vampire's exposed flesh, but the rank 4 version can draw sunlight into an area as large as a city block, which almost certainly will destroy Vampires in that area."
effect.save()
effect.add_source("Blood Treachery", 89)
effect, _ = Effect.objects.get_or_create(name="Laser Enhancement", forces=2)
effect.description = "This allows the Technomage the ability to strengthen lasers by improving the focus of light. Thus, a laser pointer can become a deadly weapon."
effect.save()
effect.add_source("Technocracy: Void Engineers", 42)
effect, _ = Effect.objects.get_or_create(name="Laser Production", forces=3, prime=2)
effect.description = "A stronger version of Laser Enhancement, this causes the laser to do aggravated damage."
effect.save()
effect.add_source("Technocracy: Void Engineers", 42)
effect, _ = Effect.objects.get_or_create(
    name="Tsuiho - The Fires of Heaven", correspondence=4
)
effect.description = "The Wu Lung can truly show their enemies the power of heaven."
effect.save()
effect.add_source("Dragons of the East", 60)
effect, _ = Effect.objects.get_or_create(
    name="'Ahiu Nalu (Rogue Wave)", forces=2, entropy=2
)
effect.description = "Mighty Polynesian mages would dual on the ocean, and a common weapon was the water itself, used as a big wave, created either by tampering with probability, with the forces to form a wave, or the water directly."
effect.save()
effect.add_source("Dead Magic 2", 26)
effect, _ = Effect.objects.get_or_create(
    name="Calling the Wind Lords", spirit=2, forces=2
)
effect.description = "The Verbena summons spirits of the winds, who then influence the weather for them. More successes allow for greater changes to the weather."
effect.save()
effect.add_source("Tradition Book: Verbena (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(name="Cloud Cover", forces=5)
effect.description = "When piloting a skyrigger, this allows the mage to hide its movements above clouds to protect it from Sleeper eyes. A failure may require Pilot Skyrigger to recover from, success allows the ship to remain hidden."
effect.save()
effect.add_source("Order of Reason", 108)
effect, _ = Effect.objects.get_or_create(name="Dousing", correspondence=1, life=1)
effect.description = "The Verbena can attempt to find water using a forked stick (hazel is preferred). They do this by sensing the minute lifeforms in the water, rather than seeking the water itself."
effect.save()
effect.add_source("Tradition Book: Verbena (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(
    name="Dowsing", correspondence=2, matter=1, forces=2
)
effect.description = "With Dowsing, nothing is hidden from the mage. When searching for a substance, particularly water, this rote finds it and brings it (or any other liquid) to the surface."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 43)
effect, _ = Effect.objects.get_or_create(name="Heenalu (Wave Walking)", forces=2)
effect.description = "This rote allows a mage to walk on the surface of water, either through levitation or by strengthening the water's surface itself."
effect.save()
effect.add_source("Dead Magic 2", 27)
effect, _ = Effect.objects.get_or_create(name="Mahu (Steam)", forces=2, prime=2)
effect.description = (
    "This rote converts water directly to steam, scalding anyone caught in it."
)
effect.save()
effect.add_source("Dead Magic 2", 28)
effect, _ = Effect.objects.get_or_create(name="Sing Down the Rain", matter=3, forces=2)
effect.description = "The mage sings out a short poem or song to call to the ghosts that ride the clouds. This nudges the clouds into the desired position and pulls the moisture out into rain."
effect.save()
effect.add_source("Dead Magic", 30)
effect, _ = Effect.objects.get_or_create(name="Storm Rune", forces=3, entropy=3)
effect.description = "This rune allows the mage to calm storms and waves at sea."
effect.save()
effect.add_source("Dead Magic 2", 99)
effect, _ = Effect.objects.get_or_create(name="Tempest in a Teapot", forces=5)
effect.description = "While Weather Working can manipulate existing storms, Tempest in a Teapot can create a storm out of nothing, with more successes indicating more power in the storm."
effect.save()
effect.add_source("Mage: The Ascension Second Edition", 199)
effect.add_source("Mage: The Ascension Revised", 168)
effect, _ = Effect.objects.get_or_create(name="Waipuilani (Waterspout)", forces=3)
effect.description = "If there are clouds, this manipulates the local weather to create a waterspout, a tornado over open water. Otherwise, the mage can use the power of Forces directly to accomplish the same goal."
effect.save()
effect.add_source("Dead Magic 2", 29)
effect, _ = Effect.objects.get_or_create(name="Weather Working", forces=4)
effect.description = "This rote manipulates the weather, and can cause rapid changes such as heat waves, clearing a cloudy day, etc."
effect.save()
effect.add_source("Mage: The Ascension Revised", 167)
effect.add_source("Dead Magic 2", 103)
effect, _ = Effect.objects.get_or_create(
    name="Cold Water's Blessing", matter=2, prime=2
)
effect.description = "Clean water supports life and acts as a protection against evil. By hitting the target with cold water (including tricking them into entering a river), the mage channels the water's power to support life and washes away evil magick, unweaving any malign magic on the target."
effect.save()
effect.add_source("Dead Magic", 26)
effect, _ = Effect.objects.get_or_create(name="Contingent Effect", time=4)
effect.description = "Allows the mage to set a trigger for an effect. If done, the effect hangs, ready to fire, but only does so when the trigger occurs."
effect.save()
effect.add_source("Mage: The Ascension Revised", 193)
effect, _ = Effect.objects.get_or_create(name="Counterspell Rune", correspondence=1)
effect.description = "This Rune acts as Countermagick. It can serve as simple Prime countermagick or Sphere-specific countermagick as needed."
effect.save()
effect.add_source("Dead Magic 2", 98)
effect, _ = Effect.objects.get_or_create(name="Divert Prime Force", prime=2)
effect.description = "This allows a Void Engineer to tap a source of Quintessence (including their own avatar), to power an effect."
effect.save()
effect.add_source("Technocracy: Void Engineers", 45)
effect, _ = Effect.objects.get_or_create(name="Enchant Life", prime=3)
effect.description = "Allows the mage to infuse a living being with Quintessence, making it seem more real and anchoring it in reality. Additionally, this causes the creature's natural weapons to do aggravated damage. This costs a point of Quintessence."
effect.save()
effect.add_source("Mage: The Ascension Revised", 184)
effect, _ = Effect.objects.get_or_create(name="Master's Enchantment", prime=5)
effect.description = "A Master of Prime may enchant a living being, a place or a time. In the case of a living being, this creates a Relic, a sort of living Talisman. For a place it creates a Node and for time a Juncture (which functions similarly to a Node). Creating a Node requires a massive number of successes."
effect.save()
effect.add_source("Mage: The Ascension Revised", 185)
effect, _ = Effect.objects.get_or_create(name="Parma Magica", prime=3)
effect.description = "It is not an exaggeration to call Parma Magica the greatest accomplishment of Bonisagus himself, nor to say that the rote is responsible for the creation of the Order of Hermes itself. By advancing countermagick significantly, it allowed Hermetics to meet and form alliances before they had developed trust. This rote allows the Hermetic to store up to two points of Quintessence per success which can be used for countermagick and unweaving the effects of others. These Quintessence points no longer count towards the mage's limit but are limited by how much Quintessence the mage can carry."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (First Edition)", 65)
effect, _ = Effect.objects.get_or_create(name="Programmed Event", time=4)
effect.description = "An Adept of Time can stop time completely in a small area and set a time when it will resume. Objects and people (other than those the mage makes immune) are frozen so long as no one outside the effect comes into contact with anything inside it."
effect.save()
effect.add_source("Mage: The Ascension First Edition", 219)
effect.add_source("Mage: The Ascension Second Edition", 223)
effect.add_source("Mage: The Ascension Revised", 193)
effect, _ = Effect.objects.get_or_create(name="Watch the Weaving", prime=1)
effect.description = "This allows the mage to see effects as they are being formed, in a way compatible with their paradigm. For instance, Hermetics have a formalized system where different spheres and intentions yield different colors and shapes of magick."
effect.save()
effect.add_source("Mage: The Ascension Revised", 182)
effect, _ = Effect.objects.get_or_create(
    name="Awaken the Sleeping Earth", matter=3, prime=3
)
effect.description = "When a mage finds a Node that is dormant, they can tap it. This rote opens a channel into the Node and allows the Quintessence to flow from it into some vessel."
effect.save()
effect.add_source("Book of Chantries", 149)
effect, _ = Effect.objects.get_or_create(name="Glorious is the Temple", mind=2, prime=3)
effect.description = "With this effect, a mage can lead a group ritual and provide Quintessence to anyone assisting them with it, without breaking the flow of the ritual itself."
effect.save()
effect.add_source("Artisan's Handbook", 52)
effect, _ = Effect.objects.get_or_create(name="Leying of the Line", matter=3, prime=3)
effect.description = "The mage can use this rote to create roughly a mile of ley line per success. The line transfers Quintessence from a Node to whatever is at the end of the line, usually a Chantry. Of course, Quintessence can be drawn from the Node itself, cutting off the supply."
effect.save()
effect.add_source("Book of Chantries", 149)
effect, _ = Effect.objects.get_or_create(name="Locate Quintessence Flow", prime=1)
effect.description = "This allows Void Engineers to trace Quintessence flows back to the Node that they originate at."
effect.save()
effect.add_source("Technocracy: Void Engineers", 45)
effect, _ = Effect.objects.get_or_create(name="Node Raider", prime=3)
effect.description = "This rote allows the mage to pull Quintessence out of a Node roughly, in a way that can damage the Node. Usually used either in desperation or as an attack on an enemy's resources, this rote gives the mage one point of Quintessence per success, which can be redirected into a Periapt if the mage has one. The node, however, gives no Quintessence or Tass for a number of days equal to the number of successes. For every ten successes, the Node loses one level of power permanently, and if it drops to zero, it is destroyed."
effect.save()
effect.add_source("Guide to the Traditions", 280)
effect, _ = Effect.objects.get_or_create(
    name="Primal Credit Rating", correspondence=3, entropy=2, prime=3
)
effect.description = "The Syndicate agent can make the target have a hard time drawing Primal Energy from technological sources. For the duration, each success devoted to this effect prevents the absorption of one point of Primal Energy every time the target might collect it from a source that has Rank 1 Data sympathy."
effect.save()
effect.add_source("Convention Book: Syndicate (Revised)", 75)
effect, _ = Effect.objects.get_or_create(
    name="Prime Location", correspondence=1, prime=1
)
effect.description = "Mages understand how important location is, almost as much as realtors. This rote allows the mage to find the specific location of a Node. With Correspondence 1, it must be nearby, with Correspondence 2 it can be anywhere."
effect.save()
effect.add_source("Book of Shadows", 145)
effect, _ = Effect.objects.get_or_create(name="Sense Node", correspondence=2, prime=1)
effect.description = (
    "With the proper equipment, a Watcher can detect if a building contains a Node."
)
effect.save()
effect.add_source("Technocracy: New World Order", 48)
effect, _ = Effect.objects.get_or_create(name="Tap Node", prime=3)
effect.description = "This allows the Void Engineer to draw power from a Node, to the point where it is temporarily useless. This requires a number of successes proportional to the strength of the Node being tapped."
effect.save()
effect.add_source("Technocracy: Void Engineers", 45)
effect, _ = Effect.objects.get_or_create(name="Terminal Sanitization", prime=5)
effect.description = "When a Node has been corrupted by Nephandic ritual or a Marauder, this essentially turns it off until its resonance has been scrubbed."
effect.save()
effect.add_source("Technocracy: Void Engineers", 46)
effect, _ = Effect.objects.get_or_create(name="Wellspring", prime=4)
effect.description = "At a location with Resonance particularly in tune with the mage, this rote allows the mage to draw some Quintessence from this spot, effectively using it as a Node."
effect.save()
effect.add_source("Mage: The Ascension Revised", 185)
effect, _ = Effect.objects.get_or_create(name="Bond of Blood", prime=3)
effect.description = "A Disciple of Prime can pull Quintessence directly out of a Node, out of a willing target, or can reverse these, placing Quintessence in the Node or gifting Quintessence to an ally."
effect.save()
effect.add_source("Mage: The Ascension First Edition", 211)
effect.add_source("Mage: The Ascension Second Edition", 215)
effect.add_source("Mage: The Ascension Revised", 183)
effect, _ = Effect.objects.get_or_create(
    name="The Burning Lotus", forces=3, entropy=4, prime=5
)
effect.description = "A suicide maneuver that is rarely used, the Euthanatos pulls all the Quintessence they can, from their body, the surrounding area, anything at all. This Quintessence then fuels a massive storm of elemental fury that consumes and degrades anything in its path for 20 feet per success. With Spirit, this rote can be sent across the Gauntlet and with Mind the mage sends out a final message before being consumed."
effect.save()
effect.add_source("Tradition Book: Euthanatos (First Edition)", 68)
effect, _ = Effect.objects.get_or_create(name="Convert Node to Tass", prime=3)
effect.description = "Despite the name, this procedure doesn't actually remove the Node, but rather draws all the available Quintessence from it and store it in devices that use Tass to power their effects, or even store it directly as Tass."
effect.save()
effect.add_source("Technocracy: Void Engineers", 46)
effect, _ = Effect.objects.get_or_create(name="Cup of Joe", prime=3)
effect.description = "A Hollow One can use this rote to transfer a number of points of Quintessence up to their Arete into a caffeinated beverage, which then are transferred to whoever drinks it."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 62)
effect, _ = Effect.objects.get_or_create(name="Drain Tass", prime=3)
effect.description = "Allows the mage to draw Tass from a node in excess of their avatar rating. Doing so often or to an extreme level may permanently damage the Node."
effect.save()
effect.add_source("Order of Reason", 83)
effect, _ = Effect.objects.get_or_create(name="Economic Warfare", prime=4)
effect.description = "For a period of time, each success decreases the target's Resources background by one. If enough successes are spent to make the duration permanent, two successes are needed to decrease Resources permanently by one."
effect.save()
effect.add_source("Convention Book: Syndicate (Revised)", 83)
effect, _ = Effect.objects.get_or_create(name="Footbind", life=2, forces=2, prime=3)
effect.description = "This excruciatingly painful and debilitating ritual is often performed on Wu-Keng when they join the craft. The Wu-Keng has all the difficulties that footbinding causes, including deformed feet, often to the point of being unable to walk unaided. In exchange, the wrappings used allow the mage to draw Quintessence from the surroundings into their bindings, and use that Quintessence as needed."
effect.save()
effect.add_source("Book of Crafts", 119)
effect, _ = Effect.objects.get_or_create(name="Fount of Paradise", prime=5)
effect.description = "With Master of Prime, a mage can draw Quintessence from the Universe at large, not needing to be in any special place to obtain it."
effect.save()
effect.add_source("Mage: The Ascension Revised", 185)
effect, _ = Effect.objects.get_or_create(
    name="The Hand of the Siphoner", matter=1, prime=3
)
effect.description = "By touching the physical object tied to a Node, the mage can draw Quintessence from it at one point per success. This does not work on dormant Nodes."
effect.save()
effect.add_source("Book of Chantries", 149)
effect, _ = Effect.objects.get_or_create(
    name="Hymn of Beatific Harmony", correspondence=3, prime=3
)
effect.description = "This rote allows Quintessence to be sent anywhere on Earth."
effect.save()
effect.add_source("Mage: The Ascension First Edition", 226)
effect, _ = Effect.objects.get_or_create(name="Primal Infusion", life=3, prime=3)
effect.description = "The recipient of this effect is treated for three to six months with specialized drugs and chemicals. The result is that every week they generate a point of Prime Energy, which causes one health level of damage that cannot be healed while the Prime Energy is held. They can hold one point of Prime Energy per dot of Stamina. Furthermore, any roll to resist disease has a difficulty increase of two, as this procedure weakens the body significantly."
effect.save()
effect.add_source("Technocracy: Progenitors", 44)
effect.add_source("Convention Book: Progenitors (Revised)", 74)
effect, _ = Effect.objects.get_or_create(name="Primal Net", matter=2, life=2, prime=2)
effect.description = "This procedure is performed at the level of an entire hospital and siphons off a small amount of Prime Energy from people in persistent vegetative states or long-term intensive care. It slightly decreases the recovery rate for coma patients. This works distressingly well when paired with Primal Infusion."
effect.save()
effect.add_source("Technocracy: Progenitors", 46)
effect.add_source("Convention Book: Progenitors (Revised)", 74)
effect, _ = Effect.objects.get_or_create(
    name="Radiate Prime Energy", entropy=2, prime=3
)
effect.description = "This rote allows the mage to force Quintessence out of a target (limited by the target's avatar rating)."
effect.save()
effect.add_source("Mage: The Ascension First Edition", 226)
effect, _ = Effect.objects.get_or_create(name="Recharge Device", prime=3)
effect.description = "With this procedure, Technocratic Devices can be recharged, infusing Primal Energy into them."
effect.save()
effect.add_source("Technocracy: Iteration X", 48)
effect, _ = Effect.objects.get_or_create(name="Recharge Gift", prime=5)
effect.description = "Quintessence flows through everything, and with this rote, a mage can consume those Patterns to refill their Quintessence store."
effect.save()
effect.add_source("Mage: The Ascension First Edition", 212)
effect.add_source("Mage: The Ascension Second Edition", 215)
effect, _ = Effect.objects.get_or_create(name="The Rush", prime=1)
effect.description = (
    "This rote allows the mage to store more Quintessence than their avatar rating."
)
effect.save()
effect.add_source("Mage: The Ascension First Edition", 210)
effect.add_source("Mage: The Ascension Second Edition", 214)
effect, _ = Effect.objects.get_or_create(name="Sense Quintessence", prime=1)
effect.description = "This rote allows the mage to sense free Quintessence, particularly any source of Quintessence or any magickal effect."
effect.save()
effect.add_source("Mage: The Ascension First Edition", 210)
effect.add_source("Mage: The Ascension Second Edition", 214)
effect, _ = Effect.objects.get_or_create(
    name="Spinning Thread", spirit=2, forces=3, prime=2
)
effect.description = 'Allows the Weaver to pull esoteric things, such as "the shriek of a thrice cursed ifrit" and convert it into a physical form, Tass.'
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 91)
effect, _ = Effect.objects.get_or_create(
    name="Delay Paradox", time=3, spirit=3, prime=3
)
effect.description = "The Taftani tend to accrue large amounts of paradox. Their very survival has depended on being able to find ways to mitigate the damage that it does. With this rote, the Taftani can delay the full backlash, and cause their Paradox to accrue at a rate of at most one per day, with a number of days equal to the number of successes in between points. This spreads out the damage and allows the Taftani to avoid a single, large paradox backlash."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 89)
effect, _ = Effect.objects.get_or_create(name="Flames of Purification", prime=4)
effect.description = "The Flames of Purification is a direct attack on the target's Pattern, attempting to dissolve the Pattern and return the Quintessence that makes it up to the universe. Optionally, some of that Quintessence can be captured by the mage for other purposes."
effect.save()
effect.add_source("Mage: The Ascension First Edition", 211)
effect.add_source("Mage: The Ascension Second Edition", 215)
effect.add_source("Mage: The Ascension Revised", 184)
effect, _ = Effect.objects.get_or_create(name="Healthy Skepticism", entropy=3, mind=2)
effect.description = "The Technocrat using this provides a logical explanation for why some supernatural effect is impossible, causing them to count as a witness for vulgar mystical effects."
effect.save()
effect.add_source("Guide to the Technocracy", 209)
effect, _ = Effect.objects.get_or_create(name="Holy Stroke", prime=2)
effect.description = "By spending a point of Quintessence, the mage can attack something directly with a bolt of pure, primal energy."
effect.save()
effect.add_source("Mage: The Ascension Revised", 183)
effect, _ = Effect.objects.get_or_create(name="Matter-Energy Converter", prime=2)
effect.description = "This Procedure is focused through an energy weapon and disrupts Life Patterns. The simpler version merely causes effects like Rubbing of Bones, which is painful but causes no damage. The more advanced version can directly destroy a living Pattern."
effect.save()
effect.add_source("Technocracy: Void Engineers", 48)
effect, _ = Effect.objects.get_or_create(name="Paradox Ward", prime=5)
effect.description = "The Master of Prime can invest Quintessence into an object, doing so with great care and attention to detail, and in doing so, smooth out the universe for them, canceling out Paradox that they have (or will) accumulate."
effect.save()
effect.add_source("Mage: The Ascension Revised", 185)
effect, _ = Effect.objects.get_or_create(
    name="Penance for the Sicarii", correspondence=3, prime=4
)
effect.description = "In Chorister legends, there are two groups of monks, White and Red. The Red Monks brought justice and righteousness to the world without fear, because the White Monks took the paradox intended for them. This rote allows a mage to take on another's paradox as it hits. With Time, the effect can be cast well in advance rather than needing to cast it at the time."
effect.save()
effect.add_source("Tradition Book: Celestial Chorus (Revised)", 58)
effect, _ = Effect.objects.get_or_create(name="Quintessence Blast", prime=5)
effect.description = "By supercharging a crystal with Quintessence, a Master of Prime is capable of (temporarily) drawing in and dispelling a Paradox Spirit. The crystal is destroyed, and the mage who does this will surely be remembered by that Paradox Spirit."
effect.save()
effect.add_source("Mage: The Ascension First Edition", 212)
effect.add_source("Mage: The Ascension Second Edition", 215)
effect, _ = Effect.objects.get_or_create(name="Spirit Pilgrimage", life=3, prime=5)
effect.description = "Masters of Prime can stop the flow of Quintessence to parts of their body, causing them to become incorporeal."
effect.save()
effect.add_source("Mage: The Ascension First Edition", 226)
effect, _ = Effect.objects.get_or_create(name="Balancing the Furies", prime=3)
effect.description = "This allows the Akashic to temporarily change the mage's Resonance, or at Prime 5, pass it along to another being."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 71)
effect_charge_the_resonance = Effect.objects.get_or_create(
    name="Charge the Resonance", matter=2, mind=2
)[0]
effect, _ = Effect.objects.get_or_create(name="Node Spike", mind=2, prime=3)
effect.description = "By performing a symbolically painful or poisonous act at a Node, the mage can turn that concentrated pain or hate into a Resonance for the Node that makes it much more difficult to use. Successes are split between duration and strength, with the strength acting as an empathic attack, causing anyone trying to use the Node to feel intense pain, nausea and disorientation if they fail a Willpower roll. With Mind 3, it becomes an actual mental attack, causing damage to anyone trying to use the Node."
effect.save()
effect.add_source("Guide to the Traditions", 281)
effect, _ = Effect.objects.get_or_create(
    name="Occlude the Seal of Power", matter=2, mind=2, prime=4
)
effect.description = "A rote originating among House Bonisagus but spreading to the rest of the Order quickly, this allows the mage to temporarily storing their resonance in an object. The mage lights four pieces of frankincense, breathes deeply 10 times while exhaling onto an object made of some precious substance and speaks the Enochian names of the spheres. At the end, they pass a point of Quintessence into the object, and for the duration of the effect one point of their resonance is on that object."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="Orgone Accumulator", prime=3)
effect.description = "Some Etherites work with the Odyllic Force, stored as Orgone, a representation of the emotional nature of the universe, not just the physical. This allows them to imbue their devices with Resonance. With Prime 3, each success allows a focus to hold two Resonance traits for the duration or until they are used. Prime 5 also gives the benefits of the Fount of Paradise effect."
effect.save()
effect.add_source("Tradition Book: Sons of Ether (Revised)", 62)
effect, _ = Effect.objects.get_or_create(name="Psychic Impression", mind=2)
effect.description = "The mage imparts an emotional signature to a location, granting it a Resonance trait based on the emotion imparted."
effect.save()
effect.add_source("Mage: The Ascension Second Edition", 210)
effect.add_source("Mage: The Ascension Revised", 177)
effect, _ = Effect.objects.get_or_create(name="Tag", correspondence=2, prime=3)
effect.description = "This Chaotician rote marks a person as a criminal in the eyes of the Virtual Adepts. The mark is unseen, but noticeable in the target's Resonance. Each success subtracts one from the difficulty to see it."
effect.save()
effect.add_source("Digital Web", 99)
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 64)
effect, _ = Effect.objects.get_or_create(name="The Ball Game", life=2)
effect.description = "By having the sacrifices play some sort of competitive athletic game, the difficulty of the sacrifice is decreased by one."
effect.save()
effect.add_source("Dead Magic", 76)
effect, _ = Effect.objects.get_or_create(
    name="Blood for the Gods", spirit=3, life=2, prime=1
)
effect.description = "Unlike Heart for Huitzilopochtli, Blood for the Gods makes a sacrifice dedicated to an appropriate deity in exchange for a boost of two to some Attribute or Talent for the duration of the effect. This is a boon from a spirit, bound into the mage with Life rather than acquired through the Better Body rote."
effect.save()
effect.add_source("Dead Magic", 75)
effect, _ = Effect.objects.get_or_create(name="Blood of the Sacred King", prime=3)
effect.description = "This rote allows the Verbena to sacrifice a person in exchange for Quintessence. A Sleeper sacrificed this way gives one Quintessence for each bashing or lethal health level (so 14 in total for an average person). If a mage is sacrificed, this rote can restore a dying Node. For each two dots of Arete, the Node gains one point, rounded up if the mage rolls any 10s, down otherwise. A mage sacrificed in this way cannot be brought back by any means, does not become a ghost, and cannot be contacted in any way. The only remnant of the mage is in the Resonance of the Node."
effect.save()
effect.add_source("Tradition Book: Verbena (Revised)", 65)
effect, _ = Effect.objects.get_or_create(name="Cup of Itz", life=2, prime=1)
effect.description = "Using a large, decorated bowl, the mage pierces their genitalia and allows blood to drain out into the bowl as an offering to the gods. This allows them to gain Quintessence as in Heart's Blood. The Life component of the rote prevents the mage from feeling the pain, preventing wound penalties."
effect.save()
effect.add_source("Dead Magic", 77)
effect, _ = Effect.objects.get_or_create(
    name="Heart for Huitzilopochtli", spirit=5, life=5, prime=5
)
effect.description = "For one of any number of possible reasons, the Aztecs engaged in regular human sacrifice. This rote allows a mage who sacrifices a victim and tears out their heart to generate three points of Quintessence for each success. With five or more successes, the avatar itself of the victim is destroyed to create this Quintessence. The mage gains Entropic synergy: often Death, but if used as part of a fertility ritual, it could be Renewal."
effect.save()
effect.add_source("Dead Magic", 74)
effect, _ = Effect.objects.get_or_create(name="Heart's Blood", prime=1)
effect.description = "The mage can sacrifice their health for Quintessence, at a rate of one point per health level of bashing damage taken."
effect.save()
effect.add_source("Mage: The Ascension Second Edition", 214)
effect.add_source("Mage: The Sorcerer's Crusade", 269)
effect.add_source("Mage: The Ascension Revised", 182)
effect, _ = Effect.objects.get_or_create(name="Kaumaha (Sacrifice)", spirit=2, prime=3)
effect.description = "By throwing a living being into a volcano, a mage can harvest the Quintessence given off by the sacrifice, as in Lambs to the Slaughter."
effect.save()
effect.add_source("Dead Magic 2", 27)
effect, _ = Effect.objects.get_or_create(name="Lanbs to the Slaughter", prime=3)
effect.description = "Though self-sacrifice as in Heart's Blood is preferred by most, a mage can sacrifice others for Quintessence just as they can sacrifice of themselves. This sacrifice can be a material object, an animal, or even a person, but to gain the Quintessence from this rote, the subject (if intelligent) must be willing."
effect.save()
effect.add_source("Mage: The Ascension Revised", 184)
effect, _ = Effect.objects.get_or_create(name="Midnight Oil", prime=1)
effect.description = "This rote allows a member of the Order of Reason to sacrifice their health to get a boost of quintessence."
effect.save()
effect.add_source("Order of Reason", 82)
effect, _ = Effect.objects.get_or_create(name="Self-Sacrifice", prime=1)
effect.description = "The Verbena may make a sacrifice to gain Quintessence. By self-harming, such as cutting runes into their flesh, the mage gains one point of Quintessence for each level of bashing damage taken, and an additional point for each lethal."
effect.save()
effect.add_source("Tradition Book: Verbena (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="Arrest the Flight of Arrows", forces=2)
effect.description = "This rote allows the mage to stop missile weapons from harming the mage. Every success rolled is subtracted from the attack roll for the missile, as the kinetic energy of it is leeched away."
effect.save()
effect.add_source("Tradition Book: Verbena (Revised)", 64)
effect, _ = Effect.objects.get_or_create(
    name="Crowdsourced Combat", correspondence=2, forces=1, mind=1
)
effect.description = "Filtering the fighting techniques of recorded MMA fights, martial arts training videos, military manuals and police reports through Progenitor biomechanical analyses and Iteration X tactical simulations, this Procedure matches the technique to the situation at hand for a Syndicate agent. Each success reduces the difficulty of combat rolls for one ability of the Syndicate Agent's by 1, and successes are divided between combat abilities and then duration."
effect.save()
effect.add_source("Convention Book: Syndicate (Revised)", 72)
effect, _ = Effect.objects.get_or_create(name="Infidel's Laughter", spirit=2, forces=2)
effect.description = "This rote allows the Taftani to reverse the momentum of any attack that comes very close to them, causing bullets and knives to bounce off them. With enough successes, they even retrace their original paths, which can cause bullets to hit the person who fired them."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 89)
effect, _ = Effect.objects.get_or_create(name="Lucky Blow", entropy=2)
effect.description = "This rote allows the mage to detect weaknesses during combat and exploit them. Against normal opponents, successes can be used to decrease the difficulty on a single attack roll or to bypass armor by finding a location that isn't protected. Against non-human opponents, it allows the mage to find the opponents weaknesses, allowing called shots even when the physiology is unfamiliar."
effect.save()
effect.add_source("Order of Reason", 70)
effect, _ = Effect.objects.get_or_create(
    name="Sense the Echo of the Dragon", time=2, mind=3
)
effect.description = "By meditating on an upcoming fight and the opponent's style, this rote allows a mage to predict their opponent's movements in combat. In particular, it gives additional dice on defensive maneuvers."
effect.save()
effect.add_source("Mage: The Ascension First Edition", 226)
effect, _ = Effect.objects.get_or_create(
    name="Spearcatcher Rune", correspondence=1, time=3
)
effect.description = "This rune slows down time as the mage sees a spear coming for them, and they become acutely aware of the location of each projectile. Each success allows them to pluck one projectile from the air. Forces must be used to do this with bullets, to dissipate the heat from the bullets, or else use heat-resistant gloves."
effect.save()
effect.add_source("Dead Magic 2", 98)
effect, _ = Effect.objects.get_or_create(name="Strategy", time=2)
effect.description = "By stopping and taking a moment to think, the mage gains a bonus of -1 difficulty per success on their next attack in the combat, due to gaining an insight into what their opponent is about to do and where they are about to be."
effect.save()
effect.add_source("Order of Reason", 87)
effect, _ = Effect.objects.get_or_create(name="Targeting Computation", correspondence=1)
effect.description = "This allows an Iterator to locate and track their enemies. This procedure removes cover penalties (except for full cover) and reduces the difficulty of the next projectile attack on that target."
effect.save()
effect.add_source("Technocracy: Iteration X", 47)
effect.add_source("Order of Reason", 66)
effect.add_source("Artisan's Handbook", 46)
effect, _ = Effect.objects.get_or_create(
    name="Time-Motion Study", correspondence=1, time=1
)
effect.description = "This Procedure allows an Iterator to analyze their movements and determine the most efficient way to accomplish a task. It gives a bonus of one per success of their next initiative roll."
effect.save()
effect.add_source("Technocracy: Iteration X", 49)
effect, _ = Effect.objects.get_or_create(
    name="Wearing the Bear Shirt", spirit=4, life=3, mind=1
)
effect.description = "Also known as berserking, the mage becomes terrifying in battle. The mage channels the spirit of a bear, borrowing its strength, stamina, and ferocity. For each success, the mage adds one dot to Strength or Stamina or may ignore a level of wound penalties for the scene. Attributes may be increased to legendary levels with this, but at the cost of Permanent Paradox during the duration of the rote."
effect.save()
effect.add_source("Dead Magic 2", 104)
effect, _ = Effect.objects.get_or_create(name="Wrath of God", prime=2)
effect.description = "This effect allows the mage to spend quintessence to turn the damage from an attack against a supernatural creature from non-aggravated to aggravated damage."
effect.save()
effect.add_source("Order of Reason", 82)
effect, _ = Effect.objects.get_or_create(
    name="Battle Rune", correspondence=3, life=4, mind=3
)
effect.description = "This rune turns a group of people into a coordinated and formidable battle group. Each success adds a person to the effect, bringing them to peak physical health, healing all bashing damage at the end of each turn, and halving damage penalties from lethal damage. They also have their temporary Willpower replenished until the end of the scene, at which point they return to their previous level and then lose one."
effect.save()
effect.add_source("Dead Magic 2", 99)
effect, _ = Effect.objects.get_or_create(
    name="Coordinated Fire", correspondence=1, time=1, mind=2
)
effect.description = "By linking several peoples' equipment together and giving good information to their leader, Void Engineers can combine their fire into a single attack. Each success from the team leader allows one more person to be involved in the effect, and then combine their Dexterity + Firearms or Energy Weapons into a single massive dice pool (burst and fully automatic bonuses are only added once), if the target can soak, it may soak once for each weapon used."
effect.save()
effect.add_source("Convention Book: Void Engineers (Revised)", 85)
effect, _ = Effect.objects.get_or_create(name="Hail of Bullets", time=3, forces=2)
effect.description = "This group Procedure causes a collection of New World Order agents to fill the air with an unrealistic number of bullets or lasers. Each member of the group must be using a weapon that has been altered to increase the rate of fire and each success gives an additional attack to the group as a whole."
effect.save()
effect.add_source("Technocracy: New World Order", 48)
effect, _ = Effect.objects.get_or_create(name="Legion's Life", life=2, prime=3)
effect.description = "Requiring a group of at least twenty people who have bonded closely (such as with common military training), the mage can use this bonding to siphon off Quintessence from the group rather than from individuals, not taking much from any single person. For every twenty people in the group, the mage can gain one Quintessence without causing any harm. The mage can pull a maximum of one Quintessence per success on this rote. This draw may be done once per day."
effect.save()
effect.add_source("Dead Magic", 106)
effect, _ = Effect.objects.get_or_create(name="Marching Orders", mind=1)
effect.description = "This Artificer rote comes from attempting to quantify everything involving in military matters. The mage uses this rote before leading others into battle, and the successes from it may be used at various points in that battle to represent superior positioning and morale for the mage's troops."
effect.save()
effect.add_source("Order of Reason", 78)
effect, _ = Effect.objects.get_or_create(name="Mind of the Ant Hill", mind=4)
effect.description = "The Romans were masters of military coordination and devised this technique. For every success, the group has a die that any member can use in combat once. Usually, it is prepared as an extended ritual before battle, using war machines and siege engines as foci and creating a very large pool for the group's use."
effect.save()
effect.add_source("Dead Magic", 107)
effect, _ = Effect.objects.get_or_create(
    name="108 Plum Blossoms", correspondence=2, forces=2
)
effect.description = "By practicing the 108 Plum Blossoms stances, the Wu Lung can obtain preternatural balance. They will only lose their balance on a frictionless surface."
effect.save()
effect.add_source("Dragons of the East", 59)
effect, _ = Effect.objects.get_or_create(
    name="Arashi-Waza", correspondence=2, time=3, forces=2
)
effect.description = "This rote allows an Akashic to move quickly, spinning to gather speed and power and then unleashing their attack on enemies within range. Successes either are spent to increase effective combat dice or allow targets that are usually unreachable to be targeted, but otherwise the mage uses standard multiple-action rules."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 68)
# effect, _ = Effect.objects.get_or_create(name="Bullet Catch", time=2, life=2, forces=2)
# effect.description = "A skilled martial artist can catch many weapons as they are used against them. However, bullets can only be caught that way through the enlightened martial art of Do."
# effect.save()
# effect.add_source("Mage: The Ascension 20th Anniversary Edition", 607)
effect, _ = Effect.objects.get_or_create(name="Dragon Fist", life=3, prime=2)
effect.description = "The Akashic focuses their Chi and their attacks do aggravated damage. Each attack expends a point of Quintessence. The version with just Life works on living opponents by rupturing organs. The version with Forces also causes their fists to burst into flame, burning their targets."
effect.save()
effect.add_source("Book of Shadows", 147)
effect, _ = Effect.objects.get_or_create(name="Eight Drunken Hsien", life=2, mind=3)
effect.description = 'Akashics can use Do to defend against multiple opponents at a time, and make it look like an accident. Often called the "drunken master" technique, the Akashic takes a staggering stance that appears drunk, and though every move is effective, all of them appear to be accidental. The Mind 3 version makes the movements seem accidental, the Entropy and Life version actually randomizes movements, while still directing them at opponents. Each success lowers the Akashic\'s difficulty to hit and increases the difficulty to hit them.'
effect.save()
effect.add_source("Dragons of the East", 50)
effect, _ = Effect.objects.get_or_create(
    name="The Final Blow", life=3, entropy=4, mind=5, prime=3
)
effect.description = "One of the most famous applications of Do, this rote allows the Akashic using it to keep standing beyond the point where they should have died in order to complete a battle. Each success adds an extra health level which, in addition to the spending of a Willpower point, allows the Akashic to continue fighting, even after death. Additional successes are spent on duration."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 68)
effect, _ = Effect.objects.get_or_create(
    name="Flying Dragon Kick", correspondence=1, forces=4
)
effect.description = "With this maneuver, an Akashic can stay aloft even for several minutes of long-distance flight to deliver a flying kick to a target, so long as the target was in sight (including Correspondence) and the mage travels a straight line."
effect.save()
effect.add_source("Book of Shadows", 148)
effect, _ = Effect.objects.get_or_create(name="Focus of the Blow", forces=1, mind=1)
effect.description = "Damage difficulty is decreased by one per success. Furthermore, for the duration, a teacher can tell if the maneuver was employed correctly with complete accuracy."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (First Edition)", 63)
effect, _ = Effect.objects.get_or_create(name="Hands of Death", forces=2)
effect.description = "Either using Life to hit internal organs precisely or Forces to hit harder (or both), this makes the Technocrat much more capable at hand-to-hand combat."
effect.save()
effect.add_source("Technocracy: Syndicate", 48)
effect.add_source("Guide to the Technocracy", 212)
effect.add_source("Mage: The Ascension 20th Anniversary Edition", 601)
effect, _ = Effect.objects.get_or_create(
    name="Long Fist", correspondence=4, forces=3, prime=2
)
effect.description = "This technique focuses the Akashic's Chi to strike additional targets at a rate of one per success. This attack does Forces damage rather than regular punching damage, and the targets may be out of normal reach (up to 3 yards per level of Do) and may punch through objects without damaging them."
effect.save()
effect.add_source("Book of Shadows", 148)
effect, _ = Effect.objects.get_or_create(name="Piercing Cry", matter=3, entropy=3)
effect.description = "This Do technique allows the Akashic to shatter solid objects. One success allows them to break glass, while three or four is enough to crack a wall or heavy door."
effect.save()
effect.add_source("Book of Shadows", 148)
effect, _ = Effect.objects.get_or_create(name="Purifying Step", forces=2)
effect.description = "The Akashic steps forward (or claps hands together) to cause the ground to shake. The Forces version of this rote directly transmits energy through the ground to the target, which can cause direct injury or push them three feet per success in any direction. The Spirit version calls a spirit through the strong step, is a quick but less directed version of Call Spirit."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 66)
effect, _ = Effect.objects.get_or_create(
    name="Repeating Blow", correspondence=3, forces=3, mind=1, prime=2
)
effect.description = "The Akashic spends several rounds attacking and pulling back a blow, storing the energy that they had put into it. For each turn spent this way, the difficulty increases. Up to a maximum of five, each success acts as a multiplier to the damage dice pool when the final blow actually lands. Due to the near impossibility of hitting a moving target with this rote, it is most useful for destroying barriers, vehicles, and other stationary targets."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(name="Righteous Fist", time=4, life=3, mind=4)
effect.description = "Akashics of the Hsien Chuan and Lohan Chuan schools can set the injury from a blow to trigger when they do a proscribed act or think a banned thought. The Akashic strikes the Metal Element pressure point while chanting a portion of the Drahma Sutra, and they can seal away a thought or action, binding the target to take damage should they violate this ban."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="Rolling Hands", forces=1)
effect.description = "When a martial artist makes contact with an opponent, this rote allows them to react more quickly by sensing the opponent's movement extremely finely. This allows a difficulty reduction of 1 per success for any parry or block."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="Screech of the Owl", entropy=3, mind=3)
effect.description = "Often, an Akashic prefers to avoid battle. With this technique, the Akashic can stun up to their Stamina + Intimidation number of opponents, for a number of turns equal to the successes."
effect.save()
effect.add_source("Book of Shadows", 148)
effect, _ = Effect.objects.get_or_create(name="Spirit Wounder", spirit=2)
effect.description = "By focusing their Chi, an Akashic can use Do to harm spirits just as they would humans."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(
    name="Blade Sense", correspondence=1, matter=1, life=1
)
effect.description = "A combination of extra-spatial awareness, physical precision, and a bond with the blade, this gives the fencer a bonus to difficulty on the next parry or attack roll."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 94)
effect, _ = Effect.objects.get_or_create(name="The Hero's Challenge", mind=2)
effect.description = "When a swordsman is outnumbered, a taunt backed by this rote can mock their enemies into coming at them one at a time instead of all at once."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 91)
effect, _ = Effect.objects.get_or_create(
    name="Iron Snake", correspondence=2, forces=2, mind=3
)
effect.description = "Only extremely skilled melee fighters among the Akashics (six dice in Dexterity + Melee) can attempt this rote. With any flexible weapon, such as a chain, rope, or cloth, the mage can entrance their enemy and strike in unexpected ways. This causes the opponent's melee dice pools to decrease by one per success."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 67)
effect, _ = Effect.objects.get_or_create(
    name="Jabarut (The Darwishim Battle Trance)",
    correspondence=1,
    time=3,
    life=3,
    prime=3,
)
effect.description = 'The Ahl-i-Batin goes into a trance for battle, giving rise to legends of the whirling dervish. The rote causes the mage\'s hand-to-hand attacks to do aggravated damage, and beyond the first success, successes are spent on increasing accuracy, damage and gaining extra actions. Furthermore, they will know the location of all their opponents, can spend successes to increase Physical Attributes as in Better Body, or even spend two successes for an extra "Bruised" health level.'
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 41)
effect, _ = Effect.objects.get_or_create(name="Splitting a Cuirass", life=1, entropy=1)
effect.description = "Like Cynical Eye, Splitting the Cuirass allows the user to find flaws in armor, with Life used for natural armor and Matter used otherwise."
effect.save()
effect.add_source("Artisan's Handbook", 48)
effect.add_source("The Swashbuckler's Handbook", 95)
effect, _ = Effect.objects.get_or_create(name="Swordbreaker Rune", forces=2)
effect.description = "With just Forces, this creates a field that redirects kinetic energy around them to protect them from a weapon. With Matter, it makes an enemy's weapon brittle and easily broken."
effect.save()
effect.add_source("Dead Magic 2", 98)
effect, _ = Effect.objects.get_or_create(
    name="Wind-Water Skein", correspondence=3, matter=3, forces=2, prime=2
)
effect.description = "The Wu-Keng creates a bridal gown with a ragged edge with threads still on the needles. By donning the gown, they gain the ability to control these needles. They can go virtually anywhere, and the Wu-Keng has enough control over them to attack, throw, reel-in or immobilize the target. This silk is nearly indestructible."
effect.save()
effect.add_source("Dragons of the East", 66)
effect, _ = Effect.objects.get_or_create(name="Deadaim", forces=1, entropy=1)
effect.description = "Enhances the mage's ability to aim a gun, successes decrease the difficulty of the attack by one per success."
effect.save()
effect.add_source("Initiates of the Art", 81)
effect, _ = Effect.objects.get_or_create(name="Death Ray", entropy=4, prime=2)
effect.description = "What is a Mad Scientist without a Death Ray? There are fundamentally two different kinds of death rays: one that is essentially a laser, focusing energy of some sort at a target. The other is more of a disintegration beam, through some technique or other it sends a black, jagged bolt at the target which disrupts its Pattern directly. With Time 3, either of these can be treated as an automatic weapon. Both versions inflict aggravated damage and requires a successful Dexterity + Firearms roll to hit the target."
effect.save()
effect.add_source("Tradition Book: Sons of Ether (Revised)", 60)
effect, _ = Effect.objects.get_or_create(name="Emit Beam-Ray", forces=3, prime=2)
effect.description = "By efficiently combining several techniques, Iteration X's Time-Motion Managers developed this procedure. It attacks the target with a variety of simple forces: microwaves attack with heat, a laser attempts to burn and blind, noise can deafen, and X-rays have little immediate effect, but if the target survives the short term, can cause cancer."
effect.save()
effect.add_source("Technocracy: Iteration X", 49)
effect, _ = Effect.objects.get_or_create(name="Golden Gunman", time=3, forces=2)
effect.description = "When dual-wielding firearms and making a dramatic entrance, the Technocrat can get off an extra shot each turn for each success. As an option, successes can be spent to increase damage."
effect.save()
effect.add_source("Guide to the Technocracy", 216)
effect.add_source("Mage: The Ascension 20th Anniversary Edition", 605)
effect, _ = Effect.objects.get_or_create(name="Grand Salvo", forces=2)
effect.description = "Increases the damage from any weapon that fires off at least five attacks within a single round. For every two successes, an additional shot can be fired."
effect.save()
effect.add_source("Artisan's Handbook", 50)
effect, _ = Effect.objects.get_or_create(name="Holdout Weapon", matter=3, prime=2)
effect.description = "With this Procedure, an Agent can materialize a small, easily concealed weapon, particularly useful in desperate situations."
effect.save()
effect.add_source("Technocracy: New World Order", 49)
effect.add_source("Guide to the Technocracy", 213)
effect, _ = Effect.objects.get_or_create(name="Hot-Shotting", forces=3)
effect.description = "Sometimes, conspiracy and cover up fail and the only solution is to start shooting. Hot-Shotting makes that significantly easier, allowing the Technocrat to add successes to their damage on the next gunshot."
effect.save()
effect.add_source("Guide to the Technocracy", 210)
effect.add_source("Mage: The Ascension 20th Anniversary Edition", 601)
effect, _ = Effect.objects.get_or_create(name="Laserblast", forces=3, prime=2)
effect.description = "A direct Forces attack, via a laser fired from an energy weapon."
effect.save()
effect.add_source("Technocracy: Void Engineers", 48)
effect, _ = Effect.objects.get_or_create(name="Magic Bullet", forces=2, entropy=2)
effect.description = "For those Euthanatos more comfortable with modern technology, this rote allows them to fire a bullet and cause chance to break just right for it to hit multiple targets, ricochet in unpredictable ways, or otherwise behave unexpectedly. In particular, it allows the mage to hit additional targets with the same bullet."
effect.save()
effect.add_source("Tradition Book: Euthanatos (Revised)", 61)
effect, _ = Effect.objects.get_or_create(
    name="Ricochet", correspondence=1, time=1, matter=1, forces=1
)
effect.description = "When defending against an incoming missile attack slower than a bullet, the successes are subtracted before determining if it hits. The Akashic is using Do to track the attack and deflect it. If the number of successes is greater than that of the attacker, the Akashic has the choice to try to deflect the attack back at the source."
effect.save()
effect.add_source("Hidden Lore", 12)
effect, _ = Effect.objects.get_or_create(name="Rudra's Bow", life=3, forces=2)
effect.description = "The Euthanatos calls upon the archers of legend (Rudra in India, Artemis in Greece, etc.) to make their bow supernaturally powerful. Other spheres may be invoked for additional effects, but the core effect is that each success adds two dice of aggravated damage (via Life 3) as anyone hit by the arrows fired from the bow is immediately attacked by vicious, fast-acting disease."
effect.save()
effect.add_source("Tradition Book: Euthanatos (Revised)", 61)
effect, _ = Effect.objects.get_or_create(name="The Swift Lock", forces=2)
effect.description = (
    "Increases a flintlock firearm's rate of fire by one turn per shot."
)
effect.save()
effect.add_source("Artisan's Handbook", 49)
effect, _ = Effect.objects.get_or_create(name="Tamping", forces=2)
effect.description = "An Artificer rote, the mage measures out and uses extra black powder (in Dark Fantastic era weapons, other techniques are required for modern weapons) to improve the effectiveness of the firearm and increase the size of the damage dice pool by one per success."
effect.save()
effect.add_source("Order of Reason", 71)
effect, _ = Effect.objects.get_or_create(name="Tension", forces=2)
effect.description = "An old Artificer trick for reloading crossbows faster: with three successes, the number of rounds to reload the weapon is decreased by one."
effect.save()
effect.add_source("Order of Reason", 72)
effect, _ = Effect.objects.get_or_create(
    name="Trickshot", correspondence=1, forces=1, entropy=1, mind=1
)
effect.description = "With Trickshot, the mage can arrange nearly impossible shots effectively. Successes subtract from the difficulty of the next shot the mage fires."
effect.save()
effect.add_source("Initiates of the Art", 81)
effect, _ = Effect.objects.get_or_create(name="Bloodsight", life=1)
effect.description = "This rote allows a Verbena to sense how healthy a person or animal is, what diseases or injuries they might have, if they are pregnant, how old they are, anything directly tied to their physical state."
effect.save()
effect.add_source("Tradition Book: Verbena (First Edition)", 63)
effect, _ = Effect.objects.get_or_create(
    name="Conclave Wellness Works", life=1, entropy=2, mind=2
)
effect.description = "At the start of a season, the Sisters of Hippolyta burn incense and sing to welcome it and extend their perceptions to the whole community, sensing the health and mental state of everyone. This alerts them to any problems or illnesses."
effect.save()
effect.add_source("Book of Crafts", 88)
effect, _ = Effect.objects.get_or_create(name="Detect Mental Anomalies", mind=1)
effect.description = "The Void Engineer can perform a quick mental scan and determine if someone's mind has been tampered with or altered in some way, as well as detecting mental illness."
effect.save()
effect.add_source("Technocracy: Void Engineers", 44)
effect, _ = Effect.objects.get_or_create(name="Examine Humors", life=1)
effect.description = "A Cosian rote, by examining the patient's body fluids, insight can be gained into the patient's health issues. Each success gives a -1 difficulty on a medicine roll for diagnostic purposes. With Mind 2 added, the mage can gain insight into any unusual issues with the patient's temperament."
effect.save()
effect.add_source("Order of Reason", 73)
effect, _ = Effect.objects.get_or_create(name="Prayer of Healing Revelation", life=1)
effect.description = "Allows the mage to detect injuries in the target."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 198)
effect.add_source("Mage: The Ascension (Second Edition)", 201)
effect.add_source("Mage: The Ascension (Revised)", 170)
effect, _ = Effect.objects.get_or_create(name="Accidental Overdose", matter=4, life=4)
effect.description = "This rote directly transforms inorganic material in the target's blood stream into a drug, causing them to react as though they'd ingested it. This usually leads to an overdose."
effect.save()
effect.add_source("World of Darkness: Outcasts", 90)
effect, _ = Effect.objects.get_or_create(name="Adaptive Chemistry", matter=3, prime=2)
effect.description = "This tends to act as an emergency chemistry kit. With it, a Progenitor is able to change one drug into another so that they always have the right tool for the job. Some less ethical Scientists have used it to alter poisons in a victim's system to destroy evidence of murder."
effect.save()
effect.add_source("Convention Book: Progenitors (Revised)", 72)
effect, _ = Effect.objects.get_or_create(name="Cinnabar Tears", matter=2, life=3)
effect.description = "The Akashic ingests a tiny amount of a poison, which then alchemically transforms some body fluid within the Akashic into that poison. The Akashic is immune to the poison they create, and generally the toxin will do one level of damage per success in addition to the damage from a strike."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="DMSO", matter=3, life=3, prime=2)
effect.description = "DMSO, or dimethyl sulfoxide, is a chemical that opens the pores on the skin (often used in contact poisons). This procedure causes the Technocrat's touch to have the same effect, which causes anything on the victim's or Technocrat's skin to seep inside, often causing illness and sometimes death."
effect.save()
effect.add_source("Guide to the Technocracy", 212)
effect, _ = Effect.objects.get_or_create(
    name="Drug Enhancement", matter=2, life=2, prime=1
)
effect.description = "Progenitors can get more out of even mundane drugs, and this rote doubles the benefits without changing the drawbacks of them."
effect.save()
effect.add_source("Technocracy: Progenitors", 44)
effect.add_source("Convention Book: Progenitors (Revised)", 72)
effect, _ = Effect.objects.get_or_create(name="Experience Substance", matter=1, mind=2)
effect.description = "This rote allows a mage to experience the mental effects of a drug or substance without having to consume it. This is most effective for stimulants, hallucinogens and narcotics, as more physically active drugs don't work."
effect.save()
effect.add_source("Hidden Lore", 17)
effect, _ = Effect.objects.get_or_create(name="Good Eatin'/Cleanse the Clown", life=2)
effect.description = "Life kills any parasites that might be in food, Matter purifies it and improves the taste. A very useful effect for mages living on the street."
effect.save()
effect.add_source("Orphan's Survival Guide", 124)
effect, _ = Effect.objects.get_or_create(
    name="Manufacture Enlightened Drugs", matter=3, life=3, prime=3
)
effect.description = 'This allows the creation of enlightened drugs. Each dose requires five points of Prime Energy which are transferred to the user. For common examples see "Enlightened Drugs" in Convention Book: Progenitors (Revised) on page 73.'
effect.save()
effect.add_source("Technocracy: Progenitors", 44)
effect.add_source("Convention Book: Progenitors (Revised)", 73)
effect, _ = Effect.objects.get_or_create(name="Metabolic Mastery", life=5)
effect.description = "Now, the Progenitor can create the effects of any drug, poison, or metabolic product, even if it isn't present. This is possible through direct manipulation of the body's receptors."
effect.save()
effect.add_source("Technocracy: Progenitors", 44)
effect, _ = Effect.objects.get_or_create(
    name="Persephone's Nectar", correspondence=3, matter=2, life=3
)
effect.description = "A signature of the Golden Chalice, this rote turns any ordinary liquid into a poison specific to the target of the effect. Some variants may mystically age targets, put them to sleep, or induce visions, but the most common use is to kill the target. Correspondence is used to tie it to the Pattern of the specific target, so that it cannot harm anyone else."
effect.save()
effect.add_source("Tradition Book: Euthanatos (Revised)", 62)
effect, _ = Effect.objects.get_or_create(name="The Poison Maiden", life=4)
effect.description = "The subject is first made immune to a poison, and then their biochemistry is altered so that they secrete it, exhaling it with each breath and sweating it from their pores. Each success spent on duration makes it last for a month, and for five successes it can be made permanent."
effect.save()
effect.add_source("Book of Shadows", 146)
effect, _ = Effect.objects.get_or_create(name="Polysorbate", life=2, mind=2, prime=1)
effect.description = 'By persuading someone that they have gotten a "bad batch" of some chemical that\'s common in food, a Progenitor can cause one of any number of effects, with the following examples: the food they ate is not filling, and they are hungry again an hour later; lethargy and inaction.'
effect.save()
effect.add_source("Guide to the Technocracy", 211)
effect, _ = Effect.objects.get_or_create(name="Purge", life=2)
effect.description = "This rote allows a mage to clean a target out of drugs or illnesses. Life 2 is enough for themselves, Life 3 for another target."
effect.save()
effect.add_source("Orphan's Survival Guide", 125)
effect, _ = Effect.objects.get_or_create(name="Purging the System", matter=3, life=3)
effect.description = "This rote cures physical substance addiction."
effect.save()
effect.add_source("World of Darkness: Outcasts", 91)
effect, _ = Effect.objects.get_or_create(name="Purify", life=3)
effect.description = "This rote allows a Cultist to flush drugs, poisons, and diseases out of the target's body. Matter allows them to remove drugs or poisons, Life allows them to remove diseases other than the worst (such as HIV and Cancer, which only go into remission), and both can, of course, do both."
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (First Edition)", 66)
effect, _ = Effect.objects.get_or_create(name="Sustenance Pill", life=3, prime=2)
effect.description = "A Technocrat properly prepared can take one of these pills and not need food or rest for a number of days equal to the successes they roll."
effect.save()
effect.add_source("Hidden Lore", 52)
effect, _ = Effect.objects.get_or_create(
    name="Taking Poison for the Enemy", correspondence=2, matter=2, life=2
)
effect.description = "The Batini can build upon the similarities between them and their victim so that poison that they ingest affects the target instead."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 44)
effect, _ = Effect.objects.get_or_create(name="Tolerance", life=2, mind=1)
effect.description = "This rote allows a Cultist to regain control of themselves despite whatever methods they've used to alter their consciousness. Usually through some sort of meditative technique, they use Mind to regain self-control and Life to purge their body of the aftereffects of their trip. If the trip is bad enough to cause bashing or lethal damage, Tolerance can give the Cultist soak dice."
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (Revised)", 72)
effect, _ = Effect.objects.get_or_create(name="Witch's Diplomacy", matter=2, life=3)
effect.description = "Creates a deadly poison that the mage can then attempt to get into their target. Other spheres can be used to give other effects to the poison, almost any effect that those spheres can manage."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 93)
effect, _ = Effect.objects.get_or_create(name="Accelerated Aging", time=3, life=3)
effect.description = "Progenitors have developed a chemical compound that, when ingested, causes the subject to age five years. Without weekly maintenance, however, the subject will return to their natural age after a month."
effect.save()
effect.add_source("Convention Book: Progenitors (Revised)", 72)
effect, _ = Effect.objects.get_or_create(name="Allergic Reaction", life=4, prime=2)
effect.description = "Triggers an allergic reaction in the target. It can range from an irritating rash or a stuffy nose to death, depending on the damage dealt by the effect."
effect.save()
effect.add_source("World of Darkness: Outcasts", 90)
effect, _ = Effect.objects.get_or_create(
    name="Ana'ana (The Death Prayer)", correspondence=3, life=3
)
effect.description = "By chanting out why they want a target to die while drumming a martial rhythm, Polynesian mages cause them to become ill, and badly enough that they only have a limited time to persuade the mage to call off the attack, whether direct of via a spirit."
effect.save()
effect.add_source("Dead Magic 2", 27)
effect, _ = Effect.objects.get_or_create(
    name="Blight of Aging", life=4, entropy=4, prime=3
)
effect.description = "Subtle versions of this effect can cause old wounds to reopen, the target to fall victim to diseases or even fall into a coma. More blatant versions cause them to age instantly."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 193)
effect.add_source("Mage: The Ascension (Second Edition)", 195)
effect.add_source("Mage: The Ascension (Revised)", 164)
effect, _ = Effect.objects.get_or_create(
    name="Bone Twisting Palm", life=4, entropy=4, prime=3
)
effect.description = "This rote has two forms. Both twist the target's bones until they break, harming the target and often leaving them disabled without magical healing. One version is attempting to cause as much damage as possible, and it does aggravated damage. The other is instead attempting to cause permanent disability, in which case lethal damage is done, but for the duration of the effect, the limbs being twisted are useless."
effect.save()
effect.add_source("Book of Shadows", 141)
effect, _ = Effect.objects.get_or_create(name="Curseof the Mayfly", life=4, entropy=4)
effect.description = "This effect ages the target by three years per success."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 222)
effect, _ = Effect.objects.get_or_create(
    name="Destructive Genegineering", life=3, entropy=3
)
effect.description = "Quick and dirty genetic engineering allows the Progenitor to inflict the target with genetic disorders. Each day, the target rolls Stamina at difficulty 7. Success rejects the mutation. Otherwise, all activities that could be hampered by the mutation have difficulty 2 higher."
effect.save()
effect.add_source("Convention Book: Progenitors (Revised)", 73)
effect, _ = Effect.objects.get_or_create(name="Fluids of Death", life=4, entropy=4)
effect.description = (
    "The mage can brew a potion that causes anything it touches to wither and die."
)
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 224)
effect, _ = Effect.objects.get_or_create(name="Fuck Off/Fuck Off and Die", mind=2)
effect.description = "The gentler version allows the mage to give someone a look that causes them to want to get away unless they succeed on a Willpower roll. The stronger version additionally does aggravated damage in the form of heart failure and brain hemorrhage if the victim fails their Willpower roll."
effect.save()
effect.add_source("Orphan's Survival Guide", 124)
effect, _ = Effect.objects.get_or_create(name="Heart Murmurs", entropy=4)
effect.description = "The human body is an incredibly delicate and complex system. By injecting chaos into it, this system can be broken down, causing damage. The mage has no control over what sort of damage is done without Life."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 195)
effect, _ = Effect.objects.get_or_create(name="Little Good Death", life=2)
effect.description = "This rote allows the mage to attack simple creatures. Essentially a variant on Rip the Man-Body."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 198)
effect.add_source("Mage: The Ascension (Second Edition)", 202)
effect, _ = Effect.objects.get_or_create(name="Rip the Man-Body", life=3)
effect.description = "This allows the mage to attack the Pattern of a complex lifeform, such as a person, directly."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 200)
effect.add_source("Mage: The Ascension (Second Edition)", 203)
effect.add_source("Mage: The Ascension (Revised)", 171)
effect, _ = Effect.objects.get_or_create(
    name="Simulate Inborn Errors of Metabolism", life=4, entropy=4
)
effect.description = "The Genegineer can cause someone to contract a temporary and severe genetic disease, which lasts for one hour per success. Virtually any genetic disease can be created in this way."
effect.save()
effect.add_source("Technocracy: Progenitors", 44)
effect, _ = Effect.objects.get_or_create(
    name="Spy's Stigmata", correspondence=1, life=2, prime=2
)
effect.description = "Causes a target that is attempting to spy on the mage to get a rash in some mark of the mage's choice. This rash is visible and remains until healed with Life 2."
effect.save()
effect.add_source("Hidden Lore", 13)
effect, _ = Effect.objects.get_or_create(name="Witch's Vengeance", entropy=4)
effect.description = "Either ages the target or damages them directly and can do so at a distance with Correspondence."
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 273)
effect.add_source("Mage: The Ascension 20th Anniversary Edition", 610)
effect, _ = Effect.objects.get_or_create(name="Aphrodite's Blessing", life=2)
effect.description = "Without dulling the sensations caused by an extreme environment, the Cultist continually repairs any damage that it causes."
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (First Edition)", 65)
effect, _ = Effect.objects.get_or_create(name="Chirurgeon", life=3)
effect.description = "This rote has identical effects to Rapid Healing but can be used on a patient in the mage's care."
effect.save()
effect.add_source("Order of Reason", 74)
effect, _ = Effect.objects.get_or_create(
    name="Distill the Azoth Elixir", matter=2, life=5, prime=3
)
effect.description = "A closely guarded secret, this rote allows Hermetics to create Azoth, a liquid that captures the pure essence of life. Azoth can heal any injury, cure any disease, and even restore the recently dead to life. It can be bottled and stored for up to a week before it loses its potency. For each success, the mage must spend one Quintessence to distill one dram of Azoth. Each dose can heal three levels of aggravated damage, ten doses can restore a person who died recently (what this means is a judgment call for the Storyteller), though a person resurrected this way is just a husk. It is rumored that with Mind and Spirit magick, a greater Azoth could be distilled that solves this problem, but many consider this to just be a legend."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (First Edition)", 67)
effect, _ = Effect.objects.get_or_create(name="Ease of Passage", life=4)
effect.description = "This rote allows the mage to assist a childbirth, decreasing the risks without otherwise altering the experience of birth."
effect.save()
effect.add_source("Book of Crafts", 89)
effect, _ = Effect.objects.get_or_create(
    name="Hajjaj", correspondence=3, life=3, mind=2
)
effect.description = "This rote, in general, allows the Batini to steal the health of others, and is considered an extreme and unpopular technique. The normal use causes the target to start wasting away, and whenever they lose a health level, the Batini gains one. With Time 4 to trigger it, the rote can also be used to frustrate a Vampire: whenever they draw blood from the mage, it immediately returns, preventing them from feeding or embracing the mage."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 41)
effect, _ = Effect.objects.get_or_create(name="Heal Self", life=2)
effect.description = "This allows the mage to heal themselves of damage, at one success per health level. Aggravated damage requires the expenditure of Quintessence."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 199)
effect.add_source("Mage: The Ascension (Second Edition)", 202)
effect.add_source("Mage: The Ascension (Revised)", 170)
effect, _ = Effect.objects.get_or_create(name="Heal Simple Creature", life=2)
effect.description = "The mage can repair virtually any injury or disease in a simple life form, which covers almost all plants and animals other than humans."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 199)
effect.add_source("Mage: The Ascension (Second Edition)", 202)
effect, _ = Effect.objects.get_or_create(name="Healer Rune", life=1)
effect.description = "This rune song makes the mage a more effective healer by letting them see the injury or illness directly. At higher levels, it can directly heal greater and greater injuries, and with Mind instead of Life, can cure mental illnesses and traumas as well."
effect.save()
effect.add_source("Dead Magic 2", 98)
effect, _ = Effect.objects.get_or_create(name="Healing Figurine", life=3)
effect.description = "By making a carved figure to hold healing energies, the mage can accelerate healing for a target who sleeps in the same room as the figurine."
effect.save()
effect.add_source("Dead Magic", 29)
effect, _ = Effect.objects.get_or_create(
    name="Healing Slumber", spirit=2, life=3, mind=2
)
effect.description = "The simplest version heals the target and gives them good dreams and good spirit energy. With Mind 4, mental illness can be healed, and with Spirit 4 possession can be healed."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (First Edition)", 67)
effect, _ = Effect.objects.get_or_create(name="Massage Therapy", life=3)
effect.description = "The mage can cure almost any wound, ache, or blemish from their subject with Life, or mental trauma with Mind, through a massage with special oils and herbs."
effect.save()
effect.add_source("Book of Crafts", 89)
effect, _ = Effect.objects.get_or_create(name="Mukashuan", life=3)
effect.description = "Caribou have been associated with healing among the Inuit for generations. Using Caribou marrow, the mage can heal the subject. With spirit, a helper is summoned and induced to aid in the recovery. Particularly lucky mages may even get help from Caribou Master, healing the patient instantly."
effect.save()
effect.add_source("Dead Magic", 131)
effect, _ = Effect.objects.get_or_create(name="Rapid Healing", life=2)
effect.description = "With proper care, the caster can heal from bad injuries in a matter of days, rather than months. For each success, the mage can heal a level of non-aggravated damage at a maximum rate of one per day. Aggravated damage is only healed on a successful Stamina roll (difficulty 8) and does get a dice pool penalty due to the injuries, as well as needing to spend quintessence. This cannot heal any injury that is truly impossible to heal naturally: if a character loses a limb, this rote is of little help."
effect.save()
effect.add_source("Order of Reason", 73)
effect, _ = Effect.objects.get_or_create(name="Serene Temple", life=2, mind=1)
effect.description = "This rote allows the mage to change the speed at which their body (and mind) operate. They can speed it up to flush toxins or improve healing, but they can also slow it down to control bleeding, endure extreme temperature, or fake death."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 226)
effect, _ = Effect.objects.get_or_create(name="Stay the God's Hand", life=1, entropy=1)
effect.description = "Two rotes commonly used together by Babylonian physicians, the first (with Life 1) attempts to diagnose the source of a malady, usually determining which god the target has gained the disfavor of. The second (with Life 3) attempts to heal it."
effect.save()
effect.add_source("Dead Magic", 52)
effect, _ = Effect.objects.get_or_create(name="Surpu", spirit=2, life=3)
effect.description = "Although purification rituals for specific illnesses were known to the Babylonians, there were many ailments they could not identify. This catch-all ritual begins by listing all possible sins the subject has committed to ensure that the cause of the subject's illness is included, then an object is slowly dismantled and burned, often an onion burned layer by later. For each success, the symptoms disappear for one day, but they return afterwards."
effect.save()
effect.add_source("Dead Magic", 55)
effect, _ = Effect.objects.get_or_create(name="Trauma", life=3)
effect.description = "A Cosian technique for emergency medicine, if the mage can get to the injured party quickly, within a few rounds of the injury occurring, this makes the injury significantly less than it first appeared to be. Each success can heal one level of damage (and as usual, aggravated damage requires quintessence to heal)."
effect.save()
effect.add_source("Order of Reason", 74)
effect, _ = Effect.objects.get_or_create(
    name="Trauma Transmission", correspondence=2, life=4
)
effect.description = 'Darkly referred to as "Rip the Clone Body," this Procedure relies on the common DNA between a Technocrat and their clone, this displaces all injuries from the Technocrat onto all existing clones of the Technocrat. Adding Prime makes the damage aggravated and Dimensional Science is necessary to target any off-world clones.'
effect.save()
effect.add_source("Convention Book: Progenitors (Revised)", 74)
effect, _ = Effect.objects.get_or_create(name="Adjust Major Anomalies", mind=3)
effect.description = "Thanks to the innovation of Dream therapy, where the Void Engineer enters the patient's dreams, it is possible to repair significant mental damage. Some examples include extended, forced service to a Marauder, long-term Domination or Presence, and even mundane forms of brainwashing."
effect.save()
effect.add_source("Technocracy: Void Engineers", 44)
effect, _ = Effect.objects.get_or_create(name="Adjust Minor Anomalies", mind=2)
effect.description = "This allows a Void Engineer to repair minor mental damage, such as brief contact with a Marauder, enchantment by one of the Fae, or a Vampire's Dominate."
effect.save()
effect.add_source("Technocracy: Void Engineers", 44)
effect, _ = Effect.objects.get_or_create(name="Help Rune", mind=1, prime=1)
effect.description = "This rune fortifies the user's soul, gaining them temporary Willpower points for the duration of the scene. At the end of the scene, the mage is left with two fewer Willpower points than when they began. With Prime 2, the mage gains the benefits of Holy Stroke, and with Prime 5, they can throw raw destruction at their enemies."
effect.save()
effect.add_source("Dead Magic 2", 97)
effect, _ = Effect.objects.get_or_create(name="Physiological Rule", life=4)
effect.description = "The Progenitor has precision control over the biochemistry of themselves and others. They can destroy cells in specific locations, cause changes to cellular structure (such as permeability, which can result in dehydration) and can cause various changes in neurochemistry."
effect.save()
effect.add_source("Technocracy: Progenitors", 44)
effect, _ = Effect.objects.get_or_create(name="Quietsong", entropy=1, mind=2)
effect.description = "The mage can enter (perception only at Mind 2, communication at 3) the interior reality of a mage in Quiet."
effect.save()
effect.add_source("Hidden Lore", 13)
effect, _ = Effect.objects.get_or_create(name="Branding the Heart", forces=2, mind=2)
effect.description = "Uses a cold branding iron to give the target the sensation of being branded, including the feeling of being burned and damage that can render them unconscious."
effect.save()
effect.add_source("Artisan's Handbook", 52)
effect, _ = Effect.objects.get_or_create(name="Buzz", prime=2)
effect.description = "A Nephandi version of Rubbing of Bones, but it stimulates the target rather than pains them. This is used to try to make them think positively towards the Nephandus."
effect.save()
effect.add_source("Hidden Lore", 48)
effect, _ = Effect.objects.get_or_create(name="Counter-Irritant", life=2)
effect.description = "By applying a cauterizing instrument to a wound, the mage drives out the pain from the injury with the subject's scream. The turn after this is completed, the subject no longer suffers wound penalties from this injury for the duration of the effect. The mage may also use successes to decrease healing time for the wound."
effect.save()
effect.add_source("Dead Magic", 27)
effect, _ = Effect.objects.get_or_create(
    name="The Curse of Consequences", spirit=1, mind=3
)
effect.description = "Given the damage that their enemies do, often in ignorance, the Dreamspeakers developed this rote to force them to understand the consequences of their actions. The target makes a Willpower roll of difficulty 5 + the Dreamspeaker's arete in order to do anything other than suffer as they are forced to, all at once, experience the misery that their actions have caused to various spirits."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (Revised)", 66)
effect, _ = Effect.objects.get_or_create(name="Curse of Macha", life=2)
effect.description = "Named for an Irish goddess who gave birth immediately after being forced to run a foot race against a horse, this rote allows a Verbena to visit the pain of childbirth onto the target."
effect.save()
effect.add_source("Tradition Book: Verbena (Revised)", 66)
effect, _ = Effect.objects.get_or_create(
    name="Degree Absolute", correspondence=4, mind=5
)
effect.description = "This Procedure places a captured target into a lifelike virtual reality, tailored to the needs of the Agent performing the procedure."
effect.save()
effect.add_source("Technocracy: New World Order", 50)
effect, _ = Effect.objects.get_or_create(name="Dukhamarana Moksa", life=3, entropy=4)
effect.description = "Also called Release of Agonizing Death, this rote is used when a Euthanatos deems someone worthy of a particularly painful death. Not only does it do unsoakable aggravated damage, but the wounds caused won't heal without active mystical intervention, as the target's ability to replenish their Pattern has itself been destroyed. Anyone killed with this effect turns into a lifeless dust and cannot be recreated. If the target is killed, the user gains a trait of Entropic Synergy."
effect.save()
effect.add_source("Tradition Book: Euthanatos (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="Endless Parchment", life=3, prime=2)
effect.description = "An effect whose only purpose is to torture the victim. Minor demons are invoked, and the victim is flayed alive. Every time skin is pulled away; however, new skin grows to replace is, allowing the flaying to begin again and again."
effect.save()
effect.add_source("Infernalism: The Path of Screams", 86)
effect, _ = Effect.objects.get_or_create(name="General Anesthesia", life=1, mind=1)
effect.description = "Etherites with an interest in medicine quickly determined that taking away pain improves performance. This rote allows them to ignore one level of wound penalties per success."
effect.save()
effect.add_source("Tradition Book: Sons of Ether (First Edition)", 63)
effect, _ = Effect.objects.get_or_create(name="Knock Out", mind=3, prime=2)
effect.description = "Most Etherites prefer to avoid combat, but sometimes it is unavoidable. This combines the Prime effect Rubbing of Bones with Mind to stun the target for two rounds per success. This is resisted with Willpower, difficulty 8, and each success on this roll cancels one on the Etherite's."
effect.save()
effect.add_source("Tradition Book: Sons of Ether (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(name="Prolong Pleasure/Pain", time=3, mind=3)
effect.description = "The Cultist creates a simple time loop, causing the subject to experience the action setting into motion for as long as the magic lasts. To focus through it, the subject needs to make a Willpower roll with difficulty determined by the strength of the stimulus, +1 for each hour. Any new strong sensation cancels the effect."
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (First Edition)", 66)
effect, _ = Effect.objects.get_or_create(name="Rubbing of Bones", prime=2)
effect.description = "Though it causes no permanent harm, any disruption or ripple in the Quintessence in a Pattern causes intense pain. This rote does that to a target. This disables the character for the duration, though Willpower points may be spent to act."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 211)
effect.add_source("Mage: The Ascension (Second Edition)", 215)
effect, _ = Effect.objects.get_or_create(name="Turkey Basting", life=3, mind=3)
effect.description = "By describing the tortures that the Syndicate agent could do to the target, they lock them into a mental loop where they feel all those tortures and more, without taking any actual damage. To maintain control, the victim needs to roll Willpower with difficulty 5 + the number of success on Turkey Basting. Failing this roll causes the victim to tell them anything they want to know, and botching drives them insane from the torture. Each hour the victim loses a Willpower point and rolls again."
effect.save()
effect.add_source("Technocracy: Syndicate", 48)
effect, _ = Effect.objects.get_or_create(name="Stop-Gap Resurrection", life=4, mind=4)
effect.description = "Once, for one minute per success, this procedure can restore the dead (temporarily) to life. Most often, this is used to get reliable eyewitnesses for investigations."
effect.save()
effect.add_source("Convention Book: Progenitors (Revised)", 74)
effect, _ = Effect.objects.get_or_create(name="Waters of the Well of Life", life=5)
effect.description = "For a subject who has been dead for fewer hours than the Verbena's Arete, with at least four successes, the Verbena can restore the subject to life. They return with only a single health level and must recover normally. This effect is always vulgar."
effect.save()
effect.add_source("Tradition Book: Verbena (Revised)", 68)
effect, _ = Effect.objects.get_or_create(name="Gift of Prana", life=2, prime=3)
effect.description = "By meditating on the Great Wheel and focusing on the flow of Prana (life-energy), a Euthanatos may grant health to their allies. This rote requires a point of Quintessence, and each success creates two temporary health levels. At the end of the duration, if the target is injured and has any of these health levels left, they are automatically used to heal the target as much as possible (the caster chooses if it will heal bashing or lethal, the latter of which is usually vulgar). Life 3 is required to target someone other than the Euthanatos."
effect.save()
effect.add_source("Tradition Book: Euthanatos (Revised)", 61)
effect, _ = Effect.objects.get_or_create(name="Hua To's Cure", spirit=4, prime=2)
effect.description = "The Wu-Keng calls on the deified healer Hua To with songs and written invocations, and then crafts health levels out of ephemera, reducing the subject's wound penalties as if those health levels were real. With Life 3, this will also actually heal one health level per success and grant one ephemeral one as well."
effect.save()
effect.add_source("Dragons of the East", 67)
effect, _ = Effect.objects.get_or_create(name="Alloy", matter=4)
effect.description = "With Alloy, the mage can take two Patterns and mix them together, creating a new substance with some properties from each."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 174)
effect, _ = Effect.objects.get_or_create(name="Alter State", matter=3)
effect.description = "The weaker version directly changes the state of Matter for the duration of the effect. The Matter 5 version directly changes the melting or boiling point of a material, which can cause it to immediately boil, freeze, melt or condense, depending on the new points."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 203)
effect.add_source("Mage: The Ascension (Second Edition)", 206)
effect, _ = Effect.objects.get_or_create(name="Alter Weight", matter=5)
effect.description = "As a Master of Matter, a mage can alter fundamental properties of matter. With this rote, the mage can increase or decrease an object's weight without altering any other properties of the object."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 203)
effect.add_source("Mage: The Ascension (Second Edition)", 207)
effect.add_source("Mage: The Ascension (Revised)", 174)
effect, _ = Effect.objects.get_or_create(name="Guncotton's Blessing", matter=3)
effect.description = (
    "The mage causes any organic substance to become a potent explosive."
)
effect.save()
effect.add_source("Dead Magic II", 65)
effect, _ = Effect.objects.get_or_create(
    name="The Incredible Shrunken Machine", matter=5, forces=3, prime=2
)
effect.description = "This allows an Etherite to take a fully functioning machine and shrink it down to nanotechnology. The machine will continue to function based on how many effects are spent on duration."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 224)
effect, _ = Effect.objects.get_or_create(name="Matter Association", matter=5)
effect.description = "The Master can alter the fundamental properties of matter. This can create materials that will not interact with specific other materials (such as bullets that just pass-through armor) or can create superconductive materials or materials of one sort with properties of materials of another."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 174)
effect, _ = Effect.objects.get_or_create(name="Matter Pattern Disassociation", matter=5)
effect.description = "A technique invented by Etherites, this rote makes two materials insubstantial with respect to each other: they can just pass through one another. The two substances are unchanged otherwise."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 202)
effect.add_source("Mage: The Ascension (Second Edition)", 207)
effect, _ = Effect.objects.get_or_create(name="Melt and Reform", matter=2)
effect.description = "The mage can transform an object into an easier to modify form, such as stone into clay."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 173)
effect, _ = Effect.objects.get_or_create(name="Sculpture", matter=3)
effect.description = "The mage can change the shape of an object as in Melt and Reform, but without having to transmute it into a more malleable form first."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 203)
effect.add_source("Mage: The Ascension (Second Edition)", 206)
effect.add_source("Mage: The Ascension (Revised)", 173)
effect, _ = Effect.objects.get_or_create(
    name="Semi Auto CAD CAM", correspondence=5, matter=3
)
effect.description = "Through computer modeling, a mage can combine two guns into a single weapon that mixes their styles and their abilities. Choose one gun as the base. For each success, the mage can change one of Difficulty, Damage, Range, Rate, Clip and Conceal on it to the stat of the other."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 221)
effect, _ = Effect.objects.get_or_create(name="Tapping the Signal", matter=5)
effect.description = "A rote beloved by some Technomages, hated by others, this converts any material into a conductor, which can be used to send signals. While this can be used to connect (wired) to networks remotely, it is particularly popular as a way to tap into isolated lines and thus eavesdrop on secure communication."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 204)
effect.add_source("Mage: The Ascension (Second Edition)", 207)
effect, _ = Effect.objects.get_or_create(
    name="Transephemeration Ray Projector", matter=3, life=3
)
effect.description = "Targeting both a person and an inanimate object with beams of light, this rote causes the person and object to no longer interact, just passing through one another."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 225)
effect, _ = Effect.objects.get_or_create(name="Transformers", matter=4)
effect.description = "Just as Alloy mixes two substances, Transformers allows the mage to combine two devices into a single one, such as a wristwatch/dartshooter."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 207)
effect.add_source("Mage: The Ascension (Revised)", 174)
effect, _ = Effect.objects.get_or_create(name="Analyze Substance", matter=1)
effect.description = "This rote allows the mage to determine what an object is made of."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 202)
effect.add_source("Mage: The Ascension (Second Edition)", 206)
effect.add_source("Mage: The Ascension (Revised)", 173)
effect, _ = Effect.objects.get_or_create(name="Evaluation", matter=1)
effect.description = "This gives the Void Engineer detailed information about a physical object within line of sight."
effect.save()
effect.add_source("Technocracy: Void Engineers", 44)
effect, _ = Effect.objects.get_or_create(name="Machine God", matter=1, forces=1, mind=2)
effect.description = 'This procedure allows an Iterator to "think like a machine" which gives them insight into the operation and repair of machines, computers, robots, and other pieces of high technology.'
effect.save()
effect.add_source("Technocracy: Iteration X", 50)
effect, _ = Effect.objects.get_or_create(
    name="Perfection of the Tools", matter=1, mind=1
)
effect.description = "An Artisan using this effect gets a minus one difficulty per success on any task that they plan out carefully and ensure that they have the proper tools for."
effect.save()
effect.add_source("Artisan's Handbook", 47)
effect, _ = Effect.objects.get_or_create(name="Abundance", matter=2, prime=2)
effect.description = 'Also known as "Loaves and Fishes" among Christian Choristers, by blessing or giving a prayer of thanks for food, a source of food or water fails to run out as it is consumed. It does this such that no one ever sees food or drink being created explicitly, such as a never-emptying canteen or a canister of flour that never seems to run out.'
effect.save()
effect.add_source("Tradition Book: Celestial Chorus (Revised)", 57)
effect, _ = Effect.objects.get_or_create(name="Apportation", correspondence=2)
effect.description = (
    "Allows the mage to pull a small object to their location from elsewhere."
)
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 189)
effect.add_source("Mage: The Ascension (Revised)", 159)
effect, _ = Effect.objects.get_or_create(
    name="Kiss of the Virtuous Maiden", correspondence=2, forces=2
)
effect.description = "The Wu-Keng rarely kill, themselves. However, when they must, they write a brief poem declaring their faithfulness to their demon lord. They then burn the poem and conceals a weapon nearby. When in combat, they can then produce the weapon, catching their opponent by surprise. Often, Correspondence is used to hide it in an unlikely location, such as the mage's mouth."
effect.save()
effect.add_source("Dragons of the East", 66)
effect, _ = Effect.objects.get_or_create(name="Pickpocket", correspondence=2)
effect.description = "Originating among the Ksirafai, this rote sizes up a target so that the mage knows exactly where on their person an object is as well as the best access to it. This decreases the difficulty of rolls to pick the pocket of the target for the object in question."
effect.save()
effect.add_source("Order of Reason", 66)
effect, _ = Effect.objects.get_or_create(name="Ripple Through Space", correspondence=4)
effect.description = "This allows the mage to move one object from any location to any other location. The larger the object the more successes and the more consequences in general."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 186)
effect, _ = Effect.objects.get_or_create(
    name="Spatial Sheath", correspondence=2, matter=1
)
effect.description = "As carrying around swords is frowned upon in modern society, this Templar rote pushes all but the entry point of a scabbard to another location, allowing them to store a sword with only the hilt needing to be hidden directly on them."
effect.save()
effect.add_source("Book of Crafts", 103)
effect, _ = Effect.objects.get_or_create(
    name="Summon Weapon", correspondence=2, matter=1
)
effect.description = "Instantaneously causes a weapon to appear in the mage's hands. If a weapon cannot be summoned from elsewhere, the mage can use the second form to create a duplicate of a known weapon."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (First Edition)", 63)
effect, _ = Effect.objects.get_or_create(name="Dash and a Pinch", matter=2)
effect.description = "With access to basic ingredients, a mage can produce virtually any mixture whatsoever. Regardless of actual plausibility, the mage mixes together various things that they have and transmutes it into the desired mixture. This is particularly useful to chemists and to cooks. With Mind 2, a cook can hastily produce or improve a meal to the point where it can affect someone's mental state, making a guest lethargic enough to retire early, to encourage people to drink more than they otherwise would, etc."
effect.save()
effect.add_source("Order of Reason", 75)
effect, _ = Effect.objects.get_or_create(name="Exotic Matter", matter=5)
effect.description = "When an Etherite truly becomes a Master of Matter, they start to feel constrained by normal materials. Fortunately, with work, they can create new, strange forms of Matter with properties unlike any that have come before."
effect.save()
effect.add_source("Tradition Book: Sons of Ether (Revised)", 61)
effect, _ = Effect.objects.get_or_create(name="Exotic Matter - Antimatter", matter=5)
effect.description = "By using particle accelerators, research time at CERN, post-modern alchemy, or a variety of other techniques, an Etherite can create Antimatter. Antimatter consists of particles with opposite charges from regular matter: instead of electrons, positrons, and for most other particles just anti-particles. Antimatter's most important property is that when it encounters regular matter, the two annihilate each other converting perfectly to energy. In short: an explosion. Antimatter requires at least 20 successes to create, and only after that can successes go to the amount/damage/area. Each success then causes three dice of aggravated damage in a radius of 100 yards per success. For anything other than immediate explosion, magnetic containment fields and vacuum pumps are strongly recommended."
effect.save()
effect.add_source("Tradition Book: Sons of Ether (Revised)", 61)
effect, _ = Effect.objects.get_or_create(
    name="Exotic Matter - Primium", matter=5, prime=3
)
effect.description = "Among the only groups that know how to make Primium are Iteration X and the Society of Ether. It's an alchemically perfect alloy of gold and silver. Expensive alchemy or nuclear furnaces, not to mention base materials, go into its creation, keeping it far out of reach of anyone without Resources 5. Additionally, it requires quintessence: each success needs to be backed by a point of quintessence. Just to create Primium requires 15 successes, and only after that can successes be spent on mass and potency. Primium itself has a near perfect sheen and is a very strong material. However, its real value is its potency against the supernatural. A Primium weapon will cause aggravated damage, and it provides permanent countermagick: two dice per success spent on it, though no more than 10 dice against any given effect. This countermagick has a radius of about two yards, and if the Primium is used as a weapon, these dice are rolled against any supernatural defenses."
effect.save()
effect.add_source("Technocracy: Iteration X", 48)
effect.add_source("Tradition Book: Sons of Ether (Revised)", 62)
effect, _ = Effect.objects.get_or_create(name="Industry", matter=3)
effect.description = "The mage can, given appropriate materials and time, construct complex objects, such as ornate furniture, but also false walls, hidden switches, secret doors, and the like. However, as an Order of Reason rote, Industry takes much longer than Tradition methods do, each roll requiring a full day (eight hours) in a workspace."
effect.save()
effect.add_source("Order of Reason", 76)
effect, _ = Effect.objects.get_or_create(
    name="Inscribe Amulet", time=4, matter=1, entropy=1
)
effect.description = 'This creates an object with a hanging effect on it which will be triggered under some circumstance predetermined by the user. These circumstances may include "not in front of Sleepers" and "if reality permits it" to avoid Witnesses and even Vulgarity.'
effect.save()
effect.add_source("Mage Storyteller's Companion", 63)
effect, _ = Effect.objects.get_or_create(
    name="Jury Rig", correspondence=2, matter=2, mind=1, prime=2
)
effect.description = "By careful examination of a broken machine, an Etherite may determine exactly what needs to be done to repair it and then proceed to do so using whatever techniques they prefer. The worse condition the machine is in, the more successes are required to do the repair."
effect.save()
effect.add_source("Book of Shadows", 142)
effect, _ = Effect.objects.get_or_create(
    name="Na Kua's Gift", matter=3, forces=3, mind=3, prime=2
)
effect.description = "By mimicking the creation of humanity by Na Kua, the Wu-Keng can create a servitor. Using Matter to shape it and Forces and Mind to animate it, the creature has a dot of Strength and Stamina for each success and the creator's Dexterity."
effect.save()
effect.add_source("Dragons of the East", 67)
effect, _ = Effect.objects.get_or_create(name="O'Doul's Ingeniae", prime=5)
effect.description = "Allows the mage to create objects out of pure quintessence. Similar to a Matter 3/Prime 2 effect, this avoids the requirement of Matter in exchange for needing mastery of Prime."
effect.save()
effect.add_source("Order of Reason", 109)
effect, _ = Effect.objects.get_or_create(name="Psychiatric Compounds", life=3, mind=2)
effect.description = "Using Synthetic Rituals, the Technocrat is able to create medications that alter the behavior of the brain. Once ingested, it can cause one of: evoking an extreme emotion, with Willpower to resist (Mind 2 version); forgetting the last few minutes or hours (Mind 3, resisted by Willpower); increased difficulty on Willpower rolls; or dulling the mind to willworking (increasing the difficulty of Arete rolls)."
effect.save()
effect.add_source("Guide to the Technocracy", 212)
effect, _ = Effect.objects.get_or_create(
    name="Spear of my Fathers", spirit=3, matter=3, prime=2
)
effect.description = "The shaman can convert ephemera directly into matter, with more successes necessary for larger and more complex objects."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (First Edition)", 67)
effect, _ = Effect.objects.get_or_create(
    name="Spontaneous Material Construction", matter=2, prime=2
)
effect.description = "This allows the mage to create small objects made of a single substance from pure Quintessence. More successes allow the object to be large or more intricate. With Matter 4, composite objects can be created."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 225)
effect, _ = Effect.objects.get_or_create(
    name="Temple Pillars", matter=3, forces=4, prime=2
)
effect.description = "This rote raises a structure from the ground, creating it out of the local material as it rises, transmuting it as needed. The larger the structure, the more successes are needed."
effect.save()
effect.add_source("Hidden Lore", 51)
effect, _ = Effect.objects.get_or_create(name="Burn-Out", forces=2, prime=1)
effect.description = "By overloading a light bulb with Quintessence, a Hollow One is able to cause it to explode, creating a blinding flash of light and up to one health level of bashing damage to anyone standing too close to it."
effect.save()
effect.add_source("World of Darkness: Outcasts", 91)
effect, _ = Effect.objects.get_or_create(name="Chainbreaker Rune", matter=1, entropy=1)
effect.description = "The most basic level allows the mage to detect weaknesses in any sort of physical binding. As the mage grows more powerful, they can unlock the bonds or destroy them utterly."
effect.save()
effect.add_source("Dead Magic II", 98)
effect, _ = Effect.objects.get_or_create(name="Erode Matter", entropy=3)
effect.description = (
    "This rote infuses entropy and chaos into an object, causing it to decay."
)
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 193)
effect, _ = Effect.objects.get_or_create(name="Sabotage", entropy=2)
effect.description = "Using either Matter or Entropy, the mage determines how best to destroy an object and proceeds to do it."
effect.save()
effect.add_source("Order of Reason", 76)
effect, _ = Effect.objects.get_or_create(name="Sanitize Evidence", matter=2, forces=2)
effect.description = "Sometimes, it's important for physical evidence to just disappear, to evaporate. With this procedure, a Technocrat can convert matter directly into energy. It takes at least an hour, and each success can convert up to ten pounds of matter."
effect.save()
effect.add_source("Guide to the Technocracy", 213)
effect.add_source("Mage: The Ascension (20th Anniversary Edition)", 603)
effect, _ = Effect.objects.get_or_create(name="Slay Machine", entropy=3)
effect.description = "Essentially the negation of Like Clockwork, Slay Machine causes a device to break down more quickly. The number of successes determine how much chaos is caused, and the more complex the machine the fewer are needed to disable it, though more are needed to destroy it completely beyond repair."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 192)
effect.add_source("Mage: The Ascension (Second Edition)", 194)
effect.add_source("Mage: The Ascension (Revised)", 163)
effect, _ = Effect.objects.get_or_create(
    name="Tulugaak's Harpoon", matter=3, forces=3, prime=2
)
effect.description = "Following in the footsteps of Tulugaak, the mage hurls an object (traditionally a harpoon) which strikes with enough force to cause whatever it hits to explode outward. The fragments scatter and multiply over a wide area."
effect.save()
effect.add_source("Dead Magic", 132)
effect, _ = Effect.objects.get_or_create(
    name="Beads on a String", correspondence=2, spirit=2, matter=2, entropy=2, mind=2
)
effect.description = "This hard to verify effect is often included on powerful wonders and talismans owned by a mage. It causes them to find their way to the mage in their next incarnation."
effect.save()
effect.add_source("Mage Storyteller's Companion", 62)
effect, _ = Effect.objects.get_or_create(name="Bottle of Smoke", entropy=3, prime=2)
effect.description = "An ancient weapon of the Solificati, this creates a magickal smoke which can have many different effects, including: redirecting probability (Entropy), scramble mechanical workings (Matter), burn exposed skin (Life), disabling hallucinations (Mind), corrode materials (Matter). Time allows it to be set to go off on a delayed trigger."
effect.save()
effect.add_source("Book of Crafts", 42)
effect, _ = Effect.objects.get_or_create(name="Craft Biomechanism", matter=5, prime=3)
effect.description = "This allows the Iterator, usually a Biomechanic, to craft a biomechanical replacement part for a human being. Though still clearly mechanical, it looks somewhat organic, is light and strong, and when attached via Attach Biomechanism functions fully as the original part did."
effect.save()
effect.add_source("Technocracy: Iteration X", 49)
effect, _ = Effect.objects.get_or_create(name="Create Fetish", spirit=4)
effect.description = "The mage can bind spirits to objects to give access to some of the spirit's powers to the owner of the object, which will work best if the spirit is cooperating."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 215)
effect.add_source("Mage: The Ascension (Second Edition)", 219)
effect, _ = Effect.objects.get_or_create(name="Create Talen", spirit=3)
effect.description = "This allows a shaman to create a talen, a single-use fetish. It either contains an awakened spirit or else a bit of a patron spirit's power. It must incorporate Tass, or else Prime 2 is necessary to infuse it with Quintessence."
effect.save()
effect.add_source("The Spirit Ways", 90)
effect, _ = Effect.objects.get_or_create(name="Create Talismans and Artifacts", prime=4)
effect.description = "An Adept of Prime is capable of binding magic permanently to objects, creating Talismans and Artifacts, so long as they have access to sufficient Quintessence. They are also capable of created Soulgems, which are a special sort of Periapt that holds Quintessence with appropriate Resonance. It is attuned directly to the mage's avatar and so can only be used by them."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 211)
effect.add_source("Mage: The Ascension (Second Edition)", 215)
effect.add_source("Mage: The Ascension (Revised)", 184)
effect, _ = Effect.objects.get_or_create(name="Enchant Weapon", prime=2)
effect.description = "The mage can use this to create an idealized form of a weapon or object. This form usually occupies the same space as the weapon but need not be quite the same thing (for instance, a jacket may become a Kevlar vest). Such an object interacts directly with Patterns, and so can cause aggravated damage. This almost always requires a point of Quintessence when cast."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 214)
effect.add_source("Mage: The Ascension (Revised)", 183)
effect, _ = Effect.objects.get_or_create(name="Fits Like a Glove", matter=3)
effect.description = "This effect causes whatever it is used on to automatically resize itself to fit whoever it is using it."
effect.save()
effect.add_source("Mage Storyteller's Companion", 63)
effect, _ = Effect.objects.get_or_create(name="Gorningstakkr", matter=5, prime=2)
effect.description = "The Wound-Proof Shirt. This ritual creates a shirt that is an extremely potent defense. The most basic version gives the wearer luck and will heal wounds. The Matter 5 version acts as powerful armor, granting four soak dice without hindering mobility at all. Furthermore, stabbing and cutting weapons only deal bashing, as they cannot penetrate the cloth. Another variant doesn't just heal the user but harms their enemies."
effect.save()
effect.add_source("Dead Magic II", 102)
effect, _ = Effect.objects.get_or_create(name="Memento Mori", spirit=3, mind=3)
effect.description = "The mage awakens the spirit of an object, gives it complete information about their consciousness, and then lulls it back to sleep. This spirit then acts as a backup copy of the mage's consciousness. This spirit can be used to restore the consciousness of the mage and is particularly useful as insurance against Technocratic tampering."
effect.save()
effect.add_source("Mage Storyteller's Companion", 62)
effect, _ = Effect.objects.get_or_create(
    name="Pretty-Shinies",
    correspondence=1,
    spirit=1,
    matter=1,
    entropy=1,
    mind=1,
    prime=1,
)
effect.description = "This effect helps the mage find objects with some magic to them. It gives no information on what the object is, so it can be anything from a lucky penny to a Wraith's fetter or a Werewolf's weapon."
effect.save()
effect.add_source("Mage Storyteller's Companion", 63)
effect, _ = Effect.objects.get_or_create(
    name="Talisman Tattoos", matter=4, life=3, prime=3
)
effect.description = "Converts a nonliving and nonmagical object into a tattoo on the mage's body at the cost of a point of Quintessence. The tattoo can be released from the mage's body by using this rote and spending a point of Quintessence."
effect.save()
effect.add_source("World of Darkness: Outcasts", 91)
effect, _ = Effect.objects.get_or_create(
    name="Talisman Transmogrification", matter=3, prime=3
)
effect.description = "With a number of successes beating the Talisman's rating, this rote allows a mage to reshape a Talisman."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 225)
effect, _ = Effect.objects.get_or_create(
    name="Walking Chair", spirit=4, matter=4, prime=2
)
effect.description = "This rote animates inanimate objects. It summons spirits who can possess them and gives them the ability to move around."
effect.save()
effect.add_source("Hidden Lore", 16)
effect, _ = Effect.objects.get_or_create(name="Watchdog", matter=3, prime=2)
effect.description = "Stating a trigger for the effect at casting, an object is imbued with the ability to do one action when that trigger is activated. The most well-known example are the standing stones around Britain falling on those who try to take them down."
effect.save()
effect.add_source("Dead Magic II", 123)
effect, _ = Effect.objects.get_or_create(name="Anitquing", matter=4, entropy=2, prime=2)
effect.description = "This rote is the key to the Hollow One aesthetic: it allows the Hollow One to restore objects found at junk sales, thrift stores and the like that are completely nonfunctional to full function."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 61)
effect, _ = Effect.objects.get_or_create(name="The Aura Adamantium", matter=3)
effect.description = "Effects an extreme hardening of an object to make it harder to break. At Matter 3, it becomes difficult but not impossible to break, but at Matter 5, the object can only be destroyed by magickal effects."
effect.save()
effect.add_source("Mage Storyteller's Companion", 62)
effect, _ = Effect.objects.get_or_create(name="Awaken the Inanimae", spirit=3)
effect.description = "This rote causes the spirit of an inanimate object to become awake. Though they can't do much on their own, they often help those who treat them well in small ways: an awakened gun may misfire when used by an enemy, or an awakened building might cause problems for burglars. The spirit is more powerful for old and psychically charged items: new objects have weaker spirits than heirlooms that have been actively used and well-treated for generations. The stronger spirits are also harder to awaken."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 218)
effect.add_source("Mage: The Ascension (Revised)", 187)
effect.add_source("Mage: The Ascension (20th Anniversary Edition)", 607)
effect, _ = Effect.objects.get_or_create(name="Bambolai", spirit=3, prime=2)
effect.description = "With this, a Cultist can intensify a drug. With Spirit, the drug is awakened to improve it, with Matter and Prime the drug is charged with Quintessence. Either way, each success doubles the potency of the drug, and more than five successes causes it to require a difficulty 8 Stamina roll to avoid blacking out."
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (First Edition)", 66)
effect, _ = Effect.objects.get_or_create(name="Berate the Demon", spirit=3, matter=3)
effect.description = "By berating their equipment, a mage can reduce the difficulty of the next ritual they use it in by one."
effect.save()
effect.add_source("Dead Magic", 57)
effect, _ = Effect.objects.get_or_create(
    name="Caffeine Plus", time=2, spirit=1, life=3, mind=1
)
effect.description = "Through the Synthetic Ritual technique, a Progenitor can break down caffeine molecules and rebuild them into a far more potent version of the compound. Each dose includes one of the following benefits: sleep is no longer necessary for the duration concentration is easier so Empower Mind has a -2 difficulty; the ability to see other Dimensions; tasks taking half the time but at a +2 difficulty. It also comes with one of the following drawbacks: the user is edge and disturbed. Willpower rolls are at +2 difficulty, +3 specifically related to emotional outbursts; the user burns off one point of Primal Energy per hour, losing health levels when they run out of stored energy; the user is unconscious for twice the duration after the Procedure ends."
effect.save()
effect.add_source("Guide to the Technocracy", 211)
effect, _ = Effect.objects.get_or_create(name="Like Clockwork", entropy=3)
effect.description = "The mage protects an object from Entropy and decay, allowing it to run perfectly for years. Mystics tend to perform this with small charms, whereas Technomages use regular maintenance on their devices."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 194)
effect.add_source("Mage: The Ascension (Revised)", 163)
effect, _ = Effect.objects.get_or_create(name="Maintain Device", prime=3)
effect.description = (
    "Allows the mage to refuel a Device with new quintessence from a Node."
)
effect.save()
effect.add_source("Order of Reason", 83)
effect, _ = Effect.objects.get_or_create(name="Obsidian Steel", matter=4)
effect.description = "Obsidian was the preferred material for blades in pre-Columbian Mesoamerica. It is, unfortunately, fragile, though otherwise it is a near-perfect material for weapons. Obsidian Steel gives obsidian the durability of a harder stone or even metal."
effect.save()
effect.add_source("Dead Magic", 77)
effect, _ = Effect.objects.get_or_create(
    name="Penny Dreadful's Bright New Penny", time=2, matter=3, prime=2
)
effect.description = "Penny Dreadful designed this rote to restore old items to new condition, making her a rather effective antiquer. The Matter 3 version restores, the Matter 4 version recreates fully the object at an earlier point in its timeline."
effect.save()
effect.add_source("Book of Shadows", 142)
effect.add_source("Mage: The Ascension (20th Anniversary Edition)", 608)
effect, _ = Effect.objects.get_or_create(name="Perfection of the True Form", matter=3)
effect.description = "This rote allows alchemists of the Children of Knowledge to perfect an object. This will do things like make bullet-proof glass impervious to all bullets but doesn't provide further defenses against anything else."
effect.save()
effect.add_source("Book of Crafts", 41)
effect, _ = Effect.objects.get_or_create(name="Perpetual Motion", matter=5, prime=2)
effect.description = "This Procedure alters and creates Forces so that an object can continue to move without external actions or fuel. The simplest use is in setting things into motion so that they don't ever stop, but alternate uses include operating a vehicle without the need of fuel. Despite the name, this requires at least five successes to make permanent."
effect.save()
effect.add_source("Technocracy: Iteration X", 49)
effect, _ = Effect.objects.get_or_create(name="Shaman's Craft", spirit=3, matter=3)
effect.description = "An ancient rote devised by the Spirit Smiths, allowing them to repair and improve broken objects. While working, this rote will at least temporarily (permanently with enough successes) awaken the spirit of the object being repaired. Prime 2 is necessary if the object has significant missing parts. Minor damage can be fixed with only one success, and three will repair all but the most severe damage."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (Revised)", 68)
effect, _ = Effect.objects.get_or_create(name="Vitality", prime=2)
effect.description = "Through fine artisanship, this rote perfects the pattern of an object, adding health levels to it which must be removed before it begins to take damage."
effect.save()
effect.add_source("Order of Reason", 82)
effect, _ = Effect.objects.get_or_create(
    name="Back to the Earth", matter=4, life=3, prime=2
)
effect.description = "Vulgar enough that few non-Marauders would try it, this rote transforms inorganic matter into living wood."
effect.save()
effect.add_source("Hidden Lore", 51)
effect, _ = Effect.objects.get_or_create(name="The Golden Lion", matter=2)
effect.description = "This rote refines objects to their idealized states. Stone becomes crystal, glass becomes jewelry. The object being crafted is extraordinarily fine and tough. With Prime 2, the object exists on both sides of the Gauntlet and can cause aggravated damage. With Prime 3, the object may become a Wonder or a Talisman."
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 271)
effect, _ = Effect.objects.get_or_create(name="Luster", matter=2)
effect.description = "The effect makes an inanimate object seem much more valuable than it is: pyrite might look like gold, iron as silver, glass as gems, etc. Matter transmutes the surface, at least temporarily, Forces changes the appearance more directly, and Mind makes those who look at it believe it to be more valuable than it is."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 92)
effect, _ = Effect.objects.get_or_create(name="Seeds of Gold", matter=2)
effect.description = "Through the alchemical skill of the Children of Knowledge, they can sprinkle a simple version of the Philosopher's Stone in powder form over a seed, and as the plant grows, it will convert base metals in the ground around it into gold. Each success can create a half-ounce of unrefined gold."
effect.save()
effect.add_source("Book of Crafts", 40)
effect, _ = Effect.objects.get_or_create(name="Simple Transmutation", matter=2)
effect.description = "Allows the mage to transform one pure substance into another."
effect.save()
effect.add_source("Order of Reason", 75)
effect, _ = Effect.objects.get_or_create(name="Straw into Gold", matter=2)
effect.description = "A form of minor transmutation that can convert a base, cheap substance into something of value, such as straw into gold, or tears into diamonds."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 206)
effect.add_source("Mage: The Ascension (Revised)", 173)
effect, _ = Effect.objects.get_or_create(name="Transmutation", matter=4)
effect.description = "The mage can transform virtually any substance into virtually any other. The mage can only affect one type of material at a time."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 204)
effect, _ = Effect.objects.get_or_create(name="Checklist", entropy=2)
effect.description = "Breaks down any task into small but logical steps to help remove human error. With Entropy on non-Enlightened rolls, the Void Engineer removes the possibility of a botch. With Prime, the Void Engineer can counteract Paradox at a one-for-one cost with Primal Energy."
effect.save()
effect.add_source("Convention Book: Void Engineers (Revised)", 85)
effect, _ = Effect.objects.get_or_create(name="Confusing Apishtiss", forces=2)
effect.description = "An Inuit shaman can enhance their shouts at a target, disorienting them. Traditionally, this was used to cause a particularly prized species of goose to fall from the sky, but now it is more often used on human enemies, raising the difficulties of their actions for the duration."
effect.save()
effect.add_source("Dead Magic", 131)
effect, _ = Effect.objects.get_or_create(
    name="Degrade Order", correspondence=2, time=3, entropy=2
)
effect.description = 'This rote causes things to fall apart. More specifically, it inserts chaos into a system with Entropy and then speeds up the decay with Time and uses Correspondence to bound the effect so that the affected thing becomes a closed system, and the disorder can\'t "escape."'
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (First Edition)", 61)
effect, _ = Effect.objects.get_or_create(name="Destroy Structures", matter=3)
effect.description = (
    "The mage can break down structures by directly attacking their Patterns."
)
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 203)
effect.add_source("Mage: The Ascension (Second Edition)", 206)
effect.add_source("Mage: The Ascension (Revised)", 173)
effect, _ = Effect.objects.get_or_create(name="Disintegrator", matter=3, prime=2)
effect.description = "Focused through an energy weapon, a Disintegrator causes the bonds between molecules in non-living Matter to be destroyed, causing it to crumble to dust."
effect.save()
effect.add_source("Technocracy: Void Engineers", 48)
effect, _ = Effect.objects.get_or_create(
    name="Ebon Dragon's Tale", matter=2, life=3, entropy=4, prime=2
)
effect.description = "By digging a deep pit and petitioning for the release of the dark waters brought by the ancient black dragon, a Wu-Keng can bring about a stream that rots flesh, actively drowns those caught in it, and ruins the Earth where it passes."
effect.save()
effect.add_source("Dragons of the East", 67)
effect, _ = Effect.objects.get_or_create(name="Jolt", life=2)
effect.description = "Gifts the mage a burst of energy and consciousness. This allows the mage to endure hours or days of being online with minimal fatigue. With Mind, a Mental Shield is added to the effect, to protect against Mind effects and allowing multi-tasking."
effect.save()
effect.add_source("Digital Web 2.0", 112)
effect, _ = Effect.objects.get_or_create(name="Kinetic Push", forces=2)
effect.description = "Through psychic abilities or transduction coils and magnetic levitation, the Technocrat can create a kinetic force to push an object. This can either manipulate an object that is roughly the size of a person, or it can be used as an attack."
effect.save()
effect.add_source("Guide to the Technocracy", 209)
effect, _ = Effect.objects.get_or_create(name="Lobotomize", mind=5)
effect.description = "This procedure is only used on an Agent whose mental health is compromised to the point of being irreparable. This procedure completely erases large portions of the subject's memory and personality and damages their connection to their avatar, but at least leaves them alive. Some Void Engineers oppose it, preferring a dignified death."
effect.save()
effect.add_source("Technocracy: Void Engineers", 45)
effect, _ = Effect.objects.get_or_create(name="Mershakushtu Qurdu", entropy=3)
effect.description = 'This rote, whose name means "Victorious Marduk," reflects the fact that Babylonians understood that things could be uncreated as they could be created, and that history is not set in stone. This rote strengthens a Pattern\'s position in the consensus.'
effect.save()
effect.add_source("Dead Magic", 51)
effect, _ = Effect.objects.get_or_create(name="Mutate Ephemera", entropy=5)
effect.description = "A Master of Entropy is capable of directly destroying thoughts and spirits, as well as other non-physical things."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 164)
effect, _ = Effect.objects.get_or_create(
    name="Night Battle", spirit=2, forces=3, mind=4, prime=2
)
effect.description = "The shaman enters a deep trance and allows their spirit to roam separately from their body. The spirit takes the form of a large predator and can only be perceived by mages with Spirit sight and others with similar perceptions. The target of this attack will seem to have been attacked by a large predator, specifically whichever one the mage's spirit form took. At least two successes must be spent to ensure that this effect lasts for a scene, and Correspondence magick must be used to locate any target the mage doesn't already know the whereabouts of. Further successes are spent on Forces damage to the target."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (Revised)", 69)
effect, _ = Effect.objects.get_or_create(
    name="Shango's Grave", matter=2, forces=5, entropy=3, prime=2
)
effect.description = "This rote creates a storm over a battlefield. The storm specifically makes it impossible to remove the bodies, including lightning striking anyone who does try to remove them. Thanks to Matter, this can even create such a storm in a dry place, creating the moisture and the winds from nothing."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 222)
effect, _ = Effect.objects.get_or_create(name="Sneaking Shadow", forces=2, mind=2)
effect.description = "Using tricks of the light, the Ahl-i-Batin can alter the target's shadow. Mind is used to prevent the target from seeing that their shadow is altered, so that only others can see it. The target starts to become paranoid unless they make a Willpower roll gathering as many successes as went into the rote. If they become paranoid, they can make a Wits + Alertness roll to realize that their shadow is behaving oddly, or else be at -2 to all dice pools for the duration. Mages who notice it will immediately recognize that magick is involved, but Sleepers must roll Willpower against difficulty 8 or else feel that they are haunted by that shadow, seeing it everywhere, for the duration."
effect.save()
effect.add_source("Book of Shadows", 139)
effect, _ = Effect.objects.get_or_create(
    name="Unleash Nanotech Destruction", correspondence=3, entropy=3
)
effect.description = "A kill-switch included in every DEI, if an Iterator with a DEI defects, they can be remotely terminated by a nanotech virus that will attack their biomechanisms and disrupt any machines that they try to use."
effect.save()
effect.add_source("Technocracy: Iteration X", 49)
effect, _ = Effect.objects.get_or_create(name="Unseen Arm", forces=5, prime=2)
effect.description = "The mage can directly alter kinetic energy, creating arbitrary amounts from nothing, or destroying it. This allows them to give the target object whatever velocity they want: pennies moving at the speed of bullets, stopping a speeding train instantly, etc."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 223)
effect, _ = Effect.objects.get_or_create(name="Consecration", prime=1)
effect.description = "The mage can attune an objects Pattern to their own, making them count as one for many purposes. For instance, a consecrated object will remain with them when they change shape, step sideways, or teleport. With Prime 2, this can be done with a living thing, and is essential in bonding a Familiar."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 181)
effect, _ = Effect.objects.get_or_create(name="Joyride", correspondence=2, entropy=2)
effect.description = "With this rote, a mage can make sure that traffic lights aren't a problem while they drive. Entropy alters chance so that the lights happen to be green for them, and Forces does it directly."
effect.save()
effect.add_source("Hidden Lore", 14)
effect, _ = Effect.objects.get_or_create(name="Pathfinding", spirit=1, entropy=1)
effect.description = "By watching the ebb and flow of the Avatar Storm, the mage can find places and times where it is weaker. This rote gives temporary dice for soaking damage from the Avatar Storm."
effect.save()
effect.add_source("Infinite Tapestry", 182)
effect, _ = Effect.objects.get_or_create(name="Pixie Lead", correspondence=2, mind=3)
effect.description = "Causes the target to perceive one route while following a different one. Very useful for evading pursuit anywhere but a wide-open field."
effect.save()
effect.add_source("Book of Shadows", 145)
effect, _ = Effect.objects.get_or_create(name="Remebrance", mind=2, prime=2)
effect.description = "By creating a Body of Light with Prime and a Psychic Impression with Mind, the mage creates a snapshot of their Pattern and persona. For each success, the mage can avoid Disembodiment for an additional day while remaining in the Umbra, though at the beginning of each day, the mage must spend a point of quintessence to power this effect."
effect.save()
effect.add_source("Infinite Tapestry", 183)
effect, _ = Effect.objects.get_or_create(
    name="Remote Piloting Override", matter=1, forces=3, prime=2
)
effect.description = "Iteration X has developed this technique to take remote control of any mundane motor vehicle. The driver/pilot can roll Strength + Drive at difficulty 7 to resist this effect."
effect.save()
effect.add_source("Hidden Lore", 53)
effect, _ = Effect.objects.get_or_create(name="Teleoperate", correspondence=2, forces=2)
effect.description = "Though both the New World Order and Iteration X are better known for it, there are plenty of hackers among the Void Engineers. These hackers developed the technology to remotely seize the controls of electronically controlled vehicles and devices, allowing Void Engineers to operate drones in inhospitable locations without building them from scratch, among other things."
effect.save()
effect.add_source("Convention Book: Void Engineers (Revised)", 87)
effect, _ = Effect.objects.get_or_create(
    name="Wayfarer's Reckoning", correspondence=2, matter=1, forces=1
)
effect.description = "This rote allows the mage to get the lay of the land (or air for Skyriggers) around them. With Correspondence giving the general notion, Matter providing a map of physical obstacles and Forces mapping the moving elements, such as weather, fires, rivers, etc."
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 271)
effect, _ = Effect.objects.get_or_create(
    name="We'll Get There", correspondence=1, entropy=2
)
effect.description = "Combining good luck with good direction sense, this guarantees that a Hollow One will get where they want to go, even if they don't know precisely where it is."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 64)
effect, _ = Effect.objects.get_or_create(
    name="Ala Wai (Short Waters)", correspondence=3
)
effect.description = "Early Polynesian wayfinders were able to travel great distances over the water, making their boats move five miles with each paddle stroke."
effect.save()
effect.add_source("Dead Magic 2", 27)
effect, _ = Effect.objects.get_or_create(name="Merlin's Ride", correspondence=3)
effect.description = "The Verbena can cross great distances quickly by riding a horse with this rote. It allows them to move so quickly that the scenery blurs and, they arrive faster than expected. Each success causes the travel time to decrease by 20%, to a minimum of 0. Correspondence 4 is needed to take others with the mage."
effect.save()
effect.add_source("Tradition Book: Verbena (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(
    name="The Seven-League Stride", correspondence=3
)
effect.description = "This rote allows the mage to step from one place to another nearly instantly. Depending on specifics of the mage's paradigm, the mage may disappear in one place and appear in another, or may be seen to blur past, moving between places at incredible speed."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 185)
effect.add_source("Mage: The Ascension (Second Edition)", 189)
effect.add_source("Mage: The Ascension (Revised)", 159)
effect, _ = Effect.objects.get_or_create(name="Shortcut", correspondence=2)
effect.description = "Originally a Celestial Master procedure, this rote finds unreproducible shortcuts between two points. Works very well when paired with Navigation, this rote can decrease travel time by up to 50%. For single day trips, each success up to five decreases travel time by 10%, for longer trips each increases distance covered that day by 10%. The routes found are often surprisingly short and contain confusing landmarks which prevent them from being found again without another use of this rote."
effect.save()
effect.add_source("Order of Reason", 67)
effect, _ = Effect.objects.get_or_create(
    name="Internalize Ephemeral Object", spirit=4, mind=1, prime=3
)
effect.description = "A mage employing an Astral Sojourn can use this effect to bring an object back from the Umbra into the physical world. First, the mage uses Mind 1 to Mentally Empower themselves so that they can study every aspect of the object. When the mage returns to his body, the object's Pattern is stored in the mage's mind, and needs to find an appropriate physical object to use the Prime and Spirit spheres, as well as any other necessary for the object's effects, to invest the essence of the Pattern into the new object."
effect.save()
effect.add_source("Infinite Tapestry", 182)
effect, _ = Effect.objects.get_or_create(name="Leap Beyond", spirit=5, mind=4)
effect.description = "Less dangerous than traveling physically, with this rote a mage can Astral Project beyond the Horizon and into the Deep Umbra."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 227)
effect, _ = Effect.objects.get_or_create(name="Untether", mind=5)
effect.description = "This rote allows the mage to separate their mind from their body and become an Astral traveler. See Astral Travel on pages 87-88 and 476-478 of Mage: The Ascension 20th Anniversary Edition."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 207)
effect.add_source("Mage: The Ascension (Second Edition)", 211)
effect, _ = Effect.objects.get_or_create(
    name='Amon Maat, "Hidden Justice"', correspondence=3, life=2
)
effect.description = "The Hem-Ka Sobk mage mixes some of their blood into cold water and wash their feet, sprinkle it on a door or windowsill, and whisper a chant to their protector. This allows them to bypass the door and enter a home while the occupants sleep. Furthermore, they can sense everything in the house. Correspondence and Life do this directly (including keeping the people asleep), Spirit enters via the Umbra and summons a spirit to keep the residents asleep."
effect.save()
effect.add_source("Book of Crafts", 57)
effect, _ = Effect.objects.get_or_create(name="Dingo's Touch", forces=2, entropy=1)
effect.description = "This rote allows the mage to find their way into places that they normally couldn't, just like dingos tend to do. Locks open, doors unlock, and windows just slide open."
effect.save()
effect.add_source("Dead Magic 2", 63)
effect, _ = Effect.objects.get_or_create(name="Infiltration", correspondence=3)
effect.description = "Originating with the Ksirafai, Infiltration allows the mage to bypass security entirely and enter any building. Only magick can detect how the mage accessed the building. The number of successes required is at the Storyteller's discretion based on how tight the security is, which is at least one more than the Perception of the highest ranked guard that needs to be bypassed."
effect.save()
effect.add_source("Order of Reason", 68)
effect, _ = Effect.objects.get_or_create(name="Pass the Key", matter=2, entropy=2)
effect.description = "This rote acts as a mystical lockpick. It unlocks a target door. Forces is necessary to handle electronic locks."
effect.save()
effect.add_source("Orphan's Survival Guide", 124)
effect, _ = Effect.objects.get_or_create(name="Safecracker", matter=1, entropy=2)
effect.description = "The mage randomly twists the dial on a lock and manages to unlock it. For each success, the mage learns one digit of the combination, more successes are needed to work out longer combinations. An additional success is needed for time-locks."
effect.save()
effect.add_source("Hidden Lore", 16)
effect, _ = Effect.objects.get_or_create(
    name="Thief in the Night", correspondence=1, forces=1
)
effect.description = "The Knights Templar developed this effect to defeat electronic alarm systems. It allows them to detect the presence of such a system and how it is activated. With Entropy and Forces 2, the Templar can disrupt such systems. If Matter is substituted for Forces, it can detect mechanical traps instead."
effect.save()
effect.add_source("Book of Crafts", 102)
effect, _ = Effect.objects.get_or_create(
    name="Chain of Whispers", correspondence=2, mind=3
)
effect.description = "The mage speaks a rumor (truth doesn't matter) and this effect causes that rumor to spread rapidly. Those who hear it have a magickal compulsion to spread the rumor so long as they believe it, and it will pass through two people per success."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 93)
effect.add_source("Mage: The Ascension (20th Anniversary Edition)", 608)
effect, _ = Effect.objects.get_or_create(name="Cry of Distress", mind=3)
effect.description = "Though gestures and intentions, two mages from the same organization can pass basic messages, particularly warnings."
effect.save()
effect.add_source("Order of Reason", 79)
effect, _ = Effect.objects.get_or_create(
    name="Death Song", time=2, life=2, mind=1, prime=1
)
effect.description = "Using Life to gain the time needed before death, the Chorister processes their memories and composing them into a final song, recording their stories and often including a final prophecy. When this rote is finished, the mage dies."
effect.save()
effect.add_source("Tradition Book: Celestial Chorus", 64)
effect, _ = Effect.objects.get_or_create(
    name="Dreamcry", correspondence=2, spirit=2, mind=2
)
effect.description = "The Dreamspeaker can send a vision into the dreams of someone they know. With Correspondence 3, they can contact more than one person simultaneously."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (First Edition)", 67)
effect, _ = Effect.objects.get_or_create(
    name="Dreamline", correspondence=2, time=2, mind=2
)
effect.description = "There is a bond that all Cultists share. With this rote, a mage can reach through this bond. They can send an empathic impression (Mind 2) or a specific message (Mind 3) to other Cultists, Time 3 permits many messages to be sent in a short time period. The variant with Spirit sends a spirit to deliver the message rather than relying on this bond."
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (First Edition)", 66)
effect, _ = Effect.objects.get_or_create(name="Flower Gesture", time=3, mind=3)
effect.description = "This is one of the most effective teaching rotes ever devised. With it, an Akashic can instantaneously transmit their ideas in a burst of thought to another, essentially accelerated Telepathy."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 71)
effect, _ = Effect.objects.get_or_create(name="Override Signal", forces=2)
effect.description = "With this rote, a Virtual Adept can intercept and jam a signal. With Forces, this covers the electromagnetic spectrum: infrared, ultraviolet, visible light, radio, etc. With Life, this can extend into signals within a target's brain, potentially capable of putting them into a coma. More successes are required for less familiar signals."
effect.save()
effect.add_source("Book of Shadows", 144)
effect, _ = Effect.objects.get_or_create(
    name="Pirated Media Blitz", correspondence=3, forces=2, mind=4
)
effect.description = "Over an area determined by number of successes, this procedure is used by the New World Order to hijack television, radio, etc. signals and transmit 'emergency bulletins' regarding 'dangerous criminals.' If the procedure succeeds, the viewers will believe that the transmission is real, and become convinced that the people described are dangerous criminals."
effect.save()
effect.add_source("Technocracy: New World Order", 49)
effect, _ = Effect.objects.get_or_create(
    name="Point-to-Point Narrow-Band Transmission", correspondence=2, forces=2
)
effect.description = "Forces 2/Correspondence 2 allows the mage to transmit to an active device, hijacking or altering the signal. Adding Forces 3/Prime 2 allows them to transmit to a device that is currently off."
effect.save()
effect.add_source("Hidden Lore", 18)
effect, _ = Effect.objects.get_or_create(
    name="Public Posting", correspondence=2, mind=2, prime=2
)
effect.description = "A Virtual Adept can fire off a broadcast to all mages, whether at computers or not, with this rote. Usually a short message or emotional sentiment. With Mind 3, the message can be detailed and specific."
effect.save()
effect.add_source("Hidden Lore", 20)
effect, _ = Effect.objects.get_or_create(
    name="Sound/Thought Transfer", forces=2, mind=3
)
effect.description = "Hollow Ones can evoke certain thoughts and emotions using sounds and do so by recording the information and playing it underneath music or other sounds, so as to remain hidden from those who aren't supposed to hear it."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 63)
effect, _ = Effect.objects.get_or_create(name="Subliminal Impulse", mind=2)
effect.description = (
    "The mage can transmit a single word or image into the target's subconscious."
)
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 206)
effect.add_source("Mage: The Ascension (Second Edition)", 210)
effect, _ = Effect.objects.get_or_create(
    name="Subliminal Transmission", correspondence=2, mind=2
)
effect.description = "From the Digital Web, the mage can send subliminal messages to people watching a screen, one with Correspondence 2, but many screens with Correspondence 3. Mind 2 only allows emotional manipulation as in Subliminal Impulse, whereas Mind 4 allows full Possession."
effect.save()
effect.add_source("Digital Web 2.0", 113)
effect, _ = Effect.objects.get_or_create(
    name="Temper Viasilicos", correspondence=2, mind=1
)
effect.description = "This allows the mage to use a Viasilicos, a geometrically perfect crystal created by the Order of Reason, to transmit a message to another Viasilicos. One success beyond distance charts allows for a single sentence, two successes allows for a paragraph and three allows for a conversation."
effect.save()
effect.add_source("Order of Reason", 107)
effect, _ = Effect.objects.get_or_create(
    name="Thunder's Gauntlet", correspondence=3, forces=3, mind=3, prime=2
)
effect.description = "Originating in House Tytalus, this ancient Hermetic rote allows the mage to issue a Certamen challenge, no matter how far the opponent is. The original version used Pentacles of Mars and invocations to Gabriel and delivered the call with a painful thunderclap, but modern mages have adapted it to allow for spikes erupting from the ground (via Matter) or internal hemorrhaging (Life)."
effect.save()
effect.add_source("Blood Treachery", 88)
effect, _ = Effect.objects.get_or_create(name="Adder's Tongue", mind=2)
effect.description = (
    "With this rote, a Verbena can understand the speech of all animals within earshot."
)
effect.save()
effect.add_source("Tradition Book: Verbena (Revised)", 64)
effect, _ = Effect.objects.get_or_create(name="Auspicious Dialogues", mind=3)
effect.description = "Though not direct translation, this rote allows the Akashic to understand and use slang and dialect of a language that they already speak. Each success lowers social difficulties by one for a specific subculture or speaking style."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 69)
effect, _ = Effect.objects.get_or_create(name="Babel", mind=4)
effect.description = "The Marauder causes those around them to speak their native language. The number of successes determine how many people are affected for how long. They don't even realize that the language they're speaking has changed without a Wits + Awareness roll (difficulty 8) or until they try to speak with someone not affected."
effect.save()
effect.add_source("Hidden Lore", 51)
effect, _ = Effect.objects.get_or_create(name="Ravensong", life=2, mind=2)
effect.description = "Hollow Ones are so adept at gossip that they developed this rote, which allows them to communicate with small, smart animals such as rats, ferrets, cats and corvids."
effect.save()
effect.add_source("Orphan's Survival Guide", 126)
effect, _ = Effect.objects.get_or_create(name="Semiotic Communication", mind=2)
effect.description = "Syndicate agents know the symbols of the modern age and can use them to communicate. Whether it's the cut of a suit and the color of a tie, or graffiti on a wall, or pop culture references, they can send messages secretly using these symbols. Only Mind is needed for most uses, but to place symbols that will be read by someone once they're found, Matter is needed as well."
effect.save()
effect.add_source("Convention Book: Syndicate (Revised)", 75)
effect, _ = Effect.objects.get_or_create(name="Speaking in Tongues", mind=3)
effect.description = "This Chorister rote allows the Mage to speak in their language while causing their listeners to hear it in their own."
effect.save()
effect.add_source("Tradition Book: Celestial Chorus", 64)
effect, _ = Effect.objects.get_or_create(name="Time's Tongue", time=2, mind=3)
effect.description = "This rote allows the mage to translate or comprehend a dead language, with more successes translating to a better translation. One success would allow a common dead language like Latin or Greek to be understood, but more successes are needed for more obscure languages."
effect.save()
effect.add_source("Tradition Book: Celestial Chorus (Revised)", 59)
effect, _ = Effect.objects.get_or_create(
    name="Tower of Babel/Speak in Tongues", forces=2, mind=2
)
effect.description = "Two related rotes from an obscure Hermetic House, Tower of Babel inserts chaos into speech with Entropy to cause the sounds to come out as complete gibberish. In contrast, Speak in Tongues uses Mind to allow the target to speak any language that the mage does through similar techniques of altering the sound itself."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(
    name="What Did You Say?", correspondence=2, mind=2
)
effect.description = "One of the most basic and useful Nephandi tricks is this mystical form of gaslighting. The target is caused to mishear perfectly ordinary conversation to be vaguely ominous and hostile."
effect.save()
effect.add_source("Hidden Lore", 48)
effect, _ = Effect.objects.get_or_create(name="Breach Alien Gauntlet", spirit=4)
effect.description = "This Procedure allows the Void Engineer to breach gauntlets other than the one around the Earth, such as around other planets or more general Horizon realms."
effect.save()
effect.add_source("Technocracy: Void Engineers", 42)
effect, _ = Effect.objects.get_or_create(name="Create Gauntlet", spirit=5)
effect.description = "At the highest levels, a Void Engineer can create a Gauntlet around a region of the Deep Umbra. One level is created for each two successes, and the duration is determined by the successes spent on it."
effect.save()
effect.add_source("Technocracy: Void Engineers", 42)
effect, _ = Effect.objects.get_or_create(
    name="Create Horizon Realm Construct", spirit=5, matter=4, prime=4
)
effect.description = "With a huge amount of planning, a Void Engineer (usually with a backup team) can create a Horizon Realm and build the Construct within it. This can require huge numbers of successes, to the point where large Horizon Realms can require hundreds of construction specialists to build."
effect.save()
effect.add_source("Technocracy: Void Engineers", 48)
effect, _ = Effect.objects.get_or_create(name="Corrupt Text", matter=2)
effect.description = "Weavers are paranoid about their knowledge ever falling into the hands of their enemies. This rote allows them to destroy texts rather than risk losing them. The simplest version smears the ink on the pages, ruining them. With Mind, specific passages can be targeted, and with Entropy the effect can hang and trigger if someone other than the mage themselves opens the book."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 88)
effect, _ = Effect.objects.get_or_create(name="Craft Tome", entropy=3, mind=1)
effect.description = "Whereas Cypher Wheel encrypts a short message, Craft Tome creates an entire work of novel length which has the hidden meaning encoded throughout it. A combination of secret meanings, subtle themes and clever wordplay convey complex messages to the reader who knows how to find such messages."
effect.save()
effect.add_source("Order of Reason", 89)
effect, _ = Effect.objects.get_or_create(name="Cypher Wheel", mind=1)
effect.description = "The High Guild and the Ksirafai especially, but the Order of Reason as a whole, has a need to be able to communicate securely. This technique uses Mind 1 to encrypt a message so that only the intended recipient can read it. However, the Entropy 1 version can be used to attempt to crack the code and read a message without authorization. With Matter 2, a secret message can be included on the paper which is invisible to the naked eye, and only discoverable by someone using Matter to render it visible."
effect.save()
effect.add_source("Order of Reason", 77)
effect, _ = Effect.objects.get_or_create(name="Neon-Mail", life=1, forces=2)
effect.description = "Reality Hackers in Las Vegas developed a technique for altering the message on a neon sign when a specific person walks near it, so as to send them a hidden message. With Correspondence included, the message can appear on any sign in an area, instead of a specific sign."
effect.save()
effect.add_source("Fallen Tower: Las Vegas", 119)
effect, _ = Effect.objects.get_or_create(
    name="Unravelling the Text", matter=2, entropy=2, prime=2
)
effect.description = "An active defense for Hermetic texts from outsiders, this rote causes someone attempting to read a book to start losing their place, to jump around the page, and be unable to focus."
effect.save()
effect.add_source("Book of Shadows", 142)
effect, _ = Effect.objects.get_or_create(
    name="Unseen Nomenclature", matter=2, mind=2, prime=2
)
effect.description = "Hermetics often need to hide their teachings in plain sight. This rote allows them to do so in a book. mages who read it will be able to tell that there is something hidden, but only those who know how to parse it or who succeed at Wits + Intelligence difficulty 8 roll. The more distinct from the printed text the message is, the more successes are needed to hide it."
effect.save()
effect.add_source("Book of Shadows", 142)
effect, _ = Effect.objects.get_or_create(name="Writing on the Wall", matter=1, mind=3)
effect.description = "Hollow Ones can leave symbols written on walls via graffiti. To understand then, though, requires this rote. One success gives the user the gist of the message, more add details."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 64)
effect, _ = Effect.objects.get_or_create(
    name="Agama Re Sojourn/Agama Te Sojourn", spirit=3, life=2, entropy=4
)
effect.description = "This rote allows the Euthanatos to fall to the cusp of death and lets them mimic a Wraith and enter the Underworld, and to bring companions with them if they have Spirit 4. It has a threshold of seven successes, before duration is considered. Entropy and Life give the mage the mystical attributes of death, and Spirit allows the mage to cross the Shroud. The mage exists for all purposes as a Wraith, inhabiting a corpus with 10 health levels and no wound penalties. If the mage loses all their Health levels, the mage gains a new Entropy Synergy trait and is then drawn into a Harrowing."
effect.save()
effect.add_source("Tradition Book: Euthanatos (First Edition)", 67)
effect.add_source("Tradition Book: Euthanatos (Revised)", 63)
effect, _ = Effect.objects.get_or_create(
    name="Death's Passage", spirit=3, life=2, entropy=4
)
effect.description = "An extreme technique for bypassing walls, this allows the mage to step into the Underworld in order to get around. Of course, travel through the Underworld isn't safe, and the mage still must get across and return. The mage also acquires Jhor from this trip."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 93)
effect, _ = Effect.objects.get_or_create(name="The Gate of Culsu", spirit=4)
effect.description = "By drawing a representation of a doorway, the mage can open a gateway to a point in the Underworld. Correspondence is needed to go anywhere other than the same Shadowlands reflection of where the door was drawn."
effect.save()
effect.add_source("Dead Magic 2", 144)
effect, _ = Effect.objects.get_or_create(name="Going Under the Cloak", life=2, mind=4)
effect.description = "The mage enters a trance, suspending themselves between life and death, and projecting their mind into the Shadowlands as an astral form."
effect.save()
effect.add_source("Dead Magic 2", 103)
effect, _ = Effect.objects.get_or_create(name="Wings of the Lasa", spirit=3, life=3)
effect.description = "When in the Underworld, this rote grows wings on the back of the mage, made from the local ephemera."
effect.save()
effect.add_source("Dead Magic 2", 145)
effect, _ = Effect.objects.get_or_create(name="Liquor's Calling", spirit=2, mind=1)
effect.description = "The rote causes an Aboriginal Australian who has gotten drunk to gain a distant connection to the Dreamtime."
effect.save()
effect.add_source("Dead Magic 2", 65)
effect, _ = Effect.objects.get_or_create(
    name="Presentation of the Passage Stick", spirit=3
)
effect.description = "The mage sends out a spiritual call into the Dreamtime introducing themselves to anyone or anything who is aware of such things, such as the local Aboriginal mages. It is considered to be extremely rude to cross into another family's territory without doing this."
effect.save()
effect.add_source("Dead Magic 2", 65)
effect, _ = Effect.objects.get_or_create(
    name="Sense the Dreamsong", correspondence=1, spirit=1
)
effect.description = "This allows the mage to ascertain the boundaries and strength of the Dreamtime where they are."
effect.save()
effect.add_source("Dead Magic 2", 66)
effect, _ = Effect.objects.get_or_create(
    name="Sing the Dreaming Earth", spirit=5, mind=3, prime=5
)
effect.description = "This allows the mage to create a variant of a shallowing called a Sleeping Land (rules in Dead Magic 2, page 54-55), with area determined by the number of successes. This is a type of Shallow Realm, a minor realm that is very close to the world and don't form accidentally."
effect.save()
effect.add_source("Dead Magic 2", 54)
effect, _ = Effect.objects.get_or_create(name="Songline Soaring", spirit=3)
effect.description = "By humming a Songline, the mage can take advantage of the spatial distortion of the Dreamtime to move to any other point along the line instantaneously."
effect.save()
effect.add_source("Dead Magic 2", 66)
effect, _ = Effect.objects.get_or_create(name="Songline Walking", spirit=1)
effect.description = "This allows the mage to detect and follow the path of a Songline that they have been introduced to."
effect.save()
effect.add_source("Dead Magic 2", 66)
effect, _ = Effect.objects.get_or_create(name="Alley Vanish", correspondence=3, mind=2)
effect.description = "On the Hollow One's turf, they know all the short cuts and non-obvious ways to get around. So, if they need to escape from pursuit, they can use this rote to vanish in an alleyway."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 61)
effect, _ = Effect.objects.get_or_create(
    name="Daedalus Gateway", correspondence=4, mind=3
)
effect.description = "This procedure teleports a target but leaves them not realizing that they've been teleported. It can be defeated by Correspondence senses or expenditure of Willpower to overcome the Mind aspect."
effect.save()
effect.add_source("Technocracy: New World Order", 49)
effect, _ = Effect.objects.get_or_create(name="The Endless Pool", correspondence=4)
effect.description = "The mage of the Hem-Ka Sobk finds or creates a large pool of water, marks the boundary with their spit and urine, and puts in a drop of their blood. When the victim steps into the pool, they are pulled into the water and transported to another location. A stronger version holds the victim there, suspended in time, where Time 4 does so after some duration, and 5 can do so indefinitely."
effect.save()
effect.add_source("Book of Crafts", 58)
effect, _ = Effect.objects.get_or_create(name="Free Conjunction", correspondence=5)
effect.description = "Like Hermes Portal, this creates a path between two points that anyone can step through. However, this allows the environments to freely mix, rather than keeping them on different sides of the portal."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 188)
effect, _ = Effect.objects.get_or_create(
    name="Heaven's Tumbling Pebbles", correspondence=3, entropy=2
)
effect.description = "By crushing a bluestone in a blue porcelain bowl, a Wu-Keng can flee to a safe location. Entropy 2 makes the location random, but safe. Correspondence 3 takes the Wu-Keng there, 4 lets them take a group, but 5 randomly overlays many different locations into a chaotic mess, so that no one knows which location they will end up attached to when it ends."
effect.save()
effect.add_source("Dragons of the East", 66)
effect, _ = Effect.objects.get_or_create(name="Hermes Portal", correspondence=4)
effect.description = "Creates a free-standing portal between two locations, stable enough that anyone can walk through it."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 186)
effect.add_source("Mage: The Ascension (Second Edition)", 190)
effect.add_source("Mage: The Ascension (Revised)", 160)
effect, _ = Effect.objects.get_or_create(name="Mercury's Bridge", correspondence=3)
effect.description = "This effect allows the mage to travel from one place to another. The Correspondence 4 version allows them to take others along, and Spirit can be included to allow transport across the Gauntlet."
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 272)
effect, _ = Effect.objects.get_or_create(name="Riding the Railroad", correspondence=3)
effect.description = "The Hollow One method of teleportation from Chantry to Chantry, this provides instantaneous travel at the cost of physical exhaustion, severe jet lag, and other consequences that are normal to mundane travel."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 62)
effect, _ = Effect.objects.get_or_create(name="Shuttle", correspondence=3)
effect.description = "This allows a Void Engineer to teleport or, with Correspondence 4, to bring others with them."
effect.save()
effect.add_source("Technocracy: Void Engineers", 41)
effect, _ = Effect.objects.get_or_create(name="Voidcast", correspondence=4, spirit=3)
effect.description = "Thanks to advancements in quantum field inversion and particle matrix fluctuation, a Void Engineer can create a Faraday cage to contain everything to transport and then teleport the contents to wherever they want. The lesser version is restricted to any place within the Spatial Horizon, but the greater version can go anywhere."
effect.save()
effect.add_source("Convention Book: Void Engineers (Revised)", 87)
effect, _ = Effect.objects.get_or_create(name="Breach Gauntlet Undetectably", spirit=3)
effect.description = "At a cost of requiring two more successes than Stepping Sideways, a Void Engineer can dissolve the Gauntlet, step through, and restore it, making it much harder to detect their passage. This technique can also extract someone or something that has become trapped within the Gauntlet."
effect.save()
effect.add_source("Technocracy: Void Engineers", 42)
effect, _ = Effect.objects.get_or_create(name="Breach the Gauntlet", spirit=4)
effect.description = "Like Stepping Sideways, this rote allows the mage to enter the Umbra. However, this creates a gateway that others can use as well, allowing the mage to bring them along."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 215)
effect.add_source("Mage: The Ascension (Second Edition)", 218)
effect.add_source("Mage: The Ascension (Revised)", 189)
effect, _ = Effect.objects.get_or_create(name="Break the Dreamshell", spirit=5)
effect.description = "A Master of Spirit can finally step beyond the Horizon, leaving the part of the Umbra that is particularly close to Earth (or to whatever Realm they happen to be in) and going into the Deep Umbra."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 215)
effect.add_source("Mage: The Ascension (Second Edition)", 219)
effect.add_source("Mage: The Ascension (Revised)", 189)
effect, _ = Effect.objects.get_or_create(name="Bridge of Blood", spirit=4, prime=3)
effect.description = "This brutal rote allows the mage to grab a random spirit (or a specific one if they can do so) and forces it to manifest in the same space as the mage while the mage is Stepping Sideways. This sacrifices the spirit to allow the mage to cross the Gauntlet safely, causing the Avatar Storm to attack it instead of them. The mage needs at least as many successes as their avatar rating, must spend one point of quintessence per dot of avatar. The spirit then takes the damage from the Avatar Storm instead of the mage."
effect.save()
effect.add_source("Infinite Tapestry", 181)
effect, _ = Effect.objects.get_or_create(name="Deep Umbra Travel", spirit=5)
effect.description = "The Deep Umbra is a dangerous place: large tracts of barren territory, distances between anything of interest are large but variable, hallucinations and visions are common, as are bizarre spirits less tied to the consciousness of humanity. Masters of Spirit are the only ones who can travel there with any degree of safety, others are in danger from the environment nearly instantaneously."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 215)
effect.add_source("Mage: The Ascension (Second Edition)", 219)
effect.add_source("Mage: The Ascension (Revised)", 189)
effect, _ = Effect.objects.get_or_create(name="Deep Universe Survival", spirit=5)
effect.description = "Chairs of the Void Engineers build computer simulations and particle emitters that will create a bubble of survivable reality to protect them from the Deep Universe. Usually, this is applied to vehicles rather than to individuals."
effect.save()
effect.add_source("Convention Book: Void Engineers (Revised)", 87)
effect, _ = Effect.objects.get_or_create(
    name="Detect the Dream Gateway", correspondence=1, spirit=1
)
effect.description = (
    "This rote allows the mage to find places where the Gauntlet is unusually weak."
)
effect.save()
effect.add_source("Book of Shadows", 145)
effect, _ = Effect.objects.get_or_create(name="Dream Locus", spirit=2, matter=1)
effect.description = "This rote allows a Dreamspeaker to bring their material belongings with them when they use Stepping Sideways."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 227)
effect, _ = Effect.objects.get_or_create(
    name="Dreamquest", spirit=3, entropy=2, mind=2, prime=2
)
effect.description = "Shamans have long known that making changes in the spirit world can change the physical world. Drawing upon that connection, this rote lets the shaman know what needs to be done to accomplish their goal, though it does so by giving them a quest to accomplish, with difficulty generally scaling with the alterations to reality that they want to make. The resulting effects occur purely coincidentally, outside the control of the characters. This rote in fact begins the effect, with Spirit 3 required to enter the Umbra and begin, 4 to bring companions with them, and Mind 4 to use Untether to enter the Umbra themselves."
effect.save()
effect.add_source("The Spirit Ways", 92)
effect, _ = Effect.objects.get_or_create(
    name="Gateway Transport", correspondence=5, spirit=5
)
effect.description = "One of the most powerful transportation procedures that the Void Engineers have developed, this opens a gate to a point in the Deep Universe, one large enough to pilot a Voidship through."
effect.save()
effect.add_source("Technocracy: Void Engineers", 48)
effect, _ = Effect.objects.get_or_create(name="Holopuni'au'nei", spirit=3)
effect.description = "A Kopa Loei rote that translates literally to 'to sail around the world' or 'to avoid the physical world.' This is Stepping Sideways."
effect.save()
effect.add_source("Book of Crafts", 74)
effect, _ = Effect.objects.get_or_create(name="Karmic Inversion", life=3, prime=4)
effect.description = "By linking themselves to another mage through horrific torture, the mage is able to avoid taking damage from the Avatar Storm, instead shunting it off to the linked target."
effect.save()
effect.add_source("Dead Magic 2", 81)
effect, _ = Effect.objects.get_or_create(
    name="Leap Sideways", correspondence=3, spirit=3
)
effect.description = "An improved version of Stepping Sideways, Leap Sideways allows the mage to not only enter or exit the Umbra, but also to transport themselves anywhere on Earth or the Near Umbra."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 227)
effect, _ = Effect.objects.get_or_create(
    name="Long-Distance Universal Travel", spirit=5
)
effect.description = "This allows the Void Engineer to travel the Deep Universe freely, and even breach Horizon Realms without using the proper entrance. This rote is also sometimes called Puncture Reality Barrier, as that is the name that some Void Engineers give to the Horizon."
effect.save()
effect.add_source("Technocracy: Void Engineers", 42)
effect, _ = Effect.objects.get_or_create(name="Moving the World Walls", spirit=2)
effect.description = (
    "This rote allows a shaman to strengthen or weaken the Gauntlet in an area."
)
effect.save()
effect.add_source("Technocracy: New World Order", 49)
effect.add_source("Tradition Book: Dreamspeakers (Revised)", 66)
effect, _ = Effect.objects.get_or_create(name="Reverie", spirit=3)
effect.description = "Allows the mage of the Order of Reason to enter the Umbra where the Gauntlet is weak (rating 5 or below)."
effect.save()
effect.add_source("Order of Reason", 85)
effect, _ = Effect.objects.get_or_create(name="Schedule of Heaven", time=1, spirit=3)
effect.description = "The Long Count governs the spirit worlds as well as the mundane. A mage who studies it can use it to find times when crossing into the Umbra will be easier because the spirit worlds are closer. Successes decrease the difficulty to cross the Gauntlet."
effect.save()
effect.add_source("Dead Magic", 78)
effect, _ = Effect.objects.get_or_create(name="Shield of the Soul", spirit=2, prime=3)
effect.description = "This rote allows the mage to hide their avatar inside of a Familiar. If this rote is in effect while crossing the Gauntlet, it allows the mage to avoid the Avatar Storm."
effect.save()
effect.add_source("Infinite Tapestry", 183)
effect.add_source("Forged by Dragon's Fire", 79)
effect, _ = Effect.objects.get_or_create(name="Spirit Cloak", spirit=2, mind=2)
effect.description = "This hides the shaman's aura in the Umbra, causing them to stand out significantly less to the Umbra's natives."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (First Edition)", 67)
effect, _ = Effect.objects.get_or_create(
    name="Spirit Journey", correspondence=2, spirit=2
)
effect.description = "This rote allows the shaman to enter a deep trance and sends their perceptions off into the Umbra. They cannot affect anything, but they can view any location on Earth or the Umbra and communicate with spirits they encounter."
effect.save()
effect.add_source("The Spirit Ways", 88)
effect, _ = Effect.objects.get_or_create(name="Stepping Sideways", spirit=3)
effect.description = (
    "The mage can now cross through the Gauntlet and enter the Near Umbra directly."
)
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 214)
effect.add_source("Mage: The Ascension (Second Edition)", 218)
effect.add_source("Mage: The Ascension (Revised)", 188)
effect, _ = Effect.objects.get_or_create(name="Storm Watch", spirit=1, prime=1)
effect.description = "This rote allows the mage to see the Avatar Storm in a general sense. The mage can then see the density of shards in places and can chart the safest route through the storm."
effect.save()
effect.add_source("Infinite Tapestry", 184)
effect.add_source("Mage: The Ascension (Revised)", 167)
effect, _ = Effect.objects.get_or_create(
    name="Sucking Gate", spirit=4, forces=4, prime=2
)
effect.description = "Sometimes, a fight really, REALLY requires a change of venue. For Dreamspeakers, that is often a move into the Umbra. With this rote, they not only Breach the Gauntlet, but also cause those near it to be sucked through. Particularly effective in the age of the Avatar Storm."
effect.save()
effect.add_source("Book of Shadows", 141)
effect, _ = Effect.objects.get_or_create(name="Trailblazing", spirit=2, prime=2)
effect.description = "For one day per success, the Dreamspeaker creates a trail behind them that they can follow back, and it also provides countermagickal defenses for the trail to avoid it being dispelled."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (First Edition)", 67)
effect, _ = Effect.objects.get_or_create(
    name="Umbral Visions", correspondence=2, spirit=2, mind=1
)
effect.description = "After a lengthy, meditative ritual, the shaman goes into a deep trance and projects their senses into the Umbra. They do not enter physically, which keeps them safe from the Avatar Storm. Not only can they project their senses to any place that they know (Correspondence 2) or to any object or person they know (Correspondence 3), but they can also communicate with any spirits or other beings there."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="Universal Travel", spirit=3)
effect.description = "This allows a Void Engineer to survive traveling in the Umbra."
effect.save()
effect.add_source("Technocracy: Void Engineers", 42)
effect, _ = Effect.objects.get_or_create(
    name="Walking the Open Path", spirit=2, prime=1
)
effect.description = "An enhanced version of Moving the World Walls, Walking the Open Path decreases the Gauntlet to zero at a Node, creating a temporary Shallowing and allowing entrance into the Umbra."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (Revised)", 66)
effect, _ = Effect.objects.get_or_create(name="Aquatic Survival", matter=4, life=1)
effect.description = "The Matter version of this Procedure creates an aquatic suit and air supply, the Life version creates synthetic gills, reinforces muscles and bones and even nitrogen-processing to allow for survival in the depths."
effect.save()
effect.add_source("Convention Book: Void Engineers (Revised)", 87)
effect, _ = Effect.objects.get_or_create(
    name="The Barrel of Iskander", matter=2, forces=1
)
effect.description = "With a barrel made of iron and glass, it becomes airtight and allows a clear view of its surroundings, no matter how deep it is submerged underwater. With Life 2, the user will be comfortable in the confined space for longer."
effect.save()
effect.add_source("Artisan's Handbook", 52)
effect, _ = Effect.objects.get_or_create(
    name="Format Space", correspondence=5, spirit=4
)
effect.description = "A team of Void Engineers mark the boundaries of an area that they will use to simulate space, with at least four reference points at the vertices of a tetrahedron. The first successes go to making contact with these points, followed by duration. Afterwards, each success can be used to raise the Gauntlet for Spirit magic by one and decrease it for Dimensional Science by one, to a maximum of 10 and 0, respectively, five successes can be spent to make all mystic magick vulgar, and all Technocratic Procedures coincidental, with exceptions only those that are vulgar everywhere, such as Format Space, and five successes to force the local physics to conform to the consensus."
effect.save()
effect.add_source("Convention Book: Void Engineers (Revised)", 86)
effect, _ = Effect.objects.get_or_create(name="Liftoff", matter=4, forces=5, prime=2)
effect.description = "This Void Engineer effect can turn any airborne vehicle into a spaceworthy vehicle, and with the addition of Dimensional Science 4, it makes the vehicle capable of Umbral travel as well."
effect.save()
effect.add_source("Hidden Lore", 54)
effect, _ = Effect.objects.get_or_create(name="Nitrogen Narcosis", matter=2, life=3)
effect.description = "By using a decompression suit or chamber, Void Engineers can avoid the deadly consequences of nitrogen narcosis, also called The Bends."
effect.save()
effect.add_source("Technocracy: Void Engineers", 48)
effect, _ = Effect.objects.get_or_create(name="VAR", matter=4, life=1, forces=2)
effect.description = "Vacuum, Atmosphere and Radiation survival protects the Void Engineer from hazards of conventional space: lack of oxygen, radiation, etc."
effect.save()
effect.add_source("Convention Book: Void Engineers (Revised)", 87)
effect, _ = Effect.objects.get_or_create(name="Body of the Spirit", spirit=3, life=3)
effect.description = "This allows a Wu Lung mage to transform their body temporarily into ephemera and travel about the physical world as a spirit."
effect.save()
effect.add_source("Book of Crafts", 135)
effect, _ = Effect.objects.get_or_create(name="Daedalus's Wings", forces=2)
effect.description = "The mage constructs elaborate wings out of metal and canvas, mechanisms to move them through the mage's muscle power, and finds a launch point. This effect then allows the mage to fly. Often this is combined with Life 3 to strengthen the mage for the flight, or alternately done solely with Life to grow wings rather than fly using a device."
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 270)
effect, _ = Effect.objects.get_or_create(name="Levitation Walk", spirit=2, forces=2)
effect.description = "This allows the Wu Lung to levitate and move as quickly as if they were in the Umbra."
effect.save()
effect.add_source("Book of Crafts", 134)
effect, _ = Effect.objects.get_or_create(name="Navigation", correspondence=1)
effect.description = "Originating with the Void Seekers and Celestial Masters, this rote allows a mage who is lost to determine their location from sketchy information. One success determines location, three or more successes gives insight into the surrounding geography. Notably, whatever path is chosen always leads to some kind of adventure."
effect.save()
effect.add_source("Order of Reason", 65)
effect, _ = Effect.objects.get_or_create(name="Pilot Skyrigger", correspondence=5)
effect.description = "Allows the user to create and pilot a skyrigger, that is, a flying ship. This effect is used primarily for actually piloting the ship and avoiding obstacles."
effect.save()
effect.add_source("Order of Reason", 108)
effect, _ = Effect.objects.get_or_create(name="Rooftop Leap", life=3, forces=3)
effect.description = "Through strengthened leg muscles and careful application of force, the Hollow One is able to leap from rooftop to rooftop in a city."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 63)
effect, _ = Effect.objects.get_or_create(name="Sure Footing", matter=3, prime=2)
effect.description = "Without changing the appearance of Matter, alters it so that the mage can walk over it normally."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (First Edition)", 62)
effect, _ = Effect.objects.get_or_create(name="Thunder Bridge", forces=3, prime=2)
effect.description = "The Wu Lung have a unique method of traveling that most other factions of mages lack: they can ride lightning. This rote summons a lightning bolt that can carry the mage from place to place. With Matter, metal weapons are deflected from the mage while in transit."
effect.save()
effect.add_source("Dragons of the East", 58)
effect, _ = Effect.objects.get_or_create(name="Traffic Pulse", forces=2, entropy=2)
effect.description = "This rote gives the mage significant control over traffic patterns, allowing them to manipulate traffic lights, how heavy traffic is, and even prevent or cause minor accidents."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 64)
effect, _ = Effect.objects.get_or_create(name="Walking on Water", forces=2)
effect.description = "By increasing the molecular cohesion in water, the mage can walk along it. With enough successes, others can follow the path they walk. The Forces version strengthens the normal force of the water to the same effect."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 197)
effect.add_source("Mage: The Ascension (Second Edition)", 198)
effect, _ = Effect.objects.get_or_create(name="Wings of Icarus", forces=4)
effect.description = "By making a pair of wings out of feathers and wax and donning them, this rote allows a mage to fly clumsily. Strong winds can decrease the difficulty, and extended rituals are strongly recommended."
effect.save()
effect.add_source("Dead Magic", 108)
effect, _ = Effect.objects.get_or_create(name="Calculate Kinematics", correspondence=1)
effect.description = "This Procedure allows a Void Engineer to determine how far away an object is as well as its direction of motion, orientation and speed."
effect.save()
effect.add_source("Technocracy: Void Engineers", 41)
effect, _ = Effect.objects.get_or_create(name="Eagle Eye", correspondence=2, life=1)
effect.description = "An Ahl-i-Batin can view the world from the eyes of a bird, allowing them to see everything from far above."
effect.save()
effect.add_source("Book of Shadows", 138)
effect, _ = Effect.objects.get_or_create(name="Find the Sun", correspondence=1)
effect.description = "Navigation at sea is difficult without the sun. This rote allows them to find any of the major or minor directions, even at night."
effect.save()
effect.add_source("Book of Crafts", 73)
effect, _ = Effect.objects.get_or_create(
    name="Information Glut", correspondence=2, time=2, mind=1
)
effect.description = "This rote amps up one sense, allowing the mage to perceive things they normally couldn't. Each success gives +1 to Perception for the scene or -1 to Alertness checks."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (First Edition)", 62)
effect, _ = Effect.objects.get_or_create(
    name="Information Overload", correspondence=2, mind=2
)
effect.description = "This rote vastly increases the target's perceptive abilities. If the Reality Coder chooses, it can be an enlightening experience, making virtual space seem every bit as real as real space, but it can also cause significant harm by breaking the normal filters that allow people to deal with their senses."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 66)
effect, _ = Effect.objects.get_or_create(name="Landscape of the Mind", correspondence=1)
effect.description = "This allows the mage to perceive a great area of space, though trying to process an area larger than a city block requires Mind."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 185)
effect.add_source("Mage: The Ascension (Second Edition)", 189)
effect.add_source("Mage: The Ascension (Revised)", 159)
effect, _ = Effect.objects.get_or_create(
    name="Lay of the Land", correspondence=2, life=2
)
effect.description = "A Verbena can gain information about an area by communing with the plants and animals in it. One success establishes the connection, additional successes increase the range and duration."
effect.save()
effect.add_source("Tradition Book: Verbena (Revised)", 66)
effect, _ = Effect.objects.get_or_create(name="Sense Connection", correspondence=1)
effect.description = "Allows the mage to determine if an object is being manipulated remotely or if two Patterns are connected."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 158)
effect, _ = Effect.objects.get_or_create(name="Sousveillance", correspondence=1, mind=1)
effect.description = "Surveillance is watching something from afar, so sousveillance is watching from within. The Agent can take in everything at once, though no details that they couldn't possibly perceive without this Procedure. Effectively, all Perception rolls automatically succeed. With other spheres, their senses are enhanced to detect appropriate things."
effect.save()
effect.add_source("Convention Book: New World Order (Revised)", 84)
effect, _ = Effect.objects.get_or_create(name="Whereami?", correspondence=1)
effect.description = "Gives the mage absolute knowledge of their location, so long as no one is magically obscuring it."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 189)
effect.add_source("Mage: The Ascension (Revised)", 159)
effect, _ = Effect.objects.get_or_create(name="Cynical Eye", matter=1, entropy=1)
effect.description = "A mage using Cynical Eye can spot the weaknesses in things. The mage inspects a person or an object in detail, revealing a flaw that can be exploited. With Mind can be used to find character flaws, with Matter can be used to find structural flaws."
effect.save()
effect.add_source("Order of Reason", 68)
effect, _ = Effect.objects.get_or_create(name="Danse Macabre", entropy=1)
effect.description = "Originating with the Cosians and the Ksirafai, this rote is an early forensics effect. Its purpose is to look for tiny signs in the damage and decay on a corpse to determine how and when it died, and with enough successes deduce characteristics of the killer. It's also useful for examining the undead (although not Vampires) to gain insight into their existence and into the necromancers who raise them."
effect.save()
effect.add_source("Order of Reason", 69)
effect, _ = Effect.objects.get_or_create(name="Detect Lie", entropy=1)
effect.description = "By detecting flaws in the target's statements and composure, the mage can tell when someone is lying."
effect.save()
effect.add_source("Order of Reason", 70)
effect, _ = Effect.objects.get_or_create(name="Dim Mak", entropy=1)
effect.description = "An Akashic technique for detecting the weak points in objects and people, similar to Locate Disorder and Weakness. By hitting them, the mage gains dice of their damage roll, one per success."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 191)
effect.add_source("Mage: The Ascension (Second Edition)", 193)
effect, _ = Effect.objects.get_or_create(name="Idealism", entropy=1)
effect.description = "Originating with the High Guild and Explorators, just as a user of Cynical Eye can detect flaws in things, the user of Idealism can find encouraging minor events or good omens, such as birds singing at an opportune moment. With increasing numbers of successes, the event can be more directly positive."
effect.save()
effect.add_source("Order of Reason", 69)
effect, _ = Effect.objects.get_or_create(name="Locate Disorder and Weakness", entropy=1)
effect.description = "Basic Entropy senses allow the mage to find the most disordered point in a structure, effectively finding the weakest spot to attack it."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 192)
effect.add_source("Mage: The Ascension (Second Edition)", 193)
effect.add_source("Mage: The Ascension (Revised)", 162)
effect, _ = Effect.objects.get_or_create(name="Oathbreaker's Lash", forces=3, entropy=1)
effect.description = "A Quaesitor rote, designed to bring the consequences of lies down upon liars. By putting the person to be interrogated into a Seal of Solomon and invoking Uriel, the Angel of Judgment, the Quaesitor can determine the truth of what the person interrogated is saying and bring consequences to them for lies. The person being interrogated needs to beat this number on Manipulation + Subterfuge rolls to lie undetectably. If a lie is detected, the difference creates the dice pool for an electrical attack via Forces on the interrogated. Optionally, this rote may only cause pain, and not any actual damage. In this case, the damage rolled only gives wound penalties, but disappears at the end of the scene."
effect.save()
effect.add_source("Blood Treachery", 87)
effect, _ = Effect.objects.get_or_create(name="Organize", entropy=1)
effect.description = "By detecting weaknesses in their plans, this procedure allows an Iterator to improve them, minimizing those weak points."
effect.save()
effect.add_source("Technocracy: Iteration X", 47)
effect, _ = Effect.objects.get_or_create(name="Ring of Truth", entropy=1)
effect.description = (
    "By paying attention to the strands of Fate, the mage can detect lies."
)
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 193)
effect.add_source("Mage: The Ascension (Revised)", 162)
effect, _ = Effect.objects.get_or_create(
    name="See the Soul's Burn", spirit=1, entropy=2, mind=1
)
effect.description = "Though not able to see the details, this rote allows a Euthanatos to see whether the target is guilty, in general terms."
effect.save()
effect.add_source("Tradition Book: Euthanatos (First Edition)", 66)
effect, _ = Effect.objects.get_or_create(name="Sense Corruption", spirit=1, entropy=1)
effect.description = "Developed by a Chorister who allied with Werewolves against a common threat, this allows the mage to sense the taint and corruption of the Wyrm in the Umbra or a spirit."
effect.save()
effect.add_source("Book of Shadows", 139)
effect, _ = Effect.objects.get_or_create(name="Audio Tap", forces=1)
effect.description = "Iteration X field agents often need to hear things being whispered or spoken from far away or over electronic communications media. With this procedure, they can pick up transmissions all along the electromagnetic spectrum, including phone calls, the audio from television broadcasts, etc."
effect.save()
effect.add_source("Technocracy: Iteration X", 47)
effect, _ = Effect.objects.get_or_create(name="Current Metering", forces=1)
effect.description = "The Technocrat has access to substantial infrastructure. This access allows them to determine how much energy is being used in an area."
effect.save()
effect.add_source("Guide to the Technocracy", 209)
effect, _ = Effect.objects.get_or_create(name="Darksight", forces=1)
effect.description = "This rote allows the mage to shift their vision to different parts of the electromagnetic spectrum, giving them the ability to see things they couldn't normally and in situations where there is no visible light."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 195)
effect.add_source("Mage: The Ascension (Second Edition)", 198)
effect.add_source("Order of Reason", 70)
effect.add_source("Mage: The Ascension (Revised)", 166)
effect, _ = Effect.objects.get_or_create(name="Ear of Dionysus", forces=1)
effect.description = "Developed by the Ksirafai (and independently by the Craftmasons), this rote enhances the mage's hearing to the point where they can discern the faintest auditory cues. Among the more impressive applications are determining someone's weight from the sound of their footfalls, what items they have on them from the sound of their motion, or what the relationship between two people is based on the undertones of their conversation."
effect.save()
effect.add_source("Order of Reason", 72)
effect, _ = Effect.objects.get_or_create(name="Quantify Energy", forces=1)
effect.description = (
    "Allows the mage to sense how much energy and of what kinds are in the area."
)
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 195)
effect.add_source("Mage: The Ascension (Second Edition)", 198)
effect.add_source("Mage: The Ascension (Revised)", 166)
effect, _ = Effect.objects.get_or_create(name="Tune Psychic Radio", forces=2, mind=1)
effect.description = "The mage who uses this rote can listen in on any radio frequency they desire, without a receiver. This allows them to overhear secret communication quite easily, often helpful in tense situations."
effect.save()
effect.add_source("Book of Shadows", 140)
effect, _ = Effect.objects.get_or_create(name="Alarm System", correspondence=1, life=1)
effect.description = "The mage can sense if there are any life forms around them."
effect.save()
effect.add_source("Initiates of the Art", 81)
effect, _ = Effect.objects.get_or_create(name="Gene Scan", life=1)
effect.description = (
    "This Procedure scans (and stores) the genetic code of an individual."
)
effect.save()
effect.add_source("Technocracy: Progenitors", 42)
effect, _ = Effect.objects.get_or_create(name="Genetics Scan", life=1)
effect.description = "Scans the area for life forms. This can filter by species, to avoid being overwhelmed by ants, gnats and mosquitos."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 198)
effect.add_source("Mage: The Ascension (Second Edition)", 201)
effect, _ = Effect.objects.get_or_create(
    name="Genome Mapping", correspondence=3, life=2
)
effect.description = "With just a DNA sample, a New World Order agent can establish a Data connection to the person whose sample it is. Each success adds a level of separation from the DNA to the subject where it will still work, for example, three successes are needed if the sample comes from the target's great-grandfather."
effect.save()
effect.add_source("Convention Book: New World Order (Revised)", 85)
effect, _ = Effect.objects.get_or_create(name="Life Scan", life=1)
effect.description = "A Life Scan will determine what living things are in the area."
effect.save()
effect.add_source("Technocracy: Progenitors", 40)
effect.add_source("Mage: The Ascension (Revised)", 170)
effect, _ = Effect.objects.get_or_create(name="Life Sense", life=1)
effect.description = "By reading a Pattern and analyzing the biochemistry, a Pharmacopeist can identify the basic facts about a target."
effect.save()
effect.add_source("Technocracy: Progenitors", 43)
effect, _ = Effect.objects.get_or_create(name="Pattern Store", life=1)
effect.description = "This Procedure allows the Progenitor to memorize and record the Pattern of a life form."
effect.save()
effect.add_source("Technocracy: Progenitors", 41)
effect, _ = Effect.objects.get_or_create(name="Scan Life Signs", life=1)
effect.description = "Determines the presence of life forms, identifies them, and detects any magickal or technological effects that enhance or weaken it."
effect.save()
effect.add_source("Technocracy: Void Engineers", 43)
effect, _ = Effect.objects.get_or_create(name="Sequencing", correspondence=3, life=3)
effect.description = "Using a combination of body heat tracking, surveillance satellites and sonic sensors, a Technocrat can keep track of all life forms around them. Commonly, the sensors to do this are built into a surveillance vehicle and the information is related to a team via Coordination."
effect.save()
effect.add_source("Guide to the Technocracy", 206)
effect, _ = Effect.objects.get_or_create(name="Assess Affinity", matter=1, prime=1)
effect.description = "A Hermetic takes an object into a circle for assessment and performs a dedication ritual. With success, the mage gains information about the object's affinities, such as elements, astrological signs, what properties it should be assigned in complex rituals, etc."
effect.save()
effect.add_source("Artisan's Handbook", 47)
effect, _ = Effect.objects.get_or_create(name="Fragments of Dream", matter=1)
effect.description = "This rote allows the mage to see hidden things, including what's in a sealed room, a box, or hidden levers and switches."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 202)
effect.add_source("Mage: The Ascension (Second Edition)", 206)
effect.add_source("Mage: The Ascension (Revised)", 173)
effect, _ = Effect.objects.get_or_create(name="Hidden Switch", matter=1)
effect.description = (
    "This rote helps the mage find hidden switches, secret doors, or other features."
)
effect.save()
effect.add_source("Order of Reason", 74)
effect, _ = Effect.objects.get_or_create(name="Holes in the Desert", matter=1)
effect.description = 'With this rote, a mage can detect if something is "different" underneath a desert\'s sand. Successes reduce the difficulty of a roll to determine what it is that has been found, which could be anything from a buried body to a hidden source of water, if there is anything to find.'
effect.save()
effect.add_source("Fallen Tower: Las Vegas", 120)
effect, _ = Effect.objects.get_or_create(
    name="Instant Measurement", correspondence=1, matter=1, mind=1
)
effect.description = "This popular Etherite rote allows the user to find hidden spaces, and, especially, to find any that have someone hiding in them."
effect.save()
effect.add_source("Hidden Lore", 18)
effect, _ = Effect.objects.get_or_create(name="Monarch's Friend", matter=1)
effect.description = "This rote detects poisoned food and drink. With Forces 3/Prime 2, it also makes it glow for all to see."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 92)
effect, _ = Effect.objects.get_or_create(
    name='Aai-ab "Washing the Heart"', spirit=1, mind=2
)
effect.description = "By holding a feather (representing Ma'at), a Hem-Ka Sobk traces the scars over their heart and then can see a symbolic manifestation of their target based on their spiritual nature and thoughts. This is a combination of aura reading and reading surface thoughts."
effect.save()
effect.add_source("Book of Crafts", 57)
effect, _ = Effect.objects.get_or_create(name="Cram Session", time=3, mind=1)
effect.description = "A Technocrat that needs to find something out can conduct a Cram Session. Doing so divides the time needed to find the information by the number of successes."
effect.save()
effect.add_source("Guide to the Technocracy", 216)
effect, _ = Effect.objects.get_or_create(name="Deduction", life=1, mind=1)
effect.description = "The mage picks up subtle signals about a person and integrates them together to determine if they are a threat or not. This gives a difficulty reduction of one per success on the next Mental, Intuition or Enigma roll regarding that person."
effect.save()
effect.add_source("Hidden Lore", 18)
effect, _ = Effect.objects.get_or_create(name="Find the Guilty", mind=2)
effect.description = "A Priest organizes a group to perform a ritual dance to try to root out anyone who bore ill-will towards the recently deceased."
effect.save()
effect.add_source("Dead Magic", 27)
effect, _ = Effect.objects.get_or_create(name="Followme", correspondence=1, mind=2)
effect.description = "The mage helps their friends find them despite having Arcane."
effect.save()
effect.add_source("Initiates of the Art", 81)
effect, _ = Effect.objects.get_or_create(
    name="I Know Your Cousin", correspondence=3, life=1, mind=2
)
effect.description = "This rote allows a mage to determine basic facts about the nearest relative of the target. At three successes spent on strength of the effect, the mage gets a familiar name, and each success beyond that gives a minor fact."
effect.save()
effect.add_source("Fallen Tower: Las Vegas", 120)
effect, _ = Effect.objects.get_or_create(
    name="Ishin Den Shin", correspondence=2, mind=2
)
effect.description = (
    "Allows the Akashic to sense the emotions and mental state of those affected."
)
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 77)
effect, _ = Effect.objects.get_or_create(name="Lip Reading", entropy=2, mind=3)
effect.description = "Even as early as the Renaissance, lip-reading was in common use by the Ksirafai and other spy organizations. When trying to determine the target's plans, the spy watches them carefully, hoping to catch a glimpse of them muttering to themselves, speaking idly to something symbolic of an ancestor or absent friend, etc. With Time added in, the user is more likely to happen to find them at a time when they are doing so."
effect.save()
effect.add_source("Order of Reason", 91)
effect, _ = Effect.objects.get_or_create(name="Mind Empowerment", mind=1)
effect.description = "The mage can sense the surface emotions of others. Other uses of this effect are to increase Mental Attributes temporarily, to see auras, to process more information than usual, and many other effects."
effect.save()
effect.add_source("Technocracy: Progenitors", 42)
effect.add_source("Mage: The Ascension (Revised)", 176)
effect, _ = Effect.objects.get_or_create(
    name="Mindfulness of Wrong Thought", life=1, mind=2
)
effect.description = "While meditating, this rote protects the Akashic. It gives them the ability to detect a hostile being in the vicinity. With Matter instead of Life, it can detect traps near the meditating Akashic."
effect.save()
effect.add_source("Hidden Lore", 13)
effect, _ = Effect.objects.get_or_create(name="No-Mind", mind=1)
effect.description = "The mage senses the minds in their general vicinity."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 206)
effect.add_source("Mage: The Ascension (Second Edition)", 209)
effect.add_source("Mage: The Ascension (Revised)", 176)
effect, _ = Effect.objects.get_or_create(name="Pathos", mind=1)
effect.description = "A very slight variant on Read the Soul which allows the mage to see auras, it gives more information about emotional states and less about states of being."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 205)
effect.add_source("Mage: The Ascension (Second Edition)", 210)
effect, _ = Effect.objects.get_or_create(name="Read the Soul", mind=1)
effect.description = "This rote gives the mage the ability to read auras."
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 269)
effect, _ = Effect.objects.get_or_create(name="Right-Click", correspondence=3, mind=3)
effect.description = "Creates a heads-up display for the Technocrat, scanning people's surface thoughts (with Mind) and computers (with Data) to give the Agent basic information about whatever they are looking at. Other spheres can add more information to this display."
effect.save()
effect.add_source("Mage: The Ascension (20th Anniversary Edition)", 602)
effect, _ = Effect.objects.get_or_create(name="True Form", spirit=1, entropy=1, mind=1)
effect.description = "This rote gives a Cultist who is using a hallucinogen the ability to perceive what lies underneath appearances. Usually this has something to do with the target's Nature. With Life, information about the health and physical state of the target is also gained."
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (Revised)", 70)
effect, _ = Effect.objects.get_or_create(
    name="Detect Reality Deviation", spirit=2, prime=1
)
effect.description = "This allows the Agent to detect and identify Reality Deviants, with different non-human groups requiring different techniques to discover. For example, Life 2 will allow the detection of Vampires, but, for unknown reasons, Dimensional Science is needed to identify Werewolves."
effect.save()
effect.add_source("Technocracy: New World Order", 48)
effect.add_source("Convention Book: New World Order (Revised)", 87)
effect, _ = Effect.objects.get_or_create(name="Dialectic", prime=1)
effect.description = "The mage converses with the target, and gains insight into whether the target has magickal or supernatural powers. With Mind 1 it allows some insight to be gained into the target's aura, and with Entropy 1 lies can be detected."
effect.save()
effect.add_source("Order of Reason", 80)
effect, _ = Effect.objects.get_or_create(name="Find Reality Flaws", entropy=1, prime=1)
effect.description = "This rote allows an Etherite to determine if an object of phenomenon is a result of Paradox, rather than being naturally occurring."
effect.save()
effect.add_source("Tradition Book: Sons of Ether (First Edition)", 63)
effect, _ = Effect.objects.get_or_create(name="Hallmark", mind=2, prime=1)
effect.description = "By examining a magickal working, the mage can detect the mystical fingerprint of the mage who performed it. This allows the mage to identify those fingerprints, though to know which mage it is from, they need to already know the identity that goes with them."
effect.save()
effect.add_source("Book of Shadows", 145)
effect, _ = Effect.objects.get_or_create(name="Inquisitor", prime=1)
effect.description = "Identical to Dialectic, except that the interaction is an interrogation, rather than a discussion."
effect.save()
effect.add_source("Order of Reason", 80)
effect, _ = Effect.objects.get_or_create(
    name="Lore Rune", correspondence=1, spirit=1, matter=1, life=1, mind=1, prime=1
)
effect.description = "This rune grants the ability to identify any supernatural in their vicinity. One success allows them to tell that that someone is not human, more are required to tell them apart, and with large numbers their basic powers can be discerned."
effect.save()
effect.add_source("Dead Magic 2", 100)
effect, _ = Effect.objects.get_or_create(
    name="Patterns of the Long Count", spirit=1, prime=1
)
effect.description = "By reading the Long Count of the Mayan calendar, understanding the patterns in it, the mage can lower the difficulty of effects involving one Sphere by one. This only applies to mages who believe in the Long Count."
effect.save()
effect.add_source("Dead Magic", 78)
effect, _ = Effect.objects.get_or_create(
    name="Spot the Man", correspondence=1, matter=1, life=1, prime=1
)
effect.description = "When successful, the Hollow One will be able to detect any Technomagickal implants or Primium in the target to be viewed."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 63)
effect, _ = Effect.objects.get_or_create(
    name='Hersh, "To Be Patient"', correspondence=1, spirit=1, mind=1
)
effect.description = "The Hem-Ka Sobk enters a meditative trance clearing away doubt and hesitation to reach an emotionless, calm place. This sharpens senses and allows them to feel the Sekhem of Sobk flow through them, and they become one with the crocodile. Without this rote, they are denied access to many of their powers."
effect.save()
effect.add_source("Book of Crafts", 56)
effect, _ = Effect.objects.get_or_create(name="Mirrorshades", spirit=1)
effect.description = "Allows the Technocrat to see Extra Dimensional Entities by looking around an area with specially polarized sunglasses."
effect.save()
effect.add_source("Guide to the Technocracy", 207)
effect, _ = Effect.objects.get_or_create(name="See No Evil", spirit=1)
effect.description = "This rote allows the mage to see things that have footprints in the Umbra: ghosts, spirits, the Gnosis of a Werewolf, a faerie's Glamour and the like."
effect.save()
effect.add_source("Order of Reason", 84)
effect, _ = Effect.objects.get_or_create(name="Spirit Sight", spirit=1)
effect.description = "Spirit Sight allows the mage to see what is on the other side of the Gauntlet without being able to affect it directly."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 214)
effect.add_source("Mage: The Ascension (Second Edition)", 217)
effect.add_source("Mage: The Ascension (Revised)", 187)
effect, _ = Effect.objects.get_or_create(
    name='Utchatti, "The Two Divine Eyes"', correspondence=1, spirit=1
)
effect.description = "By touching scar patterns around their eyes with wet fingers, the Hem-Ka Sobk can sense objects near them that have been touched by Sekhem."
effect.save()
effect.add_source("Book of Crafts", 56)
effect, _ = Effect.objects.get_or_create(name="Cram", time=3, mind=1)
effect.description = "With access to a proper library, the mage can become an expert in any topic contained within the library in a hurry. For each success, the mage gains a temporary dot for a Knowledge trait relevant to the question being studied (to a maximum of five). This dot disappears at the end of a day."
effect.save()
effect.add_source("Order of Reason", 91)
effect, _ = Effect.objects.get_or_create(name="Download Specialization", time=3)
effect.description = "The Agent can become temporarily an instant expert in some subject area. Each success spent on potency gives one level of Hypercram for the duration."
effect.save()
effect.add_source("Technocracy: New World Order", 48)
effect, _ = Effect.objects.get_or_create(
    name="Evaluate Fourth Dimensional Fabric", time=1
)
effect.description = (
    "This allows a Void Engineer to determine if time has been tampered with."
)
effect.save()
effect.add_source("Technocracy: Void Engineers", 46)
effect, _ = Effect.objects.get_or_create(name="Internal Clock", time=1)
effect.description = "This effect gives the mage a perfect internal clock. The only way for them to lose track of the time is to have it or their perceptions of it be altered magickally."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 218)
effect.add_source("Technocracy: Iteration X", 48)
effect.add_source("Mage: The Ascension (Second Edition)", 223)
effect, _ = Effect.objects.get_or_create(name="Perfect Time", time=1)
effect.description = "The mage can perfectly determine when they are."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 191)
effect, _ = Effect.objects.get_or_create(name="Perfect Timing", time=1)
effect.description = "This rote allows the mage to not only know exactly what time of day it is, but also to coordinate activities precisely with others and to intuitively show up at just the right moment during a crisis."
effect.save()
effect.add_source("Order of Reason", 85)
effect, _ = Effect.objects.get_or_create(name="Sense the Fleeting Moment", time=1)
effect.description = "The Verbena who uses this rote will know exactly the correct moment to act for maximum effectiveness. This decreases the difficulty of a specified mundane task by 1 per success, once."
effect.save()
effect.add_source("Tradition Book: Verbena (First Edition)", 63)
effect, _ = Effect.objects.get_or_create(name="Time Sense", time=1)
effect.description = "A mage with even basic knowledge of the Time sphere can determine if Time has been manipulated in an area."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 217)
effect.add_source("Mage: The Ascension (Second Edition)", 223)
effect.add_source("Mage: The Ascension (Revised)", 192)
effect, _ = Effect.objects.get_or_create(name="Kohl Sight", correspondence=1)
effect.description = "By using kohl (a thick, black powder) around their eyes, the Taftani can see things they normally couldn't. This allows them to see into the distance without interference from storms, glare or any other optical effects. The Entropy version instead allows them to see their target's destiny, though in vague terms. With Spirit, they can see into the Invisible World."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 87)
effect, _ = Effect.objects.get_or_create(
    name="Mark of the Beast", correspondence=3, life=1, prime=3
)
effect.description = "This rote marks the blood in a human with Quintessence so that it can be tracked. This lets a mage find the person, and any Vampire who drinks their blood."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 226)
effect, _ = Effect.objects.get_or_create(
    name="Smart Drink", time=1, spirit=1, life=2, mind=2, prime=1
)
effect.description = "Also called the Elixir of Enlightenment by the Children of Knowledge, Smart Drink allows a Sleeper to see the world how it really is, according to them. A Cultists have a similar effect that works through drugs, rather than a drink. The subject gets an energizing boost from Life, the ability to see magick and spirits through Prime and Spirit, Mind opens them up to these new perceptions, and Time lets them perceive the imperfections in the flow of time."
effect.save()
effect.add_source("Book of Crafts", 41)
effect, _ = Effect.objects.get_or_create(
    name="Blood from a Stone", spirit=4, life=3, mind=4
)
effect.description = "The Hollow One needs to first create a Fetter Ball connected to a Wraith that they know, and then pierces it with a needle. This causes the Wraith's Angst to turn to blood and drip out of the ball, leaving the Wraith much calmer after, despite it often objecting in advance to the ritual."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 65)
effect, _ = Effect.objects.get_or_create(name="Coffin for a Fisher", spirit=3, matter=2)
effect.description = "By building a coffin in the shape of something related to the subject's job, the mage can send the accoutrements of the job to the afterlife with them as relics."
effect.save()
effect.add_source("Dead Magic", 26)
effect, _ = Effect.objects.get_or_create(name="Fetter Ball", spirit=4, prime=2)
effect.description = "This creates a one-point fetter for a Wraith, in the possession of the Hollow One. The Wraith must participate willingly and sign a pact with the mage. The contract is the crumpled into a ball and encased in wax. The Wraith cannot affect the wax ball, and it becomes a very effective focus for necromantic magic targeting the Wraith."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 65)
effect, _ = Effect.objects.get_or_create(
    name="Voice Across the Void", correspondence=2, spirit=3, mind=3
)
effect.description = "A Hollow One who has a Fetter Ball for a Wraith can use this rote to communicate with them no matter where they are. Even one success creates two-way communication regardless of distance."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 66)
effect, _ = Effect.objects.get_or_create(
    name="Voice of the Jade Ancestors", spirit=2, mind=2
)
effect.description = "Given an item of value to the deceased (a Fetter, in Wraith: The Oblivion terms), a member of the Wu Lung can summon them (if they are available) for advice."
effect.save()
effect.add_source("Book of Crafts", 134)
effect, _ = Effect.objects.get_or_create(name="Ghost-Burning", spirit=2, forces=2)
effect.description = "This rote allows the mage to direct a light-based attack across the gauntlet, at a spirit or a ghost."
effect.save()
effect.add_source("Artisan's Handbook", 52)
effect, _ = Effect.objects.get_or_create(
    name="Shadow Sight", correspondence=1, spirit=1, entropy=1, mind=1
)
effect.description = "This allows Hollow One necromancers to not only see ghosts, but to see the Shadowlands how the Wraiths see it: morbid black-and-white, the weak points of everything completely obvious, the auras of living things giving away that they are, in fact, alive. By focusing on an individual Wraith, the Hollow One can even see its Shadow."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 66)
effect, _ = Effect.objects.get_or_create(
    name="Shelter from the Storm", spirit=4, entropy=1, prime=4
)
effect.description = "This rote allows the mage to turn a room or building into a Haunt (one level per success) and must last for at least a scene. This provides many benefits, but most notably it protects from the Maelstrom."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 66)
effect, _ = Effect.objects.get_or_create(name="Soothe the Dead", spirit=3)
effect.description = "Using a voice disguising tube or other technique to make his voice audible to both living and dead, the mage soothes the ghosts, pushing the Wraiths into Slumber so that they do not cause problems for the living."
effect.save()
effect.add_source("Dead Magic", 30)
effect, _ = Effect.objects.get_or_create(
    name="Soul-Forging", spirit=4, matter=3, prime=3
)
effect.description = "For more detail, see pages 87-89 of Infernalism: The Path of Screams. This rote allows a mage to perform the terrible act of Soul-Forging, transforming a Wraith into an object."
effect.save()
effect.add_source("Infernalism: The Path of Screams", 87)
effect, _ = Effect.objects.get_or_create(name="Atitsiak", spirit=3, life=4)
effect.description = "Traditionally, Inuit children are named for the most recently deceased member of the community and were thought to gain some characteristics inherited from that individual. This rite allows the mage to briefly adopt the name of a dead person and take on some of their characteristics."
effect.save()
effect.add_source("Dead Magic", 130)
effect, _ = Effect.objects.get_or_create(name="Kispu", correspondence=3, entropy=3)
effect.description = "Inspired by a Babylonian ritual to ease the transition of a soul to the afterlife, modern Euthanatos sacrifice an animal, recite the names of gods of the dead, and, in doing so, can prevent a person from becoming a Wraith."
effect.save()
effect.add_source("Dead Magic", 57)
effect, _ = Effect.objects.get_or_create(
    name="Lichedom", spirit=4, matter=4, life=4, entropy=4, mind=1, prime=3
)
effect.description = "Lichedom is, in some sense, the easy route to immortality. It is the only route that doesn't require a Master, for instance. However, it is forbidden in the strongest terms, and virtually all mages will unite to destroy a Liche if one is found. The mage surrounds themselves with the trappings of their life and their magic, and ritually severs the connection between their avatar and their body. To finish the ritual, the mage kills himself while invoking the final piece of magic, binding their avatar back to their own body right as they reach the point between life and death, freezing themselves there. As such, the Liche becomes a sort of undead, hovering on the edge of death but not crossing over. This is, overall, an extremely complex rite with many requirements, almost every single one of which is criminal in the eyes of most mages. For every detail, see Dead Magic pages 109-112."
effect.save()
effect.add_source("Dead Magic", 109)
effect, _ = Effect.objects.get_or_create(
    name="Song of Orpheus", matter=2, life=4, mind=2, prime=2
)
effect.description = "This rote restores the dead to life. But it isn't that simple. The Pattern spheres and Prime are needed to restore the body, and Time is needed to make sure it is correct, viewing the precise Pattern in the past. Spirit is needed to call the soul/avatar back. Of course, this assumes that it is free to return. In most cases, both the soul and the avatar must be found first, and often the soul has moved on and the avatar has been reborn. This rote should never be used as an easy 'get out of death free' card, but instead should always require multiple sessions, often multiple stories, of work to prepare."
effect.save()
effect.add_source("Book of Shadows", 147)
effect, _ = Effect.objects.get_or_create(name="Walk to Too'ga", spirit=3)
effect.description = "By cutting off their small finger, taking two lethal damage, the mage can protect themselves in their death. When they die, this prevents them from becoming a ghost, and ensures that they move on to whatever afterlife there may be."
effect.save()
effect.add_source("Dead Magic", 30)
effect, _ = Effect.objects.get_or_create(
    name="Eternal Discipline of the Family", spirit=4, entropy=2, mind=2, prime=4
)
effect.description = "Joins a Wu-Keng to a Wraith as parent or spouse. The mage enacts the ritual as though adopting, being adopted by, or marrying a living human, but with their altar burning candles, red-ink charms, and gold and silver paper to symbolize the Wraith. This turns the mage into a Fetter for a Wraith, though the Wraith must be willing, essentially serving their proper part in the ceremony."
effect.save()
effect.add_source("Dragons of the East", 67)
effect, _ = Effect.objects.get_or_create(name="Ghost Rune", spirit=2, entropy=1)
effect.description = "The mage may use this rune to summon the spirit of a volva, a woman gifted with prophecy, and ask her questions about the Wyrd. If the ghost is skilled with the arcanos of Fatalism, then Entropy and Spirit suffice, otherwise the ghost merely channels the mage's own Correspondence and Time to read the Wyrd."
effect.save()
effect.add_source("Dead Magic 2", 99)
effect, _ = Effect.objects.get_or_create(name="Hear and Obey", spirit=5, life=4)
effect.description = "This is one of most infamous techniques available to the Bata'a: the creation of the zombi. With Spirit, it traps the soul while killing and reviving the body, creating an animate servant with no passion or emotion, even if they are somehow restored to life and have the damage to their soul repaired. The Mind version traps the victim's mind in their own corpse as it decays and moves it around like a puppet while they are forced to watch. This version is usually used as a punishment for treachery."
effect.save()
effect.add_source("Book of Crafts", 26)
effect, _ = Effect.objects.get_or_create(name="Reanimation", spirit=2)
effect.description = "Either by summoning a spirit or directly manipulating it with Forces, the mage can cause a corpse to become mobile, creating an animate skeleton or body, depending on the state of the remains."
effect.save()
effect.add_source("Tradition Book: Euthanatos (Revised)", 66)
effect, _ = Effect.objects.get_or_create(name="Summon Volva", spirit=2, entropy=1)
effect.description = "This rote is identical to the Ghost Rune."
effect.save()
effect.add_source("Dead Magic 2", 103)
effect, _ = Effect.objects.get_or_create(name="Field of Yin", life=1, entropy=5)
effect.description = "A male Wu-Keng can disguise himself as a woman perfectly, either by destroying the idea that they are male so that others cannot perceive them as male or else by transforming themselves."
effect.save()
effect.add_source("Book of Crafts", 120)
effect, _ = Effect.objects.get_or_create(name="Goanna's Hiding", matter=2)
effect.description = "The mage's clothing takes on an appearance like the surrounding area, making it easier for them to hide. This rote decreases the difficulty of Dexterity + Stealth rolls."
effect.save()
effect.add_source("Dead Magic 2", 64)
effect, _ = Effect.objects.get_or_create(name="Mindscreen", mind=1)
effect.description = "A Nephandi trick, this rote allows them to disguise their thoughts. They cannot pass as a Sleeper but can hide their malevolent intent."
effect.save()
effect.add_source("Hidden Lore", 48)
effect, _ = Effect.objects.get_or_create(name="Passing", life=3)
effect.description = "Sometimes, certain people are not safe. Whether you're the wrong race, sex or otherwise, this rote allows the mage to change their features to match whatever it is they need to be to be safe."
effect.save()
effect.add_source("Orphan's Survival Guide", 128)
effect, _ = Effect.objects.get_or_create(name="Downvote", correspondence=3, entropy=3)
effect.description = "This Procedure seeks out specific information and uses the appropriate techniques to decrease its ranking in search engines. Most Syndicate agents prefer this over censorship, which tends to draw civil liberties lawyers and conspiracy theorists and ends up with more attention to the information being hidden. Each success on this Effect gives the information a dot of Arcane, obscuring the data everywhere it exists."
effect.save()
effect.add_source("Convention Book: Syndicate (Revised)", 73)
effect, _ = Effect.objects.get_or_create(
    name="Encrypt Thoughts", life=1, mind=1, prime=2
)
effect.description = "By running their thoughts through an encryption algorithm, the Virtual Adept makes them harder to read. Each success subtracts from any outside party's attempts to read the Adept's mind, beyond countermagick."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (First Edition)", 61)
effect, _ = Effect.objects.get_or_create(name="Move Along", mind=2)
effect.description = "By stationing Agents at the perimeter of an area they want quarantined, the New World Order can make people prefer to just 'move along' rather than risk any trouble."
effect.save()
effect.add_source("Technocracy: New World Order", 45)
effect, _ = Effect.objects.get_or_create(
    name="Secure the Scene", matter=1, forces=1, mind=2
)
effect.description = "Technocrats need to score at least three successes to Secure a Scene, and more successes are needed the larger the area to secure is. Mind discourages anyone from entering the area (avoidance with 2, driving them away with 3), while Forces and Matter are used to catalog the evidence that needs to be cleaned up. Forces 3 can be added to create a blackout effect rendering the area dark, to avoid anyone seeing the cleanup process."
effect.save()
effect.add_source("Mage: The Ascension (20th Anniversary Edition)", 604)
effect, _ = Effect.objects.get_or_create(name="Shield", mind=1)
effect.description = "Creates a mental shield which defends against Mind magick."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 210)
effect, _ = Effect.objects.get_or_create(
    name="Soul Cloak", spirit=3, entropy=2, mind=2, prime=2
)
effect.description = "An essential tool for any mage who needs to mask their aura, it is rarely found outside of Infernalists and the Fallen. This effect confuses the aura perceptions of others, hiding the hues that reveal the evil of the mage behind kindly shimmering hues."
effect.save()
effect.add_source("Infernalism: The Path of Screams", 87)
effect, _ = Effect.objects.get_or_create(name="At Ease", mind=2)
effect.description = "With this rote, the Tradition mage seems like a harmless eccentric, causing others to fear them less and mitigating any unsettling effects of their Resonance."
effect.save()
effect.add_source("Guide to the Traditions", 280)
effect, _ = Effect.objects.get_or_create(name="Dontcme", correspondence=1, entropy=2)
effect.description = "The mage can bend space and probability around them, granting them temporary levels of Arcane."
effect.save()
effect.add_source("Initiates of the Art", 81)
effect, _ = Effect.objects.get_or_create(
    name='Ghayba (Occultation or "Unbeingness")[0]',
    correspondence=4,
    spirit=3,
    mind=2,
    prime=4,
)
effect.description = "This not only allows the Batini to gain temporary Occult, but to make it permanent and increase Occult beyond 5 (see Lost Paths: Ahl-i-Batin and Taftani page 39 for details). Each dot of Arcane costs two successes, and each success spent lasts for one lunar year (approximately 336 days). Furthermore, if the mage accidentally reaches Arcane 11, they disappear, the Tellurian itself forgetting that they exist."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 43)
effect, _ = Effect.objects.get_or_create(name="Non-Descript", mind=2)
effect.description = "Makes the Agent not stand out and generally seem unimportant to observers. This acts as the Cloaking background for the duration."
effect.save()
effect.add_source("Guide to the Technocracy", 214)
effect, _ = Effect.objects.get_or_create(name="Pass for Normal", mind=2, prime=2)
effect.description = "This effect adds a dot each to Wits, Expression and Etiquette, as well as suppressing the worst responses to the general weirdness that many mages carry with them."
effect.save()
effect.add_source("Hidden Lore", 18)
effect, _ = Effect.objects.get_or_create(
    name="Selective Edit", correspondence=2, entropy=2
)
effect.description = "This Procedure gives an operative a temporary Cloaking background, hiding them effectively from electronic surveillance, causing them to not appear in video feeds, etc."
effect.save()
effect.add_source("Guide to the Technocracy", 206)
effect, _ = Effect.objects.get_or_create(
    name='Sjonhverfing ("Deceiving of the Sight")[0]', mind=2
)
effect.description = "With this magic, the mage can cloud the minds of men. The most basic version allows the mage to strike fear into all those in their presence. A more advanced version allows them to instill illusions into those minds, making them see what the mage wishes them to. With Entropy, they can destroy the target's sense of up and down, or even summon a mist. This is dispelled if the mage is blindfolded."
effect.save()
effect.add_source("Dead Magic 2", 103)
effect, _ = Effect.objects.get_or_create(name="Well, It Is Vegas", mind=3)
effect.description = "In a place like Las Vegas, where strange sights have become commonplace, this rote allows the mage to take on temporary Arcane."
effect.save()
effect.add_source("Fallen Tower: Las Vegas", 121)
effect, _ = Effect.objects.get_or_create(name="Antinoise", forces=2)
effect.description = "Creates a sonic dampening field around the agent, inverting and silencing all audio signals the enter the affected area."
effect.save()
effect.add_source("Technocracy: Iteration X", 48)
effect, _ = Effect.objects.get_or_create(name="Being Invisible", forces=3, mind=3)
effect.description = "So long as the Hollow One stays still, this rote hides them in the shadows and causes people to look the other way, rendering them effectively invisible."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 61)
effect, _ = Effect.objects.get_or_create(name="Cloak of Shadows", entropy=2)
effect.description = "An old Ksirafai trick, the Cloak of Shadows warps chance and detects weaknesses to help with stealth. By taking some time to scout the area where the mage wants to be sneaky, this rote helps to detect the best places to hide and to avoid passing unnoticed. As such, this rote provides a difficulty decrease on a stealth roll."
effect.save()
effect.add_source("Order of Reason", 69)
effect, _ = Effect.objects.get_or_create(name="Dark Streets", forces=2, entropy=2)
effect.description = "The mage causes streetlight to flicker and dim, shadows to grow longer, etc., so that the mage has the cover of darkness to hide them or keep their features ambiguous."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 62)
effect, _ = Effect.objects.get_or_create(
    name="Dreamer's Shroud from Day", correspondence=4
)
effect.description = "This rote allows the mage to warp space around them so that they are hidden from sight, making them effectively invisible."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 186)
effect, _ = Effect.objects.get_or_create(name="Energy Shield", forces=2)
effect.description = "Allows the mage to block out a specific type of energy, allowing the mage to render something invisible, inaudible, immune to electricity, etc."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 166)
effect, _ = Effect.objects.get_or_create(
    name='Huli Shjalmr ("Helmet of Hiding")[0]', forces=2, prime=2
)
effect.description = "The Huli Shjalmr grants the power of invisibility, by either warping light around them, hiding themselves from the Minds of those around them, or destroying the very concept of them in those minds."
effect.save()
effect.add_source("Dead Magic 2", 103)
effect, _ = Effect.objects.get_or_create(name="Return to Darkness", forces=2, entropy=2)
effect.description = "By causing whatever is necessary to fail, this rote extinguishes all nearby light sources, plunging the area into darkness. Forces 3 is necessary for a larger area or brighter light sources."
effect.save()
effect.add_source("Hidden Lore", 16)
effect, _ = Effect.objects.get_or_create(name="Shadow Project", forces=2)
effect.description = "This effect pushes away light, drawing shadows around the mage and hiding them from sight."
effect.save()
effect.add_source("Orphan's Survival Guide", 126)
effect, _ = Effect.objects.get_or_create(name="Shinobijutsu", correspondence=3)
effect.description = "The variants on this rote are different ways for an Akashic to become unseen. With Correspondence, the Akashic folds space so that light passes around them, with Forces they can create a more traditional illusion of invisibility, with Mind they can alter the perceptions of others directly to not see them, and with Entropy they can destroy the very idea of the mage's presence."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 69)
effect, _ = Effect.objects.get_or_create(name="The Silent Circle", forces=2)
effect.description = (
    "Creates an area where sound and light are dampened, though not entirely removed."
)
effect.save()
effect.add_source("The Swashbuckler's Handbook", 93)
effect, _ = Effect.objects.get_or_create(name="Smoke Screen", matter=2, mind=3)
effect.description = "Using a cigarette, the Hollow One releases a powerful hallucinogen into the air. Targets can resist the effects with a Willpower roll. Successes determine how long the cloud lasts (in hours) and how wild the hallucinations are."
effect.save()
effect.add_source("World of Darkness: Outcasts", 91)
effect, _ = Effect.objects.get_or_create(name="Smoke-bomb Trick", matter=2, prime=2)
effect.description = "Fills the area with a thick black smoke that blocks vision and irritates eyes. The smoke remains effective for one round per success."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (First Edition)", 63)
effect, _ = Effect.objects.get_or_create(name="Sulfurous Darkness", matter=1, forces=2)
effect.description = "With a flame and some chemicals, the mage can create a flash and fill a space (size depending on successes) with black, unpleasant smoke. If Life and Entropy are added, everyone within the area must roll Stamina at difficulty 8 or else spend two rounds choking and gagging."
effect.save()
effect.add_source("Artisan's Handbook", 51)
effect, _ = Effect.objects.get_or_create(name="Summon Fog", matter=3)
effect.description = "Conjures up a fog, which can provide cover, make Perception rolls more difficult, or other effects determined by the Storyteller."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 63)
effect, _ = Effect.objects.get_or_create(name="Veil of Invisibility", life=3, forces=2)
effect.description = "The mage alters their body to the point where it no longer interacts with light. Though one success might just render them blurry, three or more grant complete invisibility."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 223)
effect, _ = Effect.objects.get_or_create(
    name="Ariadne's Thread", correspondence=1, matter=1
)
effect.description = "The mage who uses this rote is always capable of backtracking. This gives them a perfect recollection of the actual locations in space that they have passed through. Regardless of if every landmark along the way changes, they will be able to find their way back."
effect.save()
effect.add_source("Book of Shadows", 144)
effect, _ = Effect.objects.get_or_create(name="Chain", correspondence=3)
effect.description = (
    "Chain allows a mage to strengthen or weaken the connections between objects."
)
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 189)
effect.add_source("Mage: The Ascension (Revised)", 159)
effect, _ = Effect.objects.get_or_create(name="Smoker's Timing", time=2)
effect.description = "It's a well-known urban legend that if a smoker is waiting for something, it will happen the moment they start a cigarette. Taking advantage of that, a Tradition mage can predict when something will happen by timing it with their cigarette. A single success causes them to have taken a single drag on the cigarette before things happen, while four or more successes might cause it to happen just when they finish a cigarette."
effect.save()
effect.add_source("Guide to the Traditions", 280)
effect, _ = Effect.objects.get_or_create(name="Perfect Fuse", time=1, forces=2)
effect.description = "Allows the mage to set a fuse for the appropriate amount of time for their purposes, whatever they may be."
effect.save()
effect.add_source("Artisan's Handbook", 51)
effect, _ = Effect.objects.get_or_create(name="Synchronize Watches", time=1)
effect.description = "This procedure coordinates the timing of an operation, allowing each member of an amalgam to agree on what time it is, precisely."
effect.save()
effect.add_source("Technocracy: New World Order", 48)
effect, _ = Effect.objects.get_or_create(name="Co-Location", correspondence=5)
effect.description = "A Master of Correspondence can cause two distinct locations to overlap and interact directly. No damage is caused by superimposition, but once separated two objects cannot be superimposed again."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 188)
effect.add_source("Mage: The Ascension (Second Edition)", 191)
effect.add_source("Mage: The Ascension (Revised)", 160)
effect, _ = Effect.objects.get_or_create(
    name="Conference Call", correspondence=4, forces=4, prime=2
)
effect.description = "Using a specially arrange conference room that includes hard-light projectors, high-speed internet connections and proper computers, a Syndicate agent can be in multiple meetings at once."
effect.save()
effect.add_source("Technocracy: Syndicate", 49)
effect, _ = Effect.objects.get_or_create(name="Polyappearance", correspondence=4)
effect.description = "The mage is in multiple places simultaneously. Observers see the mage's interactions with all locations; however, they are not able to act independently. To process the information from multiple locations, Mind is extremely helpful, and with Life and Prime in addition to Mind, the mage can create additional bodies and split their attention."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 187)
effect.add_source("Mage: The Ascension (Second Edition)", 191)
effect.add_source("Mage: The Ascension (Revised)", 160)
effect, _ = Effect.objects.get_or_create(
    name="Simon's Petition", correspondence=4, mind=1
)
effect.description = "The legendary Simon of Ghita was able to address many visitors to his tower simultaneously from different windows. This effect allows a mage to be in multiple places at once and hold independent conversations."
effect.save()
effect.add_source("Order of Reason", 107)
effect, _ = Effect.objects.get_or_create(name="Accelerate Time", time=3)
effect.description = "The mage can dilate time, speeding it up in a given area, as though fast-forwarding."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 218)
effect.add_source("Mage: The Ascension (Second Edition)", 223)
effect, _ = Effect.objects.get_or_create(name="An Hour in Hellfire", time=3, mind=3)
effect.description = "Originating among the Fallen, this rote allows the mage to prolong any sensation whatsoever. Whether painful or pleasurable in origin, it is drawn out for an endless moment and amplified to the point of being overwhelming. Contrary to the title, this is not just an hour, but rather lasts for the usual duration, and is most commonly used as a form of torture. To concentrate while the victim of this effect, a Willpower roll is necessary with difficulty determined by how intense the base sensation is. This effect can only be broken, however, by a sensation more powerful than the original stimulus."
effect.save()
effect.add_source("Infernalism: The Path of Screams", 86)
effect, _ = Effect.objects.get_or_create(name="Distort Time", time=3)
effect.description = "A Disciple of Time can generate fast and slow time bubbles. Every two successes allow the mage to accelerate or decelerate by one factor, so that two successes doubles, four triples, etc. This includes actions in combat."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 193)
effect, _ = Effect.objects.get_or_create(
    name="Establish and Exchange Temporal Event Fields", time=5
)
effect.description = "This allows the Void Engineer to create a 'Temporal Event Field' around a distant point in time. By using Establish Local Temporal Event Field around the Chrononaut, the two fields can have their contents exchange, essentially time travel."
effect.save()
effect.add_source("Technocracy: Void Engineers", 47)
effect, _ = Effect.objects.get_or_create(
    name="Establish Local Temporal Event Field", time=4
)
effect.description = "This procedure pauses time around an individual or an object."
effect.save()
effect.add_source("Technocracy: Void Engineers", 46)
effect, _ = Effect.objects.get_or_create(
    name="The Frenzy of the Spinning Wheels", time=3
)
effect.description = "Allows the user to operate machinery that requires many simultaneous actions by themselves."
effect.save()
effect.add_source("Artisan's Handbook", 52)
effect, _ = Effect.objects.get_or_create(
    name="The Moment that Stretches", time=3, mind=1
)
effect.description = "The mage can alter their sense of time, allowing them to subjectively experience a much longer period's time than occurs. Note, this doesn't give extra actions and no other magick may be done during this, but mental processes move much more quickly. Mind 4 is needed to include others."
effect.save()
effect.add_source("Hidden Lore", 14)
effect, _ = Effect.objects.get_or_create(
    name="Nick of Time", correspondence=3, time=2, entropy=3
)
effect.description = "This rote gives the Reality Hacker excellent timing, just right for whatever it is they need to do in a situation. Often, this helps find jobs, being online at the right time, or at the next table to someone who needs to hire a person like them."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 64)
effect, _ = Effect.objects.get_or_create(
    name="Quantum Temporal Travel", correspondence=3, time=3, entropy=4
)
effect.description = "Rather than attempting 'true' time travel, some Etherites have developed a technique for traveling to the pasts and futures of alternate timelines. This cannot change the present, but it can still be useful: visiting a Utopian future for inspiration, for instance. Some Ethernauts even explore these universes out of pure curiosity, venturing into strange alternate realities. Correspondence 3 transports one person, 4 can transport a group, Time 4 allows very short hops (one round/success) while Time 5 is needed for extended journeys, and Time combined with Entropy allows the mage to travel to an alternate timeline rather than the 'true' one."
effect.save()
effect.add_source("Tradition Book: Sons of Ether (Revised)", 63)
effect, _ = Effect.objects.get_or_create(
    name="Serenity of the Stone", time=5, life=3, entropy=4, mind=3, prime=5
)
effect.description = "Rather than actively making a mage younger, some opt to slow the process of aging to the point where it is barely happening at all. Maintaining it requires that the mage expend a point of Quintessence every week, or else take a Lethal damage per day and begin aging rapidly to at least (often more) than their actual age. This effect usually causes a mage to age by a single year for every fifty that they experience."
effect.save()
effect.add_source("Horizon: Stronghold of Hope", 115)
effect.add_source("Masters of the Art", 76)
effect, _ = Effect.objects.get_or_create(
    name="Shed the Years", time=2, life=3, entropy=4, mind=2, prime=5
)
effect.description = "Potions of Youth, Phoenix Engines, and other techniques for decreasing age all fall under this rote. With it, the mage can return their body to the state it was in nine years prior. It requires at least five successes and is vulgar everywhere on Earth and only safely used in an appropriate Horizon Realm."
effect.save()
effect.add_source("Horizon: Stronghold of Hope", 114)
effect.add_source("Masters of the Art", 76)
effect, _ = Effect.objects.get_or_create(name="Sidestep Time", time=5)
effect.description = "The Master of Time can step outside of the flow of time, effectively halting the entire world, from their perspective."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 219)
effect.add_source("Mage: The Ascension (Second Edition)", 223)
effect.add_source("Mage: The Ascension (Revised)", 193)
effect, _ = Effect.objects.get_or_create(name="Slow Time", time=3)
effect.description = "The opposite of Elemental Magick, Slow Time decreases the flow of time in a small area."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 219)
effect.add_source("Mage: The Ascension (Second Edition)", 223)
effect, _ = Effect.objects.get_or_create(name="St. Vitus's Kiss", time=3)
effect.description = "This effect speeds up the mage's reflexes, giving extra actions for successes after the first."
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 272)
effect.add_source("The Swashbuckler's Handbook", 95)
effect, _ = Effect.objects.get_or_create(name="Symphony of the Soul", time=3)
effect.description = "This rote grants the mage extra actions in combat and is particularly appropriate for melee combat and fencing."
effect.save()
effect.add_source("Order of Reason", 87)
effect, _ = Effect.objects.get_or_create(name="Time Warp", time=3)
effect.description = "If need be, a Disciple of Time can rewind time locally, spending successes on area, granting immunity from the effect to others, and how far back to rewind (up to one round per success). Repeated use of this effect becomes harder, as rewinding past an already performed rewind needs to spend successes to overcome the successes on the original rote."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 193)
effect, _ = Effect.objects.get_or_create(
    name="Tune In, Turn On, Drop Out", time=4, life=3
)
effect.description = "This rote freezes time for the mage's Pattern, causing them to fake death. For each hour in this state, the mage takes one level of Lethal damage. The mage has frozen time for their brain as well, so they have no awareness of the time passing or what is going on around them."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 228)
effect, _ = Effect.objects.get_or_create(
    name="Zen and the Art of Panhandling", time=5, prime=3
)
effect.description = "The mage can 'borrow' Quintessence from their future self, but they cannot be sure how far into the future. They may gain one Quintessence for each success, and at some point, in the future, the Storyteller informs them that they have lost an equivalent amount of Quintessence."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 229)
effect, _ = Effect.objects.get_or_create(name="Blindside", correspondence=4, matter=2)
effect.description = "Though this only causes minor damage, the Nephandus can use it to get under their victim's skin by attacking them using a route that seems impossible. Some popular choices are to reach through a drain, send gas through a telephone handset, or fill a confined area with water."
effect.save()
effect.add_source("Hidden Lore", 50)
effect, _ = Effect.objects.get_or_create(name="Bubble of Reality", correspondence=4)
effect.description = "A mage with the appropriate knowledge can create a pocket dimension, trapping an object or being outside of space."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 190)
effect.add_source("Mage: The Ascension (Revised)", 160)
effect, _ = Effect.objects.get_or_create(name="Daedalean Labyrinth", correspondence=5)
effect.description = "Creates a region of confusing space, where it is easy to become lost. This is usually used to protect a secret portion of a library, a mansion at the center of a hedge maze, or the like. Anyone trapped in the Labyrinth gets lost if they don't get more successes on a Willpower roll than the labyrinth designer got in creating it. Once lost, Correspondence is necessary to find your location and work your way out of the labyrinth."
effect.save()
effect.add_source("Order of Reason", 107)
effect, _ = Effect.objects.get_or_create(name="Maze of the Minotaur", mind=3)
effect.description = "A craftsman can build a maze so complex that it causes anyone inside it to lose their sense of direction. With just Mind, the target loses track of their path, doubts their techniques to keep track of it, and needs to acquire more successes on Wits + Enigmas rolls than the number of successes on this effect. With Correspondence included, the area itself becomes more confusing and mutable."
effect.save()
effect.add_source("Dead Magic", 107)
effect, _ = Effect.objects.get_or_create(name="Singularity", correspondence=4, time=3)
effect.description = "Using exotic matter, a Void Engineer can produce an actual singularity. This singularity will slow down time nearby and cause other relativistic effects. They can also be used as gateways to another location. Successes are first spent on targets/area, then distance and duration, and then time slows by a factor of 1 + successes. Optionally, time travel to up to one round per success before the Singularity is formed is possible, though of course at the levels of paradox caused by time travel."
effect.save()
effect.add_source("Convention Book: Void Engineers (Revised)", 86)
effect, _ = Effect.objects.get_or_create(name="Spatial Mutations", correspondence=5)
effect.description = "Though creating space directly is more complex than can be achieved with a single Sphere, a Master of Correspondence can bend space to their whim. They can cause things to shrink, grow, distort in other way, can cause geometries that are impossible in the normal world, their imagination is the only limit."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 188)
effect.add_source("Mage: The Ascension (Second Edition)", 191)
effect.add_source("Mage: The Ascension (Revised)", 160)
effect, _ = Effect.objects.get_or_create(name="Chiminage Rune", spirit=2, prime=3)
effect.description = "This rune creates a channel between the mage and the spirit allowing them to send Quintessence to the spirit in exchange for a service. With Prime 4, Quintessence can be drawn from the earth, rather than from the mage's personal reserves."
effect.save()
effect.add_source("Dead Magic 2", 101)
effect, _ = Effect.objects.get_or_create(name="Dimension Bomb", spirit=3)
effect.description = "Often used to attack Extra Dimensional Entities, the Technocrat can push a small object through the Gauntlet."
effect.save()
effect.add_source("Guide to the Technocracy", 207)
effect.add_source("Mage: The Ascension (20th Anniversary Edition)", 605)
effect, _ = Effect.objects.get_or_create(name="Hellfire", spirit=2)
effect.description = "Like the Prime effect Wrath of God, except that it works against ghosts and spirits."
effect.save()
effect.add_source("Order of Reason", 85)
effect, _ = Effect.objects.get_or_create(
    name="Sharing the Outsider's Gaze", spirit=3, mind=4, prime=1
)
effect.description = "This allows the mage to share in a Spirit's senses. Spirits often have senses completely alien to humans (tasting quintessence, experiencing emotions as tangible, etc.). Each success gives access to a sense that is analogous to a human sense but attuned to something else (such as seeing destiny), two successes allows access to a truly alien sense (i.e., four-dimensional perception) though this requires a Willpower roll with difficulty at least 7. Success means that the mage can effectively use the sense, failure or, worse, botching, risks pushing the mage into Quiet."
effect.save()
effect.add_source("Infinite Tapestry", 183)
effect, _ = Effect.objects.get_or_create(
    name="Spirit Eating", spirit=2, mind=3, prime=3
)
effect.description = "The Dreamspeaker empowers a weapon to attack a spirit, as in Spirit Slaying. Unlike Spirit Slaying, the mage doesn't only attack the spirit, but siphons off its Prime energy and its knowledge, consuming them. The spirit destroyed this way is gone forever. Each level of damage done with this rote gives the user a point of Quintessence and reduces the spirit's Power by 5 points. If the spirit's Power reaches 0, it is destroyed forever. Successes on this effect also go into absorbing the memories of the spirit. One success gives a few memories, two gives access to the most recent memories, three give most memories and four or more give access to virtually all memories."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (Revised)", 69)
effect, _ = Effect.objects.get_or_create(name="Spirit Slaying", spirit=2, prime=2)
effect.description = "A Dreamspeaker can infuse a weapon with prime energy so that it can strike through the Gauntlet at spirits."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (Revised)", 69)
effect, _ = Effect.objects.get_or_create(name="Spirit Wounding", spirit=4, matter=3)
effect.description = "Learned from the Fae, this rote allows a Verbena to push physical objects into the Umbra without entering it themselves."
effect.save()
effect.add_source("Book of Shadows", 143)
effect, _ = Effect.objects.get_or_create(name="The Spirit's Caress", spirit=2)
effect.description = "The mage can directly interact with spirits through the Gauntlet with this rote, reaching across to touch them. It can be used to attack a spirit, but it can also be combined with Bond of Blood to give Quintessence to the spirit."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 218)
effect.add_source("Mage: The Ascension (Revised)", 187)
effect, _ = Effect.objects.get_or_create(name="Spiritual Persuasion", spirit=2, mind=2)
effect.description = "This rote both summons a spirit and influences it to be more favorably inclined towards the shaman. It decreases the difficulty of rolls to persuade the spirit by one per success."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="Binding Song", correspondence=4, time=3)
effect.description = "The Binding Song halts a person in time and space. They will perceive what is going on around them, and if the caster wishes, they may speak, but all other movement is impossible."
effect.save()
effect.add_source("Dead Magic 2", 126)
effect, _ = Effect.objects.get_or_create(
    name="Bottle of Djinn", spirit=4, matter=3, prime=2
)
effect.description = "Using techniques going back to Suleiman the Wise himself, the Taftani is no longer at the mercy of Djinni, but rather can control them. By creating a container and a trigger phrase, a djinn can be sucked into the bottle, and the mage has three turns to seal the bottle so that the djinn cannot escape."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 88)
effect, _ = Effect.objects.get_or_create(
    name="Circle of Binding", correspondence=4, spirit=4, prime=4
)
effect.description = "The Order of Hermes has always had powerful techniques for summoning and binding spirits. Most of these techniques have, at their core, a Circle of Binding. This takes the form of a circle inlaid on the floor (often in a precious metal) and graven with sigils and signs. This rote summons the spirit and traps it within wards, permitting spirits in but not out of the Circle. The usage of Prime accrues successes to resist any mystical effect that the spirit uses within the Circle."
effect.save()
effect.add_source("Infinite Tapestry", 182)
effect, _ = Effect.objects.get_or_create(name="Coerce Spirit", spirit=2, mind=3)
effect.description = "Sometimes a shaman doesn't know how to handle a spirit or otherwise cannot manage a negotiation. Instead, they can use this rote, though it tends to hurt their relationship with spirits in general. The Spirit 2 version attempts to seize control of the spirit's consciousness, whereas Spirit 4 allows the shaman to take over the spirit's ephemeral nature directly."
effect.save()
effect.add_source("The Spirit Ways", 89)
effect, _ = Effect.objects.get_or_create(name="Compel the Unseen", spirit=2, prime=3)
effect.description = (
    "Hermetics have used this rote for centuries to force a spirit to materialize."
)
effect.save()
effect.add_source("Tradition Book: Order of Hermes (First Edition)", 65)
effect, _ = Effect.objects.get_or_create(name="Drahma Protector", spirit=4, mind=4)
effect.description = "This rote makes a spirit accept the Akashic paradigm. The spirit will then protect Akashics wherever it finds them. The mage needs more successes than the spirit's Gnosis + Willpower to make the spirit loyal to the Akashayana for the duration of the effect."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 69)
effect, _ = Effect.objects.get_or_create(
    name="Ensure the Endless Sleep", spirit=2, matter=2, mind=3
)
effect.description = "It is essential that Dreamtime spirits stay asleep (see Dreamborn Rising for some consequences if they do not). This rote allows mages to guarantee that such spirits stay in a deep slumber."
effect.save()
effect.add_source("Dead Magic 2", 64)
effect, _ = Effect.objects.get_or_create(name="Exorcism", spirit=4)
effect.description = "Just as an Adept of Spirit can bind a spirit to an object or person, they can forcibly remove one. This rote triggers a contested Willpower roll between the spirit and the mage, and if the mage can gather enough successes (determined by the strength of the Spirit), the mage can force the Spirit out."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 219)
effect, _ = Effect.objects.get_or_create(name="Exorcism Song", spirit=2, mind=4)
effect.description = "A combination of Mind and Spirit magick are used to gentle coax a spirit who is unwanted to leave their host."
effect.save()
effect.add_source("Dead Magic 2", 126)
effect, _ = Effect.objects.get_or_create(name="Gauntlet Prison", spirit=4)
effect.description = "An Adept of Spirit has fine enough control over the Gauntlet to trap a spirit, or other traveler, inside it."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 215)
effect.add_source("Mage: The Ascension (Second Edition)", 218)
effect, _ = Effect.objects.get_or_create(
    name="Halt the Nagloper", time=2, matter=2, life=2
)
effect.description = "By placing a false club at the entrance to a home, it causes a nagloper who tries to enter to freeze so long as no one speaks within its hearing."
effect.save()
effect.add_source("Dead Magic", 28)
effect, _ = Effect.objects.get_or_create(name="The Holy Pentacles", spirit=4)
effect.description = "Hermetics have special symbols, called pentacles, that they use for summoning and binding of spirits. This effect combines Breach the Gauntlet and Gauntlet Prison to first permit a spirit to enter and then to trap them within the area."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (First Edition)", 66)
effect, _ = Effect.objects.get_or_create(name="Imbue Flesh", spirit=2, life=2)
effect.description = "Given a body with no spirit in it, this allows the mage to bind a spirit to it as a Familiar."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 224)
effect, _ = Effect.objects.get_or_create(
    name="Lesser Binding of Spirits", spirit=2, prime=2
)
effect.description = "While higher levels of Spirit are needed to directly compel spirits to do a mage's bidding, this rote summons a spirit and immediately encloses it in a cage of primal energy. Another success creates the primal cage capable of causing two levels of aggravated damage at any time the mage wills it, two additional successes can make the effect last for up to a day (or until used) and cause four levels of damage instead of two. With Mind 2, the mage creates a sensation of the futility of resistance in the spirit."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (Revised)", 66)
effect, _ = Effect.objects.get_or_create(name="Living Bridge", spirit=4)
effect.description = "The mage makes a pact with a powerful spirit and may channel some of that spirit's powers for the duration of the effect."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 219)
effect, _ = Effect.objects.get_or_create(
    name="Lull the Waking Dreamborn", spirit=2, mind=3
)
effect.description = "This long ritual is used by Aboriginal Australians to lull a spirit into slumber. The ritual gathers successes opposed by the spirit's Willpower roll. If the mage is a child of a specific Dreamborn who is being lulled back to sleep, the difficulty of the ritual is at -2. If the spirit loses, it falls into Slumber."
effect.save()
effect.add_source("Dead Magic 2", 65)
effect, _ = Effect.objects.get_or_create(
    name="Physical Exorcism", spirit=4, life=3, prime=2
)
effect.description = "Sometimes, an invasive spirit needs to be destroyed. This rote not only expels it from whoever or whatever it is possessing, but also binds it into a newly created physical form that can be killed."
effect.save()
effect.add_source("The Spirit Ways", 91)
effect, _ = Effect.objects.get_or_create(
    name="Weaver's Retribution", correspondence=3, spirit=4, forces=3, mind=2, prime=2
)
effect.description = "This rote is rarely taught, and even more rarely used. It is largely considered a suicide maneuver only to be used in the most desperate circumstances. The Taftani first expands their senses to find every djinn within several kilometers, then simultaneously unseals all of them. The djinni then proceed to do whatever they want, which is usually wanton and undirected destruction, killing the mage, their enemies, and whatever else is nearby."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 92)
effect, _ = Effect.objects.get_or_create(name="Detect Possession", spirit=1)
effect.description = "Determines if there is a foreign spirit in a person or object, though without Cosmology or Mind magick, the mage doesn't necessarily understand much other than that the spirit is present."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 217)
effect.add_source("Mage: The Ascension (Revised)", 187)
effect, _ = Effect.objects.get_or_create(
    name="Evaluate Gauntlet/Scan Locality", spirit=1
)
effect.description = "This allows the Void Engineer to check the strength of the Gauntlet in a given location."
effect.save()
effect.add_source("Technocracy: Void Engineers", 41)
effect, _ = Effect.objects.get_or_create(
    name="Sense the Demon's Weakness", spirit=1, entropy=1
)
effect.description = "This allows a Wu Lung to focus on a demon and determine the essential weakness of its nature."
effect.save()
effect.add_source("Book of Crafts", 135)
effect, _ = Effect.objects.get_or_create(
    name="Sense the Nagloper", time=2, matter=1, life=2
)
effect.description = "The mage makes a shallow cut in the subject and rubs in a magickal powder. If a nagloper approaches, this burns and itches, awakening the subject so that they may defend themselves."
effect.save()
effect.add_source("Dead Magic", 28)
effect, _ = Effect.objects.get_or_create(name="Shadows in the Mist", spirit=1, forces=2)
effect.description = "In a fog or a mist, this rote allows the wisps to form the rough shapes of umbral objects and beings."
effect.save()
effect.add_source("Book of Shadows", 143)
effect, _ = Effect.objects.get_or_create(
    name='Ap-Sobk "The Last Judgment of Sobk"', spirit=4
)
effect.description = "For a high-ranking member of the Hem-Ka Sobk, they can spit on their palms, rub them together, and petition Sobk for assistance. If they succeed, it is equivalent to Living Bridge, causing the mage to be possessed by the crocodile god itself. Misuse of this rote results in the spirit killing the mage."
effect.save()
effect.add_source("Book of Crafts", 58)
effect, _ = Effect.objects.get_or_create(
    name="Call Forth the Forgotten", spirit=2, life=5, prime=2
)
effect.description = "The mage calls forth a creature of myth, summoning an appropriate spirit to inhabit a newly created form. If the creature is to have any powers other than just a body, the mage needs to include other Spheres (such as Forces for flight or fire-breathing, in the case of a dragon)."
effect.save()
effect.add_source("Book of Shadows", 147)
effect, _ = Effect.objects.get_or_create(name="Call Spirit", spirit=2)
effect.description = "Allows the mage to call out for a spirit to show up, it can be a general call or specific. Powerful spirits rarely appear, but a powerful call can compel weaker ones to do so."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 214)
effect.add_source("Mage: The Ascension (Second Edition)", 217)
effect.add_source("Mage: The Ascension (Revised)", 187)
effect, _ = Effect.objects.get_or_create(name="Call the Dreamborn Sibling", spirit=2)
effect.description = (
    "This rote is used by Aboriginal Australians to summon spirits of the Dreamtime."
)
effect.save()
effect.add_source("Dead Magic 2", 63)
effect, _ = Effect.objects.get_or_create(
    name="Conjure the Jade Warrior", spirit=5, matter=3, prime=3
)
effect.description = "This rote is used by the Wu Lung to create a giant warrior clad in ancient, jade armor. This warrior is then inhabited by a warrior spirit and exists both physically and in the spirit realm simultaneously."
effect.save()
effect.add_source("Book of Crafts", 135)
effect, _ = Effect.objects.get_or_create(
    name="Dreamborn Rising", spirit=2, matter=4, life=4, mind=3
)
effect.description = "This rote can rouse a quiescent Dreamborn spirit. As this only can affect the most powerful such spirits and they emerge ravenous for Quintessence and life form with no sense of who they are, this rote is forbidden. This is in direct opposition to Ensure the Endless Sleep."
effect.save()
effect.add_source("Dead Magic 2", 63)
effect, _ = Effect.objects.get_or_create(
    name="Drums of Elemental Fire", spirit=2, matter=2, forces=2
)
effect.description = "Drums are a well-known and long venerated instrument for spirit magic. With this rote, a drummer can bring forth an elemental spirit. Of course, this doesn't guarantee that the elemental will be friendly."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 227)
effect, _ = Effect.objects.get_or_create(name="Enter the Sauna", spirit=2)
effect.description = "The mage uses a meditative trance to reach out to spirits. For each success, the mage may ask one yes/no question of the divining spirits."
effect.save()
effect.add_source("Dead Magic 2", 126)
effect, _ = Effect.objects.get_or_create(name="Free the Mad Howlers", spirit=3)
effect.description = "This rote summons frenzied, angry spirits to attack their enemies. With Spirit 3 the mage summons spirits who can materialize, with Spirit 4 they seal the spirits into their targets as though they were a fetish, causing the spirits to possess them."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 218)
effect, _ = Effect.objects.get_or_create(name="Gremlins", spirit=2, entropy=2)
effect.description = "A Dreamspeaker who must deal with a Technomagickal problem will often summon gremlins, spirits that arose during the Second World War that interfere with machinery."
effect.save()
effect.add_source("Hidden Lore", 15)
effect, _ = Effect.objects.get_or_create(
    name="Here Kitty, Kitty", correspondence=3, time=3, mind=3
)
effect.description = "Created by a Virtual Adept named Zer0 Effect, this rote summons something that hates your opponent... though there's no guarantee that it won't ALSO hate you. Mind draws something from your opponent's fears, and Correspondence and Time open coincidental means for that thing to show up in a timely manner."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 62)
effect, _ = Effect.objects.get_or_create(name="Jack in the Green", spirit=3, life=2)
effect.description = "This rote awakens the spirit of a tree and allows the mage to communicate with it. Winter makes it harder, as does the tree being in an urban setting."
effect.save()
effect.add_source("Hidden Lore", 18)
effect, _ = Effect.objects.get_or_create(name="Loving Scar", spirit=2, life=3)
effect.description = "The Nephandus scars the victim. The more intimate the situation the leads to it, and the more willing the victim is, the more effective this rote is. This scar does no damage, but Life 4 is needed to remove it. The victim then attracts low level spirits to spy on them and torment them, though they do no (lasting, physical) damage."
effect.save()
effect.add_source("Hidden Lore", 49)
effect, _ = Effect.objects.get_or_create(name="Nuzzlings", spirit=3, matter=3, prime=5)
effect.description = "This creates a zone of objects animated by spirits centered on the mage. Successes dictate how large this zone is, and the objects drain Quintessence from any sources in the area."
effect.save()
effect.add_source("Hidden Lore", 52)
effect, _ = Effect.objects.get_or_create(
    name="Protection of the Golden Race", spirit=5, prime=2
)
effect.description = "The Golden Race are the first humans in Greek mythology, the ones who lived during the Golden Age. This rote summons a member of the Golden Race to protect the mage from an opponent. It is always vulgar and may require many successes, but if the member of the Golden Race appears, there is a flash of golden light as it harms the attacker in some appropriate manner."
effect.save()
effect.add_source("Dead Magic", 108)
effect, _ = Effect.objects.get_or_create(
    name="Pygmalion's Paradigm", spirit=2, matter=4, life=3, prime=2
)
effect.description = "The mage crafts a body out of high-quality materials to be inhabited by a Familiar. The number of successes determines how powerful a Familiar can be housed in this body."
effect.save()
effect.add_source("Book of Shadows", 146)
effect, _ = Effect.objects.get_or_create(
    name="Satan's Song", spirit=2, forces=2, mind=2, prime=3
)
effect.description = "Although Prime is the highest ranked sphere, this is primarily a Mind and Spirit effect. The mage begins a musical performance, and uses it to summon demons, and to cause hallucinations in the audience. The Song inflames whatever lusts the audience is feeling, and can quickly, with enough successes, bring absolute mayhem to wherever the Song is being performed. With further Pattern spheres added in, the Song will raise the dead, bringing undead into the chaotic and unconstrained revelry along with the hallucinations and the demons."
effect.save()
effect.add_source("Infernalism: The Path of Screams", 86)
effect, _ = Effect.objects.get_or_create(name="Shaking Tent", spirit=3)
effect.description = "The Innu Shaman enters a cylindrical tent calls up a spirit. The shaman opens themselves up to communion with the spirit to negotiate whatever it is that they want from it. This ritual confines the spirit to the tent, so long as no one is foolish enough to open it."
effect.save()
effect.add_source("Dead Magic", 131)
effect, _ = Effect.objects.get_or_create(
    name="Spirit Roster", correspondence=2, spirit=1
)
effect.description = "This rote finds any nearby spirits and, with Spirit 2, allows the mage to speak with them."
effect.save()
effect.add_source("Hidden Lore", 15)
effect, _ = Effect.objects.get_or_create(name="Summon Paradox Spirit", spirit=2)
effect.description = "Under desperate circumstances, a Technocrat who knows how can summon a Paradox Spirit into an area. It will tend to focus on whoever has accumulated the most Paradox, but it is still a desperate gamble, not used unless there is no other choice."
effect.save()
effect.add_source("Technocracy: New World Order", 49)
effect, _ = Effect.objects.get_or_create(
    name="Summon the Earthly Gods", correspondence=4, spirit=4, mind=4
)
effect.description = "The Wu Lung claim a Heavenly authority over Eastern supernatural beings. This rote allows them to summon a Kuei-Jin, Hengeyokai or Hsien for an audience, where they cannot harm the mage. This requires 2 successes plus a number equal to the target's permanent Willpower to force the target to travel the swiftest way it can to the Wu Lung's location, though with two additional successes the target is teleported before the mage immediately."
effect.save()
effect.add_source("Dragons of the East", 59)
effect, _ = Effect.objects.get_or_create(
    name="Visionary Bloodletting", spirit=2, mind=1
)
effect.description = "Through bloodletting (at least two lethal damage) in a spiritually significant location on the mage's body, they can commune with gods and spirits and receive visions from them. Spirit calls to the spirit or god and allows the mage to see their message, Mind filters it through appropriate symbols for the mage to interpret."
effect.save()
effect.add_source("Dead Magic", 76)
effect, _ = Effect.objects.get_or_create(name="Zeitgeist", time=2, spirit=2, mind=2)
effect.description = 'The Cultist calls forward the spirit of some time period, such as "The Summer of Love", "Black Tuesday" or "The Burning Times." This unleashes the spirit\'s resonance, to touch the emotions of everyone affected by the rote.'
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (First Edition)", 65)
effect.add_source("Tradition Book: Cult of Ecstasy (Revised)", 73)
effect, _ = Effect.objects.get_or_create(name="Affix Gauntlet", spirit=4)
effect.description = "The mage is capable of precisely hardening the Gauntlet. This allows the mage to prevent spirits from entering or leaving a space, to place a spirit within a person or object, or any number of other effects."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 189)
effect, _ = Effect.objects.get_or_create(name="Circle Ward", spirit=2, mind=1, prime=2)
effect.description = "By summoning four separate, powerful spirits, usually forming a symbolic set of four (seasons, directions, elements), the Verbena creates a safe space in which to work."
effect.save()
effect.add_source("Tradition Book: Verbena (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(name="Counterintelligence", correspondence=1)
effect.description = "Though proactive measures are preferred, in some situations even the New World Order must react to others. This Procedure provides defenses, particularly to mental attacks, and acts as countermagick."
effect.save()
effect.add_source("Technocracy: New World Order", 44)
effect.add_source("Convention Book: New World Order (Revised)", 87)
effect, _ = Effect.objects.get_or_create(
    name="Defense Screen vs. Higher Lifeforms", life=3
)
effect.description = "Like Defense Screen Versus Lower Lifeforms, but it repels more complex life, such as sharks, dolphins or even people, though people can overcome it with a Willpower roll."
effect.save()
effect.add_source("Technocracy: Void Engineers", 43)
effect, _ = Effect.objects.get_or_create(
    name="Defense Screen vs. Lower Lifeforms", life=2
)
effect.description = "This Procedure uses chemical pheromones and ultrasonic vibrations to repel lower lifeforms."
effect.save()
effect.add_source("Technocracy: Void Engineers", 43)
effect, _ = Effect.objects.get_or_create(name="Etheric Shielding", spirit=2, matter=2)
effect.description = "Regular matter can be imbued with the ability to block out otherworldly creatures. Each success spent increases the Gauntlet at the location of the material, blocking spirits from crossing it. If Prime is included, then the material gets additional soak dice against spirit attacks."
effect.save()
effect.add_source("Tradition Book: Sons of Ether (Revised)", 61)
effect, _ = Effect.objects.get_or_create(name="Fortify Gauntlet", spirit=2)
effect.description = "To protect the world from dangerous aliens, Void Engineers have developed techniques for increasing the Gauntlet in small areas."
effect.save()
effect.add_source("Technocracy: Void Engineers", 41)
effect, _ = Effect.objects.get_or_create(name="Magic Circle", spirit=2, prime=2)
effect.description = "This rote creates a circle around the user, of radius one yard per success up to the Verbena's arete. Further successes go to duration (up to the length of a ritual performed inside it) and countermagick. This countermagick protects those inside the circle from attempts to disrupt the ritual, and spirits must make Willpower rolls against it to cross the boundary."
effect.save()
effect.add_source("Tradition Book: Verbena (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="The Master's Hand", life=1, prime=2)
effect.description = 'This sets a device or warding or other long-term and permanent effects to only work or to permit passage to a list of "approved users."'
effect.save()
effect.add_source("Mage Storyteller's Companion", 63)
effect, _ = Effect.objects.get_or_create(
    name="Protection Song", correspondence=4, forces=2
)
effect.description = "This rote combines Ward and Energy Shield and with Spirit, extends to the Umbra as well."
effect.save()
effect.add_source("Dead Magic 2", 126)
effect, _ = Effect.objects.get_or_create(name="Psychic Sterilization", spirit=4)
effect.description = "This Technomagickal rote strengthens the gauntlet in such a way as to keep spirits out of an area."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 215)
effect.add_source("Mage: The Ascension (Second Edition)", 218)
effect, _ = Effect.objects.get_or_create(name="Quahuitl", correspondence=4)
effect.description = "A quahuitl is a cord cut to a specific length for measuring. When used by a mage, they can set specific areas to have specific purposes, like zoning. Functionally like Ward, it prevents the wrong sort of beings from entering or exiting areas."
effect.save()
effect.add_source("Dead Magic", 79)
effect, _ = Effect.objects.get_or_create(
    name="Quantum Interference Shielding", correspondence=2
)
effect.description = "When encountering Extra Dimensional Entities, every Technocrat learns the importance of defense. This procedure allows the Technocrat to strengthen the Gauntlet. With Prime, this shielding also provides countermagick against any attempts to cross or attacks across the Gauntlet."
effect.save()
effect.add_source("Guide to the Technocracy", 207)
effect, _ = Effect.objects.get_or_create(name="Reconstruct Gauntlet", spirit=4)
effect.description = "At this point, a Void Engineer can repair a damaged piece of the Gauntlet, preventing anything from crossing through."
effect.save()
effect.add_source("Technocracy: Void Engineers", 42)
effect, _ = Effect.objects.get_or_create(
    name="Repel the Hungry Dead", spirit=4, prime=2
)
effect.description = (
    "This creates a spiritual barrier around the Wu Lung that prevents possession."
)
effect.save()
effect.add_source("Book of Crafts", 135)
effect, _ = Effect.objects.get_or_create(name="Repel the Kuei", mind=2)
effect.description = "By setting off a string of firecrackers, a Wu Lung can drive away unwanted demons, ghosts and even people."
effect.save()
effect.add_source("Dragons of the East", 59)
effect, _ = Effect.objects.get_or_create(
    name="Safe Little World", correspondence=4, life=3
)
effect.description = "The effect protects the mage's things, so that no one can tamper with them. It prevents anyone or anything from entering without the mage's knowledge. The simplest version prevents human trespassers. With Spirit 3, it can prevent spirits from entering. The Spirit 3/Mind 2 can post a spirit as a guard on the area, and it can attack anyone who enters the area. A simple Mind 3, Life 1, Correspondence 2 effect will let the mage know if anyone enters the area without preventing them from doing so."
effect.save()
effect.add_source("Orphan's Survival Guide", 129)
effect, _ = Effect.objects.get_or_create(
    name="Salt on the Earth", correspondence=4, entropy=1
)
effect.description = "This rote wards an area against Entropic energies. The most common application is to create a circle of salt and use it to block ghosts from entering an area."
effect.save()
effect.add_source("Tradition Book: Euthanatos (Revised)", 66)
effect, _ = Effect.objects.get_or_create(
    name="Secret Labyrinth", spirit=4, mind=3, prime=2
)
effect.description = "Creates a maze around a location designed particularly to trap spirits by strengthening the Gauntlet. The spirit may roll Willpower with difficulty 7, and on more successes than the mage, may refuse to enter the labyrinth. Otherwise, they may roll Intelligence + Enigmas once per day to escape the maze."
effect.save()
effect.add_source("Artisan's Handbook", 53)
effect, _ = Effect.objects.get_or_create(
    name="The Seven Golden Swords of the Tiger",
    correspondence=4,
    spirit=3,
    matter=3,
    forces=2,
    prime=2,
)
effect.description = "A powerful Wu Lung alchemical technique, it creates either a circle of blades or an ultra-sharp barrier. Both versions prevent people, spirits or Correspondence from entering the area it surrounds."
effect.save()
effect.add_source("Book of Crafts", 135)
effect, _ = Effect.objects.get_or_create(name="Spirit Wall", spirit=4)
effect.description = "The mage creates a sigil and uses it to summon a spirit, open a gateway for it, and then trap it with walls to protect the mage from that summoned spirit."
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 273)
effect, _ = Effect.objects.get_or_create(name="Spirit Warding", spirit=2, prime=2)
effect.description = "Spirit Warding protects an area from spiritual attack or interference. With Spirit 2, each success increases the Gauntlet by one to a maximum of ten, and the Spirit 4 version actually creates a shield that prevents spirits from materializing in the region. Furthermore, the Prime 2 component causes damage to any spirit that tries to enter the region."
effect.save()
effect.add_source("The Spirit Ways", 89)
effect, _ = Effect.objects.get_or_create(name="Telltale", correspondence=2)
effect.description = "The Gabrielites and Craftmasons use this common defensive rote to protect objects smaller than a housecat from being stolen via Correspondence magick. The successes of this effect must be overcome before the object can be disturbed."
effect.save()
effect.add_source("Order of Reason", 65)
effect, _ = Effect.objects.get_or_create(name="Time Wards", time=2)
effect.description = "This blocks out a small period of time near the mage so that others cannot easily see into it."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 192)
effect, _ = Effect.objects.get_or_create(
    name="Twisted Yarrow Stalks", correspondence=4, entropy=2, mind=3
)
effect.description = "The Wu-Keng prefer not to announce their power when warding themselves. Using techniques from the I, Ching, the Wu-Keng not only creates a Ward, but creates random impressions of what is there, rather than leaving a more traditional blank space announcing the presence of something of interest."
effect.save()
effect.add_source("Dragons of the East", 66)
effect, _ = Effect.objects.get_or_create(
    name="Wall of Mirrors", correspondence=4, forces=3
)
effect.description = "A purely defensive rote, that, in fact, prevents attacks from being used effectively, the Wall of Mirrors causes all attacks targeting the Chorister to lose successes (depending on strength) as they are deflected through teleportation and alteration of kinetic energy to miss, ricocheting off things, bouncing off a wall, etc."
effect.save()
effect.add_source("Book of Shadows", 140)
effect, _ = Effect.objects.get_or_create(
    name="War of the Inner Sanctum", correspondence=4, life=3
)
effect.description = (
    "This warding effect prevents any living thing from entering a demarcated region."
)
effect.save()
effect.add_source("Tradition Book: Order of Hermes (First Edition)", 66)
effect, _ = Effect.objects.get_or_create(name="Ward", correspondence=4)
effect.description = "A Ward prevents others from being to form connections to the protected location. With conjunctional spheres, it is possible to filter who and what can get through the Ward, and to determine the consequences for crossing it."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 189)
effect.add_source("Mage: The Ascension (Revised)", 159)
effect, _ = Effect.objects.get_or_create(name="Ward Rune", correspondence=4, mind=3)
effect.description = "This rune creates a Ward, preventing the unwanted from being able to find the mage's location. With Spirit, this barrier also stops wraiths and spirits."
effect.save()
effect.add_source("Dead Magic 2", 99)
effect, _ = Effect.objects.get_or_create(name="Warding Heads", spirit=3)
effect.description = "The mage carves a wooden head or mask, and in doing so, makes it into a ward against malevolent spirits."
effect.save()
effect.add_source("Dead Magic", 30)
effect, _ = Effect.objects.get_or_create(name="Zisurru", correspondence=2, spirit=2)
effect.description = "The original ward against demons, from which most Hermetic warding is descended, it creates a boundary which spirits cannot cross."
effect.save()
effect.add_source("Dead Magic", 55)
effect, _ = Effect.objects.get_or_create(name="Back Door Parole", life=3, prime=1)
effect.description = "The simpler version lets the mage enter a trance and stop their bodily functions without damaging them. With Mind, the mage can stay aware of their surroundings. In this case, the mage is capable of walking around and acting while appearing to be dead, fooling almost anyone other than a mage sensing the living Quintessence in them. Notably, this is effective at tricking Vampires."
effect.save()
effect.add_source("Orphan's Survival Guide", 127)
effect, _ = Effect.objects.get_or_create(name="Deceive the Eyes", life=2)
effect.description = "A member of the Hem-Ka Sobk can hide their scars and tattoos by rubbing ash into a cut in their arms and blowing dust into the faces of a person allows them to disguise something they don't want discovered."
effect.save()
effect.add_source("Book of Crafts", 57)
effect, _ = Effect.objects.get_or_create(
    name="Jivitamarana (Death in Life)[0] Yoga", life=4, entropy=4
)
effect.description = "This effect creates a state of living near-death for the mage. For the duration, the mage can soak lethal damage, halves all bashing damage (before soaking), and ignores wound penalties. Life effects targeting the mage are at +1 difficulty as well. However, the mage automatically fails any touch-based Perception tests and gains an additional Entropic Synergy trait for the duration."
effect.save()
effect.add_source("Tradition Book: Euthanatos (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="Love Me, Love Me", life=3, mind=2)
effect.description = "The mage changes their (or another's) physical form to be more appealing to the target in subtle ways, making them more likely to fall in love with them."
effect.save()
effect.add_source("Dead Magic 2", 81)
effect, _ = Effect.objects.get_or_create(name="Persona", life=2, mind=2)
effect.description = "The Agent changes their appearance sufficiently to be unrecognizable. Mind 2 is used to aid in the disguise by preventing people from wanting to look more closely. Life 2 is all that is needed for a new appearance, but Life 4 is needed to mimic another specific person convincingly."
effect.save()
effect.add_source("Technocracy: New World Order", 49)
effect, _ = Effect.objects.get_or_create(name="Rouge", life=2)
effect.description = "With careful application of cosmetics, the mage can decrease difficulties on Appearance based rolls for a scene by the number of successes. Another option is to use successes to create an effective Arcane for the user, rendering their features so plain as to be unremarkable. A third option is to create more memorable features: one success can create a flaw or feature that is memorable, three will cause viewers to recall incorrect hair color and other features and five or more successes will give an appearance completely unlike the mage's actual one."
effect.save()
effect.add_source("Order of Reason", 73)
effect, _ = Effect.objects.get_or_create(
    name="Uther's Butchered Visage", life=3, mind=1
)
effect.description = "By cutting away their own flesh, the mage can transform into a perfect physical duplicate of anyone whose Pattern they have had the opportunity to examine."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 224)
effect, _ = Effect.objects.get_or_create(name="Agrivelopment", matter=3, life=3)
effect.description = "With this Procedure, Progenitor Agronomists can grow plants as much in a day as they normally would in a month. This also restores topsoil and fertilizes it. Though this can turn a patch of desert into farmland, the seeds need to be provided and the plants must be protected from hostile weather."
effect.save()
effect.add_source("Convention Book: Progenitors (Revised)", 73)
effect, _ = Effect.objects.get_or_create(name="Alter Simple Creature", life=2)
effect.description = "This allows the mage to heal or harm simple creatures or to modify their basic properties in non-extreme ways, up to the judgment of the Storyteller."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 170)
effect, _ = Effect.objects.get_or_create(name="Alter Small Sequence", life=2)
effect.description = "The Progenitor can make a single point mutation to a genetic code. Some things that can be done with this include correcting a genetic error in a developing fetus, there is a point mutation that causes a person to only need 4 hours of sleep to be fully rested, cause cancer."
effect.save()
effect.add_source("Technocracy: Progenitors", 43)
effect, _ = Effect.objects.get_or_create(
    name="Attach Biomechanism", matter=5, life=3, prime=3
)
effect.description = "Once a biomechanism has been made through Craft Biomechanism, it must be attached to the user. The Life Pattern of the person and the Matter Pattern of the mechanism must be carefully joined together through surgery."
effect.save()
effect.add_source("Technocracy: Iteration X", 50)
effect, _ = Effect.objects.get_or_create(name="Augment Simple Lifeform", life=2)
effect.description = "This FACADE Engineer Procedure is used to alter simple lifeforms. It can increase size, for instance, creating gigantic killer bees or spiders."
effect.save()
effect.add_source("Technocracy: Progenitors", 41)
effect, _ = Effect.objects.get_or_create(name="Brittle Bones", life=4, entropy=4)
effect.description = "The targets bones are rendered brittle and weak, reducing their soak dice by one per success."
effect.save()
effect.add_source("World of Darkness: Outcasts", 90)
effect, _ = Effect.objects.get_or_create(name="Genetic Pattern Matching", life=4)
effect.description = "The Genegineer can split code from one life form into another, making limited hybrids. They could give a human eyes like a cat's for night vision, sonar like a dolphin, or glands that secrete particular smells. The more complex the addition, the more difficult the Effect."
effect.save()
effect.add_source("Technocracy: Progenitors", 43)
effect, _ = Effect.objects.get_or_create(
    name="Graft Alien Bio-Matter Between Aliens", life=3
)
effect.description = "FACADE Engineers at this level can graft parts between animals of different species. The Progenitor takes a characteristic from one species and gives it to another. Examples include snake fangs for a guard dog, a scorpion tail for a cat, or the coloring of one snake for another."
effect.save()
effect.add_source("Technocracy: Progenitors", 41)
effect, _ = Effect.objects.get_or_create(
    name="Graft Alien Bio-Matter to Humans", life=4
)
effect.description = "Similar to Graft Alien Bio-Matter Between Animals, this Procedure grafts animal characteristics onto humans. This includes limbs and organs, additional human parts or genetically alien matter. Examples include adding additional fingers or limbs, claws, feathers, or additional organs. This Procedure can be very vulgar."
effect.save()
effect.add_source("Technocracy: Progenitors", 41)
effect, _ = Effect.objects.get_or_create(name="Green Thumb", life=2)
effect.description = "The mage can help their plants grow, altering its properties: smell, color, size. They could create a rose with an extremely powerful scent."
effect.save()
effect.add_source("Book of Crafts", 88)
effect, _ = Effect.objects.get_or_create(
    name="Higher Lifeform Grafting and Recombination", life=4
)
effect.description = "The Progenitor may make large scale alterations to humans and higher lifeforms (gorillas, wolves, etc.). This includes adding or subtracting limbs, adding or removing organs (like the appendix), or adding animal traits to humans. The Progenitor could give themselves claws, fangs, or functional wings."
effect.save()
effect.add_source("Technocracy: Progenitors", 40)
effect, _ = Effect.objects.get_or_create(
    name="Limited Grafting and Recombination", life=3
)
effect.description = "The Progenitor can now manipulate their own body, performing Pattern alterations. This includes altering the muscles in their leg for a jump, change the structure of their ears to hear better, change skin pigment, alter finger prints, etc. These are generally small changes, though they can have major effects on the body's function."
effect.save()
effect.add_source("Technocracy: Progenitors", 40)
effect, _ = Effect.objects.get_or_create(name="Lower Lifeform Manipulation", life=2)
effect.description = "The Progenitor can alter simple animals and plants through genetic manipulation. Resistance to disease, increased growth rates and alterations of color are all possible."
effect.save()
effect.add_source("Technocracy: Progenitors", 40)
effect, _ = Effect.objects.get_or_create(
    name="Major Environmental Alteration", matter=3
)
effect.description = "Similar to Minor Environmental Alteration, but the Engineer can now take on larger challenges. They may alter a single asteroid's trajectory to mine it for materials. They may alter the course of a planet's rotation, but only by a factor of degrees. Of course, even degrees may have major effects on the planet's ecosystem."
effect.save()
effect.add_source("Technocracy: Void Engineers", 44)
effect, _ = Effect.objects.get_or_create(
    name="Minor Environmental Alteration", matter=2
)
effect.description = "The Void Engineer at this point can make simple changes to various environments. This includes such tasks as changing the color of soil from one shade to another, making minor changes in the geography of an area (adding or subtracting mass), or altering the composition of certain types of rock. This power is limited to fairly small areas, such as rooms or small asteroids."
effect.save()
effect.add_source("Technocracy: Void Engineers", 44)
effect, _ = Effect.objects.get_or_create(
    name="Mokupuni Palahalaha Wiki", time=3, life=2, prime=3
)
effect.description = "Polynesian mages often want their own islands and reefs away from prying eyes. This rote, whose name translates to Coral Island Bloom, fast-forwards the growth cycle of coral, allowing them to grow entire reefs in days, rather than centuries."
effect.save()
effect.add_source("Dead Magic 2", 29)
effect, _ = Effect.objects.get_or_create(name="Mold Tree", life=2)
effect.description = "Mages, mostly Verbena, use this rote to rework the Patterns of trees, including bending its branches and trunk into new shapes."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 199)
effect.add_source("Mage: The Ascension (Second Edition)", 202)
effect, _ = Effect.objects.get_or_create(
    name="Personal Compression", correspondence=5, life=3
)
effect.description = "By warping space in dramatic ways, the mage is capable to shrinking, and dramatically so. Each success allows the mage to decrease their size and mass by up to 15%, and seven successes allows them to take any size that they want. With Matter, they can bring possessions along with them."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 220)
effect, _ = Effect.objects.get_or_create(
    name="Phosphoric Marker", correspondence=1, life=3, forces=3
)
effect.description = "Also called 'Greek Life-Fire', this causes every living thing in the area to glow like a firefly. The mage can omit any specific beings that they want, often making it easier for them and their allies to hide during a firefight."
effect.save()
effect.add_source("Hidden Lore", 17)
effect, _ = Effect.objects.get_or_create(name="Clone", life=5)
effect.description = "The FACADE Engineer can replicate a human or animal given a tissue sample. No alterations to the original that were not genetic are carried over, and this Procedure is often used to grow new bodies for agents operating in high-risk areas."
effect.save()
effect.add_source("Technocracy: Progenitors", 41)
effect, _ = Effect.objects.get_or_create(name="Cloning", life=5)
effect.description = "The Progenitor can create a full human body, duplicating a body from a tissue sample. This is just an empty body unless other Technology is used."
effect.save()
effect.add_source("Technocracy: Progenitors", 40)
effect, _ = Effect.objects.get_or_create(
    name="Courtesan's Draught/Blessed Heir", life=2
)
effect.description = "Life 2 for self, 3 for others, this rote allows the user to control the target's fertility, either increasing or decreasing it. Correspondence can be added to target at a distance."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 90)
effect, _ = Effect.objects.get_or_create(
    name="Fatherless Birth", spirit=5, life=5, entropy=5, prime=5
)
effect.description = "One of the most difficult rotes, but capable of creating a future great hero, Fatherless Births actually have a spirit for a father, in general. The target must never have conceived a child nor have a chance to otherwise become pregnant. The mage summons the spirit to be the father, uses Life and Prime to create the seed of the magical child that the woman must consume. Entropy both guarantees that the seed leads to pregnancy and that the child will have a great destiny."
effect.save()
effect.add_source("Dead Magic 2", 118)
effect, _ = Effect.objects.get_or_create(name="Flesh Toys", life=3, prime=2)
effect.description = "The mage creates life, with simple life at Life 3 and more complex requiring Life 5. The amount and complexity of the creatures determines the number of successes, with the number doubled for creating something fundamentally new."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 224)
effect, _ = Effect.objects.get_or_create(
    name="The Foundling", correspondence=2, spirit=4, matter=2, life=5, mind=3
)
effect.description = "Used by a Master who knows that they are about to die, this ties the mage's avatar to their most prized possession as a phylactery, teleports it somewhere on Earth to a couple that is desperate for a child, and creates the body of a newborn to hold their spirit. The couple are influenced to hold the phylactery and keep it safe for the child until it is older, and when the child is ready to make their way into the world, the Memento Mori effect triggers, prompting Awakening and returning the mage's memories of their previous life."
effect.save()
effect.add_source("Mage Storyteller's Companion", 63)
effect, _ = Effect.objects.get_or_create(name="Genetic Mastery", life=5)
effect.description = "With complete mastery of genetics, a Genegineer at this level can create virtually any creature that they can imagine, with enough successes."
effect.save()
effect.add_source("Technocracy: Progenitors", 43)
effect, _ = Effect.objects.get_or_create(
    name="Oak of Sanguine Root", correspondence=2, matter=3, life=3, prime=2
)
effect.description = "This Hermetic rote causes an oak tree to sprout and quickly grow inside a Vampire's body. It feeds on the undead corpse and the power of its blood, dealing standard Life effect damage to the Vampire as well as piercing its heart with a wooden stake. Finally, removing the tree, which is almost certain to die quickly, will likely also cause damage to the Vampire, as it is intertwined among the Vampire's organs and bones."
effect.save()
effect.add_source("Blood Treachery", 89)
effect, _ = Effect.objects.get_or_create(name="Spontaneous Generation", life=3, prime=2)
effect.description = "Greek philosophy permitted the creation of life or matter from nothing. Of course, only certain things cause the spontaneous generation of other things, such as maggots coming from old meat. This allows the mage, supported by some theory of spontaneous generation, to create something from nothing."
effect.save()
effect.add_source("Dead Magic", 108)
effect, _ = Effect.objects.get_or_create(
    name="Supporting the Brain", matter=2, life=4, mind=2, prime=2
)
effect.description = "Using Pattern spheres to handle the physical issues and Mind to handle the mental ones, this rote allows an Etherite to keep a brain alive outside of its body, whether just in a jar or in a new, better body. A robot body."
effect.save()
effect.add_source("Book of Shadows", 143)
effect, _ = Effect.objects.get_or_create(name="Thorn Wall", time=3, life=2, prime=2)
effect.description = "A traditional Verbena rote that is vulgar almost everywhere on Earth, the Verbena clasps a thorn branch as a wand, and lets their blood fall on the ground. Where it falls, dense thorn bushes spring up in a shape dictated by the mage."
effect.save()
effect.add_source("Hidden Lore", 18)
effect, _ = Effect.objects.get_or_create(name="Animal Form", life=5)
effect.description = "This rote allows the mage to transform a target into an animal. Conversely, animals can be turned into humans with this level of control. This does run the risk of the target losing themselves in their new form, their mind reverting to the sort that belongs in their new form."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 201)
effect.add_source("Mage: The Ascension (Second Edition)", 203)
effect.add_source("Mage: The Ascension (Revised)", 171)
effect, _ = Effect.objects.get_or_create(name="Animal Shift", life=4)
effect.description = "This Babylonian rote allows a mage to shift into an animal form."
effect.save()
effect.add_source("Dead Magic", 50)
effect, _ = Effect.objects.get_or_create(name="Avatar Form", life=4, mind=2, prime=2)
effect.description = "The Akashic attempts to mirror Vibansumitra's manifestation of his Avatar in the physical realm. It hardens the skin to extreme temperatures (and optionally like armor, at a cost of speed), the mage grows four additional arms and may add four dice to any manual task's dice pool, though difficulties may increase due to the need to focus when coordinating six arms. Mind is used to project an overwhelming feeling of awe into all who see the Avatar Form."
effect.save()
effect.add_source("Book of Shadows", 138)
effect, _ = Effect.objects.get_or_create(name="Circe's Enchantment", life=5)
effect.description = "This rote allows a Verbena to transform a human into an animal. Five successes are required to transform the target fully (fewer may result in a partial transformation), with other successes put into targets and duration."
effect.save()
effect.add_source("Tradition Book: Verbena (Revised)", 66)
effect, _ = Effect.objects.get_or_create(
    name="Deity Form", spirit=2, life=4, forces=3, prime=4
)
effect.description = "This rote allows the mage to become an Avatar of a god, though at the cost of paradox as it is always vulgar. The mage gains the benefits of Friction Curse, Telekinesis and Better Body, they take on the aspect of the deity via Mutate Form and use Wellspring to replenish power. Spirit calls to the deity who permits this transformation. Optionally, Entropy 5 can be added to renew the deity's worship, reinvigorating the idea of the deity in those who see its avatar."
effect.save()
effect.add_source("Dead Magic 2", 80)
effect, _ = Effect.objects.get_or_create(name="Dionysus's Gift", life=4)
effect.description = "Dionysus was a shapechanger, and many Cultists look to him to gain the ability. This allows them to change shape (with Life 5 without the risk of losing themselves), or to change the shapes of others. With Matter or Forces, they can even turn their targets into inanimate objects and energy."
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (First Edition)", 66)
effect, _ = Effect.objects.get_or_create(name="Eagle Form", spirit=2, mind=4)
effect.description = "The mage shapechanges their Astral Form to an Eagle, giving them the ability to move more easily through the Umbra and the Gauntlets between Umbral Realms."
effect.save()
effect.add_source("Dead Magic 2", 128)
effect, _ = Effect.objects.get_or_create(name="Holy Union", spirit=4, mind=3, prime=3)
effect.description = "The Holy Union ritual summons a psychopomp spirit from the deep Umbra and binds a part of its essence to the mage's avatar, granting several of the psychopomp's powers to the mage, specifically related to guiding souls and manipulating avatars. The version that can manipulate the avatars of the living requires Life 5. This is the ritual used by Heylel to become rebis, which is still the term for those who go through this ritual."
effect.save()
effect.add_source("Ascension", 197)
effect, _ = Effect.objects.get_or_create(
    name="Iron Avatar", matter=3, life=3, mind=2, prime=2
)
effect.description = "This rote merges the visages of Kali and Shiva to turn the caster into a four-armed killer. The user of the rote becomes 10 feet tall; their skin turns the color of wrought iron, and their four hands end in talons, each holding a menacing weapon. Usually, these weapons are swords, though variants with other weapons exist."
effect.save()
effect.add_source("Tradition Book: Euthanatos (First Edition)", 67)
effect.add_source("Tradition Book: Euthanatos (Revised)", 60)
effect, _ = Effect.objects.get_or_create(
    name="Jaguar Cloak", spirit=2, matter=3, life=5, prime=3
)
effect.description = "This effect enchants a jaguar skin and attunes it to a specific wearer. When worn, the user can transform into a jaguar. With particularly strong will, the warrior can manage partial transformation. Life transforms, Matter binds the skin to the wearer, and Prime and Spirit recharge the enchantment as the wearer kills their enemies in combat."
effect.save()
effect.add_source("Dead Magic", 78)
effect, _ = Effect.objects.get_or_create(name="LERMUization", spirit=5, life=5)
effect.description = "The Living Entity Reality Modulator Unit (LERMU) protects people from the Deep Universe, including Void Adaptation, vacuum and cosmic radiation. A LERMU no longer needs to eat or breathe, absorbing energy from ambient radiation. A LERMU can use their feet as easily as their hands and can see a longer distance in a much larger part of the light spectrum. LERMUization requires five successes before duration and causes three points of permanent paradox."
effect.save()
effect.add_source("Convention Book: Void Engineers (Revised)", 87)
effect, _ = Effect.objects.get_or_create(name="Lesser Shapechanging", life=4)
effect.description = "This allows the mage to shapeshift into any animal of roughly similar mass to the mage. This doesn't give the mage any experience or talent for using the animal's features, and they will need to practice things like flying as a bird or catlike balance."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 203)
effect, _ = Effect.objects.get_or_create(name="Mutate Form", life=4)
effect.description = "Before, the mage could alter their own Pattern or simple Patterns, with Mutate Form, the mage can make alterations as large of those of Better Body to any living creature. This also allows the mage to transform themselves into an animal. However, this comes with the risk of losing themselves to the new form."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 200)
effect.add_source("Mage: The Ascension (Second Edition)", 203)
effect.add_source("Mage: The Ascension (Revised)", 171)
effect, _ = Effect.objects.get_or_create(
    name="The Notorious Vampiric Lawnchair", matter=5, life=5
)
effect.description = "Often conjectured, rarely performed, this exceptionally difficult effect transforms a Vampire into some inanimate object. To succeed, this requires a massive number of successes, and even if successful, there are numerous ways for it to go badly for the mage."
effect.save()
effect.add_source("Mage: The Ascension (20th Anniversary Edition)", 610)
effect, _ = Effect.objects.get_or_create(name="One with Beasts", life=4)
effect.description = "Powerful mages of the Bata'a can shapeshift, taking the forms of animals. With Life 4, it is equivalent to Lesser Shapechanging, Life 5 is Perfect Metamorphosis. Spirit 4 is a much riskier formulation, where the mage invites a spirit to change their form and ride along. This carries many risks, including the spirit will leave without returning them to their original form."
effect.save()
effect.add_source("Book of Crafts", 26)
effect, _ = Effect.objects.get_or_create(name="Perfect Metamorphosis", life=5)
effect.description = "The mage is now able to transform into an animal without risk of losing their mind. Additionally, size is no longer an issue, and the mage can become any creature that they desire."
effect.save()
effect.add_source("Mage: The Ascension (Second Edition)", 203)
effect.add_source("Mage: The Ascension (Revised)", 171)
effect, _ = Effect.objects.get_or_create(name="Qayaq's Fish", matter=3, life=3)
effect.description = "By carving an animal out of pieces of wood and putting them together, an Inuit mage can evoke the hero Qayaq and change the animal from wood to the real thing. Successes go to duration and how large an animal can be managed."
effect.save()
effect.add_source("Dead Magic", 131)
effect, _ = Effect.objects.get_or_create(name="Rokea'ole", spirit=3, life=3)
effect.description = "While true sharks are considered good luck by Polynesian mages, the Rokea are considered semi-divine pains in the ass. They often end up in conflict, and this rote allows the mage to force the Rokea into its breed form for ten minutes per success."
effect.save()
effect.add_source("Dead Magic 2", 29)
effect, _ = Effect.objects.get_or_create(name="Shapechange Curse", life=5, mind=4)
effect.description = "Similar to Animal Form, it also suppresses the target's mind, giving them the mind of an animal for the duration."
effect.save()
effect.add_source("Dead Magic 2", 120)
effect, _ = Effect.objects.get_or_create(name="Shapeshifter Prison", life=4)
effect.description = "Through a combination of the right elements, mostly silver, this effect allows the creation of a prison that prevents shape-shifts from changing shape. Three successes are required to start the effect, and shapeshifting requires a Stamina + Primal Urge roll with more successes than the remainder for a natural shapeshifter, or on an Arete roll from a mage. With Prime, the effect deals damage to any shapeshifter that touches them based on the number of successes more than three rolled at creation."
effect.save()
effect.add_source("Order of Reason", 109)
effect, _ = Effect.objects.get_or_create(name="Shapeshifting", life=5)
effect.description = "The Progenitor can manipulate their body fully, changing their shape into any living thing they desire."
effect.save()
effect.add_source("Technocracy: Progenitors", 40)
effect, _ = Effect.objects.get_or_create(
    name="Storm of Crows", correspondence=3, life=5, mind=1, prime=2
)
effect.description = "When cornered, powerful Infernalists have been known to be able to transform into a flock of crows, a swarm of rats or another collection of smaller animals, including insects. This effect allows them to do that, splitting their consciousness among all the creatures. Should one of them be caught, it can be disintegrated by the mage, though a quick opponent may be able to use it as a correspondence link to the whole of the Infernalist. This requires some piece of the animal to be transformed into."
effect.save()
effect.add_source("Infernalism: The Path of Screams", 89)
effect, _ = Effect.objects.get_or_create(
    name="Vulcan's Hammer", matter=3, life=4, forces=3
)
effect.description = "It is important for a Hermetic mage to be capable of subtlety. Sometimes, however, a Hermetic needs to be the most blatant person on the planet. The mage sculpts a statuette of themselves out of iron-rich clay, inscribing their True Name onto it ten times, kneading it into the clay before firing it. With this clay statuette, the mage can assume the shape of Vulcan's Hammer, a grossly vulgar war form made from iron. In this form, the mage gets +3 Strength, -2 Dexterity (minimum 1), 4 Stamina, fails all Social Attribute rolls automatically (other than intimidation), and anyone who comes into physical contact with the mage takes standard Forces damage from this effect. With Prime 2, the mage deals aggravated damage with hand-to-hand attacks."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="Wasp-Spasm", life=4, forces=3, prime=3)
effect.description = "The mage's very body warps to make them into a fury-filled warrior. They get an extra dot in all Physical Attributes for every two successes and two extra dice of damage in melee due to emitting extreme heat. If the mage maintains this form for longer than a scene, they must spend a point of Willpower for each extra duration or else become a mindless berserker."
effect.save()
effect.add_source("Dead Magic 2", 120)
effect, _ = Effect.objects.get_or_create(name="The Weeping Willow", life=5)
effect.description = "This allows a Sister of Hippolyta to transform a woman, often one who has run out of options, into a tree, where any tormentor cannot cause her further pain. Rarely, it has been used on devoted lovers who suffer due to the mage's comings and goings."
effect.save()
effect.add_source("Book of Crafts", 89)
effect, _ = Effect.objects.get_or_create(name="Wolf Form", life=4, mind=2)
effect.description = "As the Mutate Form effect, the mage transforms into a wolf. Thanks to the Mind sphere, the mage maintains their human consciousness."
effect.save()
effect.add_source("Dead Magic 2", 129)
effect, _ = Effect.objects.get_or_create(name="Adaptation", life=2)
effect.description = "The Ahl-i-Batin have learned how to function in extreme environments. This allows them to ignore natural difficulties, such as the heat and dryness of a desert, and even to breathe underwater, though that requires the Life 3 version. With Forces, even stronger than normal desert heat or cold, or deep-water pressure, can be withstood."
effect.save()
effect.add_source("Technocracy: Void Engineers", 44)
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 40)
effect, _ = Effect.objects.get_or_create(name="Adrenal Rush", life=3, prime=2)
effect.description = "By playing an intense video game, a Virtual Adept can get a rush of adrenaline and make other slight changes to their system, refreshing them and giving them a boost of energy. This can help fight off poisons and viruses, gain dots of Stamina, Strength or Alertness, and of course, skip the need for sleep."
effect.save()
effect.add_source("Book of Shadows", 143)
effect, _ = Effect.objects.get_or_create(name="Advanced Therapies", life=3)
effect.description = "This Procedure produces the same effects as Better Body (increased physical attributes and appearance in particular) but requires long-term planning and is restricted to what is possible naturally for humans to accomplish or have. Over at least four weeks, the Syndicate agent pursues a regimen of two hours of exercise, drug therapy and minor surgery every day, and at the end of this period they can spend successes on Attributes and duration, though permanency is impossible without spending Experience Points."
effect.save()
effect.add_source("Convention Book: Syndicate (Revised)", 72)
effect, _ = Effect.objects.get_or_create(name="Battery Man", life=4, forces=2)
effect.description = "This rote allows the Etherite to store electricity in their body for later use, including powering objects, dramatic effect, and electrocuting a target (for damage based on number of successes on this rote in the first place). If this energy is not discharged within an hour, however, the Etherite takes one health level of damage per success."
effect.save()
effect.add_source("Tradition Book: Sons of Ether (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(name="Better Body", life=3)
effect.description = "Better Body allows the mage to make significant alterations to themselves, including increasing physical attributes, appearance, growing claws or gills, natural armor, etc."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 199)
effect.add_source("Mage: The Ascension (Second Edition)", 202)
effect.add_source("Mage: The Ascension (Revised)", 171)
effect.add_source("Technocracy: Progenitors", 43)
effect.add_source("Book of the Fallen", 155)
effect, _ = Effect.objects.get_or_create(name="Biochemical Regulation", life=3)
effect.description = "The Progenitor can alter the biochemistry of the body. Among other things, the Progenitor can now speed healing, enhance Physical Attributes, increase the time someone can hold their breath, deoxygenate blood, inhibit clotting, or cause general cellular degeneration."
effect.save()
effect.add_source("Technocracy: Progenitors", 44)
effect, _ = Effect.objects.get_or_create(name="Bio-Luminescence", life=3, forces=3)
effect.description = "With this rote, an Etherite can make themselves glow in the dark. Each success causes them to glow brighter and in a larger area. It may be concentrated onto certain parts of the body."
effect.save()
effect.add_source("Tradition Book: Sons of Ether (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(name="Brain Boost", mind=1)
effect.description = "This is the Mental equivalent of Better Body, allowing the increase of Mental Attributes."
effect.save()
effect.add_source("Digital Web 2.0", 114)
effect, _ = Effect.objects.get_or_create(name="Chakra Influence", life=3)
effect.description = "In Traditional Tantric practice, there are seven chakras located in the body. Each of them can be affected by one or more of Life, Mind and Prime. This rote allows the mage to control both their own chakras and those of others."
effect.save()
effect.add_source("Dead Magic 2", 80)
effect, _ = Effect.objects.get_or_create(name="Crocodile Blood", matter=2, life=4)
effect.description = "This procedure alters the Technocrat's blood chemistry to allow them to hold their breath for an hour per success when calm and still or a minute per success during intense action."
effect.save()
effect.add_source("Hidden Lore", 53)
effect, _ = Effect.objects.get_or_create(name="Go Ti Ta", spirit=4, life=4)
effect.description = "The Wu-Keng have very few combat-oriented rotes. This is one of them. It derives from a fertility ritual where combatants spar with deer antlers. By inscribing a deer on an oracle of bone, then casting it into a fire, the mage gains the benefits of Better Body along with access to one spirit's gifts. Though usually the mage will only wear horned headgear, sometimes they will in fact grow horns from this rote."
effect.save()
effect.add_source("Dragons of the East", 68)
effect, _ = Effect.objects.get_or_create(name="Mele Lapa'au", life=2)
effect.description = "This rote was developed by the wayfinders of the Kopa Loei so that they could adapt for the elements or make other changes to themselves. They do so by invoking different gods for different effects: Komo-ho'ali'I, Kane or Kanaloa for breathing water; Pele for withstanding fire; Kane or Lono for withstanding cold; Kane for healing injuries; Maui for changing appearance; Hina for increasing potency/fertility; Ku for toughening skin. Life 2 suffices for healing and potency, 3 for the rest, and one more is needed to pass the effect to someone else."
effect.save()
effect.add_source("Book of Crafts", 73)
effect, _ = Effect.objects.get_or_create(name="Multi-Tasking", mind=1)
effect.description = "This allows the mage to do multiple things at a time without having to split their attention. Only mundane tasks can be done, and they cannot conflict (so programming and talking on the phone are fine but listening to multiple songs simultaneously is not). This does not permit more than one magickal effect to be used, nor more than one Willpower point to be spent."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 205)
effect.add_source("Mage: The Ascension (Second Edition)", 209)
effect, _ = Effect.objects.get_or_create(
    name="Nanotech Integration", matter=2, life=4, prime=5
)
effect.description = "This Procedure, from collaboration with Iteration X, injects nanotech into the subject to make them more resilient. The recipient gains three dots of Stamina and regenerates a health level every turn. They also have immunity to mundane drugs, diseases and poisons, whether they like it or not. Only a Master of Life, Entropy or Matter can destroy the nanobots without otherwise harming the recipient."
effect.save()
effect.add_source("Technocracy: Progenitors", 45)
effect.add_source("Convention Book: Progenitors (Revised)", 74)
effect, _ = Effect.objects.get_or_create(
    name="Our Enemies are Delicious", spirit=3, life=3
)
effect.description = "If a mage sacrifices a person, they can ensure that anyone who eats the flesh will have their Physical Attributes increased by one and their Social Attributes decreased by one for the duration of the effect. Each day after, one Physical dot gained is lost and one social dot is regained."
effect.save()
effect.add_source("Dead Magic", 76)
effect, _ = Effect.objects.get_or_create(name="Positronic Brain", mind=1)
effect.description = (
    "Each success adds one dot to any Mental Attribute for the duration."
)
effect.save()
effect.add_source("Technocracy: Iteration X", 48)
effect, _ = Effect.objects.get_or_create(name="Simple Biochemical Manipulation", life=2)
effect.description = "The Pharmacopeist can manipulate a substance's effects on a Pattern, for instance making medication work faster or slower, and increasing or decreasing its effectiveness."
effect.save()
effect.add_source("Technocracy: Progenitors", 43)
effect, _ = Effect.objects.get_or_create(name="Strength of the Earth", life=3)
effect.description = "By drawing on the Earth itself as a source, the Verbena can increase their Strength, one dot per success, so long as the Verbena is in contact with the ground."
effect.save()
effect.add_source("Tradition Book: Verbena (Revised)", 68)
effect, _ = Effect.objects.get_or_create(name="Survivor's Charm", life=2)
effect.description = "This rote hardens the user against the elements, making is easy to survive in extreme environments and gaining a resistance to freezing cold, the intense heat and to minor burns. With Life 3, this protection can be given to others."
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 271)
effect, _ = Effect.objects.get_or_create(name="Talons", life=3)
effect.description = "This rote causes the mage to grow claws that are as sharp as steel. They do Strength + 2 aggravated damage, and last for two turns per success. Each successful strike costs one Quintessence."
effect.save()
effect.add_source("Book of Shadows", 146)
effect.add_source("Mage: The Ascension (20th Anniversary Edition)", 609)
effect, _ = Effect.objects.get_or_create(name="Thick Skin", life=2)
effect.description = "The basic version protects the mage from extreme environments, while the stronger version hardens the mage and allows them to soak Aggravated damage."
effect.save()
effect.add_source("Orphan's Survival Guide", 126)
effect, _ = Effect.objects.get_or_create(name="Titan's Power", life=3)
effect.description = "Allows the mage to temporarily gain dots in Strength, Dexterity, Stamina and/or Appearance."
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 273)
effect, _ = Effect.objects.get_or_create(name="Tumo", life=2)
effect.description = "This allows Akashics to endure extremes of heat and cold. With Life alone, heat well outside of the comfort zone of most humans is no issue. With Forces added in, even heat and cold that would hurt a normal person (such as the center of a bonfire or the Antarctic) is comfortable: each success reduces the damage by two levels."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 70)
effect, _ = Effect.objects.get_or_create(name="Apathy", entropy=3, mind=2)
effect.description = "This rote causes the target to become depressed, suddenly lacking energy and unable to focus."
effect.save()
effect.add_source("World of Darkness: Outcasts", 91)
effect, _ = Effect.objects.get_or_create(name="Olive Branch", mind=2)
effect.description = "This rote allows the user to act as a calmer head and try to prevent a fight from breaking out."
effect.save()
effect.add_source("Order of Reason", 79)
effect, _ = Effect.objects.get_or_create(
    name="Pass Calmly", correspondence=2, life=1, mind=2
)
effect.description = "Although of no use in combat, many Akashics find this rote useful to calm all Sleepers sufficiently close to them, within about two yards per success."
effect.save()
effect.add_source("Hidden Lore", 13)
effect, _ = Effect.objects.get_or_create(name="Peace of Buddha", mind=2)
effect.description = "The Akashic can force a feeling of peace into their target's mind. The number of successes must match or exceed the opponent's Willpower, and if so, the target will lose their will to do harm (to anyone) for the duration."
effect.save()
effect.add_source("Book of Shadows", 138)
effect, _ = Effect.objects.get_or_create(name="Peace Rune", mind=2)
effect.description = "The user of this rune calms hearts and minds, directly or by destroying the concept of conflict in the minds of those involved."
effect.save()
effect.add_source("Dead Magic 2", 99)
effect, _ = Effect.objects.get_or_create(name="Rat's Rage/Lost Cousin", life=2, mind=2)
effect.description = "This rote allows the mage to enforce a strong detachment, viewing the world dispassionately and even themselves as an observer. If they stay motionless, the Mind even becomes like a stone and Torture becomes useless. With at least three successes, the mage may act deliberately, devoid of emotion or empathy. For the duration, the mage may not spend Willpower points and all rolls to dodge attacks and all social rolls have +3 difficulty."
effect.save()
effect.add_source("Guide to the Technocracy", 214)
effect, _ = Effect.objects.get_or_create(name="Stoicism", matter=1, mind=1)
effect.description = "The mage uses Greek philosophical principles to maintain emotional detachment, viewing themselves as unchanging like stone while observing the world with dispassion."
effect.save()
effect.add_source("Dead Magic", 108)
effect, _ = Effect.objects.get_or_create(
    name='Abh-t-ab, "Biting the Heart"', correspondence=2, mind=2
)
effect.description = "The Hem-Ka Sobk causes the subject to experience an acute fear response, usually resulting in them fleeing or freezing."
effect.save()
effect.add_source("Book of Crafts", 57)
effect, _ = Effect.objects.get_or_create(name="The Argument of Princes", mind=2)
effect.description = "Identical to Show of Force, but requires a weapon be used with intent to terrify and intimidate."
effect.save()
effect.add_source("Artisan's Handbook", 50)
effect, _ = Effect.objects.get_or_create(name="Capiche?", mind=2)
effect.description = "This rote gives a difficulty bonus to attempts to intimidate people when mimicking the affectations of mobsters."
effect.save()
effect.add_source("Fallen Tower: Las Vegas", 119)
effect, _ = Effect.objects.get_or_create(name="Hoodoo Man's Heartbeat", mind=2)
effect.description = "This rote allows a Bata'a to intimidate a target. With Mind, it acts as Subliminal Impulse, twisting the victim's perceptions making things seem more sinister. With Spirit, it calls upon a spirit of torment, though this is less reliable."
effect.save()
effect.add_source("Book of Crafts", 25)
effect, _ = Effect.objects.get_or_create(name="Primal Dread", mind=2)
effect.description = "The mage instills fear in a target, enhancing whatever fear might already be there. If none is present, Prime 2 is needed to create it from quintessence."
effect.save()
effect.add_source("Tradition Book: Celestial Chorus (Revised)", 57)
effect, _ = Effect.objects.get_or_create(name="Show of Force", mind=2)
effect.description = "This rote allows the user to attempt to cow the target into submission through intimidation."
effect.save()
effect.add_source("Order of Reason", 79)
effect, _ = Effect.objects.get_or_create(name="Bewitchment", mind=2)
effect.description = "Using speech, manners, costume, cosmetics and human nature, the mage enchants their target, seducing them. For long-term effects, this requires Mind 3, Entropy can be used to help wear down defenses and Life can be used to prompt bursts of animal passion."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 90)
effect, _ = Effect.objects.get_or_create(name="Charm Rune", mind=2)
effect.description = "This rune gives the mage an aura of friendliness and charm, causing others to think well of them and making most Social rolls that are non-confrontational to become easier."
effect.save()
effect.add_source("Dead Magic 2", 101)
effect, _ = Effect.objects.get_or_create(name="Exalted Desire", life=4, mind=2, prime=2)
effect.description = "This effect causes the target to experience an unusual high from something pleasurable. The Nephandus can use this to create an addiction, weakening the target and making them easier to manipulate later."
effect.save()
effect.add_source("Hidden Lore", 50)
effect, _ = Effect.objects.get_or_create(
    name="Kuoha (The Passion Prayer)", correspondence=3, life=2, mind=2
)
effect.description = "By wearing only fragrant floral leis and beating out a primal rhythm on a drum, a Polynesian mage can incite passion in a person of their choosing."
effect.save()
effect.add_source("Dead Magic 2", 27)
effect, _ = Effect.objects.get_or_create(name="Lecherous Kiss", life=2, mind=2, prime=2)
effect.description = "This Hollow One rote is designed for seduction. Mind puts the target into a sexually receptive state of mind, and Life triggers the appropriate parts of the endocrine system, both of which are fueled by Prime."
effect.save()
effect.add_source("Book of Shadows", 142)
effect, _ = Effect.objects.get_or_create(name="Romance", mind=2)
effect.description = "Especially useful for groups like the High Guild and the Ksirafai, this rote makes the mage more attractive and suave to others, decreasing the difficulty of attempts at seduction."
effect.save()
effect.add_source("Order of Reason", 78)
effect, _ = Effect.objects.get_or_create(name="Taliesin's Song", life=3, mind=2)
effect.description = "By altering their vocal cords to make their singing enchanting, a Verbena can influence others with a song. This adds automatic successes to the Verbena's social rolls against a target for the duration."
effect.save()
effect.add_source("Tradition Book: Verbena (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(name="Be Cool", mind=2)
effect.description = "The Hollow Ones devote a lot of time to appearing cool, and this rote is a shortcut. With it, the people around the mage get a general impression of coolness from them."
effect.save()
effect.add_source("Book of Shadows", 141)
effect, _ = Effect.objects.get_or_create(name="Branding", mind=2)
effect.description = "It's become a common shortcut in the mind to associate emotions with brands. The Syndicate agent can tailor their appearance and mannerisms to match a brand, and thus, influence the emotions of the target in an appropriate way."
effect.save()
effect.add_source("Convention Book: Syndicate (Revised)", 72)
effect, _ = Effect.objects.get_or_create(name="Comp Me", entropy=3)
effect.description = "In most casinos, everyone assumes that if you're there, you're gambling. So, to keep people there, the House will comp small things. With this rote, a mage in a casino either aligns with the in-place system (Entropy) or else gives the strong impression of gambling (Mind), allowing the mage to take advantage of the system of comps."
effect.save()
effect.add_source("Fallen Tower: Las Vegas", 119)
effect, _ = Effect.objects.get_or_create(name="Cool Glamour", mind=2)
effect.description = "Hollow Ones often put a lot of work into their appearance. With this rote, when they do so, they get the ability to roll Appearance + Intimidation to come across is cool, self-confident and powerful, making others want to treat them with respect."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 62)
effect, _ = Effect.objects.get_or_create(name="Empathic Projection", mind=2)
effect.description = "The mage can project an emotion into a target, forcing them to feel it with an intensity proportional to how many successes are achieved."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 176)
effect, _ = Effect.objects.get_or_create(name="Gatha", mind=2, prime=2)
effect.description = "An Akashic poet can weave emotion into every character of the work. The writer chooses an emotion to be invoked in anyone who reads or hears the poem."
effect.save()
effect.add_source("Dragons of the East", 51)
effect, _ = Effect.objects.get_or_create(name="The Golden Apple", matter=2, mind=2)
effect.description = "Hermetics use this rote to imbue an object with a near-irresistible pull. The weaker version merely draws attention towards the imbued object, causing those who see it to fixate on it with whatever emotion the Hermetic chooses to create. The stronger version uses the victim's own emotions as fuel, creating a viscous cycle."
effect.save()
effect.add_source("Blood Treachery", 91)
effect, _ = Effect.objects.get_or_create(name="Grand Style", matter=1, mind=2)
effect.description = "Through some form of art, a Cultist can alter moods on a mass scale. Though live music can be used (Forces), physical art (Matter) is much more common. The effect causes those who perceive the art to experience a certain emotion. With Prime 2, it can create the emotion, otherwise it only emphasizes that which is already there."
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (Revised)", 71)
effect, _ = Effect.objects.get_or_create(name="High Rhetoric", mind=2)
effect.description = "This effect allows the user to give a speech and convey an emotion to an audience. Although it can sway an audience, it cannot cause large changes in ideology, and pushing too hard gives the listeners Willpower rolls to resist."
effect.save()
effect.add_source("Artisan's Handbook", 51)
effect, _ = Effect.objects.get_or_create(name="Hope's Birth", mind=2)
effect.description = "The mage can fan the flames of hope so long as there is any present, either in themselves or those around them. With Prime 2, all hope can be lost, and the rote will create it wholly."
effect.save()
effect.add_source("Tradition Book: Celestial Chorus (Revised)", 57)
effect, _ = Effect.objects.get_or_create(name="Incitation", mind=2)
effect.description = (
    "This rote allows the user to taunt a target to try to goad them into a fight."
)
effect.save()
effect.add_source("Order of Reason", 79)
effect, _ = Effect.objects.get_or_create(name="Initiation", mind=3, prime=2)
effect.description = "Initiation rites are used on new members of many organizations, most notable the Order of Reason and the Technocracy. This rite is more effective the more elaborate it is and ties the membership into the target's identity. This allows the user of the ritual to instill one idea or emotional reaction to the target, most often loyalty to the organization and its ideals."
effect.save()
effect.add_source("Order of Reason", 90)
effect, _ = Effect.objects.get_or_create(name="The Look/The Word", mind=2)
effect.description = "Through a well-timed look or saying just the right word, a Syndicate agent can create an impression in the target's mind, ensuring that a message is remembered."
effect.save()
effect.add_source("Technocracy: Syndicate", 46)
effect, _ = Effect.objects.get_or_create(name="Loving Cup", life=3, mind=2)
effect.description = "By sharing a drink with the target, the mage can influence the target's emotional state. Like Ultimate Argument mechanically, this requires not only that a drink be shared, but that it be alcoholic, and only one roll is permitted per drink."
effect.save()
effect.add_source("Order of Reason", 91)
effect, _ = Effect.objects.get_or_create(name="Mood Swing/Communion", mind=2)
effect.description = "Spreads sensations and emotions to one person nearby per success. With Correspondence (the version called Communion), the person doesn't need to be nearby."
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (First Edition)", 65)
effect, _ = Effect.objects.get_or_create(name="Motivational Speaking", mind=2, prime=2)
effect.description = "This Procedure allows a Technocrat to persuade a group of people without a bias about something. With Mind 2, they can evoke an emotion and with 3 a false idea. The total number of successes must be at least twice the average Willpower of the crowd."
effect.save()
effect.add_source("Guide to the Technocracy", 215)
effect, _ = Effect.objects.get_or_create(name="Petals of Love", mind=2)
effect.description = "The Sisters of Hippolyta brew a potion from rose petals that strengthens their emotional ties to each other."
effect.save()
effect.add_source("Book of Crafts", 88)
effect, _ = Effect.objects.get_or_create(name="Physiological Emotion Control", life=4)
effect.description = "An Adept of Life can alter a target's emotional state by manipulating their body chemistry directly."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 200)
effect.add_source("Mage: The Ascension (Second Edition)", 203)
effect.add_source("Mage: The Ascension (Revised)", 171)
effect, _ = Effect.objects.get_or_create(name="Scent of Control", life=3, mind=2)
effect.description = "Hollow Ones using this rote alter their sweat to exude an emotional trigger, trying to push the mental state of someone near them. This can range from 'desire me' to 'protect me' to 'leave me alone,' but if it is a completely unbidden thought, it won't go unnoticed."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 63)
effect, _ = Effect.objects.get_or_create(name="Shameful Outburst", mind=2)
effect.description = "The mage uses carefully chosen words and nonverbal cues to maneuver a target into an embarrassing outburst of some sort. Difficult to use against the Awakened or those with high Willpower, but capable of causing social devastation...or the revelation of secrets in an emotional moment...in those that it effects."
effect.save()
effect.add_source("Order of Reason", 78)
effect, _ = Effect.objects.get_or_create(name="Social Science", mind=2)
effect.description = "The Iterator can use the results of social sciences to depress the target, such as indicating that their IQ is low. Each success reduces the target's Willpower by one for the duration and is resisted with a Willpower roll at difficulty 7."
effect.save()
effect.add_source("Technocracy: Iteration X", 48)
effect, _ = Effect.objects.get_or_create(
    name="Strains of Laughter, Sleep and Sorrow", mind=2
)
effect.description = "The Bards and Skalds of the Verbena know how to use music and story to influence those who listen to it. This rote uses music to cause an audience to feel some emotion of the Verbena's choosing. Up to three successes causes them to feel it, more than that and they feel it intensely enough to act on it. Spending a point of temporary Willpower will allow them to ignore the Effect briefly, but it will return if the mage keeps performing."
effect.save()
effect.add_source("Tradition Book: Verbena (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="Subtle Persuasion", mind=2, prime=2)
effect.description = "Related to the Craft Tome effect, but rather than conveying a hidden meaning only to those who know how to read it, this effect weaves a subtle logic through the work that will persuade the reader of its correctness. Strong-willed readers are harder to persuade, but those who fail a Willpower roll vs. the author's successes in crafting the work are brought to feel an emotion that the author chose at the creation of the object."
effect.save()
effect.add_source("Order of Reason", 90)
effect, _ = Effect.objects.get_or_create(name="Witchwind", forces=5, mind=3, prime=2)
effect.description = "The witchwind is summoned by tying thirteen knots into a rope, submerging it in the blood of a black cat and three dead murderers, and then untying the knots. This causes a storm to blow through the area, and wherever the storm passes, the people fall victim to their darkest impulses. To summon it requires at least 15 successes, and if caught in it, anyone needs to make a Willpower roll at difficulty 7 to resist any temptation that they encounter."
effect.save()
effect.add_source("Infernalism: The Path of Screams", 87)
effect, _ = Effect.objects.get_or_create(name="Animal Possession", mind=4)
effect.description = "Whereas Animal Riding only gives the mage the animal's perceptions and limited control, Animal Possession allows the mage to take control of the animal fully."
effect.save()
effect.add_source("The Spirit Ways", 92)
effect, _ = Effect.objects.get_or_create(name="Animal Riding", mind=3)
effect.description = "The shaman enters the mind of an animal (Correspondence is required if not within sensory range) and shares its perceptions. The shaman has limited control but must either persuade or overwhelm the animal to make it do anything obviously dangerous."
effect.save()
effect.add_source("The Spirit Ways", 89)
effect, _ = Effect.objects.get_or_create(name="Bug Off", life=3, prime=2)
effect.description = (
    "The Kopa Loei who know this rote can create a swarm of insects to attack a target."
)
effect.save()
effect.add_source("Book of Crafts", 74)
effect, _ = Effect.objects.get_or_create(name="Horsemaster's Bidding", mind=2)
effect.description = "This rote allows the mage to force a horse to do what they want. In the case of something the horse strongly doesn't want to do, it gets a willpower roll to succeed."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 91)
effect, _ = Effect.objects.get_or_create(
    name="Mono Kahea 'Ai (Shark Call)", correspondence=3, mind=2
)
effect.description = "With this rote, a mage can summon a shark from the surrounding waters to come as close to the mage as it is possible for them to safely swim."
effect.save()
effect.add_source("Dead Magic II", 29)
effect, _ = Effect.objects.get_or_create(
    name="Ratstorm", correspondence=2, life=2, mind=2
)
effect.description = "With this rote, this mage can call a swarm of small animals to attack a target, with whichever sorts of animals are common in the area, such as rats in a city and dogs in a desert."
effect.save()
effect.add_source("Orphan's Survival Guide", 125)
effect, _ = Effect.objects.get_or_create(
    name="Sedna's Blessing", correspondence=2, mind=2
)
effect.description = "An Inuit shaman takes advantage of the gift of the woman Sedna, who created seals and whales. She is said to live at the bottom of the ocean after a failed rescue attempt from the husband she was tricked into marrying. The shaman dives into the sea and 'combs her hair,' the brambles and kelp of the ocean floor. This sends out a wave of calm, summoning seals and whales to the mage."
effect.save()
effect.add_source("Dead Magic", 131)
effect, _ = Effect.objects.get_or_create(name="Sing to the Whales", mind=2)
effect.description = "Some Inuit fishermen sing songs reminiscent of whale song to draw the whales near. By observing some sort of taboo for a week (along with anyone who is to help in the capture), the mage can draw whales in, making them much easier to hunt."
effect.save()
effect.add_source("Dead Magic", 132)
effect, _ = Effect.objects.get_or_create(name="Divine Aura", mind=2)
effect.description = (
    "This rote creates an aura around the mage that draws all eyes to them."
)
effect.save()
effect.add_source("Mage: The Sorcerer's Crusade", 270)
effect, _ = Effect.objects.get_or_create(
    name="Fifteen Minutes", correspondence=3, mind=2
)
effect.description = "The Agent chooses a target and temporarily gives them Fame for the duration, at one day per success. The Fame is usually due to something like a doctored video spreading across social media."
effect.save()
effect.add_source("Convention Book: New World Order (Revised)", 85)
effect, _ = Effect.objects.get_or_create(name="Going Viral", correspondence=4, mind=3)
effect.description = "Pushes an idea or fact into the public eye. Similar to Fifteen Minutes, this fact is suddenly everywhere, in videos, on the news, it's almost unavoidable, no matter how trivial it actually is."
effect.save()
effect.add_source("Convention Book: New World Order (Revised)", 86)
effect, _ = Effect.objects.get_or_create(
    name="An Uncompromising Commitment to Excellence", life=3, mind=4, prime=3
)
effect.description = "Targets of this procedure work harder than they've ever worked before. Successes are spent first up to the highest willpower of all targets, then to duration. Each success after that decreases difficulties in a single Attribute + Ability pool by 1. For every hour spent in this state, each target takes a level of aggravated damage from the physical and psychological strain of working beyond capacity. If one of the workers dies, the Technocrat gains 5 points of Primal Energy. Targets can roll Willpower at difficulty 8 to resist each time they suffer damage or are asked to do something blatantly self-destructive or Nature-defying."
effect.save()
effect.add_source("Convention Book: Syndicate (Revised)", 82)
effect, _ = Effect.objects.get_or_create(name="Coordination", correspondence=3, mind=3)
effect.description = "By giving every agent on a team a camera, a microphone and an earpiece, a coordinator back at a safe house can see and hear everything that the group does and give orders in real time to make sure that the team is working together even when out of sight."
effect.save()
effect.add_source("Guide to the Technocracy", 206)
effect, _ = Effect.objects.get_or_create(name="Karoshi", life=2, mind=1)
effect.description = "It is possible to work so hard that a person puts their life at risk. This rote allows a Syndicate agent to either do so themselves (lesser version) or to lead others (greater version), and each success lets them go without rest or refreshment for a day."
effect.save()
effect.add_source("Technocracy: Syndicate", 46)
effect, _ = Effect.objects.get_or_create(name="Workflow", time=3, mind=2)
effect.description = "Successes are divided among the number of people in the team, the duration of the work, and the power of the procedure. Workflow decreases the time between mundane rolls on a project significantly, dividing it by the number of successes put into power."
effect.save()
effect.add_source("Convention Book: Syndicate (Revised)", 75)
effect, _ = Effect.objects.get_or_create(name="Delion's Haze", time=3, entropy=2)
effect.description = "By randomly altering time around the victim, the mage disrupts their concentration so badly that all their dice pools for the duration are bounded by their Willpower."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 222)
effect, _ = Effect.objects.get_or_create(name="Destroy Thought", entropy=5)
effect.description = "The target has a rational thought or feeling degraded until it is gone. It will often appear as though they have rationalized themselves out of it."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 193)
effect.add_source("Mage: The Ascension (Second Edition)", 195)
effect, _ = Effect.objects.get_or_create(name="Downward Spiral", mind=3)
effect.description = "Reserved for their reviled enemies, this rote inserts a phrase into the target's mind. This phrase repeats and echoes, bringing up increasing shame, insecurity and self-loathing to the point where it can incapacitate the target, or lead to suicide."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 42)
effect, _ = Effect.objects.get_or_create(
    name="Magdeline's Dynamic Mind", entropy=2, mind=3
)
effect.description = "Causes thoughts in the target to become random and incoherent."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 222)
effect, _ = Effect.objects.get_or_create(
    name="The Trip", correspondence=2, time=2, entropy=1, mind=4
)
effect.description = "The Cultist can use this rote to seize control of a target's mind and cause them to relive some moment of their lives where they were confused, deluded or had significant misconceptions. Correspondence and Time allow the Cultist to see the incident involved directly, both confusing the target and giving the Cultist valuable information."
effect.save()
effect.add_source("Book of Shadows", 410)
effect, _ = Effect.objects.get_or_create(name="Dream Drama", forces=2, mind=3)
effect.description = "This rote allows the Hermetic to create an illusion of light and sound that will let them watch the dreams of someone who is asleep. If they are not present, Correspondence is required."
effect.save()
effect.add_source("Tradition Book: Order of Hermes (First Edition)", 64)
effect, _ = Effect.objects.get_or_create(name="Dream Play", time=2, mind=3, prime=2)
effect.description = "A Hollow One who works with Dreams can design a scenario, down to intricate details, and then causing a target to experience it as a dream. The user of this rote acts as the director, and in the dream, this takes the form of a play with substantial audience participation from the targets of the effect."
effect.save()
effect.add_source("Tradition Book: Hollow Ones (Revised)", 67)
effect, _ = Effect.objects.get_or_create(name="Nightmare Dance", spirit=2)
effect.description = "The Dreamspeaker sends disturbing dreams to someone that they don't like. The Mind version taps directly into the target's fears, whereas the Spirit version calls a spirit such as Night Terror to do it for the mage."
effect.save()
effect.add_source("Tradition Book: Dreamspeakers (First Edition)", 67)
effect, _ = Effect.objects.get_or_create(name="Delirium", mind=3)
effect.description = "The mage gets themselves into a hallucinatory state, whether through meditation, drugs or other methods, and then sends the hallucinations to a target. Successes determine number of targets. With a light show and music, Forces can be added to gain a success, making it easier to affect groups."
effect.save()
effect.add_source("Orphan's Survival Guide", 128)
effect, _ = Effect.objects.get_or_create(name="Frame Up", matter=3, mind=3)
effect.description = "The Nephandus can create simple illusions to create among the victim's friends a feeling that they are guilty of something. Matter is used to make physical evidence seem incriminating, Life is used for things such as minor aches, cheeks that have been slapped, or the symptoms of pregnancy."
effect.save()
effect.add_source("Hidden Lore", 49)
effect, _ = Effect.objects.get_or_create(
    name="Holographic Projector", correspondence=2, forces=3, mind=3, prime=2
)
effect.description = "With this rote, a Virtual Adept can project a holograph of themselves. Forces creates the visual and auditory effects and Mind creates other sensory inputs."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (First Edition)", 62)
effect, _ = Effect.objects.get_or_create(name="IFF", correspondence=2, forces=2)
effect.description = "Named to reference both 'if and only if' (as in, 'if and only if you are badly outnumbered') and 'identify friend or foe', this Virtual Adept rote copies the image of a suitable enemy and uses Forces to make the Virtual Adept look and sound identical to them. For each success, subtract one from the target's attack roll. This also cancels any previous targeting."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 62)
effect, _ = Effect.objects.get_or_create(name="Imaginary Friend", mind=4, prime=2)
effect.description = "The subject of this procedure is programmed to see and hear a fabricated persona that no one else can."
effect.save()
effect.add_source("Technocracy: New World Order", 49)
effect, _ = Effect.objects.get_or_create(
    name="Painting the War Dance", matter=2, mind=2
)
effect.description = "Using hand-mixed paints to draw images of a story, the mage channels their own thoughts (Mind) or the past (Time) and the images begin to move, playing out the story being told."
effect.save()
effect.add_source("Dead Magic", 29)
effect, _ = Effect.objects.get_or_create(
    name="Behavior Modification Device", entropy=3, mind=4
)
effect.description = "This Procedure allows the Void Engineers to alter and delete selected memories in the subject."
effect.save()
effect.add_source("Technocracy: Void Engineers", 48)
effect, _ = Effect.objects.get_or_create(name="False Witness", mind=3)
effect.description = "Creates a false memory in the target."
effect.save()
effect.add_source("The Swashbuckler's Handbook", 93)
effect, _ = Effect.objects.get_or_create(name="High Memory", entropy=2, mind=3)
effect.description = "This rote takes some information and shuffles it together with random noise in the mage's mind, rendering it much harder to detect."
effect.save()
effect.add_source("Digital Web", 99)
effect, _ = Effect.objects.get_or_create(name="Manipulate Memories", mind=4)
effect.description = "The Progenitor can block certain memories with this procedure, often used to let a newly activated clone not remember their death."
effect.save()
effect.add_source("Technocracy: Progenitors", 42)
effect, _ = Effect.objects.get_or_create(name="Manipulate Memory", mind=4)
effect.description = (
    "With Manipulate Memory, the mage can alter the memories of the target."
)
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 207)
effect.add_source("Mage: The Ascension (Second Edition)", 211)
effect.add_source("Mage: The Ascension (Revised)", 178)
effect.add_source("Technocracy: New World Order", 47)
effect, _ = Effect.objects.get_or_create(name="Move to Clone", mind=5)
effect.description = "The Progenitor can transfer their consciousness to a clone body. Note that this is more than just a duplication of the memories, but continuity of experience."
effect.save()
effect.add_source("Technocracy: Progenitors", 42)
effect, _ = Effect.objects.get_or_create(name="Nostalgia", time=3, mind=2)
effect.description = "A Cultist can pull up a memory of some overwhelming stimulus from the target's past. The Cultist can determine a positive or a negative association, but often doesn't have control over exactly what. With Life 2, the target will feel the sensation rather than just remembering it, and with Mind 3 it can be tied to a trigger, letting the Cultist encourage or discourage specific behaviors."
effect.save()
effect.add_source("Tradition Book: Cult of Ecstasy (Revised)", 71)
effect, _ = Effect.objects.get_or_create(name="Plausible Denial", mind=3)
effect.description = "The New World Order Agent can use this Procedure to induce memory blackouts in a target, forcing them to forget that they witnessed something."
effect.save()
effect.add_source("Technocracy: New World Order", 46)
effect, _ = Effect.objects.get_or_create(name="Probe Thoughts", mind=3)
effect.description = "This rote allows a Mind mage to forcibly dig into a target's mind to pull up memories or to read the subconscious."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 207)
effect.add_source("Mage: The Ascension (Second Edition)", 210)
effect.add_source("Mage: The Ascension (Revised)", 177)
effect, _ = Effect.objects.get_or_create(name="Scan Memories", mind=2)
effect.description = "This procedure scans the memories of the target, determining if there is any damage to them, and records it to use as a template for memory transfer to a new body."
effect.save()
effect.add_source("Technocracy: Progenitors", 42)
effect, _ = Effect.objects.get_or_create(name="Transfer Memories", mind=3)
effect.description = (
    "This procedure transfers memories from one individual into a blank mind."
)
effect.save()
effect.add_source("Technocracy: Progenitors", 42)
effect, _ = Effect.objects.get_or_create(name="Worm", mind=4)
effect.description = "This Cypherpunk rote is designed to erase sensitive information from the Virtual Adept's brain, without damaging personality, Sphere knowledge or general skills. Mind 4 is all that is needed to guarantee erasure, but Entropy or Time is used to make sure nothing else is erased by accident."
effect.save()
effect.add_source("Tradition Book: Virtual Adepts (Revised)", 65)
effect, _ = Effect.objects.get_or_create(name="Alter Paradigm", entropy=5, mind=5)
effect.description = "Through extensive indoctrination and torture, the New World Order can break down the basic beliefs a target has about how the world works and build up a new paradigm inside them, almost always the Technocratic worldview."
effect.save()
effect.add_source("Technocracy: New World Order", 51)
effect, _ = Effect.objects.get_or_create(
    name="The Blissful Discipline", forces=3, mind=4, prime=2
)
effect.description = "This rote is used to shock a target (see Discharge Static) whenever they think a certain thought."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 226)
effect, _ = Effect.objects.get_or_create(name="Consuming Thought", mind=3, prime=2)
effect.description = "This rote creates a thought in the target's mind, and forces it constantly to the surface, so that it is the only thing that the target can think about, without an act of Willpower."
effect.save()
effect.add_source("Hidden Lore", 13)
effect, _ = Effect.objects.get_or_create(name="Create Drone", entropy=5)
effect.description = "When Mind Control and Social Conditioning and even Indoctrination can't break a target, some New World Order Agents will instead degrade their minds to the point where they are only capable of the simplest tasks."
effect.save()
effect.add_source("Technocracy: New World Order", 44)
effect, _ = Effect.objects.get_or_create(name="Create Mind", mind=5)
effect.description = "With this effect, the Master of Mind can create an entirely new conscious mind. This can be used to create artificial intelligences in computer systems, to grant intelligence to animals, or to give an 'empty' body a consciousness."
effect.save()
effect.add_source("Mage: The Ascension (Revised)", 179)
effect, _ = Effect.objects.get_or_create(name="Deprocessing", mind=4)
effect.description = "This Procedure removes standard Technocratic Conditioning, essential for Void Engineers, especially in other Dimensions. This requires twice as many successes as the target's Willpower Conditioning. With Prime 2, each success acts as a die of countermagick against any Procedure the subject attempts that is motivated by Conditioning, including those that interfere with the Deprocessing."
effect.save()
effect.add_source("Technocracy: Void Engineers", 45)
effect.add_source("Convention Book: Void Engineers (Revised)", 85)
effect, _ = Effect.objects.get_or_create(
    name="Destructive Paranoia", entropy=2, mind=4, prime=2
)
effect.description = "After extended indoctrination (at least a week), the subject believes that they are dramatically more persecuted than they actually are, leading to paranoid delusions and further complications of mental illness."
effect.save()
effect.add_source("Technocracy: New World Order", 50)
effect, _ = Effect.objects.get_or_create(name="Hypernarrative Influence", mind=3)
effect.description = "An effective agent who understands common narratives in pop culture can take advantage of a situation and force those nearby to play along. By grabbing a hostage, can force a hostile to demand they 'let the girl go' rather than shooting, can trick a group into splitting up to 'cover more ground,' etc."
effect.save()
effect.add_source("Convention Book: Syndicate (Revised)", 74)
effect.add_source("Mage: The Ascension (20th Anniversary Edition)", 603)
effect, _ = Effect.objects.get_or_create(name="Impulse Purchase", mind=3)
effect.description = "There are two versions of this procedure, both of which make use of Enlightened Marketing techniques to persuade people to buy things that they don't need. With Mind 3, it can cause a single person to buy something at a store. With Mind 2 and Prime 2, it can be used to make a store more conducive to impulse purchases in general."
effect.save()
effect.add_source("Guide to the Technocracy", 215)
effect, _ = Effect.objects.get_or_create(
    name="Internal Obligation", time=4, mind=4, prime=3
)
effect.description = "Using acupuncture, the Akashic ensures that the target will experience a specific response whenever a certain event occurs. The target must do what the conditions require whenever this event occurs, whether it's controlling actions and memories through Mind or directly manipulating the body with Life."
effect.save()
effect.add_source("Tradition Book: Akashic Brotherhood (Revised)", 68)
effect, _ = Effect.objects.get_or_create(name="Maikai (The Seaward Pull)", mind=3)
effect.description = "The target of this effect gains the urgent need to be in the ocean, swimming as far out as possible. Without aid of some sort, this will result on most targets drowning."
effect.save()
effect.add_source("Dead Magic II", 28)
effect, _ = Effect.objects.get_or_create(name="Manchurian Condidate", mind=5)
effect.description = "With this level of Mastery, a New World Order Agent can program a target to perform a series of actions on command."
effect.save()
effect.add_source("Technocracy: New World Order", 47)
effect, _ = Effect.objects.get_or_create(name="Mind Rune", mind=4)
effect.description = "With the Mind Rune, a mage can take control of another person's mind, as with Possession or Manipulate Memories."
effect.save()
effect.add_source("Dead Magic II", 101)
effect, _ = Effect.objects.get_or_create(name="Morpheus's Kiss", life=2, mind=2)
effect.description = (
    "Puts a target who wants to sleep, at least a little bit, to sleep."
)
effect.save()
effect.add_source("The Swashbuckler's Handbook", 93)
effect, _ = Effect.objects.get_or_create(name="Nervous Control", life=3, forces=3)
effect.description = "With a controlled electronic pulse guided by intimate knowledge of neurology, the Progenitor may compel someone to repeat an action, to feel intense pain, or to feel no pain whatsoever."
effect.save()
effect.add_source("Technocracy: Progenitors", 44)
effect.add_source("Convention Book: Progenitors (Revised)", 74)
effect, _ = Effect.objects.get_or_create(name="Possession", mind=4)
effect.description = "This rote allows the mage to exert direct control over the target, forcing them to behave in a way according to the mage's will."
effect.save()
effect.add_source("Mage: The Ascension (First Edition)", 207)
effect.add_source("Mage: The Ascension (Second Edition)", 210)
effect.add_source("Mage: The Ascension (Revised)", 178)
effect, _ = Effect.objects.get_or_create(name="Processing", mind=5, prime=2)
effect.description = "Using extreme situations: loud music, straps, holographic projectors, acupuncture needles, etc. (for instance, as in A Clockwork Orange), over the course of a week a New World Order agent can completely rebuild the mind of the target, bending it to their will. Not being a blank slate, this leads to massive psychological scarring, a high suicide rate and other adverse side effects. Furthermore, in times of massive stress, the player of such a character can spend a point of Willpower for the character to return to their original personality for a single turn, though they cannot act against the Union."
effect.save()
effect.add_source("Convention Book: New World Order (Revised)", 86)
effect, _ = Effect.objects.get_or_create(name="Programming", mind=3)
effect.description = "Through careful effort, a New World Order Agent can brainwash a person (or a group if they have trained together). With more successes than the Willpower of the target (or highest among targets), the Technocrat can give a one sentence verbal command to their target."
effect.save()
effect.add_source("Guide to the Technocracy", 214)
effect, _ = Effect.objects.get_or_create(name="Psychic Intrusion", mind=2)
effect.description = "This procedure weakens the resolve of the target of an interrogation, decreasing the target's temporary Willpower by one per success."
effect.save()
effect.add_source("Technocracy: New World Order", 45)
effect, _ = Effect.objects.get_or_create(name="Purge Thought Crime", mind=3, prime=3)
effect.description = "By Conditioning someone with this Procedure, a Technocrat can prevent them from thinking along certain lines, establishing a block. The more detail to be blocked, the more successes are necessary."
effect.save()
effect.add_source("Guide to the Technocracy", 215)
effect, _ = Effect.objects.get_or_create(name="Random Impulse", entropy=2, mind=4)
effect.description = "The target loses control of their mind for a five-minute increment per success. The mage may attempt to direct their actions, once per success spent on this, but the target can resist control with Willpower at difficulty 7. Otherwise, the target's actions are random, as their mind has been scrambled and invested with chaotic energy."
effect.save()
effect.add_source("Book of Shadows", 141)
effect, _ = Effect.objects.get_or_create(name="Recant", entropy=2, mind=2)
effect.description = "This rote is used by the Knights Templar to stamp out heresy before it grows too large. If someone is a true believer in something, this will not work, but it can channel someone's thoughts down more agreeable avenues, allowing them to be persuaded away from an idea they are exploring."
effect.save()
effect.add_source("Book of Crafts", 103)
effect, _ = Effect.objects.get_or_create(
    name="Re-education Mode", time=3, mind=4, prime=2
)
effect.description = "A Technocratic variant on The Moment that Stretches, the New World Order performs this procedure on an unwilling victim. They can use it to paralyze the victim and force them to experience long stretches of mind-numbing boredom in a much shorter period of actual time."
effect.save()
effect.add_source("Hidden Lore", 53)
effect, _ = Effect.objects.get_or_create(name="See the Light", entropy=3, mind=3)
effect.description = "With Mind and Entropy, the mage disrupts the thoughts of their target, making their reasoning weak and bringing their insecurities to the fore. With the Entropy only version, thoughts are destroyed directly for the same effect."
effect.save()
effect.add_source("Tradition Book: Celestial Chorus", 65)
effect, _ = Effect.objects.get_or_create(name="Self-Possession", mind=4)
effect.description = "By repeating in their head, a phrase, mantra, poem or song that the Taftani feels embodies who they are, they train their mind to keep it on loop in the back of their mind, endlessly. This provides protection against possession and mind-control, allowing this pocket of the Taftani's confirmed nature to attempt to take control of any intruder in the mage's mind. The mage gains Willpower points for the purpose of fighting off mind control equal to the number of successes put into strength of the effect, and the invader is at -3 on all attempts to control the mage. Furthermore, the mage may attempt to counter-possess any entity that possesses them."
effect.save()
effect.add_source("Lost Paths: Ahl-i-Batin and Taftani", 91)
effect, _ = Effect.objects.get_or_create(name="Sinner's Redemption", mind=5)
effect.description = "This rote is extremely difficult but has incredible potential. If successful, the mage can restructure the fundamental belief system of the target, changing their Paradigm, their notions of right and wrong, anything. Each day, a contested Arete roll at difficulty 9 is made. If the inquisitor can accumulate more successes than the target's permanent Willpower, the change is permanent."
effect.save()
effect.add_source("Order of Reason", 109)
effect, _ = Effect.objects.get_or_create(name="Social Conditioning", mind=3, prime=2)
effect.description = "This Procedure allows the New World Order Agent to increase the Social Conditioning of another Technocrat. For details, see Mage: The Ascension 20th Anniversary Edition pages 605-607."
effect.save()
effect.add_source("Technocracy: New World Order", 46)
effect.add_source("Guide to the Technocracy", 214)
effect, _ = Effect.objects.get_or_create(name="Soul Shaping", spirit=5, mind=4, prime=3)
effect.description = "The Hollow One response to things like Room 101, this rote pushes the soul of the target out of their body, makes alterations, and returns it. One success can change their view of a person, five allows them to be almost completely rewritten, such as turning a Technomage into a Mystic, or even changing their Essence."
effect.save()
effect.add_source("World of Darkness: Outcasts", 90)
effect, _ = Effect.objects.get_or_create(
    name="Temple Gongs", matter=4, life=3, forces=4, mind=4, prime=2
)
effect.description = "This rote rings a gong loudly and then transforms people nearby into monks via Life and Mind brainwashing."
effect.save()
effect.add_source("Hidden Lore", 52)
effect, _ = Effect.objects.get_or_create(name="Ultimate Argument", mind=3)
effect.description = "With this rote, a mage can talk almost anyone into almost anything. With a number of successes equal to the target's temporary Willpower, an unsuspecting target can be persuaded. If the target resists, they get to roll Willpower to defend."
effect.save()
effect.add_source("Order of Reason", 80)
effect, _ = Effect.objects.get_or_create(name="Welcoming the Jester", mind=4)
effect.description = "The mage causes the target to act in a preposterous manner, rational thought disappearing for the duration. The target will then insult anyone who has offended them and embrace anyone who they find attractive. Essentially, it removes the target's filters."
effect.save()
effect.add_source("World of Darkness: Outcasts", 91)
effect, _ = Effect.objects.get_or_create(name="Willful Binding", mind=4)
effect.description = "Verbena often believe that so long as a person does no harm, they should be free to do as the will. However, when it comes to enforcing this on others, they tend to consider that fair game. With this rote, the Verbena can give a target a command and the target is unable to violate this command. Optionally, spending Willpower would allow them to overcome the binding for one round. This command can be as broad or specific as the mage chooses."
effect.save()
effect.add_source("Tradition Book: Verbena (Revised)", 69)

effect_palimpsest = Effect.objects.get_or_create(
    name="Palimpsest", matter=3, time=2, prime=2
)[0].add_source("Lore of the Traditions", 45)
effect_dismiss_the_discordant = Effect.objects.get_or_create(
    name="Dismiss the Discordant", mind=2, correspondence=2, entropy=2, prime=2
)[0].add_source("Lore of the Traditions", 45)

effect_bullet_rider_s_blessing = Effect.objects.get_or_create(
    name="Bullet-Rider's Blessing", entropy=1, matter=3, spirit=3
)[0].add_source("Lore of the Traditions", 82)
effect_dwennimmen = Effect.objects.get_or_create(name="Dwennimmen", mind=4, spirit=4)[
    0
].add_source("Lore of the Traditions", 82)
effect_blood_for_the_ghosts = Effect.objects.get_or_create(
    name="Blood for the Ghosts", entropy=2, prime=2, spirit=2
)[0].add_source("Lore of the Traditions", 97)
effect_the_last_sacrifice = Effect.objects.get_or_create(
    name="The Last Sacrifice", entropy=4, spirit=2
)[0].add_source("Lore of the Traditions", 97)
effect_nfts_non_fungible_tass_talismans = Effect.objects.get_or_create(
    name="NFTs (Non-Fungible Tass/Talismans)", mind=3, prime=2
)[0].add_source("Lore of the Traditions", 162)
effect_nfts_non_fungible_tass_talismans_time_tamper_protection = (
    Effect.objects.get_or_create(
        name="NFTs (Non-Fungible Tass/Talismans) (Time Tamper Protection)",
        mind=3,
        prime=2,
        time=4,
    )[0].add_source("Lore of the Traditions", 162)
)
effect_nfts_non_fungible_tass_talismans_entropy_tamper_protection = (
    Effect.objects.get_or_create(
        name="NFTs (Non-Fungible Tass/Talismans) (Entropy Tamper Protection)",
        mind=3,
        prime=2,
        entropy=3,
    )[0].add_source("Lore of the Traditions", 162)
)
effect_nfts_non_fungible_tass_talismans_tracking = Effect.objects.get_or_create(
    name="NFTs (Non-Fungible Tass/Talismans) (Tracking)",
    correspondence=2,
    mind=3,
    prime=2,
)[0].add_source("Lore of the Traditions", 162)
effect_nfts_non_fungible_tass_talismans_time_tamper_protection_tracking = (
    Effect.objects.get_or_create(
        name="NFTs (Non-Fungible Tass/Talismans) (Time Tamper Protection, Tracking)",
        correspondence=2,
        mind=3,
        prime=2,
        time=4,
    )[0].add_source("Lore of the Traditions", 162)
)
effect_nfts_non_fungible_tass_talismans_entropy_tamper_protection_tracking = (
    Effect.objects.get_or_create(
        name="NFTs (Non-Fungible Tass/Talismans) (Entropy Tamper Protection, Tracking)",
        correspondence=2,
        mind=3,
        prime=2,
        entropy=3,
    )[0].add_source("Lore of the Traditions", 162)
)
effect_save_state = Effect.objects.get_or_create(
    name="Save State", mind=3, time=2, prime=2
)[0].add_source("Lore of the Traditions", 162)
effect_locate_geospatial_nodal_point = Effect.objects.get_or_create(
    name="Locate Geospatial Nodal Point",
    forces=4,
    entropy=3,
    correspondence=3,
    matter=3,
)[0].add_source("Lore of the Traditions", 162)
from characters.models.mage.effect import Effect

# ===== NECROMANCY & DEATH MAGIC =====
effect_summon_ghost = Effect.objects.get_or_create(name="Summon Ghost", spirit=2)[
    0
].add_source("How Do You Do That", 142)

effect_summon_powerful_ghost = Effect.objects.get_or_create(
    name="Summon Powerful Ghost", spirit=3
)[0].add_source("How Do You Do That", 142)

effect_see_into_shadowlands = Effect.objects.get_or_create(
    name="See Into Shadowlands", spirit=1, entropy=1
)[0].add_source("How Do You Do That", 142)

effect_step_sideways_to_shadowlands = Effect.objects.get_or_create(
    name="Step Sideways to Shadowlands", spirit=3
)[0].add_source("How Do You Do That", 142)

effect_speak_with_dead = Effect.objects.get_or_create(
    name="Speak with Dead", spirit=2, mind=1
)[0].add_source("How Do You Do That", 142)

effect_bind_ghost = Effect.objects.get_or_create(name="Bind Ghost", spirit=4)[
    0
].add_source("How Do You Do That", 143)

effect_banish_ghost = Effect.objects.get_or_create(
    name="Banish Ghost", spirit=3, prime=2
)[0].add_source("How Do You Do That", 143)

effect_create_zombie_simple = Effect.objects.get_or_create(
    name="Create Zombie (Simple)", life=3, matter=2, prime=2
)[0].add_source("How Do You Do That", 144)

effect_create_zombie_complex = Effect.objects.get_or_create(
    name="Create Zombie (Complex)", life=4, matter=2, prime=2, mind=1
)[0].add_source("How Do You Do That", 144)

effect_restore_recently_dead_to_life = Effect.objects.get_or_create(
    name="Restore Recently Dead to Life", life=5, prime=2, spirit=4
)[0].add_source("How Do You Do That", 145)

effect_restore_long_dead_to_life = Effect.objects.get_or_create(
    name="Restore Long Dead to Life", life=5, prime=3, spirit=5, time=3
)[0].add_source("How Do You Do That", 145)

effect_create_lich_self = Effect.objects.get_or_create(
    name="Create Lich (Self)", life=5, spirit=4, prime=3, entropy=3
)[0].add_source("How Do You Do That", 146)

# ===== TIME MANIPULATION =====
effect_sense_time_flow = Effect.objects.get_or_create(name="Sense Time Flow", time=1)[
    0
].add_source("How Do You Do That", 154)

effect_see_past_recent = Effect.objects.get_or_create(name="See Past (Recent)", time=2)[
    0
].add_source("How Do You Do That", 154)

effect_see_future_near = Effect.objects.get_or_create(name="See Future (Near)", time=2)[
    0
].add_source("How Do You Do That", 154)

effect_see_past_distant = Effect.objects.get_or_create(
    name="See Past (Distant)", time=3, correspondence=2
)[0].add_source("How Do You Do That", 154)

effect_see_future_distant = Effect.objects.get_or_create(
    name="See Future (Distant)", time=3
)[0].add_source("How Do You Do That", 154)

effect_slow_time_local = Effect.objects.get_or_create(name="Slow Time (Local)", time=3)[
    0
].add_source("How Do You Do That", 155)

effect_speed_time_local = Effect.objects.get_or_create(
    name="Speed Time (Local)", time=3
)[0].add_source("How Do You Do That", 155)

effect_freeze_time_small_area = Effect.objects.get_or_create(
    name="Freeze Time (Small Area)", time=4
)[0].add_source("How Do You Do That", 155)

effect_stop_time_large_area = Effect.objects.get_or_create(
    name="Stop Time (Large Area)", time=5
)[0].add_source("How Do You Do That", 155)

effect_rewind_time_seconds = Effect.objects.get_or_create(
    name="Rewind Time (Seconds)", time=5, prime=2
)[0].add_source("How Do You Do That", 156)

effect_travel_through_time = Effect.objects.get_or_create(
    name="Travel Through Time", time=5, spirit=4, prime=3
)[0].add_source("How Do You Do That", 156)

effect_create_time_loop = Effect.objects.get_or_create(
    name="Create Time Loop", time=4, prime=2
)[0].add_source("How Do You Do That", 156)

# ===== ADVANCED CORRESPONDENCE =====
effect_teleport_self_short_range = Effect.objects.get_or_create(
    name="Teleport Self (Short Range)", correspondence=3, life=2
)[0].add_source("How Do You Do That", 127)

effect_teleport_self_long_range = Effect.objects.get_or_create(
    name="Teleport Self (Long Range)", correspondence=4, life=2
)[0].add_source("How Do You Do That", 127)

effect_teleport_others = Effect.objects.get_or_create(
    name="Teleport Others", correspondence=4, life=3
)[0].add_source("How Do You Do That", 127)

effect_create_portal_temporary = Effect.objects.get_or_create(
    name="Create Portal (Temporary)", correspondence=4, spirit=2
)[0].add_source("How Do You Do That", 128)

effect_create_portal_permanent = Effect.objects.get_or_create(
    name="Create Portal (Permanent)", correspondence=4, spirit=2, prime=2
)[0].add_source("How Do You Do That", 128)

effect_co_location_be_in_two_places = Effect.objects.get_or_create(
    name="Co-Location (Be In Two Places)", correspondence=5, life=3, mind=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 515)

effect_fold_space = Effect.objects.get_or_create(name="Fold Space", correspondence=5)[
    0
].add_source("Mage: The Ascension 20th Anniversary Edition", 515)

effect_ward_against_teleportation = Effect.objects.get_or_create(
    name="Ward Against Teleportation", correspondence=3, prime=2
)[0].add_source("How Do You Do That", 128)

# ===== ADVANCED LIFE MAGIC =====
effect_shapeshift_into_animal_self = Effect.objects.get_or_create(
    name="Shapeshift into Animal (Self)", life=4
)[0].add_source("How Do You Do That", 34)

effect_shapeshift_into_animal_others = Effect.objects.get_or_create(
    name="Shapeshift into Animal (Others)", life=5
)[0].add_source("How Do You Do That", 34)

effect_shapeshift_into_hybrid_form = Effect.objects.get_or_create(
    name="Shapeshift into Hybrid Form", life=4, prime=2
)[0].add_source("How Do You Do That", 34)

effect_create_homunculus = Effect.objects.get_or_create(
    name="Create Homunculus", life=5, prime=3, mind=2
)[0].add_source("Book of Secrets", 79)

effect_clone_body = Effect.objects.get_or_create(
    name="Clone Body", life=5, prime=2, mind=1
)[0].add_source("Book of Secrets", 79)

effect_enhance_physical_attribute_permanent = Effect.objects.get_or_create(
    name="Enhance Physical Attribute (Permanent)", life=4, prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)

effect_grant_regeneration = Effect.objects.get_or_create(
    name="Grant Regeneration", life=4, prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)

effect_age_de_age_target = Effect.objects.get_or_create(
    name="Age/De-Age Target", life=4, time=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)

effect_cure_poison_disease_aggravated = Effect.objects.get_or_create(
    name="Cure Poison/Disease (Aggravated)", life=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)

# ===== ADVANCED MIND MAGIC =====
effect_read_surface_thoughts = Effect.objects.get_or_create(
    name="Read Surface Thoughts", mind=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 519)

effect_read_deep_thoughts_memories = Effect.objects.get_or_create(
    name="Read Deep Thoughts/Memories", mind=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 519)

effect_implant_false_memory = Effect.objects.get_or_create(
    name="Implant False Memory", mind=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 519)

effect_mind_control_simple_command = Effect.objects.get_or_create(
    name="Mind Control (Simple Command)", mind=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 519)

effect_mind_control_complex = Effect.objects.get_or_create(
    name="Mind Control (Complex)", mind=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 519)

# effect_possession = Effect.objects.get_or_create(name="Possession", mind=4, life=3)[0].add_source(
#     "How Do You Do That", 164
# )
# )

effect_astral_quest = Effect.objects.get_or_create(
    name="Astral Quest", mind=5, spirit=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 519)

effect_shatter_mind = Effect.objects.get_or_create(name="Shatter Mind", mind=5)[
    0
].add_source("Mage: The Ascension 20th Anniversary Edition", 519)

effect_create_permanent_mental_illusion = Effect.objects.get_or_create(
    name="Create Permanent Mental Illusion", mind=4, prime=2
)[0].add_source("How Do You Do That", 162)

effect_mass_telepathy = Effect.objects.get_or_create(
    name="Mass Telepathy", mind=3, correspondence=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 519)

# ===== ADVANCED FORCES =====
effect_lightning_bolt = Effect.objects.get_or_create(name="Lightning Bolt", forces=3)[
    0
].add_source("Mage: The Ascension 20th Anniversary Edition", 517)

effect_fireball = Effect.objects.get_or_create(name="Fireball", forces=3)[0].add_source(
    "Mage: The Ascension 20th Anniversary Edition", 517
)

effect_force_shield = Effect.objects.get_or_create(name="Force Shield", forces=3)[
    0
].add_source("Mage: The Ascension 20th Anniversary Edition", 517)

effect_flight_self = Effect.objects.get_or_create(
    name="Flight (Self)", forces=2, life=2
)[0].add_source("How Do You Do That", 126)

effect_flight_others = Effect.objects.get_or_create(
    name="Flight (Others)", forces=3, life=2
)[0].add_source("How Do You Do That", 126)

# Duplicate of line 49 - removed

effect_control_weather_major = Effect.objects.get_or_create(
    name="Control Weather (Major)", forces=5, life=2, matter=2, prime=2
)[0].add_source("How Do You Do That", 49)

effect_laser_blast = Effect.objects.get_or_create(
    name="Laser Blast", forces=3, matter=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 517)

effect_emp_pulse = Effect.objects.get_or_create(name="EMP Pulse", forces=3, matter=2)[
    0
].add_source("Mage: The Ascension 20th Anniversary Edition", 517)

effect_nuclear_blast = Effect.objects.get_or_create(
    name="Nuclear Blast", forces=5, prime=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 517)

# ===== ADVANCED MATTER =====
effect_transmute_base_metals_to_gold = Effect.objects.get_or_create(
    name="Transmute Base Metals to Gold", matter=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)

effect_create_matter_from_nothing = Effect.objects.get_or_create(
    name="Create Matter from Nothing", matter=4, prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)

effect_alter_fundamental_properties = Effect.objects.get_or_create(
    name="Alter Fundamental Properties", matter=5
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)

effect_phase_through_matter = Effect.objects.get_or_create(
    name="Phase Through Matter", matter=3, life=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)

effect_disintegrate_object = Effect.objects.get_or_create(
    name="Disintegrate Object", matter=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)

effect_turn_to_stone = Effect.objects.get_or_create(
    name="Turn to Stone", matter=3, life=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)

# ===== ADVANCED ENTROPY =====
effect_curse_of_bad_luck = Effect.objects.get_or_create(
    name="Curse of Bad Luck", entropy=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 516)

effect_blessing_of_good_fortune = Effect.objects.get_or_create(
    name="Blessing of Good Fortune", entropy=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 516)

effect_age_object_rapidly = Effect.objects.get_or_create(
    name="Age Object Rapidly", entropy=3, time=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 516)

effect_rot_living_being = Effect.objects.get_or_create(
    name="Rot Living Being", entropy=4, life=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 516)

effect_shatter_pattern = Effect.objects.get_or_create(
    name="Shatter Pattern", entropy=5, prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 516)

effect_control_probability_major = Effect.objects.get_or_create(
    name="Control Probability (Major)", entropy=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 516)

# effect_death_curse = Effect.objects.get_or_create(name="Death Curse", entropy=5, life=4, spirit=3)[
#     0
# ].add_source("Mage: The Ascension 20th Anniversary Edition", 516)

# ===== ADVANCED PRIME =====
# "Sense Quintessence" - duplicate of line 3301, removed

# "Channel Quintessence" - duplicate of line 127, removed

effect_enchant_talisman = Effect.objects.get_or_create(
    name="Enchant Talisman", prime=3
)[0].add_source("Book of Secrets", 82)

# effect_create_wonder = Effect.objects.get_or_create(name="Create Wonder", prime=5)[0].add_source(
#     "Book of Secrets", 82
# )
# )

effect_disenchant_wonder = Effect.objects.get_or_create(
    name="Disenchant Wonder", prime=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 520)

effect_nullify_magic = Effect.objects.get_or_create(name="Nullify Magic", prime=3)[
    0
].add_source("Mage: The Ascension 20th Anniversary Edition", 520)

effect_permanently_enhance_pattern = Effect.objects.get_or_create(
    name="Permanently Enhance Pattern", prime=5
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 520)

effect_fuel_pattern_with_quintessence = Effect.objects.get_or_create(
    name="Fuel Pattern with Quintessence", prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 520)

effect_create_tass = Effect.objects.get_or_create(name="Create Tass", prime=3)[
    0
].add_source("Mage: The Ascension 20th Anniversary Edition", 520)

effect_open_seal_node = Effect.objects.get_or_create(
    name="Open/Seal Node", prime=4, spirit=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 520)

# ===== ADVANCED SPIRIT =====
# "See Spirits" - duplicate of line 144, removed

effect_touch_spirit_matter = Effect.objects.get_or_create(
    name="Touch Spirit Matter", spirit=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)

effect_step_sideways_to_umbra = Effect.objects.get_or_create(
    name="Step Sideways to Umbra", spirit=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)

effect_reach_into_umbra = Effect.objects.get_or_create(
    name="Reach Into Umbra", spirit=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)

effect_summon_spirit_minor = Effect.objects.get_or_create(
    name="Summon Spirit (Minor)", spirit=2
)[0].add_source("How Do You Do That", 148)

effect_summon_spirit_powerful = Effect.objects.get_or_create(
    name="Summon Spirit (Powerful)", spirit=3
)[0].add_source("How Do You Do That", 148)

effect_bind_spirit = Effect.objects.get_or_create(name="Bind Spirit", spirit=4)[
    0
].add_source("How Do You Do That", 148)

effect_create_spirit_gate = Effect.objects.get_or_create(
    name="Create Spirit Gate", spirit=4, prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)

# effect_create_fetish = # Effect.objects.get_or_create(name="Create Fetish", spirit=4, prime=2)[0].add_source(
#     "Mage: The Ascension 20th Anniversary Edition", 521
# )
# )

effect_strengthen_weaken_gauntlet = Effect.objects.get_or_create(
    name="Strengthen/Weaken Gauntlet", spirit=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)

effect_create_spirit = Effect.objects.get_or_create(
    name="Create Spirit", spirit=5, prime=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)

effect_permanently_destroy_spirit = Effect.objects.get_or_create(
    name="Permanently Destroy Spirit", spirit=5, prime=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)

# ===== CROSS-SPLAT EFFECTS =====
effect_break_blood_bond = Effect.objects.get_or_create(
    name="Break Blood Bond", life=4, mind=3, entropy=3, prime=1
)[0].add_source("Book of Secrets", 86)

effect_harm_vampire = Effect.objects.get_or_create(
    name="Harm Vampire", life=3, matter=2
)[0].add_source("Gods & Monsters", 58)

effect_heal_vampire = Effect.objects.get_or_create(
    name="Heal Vampire", life=3, matter=2
)[0].add_source("Gods & Monsters", 58)

effect_harm_werewolf = Effect.objects.get_or_create(
    name="Harm Werewolf", life=3, spirit=3
)[0].add_source("Gods & Monsters", 75)

effect_heal_werewolf = Effect.objects.get_or_create(
    name="Heal Werewolf", life=3, spirit=2
)[0].add_source("Gods & Monsters", 75)

effect_harm_fae = Effect.objects.get_or_create(name="Harm Fae", life=3, mind=3)[
    0
].add_source("Gods & Monsters", 104)

effect_heal_fae = Effect.objects.get_or_create(name="Heal Fae", life=3, mind=3)[
    0
].add_source("Gods & Monsters", 104)

effect_counter_fae_glamour = Effect.objects.get_or_create(
    name="Counter Fae Glamour", prime=2, mind=2
)[0].add_source("Gods & Monsters", 104)

effect_harm_ghost = Effect.objects.get_or_create(name="Harm Ghost", prime=2, entropy=3)[
    0
].add_source("Gods & Monsters", 120)

effect_strengthen_ghost = Effect.objects.get_or_create(
    name="Strengthen Ghost", spirit=3, prime=2
)[0].add_source("Gods & Monsters", 120)

# ===== PARADIGM-SPECIFIC EFFECTS =====
# Akashic Brotherhood
effect_do_strike_akashic = Effect.objects.get_or_create(
    name="Do Strike (Akashic)", life=2, mind=1, prime=1
)[0].add_source("Lore of the Traditions", 28)

effect_dragon_pearl_meditation = Effect.objects.get_or_create(
    name="Dragon Pearl Meditation", prime=3, mind=2
)[0].add_source("Lore of the Traditions", 28)

effect_chi_healing = Effect.objects.get_or_create(name="Chi Healing", life=3, prime=1)[
    0
].add_source("Lore of the Traditions", 28)

# Celestial Chorus
effect_holy_fire = Effect.objects.get_or_create(name="Holy Fire", forces=3, prime=2)[
    0
].add_source("Lore of the Traditions", 48)

effect_blessing_of_the_one = Effect.objects.get_or_create(
    name="Blessing of the One", prime=2, mind=2, life=1
)[0].add_source("Lore of the Traditions", 48)

effect_call_divine_intervention = Effect.objects.get_or_create(
    name="Call Divine Intervention", prime=4, spirit=3
)[0].add_source("Lore of the Traditions", 48)

# Cult of Ecstasy
effect_temporal_fugue = Effect.objects.get_or_create(
    name="Temporal Fugue", time=3, mind=2
)[0].add_source("Lore of the Traditions", 68)

effect_ecstatic_vision = Effect.objects.get_or_create(
    name="Ecstatic Vision", mind=2, time=1
)[0].add_source("Lore of the Traditions", 68)

# Dreamspeakers
# effect_spirit_journey = # Effect.objects.get_or_create(name="Spirit Journey", spirit=3, mind=1)[0].add_source(
#     "Lore of the Traditions", 88
# )
# )

effect_call_totem_spirit = Effect.objects.get_or_create(
    name="Call Totem Spirit", spirit=4
)[0].add_source("Lore of the Traditions", 88)

effect_medicine_work_healing = Effect.objects.get_or_create(
    name="Medicine Work Healing", life=3, spirit=1
)[0].add_source("Lore of the Traditions", 88)

# Euthanatos
effect_good_death = Effect.objects.get_or_create(
    name="Good Death", entropy=3, life=3, spirit=2
)[0].add_source("Lore of the Traditions", 108)

effect_wheel_of_fate = Effect.objects.get_or_create(
    name="Wheel of Fate", entropy=4, time=2
)[0].add_source("Lore of the Traditions", 108)

# Order of Hermes
effect_hermetic_circle_of_protection = Effect.objects.get_or_create(
    name="Hermetic Circle of Protection", prime=2, forces=2, mind=1
)[0].add_source("Lore of the Traditions", 128)

effect_summon_elemental = Effect.objects.get_or_create(
    name="Summon Elemental", forces=4, spirit=3, prime=2
)[0].add_source("Lore of the Traditions", 128)

effect_alchemical_transmutation = Effect.objects.get_or_create(
    name="Alchemical Transmutation", matter=3, prime=2
)[0].add_source("Lore of the Traditions", 128)

# Sons of Ether
effect_ether_ray = Effect.objects.get_or_create(
    name="Ether Ray", forces=3, matter=2, prime=1
)[0].add_source("Lore of the Traditions", 148)

effect_dimensional_portal_device = Effect.objects.get_or_create(
    name="Dimensional Portal Device", correspondence=4, matter=3, prime=2
)[0].add_source("Lore of the Traditions", 148)

# Verbena
effect_blood_magic_ritual = Effect.objects.get_or_create(
    name="Blood Magic Ritual", life=3, prime=2
)[0].add_source("Lore of the Traditions", 168)

effect_primal_transformation = Effect.objects.get_or_create(
    name="Primal Transformation", life=4, spirit=2
)[0].add_source("Lore of the Traditions", 168)

effect_call_the_wild_hunt = Effect.objects.get_or_create(
    name="Call the Wild Hunt", spirit=4, life=2, mind=2
)[0].add_source("Lore of the Traditions", 168)

# Virtual Adepts
effect_reality_hack = Effect.objects.get_or_create(
    name="Reality Hack", correspondence=3, forces=2, prime=1
)[0].add_source("Lore of the Traditions", 188)

effect_digital_avatar = Effect.objects.get_or_create(
    name="Digital Avatar", correspondence=3, mind=3, prime=2
)[0].add_source("Lore of the Traditions", 188)

effect_information_overload = Effect.objects.get_or_create(
    name="Information Overload", forces=3, mind=3, correspondence=2
)[0].add_source("Lore of the Traditions", 188)

# ===== TECHNOCRATIC PROCEDURES =====
effect_hit_mark_activation_primium_construct = Effect.objects.get_or_create(
    name="HIT Mark Activation (Primium Construct)", matter=4, life=2, prime=3
)[0].add_source("Technocracy Reloaded", 201)

effect_mind_wipe_flashy_thing = Effect.objects.get_or_create(
    name="Mind Wipe (Flashy Thing)", mind=3
)[0].add_source("Technocracy Reloaded", 225)

effect_biometric_scan = Effect.objects.get_or_create(
    name="Biometric Scan", life=2, correspondence=1
)[0].add_source("Technocracy Reloaded", 216)

effect_genetic_modification = Effect.objects.get_or_create(
    name="Genetic Modification", life=4, matter=2, prime=2
)[0].add_source("Technocracy Reloaded", 158)

effect_dimensional_backdoor = Effect.objects.get_or_create(
    name="Dimensional Backdoor", correspondence=4, spirit=5
)[0].add_source("Technocracy Reloaded", 227)

effect_paws_taser_anti_shapeshifter = Effect.objects.get_or_create(
    name="PAWS Taser (Anti-Shapeshifter)", forces=3, life=4, spirit=3, prime=2
)[0].add_source("Technocracy Reloaded", 224)

effect_sleepteacher_accelerated_learning = Effect.objects.get_or_create(
    name="Sleepteacher Accelerated Learning", mind=3, time=2
)[0].add_source("Technocracy Reloaded", 230)

# ===== NEPHANDI/MARAUDER EFFECTS =====
effect_infernal_pact = Effect.objects.get_or_create(
    name="Infernal Pact", prime=4, spirit=4, entropy=3
)[0].add_source("Book of the Fallen", 145)

effect_corrupt_pattern = Effect.objects.get_or_create(
    name="Corrupt Pattern", entropy=4, life=3, prime=2
)[0].add_source("Book of the Fallen", 148)

effect_summon_demon = Effect.objects.get_or_create(
    name="Summon Demon", spirit=4, prime=3, entropy=2
)[0].add_source("Book of the Fallen", 150)

effect_reality_cancer = Effect.objects.get_or_create(
    name="Reality Cancer", prime=5, entropy=5
)[0].add_source("Book of the Fallen", 155)

# ===== UTILITY & MISCELLANEOUS =====
effect_permanent_enchantment = Effect.objects.get_or_create(
    name="Permanent Enchantment", prime=5
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 520)

effect_counterspell_basic = Effect.objects.get_or_create(
    name="Counterspell (Basic)", prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 542)

effect_counterspell_advanced = Effect.objects.get_or_create(
    name="Counterspell (Advanced)", prime=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 542)

effect_dispel_paradox = Effect.objects.get_or_create(
    name="Dispel Paradox", prime=3, entropy=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 548)

effect_absorb_quintessence_from_living = Effect.objects.get_or_create(
    name="Absorb Quintessence from Living", prime=5, life=3
)[0].add_source("Book of Secrets", 102)

effect_create_horizon_realm = Effect.objects.get_or_create(
    name="Create Horizon Realm", correspondence=5, spirit=5, prime=5
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 612)

effect_ward_against_scrying = Effect.objects.get_or_create(
    name="Ward Against Scrying", correspondence=3, mind=2, prime=1
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 515)

effect_ward_against_spirits = Effect.objects.get_or_create(
    name="Ward Against Spirits", spirit=3, prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)

effect_mass_teleportation = Effect.objects.get_or_create(
    name="Mass Teleportation", correspondence=5, life=3, mind=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 515)

effect_destroy_pattern_permanently = Effect.objects.get_or_create(
    name="Destroy Pattern Permanently", prime=5, entropy=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 520)

# Effects from mage_advanced_effects.py
effect_summon_ghost = Effect.objects.get_or_create(name="Summon Ghost", spirit=2)[
    0
].add_source("How Do You Do That", 142)
effect_summon_powerful_ghost = Effect.objects.get_or_create(
    name="Summon Powerful Ghost", spirit=3
)[0].add_source("How Do You Do That", 142)
effect_see_into_shadowlands = Effect.objects.get_or_create(
    name="See Into Shadowlands", spirit=1, entropy=1
)[0].add_source("How Do You Do That", 142)
effect_step_sideways_to_shadowlands = Effect.objects.get_or_create(
    name="Step Sideways to Shadowlands", spirit=3
)[0].add_source("How Do You Do That", 142)
effect_speak_with_dead = Effect.objects.get_or_create(
    name="Speak with Dead", spirit=2, mind=1
)[0].add_source("How Do You Do That", 142)
effect_bind_ghost = Effect.objects.get_or_create(name="Bind Ghost", spirit=4)[
    0
].add_source("How Do You Do That", 143)
effect_banish_ghost = Effect.objects.get_or_create(
    name="Banish Ghost", spirit=3, prime=2
)[0].add_source("How Do You Do That", 143)
effect_create_zombie_simple = Effect.objects.get_or_create(
    name="Create Zombie (Simple)", life=3, matter=2, prime=2
)[0].add_source("How Do You Do That", 144)
effect_create_zombie_complex = Effect.objects.get_or_create(
    name="Create Zombie (Complex)", life=4, matter=2, prime=2, mind=1
)[0].add_source("How Do You Do That", 144)
effect_restore_recently_dead_to_life = Effect.objects.get_or_create(
    name="Restore Recently Dead to Life", life=5, prime=2, spirit=4
)[0].add_source("How Do You Do That", 145)
effect_restore_long_dead_to_life = Effect.objects.get_or_create(
    name="Restore Long Dead to Life", life=5, prime=3, spirit=5, time=3
)[0].add_source("How Do You Do That", 145)
effect_create_lich_self = Effect.objects.get_or_create(
    name="Create Lich (Self)", life=5, spirit=4, prime=3, entropy=3
)[0].add_source("How Do You Do That", 146)
effect_sense_time_flow = Effect.objects.get_or_create(name="Sense Time Flow", time=1)[
    0
].add_source("How Do You Do That", 154)
effect_see_past_recent = Effect.objects.get_or_create(name="See Past (Recent)", time=2)[
    0
].add_source("How Do You Do That", 154)
effect_see_future_near = Effect.objects.get_or_create(name="See Future (Near)", time=2)[
    0
].add_source("How Do You Do That", 154)
effect_see_past_distant = Effect.objects.get_or_create(
    name="See Past (Distant)", time=3, correspondence=2
)[0].add_source("How Do You Do That", 154)
effect_see_future_distant = Effect.objects.get_or_create(
    name="See Future (Distant)", time=3
)[0].add_source("How Do You Do That", 154)
effect_slow_time_local = Effect.objects.get_or_create(name="Slow Time (Local)", time=3)[
    0
].add_source("How Do You Do That", 155)
effect_speed_time_local = Effect.objects.get_or_create(
    name="Speed Time (Local)", time=3
)[0].add_source("How Do You Do That", 155)
effect_freeze_time_small_area = Effect.objects.get_or_create(
    name="Freeze Time (Small Area)", time=4
)[0].add_source("How Do You Do That", 155)
effect_rewind_time_seconds = Effect.objects.get_or_create(
    name="Rewind Time (Seconds)", time=5, prime=2
)[0].add_source("How Do You Do That", 156)
effect_travel_through_time = Effect.objects.get_or_create(
    name="Travel Through Time", time=5, spirit=4, prime=3
)[0].add_source("How Do You Do That", 156)
effect_create_time_loop = Effect.objects.get_or_create(
    name="Create Time Loop", time=4, prime=2
)[0].add_source("How Do You Do That", 156)
effect_co_location_be_in_two_places = Effect.objects.get_or_create(
    name="Co-Location (Be In Two Places)", correspondence=5, life=3, mind=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 515)
effect_fold_space = Effect.objects.get_or_create(name="Fold Space", correspondence=5)[
    0
].add_source("Mage: The Ascension 20th Anniversary Edition", 515)
effect_ward_against_teleportation = Effect.objects.get_or_create(
    name="Ward Against Teleportation", correspondence=3, prime=2
)[0].add_source("How Do You Do That", 128)
effect_shapeshift_into_hybrid_form = Effect.objects.get_or_create(
    name="Shapeshift into Hybrid Form", life=4, prime=2
)[0].add_source("How Do You Do That", 34)
effect_create_homunculus = Effect.objects.get_or_create(
    name="Create Homunculus", life=5, prime=3, mind=2
)[0].add_source("Book of Secrets", 79)
effect_clone_body = Effect.objects.get_or_create(
    name="Clone Body", life=5, prime=2, mind=1
)[0].add_source("Book of Secrets", 79)
effect_enhance_physical_attribute_permanent = Effect.objects.get_or_create(
    name="Enhance Physical Attribute (Permanent)", life=4, prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)
effect_grant_regeneration = Effect.objects.get_or_create(
    name="Grant Regeneration", life=4, prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)
effect_age_de_age_target = Effect.objects.get_or_create(
    name="Age/De-Age Target", life=4, time=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)
effect_cure_poison_disease_aggravated = Effect.objects.get_or_create(
    name="Cure Poison/Disease (Aggravated)", life=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)
effect_read_deep_thoughts_memories = Effect.objects.get_or_create(
    name="Read Deep Thoughts/Memories", mind=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 519)
effect_implant_false_memory = Effect.objects.get_or_create(
    name="Implant False Memory", mind=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 519)
effect_mind_control_simple_command = Effect.objects.get_or_create(
    name="Mind Control (Simple Command)", mind=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 519)
effect_astral_quest = Effect.objects.get_or_create(
    name="Astral Quest", mind=5, spirit=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 519)
effect_shatter_mind = Effect.objects.get_or_create(name="Shatter Mind", mind=5)[
    0
].add_source("Mage: The Ascension 20th Anniversary Edition", 519)
effect_create_permanent_mental_illusion = Effect.objects.get_or_create(
    name="Create Permanent Mental Illusion", mind=4, prime=2
)[0].add_source("How Do You Do That", 162)
effect_mass_telepathy = Effect.objects.get_or_create(
    name="Mass Telepathy", mind=3, correspondence=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 519)
effect_laser_blast = Effect.objects.get_or_create(
    name="Laser Blast", forces=3, matter=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 517)
effect_emp_pulse = Effect.objects.get_or_create(name="EMP Pulse", forces=3, matter=2)[
    0
].add_source("Mage: The Ascension 20th Anniversary Edition", 517)
effect_nuclear_blast = Effect.objects.get_or_create(
    name="Nuclear Blast", forces=5, prime=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 517)
effect_transmute_base_metals_to_gold = Effect.objects.get_or_create(
    name="Transmute Base Metals to Gold", matter=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)
effect_create_matter_from_nothing = Effect.objects.get_or_create(
    name="Create Matter from Nothing", matter=4, prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)
effect_phase_through_matter = Effect.objects.get_or_create(
    name="Phase Through Matter", matter=3, life=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)
effect_turn_to_stone = Effect.objects.get_or_create(
    name="Turn to Stone", matter=3, life=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 518)
effect_age_object_rapidly = Effect.objects.get_or_create(
    name="Age Object Rapidly", entropy=3, time=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 516)
effect_rot_living_being = Effect.objects.get_or_create(
    name="Rot Living Being", entropy=4, life=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 516)
effect_shatter_pattern = Effect.objects.get_or_create(
    name="Shatter Pattern", entropy=5, prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 516)
effect_control_probability_major = Effect.objects.get_or_create(
    name="Control Probability (Major)", entropy=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 516)
effect_enchant_talisman = Effect.objects.get_or_create(
    name="Enchant Talisman", prime=3
)[0].add_source("Book of Secrets", 82)
effect_disenchant_wonder = Effect.objects.get_or_create(
    name="Disenchant Wonder", prime=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 520)
effect_nullify_magic = Effect.objects.get_or_create(name="Nullify Magic", prime=3)[
    0
].add_source("Mage: The Ascension 20th Anniversary Edition", 520)
effect_permanently_enhance_pattern = Effect.objects.get_or_create(
    name="Permanently Enhance Pattern", prime=5
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 520)
effect_fuel_pattern_with_quintessence = Effect.objects.get_or_create(
    name="Fuel Pattern with Quintessence", prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 520)
effect_create_tass = Effect.objects.get_or_create(name="Create Tass", prime=3)[
    0
].add_source("Mage: The Ascension 20th Anniversary Edition", 520)
effect_open_seal_node = Effect.objects.get_or_create(
    name="Open/Seal Node", prime=4, spirit=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 520)
effect_touch_spirit_matter = Effect.objects.get_or_create(
    name="Touch Spirit Matter", spirit=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)
effect_step_sideways_to_umbra = Effect.objects.get_or_create(
    name="Step Sideways to Umbra", spirit=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)
effect_reach_into_umbra = Effect.objects.get_or_create(
    name="Reach Into Umbra", spirit=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)
effect_summon_spirit_minor = Effect.objects.get_or_create(
    name="Summon Spirit (Minor)", spirit=2
)[0].add_source("How Do You Do That", 148)
effect_summon_spirit_powerful = Effect.objects.get_or_create(
    name="Summon Spirit (Powerful)", spirit=3
)[0].add_source("How Do You Do That", 148)
effect_bind_spirit = Effect.objects.get_or_create(name="Bind Spirit", spirit=4)[
    0
].add_source("How Do You Do That", 148)
effect_create_spirit_gate = Effect.objects.get_or_create(
    name="Create Spirit Gate", spirit=4, prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)
effect_strengthen_weaken_gauntlet = Effect.objects.get_or_create(
    name="Strengthen/Weaken Gauntlet", spirit=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)
effect_create_spirit = Effect.objects.get_or_create(
    name="Create Spirit", spirit=5, prime=4
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)
effect_permanently_destroy_spirit = Effect.objects.get_or_create(
    name="Permanently Destroy Spirit", spirit=5, prime=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)
effect_break_blood_bond = Effect.objects.get_or_create(
    name="Break Blood Bond", life=4, mind=3, entropy=3, prime=1
)[0].add_source("Book of Secrets", 86)
effect_harm_werewolf = Effect.objects.get_or_create(
    name="Harm Werewolf", life=3, spirit=3
)[0].add_source("Gods & Monsters", 75)
effect_heal_werewolf = Effect.objects.get_or_create(
    name="Heal Werewolf", life=3, spirit=2
)[0].add_source("Gods & Monsters", 75)
effect_counter_fae_glamour = Effect.objects.get_or_create(
    name="Counter Fae Glamour", prime=2, mind=2
)[0].add_source("Gods & Monsters", 104)
effect_strengthen_ghost = Effect.objects.get_or_create(
    name="Strengthen Ghost", spirit=3, prime=2
)[0].add_source("Gods & Monsters", 120)
effect_do_strike_akashic = Effect.objects.get_or_create(
    name="Do Strike (Akashic)", life=2, mind=1, prime=1
)[0].add_source("Lore of the Traditions", 28)
effect_dragon_pearl_meditation = Effect.objects.get_or_create(
    name="Dragon Pearl Meditation", prime=3, mind=2
)[0].add_source("Lore of the Traditions", 28)
effect_chi_healing = Effect.objects.get_or_create(name="Chi Healing", life=3, prime=1)[
    0
].add_source("Lore of the Traditions", 28)
effect_blessing_of_the_one = Effect.objects.get_or_create(
    name="Blessing of the One", prime=2, mind=2, life=1
)[0].add_source("Lore of the Traditions", 48)
effect_call_divine_intervention = Effect.objects.get_or_create(
    name="Call Divine Intervention", prime=4, spirit=3
)[0].add_source("Lore of the Traditions", 48)
effect_ecstatic_vision = Effect.objects.get_or_create(
    name="Ecstatic Vision", mind=2, time=1
)[0].add_source("Lore of the Traditions", 68)
effect_call_totem_spirit = Effect.objects.get_or_create(
    name="Call Totem Spirit", spirit=4
)[0].add_source("Lore of the Traditions", 88)
effect_medicine_work_healing = Effect.objects.get_or_create(
    name="Medicine Work Healing", life=3, spirit=1
)[0].add_source("Lore of the Traditions", 88)
effect_good_death = Effect.objects.get_or_create(
    name="Good Death", entropy=3, life=3, spirit=2
)[0].add_source("Lore of the Traditions", 108)
effect_wheel_of_fate = Effect.objects.get_or_create(
    name="Wheel of Fate", entropy=4, time=2
)[0].add_source("Lore of the Traditions", 108)
effect_hermetic_circle_of_protection = Effect.objects.get_or_create(
    name="Hermetic Circle of Protection", prime=2, forces=2, mind=1
)[0].add_source("Lore of the Traditions", 128)
effect_summon_elemental = Effect.objects.get_or_create(
    name="Summon Elemental", forces=4, spirit=3, prime=2
)[0].add_source("Lore of the Traditions", 128)
effect_alchemical_transmutation = Effect.objects.get_or_create(
    name="Alchemical Transmutation", matter=3, prime=2
)[0].add_source("Lore of the Traditions", 128)
effect_ether_ray = Effect.objects.get_or_create(
    name="Ether Ray", forces=3, matter=2, prime=1
)[0].add_source("Lore of the Traditions", 148)
effect_dimensional_portal_device = Effect.objects.get_or_create(
    name="Dimensional Portal Device", correspondence=4, matter=3, prime=2
)[0].add_source("Lore of the Traditions", 148)
effect_blood_magic_ritual = Effect.objects.get_or_create(
    name="Blood Magic Ritual", life=3, prime=2
)[0].add_source("Lore of the Traditions", 168)
effect_primal_transformation = Effect.objects.get_or_create(
    name="Primal Transformation", life=4, spirit=2
)[0].add_source("Lore of the Traditions", 168)
effect_call_the_wild_hunt = Effect.objects.get_or_create(
    name="Call the Wild Hunt", spirit=4, life=2, mind=2
)[0].add_source("Lore of the Traditions", 168)
effect_reality_hack = Effect.objects.get_or_create(
    name="Reality Hack", correspondence=3, forces=2, prime=1
)[0].add_source("Lore of the Traditions", 188)
effect_digital_avatar = Effect.objects.get_or_create(
    name="Digital Avatar", correspondence=3, mind=3, prime=2
)[0].add_source("Lore of the Traditions", 188)
effect_hit_mark_activation_primium_construct = Effect.objects.get_or_create(
    name="HIT Mark Activation (Primium Construct)", matter=4, life=2, prime=3
)[0].add_source("Technocracy Reloaded", 201)
effect_mind_wipe_flashy_thing = Effect.objects.get_or_create(
    name="Mind Wipe (Flashy Thing)", mind=3
)[0].add_source("Technocracy Reloaded", 225)
effect_biometric_scan = Effect.objects.get_or_create(
    name="Biometric Scan", life=2, correspondence=1
)[0].add_source("Technocracy Reloaded", 216)
effect_genetic_modification = Effect.objects.get_or_create(
    name="Genetic Modification", life=4, matter=2, prime=2
)[0].add_source("Technocracy Reloaded", 158)
effect_dimensional_backdoor = Effect.objects.get_or_create(
    name="Dimensional Backdoor", correspondence=4, spirit=5
)[0].add_source("Technocracy Reloaded", 227)
effect_paws_taser_anti_shapeshifter = Effect.objects.get_or_create(
    name="PAWS Taser (Anti-Shapeshifter)", forces=3, life=4, spirit=3, prime=2
)[0].add_source("Technocracy Reloaded", 224)
effect_sleepteacher_accelerated_learning = Effect.objects.get_or_create(
    name="Sleepteacher Accelerated Learning", mind=3, time=2
)[0].add_source("Technocracy Reloaded", 230)
effect_infernal_pact = Effect.objects.get_or_create(
    name="Infernal Pact", prime=4, spirit=4, entropy=3
)[0].add_source("Book of the Fallen", 145)
effect_corrupt_pattern = Effect.objects.get_or_create(
    name="Corrupt Pattern", entropy=4, life=3, prime=2
)[0].add_source("Book of the Fallen", 148)
effect_summon_demon = Effect.objects.get_or_create(
    name="Summon Demon", spirit=4, prime=3, entropy=2
)[0].add_source("Book of the Fallen", 150)
effect_reality_cancer = Effect.objects.get_or_create(
    name="Reality Cancer", prime=5, entropy=5
)[0].add_source("Book of the Fallen", 155)
effect_permanent_enchantment = Effect.objects.get_or_create(
    name="Permanent Enchantment", prime=5
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 520)
effect_counterspell_basic = Effect.objects.get_or_create(
    name="Counterspell (Basic)", prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 542)
effect_counterspell_advanced = Effect.objects.get_or_create(
    name="Counterspell (Advanced)", prime=3
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 542)
effect_dispel_paradox = Effect.objects.get_or_create(
    name="Dispel Paradox", prime=3, entropy=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 548)
effect_absorb_quintessence_from_living = Effect.objects.get_or_create(
    name="Absorb Quintessence from Living", prime=5, life=3
)[0].add_source("Book of Secrets", 102)
effect_create_horizon_realm = Effect.objects.get_or_create(
    name="Create Horizon Realm", correspondence=5, spirit=5, prime=5
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 612)
effect_ward_against_scrying = Effect.objects.get_or_create(
    name="Ward Against Scrying", correspondence=3, mind=2, prime=1
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 515)
effect_ward_against_spirits = Effect.objects.get_or_create(
    name="Ward Against Spirits", spirit=3, prime=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 521)
effect_mass_teleportation = Effect.objects.get_or_create(
    name="Mass Teleportation", correspondence=5, life=3, mind=2
)[0].add_source("Mage: The Ascension 20th Anniversary Edition", 515)

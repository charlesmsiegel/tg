from characters.models.vampire.discipline import Discipline

# Physical Disciplines

celerity = Discipline.objects.get_or_create(
    name="Celerity",
    description="Supernatural speed. Each dot can add to Dexterity, allow splitting dice for "
    "multiple actions, or grant extra actions. Cost: 1 blood point per turn."
)[0]

fortitude = Discipline.objects.get_or_create(
    name="Fortitude",
    description="Supernatural toughness. Add dots to soak rolls, can even soak aggravated damage. "
    "No cost; always active."
)[0]

potence = Discipline.objects.get_or_create(
    name="Potence",
    description="Supernatural strength. Add dots to Strength damage rolls. "
    "No cost; always active."
)[0]

# Mental Disciplines

auspex = Discipline.objects.get_or_create(
    name="Auspex",
    description="Heightened senses and ESP. Powers include Heightened Senses, Aura Perception, "
    "The Spirit's Touch, Telepathy, and Psychic Projection."
)[0]

dominate = Discipline.objects.get_or_create(
    name="Dominate",
    description="Mind control. Powers include Command, Mesmerize, The Forgetful Mind, "
    "Conditioning, and Possession. Typically requires eye contact except at higher levels."
)[0]

dementation = Discipline.objects.get_or_create(
    name="Dementation",
    description="Madness manipulation. Powers include Passion, Haunting, Eyes of Chaos, "
    "Confusion, and Total Insanity. Malkavian-specific alternative to Dominate."
)[0]

# Social Disciplines

presence = Discipline.objects.get_or_create(
    name="Presence",
    description="Emotional manipulation. Powers include Awe, Dread Gaze, Entrancement, "
    "Summon, and Majesty. Does not require eye contact and can affect groups."
)[0]

# Animalistic Disciplines

animalism = Discipline.objects.get_or_create(
    name="Animalism",
    description="Control over animals. Powers include Feral Whispers, Beckoning, "
    "Subsume the Spirit, Commanding the Beast, and Drawing Out the Beast."
)[0]

protean = Discipline.objects.get_or_create(
    name="Protean",
    description="Shapeshifting. Powers include Eyes of the Beast, Feral Claws, Earth Meld, "
    "Shape of the Beast (wolf or bat), and Mist Form."
)[0]

# Stealth Disciplines

obfuscate = Discipline.objects.get_or_create(
    name="Obfuscate",
    description="Invisibility and disguise. Powers include Cloak of Shadows, Unseen Presence, "
    "Mask of a Thousand Faces, Vanish from Mind's Eye, and Cloak the Gathering. "
    "Broken by attacking or drawing attention."
)[0]

# Unique Clan Disciplines

chimerstry = Discipline.objects.get_or_create(
    name="Chimerstry",
    description="Illusion creation (Ravnos). Powers include Ignis Fatuus, Fata Morgana, "
    "Apparition, Permanency, and Horrid Reality."
)[0]

necromancy = Discipline.objects.get_or_create(
    name="Necromancy",
    description="Command the dead (Giovanni). Multiple Paths including Sepulchre Path, "
    "Bone Path, Ash Path, and Corpse in the Monster. Separate rituals like Thaumaturgy. "
    "Roll: Perception + Occult."
)[0]

obtenebration = Discipline.objects.get_or_create(
    name="Obtenebration",
    description="Shadow manipulation (Lasombra). Powers include Shadow Play, Shroud of Night, "
    "Arms of the Abyss, Black Metamorphosis, and Tenebrous Form."
)[0]

quietus = Discipline.objects.get_or_create(
    name="Quietus",
    description="Assassin arts (Assamite). Powers include Silence of Death, Scorpion's Touch, "
    "Dagon's Call, Baal's Caress, and Taste of Death."
)[0]

serpentis = Discipline.objects.get_or_create(
    name="Serpentis",
    description="Serpent powers (Followers of Set). Powers include Eyes of the Serpent, "
    "Tongue of the Asp, Mummify (remove heart), Form of the Cobra, and Heart of Darkness."
)[0]

thaumaturgy = Discipline.objects.get_or_create(
    name="Thaumaturgy",
    description="Blood magic (Tremere). Multiple Paths including Path of Blood, Lure of Flames, "
    "Movement of the Mind, and others. Rituals at levels 1-5. Primary Path advances automatically. "
    "Roll: Willpower (difficulty varies)."
)[0]

vicissitude = Discipline.objects.get_or_create(
    name="Vicissitude",
    description="Fleshcrafting (Tzimisce). Powers include Malleable Visage, Fleshcraft, "
    "Bonecraft, Horrid Form, and Bloodform. Can reshape flesh and bone of self or others."
)[0]

# Bloodline Unique Disciplines

daimoinon = Discipline.objects.get_or_create(
    name="Daimoinon",
    description="Demonic powers (Baali). Summon demons, cause corruption, and perform dark miracles."
)[0]

melpominee = Discipline.objects.get_or_create(
    name="Melpominee",
    description="Voice powers (Daughters of Cacophony). Sonic attacks, vocal manipulation, "
    "and supernatural singing."
)[0]

mytherceria = Discipline.objects.get_or_create(
    name="Mytherceria",
    description="Fae magic (Kiasyd). Fae-touched illusions and enchantments derived from "
    "the mixing of vampire vitae with fae essence."
)[0]

obeah = Discipline.objects.get_or_create(
    name="Obeah",
    description="Healing arts (Salubri Healers). Supernatural healing and restoration. "
    "One of the rarest Disciplines, possessed by the nearly extinct Salubri."
)[0]

temporis = Discipline.objects.get_or_create(
    name="Temporis",
    description="Time control (True Brujah). Manipulate time and perception. "
    "Includes temporal phasing effects."
)[0]

thanatosis = Discipline.objects.get_or_create(
    name="Thanatosis",
    description="Death feigning (Samedi). Appear dead, animate corpses, and control putrefaction."
)[0]

valeren = Discipline.objects.get_or_create(
    name="Valeren",
    description="Combat arts (Salubri Warriors). Supernatural combat abilities and protection. "
    "The warrior aspect of Salubri powers."
)[0]

visceratika = Discipline.objects.get_or_create(
    name="Visceratika",
    description="Stone shaping (Gargoyles). Stone skin, earth melding, and gargoyle-specific "
    "abilities derived from their Tremere creation."
)[0]

# Flight is a special Discipline for Gargoyles
flight = Discipline.objects.get_or_create(
    name="Flight",
    description="Supernatural flight (Gargoyles). All Gargoyle variants possess this ability. "
    "Wings required as psychological focus."
)[0]

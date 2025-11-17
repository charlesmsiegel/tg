from characters.models.wraith.thorn import Thorn

# Individual Thorns (1-3 Point Range)

Thorn.objects.get_or_create(
    name="Spectre Prestige",
    defaults={
        "thorn_type": "individual",
        "point_cost": 1,
        "activation_cost": "None (always active)",
        "activation_trigger": "Automatic",
        "mechanical_description": "Shadows communicate with Spectres; garnered respect. Can purchase multiple levels.",
        "resistance_system": "None",
        "duration": "Permanent",
        "frequency_limitation": "Cannot exceed character's Shadow purchase limits",
        "limitations": "Passive social effect only",
    }
)[0]

Thorn.objects.get_or_create(
    name="Dark Allies",
    defaults={
        "thorn_type": "individual",
        "point_cost": 1,
        "activation_cost": "None (always active)",
        "activation_trigger": "Can call for aid",
        "mechanical_description": "Shadow regularly communicates with Spectres; can call for aid. Each level increases network.",
        "resistance_system": "None",
        "duration": "Permanent (on-call aid)",
        "frequency_limitation": "Aid is Storyteller discretion",
        "limitations": "Different from Pact of Doom - relationship-based rather than transaction-based",
    }
)[0]

Thorn.objects.get_or_create(
    name="Tainted Relic",
    defaults={
        "thorn_type": "individual",
        "point_cost": 1,
        "activation_cost": "Automatic during Catharsis",
        "activation_trigger": "Whenever Shadow dominates",
        "mechanical_description": "Relic manifests only during Catharsis; even if lost or destroyed returns on Shadow dominance; potency = points invested",
        "resistance_system": "None (always manifests with Shadow)",
        "duration": "Scene (Catharsis duration)",
        "frequency_limitation": "Manifests in all Catharsis events",
        "limitations": "Relic always has significance to Psyche; manifests in all Catharsis",
    }
)[0]

Thorn.objects.get_or_create(
    name="Infamy",
    defaults={
        "thorn_type": "individual",
        "point_cost": 1,
        "activation_cost": "Automatic on Slumber",
        "activation_trigger": "Each Slumber triggers Angst gain",
        "mechanical_description": "Measures fear/loathing Shadow inspires in living. Shadowguide rolls 1 die per Infamy point (difficulty 6); each success = 1 temporary Angst; botch = temporary Angst lost",
        "resistance_system": "None (automatic mechanism)",
        "resistance_difficulty": 6,
        "duration": "Per Slumber cycle (recovers permanently next Slumber)",
        "frequency_limitation": "Maximum 5 points total",
        "limitations": "Infamous wraiths face social consequences from living world",
    }
)[0]

Thorn.objects.get_or_create(
    name="Death's Sigil",
    defaults={
        "thorn_type": "individual",
        "point_cost": 1,
        "activation_cost": "1 Willpower/scene to suppress",
        "activation_trigger": "Always active (can suppress)",
        "mechanical_description": "Manifestation of Oblivion's mark; unique to each wraith. Examples: wings of choking smoke, seawater footprints, burned flesh odor. 3-point version may alter Arcanos effects.",
        "resistance_system": "1 Willpower point to suppress for one scene (player choice)",
        "duration": "Permanent/Passive until suppressed",
        "frequency_limitation": "None",
        "limitations": "Makes wraith highly distinctive (advantages and disadvantages)",
    }
)[0]

Thorn.objects.get_or_create(
    name="Shadow Traits",
    defaults={
        "thorn_type": "individual",
        "point_cost": 2,
        "activation_cost": "Only available during Catharsis",
        "activation_trigger": "When Shadow controls Corpus",
        "mechanical_description": "Grants +1 dot in any Attribute or Ability. Can be purchased multiple times (limited by freebie points available). Each purchase adds one additional dot to same or different trait.",
        "resistance_system": "None",
        "duration": "Catharsis scene only",
        "frequency_limitation": "Stackable purchases",
        "limitations": "Only usable when Shadow controls Corpus",
    }
)[0]

Thorn.objects.get_or_create(
    name="Nightmares",
    defaults={
        "thorn_type": "individual",
        "point_cost": 2,
        "activation_cost": "1 Angst to activate",
        "activation_trigger": "When Psyche enters Slumber",
        "mechanical_description": "Shadow causes intense nightmares; wraith must roll Willpower (difficulty 6) or immediately awaken and lose all Slumber benefits",
        "resistance_system": "1 Willpower point spent before Slumber = immunity for that Slumber (Storyteller only knows)",
        "resistance_difficulty": 6,
        "duration": "One Slumber period",
        "frequency_limitation": "Costs 1 Angst per use",
        "limitations": "Defensive Willpower negates entirely",
    }
)[0]

Thorn.objects.get_or_create(
    name="Aura of Corruption",
    defaults={
        "thorn_type": "individual",
        "point_cost": 2,
        "activation_cost": "None (always active)",
        "activation_trigger": "Automatic",
        "mechanical_description": "Shadow defiles wraith's presentation; creates subtle unease in other wraiths. +2 difficulty on all Social interaction rolls",
        "resistance_system": "None",
        "duration": "Permanent",
        "frequency_limitation": "Can only be purchased once per character",
        "limitations": "Effect is cumulative with other negative modifiers",
    }
)[0]

Thorn.objects.get_or_create(
    name="Mirror, Mirror",
    defaults={
        "thorn_type": "individual",
        "point_cost": 2,
        "activation_cost": "None",
        "activation_trigger": "When wraith looks in reflective surface",
        "mechanical_description": "Shadow alters wraith's reflection (not actual appearance); distortion plays up Dark Passions; visible to all viewers, not just wraith",
        "resistance_system": "None (reflection automatically distorted)",
        "duration": "Until reflection is no longer viewed",
        "frequency_limitation": "Effectiveness dims with repeated use",
        "limitations": "Requires reflective surface; purely illusory",
    }
)[0]

Thorn.objects.get_or_create(
    name="Shadow Call",
    defaults={
        "thorn_type": "individual",
        "point_cost": 2,
        "activation_cost": "1 temporary Angst per activation",
        "activation_trigger": "Only in Tempest or at Nihil mouth",
        "mechanical_description": "Shadow summons nearby Spectres. Shadowguide spends 1 temporary Angst; rolls against permanent Angst (difficulty 7); successes = number of Spectres summoned",
        "resistance_system": "None (Spectres automatically respond)",
        "resistance_difficulty": 7,
        "duration": "Scene (Spectres act until scene ends or destroyed)",
        "frequency_limitation": "Must be in Tempest/Nihil",
        "limitations": "No effect outside Tempest/Nihil; Spectre types determined by Storyteller",
    }
)[0]

# Medium Thorns (3-5 Point Range)

Thorn.objects.get_or_create(
    name="Pact of Doom",
    defaults={
        "thorn_type": "individual",
        "point_cost": 3,
        "activation_cost": "Permanent Angst equal to levels taught",
        "activation_trigger": "Negotiated agreement between Psyche and Shadow",
        "mechanical_description": "Shadow teaches predetermined Arcanos levels; Shadow gains permanent Angst equal to levels taught. Knowledge sourced from Spectral hive-mind. Example: 1 level Arcanos = 1 permanent Angst to Shadow; 5 levels = 5 permanent Angst",
        "resistance_system": "Requires negotiation; Psyche can refuse",
        "duration": "Permanent (knowledge retained; Angst cost paid once)",
        "frequency_limitation": "Consensual arrangement",
        "limitations": "Only Shadows with Pact of Doom access hive-mind knowledge",
    }
)[0]

Thorn.objects.get_or_create(
    name="Trick of the Light",
    defaults={
        "thorn_type": "individual",
        "point_cost": 3,
        "activation_cost": "1 temporary Angst per activation",
        "activation_trigger": "Per scene (one activation per scene)",
        "mechanical_description": "Shadow alters Psyche's perception of scene; affects one sense per scene (sight, sound, smell, taste, touch). Shadowguide informs Storyteller of perception; Storyteller relays to player",
        "resistance_system": "None (perception-based, not externally resisted)",
        "duration": "Scene (lasts entire scene once activated)",
        "frequency_limitation": "One sense per scene",
        "limitations": "Only affects targeted Psyche (not other wraiths)",
    }
)[0]

Thorn.objects.get_or_create(
    name="Bad Luck",
    defaults={
        "thorn_type": "individual",
        "point_cost": 3,
        "activation_cost": "1 Angst per die reroll",
        "activation_trigger": "After roll is made (retroactive)",
        "mechanical_description": "For each Angst point spent, Shadowguide forces one die reroll (Shadowguide chooses which die). Can be spent multiple times per scene; use doesn't require announcement until after original roll",
        "resistance_system": "None (post-roll only)",
        "duration": "Immediate effect (per roll)",
        "frequency_limitation": "Multiple uses per scene possible",
        "limitations": "Most effective on critical rolls where failure has major consequences",
    }
)[0]

Thorn.objects.get_or_create(
    name="Shadowed Face",
    defaults={
        "thorn_type": "individual",
        "point_cost": 3,
        "activation_cost": "None",
        "activation_trigger": "During Catharsis (automatic with Shadow dominance)",
        "mechanical_description": "Shadow assumes completely different visage (not variety, one set appearance). +1 freebie point optional: Shadow can choose per Catharsis whether to assume Shadowed Face or retain original appearance",
        "resistance_system": "None (automatic upon Catharsis)",
        "duration": "Catharsis scene",
        "frequency_limitation": "Each Catharsis",
        "limitations": "Makes Shadow difficult to identify; potential for mistaken identity",
    }
)[0]

Thorn.objects.get_or_create(
    name="Honeyed Tongue",
    defaults={
        "thorn_type": "individual",
        "point_cost": 4,
        "activation_cost": "1 temporary Angst per use",
        "activation_trigger": "Once per scene, single sentence",
        "mechanical_description": "Shadow makes one sentence unnaturally compelling and believable. Spend 1 Angst; roll temporary Angst (difficulty = target's Manipulation + Subterfuge); success = statement accepted as fact",
        "resistance_system": "Target can spend 1 Willpower point to counteract entire effect",
        "duration": "Single statement effect (until contradicted or believed)",
        "frequency_limitation": "Once per scene maximum",
        "limitations": "Applies to one sentence only",
    }
)[0]

Thorn.objects.get_or_create(
    name="Tainted Touch",
    defaults={
        "thorn_type": "individual",
        "point_cost": 4,
        "activation_cost": "Contact-based",
        "activation_trigger": "Physical contact with target's Corpus",
        "mechanical_description": "Shadow spreads Oblivion via touch; roll 3 dice (difficulty 6); successes = temporary Angst inflicted on victim. Psyche can spend 1 Willpower to turn effect off for one scene. Willing target can accept up to 5 temporary Angst at once",
        "resistance_system": "Target aware of touch can roll Willpower (difficulty 7) to resist; each success cancels one attacker success",
        "resistance_difficulty": 6,
        "duration": "One contact per day per target (resets after 24 hours)",
        "frequency_limitation": "Once per target per day",
        "limitations": "Requires physical contact",
    }
)[0]

Thorn.objects.get_or_create(
    name="Shadowplay",
    defaults={
        "thorn_type": "individual",
        "point_cost": 5,
        "activation_cost": "1 Pathos and grants 1 temporary Angst",
        "activation_trigger": "After all normal actions expended",
        "mechanical_description": "Wraith can take additional action; costs 1 Pathos and grants 1 temporary Angst. Shadow decides availability (entirely Shadowguide discretion). Psyche cannot request this; Shadow must offer",
        "resistance_system": "Shadow decides availability",
        "duration": "Single action",
        "frequency_limitation": "Shadow must offer; Psyche cannot request",
        "limitations": "Psyche can become dependent; Shadow can withhold at critical moments",
    }
)[0]

Thorn.objects.get_or_create(
    name="Shadow Familiar",
    defaults={
        "thorn_type": "individual",
        "point_cost": 5,
        "activation_cost": "None",
        "activation_trigger": "Automatic (Familiar manifests within one week of purchase or replacement)",
        "mechanical_description": "Familiar serves as Shadow's eyes, ears, feet while Shadow remains in consciousness. Typically ravens, rats, or other carrion creatures. Avoids Shadow of other wraiths; flees if threatened; dives to Tempest if attacked. If destroyed, replacement arrives within one week",
        "resistance_system": "None",
        "duration": "Permanent",
        "frequency_limitation": "One familiar at a time",
        "limitations": "Small and harmless; avoidable by hostile wraiths; self-preserving",
    }
)[0]

Thorn.objects.get_or_create(
    name="Freudian Slip",
    defaults={
        "thorn_type": "individual",
        "point_cost": 5,
        "activation_cost": "1 Angst to activate",
        "activation_trigger": "Immediate effect",
        "mechanical_description": "Shadow forces wraith to make involuntary action or unedited statement; can also plant unbidden thoughts. Requires Willpower roll (difficulty 7); requires 2 successes to counter effect",
        "resistance_system": "Willpower roll (difficulty 7) required; requires 2 successes to counter effect",
        "resistance_difficulty": 7,
        "duration": "Immediate (single action/statement)",
        "frequency_limitation": "Requires careful crafting",
        "limitations": "Should be discussed with player beforehand; requires player comfort",
    }
)[0]

Thorn.objects.get_or_create(
    name="Shadow Life",
    defaults={
        "thorn_type": "individual",
        "point_cost": 5,
        "activation_cost": "None",
        "activation_trigger": "Whenever Psyche enters Slumber",
        "mechanical_description": "Shadow takes control of shared Corpus during Slumber; acts as it wishes. Psyche encounters all problems Shadow created upon awakening. +1 optional freebie point = Psyche completely unaware of Shadow Life phenomenon",
        "resistance_system": "None",
        "duration": "Slumber period",
        "frequency_limitation": "Each Slumber",
        "limitations": "Psyche receives all blame for Shadow's actions",
    }
)[0]

# Advanced/High-Level Thorns (6-7 Point Range)

Thorn.objects.get_or_create(
    name="Whispers",
    defaults={
        "thorn_type": "individual",
        "point_cost": 6,
        "activation_cost": "None",
        "activation_trigger": "Automatic (always able to communicate)",
        "mechanical_description": "Shadow can speak to other wraiths' Shadows without Psyche knowledge. Shadows work together; share information and stratagems. Psyche can roll Perception + Awareness (difficulty 8) to notice Shadow seems distracted",
        "resistance_system": "Perception roll only (not preventable, only detectable)",
        "resistance_difficulty": 8,
        "duration": "Permanent communication capability",
        "frequency_limitation": "None",
        "limitations": "Requires both Shadows have this Thorn (or comparable ability)",
    }
)[0]

Thorn.objects.get_or_create(
    name="Manifestation",
    defaults={
        "thorn_type": "individual",
        "point_cost": 6,
        "activation_cost": "4 temporary Angst per activation",
        "activation_trigger": "Costs 4 Angst; lasts one scene",
        "mechanical_description": "Shadow becomes separate physical entity (Corpus identical to Psyche's); can converse, affect objects, use Thorns. Identical appearance and aura to Psyche. Shadow must rest silently next scene",
        "resistance_system": "None",
        "duration": "Single scene (must rest silently following scene)",
        "frequency_limitation": "Must rest silently following scene",
        "limitations": "Two identical wraiths may trigger Doppelganger identification from Legionnaires",
    }
)[0]

Thorn.objects.get_or_create(
    name="Devil's Dare",
    defaults={
        "thorn_type": "individual",
        "point_cost": 7,
        "activation_cost": "Variable Angst per dare",
        "activation_trigger": "Shadowguide writes down dare; Psyche must complete before session end",
        "mechanical_description": "Shadow dares Psyche to perform action before session ends. If Psyche fails: loses temporary Willpower equal to Angst invested. If Psyche succeeds: Shadow gains temporary Angst equal to half invested Angst (rounded down)",
        "resistance_system": "Player can petition Storyteller for reduction if excessive",
        "duration": "Until session end",
        "frequency_limitation": "Dare must be within character's capabilities",
        "limitations": "Impossible dares lose invested Angst",
    }
)[0]

Thorn.objects.get_or_create(
    name="Vampiric Nature",
    defaults={
        "thorn_type": "individual",
        "point_cost": 7,
        "activation_cost": "Contact-based",
        "activation_trigger": "Upon physical contact with target Corpus",
        "mechanical_description": "Shadow siphons Angst from others for own use. Roll contested Willpower against any wraith or Spectre; successes = Angst points absorbed. If target willing, Shadow can accept up to 5 temporary Angst at once. Shadow doesn't need dominance for this to work",
        "resistance_system": "Target makes Willpower roll to resist; each success cancels one attacker success",
        "duration": "One contact",
        "frequency_limitation": "Once per target per session",
        "limitations": "Psyche may never suspect",
    }
)[0]

# Book of Oblivion Thorns

Thorn.objects.get_or_create(
    name="A Moment Gone",
    defaults={
        "thorn_type": "individual",
        "point_cost": 1,
        "activation_cost": "None",
        "activation_trigger": "On Shadow use",
        "mechanical_description": "Shadow retrieves specific memory from Oblivion-eaten wraith. 1 Point: Memory is true but learnable through research. 2 Points: Insight into specific event wraith attended. 3 Points: Deeply personal memory",
        "resistance_system": "None",
        "duration": "Permanent",
        "frequency_limitation": "Can use multiple times",
        "limitations": "After retrieval, Shadow or Psyche with memory-related arts can use them on Spectre's related memories",
    }
)[0]

Thorn.objects.get_or_create(
    name="Absent Heart",
    defaults={
        "thorn_type": "individual",
        "point_cost": 7,
        "activation_cost": "None",
        "activation_trigger": "On Shadow use (Willpower roll resistance)",
        "mechanical_description": "Shadow conceals Psyche's awareness of emotions or source of Passions. Willpower roll (difficulty 8); failure = effect applies. Can suppress emotion only OR subject only",
        "resistance_system": "Willpower roll (difficulty 8); failure = effect applies",
        "resistance_difficulty": 8,
        "duration": "Session duration (entire game session)",
        "frequency_limitation": "Once per session",
        "limitations": "Both options impair Passion benefits but don't eliminate them entirely",
    }
)[0]

# Collective Thorns (Require Multiple Shadows)

Thorn.objects.get_or_create(
    name="Generation of Vipers",
    defaults={
        "thorn_type": "collective",
        "point_cost": 6,
        "activation_cost": "8 temporary Angst (total pool, divided among participants)",
        "activation_trigger": "Group of Shadows influences behavior",
        "mechanical_description": "Group of Shadows influences behavior and emotions of group of wraiths. Insert negative thought into targeted wraiths' minds; each wraith rolls Willpower (difficulty 7) to resist",
        "resistance_system": "Each wraith rolls Willpower (difficulty 7) to resist",
        "resistance_difficulty": 7,
        "duration": "Scene",
        "frequency_limitation": "Cannot be used on same target more than once per session",
        "limitations": "Any Shadow with this Thorn contributes to pool",
    }
)[0]

Thorn.objects.get_or_create(
    name="Dining in Hell",
    defaults={
        "thorn_type": "collective",
        "point_cost": 7,
        "activation_cost": "Contact with targets; Willpower contest",
        "activation_trigger": "Group feeding on 3+ targets",
        "mechanical_description": "Group of Shadows feeds on Angst of 3+ wraiths or Spectres; disperses among participating Shadows. Shadows must make physical contact with targets. Contested Willpower roll; successes determine Angst extracted amount",
        "resistance_system": "Contested Willpower roll (opposed roll)",
        "duration": "One contact",
        "frequency_limitation": "Cannot be used on same target more than once per session",
        "limitations": "Minimum 3 targets required; extracted Angst divided among participating Shadows",
    }
)[0]

Thorn.objects.get_or_create(
    name="Earthquake Weather",
    defaults={
        "thorn_type": "collective",
        "point_cost": 7,
        "activation_cost": "10 temporary Angst (total pool, divided flexibly)",
        "activation_trigger": "Environmental alteration",
        "mechanical_description": "Group of Shadows changes local environment; modifies difficulties. Can raise or lower by 1: Local Shroud rating, Successes needed on Argos rolls, Local Maelstrom level. Basic effect = 3 turns. Additional 3 turns/scene/day/week: 10 Angst each. Area: line of sight to square mile/district/necropolis: 10 Angst each",
        "resistance_system": "Affected Wraiths: Willpower roll (difficulty 6) to act against Thorn, then spend 10 Pathos per turn duration reduction. Unaffected Wraiths: No Willpower roll needed, same Pathos/Willpower spending",
        "resistance_difficulty": 6,
        "duration": "3 turns base (scaling available)",
        "frequency_limitation": "Complex scaling system",
        "limitations": "Teamwork: Shadows can pool; Wraiths can pool counter-efforts",
    }
)[0]

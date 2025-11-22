from characters.models.wraith.shadow_archetype import ShadowArchetype

# 12 Shadow Archetypes from Book of Oblivion and 20th Anniversary

ShadowArchetype.objects.get_or_create(
    name="The Delver",
    defaults={
        "point_cost": 1,
        "core_function": "Relentless overanalysis and conspiracy detection",
        "modus_operandi": "Questions all surface explanations, seeks hidden meanings",
        "dominance_behavior": "Asks painfully probing questions, dissects answers, obsessively revisits issues",
        "effect_on_psyche": "Drives companions to frustration; occasionally reveals actual conspiracies",
        "strengths": "Paranoid but sometimes correct pattern recognition",
        "weaknesses": "Unable to accept simple explanations",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The Abuser",
    defaults={
        "point_cost": 1,
        "core_function": "Inflicting reciprocal pain",
        "modus_operandi": "Scrutinizes failures of others, heaps scorn",
        "dominance_behavior": "Spews vitriol in all directions; creates excuses for outbursts; demands obedience",
        "effect_on_psyche": "Reckless physical/verbal abuse; self-destructive behavior",
        "strengths": "Immediate destructive power",
        "weaknesses": "Lacks subtlety; self-sabotaging",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The Director",
    defaults={
        "point_cost": 1,
        "core_function": "Surgical, organized torment",
        "modus_operandi": "Catalogs weaknesses for strategic deployment",
        "dominance_behavior": "Lays long-range plans; reveals ammunition at exact moments",
        "effect_on_psyche": "Creates carefully timed revelations; poisonous observations about companions",
        "strengths": "Intelligent, methodical, accurate observations",
        "weaknesses": "Requires planning time; vulnerable if timetable disrupted",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The False Friend",
    defaults={
        "point_cost": 1,
        "core_function": "Separation through corrupted loyalty",
        "modus_operandi": "Makes cutting wisecracks while seeming likable",
        "dominance_behavior": "Instills contempt for allies while appearing supportive; reveals itself only after isolation achieved",
        "effect_on_psyche": "Damages relationships; promotes hypocrisy exploitation",
        "strengths": "Personable facade; difficult to detect initially",
        "weaknesses": "Revealed when switching tactics",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The Parent",
    defaults={
        "point_cost": 1,
        "core_function": "Infantilizing control through conditional love",
        "modus_operandi": "Claims exclusive ability to love/protect",
        "dominance_behavior": "Insulates Psyche from 'corrupting influences'; makes decisions unilaterally",
        "effect_on_psyche": "Alienation of all external relationships; dependence reinforcement",
        "strengths": "Emotional manipulation; claims moral authority",
        "weaknesses": "Exposed when 'outsiders' prove beneficial",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The Martyr",
    defaults={
        "point_cost": 1,
        "core_function": "Cheapening sacrifice through forced suffering",
        "modus_operandi": "Claims greater good justifies pain",
        "dominance_behavior": "Maneuvers Psyche into no-win scenarios; arranges witnesses to shame others",
        "effect_on_psyche": "Public spectacle of suffering; manipulation of circle members",
        "strengths": "Moral authority veneer; audience leverage",
        "weaknesses": "Transparent when suffering produces no results",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The Monster",
    defaults={
        "point_cost": 1,
        "core_function": "Brutal direct domination",
        "modus_operandi": "Commands obedience; destroys resistance",
        "dominance_behavior": "Demands whatever it wants; destroys what it hates; no subtlety or negotiation",
        "effect_on_psyche": "Complete spectral transformation preview",
        "strengths": "Immediate overwhelming force",
        "weaknesses": "No strategy; self-defeating behavior",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The Somnambulist",
    defaults={
        "point_cost": 1,
        "core_function": "Apathy exploitation and willful neglect",
        "modus_operandi": "Downplays urgency to prevent action",
        "dominance_behavior": "Withdraws from activities; drops commitments spectacularly; reveals surprises later",
        "effect_on_psyche": "Missed opportunities; relationship failures; revealed dereliction",
        "strengths": "Lulls Psyche into false security",
        "weaknesses": "Predictable when apathy broken",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The Perfectionist",
    defaults={
        "point_cost": 1,
        "core_function": "Confidence destruction through impossible standards",
        "modus_operandi": "Demands seven impossible things, complains about not getting eight",
        "dominance_behavior": "Criticizes all targets equally; embroils Psyche in impossible scenarios; offers 'help' to take over",
        "effect_on_psyche": "Systemic self-hatred; learned helplessness; confidence collapse",
        "strengths": "Justification for taking control; universal targets",
        "weaknesses": "Predictable criticism patterns",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The Voice of Hope",
    defaults={
        "point_cost": 1,
        "core_function": "Denial of death through false hope",
        "modus_operandi": "Claims Underworld is nightmare; holds out escape possibility",
        "dominance_behavior": "Denies reality; shifts focus from escape to 'cure'; repeats cycle",
        "effect_on_psyche": "Endless suffering through dashed hopes",
        "strengths": "Emotional sustenance facade; motivates action",
        "weaknesses": "Inevitably exposed as false",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The Stormcrow",
    defaults={
        "point_cost": 1,
        "core_function": "Doom-certainty and sabotage",
        "modus_operandi": "Details gruesome consequences with enthusiasm",
        "dominance_behavior": "Dissuades beneficial actions; points out catastrophic consequences; sabotages outcomes",
        "effect_on_psyche": "Undermines companion actions; ensures foreseen failures",
        "strengths": "Self-fulfilling prophesy mechanics",
        "weaknesses": "Depends on Psyche following suggestions",
    },
)[0]

# From Book of Oblivion - Additional Archetypes
ShadowArchetype.objects.get_or_create(
    name="The Alien",
    defaults={
        "point_cost": 1,
        "core_function": "Gaslight psyche, self-doubt",
        "modus_operandi": "Convince wraith was never human",
        "dominance_behavior": "Lying about own nature",
        "effect_on_psyche": "Identity crisis and self-doubt",
        "strengths": "Can make wraith question fundamental reality",
        "weaknesses": "Lying about own nature",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The Conqueror",
    defaults={
        "point_cost": 1,
        "core_function": "Dominate and control",
        "modus_operandi": "Violent assertion, territory claims",
        "dominance_behavior": "Can be reasoned with via strength/respect",
        "effect_on_psyche": "Forces submission through overwhelming power",
        "strengths": "Responds to strength",
        "weaknesses": "Can be reasoned with via strength/respect",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The Destroyer",
    defaults={
        "point_cost": 1,
        "core_function": "Pure destruction",
        "modus_operandi": "Tear down meaning and hope",
        "dominance_behavior": "Destructive urges exposed",
        "effect_on_psyche": "Systematic destruction of all meaning",
        "strengths": "Single-minded focus on destruction",
        "weaknesses": "Destructive urges exposed",
    },
)[0]

ShadowArchetype.objects.get_or_create(
    name="The Narcissist",
    defaults={
        "point_cost": 1,
        "core_function": "Worship and praise focus",
        "modus_operandi": "Demand attention and sacrifice",
        "dominance_behavior": "Self-love vulnerability",
        "effect_on_psyche": "Forces wraith to worship Shadow",
        "strengths": "Charismatic and demanding",
        "weaknesses": "Self-love vulnerability",
    },
)[0]

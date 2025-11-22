from items.models.changeling import Treasure

# 1-DOT TREASURES (Minor)
Treasure.objects.get_or_create(
    name="Dross Token",
    rating=1,
    treasure_type="talisman",
    creator="Changelings",
    creation_method="Solidified Glamour taken from freeholds or trods",
    permanence=True,
    special_abilities="Can be spent as Glamour (1 Glamour = 1 token); can be scattered to distract pursuing enemies; can serve as proof of Changeling identity",
    effects=["Store Glamour", "Prove Identity", "Distraction"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 180)

Treasure.objects.get_or_create(
    name="Enchanted Charm",
    rating=1,
    treasure_type="talisman",
    creator="Boggans, Craftspeople",
    creation_method="Crafted with Legerdemain or Primal Arts",
    permanence=True,
    special_abilities="Provides +1 die to a specific skill or ability",
    effects=["Skill Bonus"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 181)

Treasure.objects.get_or_create(
    name="Simple Alchemy Kit",
    rating=1,
    treasure_type="wonder",
    creator="Boggans",
    creation_method="Crafted with mundane materials and minor enchantments",
    permanence=True,
    special_abilities="Allows creation of herbal remedies and potions",
    effects=["Potion Crafting"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 181)

Treasure.objects.get_or_create(
    name="Seeming Mask",
    rating=1,
    treasure_type="wonder",
    creator="Changelings",
    creation_method="Created through Metamorphosis or Chicanery",
    permanence=True,
    special_abilities="Provides +2 difficulty against those trying to see through Seeming or glamour-based disguises",
    effects=["Enhance Disguise"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 181)

# 2-DOT TREASURES (Moderate)
Treasure.objects.get_or_create(
    name="Glamour Vessel",
    rating=2,
    treasure_type="talisman",
    creator="Skilled Changelings",
    creation_method="Created with Contract and Naming Arts",
    permanence=True,
    glamour_storage=5,
    special_abilities="Can store up to 5 Glamour points for later use",
    effects=["Glamour Storage"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 181)

Treasure.objects.get_or_create(
    name="Enchanted Weapon",
    rating=2,
    treasure_type="weapon",
    creator="Trolls, Redcaps, Warriors",
    creation_method="Enhanced with Dragon's Ire and Pyretics",
    permanence=True,
    special_abilities="Deals +1 aggravated damage; counts as cold-iron for supernatural beings if crafted with specific Arts",
    effects=["Aggravated Damage", "Cold Iron Effect"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 182)

Treasure.objects.get_or_create(
    name="Fae-Touched Armor",
    rating=2,
    treasure_type="armor",
    creator="Trolls, Sidhe Warriors",
    creation_method="Infused with Primal and Dragon's Ire",
    permanence=True,
    special_abilities="Adds +1 soak difficulty to all damage taken",
    effects=["Damage Reduction"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 182)

Treasure.objects.get_or_create(
    name="Dream Journal",
    rating=2,
    treasure_type="wonder",
    creator="Oneiromancy Practitioners",
    creation_method="Created with Oneiromancy Art",
    permanence=True,
    special_abilities="Records and preserves dreams of the writer; reader can experience recorded dreams",
    effects=["Dream Recording", "Dream Sharing"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 182)

Treasure.objects.get_or_create(
    name="Compass of True Paths",
    rating=2,
    treasure_type="wonder",
    creator="Eshu, Travelers",
    creation_method="Created with Wayfare and Soothsay",
    permanence=True,
    special_abilities="Always points toward designated destination; difficulty 6 to navigate with it",
    effects=["Navigation", "Path Finding"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 182)

# 3-DOT TREASURES (Significant)
Treasure.objects.get_or_create(
    name="Fae Crown",
    rating=3,
    treasure_type="wonder",
    creator="Sidhe Nobility",
    creation_method="Crafted with Sovereign and Naming",
    permanence=True,
    special_abilities="Grants +2 difficulty to resist commands from wearer; wearer gains +1 die to Leadership and Etiquette rolls",
    effects=["Command Authority", "Leadership Bonus"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 183)

Treasure.objects.get_or_create(
    name="Healing Draught Bottle",
    rating=3,
    treasure_type="wonder",
    creator="Spring/Summer Practitioners",
    creation_method="Infused with Spring and Pyretics",
    permanence=True,
    special_abilities="Contains healing potion that restores 3 levels of bashing or 1 lethal damage; refills slowly (1 dose per week)",
    effects=["Healing", "Health Restoration"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 183)

Treasure.objects.get_or_create(
    name="Shadowbound Cloak",
    rating=3,
    treasure_type="wonder",
    creator="Sluagh, Autumn Practitioners",
    creation_method="Crafted with Autumn and Chicanery",
    permanence=True,
    special_abilities="Wearer gains +3 difficulty for Stealth rolls in shadows; grants temporary 1-dot Stealth when in shadow",
    effects=["Shadow Concealment", "Stealth Enhancement"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 183)

Treasure.objects.get_or_create(
    name="Temporal Amulet",
    rating=3,
    treasure_type="talisman",
    creator="Chronos Practitioners",
    creation_method="Created with Chronos Art",
    permanence=True,
    special_abilities="Wearer ages one year slower than normal; can use Chronos cantrips at -1 difficulty",
    effects=["Age Slowing", "Chronos Affinity"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 183)

Treasure.objects.get_or_create(
    name="Oath Ring",
    rating=3,
    treasure_type="talisman",
    creator="Contract Practitioners",
    creation_method="Infused with Contract Art",
    permanence=True,
    special_abilities="Wearer gains +1 die for all Contract-related cantrips; glows when oaths nearby are broken",
    effects=["Contract Affinity", "Oath Awareness"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 183)

# 4-DOT TREASURES (Extensive)
Treasure.objects.get_or_create(
    name="Dragon's Fang Blade",
    rating=4,
    treasure_type="weapon",
    creator="Ancient Sidhe Warriors",
    creation_method="Forged with Dragon's Ire and Naming at highest levels",
    permanence=True,
    special_abilities="Deals +2 aggravated damage; cannot be broken; +1 difficulty for all attacks against wielder",
    effects=["Aggravated Damage", "Unbreakable", "Combat Defense"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 184)

Treasure.objects.get_or_create(
    name="Caern Totem Stone",
    rating=4,
    treasure_type="wonder",
    creator="Freehold Founders",
    creation_method="Bound to location through powerful Naming and Primal",
    permanence=True,
    glamour_storage=10,
    special_abilities="Acts as focal point for freehold; stores up to 10 Glamour; connected inhabitants gain +1 Glamour pool refresh daily",
    effects=["Freehold Focus", "Glamour Storage", "Glamour Generation"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 184)

Treasure.objects.get_or_create(
    name="Mirror of True Sight",
    rating=4,
    treasure_type="wonder",
    creator="Lore Masters",
    creation_method="Created with Naming and Chicanery",
    permanence=True,
    special_abilities="Reveals true nature and hidden deceptions; user sees through illusions, disguises, and cantrips automatically",
    effects=["Truth Seeing", "Illusion Piercing", "Identity Revelation"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 184)

Treasure.objects.get_or_create(
    name="Dreamweaver's Loom",
    rating=4,
    treasure_type="wonder",
    creator="Oneiromancy Masters",
    creation_method="Crafted with Oneiromancy and Metamorphosis",
    permanence=True,
    special_abilities="Allows creation and manipulation of complex dreams; user can affect multiple dreamers at once; dreams created last longer",
    effects=["Dream Creation", "Dream Weaving", "Multi-target Dreams"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 185)

# 5-DOT TREASURES (Legendary/Unique)
Treasure.objects.get_or_create(
    name="The Crown of Ys",
    rating=5,
    treasure_type="wonder",
    creator="Arcadian Sidhe",
    creation_method="Ancient artifact from Arcadia itself",
    permanence=True,
    special_abilities="Wearer commands respect and authority from all Changelings; +3 die to all social rolls; wearer cannot be compelled against their will; restored nightly to full Glamour",
    effects=[
        "Unquestionable Authority",
        "Social Domination",
        "Glamour Restoration",
        "Magical Resistance",
    ],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 185)

Treasure.objects.get_or_create(
    name="The Twilight Blade",
    rating=5,
    treasure_type="weapon",
    creator="Unknown Ancient Master",
    creation_method="Legendary weapon that exists between worlds",
    permanence=True,
    special_abilities="Deals +3 aggravated damage; can strike targets in Dreaming from waking world; wounds never heal naturally; wielder gains +2 dice to all combat rolls",
    effects=[
        "Aggravated Damage",
        "Reality Piercing",
        "Unhealable Wounds",
        "Combat Mastery",
    ],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 185)

Treasure.objects.get_or_create(
    name="The Green Knight's Grail",
    rating=5,
    treasure_type="wonder",
    creator="Camelot Legend",
    creation_method="Legendary artifact of healing and renewal",
    permanence=True,
    special_abilities="Can heal any wound including Banality damage; restores Glamour to full when drunk from; grants vision of righteous path for user",
    effects=[
        "Complete Healing",
        "Glamour Restoration",
        "Banality Reduction",
        "Divine Guidance",
    ],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 185)

Treasure.objects.get_or_create(
    name="The Hollow Crown",
    rating=5,
    treasure_type="wonder",
    creator="Shadow Court",
    creation_method="Artifact of mystery and secrets",
    permanence=True,
    special_abilities="Wearer gains knowledge of all bargains in their presence; can see into shadows and secrets; wearer becomes partially unseen by those they choose",
    effects=["Secret Knowledge", "Shadow Vision", "Selective Invisibility"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 186)

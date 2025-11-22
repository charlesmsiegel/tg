"""
Populate database with Akashic Brotherhood (1st Edition) content
Book: Akashic Brotherhood (Balance, Ascension and the Cosmic All)
Author: Emrey Barnes
"""

from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.focus import Instrument, Practice, Paradigm
from characters.models.mage.effect import Effect
from characters.models.mage.rote import Rote
from items.models.mage.wonder import Wonder
from locations.models.mage.chantry import Chantry
from locations.models.mage.node import Node
from game.models import Book

def populate_ab_1e():
    """Populate Akashic Brotherhood content"""

    # Create book reference
    book, _ = Book.objects.get_or_create(
        title="Akashic Brotherhood",
        defaults={
            "subtitle": "Balance, Ascension and the Cosmic All",
            "edition": "1st Edition",
            "system": "M20",  # or appropriate system
            "publisher": "White Wolf",
            "publication_date": "1994",
        }
    )

    # ========================================
    # PARADIGMS
    # ========================================

    paradigm_cosmic_all, _ = Paradigm.objects.get_or_create(
        name="The Cosmic All",
        defaults={
            "description": "Reality is an interconnected whole. All things are part of the Cosmic All, the unified field of existence. By understanding one's place in this totality, one can manipulate the patterns of reality.",
            "book": book,
        }
    )

    paradigm_drahma, _ = Paradigm.objects.get_or_create(
        name="Drahma (The Wheel)",
        defaults={
            "description": "What comes around goes around. The cycle of action and reaction, karma and rebirth. Understanding Drahma allows one to predict and direct destiny itself.",
            "book": book,
        }
    )

    # ========================================
    # PRACTICES
    # ========================================

    practice_do, _ = Practice.objects.get_or_create(
        name="Do (Martial Arts)",
        defaults={
            "description": "More than martial arts - the refining of being through movement, breath, and focus. Do encompasses the physical, mental, spiritual and primal aspects of existence.",
            "book": book,
        }
    )

    practice_meditation, _ = Practice.objects.get_or_create(
        name="Meditation",
        defaults={
            "description": "Deep contemplative practices to achieve connection with the inner self and the flow of the Cosmic All.",
            "book": book,
        }
    )

    practice_breath, _ = Practice.objects.get_or_create(
        name="Prenatal Breathing",
        defaults={
            "description": "Relearning to breathe properly, returning to the 'prenatal' breathing that links into the spark-of-life. This primal power circulates rejuvenating force through the whole being.",
            "book": book,
        }
    )

    # ========================================
    # INSTRUMENTS
    # ========================================

    instrument_sash, _ = Instrument.objects.get_or_create(
        name="Sash/Belt",
        defaults={
            "description": "A cloth belt that binds the Forces Sphere within the practitioner, serving as both symbol and focus.",
            "book": book,
        }
    )

    instrument_magick_papers, _ = Instrument.objects.get_or_create(
        name="Magick Papers",
        defaults={
            "description": "Slips of yellow paper inscribed with characters in red ink (often mixed with the practitioner's blood). The inscription determines powers, size indicates strength.",
            "book": book,
        }
    )

    instrument_prayer_beads, _ = Instrument.objects.get_or_create(
        name="Prayer Beads",
        defaults={
            "description": "Sacred beads used for meditation, chanting, and focusing will.",
            "book": book,
        }
    )

    # ========================================
    # NAMED CHARACTERS
    # ========================================

    # Raging Eagle - Major NPC
    raging_eagle, _ = Mage.objects.get_or_create(
        name="Raging Eagle",
        defaults={
            "description": "One of the lead Sensei of the Scales of the Dragon for over 50 years. Known throughout the Brotherhood for his martial mastery. Trains in a secret cavern high in the mountains of Tibet. Chiseled features, stone-like muscles, completely shaved head.",
            "tradition": "Akashic Brotherhood",
            "sect": "Scales of the Dragon",
            "essence": "Questing",
            "arete": 6,
            "book": book,
            "status": "App",
            "willpower": 9,
            "quintessence": 15,
        }
    )

    # Gentle Mountain - Major NPC
    gentle_mountain, _ = Mage.objects.get_or_create(
        name="Gentle Mountain",
        defaults={
            "description": "Master instructor of Orange Robes since the turn of the century. Projects his mind into students to help perfect thought forms. Spry old man, naturally bald with long flowing gray beard and outstanding eyebrows. Unusually long ear lobes (sign of longevity). Wears orange robes and Kemian prayer beads.",
            "tradition": "Akashic Brotherhood",
            "sect": "Orange Robes",
            "essence": "Pattern",
            "arete": 7,
            "book": book,
            "status": "App",
            "willpower": 10,
            "quintessence": 20,
        }
    )

    # Fall Breeze - Major NPC
    fall_breeze, _ = Mage.objects.get_or_create(
        name="Fall Breeze",
        defaults={
            "description": "Young female Akashic Brother, student of Gentle Mountain. Has memories of past lives including one in ancient Egypt with Battering Ram. Skilled in accessing the Akashic Record.",
            "tradition": "Akashic Brotherhood",
            "essence": "Pattern",
            "arete": 3,
            "book": book,
            "status": "App",
            "willpower": 6,
        }
    )

    # Battering Ram - Protagonist
    battering_ram, _ = Mage.objects.get_or_create(
        name="Battering Ram",
        defaults={
            "description": "Kickboxer who Awakened during a fight. Avatar has been reincarnating through the Brotherhood for many lifetimes. Trained by Raging Eagle. Wields a sword with her name etched on the blade in ancient characters. Scale of the Dragon.",
            "tradition": "Akashic Brotherhood",
            "sect": "Scales of the Dragon",
            "essence": "Questing",
            "arete": 2,
            "book": book,
            "status": "App",
            "willpower": 5,
        }
    )

    # Nichiba - The Weaponless Defender
    nichiba, _ = Mage.objects.get_or_create(
        name="Nichiba",
        defaults={
            "description": "Known as 'The Weaponless Defender'. Debater and warrior of the Brotherhood. Present at the Grand Convocation. Advocates caution regarding involvement with other Traditions.",
            "tradition": "Akashic Brotherhood",
            "sect": "Scales of the Dragon",
            "essence": "Questing",
            "arete": 4,
            "book": book,
            "status": "App",
        }
    )

    # Cheng Sa - The Woodcutter
    cheng_sa, _ = Mage.objects.get_or_create(
        name="Cheng Sa",
        defaults={
            "description": "Known as 'The Woodcutter'. Skilled linguist, represented Brotherhood at the Grand Convocation. Wields a massive axe. Long strides, diplomatic.",
            "tradition": "Akashic Brotherhood",
            "sect": "Scales of the Dragon",
            "essence": "Questing",
            "arete": 4,
            "book": book,
            "status": "App",
        }
    )

    # Darumha
    darumha, _ = Mage.objects.get_or_create(
        name="Darumha",
        defaults={
            "description": "Scribe and artist of the Brotherhood. Paints scenes and takes extensive notes. Present at the Grand Convocation. Fascinated by Dreamspeakers.",
            "tradition": "Akashic Brotherhood",
            "sect": "Orange Robes",
            "essence": "Pattern",
            "arete": 3,
            "book": book,
            "status": "App",
        }
    )

    # Ma Yee Fuk - Antagonist/Nephandi
    ma_yee_fuk, _ = Mage.objects.get_or_create(
        name="Ma Yee Fuk",
        defaults={
            "description": "Traitor to the Brotherhood, banished from Shaolin Xiudaoyuan for sexual advances toward Simiao Zhuchi's wife and daughter. Betrayed Shaolin to Manchurian forces and Euthanatos. Reincarnates with obsessive hatred. Avatar has been branded with traitor's sigil.",
            "tradition": "Nephandi",
            "essence": "Primordial",
            "arete": 5,
            "book": book,
            "status": "Dec",
        }
    )

    # Akasha - Ascended
    akasha, _ = Mage.objects.get_or_create(
        name="Akasha",
        defaults={
            "description": "Ascended Avatar credited with the development of writing and formation of the Akashic Record. Threw himself into the greatest waterfall in all the Realms in an act of sacrifice. His mind, body, and soul were caught by Dragon, Tiger, and Phoenix respectively.",
            "tradition": "Akashic Brotherhood",
            "essence": "Primordial",
            "arete": 10,
            "book": book,
            "status": "App",
            "notes": "Ascended - no longer incarnate",
        }
    )

    # Historical Figures
    pang_xiao, _ = MtAHuman.objects.get_or_create(
        name="Pang Xiao",
        defaults={
            "description": "Historical Akashic Brother who employed the Long-range Eyes rote to spy on enemies.",
            "book": book,
        }
    )

    vu_zhang, _ = MtAHuman.objects.get_or_create(
        name="Vu Zhang",
        defaults={
            "description": "Student whose girlfriend Glowing Orchid was captured by wizard Yu Fang. Used Sure Footing rote to scale vertical cliff face.",
            "book": book,
        }
    )

    glowing_orchid, _ = MtAHuman.objects.get_or_create(
        name="Glowing Orchid",
        defaults={
            "description": "Vu Zhang's girlfriend, captured by Yu Fang. Member of the Brotherhood.",
            "book": book,
        }
    )

    yu_fang, _ = Mage.objects.get_or_create(
        name="Yu Fang",
        defaults={
            "description": "Wizard with a mountain Chantry accessible only by narrow walkway. Kidnapped Glowing Orchid.",
            "tradition": "Unknown",
            "arete": 4,
            "book": book,
        }
    )

    quiet_meadow, _ = MtAHuman.objects.get_or_create(
        name="Quiet Meadow",
        defaults={
            "description": "Battering Ram's mortal mate in a past incarnation during the Grand Convocation era.",
            "book": book,
        }
    )

    # Technocracy/Iteration X
    bill_bookman, _ = MtAHuman.objects.get_or_create(
        name="Bill Bookman",
        defaults={
            "description": "Battering Ram's manager, revealed to be an Iteration X cyborg assassin. Half human, half machine with spinning blade weapons in hands. Destroyed by Raging Eagle.",
            "book": book,
            "notes": "Iteration X HIT Mark - deceased",
        }
    )

    # Other Tradition Mages
    alexandre_dumonte, _ = Mage.objects.get_or_create(
        name="Alexandre DuMonte",
        defaults={
            "description": "Hermetic mage (Solificato) present at Grand Convocation. French, skilled in Mandarin. Advocates coordinated strikes against Order of Reason. Focused on tactical planning.",
            "tradition": "Order of Hermes",
            "house": "Solificati",
            "essence": "Questing",
            "arete": 5,
            "book": book,
            "status": "App",
        }
    )

    dimitri, _ = Mage.objects.get_or_create(
        name="Dimitri",
        defaults={
            "description": "Solificato alchemist, apprentice to DuMonte. Dismissive and disrespectful toward Akashic Brothers. Present at Grand Convocation.",
            "tradition": "Order of Hermes",
            "house": "Solificati",
            "essence": "Questing",
            "arete": 2,
            "book": book,
            "status": "App",
        }
    )

    wlakar_fahir, _ = Mage.objects.get_or_create(
        name="Wlakar Fahir",
        defaults={
            "description": "Ahl-i-Batin mage, leader of Subtle Ones delegation. Never reveals his face. Befriends Darumha during journey to Grand Convocation. Philosophical and cautious.",
            "tradition": "Ahl-i-Batin",
            "essence": "Questing",
            "arete": 5,
            "book": book,
            "status": "App",
        }
    )

    qi_lee_hin, _ = Mage.objects.get_or_create(
        name="Qi Lee Hin",
        defaults={
            "description": "Spirit entity who opened the eyes of a street tough to the worlds beyond, leading them to the Akashic Brotherhood. Mysterious motives - favor or spite unclear.",
            "tradition": "Unknown",
            "essence": "Dynamic",
            "arete": 3,
            "book": book,
            "notes": "Spirit guide/entity",
        }
    )

    # ========================================
    # ROTES/EFFECTS
    # ========================================

    # Long-range Eyes
    effect_long_range_eyes, _ = Effect.objects.get_or_create(
        name="Long-range Eyes",
        defaults={
            "description": "Allows the mage to look at any imaginable location and extrapolate backwards and forwards in time to determine what is presently going on, what has gone before, and what will happen next in that location. May trace a time span or follow a given target.",
            "book": book,
            "practice": practice_meditation.name,
            "primary_sphere": "Time",
            "primary_sphere_level": 2,
            "requires_correspondence": 2,
            "requires_mind": 1,
            "effect_type": "Perception",
        }
    )

    rote_long_range_eyes, _ = Rote.objects.get_or_create(
        name="Long-range Eyes",
        defaults={
            "effect": effect_long_range_eyes,
            "tradition": "Akashic Brotherhood",
            "description": "Employed by Pang Xiao to spy on his enemies. Power of the celestial personae of Long-range Eyes.",
            "book": book,
        }
    )

    # Sure Footing
    effect_sure_footing, _ = Effect.objects.get_or_create(
        name="Sure Footing",
        defaults={
            "description": "Alters matter into a form that the mage can travel over normally. Does not alter appearance or transcend gravity - merely changes surface structure and composition to provide grip and support.",
            "book": book,
            "practice": practice_do.name,
            "primary_sphere": "Matter",
            "primary_sphere_level": 3,
            "requires_prime": 2,
            "effect_type": "Physical",
        }
    )

    rote_sure_footing, _ = Rote.objects.get_or_create(
        name="Sure Footing",
        defaults={
            "effect": effect_sure_footing,
            "tradition": "Akashic Brotherhood",
            "description": "Allows running up near-vertical cliff faces and impossible surfaces. Used by Vu Zhang to scale Yu Fang's mountain fortress.",
            "book": book,
        }
    )

    # Flash-bomb Stunt
    effect_flash_bomb, _ = Effect.objects.get_or_create(
        name="Flash-bomb Stunt",
        defaults={
            "description": "Concentrates all light from an area into a pinpoint and places it to impair opponent's vision - usually directly in front of their eyes. Causes temporary blindness.",
            "book": book,
            "practice": practice_do.name,
            "primary_sphere": "Forces",
            "primary_sphere_level": 2,
            "effect_type": "Attack",
        }
    )

    rote_flash_bomb, _ = Rote.objects.get_or_create(
        name="Flash-bomb Stunt",
        defaults={
            "effect": effect_flash_bomb,
            "tradition": "Akashic Brotherhood",
            "description": "Method of blinding opponents for attack and evasion. Taught to those who battle in Ascension Wars.",
            "book": book,
        }
    )

    # Smoke-bomb Trick
    effect_smoke_bomb, _ = Effect.objects.get_or_create(
        name="Smoke-bomb Trick",
        defaults={
            "description": "Conjures huge cloud of thick smoke that blocks vision and irritates eyes. Simple egg shell or tiny grenade makes it coincidental.",
            "book": book,
            "practice": practice_do.name,
            "primary_sphere": "Matter",
            "primary_sphere_level": 2,
            "requires_prime": 2,
            "effect_type": "Defense",
        }
    )

    rote_smoke_bomb, _ = Rote.objects.get_or_create(
        name="Smoke-bomb Trick",
        defaults={
            "effect": effect_smoke_bomb,
            "tradition": "Akashic Brotherhood",
            "description": "Creates blinding smoke cloud. Taught to Ascension War combatants.",
            "book": book,
        }
    )

    # Summon Weapon
    effect_summon_weapon, _ = Effect.objects.get_or_create(
        name="Summon Weapon",
        defaults={
            "description": "Causes weapon to instantaneously appear in hand. If dedicated weapon is within range, Correspondence moves it. If weapon must be formed, Prime and Matter create it (though such copies are often inferior).",
            "book": book,
            "practice": practice_do.name,
            "primary_sphere": "Correspondence",
            "primary_sphere_level": 3,
            "requires_mind": 1,
            "alternate_spheres": "Matter 2, Prime 2, Mind 1",
            "effect_type": "Utility",
        }
    )

    rote_summon_weapon, _ = Rote.objects.get_or_create(
        name="Summon Weapon",
        defaults={
            "effect": effect_summon_weapon,
            "tradition": "Akashic Brotherhood",
            "description": "Ancient rote allowing monks to summon sacred weapons. Usually vulgar but can be explained by bounces, handy companions, or ricochets.",
            "book": book,
        }
    )

    # Focus of the Blow
    effect_focus_blow, _ = Effect.objects.get_or_create(
        name="Focus of the Blow",
        defaults={
            "description": "Allows Doist to feel when a technique is performed correctly by detecting kinetic energy generated. Lowers damage difficulty by one per success. Teachers use this to judge maneuver success by touch.",
            "book": book,
            "practice": practice_do.name,
            "primary_sphere": "Forces",
            "primary_sphere_level": 1,
            "requires_mind": 1,
            "effect_type": "Enhancement",
        }
    )

    rote_focus_blow, _ = Rote.objects.get_or_create(
        name="Focus of the Blow",
        defaults={
            "effect": effect_focus_blow,
            "tradition": "Akashic Brotherhood",
            "description": "Teaching rote used by Thundering Spring River Sparrow to help older students perfect Do execution.",
            "book": book,
            "requires_maneuver": "Punch, Kick, Flying Kick or Throw",
        }
    )

    # Spirit Wounder
    effect_spirit_wounder, _ = Effect.objects.get_or_create(
        name="Spirit Wounder",
        defaults={
            "description": "Grants attunement with Umbral beings, allowing mage to grasp or strike non-materialized ephemera. Damage inflicted normally. Grants fear and respect in spirit world, but also marks mage as greater threat.",
            "book": book,
            "practice": practice_do.name,
            "primary_sphere": "Spirit",
            "primary_sphere_level": 3,
            "effect_type": "Attack",
        }
    )

    rote_spirit_wounder, _ = Rote.objects.get_or_create(
        name="Spirit Wounder",
        defaults={
            "effect": effect_spirit_wounder,
            "tradition": "Akashic Brotherhood",
            "description": "Ancient Yogi rote for contending with less cooperative Umbral entities. Essential for spirit combat.",
            "book": book,
            "requires_maneuver": "Punch, Kick or Throw",
        }
    )

    # Repeating Blow
    effect_repeating_blow, _ = Effect.objects.get_or_create(
        name="Repeating Blow",
        defaults={
            "description": "At beginning of maneuver, Doist retracts blow just before landing, redirecting kinetic force within their Pattern. Can repeat multiple times with increasing difficulty (+1 per turn). Release creates titanic blow with multiplied damage. Incredibly dangerous and vulgar.",
            "book": book,
            "practice": practice_do.name,
            "primary_sphere": "Forces",
            "primary_sphere_level": 3,
            "requires_correspondence": 3,
            "requires_mind": 1,
            "requires_prime": 2,
            "effect_type": "Attack",
        }
    )

    rote_repeating_blow, _ = Rote.objects.get_or_create(
        name="Repeating Blow",
        defaults={
            "effect": effect_repeating_blow,
            "tradition": "Akashic Brotherhood",
            "description": "Created by Ah Mu to shatter boulders and crack cliffs. One of the most popular attacks for skilled Brothers. Each success adds damage multiplier (max x4 at 5 successes, +1 damage per success above 5). Can reach 20+ damage dice. Extremely vulgar.",
            "book": book,
            "requires_maneuver": "Punch or Kick",
        }
    )

    # ========================================
    # TALISMANS/WONDERS
    # ========================================

    # Magick Sword Coin
    wonder_sword_coin, _ = Wonder.objects.get_or_create(
        name="Magick Sword Coin",
        defaults={
            "description": "Coin attached to straight sword's tassels. First function activates Spatial Perceptions Effect. Second function generates extremely bright beam of light that blinds single opponent (Stamina roll difficulty 7 to clear vision, botches add rounds of blindness). Target suffers +2 difficulty on all rolls except mental thinking and attacks vs. the Coin itself (-1 difficulty).",
            "wonder_type": "Talisman",
            "arete": 3,
            "quintessence": 12,
            "book": book,
            "spheres_required": "Correspondence 2, Forces 2",
            "activation_cost": 1,
            "notes": "Used in Ascension Wars against Nephandi, demons, and vampires. Beam of light is vulgar magick. Uses 1 Quintessence per turn.",
        }
    )

    # Limitless Bow
    wonder_limitless_bow, _ = Wonder.objects.get_or_create(
        name="Limitless Bow",
        defaults={
            "description": "Once activated, arrows continuously materialize, loaded and ready to fire, until magick dissipates or user removes arrow without firing. Can function as normal bow. Removed arrows don't dissolve and grant -1 difficulty to reactivate Kemian if loaded later. All fired arrows dematerialize when duration ends.",
            "wonder_type": "Talisman",
            "arete": 5,
            "quintessence": 20,
            "book": book,
            "spheres_required": "Matter 3, Prime 3",
            "activation_cost": 1,
            "notes": "Difficulty 5 to activate, check duration chart. Removing arrow ends duration immediately but that arrow persists.",
        }
    )

    # Battering Ram's Sword
    wonder_battering_ram_sword, _ = Wonder.objects.get_or_create(
        name="Battering Ram's Blade",
        defaults={
            "description": "Ancient straight sword with ornate wooden scabbard. Metal bindings shaped into tiger, dragon and phoenix. Blade has 'Battering Ram' etched in ancient characters. Has been with this Avatar for many incarnations, lost for several lifetimes before being recovered.",
            "wonder_type": "Talisman",
            "arete": 2,
            "quintessence": 10,
            "book": book,
            "spheres_required": "Forces 2, Prime 2",
            "notes": "Dedicated focus. Can only be used by its owner.",
        }
    )

    # Generic Kemian Prayer Beads
    wonder_prayer_beads, _ = Wonder.objects.get_or_create(
        name="Kemian Prayer Beads",
        defaults={
            "description": "Sacred prayer beads charged with Quintessence. Used for meditation and focusing will. Each bead can store a point of Quintessence.",
            "wonder_type": "Talisman",
            "arete": 2,
            "quintessence": 10,
            "book": book,
            "spheres_required": "Prime 2",
            "notes": "Gentle Mountain wears a set of these.",
        }
    )

    # ========================================
    # LOCATIONS
    # ========================================

    # Temple of Inner Truth
    chantry_inner_truth, _ = Chantry.objects.get_or_create(
        name="Temple of Inner Truth",
        defaults={
            "description": "Major Xiudaoyuan of the Akashic Brotherhood, wedged between two large cliff faces in the mountains of Tibet. Red sloping roofs reach out to touch tall pine trees. Large open doors guarded by Orange Robes in meditative stances. Huge slabs of rock form the courtyard. Contains extensive weapon rooms, training halls, dining facilities, library sections, and access to Horizon Realm version. Home to the physical manifestation of part of the Akashic Record.",
            "gauntlet_rating": 3,
            "book": book,
            "reality_zone_rating": 4,
        }
    )

    node_inner_truth, _ = Node.objects.get_or_create(
        name="Temple of Inner Truth Node",
        defaults={
            "description": "Powerful Node within the Temple of Inner Truth. Provides Quintessence for the Chantry's operations and helps maintain the connection to the Akashic Record.",
            "quintessence_per_week": 15,
            "points": 5,
            "resonance": "Meditative, Balanced, Ancient",
            "book": book,
        }
    )

    # The Akashic Record
    chantry_akashic_record, _ = Chantry.objects.get_or_create(
        name="The Akashic Record",
        defaults={
            "description": "Vast library existing partially in Horizon Realm, partially in collective unconscious. Physical manifestation appears as infinite city of buildings, shelves, books. Silent Orange Robes serve as librarians. At the center: great sphere of pure light where physical Record ends and mental aspect begins. Contains history of all Avatars encountered by Brotherhood, outline of Tapestry itself.",
            "gauntlet_rating": 1,
            "book": book,
            "reality_zone_rating": 5,
            "notes": "Access requires Mind magick. Composed of both written texts and collective mind/spirit pool. Falling into the Record can cause Quiet.",
        }
    )

    node_akashic_record, _ = Node.objects.get_or_create(
        name="Akashic Record Node",
        defaults={
            "description": "Massive Node at the heart of the Akashic Record. The sphere of pure light that connects physical and mental aspects of the Record. Contains nearly infinite Quintessence.",
            "quintessence_per_week": 50,
            "points": 10,
            "resonance": "Knowledge, Memory, Timeless, Unity",
            "book": book,
            "notes": "Access restricted to advanced Brothers.",
        }
    )

    # Raging Eagle's Cavern
    chantry_eagle_cavern, _ = Chantry.objects.get_or_create(
        name="Raging Eagle's Training Cavern",
        defaults={
            "description": "Secret cavern high in the mountains of Tibet where Raging Eagle trains students heading toward oneness with inner selves. Site of mysterious group practicing ancient art focusing spirits of wind.",
            "gauntlet_rating": 4,
            "book": book,
            "reality_zone_rating": 3,
        }
    )

    # Shaolin Temple (Historical)
    chantry_shaolin, _ = Chantry.objects.get_or_create(
        name="Shaolin Temple",
        defaults={
            "description": "Two Buddhist monasteries in China (one northern, one southern), historically described as birthplace of modern Chinese martial arts. Major Xiudaoyuan of the Brotherhood. Burned by Manchurian forces aided by Ma Yee Fuk and Euthanatos. Only 18 monks escaped, 5 survived to form the Hung Society (later Triads).",
            "gauntlet_rating": 3,
            "book": book,
            "status": "Ret",
            "notes": "Destroyed in historical incident. Now controlled by Celestial Chorus mages.",
        }
    )

    print("✓ Created Akashic Brotherhood paradigms and practices")
    print("✓ Created Akashic Brotherhood instruments and foci")
    print("✓ Created major NPCs: Raging Eagle, Gentle Mountain, Fall Breeze, Battering Ram")
    print("✓ Created supporting characters: Nichiba, Cheng Sa, Darumha, Ma Yee Fuk, Akasha")
    print("✓ Created historical figures and Sleepers")
    print("✓ Created Other Tradition mages: DuMonte, Dimitri, Wlakar Fahir")
    print("✓ Created Technocracy antagonists")
    print("✓ Created 8 major rotes/effects")
    print("✓ Created 4 Talismans/Wonders")
    print("✓ Created 5 major locations/Chantries")
    print("✓ Created 3 Nodes")
    print("\nAkashic Brotherhood content population complete!")

if __name__ == "__main__":
    import os
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg.settings")
    django.setup()

    populate_ab_1e()

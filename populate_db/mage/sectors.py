from locations.models.mage.sector import Sector

# ====================
# GRID SECTORS
# ====================

# Standard Public Grid - The "Sheep Pens"
public_grid = Sector.objects.get_or_create(
    name="The Grid - Public Space",
    defaults={
        "description": "The vast expanse of the public internet where over a billion users access social media, entertainment, and information. Dismissed by old-school 'spinners' but containing more data than all written records before 2000.",
        "sector_class": "grid",
        "access_level": "free",
        "power_rating": 5,
        "security_level": 0,
        "size_rating": 6,  # Region-scale
        "estimated_users": 1000000000,  # Over a billion
        "aro_density": "overwhelming",
        "aro_count": 999999999,  # Effectively unlimited
        "administrator": "Collective - No Single Owner",
        "notable_features": """- Billions of AROs documenting world events
- Social media feeds from every platform
- Real-time data streams
- Search engine indexed content
- Public forums and communities""",
        "hazards": "Information overload, trolls, viral misinformation, data scrapers",
    }
)[0]
public_grid.add_source("The Operative's Dossier", 66)

# Warzone - Combat Grid Sector
warzone_gladiator = Sector.objects.get_or_create(
    name="Gladiator Arena Alpha",
    defaults={
        "description": "A Warzone Grid Sector designed for Enlightened combatants. Massive destructive Program-users compete in tournaments without breaking down the sector due to power surges.",
        "sector_class": "warzone",
        "access_level": "restricted",
        "power_rating": 7,  # Higher than standard
        "security_level": 5,
        "size_rating": 3,  # Block-scale arena
        "requires_password": True,
        "password_hint": "Winners only - prove your worth",
        "approved_users": "Technocratic Combatants\nVirtual Adepts - Combat Division\nApproved Tournament Fighters",
        "estimated_users": 500,
        "aro_density": "dense",
        "administrator": "RAMbo Coalition",
        "difficulty_modifier": -1,  # Easier for combat magic
        "notable_features": """- Reinforced data structures for massive firepower
- Real-time damage simulation
- Spectator AROs for audience
- Leaderboards and rankings
- Automated healing zones""",
        "hazards": "Aggressive combatants, stray fire, arena hazards, permanent icon damage",
    }
)[0]
warzone_gladiator.add_source("The Operative's Dossier", 66)

# ====================
# C-SECTORS (Constrained)
# ====================

# Spy's Demise - Speakeasy
spys_demise = Sector.objects.get_or_create(
    name="Spy's Demise",
    defaults={
        "description": "A Web-famous speakeasy where patrons exchange newspapers and notes that translate into petabytes of data. The rules of the sector enforce film noir aesthetics - no smartphones, only cigarettes and fedoras.",
        "sector_class": "c_sector",
        "access_level": "restricted",
        "power_rating": 5,
        "security_level": 7,
        "size_rating": 2,  # Single building
        "requires_password": True,
        "password_hint": "Slip the bartender a headline",
        "genre_theme": "Film Noir / Speakeasy",
        "constraints": """GENRE ENFORCEMENT PROTOCOLS:
- No modern technology visible (smartphones, tablets, etc.)
- All data exchange through period-appropriate metaphors
- Dress code: 1940s attire mandatory
- Communication: Hardboiled dialogue preferred
- Weapons: Period appropriate only (revolvers, not plasma rifles)

VIOLATION: Using anachronistic tech is vulgar with witnesses (+2 difficulty)""",
        "estimated_users": 150,
        "aro_density": "moderate",
        "administrator": "The Bartender (Unknown identity)",
        "difficulty_modifier": 1,  # Harder for incompatible paradigms
        "notable_features": """- Newspaper headlines translate to data packets
- Circled articles become files
- Back room for private exchanges
- Jazz band provides atmospheric cover
- Bourbon flows freely (non-digital, somehow)""",
        "hazards": "Genre purists, information brokers, double agents, memory wipes for violations",
    }
)[0]
spys_demise.add_source("The Operative's Dossier", 67)

# Technocratic SRVRZ
tech_vault = Sector.objects.get_or_create(
    name="Iteration X Research Vault 7",
    defaults={
        "description": "A Secured and Restricted Virtual Reality Zone (SRVRZ) of the Technocratic Union. Constraint protocols enforce strict scientific methodology - superstition-based magic regularly fails here.",
        "sector_class": "c_sector",
        "access_level": "restricted",
        "power_rating": 5,
        "security_level": 10,  # Maximum security
        "size_rating": 3,
        "requires_password": True,
        "approved_users": "Iteration X - Authorized Personnel\nUnion Oversight - Level 5+\nApproved Researchers Only",
        "genre_theme": "Hard Science / Laboratory",
        "constraints": """CONSTRAINT PROTOCOLS (SRVRZ):
- Scientific methodology REQUIRED
- Effects must follow Technocratic paradigm
- Tradition magic faces +3 difficulty
- All effects logged and monitored
- Superstitious implements fail (wands, crystals, etc.)
- Lab coats and credentials mandatory""",
        "estimated_users": 50,
        "aro_density": "dense",
        "aro_count": 10000,  # Extensive documentation
        "administrator": "Iteration X - Time-Motion Managers",
        "difficulty_modifier": -2,  # Easier for Technocrats
        "paradox_risk_modifier": 2,  # Higher for Reality Deviants
        "notable_features": """- Extensive research databases
- Experimental device schematics
- Prototype testing chambers
- AI-assisted calculation tools
- Quantum computing resources""",
        "hazards": "Automated defense systems, HIT Marks, surveillance, immediate de-rez for intruders",
    }
)[0]
tech_vault.add_source("The Operative's Dossier", 67)

# ====================
# CORRUPTED WEB
# ====================

corrupted_zone = Sector.objects.get_or_create(
    name="Whiteout Crater Z-17",
    defaults={
        "description": "A destroyed sector where data, structure, and form have been mangled beyond recognition. All attempts at reformatting have failed. Programs generate Paradox here, and the sector resists everything.",
        "sector_class": "corrupted",
        "access_level": "free",  # Can't be secured - too broken
        "power_rating": 6,  # Unstable - sometimes higher
        "security_level": 0,
        "size_rating": 3,
        "is_reformattable": False,
        "corruption_level": 10,  # Completely corrupted
        "estimated_users": 5,  # Only Marauders dare enter
        "aro_density": "sparse",
        "administrator": "None - Anarchic Space",
        "difficulty_modifier": 0,
        "paradox_risk_modifier": 3,  # Always generates Paradox
        "has_lag": True,
        "notable_features": """- Mangled data structures
- Reality breaks down randomly
- Time flows erratically
- Ghostly echoes of former users
- Fragments of destroyed AROs""",
        "hazards": "EXTREME DANGER: All Programs generate Paradox. Whiteout risk constant. 89 fatalities from reformat attempts. Recommend AVOID.",
    }
)[0]
corrupted_zone.add_source("The Operative's Dossier", 66)

hung_sector = Sector.objects.get_or_create(
    name="Frozen Moment Sector",
    defaults={
        "description": "A Hung Sector - a rare type of Corrupted Web that resists the flow of time itself. Events loop, freeze, or skip unpredictably. Increasingly rare but utterly haunting.",
        "sector_class": "corrupted",
        "access_level": "free",
        "power_rating": 6,
        "corruption_level": 10,
        "is_reformattable": False,
        "temporal_instability": True,
        "time_dilation": 0.00,  # Time effectively stopped
        "size_rating": 2,
        "estimated_users": 0,
        "aro_density": "sparse",
        "administrator": "None",
        "paradox_risk_modifier": 4,
        "notable_features": """- Time loops randomly
- Users frozen in place
- Actions replay infinitely
- Temporal echoes visible
- Past and present overlap""",
        "hazards": "Temporal prison risk, causality violations, extreme Paradox, may never escape",
    }
)[0]
hung_sector.add_source("The Operative's Dossier", 66)

# ====================
# JUNKLANDS
# ====================

abandoned_hub = Sector.objects.get_or_create(
    name="Echo Station Beta",
    defaults={
        "description": "A former administrative hub, now abandoned. The sector still carries out the motions of its previous operations - ghost processes running, automated messages to nowhere. Visitors report feeling haunted.",
        "sector_class": "junklands",
        "access_level": "free",
        "power_rating": 5,
        "security_level": 0,
        "size_rating": 3,
        "corruption_level": 6,
        "is_reformattable": True,  # Technically, but difficult
        "estimated_users": 20,
        "aro_density": "moderate",
        "administrator": "None - Abandoned",
        "difficulty_modifier": 1,
        "paradox_risk_modifier": 1,
        "notable_features": """- Automated processes still running
- Empty administrator offices
- Login screens with no users
- Echoing data transmissions
- Preserved but lifeless""",
        "hazards": "Eerie atmosphere, malfunctioning security, ghost processes, psychological effects",
    }
)[0]
abandoned_hub.add_source("The Operative's Dossier", 67)

# ====================
# HAUNTS
# ====================

digital_graveyard = Sector.objects.get_or_create(
    name="Memorial Park - Social Media Graveyard",
    defaults={
        "description": "A collection of memorial pages from deceased social media users. Content manifests as looping video feeds, howling ghost-like EDEs, static statues, and fractal pathways of tears. Not peaceful - deeply disturbing.",
        "sector_class": "haunts",
        "access_level": "free",
        "power_rating": 5,
        "security_level": 0,
        "size_rating": 4,
        "estimated_users": 1000,  # Mourners and data archaeologists
        "aro_density": "dense",
        "aro_count": 50000,  # One per deceased user
        "administrator": "Automated - No living admin",
        "difficulty_modifier": 0,
        "paradox_risk_modifier": 1,
        "notable_features": """- Complete social media histories of the dead
- Looping final posts
- Photo galleries
- Video feeds
- Connection maps
- Death date markers""",
        "hazards": "CAUTION: Psychological trauma risk. Ghost-like EDEs aggressive. Near Entropic Space boundary. Bring backup.",
    }
)[0]
digital_graveyard.add_source("The Operative's Dossier", 70)

# ====================
# TRASH SECTOR
# ====================

dev_null = Sector.objects.get_or_create(
    name="/dev/null - The Trash Sector",
    defaults={
        "description": "Where deleted data goes to die. Sysadmins have piped garbage here for decades, assuming it vanishes. It doesn't. A literal mountain range of discarded data, crushing and dangerous. If dataphytes ever find this place, the entire Web dies.",
        "sector_class": "trash",
        "access_level": "free",
        "power_rating": 5,
        "security_level": 0,
        "size_rating": 6,  # Massive - region scale
        "estimated_users": 50,  # Data scavengers and archaeologists
        "aro_density": "overwhelming",
        "aro_count": 999999999,  # Essentially infinite garbage
        "administrator": "None - Anarchic Dumping Ground",
        "difficulty_modifier": 1,
        "paradox_risk_modifier": 0,
        "notable_features": """- Mountains of deleted files
- Compressed data formations
- Streams of discarded code
- Fragmented memories
- Lost information""",
        "hazards": "EXTREME DANGER: Collapsing data piles cause lethal damage. Missing information occasionally recoverable. Dataphyte risk CATASTROPHIC.",
    }
)[0]
dev_null.add_source("The Operative's Dossier", 67)

# ====================
# STREAMLAND
# ====================

streamland = Sector.objects.get_or_create(
    name="Streamland",
    defaults={
        "description": "The Web's largest Free Sector. Between Grid and Trash, every data stream flows through here like rain. Device streams persist briefly before falling into /dev/null. No single owner - it governs itself.",
        "sector_class": "streamland",
        "access_level": "free",
        "power_rating": 5,
        "security_level": 0,
        "size_rating": 6,  # Enormous and growing
        "estimated_users": 10000000,  # Millions accessing streams
        "aro_density": "overwhelming",
        "data_flow_rate": "torrent",
        "administrator": "None - Self-Governing / Unknown",
        "difficulty_modifier": 0,
        "notable_features": """- Every Web stream visible
- Data falls like rain
- Temporary access to any device feed
- Camera phones, IoT devices, medical monitors
- Video games, television, streaming services
- Find anything with Perception + Computer (diff 7-8)""",
        "hazards": "Information overload, temporary data only, finding specific streams difficult, no privacy",
    }
)[0]
streamland.add_source("The Operative's Dossier", 67)

# ====================
# VIRGIN WEB
# ====================

virgin_expanse = Sector.objects.get_or_create(
    name="The Unformatted Expanse",
    defaults={
        "description": "The Virgin Web - raw, unformatted digital space. The wide-open sea with no sailors, no pirates, just untouched nature. Few have the knowledge to reach it, fewer still to do anything meaningful here.",
        "sector_class": "virgin",
        "access_level": "free",
        "power_rating": 5,
        "security_level": 0,
        "size_rating": 6,  # Infinite
        "estimated_users": 10,  # Only the most skilled
        "aro_density": "none",
        "administrator": "None - Primordial Space",
        "difficulty_modifier": 0,
        "notable_features": """- Unformatted possibility
- Raw digital substrate
- Potential for creation
- No existing structures
- Pure information space""",
        "hazards": "Requires advanced Data/Correspondence to access, easy to get lost, no landmarks, no help available",
    }
)[0]
virgin_expanse.add_source("The Operative's Dossier", 66)

# ====================
# SPECIAL LOCATIONS
# ====================

# Dark Web Access Point
dark_web_hub = Sector.objects.get_or_create(
    name="Onion Router Gateway",
    defaults={
        "description": "An access point to the Dark Web - the encrypted, anonymized portions of the Digital Web. Requires special software to access. Behind these gates lie both activists and monsters.",
        "sector_class": "c_sector",
        "access_level": "restricted",
        "power_rating": 5,
        "security_level": 8,
        "size_rating": 2,
        "requires_password": True,
        "password_hint": "Onion routing required - multiple layers of encryption",
        "genre_theme": "Encrypted Anonymous Network",
        "constraints": """ANONYMIZATION PROTOCOLS:
- Traffic encryption mandatory
- User identification blocked
- GPS spoofing active
- Multiple proxy layers
- Traceable connections rejected""",
        "estimated_users": 100000,
        "aro_density": "moderate",
        "administrator": "Distributed - No Central Authority",
        "difficulty_modifier": 0,
        "notable_features": """- Onion router nodes
- Encrypted marketplaces
- Anonymous forums
- Whistleblower dead drops
- Hidden service directories""",
        "hazards": "CAUTION: Illegal activity, Reality Deviants (Virtual Adepts, Glass Walkers), Nephandi lairs, botnets, surveillance risk",
    }
)[0]
dark_web_hub.add_source("The Operative's Dossier", 70-71)

# Ultima Thule Research Sector
ultima_thule_sector = Sector.objects.get_or_create(
    name="Ultima Thule Research Network",
    defaults={
        "description": "The isolated Digital Web presence of Ultima Thule Antarctic Research Station. Communication with other Constructs is nearly impossible due to spatial distortions and time dilation. Messages arrive weeks late and often garbled.",
        "sector_class": "c_sector",
        "access_level": "restricted",
        "power_rating": 6,  # High primal energy
        "security_level": 9,
        "size_rating": 1,  # Small, isolated
        "requires_password": True,
        "approved_users": "Ultima Thule Permanent Staff\nVoid Engineers - Authorized Researchers\nProgenitor - Approved Projects",
        "temporal_instability": True,
        "time_dilation": 0.25,  # Messages arrive very late
        "estimated_users": 10,
        "aro_density": "sparse",
        "administrator": "Dr. Charlot Berg / Lt. Lilian Okoye",
        "difficulty_modifier": -1,  # Easier for Technocrats
        "notable_features": """- Research databases
- EDE monitoring logs
- Wormhole generator controls
- Sample analysis data
- Distorted communication channels""",
        "hazards": "Severe communication delay, messages garbled, temporal distortion, isolation, may lose contact entirely",
    }
)[0]
ultima_thule_sector.add_source("The Operative's Dossier", 22-24)

# Arcology X Sector
arcology_x_sector = Sector.objects.get_or_create(
    name="Arcology X Digital Infrastructure",
    defaults={
        "description": "The Digital Web presence of South Korea's Arcology X Project. Integrated with Sejong City's IoT infrastructure, providing control over millions of devices. Fastest internet speeds in the world.",
        "sector_class": "c_sector",
        "access_level": "restricted",
        "power_rating": 5,
        "security_level": 8,
        "size_rating": 4,  # Neighborhood scale
        "requires_password": True,
        "approved_users": "Elemental Dragon Methodologies\nSejong City Authorized Personnel\nUnion Oversight",
        "genre_theme": "Smart City / IoT Network",
        "estimated_users": 300000,  # Sejong City population
        "aro_density": "overwhelming",
        "aro_count": 10000000,  # Every device in Sejong
        "administrator": "Yellow/Earth Dragons - NWO",
        "difficulty_modifier": -1,
        "notable_features": """- IoT device control (ALL city devices)
- Traffic management systems
- Automated drone networks (SDY)
- Surveillance feeds (every centimeter)
- Resource distribution
- Citizen happiness monitoring""",
        "hazards": "Total surveillance, potential TE attacks (Noah Campeau), Virtual Adept intrusions, system havoc risk",
    }
)[0]
arcology_x_sector.add_source("The Operative's Dossier", 13-15)

print("Digital Web Sectors populated successfully!")
print(f"Total sectors created: {Sector.objects.count()}")

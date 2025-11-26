"""
Leadership and Political Hierarchy Script

Assigns political positions and leadership roles to characters.
This establishes the power structure within each supernatural faction.
"""

from characters.models.core import CharacterModel
from game.models import Chronicle, SettingElement


def populate_leadership():
    """Assign leadership positions and political roles."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    print("Establishing political hierarchy...")

    # =========================================================================
    # VAMPIRE HIERARCHY
    # =========================================================================
    setup_vampire_hierarchy(chronicle)

    # =========================================================================
    # WEREWOLF HIERARCHY
    # =========================================================================
    setup_werewolf_hierarchy(chronicle)

    # =========================================================================
    # MAGE HIERARCHY
    # =========================================================================
    setup_mage_hierarchy(chronicle)

    # =========================================================================
    # WRAITH HIERARCHY
    # =========================================================================
    setup_wraith_hierarchy(chronicle)

    # =========================================================================
    # CHANGELING HIERARCHY
    # =========================================================================
    setup_changeling_hierarchy(chronicle)

    # =========================================================================
    # DEMON HIERARCHY
    # =========================================================================
    setup_demon_hierarchy(chronicle)

    # =========================================================================
    # HUNTER HIERARCHY
    # =========================================================================
    setup_hunter_hierarchy(chronicle)

    # =========================================================================
    # MUMMY HIERARCHY
    # =========================================================================
    setup_mummy_hierarchy(chronicle)

    print("Political hierarchy established!")


def setup_vampire_hierarchy(chronicle):
    """Set up Camarilla positions for Seattle."""
    print("\nVampire Hierarchy:")

    # Create setting element for the hierarchy
    SettingElement.objects.get_or_create(
        name="Seattle Camarilla Court",
        defaults={
            "description": """**Seattle's Camarilla Power Structure**

**Prince:** Lady Katrina Valdez (Ventrue, 7th Generation)
- Has ruled Seattle since 1952
- Known for her iron will and political acumen
- Maintains strict Masquerade enforcement

**Seneschal:** Marcus Blackwood (Tremere)
- Handles nightly court administration
- Liaison between Prince and Primogen

**Sheriff:** Viktor Kozlov (Brujah)
- Enforces the Prince's justice
- Commands a team of deputized Kindred

**Primogen Council:**
- Ventrue: Lord Sebastian Drake
- Tremere: Regent Helena Cross
- Toreador: Madame Celeste
- Nosferatu: "The Informant" (identity secret)
- Malkavian: Dr. Alice Chen
- Brujah: Jackson "Ironjaw" Thompson
- Gangrel: Rachel Nightrunner (rarely attends)

**Keeper of Elysium:** Victoria Chen
- Maintains the Seattle Art Museum Elysium
- Enforces Elysium traditions

**Harpy:** Sebastian Marsh
- Chronicles status and boons
- Arbiter of social standing"""
        }
    )
    chronicle.setting_elements.add(
        SettingElement.objects.get(name="Seattle Camarilla Court")
    )
    print("  Created Seattle Camarilla Court hierarchy")


def setup_werewolf_hierarchy(chronicle):
    """Set up Sept positions for Seattle area."""
    print("\nWerewolf Hierarchy:")

    SettingElement.objects.get_or_create(
        name="Sept of the Cascades",
        defaults={
            "description": """**Sept of the Cascades Leadership**

**Sept Alpha:** Howls-at-Dawn (Silver Fang Elder)
- Has led the sept for over 80 years
- Survivor of countless Wyrm battles
- Respected across tribal lines

**Warder:** Breaks-the-Silence (Get of Fenris Ahroun)
- Protector of the caern
- Commands the caern's defenses

**Master of the Rite:** Speaks-to-Ancestors (Uktena Theurge)
- Keeper of sacred rituals
- Maintains relations with local spirits

**Gatekeeper:** Cloud-Walker (Wendigo Ragabash)
- Controls access to the caern
- Watches for Wyrm infiltration

**Master of the Challenge:** Thunder-Striker (Get of Fenris)
- Oversees challenges and disputes
- Maintains Garou traditions

**Tribal Representatives:**
- Silver Fangs: Howls-at-Dawn (also Alpha)
- Get of Fenris: Breaks-the-Silence
- Shadow Lords: Storm's Fury
- Bone Gnawers: Cracks-the-Code
- Children of Gaia: Gaia's Whisper
- Glass Walkers: Digital-Paw
- Uktena: Speaks-to-Ancestors
- Wendigo: Cloud-Walker"""
        }
    )
    chronicle.setting_elements.add(
        SettingElement.objects.get(name="Sept of the Cascades")
    )
    print("  Created Sept of the Cascades hierarchy")


def setup_mage_hierarchy(chronicle):
    """Set up Tradition Chantry positions for Seattle."""
    print("\nMage Hierarchy:")

    SettingElement.objects.get_or_create(
        name="Seattle Tradition Council",
        defaults={
            "description": """**Seattle Tradition Council**

**Deacon (Council Head):** Dr. Helena Cross (Order of Hermes)
- Coordinates inter-Tradition affairs
- Liaison with other supernatural groups
- Rotates every 3 years

**Tradition Representatives:**
- Order of Hermes: Dr. Helena Cross (House Bonisagus)
- Virtual Adepts: James Chen
- Verbena: Elena Vasquez
- Cult of Ecstasy: Marcus "Bliss" Thompson
- Dreamspeakers: Sarah Crow-Feather
- Euthanatos: Dr. Victor Shade (observer status)
- Celestial Chorus: Father Michael Brennan
- Akashic Brotherhood: Master Lin Wei
- Sons of Ether: Professor Sterling

**Chantry Positions:**
- Cross House Regent: Dr. Helena Cross
- Node Keeper (Fremont): Elena Vasquez
- Node Keeper (Gas Works): James Chen
- Library Master: Professor Sterling
- Sentinel: Master Lin Wei

**Technocracy Known Presence:**
- NWO Cell suspected downtown
- Iteration X presence at tech companies
- Progenitor lab rumored near UW Medical"""
        }
    )
    chronicle.setting_elements.add(
        SettingElement.objects.get(name="Seattle Tradition Council")
    )
    print("  Created Seattle Tradition Council hierarchy")


def setup_wraith_hierarchy(chronicle):
    """Set up Hierarchy positions for Seattle's Shadowlands."""
    print("\nWraith Hierarchy:")

    SettingElement.objects.get_or_create(
        name="Seattle Necropolis",
        defaults={
            "description": """**Seattle Necropolis Hierarchy**

**Anacreon (City Governor):** Lord Ashworth (Masquer)
- Appointed by the Hierarchy
- Maintains order in Seattle's Shadowlands
- Old soul, pre-dates Seattle itself

**Regent of the Underworld Domains:**
- Underground Seattle: The Pioneer (Haunter)
- Waterfront: Captain Gray (Sandman)
- Hospital District: Margaret Sullivan (Pardoner) - unofficial

**Circle Leaders:**
- The Unquiet: Thomas Ashworth (Masquer)
- The Watch: Detective Morrison (Monitor)
- The Lost Generation: Emma Thornton (Puppeteer)

**Ferryman Contact:** Old Samuel
- Guides souls across the Tempest
- Neutral in Hierarchy politics

**Renegade Presence:**
- Several small Renegade groups operate outside Hierarchy control
- Most are simply avoiding the politics, not opposing the system

**Spectral Threats:**
- The Tempest is unusually active
- Reports of organized Spectre activity
- Nihils have been spotted forming near trauma sites"""
        }
    )
    chronicle.setting_elements.add(
        SettingElement.objects.get(name="Seattle Necropolis")
    )
    print("  Created Seattle Necropolis hierarchy")


def setup_changeling_hierarchy(chronicle):
    """Set up Court positions for Seattle's Kithain."""
    print("\nChangeling Hierarchy:")

    SettingElement.objects.get_or_create(
        name="Court of the Silver Rain",
        defaults={
            "description": """**Court of the Silver Rain (Seelie Court)**

**Duke:** Silvermist (Sidhe, House Fiona)
- Rules Seattle's Seelie fae
- Known for wisdom and patience
- Maintains peace between courts

**Duchess (Consort):** Lady Moonshadow (Sidhe, House Eiluned)
- Master of court intrigue
- Keeper of fae secrets

**Court Positions:**
- Chancellor: Baron Thornwick (Sidhe, House Gwydion)
- Herald: Swift-Voice (Eshu)
- Marshal: Sir Ironoath (Troll)
- Keeper of the Freehold: Rowan Brightwater (Satyr)

**Unseelie Shadow Court:**
- Count Nightshade (Sidhe, House Balor) - leads the local Unseelie
- Maintains uneasy truce with Seelie Court
- Rules from the Midnight Carnival Freehold

**Notable Kith Representatives:**
- Pooka: Jack "Patches" McGee
- Redcap: Bloody Mary (feared enforcer)
- Sluagh: The Whisper (information broker)
- Boggan: Mama Rose (freehold caretaker)
- Nocker: Geargrind (artificer)

**Threats:**
- Dauntain activity on the rise
- Banality pressure increasing
- Thallain sightings in the deep Dreaming"""
        }
    )
    chronicle.setting_elements.add(
        SettingElement.objects.get(name="Court of the Silver Rain")
    )
    print("  Created Court of the Silver Rain hierarchy")


def setup_demon_hierarchy(chronicle):
    """Set up Fallen factions for Seattle."""
    print("\nDemon Hierarchy:")

    SettingElement.objects.get_or_create(
        name="Seattle Fallen Factions",
        defaults={
            "description": """**Seattle's Fallen Factions**

Unlike other supernaturals, the Fallen have no formal hierarchy.
Instead, they organize into loose factions based on philosophy:

**Reconcilers (Largest faction):**
- Seek redemption and meaning
- Work to protect humanity
- Leader: Zephyrus (Malefactor)
- Meet at various churches and temples

**Luciferans:**
- Loyal to Lucifer's original vision
- Seek to free humanity from God's tyranny
- Local contact: Seraph (Devil)
- Very secretive

**Faustians:**
- Work within mortal society
- Build power through pacts and influence
- Marcus Wells (Fiend) has connections
- Operate through business networks

**Raveners:**
- Embrace destruction and chaos
- Dangerous to all, including other Fallen
- No organized presence (thankfully)

**Cryptics:**
- Seek answers to the great mysteries
- Why were they imprisoned? Why released now?
- Small but growing faction

**Known Earthbound:**
- One ancient Earthbound was recently destroyed/bound beneath Seattle
- Others may exist in the region
- All factions consider Earthbound existential threats

**Thrall Networks:**
- Each faction maintains mortal followers
- Faith is currency and sustenance
- Competition for thralls can cause conflict"""
        }
    )
    chronicle.setting_elements.add(
        SettingElement.objects.get(name="Seattle Fallen Factions")
    )
    print("  Created Seattle Fallen Factions")


def setup_hunter_hierarchy(chronicle):
    """Set up Hunter cell structures for Seattle."""
    print("\nHunter Hierarchy:")

    SettingElement.objects.get_or_create(
        name="Seattle Hunter Network",
        defaults={
            "description": """**Seattle Hunter Network**

Hunters operate in cells with minimal formal hierarchy.
The network is deliberately decentralized for security.

**Major Cells:**

**The Vigil** (Primary PC cell)
- Leaders: Sarah Mitchell, David Okonkwo
- Focus: Investigation and rescue operations
- Specialties: Research, surveillance, extraction
- Resources: Moderate funding, good intel network

**The Network**
- Leader: Marcus Cole
- Focus: Information gathering and distribution
- Specialties: Hacking, surveillance, communication
- Resources: Excellent technology, limited combat capability

**Support Group**
- Leader: Jennifer Hayes
- Focus: Helping survivors of supernatural encounters
- Specialties: Counseling, safe houses, witness protection
- Resources: Medical supplies, safe houses

**Independent Hunters:**
- Father Michael Brennan (lone wolf, vampire specialist)
- The Old Man (identity unknown, werewolf hunter)
- Doc Simmons (retired, advises new hunters)

**External Contacts:**
- FBI contacts (Agent Morrison - possible Imbued)
- Police connections (Detective Chen - unknowing ally)
- Medical examiner (Dr. Patel - covers unusual deaths)

**Known Threats:**
- Vampire nest at Club Nocturne (partially cleared)
- Something in the forests east of city
- Rumors of "demon worshippers" downtown"""
        }
    )
    chronicle.setting_elements.add(
        SettingElement.objects.get(name="Seattle Hunter Network")
    )
    print("  Created Seattle Hunter Network")


def setup_mummy_hierarchy(chronicle):
    """Set up Amenti organization for Seattle."""
    print("\nMummy Hierarchy:")

    SettingElement.objects.get_or_create(
        name="Seattle Web of Faith",
        defaults={
            "description": """**Seattle's Amenti Presence**

The Reborn maintain a loose organization focused on their
eternal mission to restore Ma'at.

**Local Amenti:**
- Amenhotep IV (Sefekhi) - eldest local mummy
- Dr. Constance Grey (Mesektet) - scholarly focus
- Sekhemib (Khri-habi) - recently recovered, unstable

**Cults of the Faithful:**
- Temple of the Eternal Sun (Amenhotep's cult)
- House of Scrolls (academic focus)
- Keepers of Ma'at (balance and justice)
- Lions of Sekhmet (warrior tradition)

**Sacred Sites:**
- Seattle Art Museum (Egyptian collection watched)
- Underground Seattle (ancient artifacts hidden)
- Private collections (monitored for dangerous items)

**Current Concerns:**
- Apophis cult activity detected
- Stolen artifacts appearing on black market
- Bane Mummies rumored in the region
- One mummy (Sekhemib) recently had mental break

**Relations with Others:**
- Vampires: Cautious neutrality
- Mages: Occasional cooperation on mystical matters
- Werewolves: Shared concern about corruption
- Wraiths: Complex (mummies and ghosts have history)

**Hekau Masters:**
- Amenhotep: Celestial, Nomenclature
- Constance: Alchemy, Necromancy
- Each cult has its specialists"""
        }
    )
    chronicle.setting_elements.add(
        SettingElement.objects.get(name="Seattle Web of Faith")
    )
    print("  Created Seattle Web of Faith")


if __name__ == "__main__":
    populate_leadership()

"""
Hunter item population script for Seattle Test Chronicle.

Creates HunterGear (mundane equipment) and HunterRelics (supernatural items) for
the Seattle hunter network.
"""

from accounts.models import Profile
from game.models import Chronicle
from items.models.hunter import HunterGear, HunterRelic


def populate_hunter_items():
    """Create all Hunter items for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # HUNTER GEAR - WEAPONS
    # =========================================================================

    # Standard Hunting Loadout
    combat_shotgun, created = HunterGear.objects.get_or_create(
        name="Network Combat Shotgun",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A Remington 870 modified for hunting supernatural threats.
The shotgun has been fitted with an extended magazine, improved sights, and
a heat shield for sustained firing. The stock has been carved with protective
symbols by hunters who believe in such things.

The network maintains several of these shotguns as standard issue for
combat operations. Each weapon is tracked and maintained to ensure reliability.

Silver shot, wooden slugs, and incendiary rounds are kept in separate pouches
for quick loading against different targets.""",
            "gear_type": "weapon",
            "damage": "8 dice lethal",
            "range": "20 yards",
            "rate": "1",
            "capacity": "8+1",
            "concealability": "Trench coat",
            "availability": 3,
            "legality": "restricted",
            "requires_training": True,
        },
    )
    if created:
        print(f"  Created Hunter Gear: {combat_shotgun.name}")

    # Silvered Melee Weapons
    silver_machete, created = HunterGear.objects.get_or_create(
        name="Silver-Edged Machete",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A heavy machete with a silver-plated edge, effective against
supernatural creatures vulnerable to the metal. The blade is practical rather
than elegant - it's a tool for killing, not display.

Michael O'Brien produces these at his garage, electroplating standard machetes
with silver and sharpening them to a razor edge. The process isn't cheap, but
the results speak for themselves.

Each hunter who carries one knows to maintain the silver plating regularly -
contact with blood and other fluids can degrade the coating.""",
            "gear_type": "weapon",
            "damage": "Str+3 lethal, aggravated to vulnerable targets",
            "range": "Melee",
            "rate": "N/A",
            "capacity": "N/A",
            "concealability": "Jacket",
            "availability": 3,
            "legality": "legal",
            "requires_training": False,
        },
    )
    if created:
        print(f"  Created Hunter Gear: {silver_machete.name}")

    # Special Ammunition Supply
    special_ammo, created = HunterGear.objects.get_or_create(
        name="Specialized Ammunition Cache",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A supply of specialized ammunition for various targets:
silver bullets for werewolves, wooden-tipped rounds for vampires, cold iron
shot for faeries, and salt-filled shells for spirits.

The network maintains a central supply that can be drawn upon for operations.
Each type requires specific manufacturing techniques, making them expensive
and time-consuming to produce.

Hunters are expected to account for ammunition used and report on its
effectiveness - data that helps refine future production.""",
            "gear_type": "weapon",
            "damage": "Varies by ammunition type",
            "range": "Varies by weapon used",
            "rate": "N/A",
            "capacity": "Multiple types available",
            "concealability": "Pocket",
            "availability": 4,
            "legality": "restricted",
            "requires_training": False,
        },
    )
    if created:
        print(f"  Created Hunter Gear: {special_ammo.name}")

    # =========================================================================
    # HUNTER GEAR - SURVEILLANCE
    # =========================================================================

    # Night Vision Equipment
    night_vision, created = HunterGear.objects.get_or_create(
        name="Enhanced Night Vision System",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Military-grade night vision goggles acquired through network
contacts. The system includes thermal overlay capability, allowing hunters to
track heat signatures as well as amplify available light.

The goggles have been modified to accommodate helmets and can be used with
one eye while maintaining normal vision with the other. Battery life is
approximately eight hours of continuous use.

The network has three sets available for loan, with priority given to
operations in low-light conditions.""",
            "gear_type": "surveillance",
            "damage": "",
            "range": "100 yards effective",
            "rate": "",
            "capacity": "",
            "concealability": "Bag",
            "availability": 4,
            "legality": "restricted",
            "requires_training": True,
        },
    )
    if created:
        print(f"  Created Hunter Gear: {night_vision.name}")

    # Monitoring Equipment
    surveillance_kit, created = HunterGear.objects.get_or_create(
        name="Remote Surveillance Package",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A kit containing wireless cameras, audio bugs, and motion
sensors that can be deployed for long-term observation. The equipment
transmits to a central monitoring station using encrypted frequencies.

Alex Chen manages the network's electronic surveillance operations, monitoring
feeds from multiple deployed units. The equipment is regularly swept for
compromise and updated as technology advances.

Standard deployment includes three cameras, six audio pickups, and four
motion sensors - enough to cover a typical building or outdoor area.""",
            "gear_type": "surveillance",
            "damage": "",
            "range": "500 feet transmission",
            "rate": "",
            "capacity": "",
            "concealability": "Briefcase",
            "availability": 3,
            "legality": "legal",
            "requires_training": True,
        },
    )
    if created:
        print(f"  Created Hunter Gear: {surveillance_kit.name}")

    # EMF Detector
    emf_detector, created = HunterGear.objects.get_or_create(
        name="Modified EMF Detector",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """An electromagnetic field detector modified to detect
supernatural presences. The device responds to the energies associated with
ghosts, certain vampiric disciplines, and magical effects.

The detector isn't infallible - it produces false positives near electrical
equipment and can miss subtle supernatural activity. However, strong
presences reliably trigger the device.

Hunters learn to use the EMF detector in conjunction with other senses
rather than relying on it exclusively.""",
            "gear_type": "surveillance",
            "damage": "",
            "range": "30 feet",
            "rate": "",
            "capacity": "",
            "concealability": "Pocket",
            "availability": 2,
            "legality": "legal",
            "requires_training": False,
        },
    )
    if created:
        print(f"  Created Hunter Gear: {emf_detector.name}")

    # =========================================================================
    # HUNTER GEAR - MEDICAL
    # =========================================================================

    # Field Medical Kit
    medical_kit, created = HunterGear.objects.get_or_create(
        name="Hunter Medical Kit",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A comprehensive medical kit designed for treating injuries
common to supernatural encounters. The kit includes standard first aid supplies
plus specialized items: silver nitrate for cauterizing werewolf bites, holy
water for vampire wounds, and broad-spectrum antivenins.

Dr. Sarah Mitchell maintains the medical supplies at Aegis House 1, restocking
them regularly and updating the kit based on field reports of effective
treatments.

Every team carries a medical kit on operations. Training in its use is
mandatory for all network members.""",
            "gear_type": "medical",
            "damage": "",
            "range": "",
            "rate": "",
            "capacity": "",
            "concealability": "Bag",
            "availability": 2,
            "legality": "legal",
            "requires_training": True,
        },
    )
    if created:
        print(f"  Created Hunter Gear: {medical_kit.name}")

    # =========================================================================
    # HUNTER GEAR - TRANSPORTATION
    # =========================================================================

    # Modified Van
    surveillance_van, created = HunterGear.objects.get_or_create(
        name="Network Mobile Command Vehicle",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A panel van modified to serve as a mobile surveillance and
command platform. The interior contains monitoring equipment, secure
communications gear, and storage for hunter equipment. The exterior appears
entirely mundane.

O'Brien's Garage maintains the vehicle, ensuring it runs reliably and its
equipment stays current. The van can coordinate operations, provide
overwatch, and serve as emergency extraction when needed.

Only certified drivers are authorized to operate the command vehicle,
which represents a significant investment by the network.""",
            "gear_type": "transportation",
            "damage": "",
            "range": "",
            "rate": "",
            "capacity": "",
            "concealability": "",
            "availability": 4,
            "legality": "legal",
            "requires_training": True,
        },
    )
    if created:
        print(f"  Created Hunter Gear: {surveillance_van.name}")

    # =========================================================================
    # HUNTER GEAR - UTILITY
    # =========================================================================

    # Protective Clothing
    armored_clothing, created = HunterGear.objects.get_or_create(
        name="Concealed Body Armor",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Body armor designed to be worn under normal clothing,
providing protection without obviously marking the wearer as expecting
violence. The armor includes ceramic plates and Kevlar weave.

The armor is uncomfortable for extended wear but has saved multiple hunters
from otherwise fatal injuries. The network maintains a supply for loan
during high-risk operations.

Custom fitting ensures mobility isn't significantly impaired. Each set is
assigned to a specific hunter for regular use.""",
            "gear_type": "armor",
            "damage": "",
            "range": "",
            "rate": "",
            "capacity": "",
            "concealability": "Under clothing",
            "availability": 3,
            "legality": "legal",
            "requires_training": False,
        },
    )
    if created:
        print(f"  Created Hunter Gear: {armored_clothing.name}")

    # Portable Workstation
    portable_workstation, created = HunterGear.objects.get_or_create(
        name="Field Analysis Station",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A ruggedized laptop with specialized software for analyzing
supernatural phenomena. The system includes databases of known creatures,
cross-reference tools, and secure communication links to the network.

Alex Chen developed the software over years of cataloging hunter encounters.
The system isn't a substitute for experience, but it helps identify patterns
and provide context for unfamiliar situations.

Each safe house maintains a field station for coordination and research.""",
            "gear_type": "utility",
            "damage": "",
            "range": "",
            "rate": "",
            "capacity": "",
            "concealability": "Bag",
            "availability": 3,
            "legality": "legal",
            "requires_training": True,
        },
    )
    if created:
        print(f"  Created Hunter Gear: {portable_workstation.name}")

    # =========================================================================
    # HUNTER RELICS - BLESSED ITEMS
    # =========================================================================

    # Holy Symbols
    blessed_cross, created = HunterRelic.objects.get_or_create(
        name="Cross of Saint Michael",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A silver cross blessed by Prophet Samuel Washington and
infused with genuine faith. The cross provides protection against supernatural
creatures and can be used to repel vampires and demons who fear holy symbols.

Prophet Washington blessed this cross during a particularly fervent prayer
service following the loss of a fellow hunter. The faith of the entire
congregation flows through the symbol.

The cross responds to the faith of its bearer - skeptics find it merely
jewelry, while true believers can channel its protective power.""",
            "power_level": 3,
            "background_cost": 3,
            "is_blessed": True,
            "is_cursed": False,
            "requires_faith": True,
            "is_unique": True,
            "powers": """Protection against vampires and demons
Can be used to repel supernatural creatures
Provides spiritual comfort to the faithful
Glows faintly in the presence of evil""",
            "activation_cost": "Faith and prayer",
            "origin": "Blessed by Prophet Samuel Washington",
            "limitations": "Requires genuine faith to use effectively",
        },
    )
    if created:
        print(f"  Created Hunter Relic: {blessed_cross.name}")

    # Holy Water Supply
    blessed_water, created = HunterRelic.objects.get_or_create(
        name="Consecrated Water Cache",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A supply of holy water blessed by Prophet Washington and
stored in specially prepared vials. The water burns supernatural creatures
and can cleanse minor taints.

The network maintains a rotating supply, as holy water loses potency over
time if not stored properly. Prophet's Church serves as the primary source,
with hunters regularly collecting new supplies.

The water is most effective when used with faith and prayer, though even
skeptics can weaponize it against vulnerable creatures.""",
            "power_level": 2,
            "background_cost": 1,
            "is_blessed": True,
            "is_cursed": False,
            "requires_faith": False,
            "is_unique": False,
            "powers": """Burns vampires and demons
Cleanses minor supernatural taints
Can bless areas temporarily
Enhanced effect when used with faith""",
            "activation_cost": "None - consumable",
            "origin": "Blessed at Prophet's Church",
            "limitations": "Loses potency after approximately one month",
        },
    )
    if created:
        print(f"  Created Hunter Relic: {blessed_water.name}")

    # =========================================================================
    # HUNTER RELICS - RECOVERED ARTIFACTS
    # =========================================================================

    # Werewolf Fang
    werewolf_fang, created = HunterRelic.objects.get_or_create(
        name="Fang of the First Victory",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A werewolf fang taken from the first confirmed werewolf
kill by Seattle's hunter network back in the 1970s. The fang has been mounted
and treated, retaining some connection to the creature it came from.

The fang resonates in the presence of werewolves, growing warm and vibrating
slightly. This early warning has saved hunters from ambush multiple times.

The relic serves as a reminder of what hunters can accomplish working together,
and new members are shown the fang as part of their induction.""",
            "power_level": 2,
            "background_cost": 2,
            "is_blessed": False,
            "is_cursed": False,
            "requires_faith": False,
            "is_unique": True,
            "powers": """Detects werewolf presence within 50 feet
Resonates more strongly with more powerful werewolves
Provides insight into werewolf behavior patterns""",
            "activation_cost": "None - passive",
            "origin": "Recovered from werewolf kill, Seattle 1972",
            "limitations": "Only detects werewolves, not other shapeshifters",
        },
    )
    if created:
        print(f"  Created Hunter Relic: {werewolf_fang.name}")

    # Vampire Stake
    ancient_stake, created = HunterRelic.objects.get_or_create(
        name="Stake of Final Rest",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """An old wooden stake that has been used to destroy numerous
vampires over decades of hunting. The stake has absorbed something from its
victims, making it more effective against the undead.

The stake was brought to Seattle by a hunter who came from a family with
generations of vampire hunting experience. It has since passed through
multiple hands as its bearers fell in the line of duty.

Vampires staked with this weapon cannot pull it free through supernatural
strength alone - something about the accumulated destruction resists their
efforts.""",
            "power_level": 3,
            "background_cost": 3,
            "is_blessed": False,
            "is_cursed": False,
            "requires_faith": False,
            "is_unique": True,
            "powers": """Enhanced effectiveness against vampires
Resists removal by supernatural strength
Carries weight of past victories against undead""",
            "activation_cost": "None - always active",
            "origin": "Family heirloom, dating back to Eastern European hunting traditions",
            "limitations": "Only effective against vampires",
        },
    )
    if created:
        print(f"  Created Hunter Relic: {ancient_stake.name}")

    # Captured Supernatural Item
    ghost_bell, created = HunterRelic.objects.get_or_create(
        name="Bell of the Summoned",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A small brass bell recovered from a spiritualist who was
using it to summon and bind ghosts. The bell retains its power, allowing
hunters to call nearby spirits into visibility or drive them away.

The bell's sound carries strangely - normal people hear only a faint chime,
but ghosts experience it as an overwhelming summons. Spirits within earshot
are drawn to the sound and forced to manifest.

Hunters use the bell carefully, as summoning ghosts without preparation can
be dangerous. The bell forces manifestation but does not control what appears.""",
            "power_level": 3,
            "background_cost": 3,
            "is_blessed": False,
            "is_cursed": False,
            "requires_faith": False,
            "is_unique": True,
            "powers": """Force ghosts to manifest
Drive spirits away with sustained ringing
Detect spiritual presence through resonance""",
            "activation_cost": "Ring the bell with intent",
            "origin": "Recovered from spiritualist, Seattle 1998",
            "limitations": "Forces manifestation but not control; may attract unwanted spirits",
        },
    )
    if created:
        print(f"  Created Hunter Relic: {ghost_bell.name}")

    # =========================================================================
    # HUNTER RELICS - CURSED ITEMS
    # =========================================================================

    # Cursed Amulet (Warning Example)
    cursed_amulet, created = HunterRelic.objects.get_or_create(
        name="Amulet of False Safety",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """An amulet recovered from a hunter who died under mysterious
circumstances. The amulet appears to provide protection but actually draws
supernatural attention to its wearer.

The network keeps this item secured as a warning about the dangers of
unfamiliar supernatural items. It's shown to new hunters as an example of
why everything must be thoroughly tested before use.

Several hunters have argued for destroying the amulet, but others believe
it may have research value. For now, it remains locked away.""",
            "power_level": 2,
            "background_cost": 0,
            "is_blessed": False,
            "is_cursed": True,
            "requires_faith": False,
            "is_unique": True,
            "powers": """Appears to ward against detection
Actually attracts supernatural attention
Creates false sense of security""",
            "activation_cost": "Wearing the amulet",
            "origin": "Recovered from deceased hunter, origin unknown",
            "limitations": "CURSED - Do not use. Kept for research and warning purposes only.",
        },
    )
    if created:
        print(f"  Created Hunter Relic: {cursed_amulet.name}")

    print("Hunter items populated successfully.")

    return {
        "weapons": [combat_shotgun, silver_machete, special_ammo],
        "surveillance": [night_vision, surveillance_kit, emf_detector],
        "medical": [medical_kit],
        "transport": [surveillance_van],
        "utility": [armored_clothing, portable_workstation],
        "blessed_relics": [blessed_cross, blessed_water],
        "recovered_relics": [werewolf_fang, ancient_stake, ghost_bell],
        "cursed_relics": [cursed_amulet],
    }


if __name__ == "__main__":
    populate_hunter_items()

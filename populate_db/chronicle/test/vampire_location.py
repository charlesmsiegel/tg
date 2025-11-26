"""
Vampire location population script for Seattle Test Chronicle.

Creates Elysiums, Domains, Racks, and significant Kindred locations.
"""

from accounts.models import Profile
from game.models import Chronicle
from locations.models.vampire import Domain, Elysium, Rack


def populate_vampire_locations():
    """Create all Vampire locations for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # ELYSIUMS
    # =========================================================================

    # Seattle Art Museum - Primary Elysium
    sam_elysium, created = Elysium.objects.get_or_create(
        name="Seattle Art Museum",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Seattle's primary Elysium, the Art Museum serves as neutral
ground for Kindred politics. Seneschal Victoria Ashworth maintains the location,
ensuring both physical security and social propriety.

The Prince holds formal court here on the first Friday of each month, when the
museum hosts "exclusive patron events" that conveniently empty the building of
mortal visitors. The Olympic Sculpture Park extension provides outdoor gathering
space during clement weather.

The museum's renowned collections serve as backdrop for intricate political
maneuvering, with Toreador patrons ensuring the institution remains well-funded
and prestigious.""",
            "prestige": 5,
            "keeper_name": "Victoria Ashworth",
            "elysium_type": "Museum",
            "is_protected": True,
            "allows_weapons": False,
            "has_blood_dolls": False,
            "has_art_collection": True,
            "has_library": True,
            "is_court": True,
            "shroud": 7,
        },
    )
    if created:
        print(f"  Created Elysium: {sam_elysium.name}")

    # Pioneer Square Underground - Secondary Elysium
    underground_elysium, created = Elysium.objects.get_or_create(
        name="Pioneer Square Underground Elysium",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The original streets of Seattle, buried after the Great
Fire of 1889, serve as secondary Elysium and neutral ground between Camarilla
and Anarchs. The Nosferatu claim historical stewardship, having inhabited these
tunnels for over a century.

The Underground provides discrete meeting space for negotiations that would be
inappropriate at the more prestigious Art Museum. Politics here tend toward the
practical rather than the ceremonial.

Tours operate during daytime, but certain sections remain permanently "closed
for renovation" - accessible only to those who know the proper entrances.""",
            "prestige": 3,
            "keeper_name": "The Keeper (Nosferatu Elder)",
            "elysium_type": "Underground Tunnels",
            "is_protected": True,
            "allows_weapons": False,
            "has_blood_dolls": False,
            "has_art_collection": False,
            "has_library": False,
            "is_court": False,
            "shroud": 5,
        },
    )
    if created:
        print(f"  Created Elysium: {underground_elysium.name}")

    # Father Matthias's Church
    church_elysium, created = Elysium.objects.get_or_create(
        name="St. Augustine's Chapel",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A small Catholic chapel on Capitol Hill that serves as
informal Elysium through the influence of Father Matthias, a Sanctified Lasombra.
The church provides neutral ground for Kindred seeking counsel or confession
away from political pressures.

The chapel's role as Elysium is unofficial but widely respected. Father Matthias
offers spiritual guidance to any Kindred who seeks it, regardless of sect
affiliation, and has been known to mediate disputes that other forums cannot
resolve.

The chapel maintains traditional consecration, making it genuinely uncomfortable
for some Kindred but offering unique protections against certain threats.""",
            "prestige": 2,
            "keeper_name": "Father Matthias",
            "elysium_type": "Church",
            "is_protected": True,
            "allows_weapons": False,
            "has_blood_dolls": False,
            "has_art_collection": False,
            "has_library": True,
            "is_court": False,
            "shroud": 6,
        },
    )
    if created:
        print(f"  Created Elysium: {church_elysium.name}")

    # =========================================================================
    # DOMAINS
    # =========================================================================

    # Downtown Financial District - Prince's Domain
    downtown_domain, created = Domain.objects.get_or_create(
        name="Downtown Financial District",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Prince Alexander Mercer's personal domain encompasses
Seattle's financial heart. The high-rises, banks, and corporate headquarters
serve both as hunting ground and seat of power.

The domain is well-controlled through a network of ghouls in security, building
management, and city government. Unauthorized hunting here is a serious breach
of protocol that the Sheriff addresses personally.

The Prince maintains a penthouse haven in Mercer Tower, from which he oversees
both mortal and Kindred affairs.""",
            "size": 4,
            "population": 4,
            "control": 5,
            "is_elysium": False,
            "has_rack": True,
            "is_disputed": False,
            "domain_type": "Corporate/Financial",
            "shroud": 8,
        },
    )
    if created:
        print(f"  Created Domain: {downtown_domain.name}")

    # Capitol Hill - Contested Domain
    capitol_hill_domain, created = Domain.objects.get_or_create(
        name="Capitol Hill",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Seattle's cultural heart hosts multiple Kindred claims.
The nightlife, arts scene, and diverse population make it prime hunting territory,
but no single vampire has established dominance.

The Toreador maintain strong influence through the arts community, while Brujah
hold sway in the activist circles. The Tremere Chantry occupies a converted
mansion, claiming the immediate surroundings. Younger Kindred find opportunities
in the margins.

Father Matthias's church provides neutral ground, but territorial disputes
are common and sometimes violent.""",
            "size": 4,
            "population": 5,
            "control": 2,
            "is_elysium": False,
            "has_rack": True,
            "is_disputed": True,
            "domain_type": "Cultural/Nightlife",
            "shroud": 6,
        },
    )
    if created:
        print(f"  Created Domain: {capitol_hill_domain.name}")

    # University District - Anarch Domain
    u_district_domain, created = Domain.objects.get_or_create(
        name="University District",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Baroness claims the University District as Anarch
territory, her influence extending through every club, coffee shop, and late-night
study session near the UW campus.

The student population provides excellent hunting - transient, often intoxicated,
and unlikely to be missed immediately. The Baroness maintains this domain through
a network of mortal contacts and the loyalty of younger Anarchs who appreciate
her leadership style.

Camarilla Kindred hunt here at their own risk, though the Baroness has been
known to grant temporary permission to those who ask respectfully.""",
            "size": 3,
            "population": 5,
            "control": 4,
            "is_elysium": False,
            "has_rack": True,
            "is_disputed": False,
            "domain_type": "University/Student Area",
            "shroud": 7,
        },
    )
    if created:
        print(f"  Created Domain: {u_district_domain.name}")

    # Industrial Waterfront - Anarch Domain
    waterfront_domain, created = Domain.objects.get_or_create(
        name="Industrial Waterfront",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Red Jack's territory encompasses the docks, warehouses,
and industrial facilities along Elliott Bay. The working-class population suits
his tastes, and the irregular hours of dock workers provide feeding opportunities
at all hours.

The domain is rough but functional. Red Jack doesn't care much for politics
but defends his territory fiercely against incursion. His Brujah followers
maintain order through strength rather than subtlety.

Shipping containers occasionally carry interesting cargo, and the waterfront
sees traffic from ports up and down the coast - including Kindred travelers.""",
            "size": 4,
            "population": 3,
            "control": 4,
            "is_elysium": False,
            "has_rack": True,
            "is_disputed": False,
            "domain_type": "Industrial/Docks",
            "shroud": 7,
        },
    )
    if created:
        print(f"  Created Domain: {waterfront_domain.name}")

    # Nosferatu Warren - Underground Domain
    warren_domain, created = Domain.objects.get_or_create(
        name="The Keeper's Warren",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Beneath Pioneer Square and extending through abandoned
tunnels, utility corridors, and forgotten basements, the Nosferatu maintain
their hidden domain. The Keeper has claimed these passages since the 1890s.

The Warren is less about hunting territory than about security and information
gathering. The Nosferatu trade in secrets, and their domain connects to
observation points throughout the city. Very few know the full extent of
their underground realm.

Entry is by invitation only, and those who enter without permission rarely
leave to tell of it.""",
            "size": 3,
            "population": 1,
            "control": 5,
            "is_elysium": False,
            "has_rack": False,
            "is_disputed": False,
            "domain_type": "Underground Tunnels",
            "shroud": 4,
        },
    )
    if created:
        print(f"  Created Domain: {warren_domain.name}")

    # =========================================================================
    # RACKS
    # =========================================================================

    # Pike Place Market at Night
    pike_place_rack, created = Rack.objects.get_or_create(
        name="Pike Place Market Night Rack",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """After the day crowds disperse, Pike Place Market
becomes prime hunting territory. Tourists lingering too late, restaurant
workers ending their shifts, and the homeless who shelter nearby all provide
feeding opportunities.

The rack is technically open territory, though the Toreador consider it
their informal preserve. Multiple vampires hunt here on any given night,
maintaining an unspoken rotation to avoid depleting the resource.

The market's warren-like structure provides excellent cover for discrete
feeding, and the eclectic population means missing persons rarely draw
attention.""",
            "quality": 4,
            "population_density": 4,
            "risk_level": 2,
            "rack_type": "Tourist/Market District",
            "blood_quality": "Varied - tourists, workers, artists",
            "is_protected": False,
            "is_exclusive": False,
            "is_contested": False,
            "masquerade_risk": 2,
            "shroud": 6,
        },
    )
    if created:
        print(f"  Created Rack: {pike_place_rack.name}")

    # Capitol Hill Club Scene
    club_rack, created = Rack.objects.get_or_create(
        name="Capitol Hill Club Scene",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The clubs and bars of Capitol Hill provide the city's
most reliable feeding for younger Kindred. The intoxicated, the lonely, and
the adventurous all make willing (if unknowing) vessels.

Toreador maintain several establishments where blood dolls - mortals who
enjoy being fed upon - can be found. These managed hunting grounds reduce
Masquerade risk while ensuring quality blood.

Competition for the best clubs is fierce, and territorial disputes sometimes
spill over into violence. The unofficial rule: no killing on the dance floor.""",
            "quality": 5,
            "population_density": 5,
            "risk_level": 3,
            "rack_type": "Nightclub District",
            "blood_quality": "Young, intoxicated, often ecstatic",
            "is_protected": True,
            "is_exclusive": False,
            "is_contested": True,
            "masquerade_risk": 3,
            "shroud": 6,
        },
    )
    if created:
        print(f"  Created Rack: {club_rack.name}")

    # Pioneer Square Shelters
    shelter_rack, created = Rack.objects.get_or_create(
        name="Pioneer Square Shelter District",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The homeless shelters and services around Pioneer Square
provide feeding grounds for Kindred who prefer not to be seen - primarily
Nosferatu, though others hunt here when desperation outweighs dignity.

The population is vulnerable and often overlooked by authorities. Deaths and
disappearances, while tragic, rarely prompt investigation. This makes the
area low-risk but morally questionable even by Kindred standards.

The Nosferatu claim traditional rights here and take poorly to interlopers.
Some maintain that they protect the population from worse predators.""",
            "quality": 2,
            "population_density": 4,
            "risk_level": 1,
            "rack_type": "Homeless Services Area",
            "blood_quality": "Often tainted by substances or illness",
            "is_protected": False,
            "is_exclusive": True,
            "is_contested": False,
            "masquerade_risk": 1,
            "shroud": 5,
        },
    )
    if created:
        print(f"  Created Rack: {shelter_rack.name}")

    # University Ave Bars
    university_rack, created = Rack.objects.get_or_create(
        name="University Avenue Bar District",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The bars along University Avenue, known locally as
"The Ave," cater to students looking to unwind. The young, healthy population
provides excellent feeding, and the transient student body means vessels
rarely recognize repeat predators.

The Baroness permits hunting here but monitors activity closely. Excessive
feeding or Masquerade breaches result in swift and unpleasant consequences.
Young Kindred often start their hunting careers here under Anarch supervision.

Weekend nights see the highest activity, though midweek study breaks also
provide opportunities.""",
            "quality": 4,
            "population_density": 4,
            "risk_level": 2,
            "rack_type": "Student Bar District",
            "blood_quality": "Young, healthy, often intoxicated",
            "is_protected": True,
            "is_exclusive": False,
            "is_contested": False,
            "masquerade_risk": 2,
            "shroud": 7,
        },
    )
    if created:
        print(f"  Created Rack: {university_rack.name}")

    # Waterfront Workers
    dock_rack, created = Rack.objects.get_or_create(
        name="Waterfront Docks",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The docks and surrounding industrial area see round-the-clock
activity from longshoremen, truckers, and warehouse workers. The irregular schedules
and physical labor make these workers ideal vessels - tired people don't question
drowsiness.

Red Jack claims this territory and expects tribute from anyone hunting here. His
Brujah patrol the area, ensuring both territorial integrity and Masquerade security.
The working-class blood suits certain Kindred tastes.

Ships from other ports occasionally bring foreign Kindred, making the docks an
unofficial point of entry for visitors to Seattle.""",
            "quality": 3,
            "population_density": 3,
            "risk_level": 2,
            "rack_type": "Industrial/Docks",
            "blood_quality": "Working-class, often fatigued",
            "is_protected": True,
            "is_exclusive": True,
            "is_contested": False,
            "masquerade_risk": 1,
            "shroud": 7,
        },
    )
    if created:
        print(f"  Created Rack: {dock_rack.name}")

    print("Vampire locations populated successfully.")

    return {
        "elysiums": [sam_elysium, underground_elysium, church_elysium],
        "domains": [
            downtown_domain,
            capitol_hill_domain,
            u_district_domain,
            waterfront_domain,
            warren_domain,
        ],
        "racks": [
            pike_place_rack,
            club_rack,
            shelter_rack,
            university_rack,
            dock_rack,
        ],
    }


if __name__ == "__main__":
    populate_vampire_locations()

"""
Hunter location population script for Seattle Test Chronicle.

Creates Safe Houses, Hunting Grounds, and other hunter-significant locations.
"""

from accounts.models import Profile
from game.models import Chronicle
from locations.models.core import LocationModel


def populate_hunter_locations():
    """Create all Hunter locations for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # SAFE HOUSES
    # =========================================================================

    # Aegis House 1 - Primary Safe House (Ballard)
    aegis_house_1, created = LocationModel.objects.get_or_create(
        name="Aegis House 1 (Ballard)",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Lisa "Aegis" Chen's primary safe house occupies a renovated
warehouse in Ballard's industrial area. The building appears to be a small
manufacturing concern - which it technically is, producing custom metalwork
that pays the bills and provides cover for other activities.

The facility includes medical supplies for treating hunt-related injuries,
a modest armory of conventional weapons, and secure communications equipment.
Sleeping quarters accommodate up to eight hunters for extended stays, and the
workshop can modify equipment for specific hunting needs.

Aegis maintains strict operational security. Access requires either personal
introduction or verification through the hunter network. The warehouse's
industrial neighbors pay little attention to odd hours and unusual visitors.""",
        },
    )
    if created:
        print(f"  Created Safe House: {aegis_house_1.name}")

    # Aegis House 2 - Intelligence Hub (Capitol Hill)
    aegis_house_2, created = LocationModel.objects.get_or_create(
        name="Aegis House 2 (Capitol Hill)",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Capitol Hill safe house operates from the upper floors
of a converted Victorian house. The lower floors function as a legitimate
co-working space, providing cover and income while the upper levels serve
the network's intelligence operations.

This location specializes in information gathering and analysis. The communications
center monitors police scanners, emergency services, and social media for signs of
supernatural activity. Researchers compile dossiers on known threats and track
patterns that might indicate new dangers.

The house's location in a busy neighborhood provides both cover and risk - plenty
of people around means witnesses if something goes wrong, but it also means
hunters blend into the urban environment easily.""",
        },
    )
    if created:
        print(f"  Created Safe House: {aegis_house_2.name}")

    # Aegis House 3 - Emergency Extraction (South Seattle)
    aegis_house_3, created = LocationModel.objects.get_or_create(
        name="Aegis House 3 (South Seattle)",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The South Seattle safe house serves primarily as an emergency
extraction point and last-resort refuge. Located in an industrial park with easy
highway access, the facility is designed for rapid evacuation rather than
extended occupation.

The building contains minimal supplies - emergency medical gear, backup weapons,
cash reserves, and clean vehicles. Hunters know to come here only when their
primary locations are compromised or when they need to disappear quickly.

The facility includes a concealed basement with a reinforced safe room. The
door is steel-core, the walls are concrete, and the supplies inside can sustain
a small group for several days. It's seen use twice; both times, the occupants
survived.""",
        },
    )
    if created:
        print(f"  Created Safe House: {aegis_house_3.name}")

    # =========================================================================
    # HUNTING GROUNDS
    # =========================================================================

    # Pioneer Square - High Activity Zone
    pioneer_square_zone, created = LocationModel.objects.get_or_create(
        name="Pioneer Square Hunting Zone",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Pioneer Square sees more supernatural activity than any
other district in Seattle. Vampires hunt among the nightlife, werewolves sometimes
pass through the underground, and stranger things emerge from the buried city.
Hunters maintain constant watch here, though direct action requires careful
planning.

Multiple hunter patrols rotate through the area, documenting patterns and
identifying targets. The high concentration of supernatural activity makes
Pioneer Square dangerous but also provides the best opportunities for
observation and intelligence gathering.

The tourist underground tours provide cover for daytime reconnaissance. At
night, the bar district offers excuses for extended surveillance. Hunters
learn to read the signs - which establishments cater to inhuman clientele,
which alleys should be avoided, which mortals have been touched by darkness.""",
            "shroud": 5,
        },
    )
    if created:
        print(f"  Created Hunting Ground: {pioneer_square_zone.name}")

    # University District - Monster Activity Zone
    u_district_zone, created = LocationModel.objects.get_or_create(
        name="University District Hunting Zone",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The University District's student population attracts
predators of all kinds. Derek Stone maintains this as his primary territory,
using his position as a high school teacher to identify potential victims and
track suspicious activity.

The area requires careful handling - too many students, too much visibility,
and too many potential witnesses. Hunters here focus on rescue operations and
targeted eliminations rather than the aggressive patrolling used elsewhere.

Stone's "after-school programs" provide cover for training young hunters and
investigating cases that involve students. Several of his recruits first
encountered the supernatural as college students who narrowly survived.""",
            "shroud": 7,
        },
    )
    if created:
        print(f"  Created Hunting Ground: {u_district_zone.name}")

    # Waterfront - Dangerous Zone
    waterfront_zone, created = LocationModel.objects.get_or_create(
        name="Waterfront Hunting Zone",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The waterfront is the most dangerous hunting ground in
Seattle. Something in the water - hunters don't know exactly what - makes the
entire area unpredictable. Operations here require backup, exit strategies,
and the acceptance that things may go wrong.

Despite the danger, the waterfront cannot be ignored. Supernatural cargo moves
through the docks, creatures emerge from the Sound, and the industrial areas
provide too many places for monsters to hide. Hunters patrol in pairs at minimum,
never alone.

The waterfront has claimed several hunters over the years. Their memories are
honored at the annual gathering, and their case files are studied by new
recruits as lessons in what can go wrong.""",
            "shroud": 4,
            "gauntlet": 5,
        },
    )
    if created:
        print(f"  Created Hunting Ground: {waterfront_zone.name}")

    # =========================================================================
    # RESOURCES
    # =========================================================================

    # O'Brien's Garage - Weapons and Vehicles
    obriens_garage, created = LocationModel.objects.get_or_create(
        name="O'Brien's Garage",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Michael O'Brien, the Martyr, runs this auto repair shop as
both legitimate business and hunter resource center. The garage provides vehicle
maintenance for the network, weapon storage in concealed compartments, and
modifications that don't appear on any official paperwork.

O'Brien's mechanical skills translate well to weapon maintenance and modification.
The shop has produced custom ammunition, adapted vehicles for pursuit or escape,
and repaired equipment that civilian shops would refuse to touch.

The garage serves as informal gathering spot for hunters who need a place to
talk shop. O'Brien's coffee is terrible, but the privacy is excellent, and he
never asks questions about the dents, blood stains, or bullet holes that
sometimes accompany the vehicles he services.""",
        },
    )
    if created:
        print(f"  Created Resource: {obriens_garage.name}")

    # Dr. Cole's Office - Psychological Support
    dr_coles_office, created = LocationModel.objects.get_or_create(
        name="Dr. Cole's Office",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Dr. Patricia Cole maintains a private practice specializing
in trauma therapy. Her legitimate patients include first responders, veterans,
and survivors of violent crime. Her unofficial patients are hunters dealing
with the psychological toll of their work.

The Judge understands that hunting breaks minds as readily as bodies. Her
office provides a space where hunters can process what they've seen and done
without fear of disbelief or commitment. She prescribes coping strategies
instead of medication, knowing that drugs dull the edges hunters need.

The office also serves as a screening facility. New hunters are evaluated for
psychological stability before being trusted with sensitive operations. Those
who fail the evaluation are gently redirected; those who pass know they have
someone to talk to when the nightmares get bad.""",
        },
    )
    if created:
        print(f"  Created Resource: {dr_coles_office.name}")

    # Prophet's Church - Coordination Center
    prophets_church, created = LocationModel.objects.get_or_create(
        name="Prophet's Church",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Samuel "Prophet" Washington's small church in South Seattle
serves as the network's primary coordination center. The congregation knows
their pastor has unusual commitments; they attribute his frequent absences to
community outreach, which isn't entirely inaccurate.

Major operations are planned in the church basement, where Prophet's visions
and the network's intelligence are combined into actionable strategies. The
space includes maps of Seattle marked with supernatural hot spots, case files
on active threats, and communication equipment that keeps the cells connected.

Sunday services provide cover for regular network meetings. Hunters attend from
throughout the city, their presence explained as members of the congregation.
The church's status as sacred ground provides additional protection - some
supernatural creatures cannot or will not enter.""",
        },
    )
    if created:
        print(f"  Created Resource: {prophets_church.name}")

    # =========================================================================
    # SURVEILLANCE POINTS
    # =========================================================================

    # KEXP Studios - Monitoring Point
    kexp_monitor, created = LocationModel.objects.get_or_create(
        name="KEXP Monitoring Station",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The hunters maintain a discreet monitoring presence near
KEXP's studios. The radio station's broadcasts sometimes carry anomalous content
that provides clues about supernatural activity. A rotation of observers documents
unusual patterns and reports to the network.

The monitoring equipment includes standard recording devices alongside more
esoteric detection methods developed by hunters with technical skills. Alex Chen,
the content moderator, coordinates this operation as part of their broader
surveillance of digital and broadcast media.

The station's influence on Seattle's cultural scene makes it a valuable observation
point. Music scenes attract certain supernatural elements, and the station's
audience includes both predators and potential prey.""",
        },
    )
    if created:
        print(f"  Created Surveillance Point: {kexp_monitor.name}")

    # Pike Place Overlook - Observation Post
    pike_place_overlook, created = LocationModel.objects.get_or_create(
        name="Pike Place Overlook",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A carefully selected observation post overlooking Pike Place
Market allows hunters to monitor one of Seattle's highest-traffic supernatural
areas. The position provides sight lines into the market and the surrounding
streets while offering multiple exit routes.

The overlook is staffed during peak hours - evenings and weekends when supernatural
activity increases. Observers document unusual individuals, track known threats,
and coordinate with mobile teams when action is required.

The position has proven invaluable for pattern recognition. Months of observation
have revealed feeding schedules, territorial boundaries, and the subtle signs
that distinguish supernatural entities from ordinary humans.""",
        },
    )
    if created:
        print(f"  Created Surveillance Point: {pike_place_overlook.name}")

    print("Hunter locations populated successfully.")

    return {
        "safe_houses": [aegis_house_1, aegis_house_2, aegis_house_3],
        "hunting_grounds": [pioneer_square_zone, u_district_zone, waterfront_zone],
        "resources": [obriens_garage, dr_coles_office, prophets_church],
        "surveillance": [kexp_monitor, pike_place_overlook],
    }


if __name__ == "__main__":
    populate_hunter_locations()

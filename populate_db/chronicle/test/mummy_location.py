"""
Mummy location population script for Seattle Test Chronicle.

Creates Cult Temples, Web of Faith locations, and other mummy-significant sites.
"""

from accounts.models import Profile
from game.models import Chronicle
from locations.models.core import LocationModel


def populate_mummy_locations():
    """Create all Mummy locations for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # CULT TEMPLES
    # =========================================================================

    # House of Scrolls Library
    house_of_scrolls, created = LocationModel.objects.get_or_create(
        name="House of Scrolls Library",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Hidden within the University of Washington's library system,
the House of Scrolls maintains a secret archive dedicated to Thoth's wisdom.
Sethnakht leads this scholarly cult, preserving ancient knowledge and seeking
texts lost to history.

The archive occupies a basement level that doesn't appear on official floor plans.
Access requires knowing the correct call numbers and speaking the appropriate
words. The collection includes translations of hieratic texts, studies of magical
theory, and records of Amenti history that most scholars believe are fiction.

Cult members include graduate students, professors, and research librarians -
mortals drawn to ancient wisdom who have found more than academic interest.
Some become vessels for Amenti resurrection; others serve as eyes and hands
in the mortal world.""",
            "shroud": 6,
        },
    )
    if created:
        print(f"  Created Cult Temple: {house_of_scrolls.name}")

    # Keepers of Ma'at Lodge
    keepers_lodge, created = LocationModel.objects.get_or_create(
        name="Keepers of Ma'at Lodge",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Keepers of Ma'at operate from a private club in downtown
Seattle, its membership roster reading like a who's who of the legal community.
Khonsu-mes leads this cult dedicated to justice, though their methods sometimes
extend beyond conventional law.

The lodge appears to be a typical professional organization - meeting rooms,
a small library, comfortable furniture for networking events. The ritual space
in the basement serves different purposes: ceremonies honoring Ma'at, judgments
against those who have escaped mortal justice, and the rare resurrection rite
when a Keeper vessel dies.

Members include judges, prosecutors, defense attorneys, and law enforcement
officers. Their influence extends throughout the legal system, ensuring that
Ma'at's scales find balance even when courts fail.""",
            "shroud": 6,
        },
    )
    if created:
        print(f"  Created Cult Temple: {keepers_lodge.name}")

    # Lions of Sekhmet Dojo
    lions_dojo, created = LocationModel.objects.get_or_create(
        name="Lions of Sekhmet Dojo",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Sekhmet-Hathor leads the Lions from a martial arts academy
in Rainier Valley. The dojo teaches legitimate self-defense classes while
preparing cult members for their true purpose: serving as the warrior arm
of Seattle's Amenti community.

The facility includes standard training areas, weapons practice rooms, and
a meditation space where the cult honors Sekhmet. Advanced students learn
techniques that blend ancient Egyptian martial traditions with modern combat
arts - training that serves equally well against mortal threats and the
creatures of the supernatural world.

The Lions recruit from military veterans, police officers, and those who have
survived violence and seek to prevent it. Their membership overlaps with
Harborview Medical Center staff, where several Lions work in trauma medicine.""",
            "shroud": 6,
        },
    )
    if created:
        print(f"  Created Cult Temple: {lions_dojo.name}")

    # =========================================================================
    # RESURRECTION SITES
    # =========================================================================

    # Museum Egyptian Wing
    museum_wing, created = LocationModel.objects.get_or_create(
        name="Seattle Art Museum - Egyptian Wing",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Egyptian wing of the Seattle Art Museum serves as the
primary resurrection site for the city's Amenti. Several mummies have awakened
here over the decades, drawn by the artifacts' connection to their past lives.
Meritaten herself first stirred to consciousness in this gallery.

The museum provides excellent cover for Amenti activity. Security positions
allow cult members to monitor the wing, and the artifacts themselves serve as
anchors for resurrection rituals. The temple stones in the collection remember
prayers that mortals believe are mere historical curiosities.

The Amenti maintain careful relations with museum administration, using
influence and resources to ensure the Egyptian collection remains extensive
and accessible. New acquisitions are screened for spiritual significance
before public display.""",
            "shroud": 5,
        },
    )
    if created:
        print(f"  Created Resurrection Site: {museum_wing.name}")

    # Private Collection Vault
    private_vault, created = LocationModel.objects.get_or_create(
        name="Thornwood Private Collection",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A wealthy collector's private vault serves as backup
resurrection site and secure storage for artifacts too dangerous or significant
for public display. The collection's owner, a high-ranking cult member, provides
access to trusted Amenti.

The vault contains genuine Egyptian artifacts alongside excellent forgeries that
deflect attention from the real treasures. Canopic jars, funeral masks, and
inscribed tomb goods provide the spiritual anchors necessary for resurrection
rituals. The facility includes a ritual chamber suitable for the most elaborate
ceremonies.

The collection's existence is known to few outside the cult hierarchy. Its
location and contents are secrets protected by magical and mundane security
alike.""",
            "shroud": 5,
        },
    )
    if created:
        print(f"  Created Resurrection Site: {private_vault.name}")

    # =========================================================================
    # WEB OF FAITH NODES
    # =========================================================================

    # University of Washington
    uw_node, created = LocationModel.objects.get_or_create(
        name="University of Washington - Web of Faith Node",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The University of Washington serves as a major node in
Seattle's Web of Faith, connecting the Amenti to the scholarly traditions
that preserve and transmit ancient knowledge. Academic influence spreads
from here throughout the Pacific Northwest's intellectual community.

House of Scrolls members hold positions throughout the university - faculty,
administration, and support staff. Their influence shapes curriculum, research
priorities, and the preservation of knowledge that serves Ma'at's purposes.
Students who show promise are identified and, sometimes, recruited.

The university's libraries, museums, and research facilities all contribute to
the Web, their accumulated knowledge and scholarly energy flowing into the
great pattern that sustains the Amenti's connection to the living world.""",
            "shroud": 7,
        },
    )
    if created:
        print(f"  Created Web Node: {uw_node.name}")

    # Seattle Justice Center
    justice_center, created = LocationModel.objects.get_or_create(
        name="Seattle Justice Center - Web of Faith Node",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The King County Courthouse and associated justice facilities
form another crucial node in Seattle's Web of Faith. The Keepers of Ma'at
maintain strong presence here, their influence woven through the legal system.

Every judgment rendered in these halls feeds the Web - not through any overt
magical action, but through the accumulated weight of justice sought and, sometimes,
achieved. The scales of Ma'at resonate with mortal efforts to balance wrong
against right, strengthening the connections that sustain Amenti existence.

Cult members in the legal profession serve as both active participants and
monitors, ensuring that the balance tips toward justice more often than not.
When the scales tilt too far toward corruption, they take quieter action.""",
            "shroud": 7,
        },
    )
    if created:
        print(f"  Created Web Node: {justice_center.name}")

    # Harborview Medical Center
    harborview, created = LocationModel.objects.get_or_create(
        name="Harborview Medical Center - Web of Faith Node",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Harborview Medical Center serves as the Lions of Sekhmet's
primary node in Seattle's Web of Faith. The hospital's role in healing the
wounded and protecting life aligns perfectly with Sekhmet's dual nature as
both destroyer and healer.

Lions cult members work throughout the hospital - doctors, nurses, administrators,
and support staff. Their healing work feeds the Web while identifying potential
recruits among those who survive against the odds. Survivors of supernatural
violence sometimes find themselves offered choices they never expected.

The hospital's trauma center has saved more lives than official records suggest.
Some patients arrive with injuries that conventional medicine cannot explain,
and they leave healed by methods that appear miraculous to those who don't
understand the power flowing through Sekhmet's servants.""",
            "shroud": 6,
        },
    )
    if created:
        print(f"  Created Web Node: {harborview.name}")

    # =========================================================================
    # THREATENED SITES
    # =========================================================================

    # Apophis Cult Hidden Temple
    apophis_temple, created = LocationModel.objects.get_or_create(
        name="Apophis Cult Hidden Temple",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Somewhere in Seattle, the servants of Apophis maintain a
hidden temple dedicated to the Serpent of Chaos. Apophis-Ka the Deceiver leads
this cult of fallen Amenti and corrupted mortals, working to unravel everything
the faithful have built.

The temple's location remains unknown despite extensive searching. Cult members
operate through cells, and captured servants rarely know more than their immediate
superiors. The temple moves periodically, possibly through supernatural means.

What is known: the cult performs ceremonies that corrupt the Web of Faith, they
target Amenti for destruction or conversion, and they serve something vast and
terrible that has waited in darkness since before the first dynasties. Finding
and destroying this temple is a priority, but the search has cost lives.""",
            "shroud": 4,
        },
    )
    if created:
        print(f"  Created Threatened Site: {apophis_temple.name}")

    # Corrupted Artifacts
    corrupted_storage, created = LocationModel.objects.get_or_create(
        name="Burke Museum Restricted Storage",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Burke Museum's restricted storage contains several
artifacts that radiate corruption - items touched by Apophis's servants or
carrying curses from their original tombs. The Amenti monitor these items but
have not yet found safe means of purification or destruction.

The artifacts include a set of canopic jars that whisper to those nearby, a
scarab amulet that brings misfortune to its owners, and fragments of a stele
inscribed with texts honoring the Serpent. Mortal researchers who work with
these items too closely develop nightmares, paranoia, and worse.

The corrupted collection grows slowly as items are identified and removed from
circulation. Some Amenti argue for destruction; others insist on study. The
debate continues while the artifacts wait, patient as only cursed things can be.""",
            "shroud": 5,
        },
    )
    if created:
        print(f"  Created Threatened Site: {corrupted_storage.name}")

    print("Mummy locations populated successfully.")

    return {
        "cult_temples": [house_of_scrolls, keepers_lodge, lions_dojo],
        "resurrection_sites": [museum_wing, private_vault],
        "web_nodes": [uw_node, justice_center, harborview],
        "threatened": [apophis_temple, corrupted_storage],
    }


if __name__ == "__main__":
    populate_mummy_locations()

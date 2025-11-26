"""
Werewolf item population script for Seattle Test Chronicle.

Creates Fetishes and Talens for the Sept of the Emerald Veil.
"""

from accounts.models import Profile
from game.models import Chronicle
from items.models.werewolf import Fetish, Talen


def populate_werewolf_items():
    """Create all Werewolf items for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # SEPT FETISHES - LEADERSHIP ITEMS
    # =========================================================================

    # Grand Elder's Fetish
    elders_klaive, created = Fetish.objects.get_or_create(
        name="Thunderstrike",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A grand klaive passed down through the leadership of the
Sept of the Emerald Veil for three generations. The blade is forged from silver
and meteoric iron, its edge eternally sharp and its balance perfect for Crinos
combat.

Thunderstrike contains a powerful Storm Elemental bound during a legendary
moot in 1923. The spirit agreed to serve those who protect the caern, granting
its power against the enemies of Gaia.

Lightning plays along the blade's edge when drawn in anger, and thunder
accompanies each strike. The klaive has slain Wyrm creatures, vampires, and
even a Nexus Crawler that threatened the caern in the 1970s.""",
            "rank": 5,
            "gnosis": 7,
            "spirit": "Storm Elemental (War-aspect)",
        },
    )
    if created:
        print(f"  Created Fetish: {elders_klaive.name}")

    # Warder's Fetish
    warders_shield, created = Fetish.objects.get_or_create(
        name="The Emerald Ward",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A large shield crafted from an ancient cedar that fell during
a great storm at the caern. The wood has been treated with sacred oils and
carved with protective glyphs. A Turtle spirit resides within, granting the
Warder enhanced defensive capabilities.

The shield is traditionally carried by the Warder of the Sept, who uses it
to protect the heart of the caern during moots and rituals. The Emerald Ward
has never been breached in direct combat.

The shield can expand to provide cover for multiple Garou when activated,
and the Turtle spirit can be called upon to anchor the Warder against attempts
to move them from their post.""",
            "rank": 4,
            "gnosis": 6,
            "spirit": "Turtle Spirit",
        },
    )
    if created:
        print(f"  Created Fetish: {warders_shield.name}")

    # Master of the Challenge's Fetish
    challenge_staff, created = Fetish.objects.get_or_create(
        name="Staff of Judgment",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A ironwood staff topped with a carved wolf's head, carried by
the Master of the Challenge during formal disputes and challenges. A Falcon spirit
bound within ensures that challenges are conducted fairly and honorably.

When planted in the ground during a challenge, the staff creates a circle that
neither combatant may leave until the challenge is resolved. Attempts at
treachery or dishonorable conduct within the circle are immediately revealed.

The staff also serves as a potent weapon, though its primary purpose is
maintaining the honor of Garou tradition rather than combat.""",
            "rank": 3,
            "gnosis": 5,
            "spirit": "Falcon Spirit (Honor-aspect)",
        },
    )
    if created:
        print(f"  Created Fetish: {challenge_staff.name}")

    # =========================================================================
    # SEPT FETISHES - PACK TOTEMS
    # =========================================================================

    # Storm Runners Pack Fetish
    storm_howler, created = Fetish.objects.get_or_create(
        name="The Storm Howler",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A war horn carved from the tusk of a great mammoth, recovered
from melting permafrost in Alaska. The Storm Runners pack brought this treasure
to Seattle and bound a Wind spirit within during a harrowing journey.

When blown, the horn summons fierce winds that can knock enemies from their
feet or clear the air of toxins and Wyrm-taint. The sound carries for miles in
the Umbra, allowing the pack to signal allies across great distances.

The horn responds particularly well to Get of Fenris, who honor its connection
to the storms of the far north.""",
            "rank": 3,
            "gnosis": 6,
            "spirit": "Wind Spirit (Storm-aspect)",
        },
    )
    if created:
        print(f"  Created Fetish: {storm_howler.name}")

    # Urban Shadows Pack Fetish
    shadow_cloak, created = Fetish.objects.get_or_create(
        name="Cloak of the City's Shadow",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A dark gray cloak that seems to absorb light, created by the
Bone Gnawers of the Urban Shadows pack. The cloak contains a City Spirit that
has adapted to Seattle's urban environment, allowing the wearer to move unseen
through metropolitan areas.

The cloak grants enhanced stealth in urban environments and allows the wearer
to slip through crowds without notice. It also provides a limited ability to
blend into shadows even in well-lit areas.

The City Spirit within knows the secrets of Seattle's streets and can guide
the wearer through shortcuts and hidden paths throughout the city.""",
            "rank": 3,
            "gnosis": 5,
            "spirit": "City Spirit (Seattle-aspect)",
        },
    )
    if created:
        print(f"  Created Fetish: {shadow_cloak.name}")

    # Emerald Guardians Pack Fetish
    guardian_totem, created = Fetish.objects.get_or_create(
        name="Heart of the Grove",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A fist-sized piece of petrified wood from a tree that once grew
at the center of the Discovery Park caern. When the caern was established, a
portion of this sacred wood was set aside and eventually became a powerful fetish.

The Heart allows its bearer to communicate with plant spirits throughout the caern's
territory, sensing disturbances in the natural world. It also provides enhanced
healing when used within the caern's boundaries.

The Children of Gaia who carry this fetish use it to monitor the health of the
caern and the surrounding environment, serving as an early warning system for
ecological and spiritual threats.""",
            "rank": 4,
            "gnosis": 7,
            "spirit": "Ancient Tree Spirit",
        },
    )
    if created:
        print(f"  Created Fetish: {guardian_totem.name}")

    # =========================================================================
    # PERSONAL FETISHES
    # =========================================================================

    # Sarah Thornwood's Klaive
    thornwood_klaive, created = Fetish.objects.get_or_create(
        name="Moonsilver Fang",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A elegant klaive forged for Sarah Thornwood upon her elevation
to Adren. The blade is slender compared to most klaives, designed for speed rather
than raw power, and contains a Wolf Spirit that enhances its wielder's combat
instincts.

The silver blade has been quenched in moonlight during a lunar eclipse, giving
it an ethereal shimmer and enhanced effectiveness against spirits. The weapon
responds to Sarah's moods, growing warm when she is angry and cold when she
faces danger with calculated calm.

Moonsilver Fang has served Sarah through a decade of battles and has never failed her.""",
            "rank": 3,
            "gnosis": 5,
            "spirit": "Wolf Spirit (Battle-aspect)",
        },
    )
    if created:
        print(f"  Created Fetish: {thornwood_klaive.name}")

    # Jake Redmoon's Fetish
    spirit_drum, created = Fetish.objects.get_or_create(
        name="Voice of the Ancestors",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A hand drum made from elk hide stretched over a cedar frame,
decorated with traditional Salish designs. Jake Redmoon crafted this fetish with
the help of his tribal elders, binding an Ancestor Spirit that connects him to
generations of Wendigo who have walked these lands.

When played during rituals or before battle, the drum calls upon the wisdom and
strength of past Garou. The Ancestor Spirit can provide guidance, share knowledge
of old rites, or lend spiritual support during trying times.

The drum has become central to many Sept rituals, its voice calling the Garou
to remember their duties and their heritage.""",
            "rank": 3,
            "gnosis": 6,
            "spirit": "Ancestor Spirit (Wendigo)",
        },
    )
    if created:
        print(f"  Created Fetish: {spirit_drum.name}")

    # Theurge's Spirit Whistle
    spirit_whistle, created = Fetish.objects.get_or_create(
        name="The Summoner's Call",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A bone whistle carved from the femur of a great wolf who died
defending the caern. The Sept's Theurges use this fetish to call spirits for
negotiation, binding, or assistance. An Owl Spirit dwells within, lending its
power to bridge the gap between worlds.

The whistle produces a sound that resonates strongly in the Umbra, attracting
nearby spirits and making them more amenable to communication. It can also be
used to call back a spirit that has fled an incomplete bargain.

The current keeper of the whistle is the Sept's eldest Theurge, though it may
be loaned to others for specific missions or rituals.""",
            "rank": 4,
            "gnosis": 7,
            "spirit": "Owl Spirit (Wisdom-aspect)",
        },
    )
    if created:
        print(f"  Created Fetish: {spirit_whistle.name}")

    # =========================================================================
    # TALENS - COMBAT
    # =========================================================================

    # Bane Arrows
    bane_arrows, created = Talen.objects.get_or_create(
        name="Arrows of Cleansing Fire",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A quiver of twelve arrows blessed by a Fire Elemental. Each
arrow, when fired, bursts into spiritual flame that burns particularly hot against
Wyrm creatures and Banes.

The Sept keeps a supply of these arrows for defense against spiritual incursions.
Creating them requires a complex ritual and the cooperation of an appropriate
Fire spirit, so they are not used casually.

These arrows are the most recently created batch, prepared after warnings of
increased Bane activity in the area.""",
            "rank": 2,
            "gnosis": 5,
            "spirit": "Fire Elemental",
        },
    )
    if created:
        print(f"  Created Talen: {bane_arrows.name}")

    # Moon Dust
    moon_dust, created = Talen.objects.get_or_create(
        name="Dust of Luna's Blessing",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A small pouch containing silvery powder infused with the
essence of a Lune. When thrown at a target, the dust reveals hidden spirits, breaks
certain Gifts, and can temporarily blind enemies.

The dust is particularly effective against creatures using supernatural concealment,
stripping away their defenses and revealing their true nature. It's often used
by scouts and sentries watching for infiltrators.

This particular batch was created during the last full moon and retains strong
connections to Luna's power.""",
            "rank": 1,
            "gnosis": 4,
            "spirit": "Lune",
        },
    )
    if created:
        print(f"  Created Talen: {moon_dust.name}")

    # Wyrm Scale Poison
    wyrm_poison, created = Talen.objects.get_or_create(
        name="Serpent's Bane",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A vial of viscous green liquid, created by binding a captive
Bane and extracting its essence. The poison is deadly to Wyrm creatures but
relatively harmless to Garou and other servants of Gaia.

Applied to weapons, the poison adds devastating damage against Wyrm-tainted targets.
The substance is difficult to create and morally questionable - some Garou refuse
to use weapons forged from the enemy's own corruption.

The Sept maintains a small supply for emergencies but prefers cleaner methods
of dealing with the Wyrm.""",
            "rank": 2,
            "gnosis": 6,
            "spirit": "Captured/Purified Bane essence",
        },
    )
    if created:
        print(f"  Created Talen: {wyrm_poison.name}")

    # =========================================================================
    # TALENS - UTILITY
    # =========================================================================

    # Pathstone
    pathstones, created = Talen.objects.get_or_create(
        name="Pathstones of the Emerald Veil",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A collection of smooth river stones, each containing a minor
Landscape spirit. When placed on the ground, a pathstone creates a temporary anchor
point that can be sensed by Garou who know the proper Gift.

The Sept uses these stones to mark safe paths through the Umbra and to create
emergency meeting points during battles. The stones can be placed and later
retrieved, though each use weakens the bound spirit slightly.

A set of twelve pathstones is currently in circulation among the Sept's most
active packs.""",
            "rank": 1,
            "gnosis": 4,
            "spirit": "Minor Landscape Spirit",
        },
    )
    if created:
        print(f"  Created Talen: {pathstones.name}")

    # Healing Salve
    healing_salve, created = Talen.objects.get_or_create(
        name="Gaia's Tears",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A jar of green-tinged salve created through a ritual involving
a powerful Plant spirit. When applied to wounds, the salve accelerates natural
healing and can even close aggravated wounds that would otherwise require days
to heal.

The Children of Gaia are primarily responsible for creating and distributing
this salve. Their expertise in healing rites makes them natural keepers of this
tradition.

Each jar contains enough salve for three applications. The Sept maintains a
supply at the caern for emergencies.""",
            "rank": 2,
            "gnosis": 5,
            "spirit": "Plant Spirit (Healing-aspect)",
        },
    )
    if created:
        print(f"  Created Talen: {healing_salve.name}")

    # Spirit Snare
    spirit_snare, created = Talen.objects.get_or_create(
        name="Web of the Spider",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A length of silken cord that seems to shimmer with an inner
light. Created by binding a Spider spirit, the snare can be used to temporarily
trap spirits, preventing them from fleeing or attacking.

The snare is primarily used by Theurges who need to negotiate with reluctant
spirits or by warriors who face enemies that would otherwise escape into the
Umbra. The binding lasts only minutes before the Spider spirit's power fades.

The Sept maintains several of these snares for dealing with hostile spirits.""",
            "rank": 2,
            "gnosis": 5,
            "spirit": "Spider Spirit",
        },
    )
    if created:
        print(f"  Created Talen: {spirit_snare.name}")

    # =========================================================================
    # TALENS - SPECIAL PURPOSE
    # =========================================================================

    # Death Dust
    death_dust, created = Talen.objects.get_or_create(
        name="Dust of the Final Rest",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A pouch of gray powder created through a solemn ritual with
an Ancestor spirit's blessing. When scattered over the body of a fallen Garou,
the dust ensures their spirit finds its way to the appropriate afterlife and
prevents their remains from being corrupted by the Wyrm.

The dust is used in battlefield situations where proper burial rites cannot be
performed immediately. It's considered a sacred duty to carry this dust when
facing situations where Garou might fall.

The Silent Striders traditionally prepare this dust, their understanding of
death and the spirit world making them ideal creators.""",
            "rank": 2,
            "gnosis": 5,
            "spirit": "Ancestor Spirit",
        },
    )
    if created:
        print(f"  Created Talen: {death_dust.name}")

    # Warding Stones
    warding_stones, created = Talen.objects.get_or_create(
        name="Stones of the Threshold",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A set of four carved stones that, when placed at the corners
of an area, create a temporary ward against spiritual intrusion. The ward lasts
until dawn or until one of the stones is disturbed.

The Warder uses these stones to create safe areas during travel or to protect
important locations temporarily. The stones contain minor Threshold spirits that
reinforce the boundary between the physical world and the Umbra.

A complete set of four stones is required for the ward to function. The Sept
maintains several sets for patrol use.""",
            "rank": 2,
            "gnosis": 5,
            "spirit": "Threshold Spirit",
        },
    )
    if created:
        print(f"  Created Talen: {warding_stones.name}")

    print("Werewolf items populated successfully.")

    return {
        "sept_fetishes": [elders_klaive, warders_shield, challenge_staff],
        "pack_fetishes": [storm_howler, shadow_cloak, guardian_totem],
        "personal_fetishes": [thornwood_klaive, spirit_drum, spirit_whistle],
        "combat_talens": [bane_arrows, moon_dust, wyrm_poison],
        "utility_talens": [pathstones, healing_salve, spirit_snare],
        "special_talens": [death_dust, warding_stones],
    }


if __name__ == "__main__":
    populate_werewolf_items()

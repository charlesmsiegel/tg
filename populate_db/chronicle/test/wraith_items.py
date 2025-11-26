"""
Wraith item population script for Seattle Test Chronicle.

Creates WraithArtifacts (soulforged items) and WraithRelics (objects of memory) for
the Emerald Necropolis.
"""

from accounts.models import Profile
from game.models import Chronicle
from items.models.wraith import WraithArtifact, WraithRelic


def populate_wraith_items():
    """Create all Wraith items for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # WRAITH ARTIFACTS - NECROPOLIS TREASURES
    # =========================================================================

    # Anacreon's Scepter
    anacreons_scepter, created = WraithArtifact.objects.get_or_create(
        name="The Scepter of Seattle",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A scepter forged from the corpus of a powerful wraith who
ruled Seattle's Necropolis before Octavian Grave's ascension. The previous
Anacreon was soulforged into this symbol of office after losing a Shadow-duel
to Grave - a fate that now haunts the current ruler.

The scepter grants authority over the Necropolis and its citizens. Its touch
can command obedience from lesser wraiths and provides the Anacreon with
enhanced perception of events within his domain.

The soulforged wraith within occasionally attempts to influence the bearer,
whispers of lost glory and promises of power echoing through the artifact.
Grave has learned to silence these whispers, but they never truly stop.""",
            "level": 5,
            "artifact_type": "soulforged",
            "material": "soulsteel",
            "corpus": 10,
            "pathos_cost": 3,
        },
    )
    if created:
        print(f"  Created Wraith Artifact: {anacreons_scepter.name}")

    # Legion Commander's Blade
    legion_blade, created = WraithArtifact.objects.get_or_create(
        name="Vexmark, the Legion's Edge",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A cruel blade wielded by the commander of the Emerald
Legion, Seattle's primary military force. The weapon was forged in the Great
Forges of Stygia from the corpus of a dozen war-traitors, their anger and
desperation infusing the steel with terrible power.

The blade inflicts wounds that are slow to heal, the hatred of its component
souls poisoning victims with despair. In battle, it glows with a sickly green
light that marks its wielder as a champion of the Necropolis.

Commander Marcus Stone carries Vexmark only during times of conflict, knowing
that the blade's influence can corrupt even the most disciplined soldier.""",
            "level": 4,
            "artifact_type": "soulforged",
            "material": "soulsteel",
            "corpus": 8,
            "pathos_cost": 2,
        },
    )
    if created:
        print(f"  Created Wraith Artifact: {legion_blade.name}")

    # Pardoner's Chains
    pardoner_chains, created = WraithArtifact.objects.get_or_create(
        name="Chains of Absolution",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A set of chains forged specifically for binding Shadows
during Pardoning ceremonies. The chains were created by a master Artificer
using techniques learned in the forges beneath Stygia.

When wrapped around a willing wraith, the chains allow a Pardoner to more
safely engage with the subject's Shadow, providing protection from possession
and reducing the risk of the Shadow's escape during the ritual.

Father Malcolm Grey uses these chains in his most difficult cases, where the
Shadow's strength threatens to overwhelm even experienced Pardoners.""",
            "level": 3,
            "artifact_type": "soulforged",
            "material": "stygian_steel",
            "corpus": 6,
            "pathos_cost": 1,
        },
    )
    if created:
        print(f"  Created Wraith Artifact: {pardoner_chains.name}")

    # Masquer's Mirror
    masquers_mirror, created = WraithArtifact.objects.get_or_create(
        name="The Face Stealer",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A hand mirror forged from the corpus of a vain wraith
who spent her existence perfecting the art of disguise. The mirror enhances
Moliate arts, allowing its user to copy appearances with greater precision.

By gazing into the mirror while concentrating on a target, the user can
perfectly replicate their appearance. The effect lasts until the next sunset
or until the user releases the form.

The mirror is said to contain echoes of every face it has stolen, and
prolonged use can cause the user to lose track of their own original
appearance.""",
            "level": 3,
            "artifact_type": "soulforged",
            "material": "stygian_steel",
            "corpus": 4,
            "pathos_cost": 2,
        },
    )
    if created:
        print(f"  Created Wraith Artifact: {masquers_mirror.name}")

    # =========================================================================
    # WRAITH ARTIFACTS - GUILD TOOLS
    # =========================================================================

    # Artificer's Hammer
    artificers_hammer, created = WraithArtifact.objects.get_or_create(
        name="The Soulforge Hammer",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A heavy hammer used in the creation of soulforged items.
The hammer itself is soulforged from a master Artificer who chose to become
a tool of his craft rather than face Oblivion.

The hammer reduces the difficulty of soulforging operations and allows the
user to sense the quality and nature of corpus and other materials. It
practically guides the hand of even inexperienced smiths.

Seattle's Artificers Guild maintains the hammer as a communal resource, with
strict protocols governing its use and storage.""",
            "level": 4,
            "artifact_type": "soulforged",
            "material": "soulsteel",
            "corpus": 7,
            "pathos_cost": 1,
        },
    )
    if created:
        print(f"  Created Wraith Artifact: {artificers_hammer.name}")

    # Harbinger's Lantern
    harbinger_lantern, created = WraithArtifact.objects.get_or_create(
        name="Lantern of the Deathwatch",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A ghostly lantern that illuminates the path between worlds.
The lantern helps Harbingers locate wraiths who are near their Caul-birth
or approaching Transcendence, its light visible only to the dead.

The flame within burns with the essence of hope, said to be forged from a
wraith who achieved Transcendence and left a spark of their final joy behind.
The light comforts the confused newly-dead and guides them toward the
Necropolis.

Harbingers in Seattle consider carrying this lantern a sacred duty, passed
between members based on need rather than rank.""",
            "level": 3,
            "artifact_type": "other",
            "material": "stygian_steel",
            "corpus": 5,
            "pathos_cost": 1,
        },
    )
    if created:
        print(f"  Created Wraith Artifact: {harbinger_lantern.name}")

    # Monitor's Eye
    monitors_eye, created = WraithArtifact.objects.get_or_create(
        name="The All-Seeing Orb",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A crystalline sphere that enhances Fatalism and reveals
hidden truths. The orb was created by a Monitor who wished to continue
serving even after her destruction, her essence preserved in this eternal
vigil.

Gazing into the orb allows the user to perceive the strands of fate connecting
wraiths to their fetters, their Shadows, and each other. The visions can be
cryptic but are always true.

The Monitors maintain the orb in the Hall of Records, using it to verify
testimony and uncover deception during Hierarchical proceedings.""",
            "level": 4,
            "artifact_type": "soulforged",
            "material": "stygian_steel",
            "corpus": 6,
            "pathos_cost": 3,
        },
    )
    if created:
        print(f"  Created Wraith Artifact: {monitors_eye.name}")

    # =========================================================================
    # WRAITH RELICS - OBJECTS OF MEMORY
    # =========================================================================

    # Pioneer Era Relic
    pioneer_rifle, created = WraithRelic.objects.get_or_create(
        name="The Settler's Rifle",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A Winchester rifle carried by a pioneer who died defending
his homestead from what he believed were bandits. The truth - that supernatural
creatures killed his family - bound him to this world, and his rifle followed
him into death.

The rifle functions as a potent weapon against Spectres and other creatures
of Oblivion. The pioneer's determination to protect the innocent lives on
in the weapon, responding particularly well to wraiths who share his protective
instincts.

The rifle's wielder has changed over the decades, but its purpose remains
constant: defense of the living and the dead against those who would harm
them.""",
            "level": 4,
            "rarity": "rare",
            "pathos_cost": 1,
        },
    )
    if created:
        print(f"  Created Wraith Relic: {pioneer_rifle.name}")

    # Native American Relic
    spirit_drum, created = WraithRelic.objects.get_or_create(
        name="Drum of Returning Voices",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A ceremonial drum that belonged to a Salish medicine woman
who died during the smallpox epidemics of the 1800s. The drum retains powerful
connections to the spirit world and the ancestors.

When played with proper respect, the drum can call forth echoes of those who
have passed beyond, briefly allowing communication with wraiths who have
achieved Transcendence or been destroyed. The connection is fleeting but
profound.

The drum is maintained by wraiths of indigenous descent, who ensure that it
is used only for sacred purposes and never exploited.""",
            "level": 5,
            "rarity": "legendary",
            "pathos_cost": 4,
        },
    )
    if created:
        print(f"  Created Wraith Relic: {spirit_drum.name}")

    # Great Fire Relic
    fire_badge, created = WraithRelic.objects.get_or_create(
        name="Badge of the Fallen Firefighter",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A fire captain's badge from the early 1900s, carried by
a firefighter who died saving children from a tenement blaze. His sacrifice
left such an impression that the badge became a powerful relic.

The badge provides protection against fire and heat, both physical and
supernatural. It also grants its bearer enhanced courage, suppressing fear
and bolstering resolve in the face of danger.

The badge has passed through several worthy hands, always finding its way
to wraiths who embody the heroic sacrifice that created it.""",
            "level": 3,
            "rarity": "uncommon",
            "pathos_cost": 1,
        },
    )
    if created:
        print(f"  Created Wraith Relic: {fire_badge.name}")

    # World War II Relic
    soldiers_letters, created = WraithRelic.objects.get_or_create(
        name="Letters Never Sent",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A bundle of letters written by a soldier who died in the
Pacific Theater before he could mail them home. The letters contain his hopes,
fears, and profound love for his family back in Seattle.

The relic enhances Keening, allowing its bearer to communicate emotions with
devastating clarity. The soldier's longing to reach his loved ones lives on
in the letters, amplifying any message sent through the Shroud.

The letters are heartbreaking to read, and many wraiths find themselves moved
to tears by the simple humanity preserved within.""",
            "level": 3,
            "rarity": "uncommon",
            "pathos_cost": 2,
        },
    )
    if created:
        print(f"  Created Wraith Relic: {soldiers_letters.name}")

    # Modern Tragedy Relic
    crash_photograph, created = WraithRelic.objects.get_or_create(
        name="The Last Family Photo",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A photograph recovered from the wreckage of a car accident
that claimed an entire family in the 1990s. The photo shows the family at
their happiest - a birthday party, everyone smiling, unaware of the tragedy
to come.

The relic provides powerful anchoring, making it harder for wraiths in its
presence to be affected by Nihils or Spectral attacks. The family's love for
each other persists as a bulwark against Oblivion.

The photograph is kept in the Necropolis archives, available to any wraith
who needs its protective influence during dangerous missions.""",
            "level": 3,
            "rarity": "uncommon",
            "pathos_cost": 1,
        },
    )
    if created:
        print(f"  Created Wraith Relic: {crash_photograph.name}")

    # =========================================================================
    # WRAITH RELICS - GUILD RESOURCES
    # =========================================================================

    # Usurer's Ledger
    usurers_ledger, created = WraithRelic.objects.get_or_create(
        name="The Book of Debts",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """An accounting ledger from a Victorian-era moneylender who
died clutching his records. The ledger tracks debts and obligations with
supernatural precision, allowing its keeper to sense when oaths are broken.

The Usurers Guild maintains this relic as their primary record-keeping tool.
Agreements recorded in its pages carry extra weight, and those who break
contracts find themselves marked by its power.

The original owner's ghost was destroyed long ago, but his obsessive nature
lives on in the artifact's unforgiving memory.""",
            "level": 3,
            "rarity": "rare",
            "pathos_cost": 1,
        },
    )
    if created:
        print(f"  Created Wraith Relic: {usurers_ledger.name}")

    # Spook's Camera
    ghost_camera, created = WraithRelic.objects.get_or_create(
        name="The Spirit Camera",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A vintage camera that belonged to a photographer who spent
his life trying to capture proof of the supernatural. Ironically, he succeeded
only after his death, when his camera followed him into the Shadowlands.

Photographs taken with this camera can capture images visible only to wraiths,
documenting events in the Shadowlands for posterity. The images can also be
made visible to the living with sufficient effort.

Spooks use the camera to document crimes, gather intelligence, and preserve
memories that might otherwise be lost to Oblivion.""",
            "level": 3,
            "rarity": "uncommon",
            "pathos_cost": 2,
        },
    )
    if created:
        print(f"  Created Wraith Relic: {ghost_camera.name}")

    # Sandman's Music Box
    sleep_music_box, created = WraithRelic.objects.get_or_create(
        name="Lullaby Box",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A delicate music box that plays a haunting lullaby when
opened. The box belonged to a mother who died before she could see her
children grow up, and her love for them infuses every note.

The music can induce sleep in the living, making it valuable for Sandmen who
need to manipulate dreamers. More importantly, the box can also calm wraiths
caught in Shadow-storms, its gentle melody pushing back the darkness.

The Sandmen consider the box a sacred trust, using it only when gentler
methods of influence have failed.""",
            "level": 3,
            "rarity": "uncommon",
            "pathos_cost": 2,
        },
    )
    if created:
        print(f"  Created Wraith Relic: {sleep_music_box.name}")

    # =========================================================================
    # WRAITH ARTIFACTS - SPECTRE-TOUCHED
    # =========================================================================

    # Captured Spectre Essence
    spectre_bone, created = WraithArtifact.objects.get_or_create(
        name="Bone of the Fallen",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A bone shard taken from a destroyed Spectre, still radiating
the cold of Oblivion. The artifact is dangerous to handle and can corrupt
unwary wraiths who expose themselves to its influence too long.

Despite the danger, the bone provides valuable intelligence. By communing with
the echoes of destruction within, a skilled wraith can learn about Spectral
movements and intentions - at the cost of their own stability.

The Necropolis keeps this artifact heavily warded, allowing access only to
those with legitimate research needs and strong enough wills to resist its
corruption.""",
            "level": 3,
            "artifact_type": "spectre",
            "material": "labyrinthine_adamas",
            "corpus": 4,
            "pathos_cost": 3,
        },
    )
    if created:
        print(f"  Created Wraith Artifact: {spectre_bone.name}")

    print("Wraith items populated successfully.")

    return {
        "necropolis_artifacts": [
            anacreons_scepter,
            legion_blade,
            pardoner_chains,
            masquers_mirror,
        ],
        "guild_artifacts": [artificers_hammer, harbinger_lantern, monitors_eye],
        "relics": [
            pioneer_rifle,
            spirit_drum,
            fire_badge,
            soldiers_letters,
            crash_photograph,
        ],
        "guild_relics": [usurers_ledger, ghost_camera, sleep_music_box],
        "spectre_touched": [spectre_bone],
    }


if __name__ == "__main__":
    populate_wraith_items()

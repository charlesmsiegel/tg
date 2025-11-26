"""
Vampire item population script for Seattle Test Chronicle.

Creates VampireArtifacts and Bloodstones for the Camarilla court.
"""

from accounts.models import Profile
from game.models import Chronicle
from items.models.vampire import Bloodstone, VampireArtifact


def populate_vampire_items():
    """Create all Vampire items for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # VAMPIRE ARTIFACTS - COURT TREASURES
    # =========================================================================

    # The Prince's Scepter
    princes_scepter, created = VampireArtifact.objects.get_or_create(
        name="The Scepter of Seattle",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A silver and obsidian scepter that has served as the symbol
of Princedom in Seattle since the domain's founding. The artifact was brought west by
Marcus Vane's sire and passed to him upon achieving praxis.

The scepter resonates with the blood of its bearer, amplifying the Prince's ability to
command other Kindred. Those who hold it without rightful claim find their Beast
stirred to uncontrollable frenzy.

The artifact's origins are unclear - some whisper it dates to Rome, others claim it
was crafted in colonial America. What is certain is that it has been contested by
multiple would-be Princes, and each has met Final Death.""",
            "power_level": 4,
            "background_cost": 5,
            "is_cursed": False,
            "is_unique": True,
            "requires_blood": True,
            "powers": """- Enhances Dominate disciplines by 2 dice when used during formal court
- Allows the bearer to sense treasonous intent within Elysium
- Inflicts aggravated damage to any Kindred who touches it without permission
- Bearer may spend 1 blood point to command the attention of all Kindred present""",
            "history": """Created sometime in the 18th century by a Tremere artisan for
a Ventrue Prince of Boston. The scepter passed through several hands before being
claimed by Marcus Vane's sire during the American expansion westward. It has been
the symbol of Seattle's Princedom since 1892.""",
        },
    )
    if created:
        print(f"  Created Vampire Artifact: {princes_scepter.name}")

    # The Keeper's Ledger
    keepers_ledger, created = VampireArtifact.objects.get_or_create(
        name="The Keeper's Ledger",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A leather-bound journal that has served the Keepers of Elysium
for over two centuries. The pages within never seem to run out, and entries made in
the Keeper's own blood become permanent records that cannot be altered or destroyed.

Adelaide Marsh inherited the Ledger from her predecessor and guards it zealously.
Every boon sworn, every debt incurred, every transgression committed in Elysium
is recorded within. The Ledger remembers what Kindred wish to forget.

Several Kindred have attempted to steal or destroy the artifact over the years.
None have succeeded, and the Ledger contains detailed accounts of each attempt.""",
            "power_level": 3,
            "background_cost": 4,
            "is_cursed": False,
            "is_unique": True,
            "requires_blood": True,
            "powers": """- Entries written in the Keeper's blood are mystically binding
- The Ledger can recall any boon or debt recorded within when queried
- Attempting to violate a recorded oath causes the oathbreaker intense pain
- The Keeper can sense when someone speaks falsely about recorded matters""",
            "history": """Created in Paris during the late 1700s by a Toreador occultist
for the Keeper of a prominent Elysium. The Ledger has served Keepers in five
different cities, passing to worthy successors through ritual rather than
simple inheritance.""",
        },
    )
    if created:
        print(f"  Created Vampire Artifact: {keepers_ledger.name}")

    # The Sheriff's Badge
    sheriffs_badge, created = VampireArtifact.objects.get_or_create(
        name="The Sheriff's Star",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A silver star badge, its points sharpened to razor edges,
worn by Seattle's Sheriff as both symbol of office and practical weapon. The
artifact was created during the Wild West era and has served Sheriffs in frontier
domains ever since.

Viktor Kraus wears the star openly, knowing it marks him as both judge and
executioner. The badge responds to the authority of the Prince, amplifying the
Sheriff's hunting abilities and allowing him to track those who have fled justice.

The star has been dipped in the ashes of Final Death enough times that it carries
a palpable aura of destruction.""",
            "power_level": 4,
            "background_cost": 4,
            "is_cursed": False,
            "is_unique": True,
            "requires_blood": True,
            "powers": """- Can be thrown and will return to the Sheriff's hand
- Inflicts aggravated damage to Kindred
- Allows the Sheriff to track any Kindred named by the Prince
- Bearer is immune to Obfuscate when hunting a declared criminal
- Provides 2 extra dice to Intimidation against Kindred""",
            "history": """Forged by a Tremere gunsmith in Tombstone during the 1880s.
The badge has served Sheriffs in lawless Western domains for over a century,
passing to each new Sheriff through a blood ritual that binds it to the Prince's
authority.""",
        },
    )
    if created:
        print(f"  Created Vampire Artifact: {sheriffs_badge.name}")

    # =========================================================================
    # VAMPIRE ARTIFACTS - CLAN RELICS
    # =========================================================================

    # Tremere Ritual Focus
    tremere_focus, created = VampireArtifact.objects.get_or_create(
        name="The Seattle Chantry Seal",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A bronze seal bearing the sigils of House Tremere and the
City of Seattle, used to empower blood magic rituals within the chantry. The seal
was crafted upon the founding of the Seattle chantry and has been charged with
the magical essence of every ritual performed there since.

Stefan Richter maintains the seal as part of his duties as Regent. It serves both
practical and symbolic purposes - rituals performed with the seal are more potent,
and its presence legitimizes the chantry's authority in the eyes of the Pyramid.

The seal is bound to the chantry itself; removing it from the premises causes it
to lose power and sends an alert to Vienna.""",
            "power_level": 3,
            "background_cost": 3,
            "is_cursed": False,
            "is_unique": False,
            "requires_blood": True,
            "powers": """- Reduces difficulty of Thaumaturgy rituals by 1 when used in the chantry
- Required component for certain House-specific rituals
- Can verify the identity and rank of Tremere visitors
- Allows communication with other chantry seals through ritual""",
            "history": """Created in 1910 when the Seattle chantry was officially chartered.
The seal incorporates elements from both the original Tremere founding and local
indigenous artifacts, binding the chantry to the land as well as the Pyramid.""",
        },
    )
    if created:
        print(f"  Created Vampire Artifact: {tremere_focus.name}")

    # Toreador Masterwork
    toreador_painting, created = VampireArtifact.objects.get_or_create(
        name="The Portrait of Endless Night",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A hauntingly beautiful portrait by an unknown Toreador master,
depicting a Kindred woman gazing at a moonlit garden. The painting seems to shift
slightly when viewed from different angles, and viewers often report seeing different
figures in the garden depending on their emotional state.

Victoria Cross acquired the painting through questionable means and displays it
prominently in her gallery. The portrait has a reputation for inspiring both
artistic genius and dangerous obsession in those who study it too closely.

Several mortal artists have produced masterworks after viewing the painting.
Several have also met unfortunate ends.""",
            "power_level": 3,
            "background_cost": 3,
            "is_cursed": True,
            "is_unique": True,
            "requires_blood": False,
            "powers": """- Mortals who view the painting may gain Inspiration (Crafts +2 for one month)
- Extended viewing can induce Obsession (Willpower roll or become fixated)
- Toreador viewing the painting must roll to avoid entering light trance
- The painting whispers secrets of artistic technique to those who sleep near it""",
            "history": """Painted in Venice during the Renaissance by a Toreador who
claimed the work captured the essence of Kindred existence. The artist met Final
Death shortly after completion, and the painting has passed through dozens of
hands since, leaving a trail of inspired madness.""",
        },
    )
    if created:
        print(f"  Created Vampire Artifact: {toreador_painting.name}")

    # Nosferatu Information Cache
    nosferatu_cache, created = VampireArtifact.objects.get_or_create(
        name="The Warren Archive",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Not a single artifact but a collection of encoded records
maintained by Seattle's Nosferatu. The Archive consists of hundreds of encrypted
files, coded documents, and memory devices storing information on every major
player in the city's supernatural politics.

The Archive is distributed across multiple locations in the Warren, with different
Nosferatu holding keys to different sections. Complete access requires cooperation
from multiple clan members - a security measure that has protected its contents
for decades.

Every clan, every sect, and every supernatural faction in Seattle has secrets
stored in the Warren Archive. The Nosferatu trade in this information carefully,
knowing that knowledge is their greatest weapon.""",
            "power_level": 4,
            "background_cost": 5,
            "is_cursed": False,
            "is_unique": True,
            "requires_blood": False,
            "powers": """- Contains detailed dossiers on most major Kindred in Seattle
- Includes maps of supernatural territories and safe routes
- Records of boons, debts, and political arrangements spanning decades
- Blackmail material on numerous influential figures""",
            "history": """The Archive began as a simple record-keeping system in the
1920s and has grown into a comprehensive intelligence database. Each Nosferatu
Primogen has added to and maintained the collection, making it an irreplaceable
resource for the clan.""",
        },
    )
    if created:
        print(f"  Created Vampire Artifact: {nosferatu_cache.name}")

    # =========================================================================
    # BLOODSTONES
    # =========================================================================

    # Prince's Emergency Reserve
    princes_reserve, created = Bloodstone.objects.get_or_create(
        name="The Prince's Reserve",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A set of three ruby-colored stones kept in a velvet-lined
case in the Prince's private chambers. Each stone can hold significant amounts of
vitae, serving as an emergency reserve should the Prince be wounded or need to
exercise his powers extensively.

The stones were created by the Tremere as a gift upon Marcus Vane's recognition
as Prince, and they are recharged regularly from the most potent vitae available.
Their existence is known only to the Prince's closest advisors.

The stones respond only to the Prince's blood - any other Kindred attempting to
use them finds the vitae turns to ash in their veins.""",
            "max_blood": 15,
            "blood_stored": 12,
            "is_active": True,
            "created_by_generation": 8,
            "stone_type": "Ruby",
        },
    )
    if created:
        print(f"  Created Bloodstone: {princes_reserve.name}")

    # Tremere Ritual Components
    tremere_stones, created = Bloodstone.objects.get_or_create(
        name="Chantry Ritual Stones",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A set of obsidian stones used in Tremere blood magic rituals.
The stones serve as both storage vessels and focusing elements, holding vitae until
it is needed for ritual work. Each stone is inscribed with House sigils that
glow faintly when charged.

The chantry maintains several sets of ritual stones, with different stones attuned
to different paths of Thaumaturgy. Apprentices learn to charge and discharge the
stones as part of their basic training.

These particular stones are attuned to general ritual work and are kept in the
main ritual chamber for common use.""",
            "max_blood": 10,
            "blood_stored": 7,
            "is_active": True,
            "created_by_generation": 10,
            "stone_type": "Obsidian",
        },
    )
    if created:
        print(f"  Created Bloodstone: {tremere_stones.name}")

    # Anarchs' Hidden Cache
    anarch_cache, created = Bloodstone.objects.get_or_create(
        name="The Last Resort",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A rough-cut amber stone hidden in a secure location known
only to the Anarch leadership. The stone serves as an emergency reserve for Anarchs
who find themselves wounded and unable to hunt safely.

The stone is charged communally - any Anarch who uses it is expected to contribute
to its replenishment when able. The system operates on trust rather than enforcement,
and violations are dealt with through social pressure rather than formal punishment.

The stone's location changes periodically to prevent discovery by Camarilla agents.
Currently, it rests in a hidden compartment within The Underground.""",
            "max_blood": 8,
            "blood_stored": 5,
            "is_active": True,
            "created_by_generation": 11,
            "stone_type": "Amber",
        },
    )
    if created:
        print(f"  Created Bloodstone: {anarch_cache.name}")

    # =========================================================================
    # VAMPIRE ARTIFACTS - WEAPONS
    # =========================================================================

    # Viktor's Blade
    sheriff_blade, created = VampireArtifact.objects.get_or_create(
        name="Requiem",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A black-bladed machete carried by Sheriff Viktor Kraus. The
weapon has been used in countless executions and has absorbed enough Kindred vitae
to develop a hunger of its own. The blade seems to drink the blood of its victims,
leaving wounds that do not heal normally.

Viktor claims the blade was a gift from his sire, who used it in the trenches of
World War I. The weapon has since become synonymous with the Sheriff's brutal
efficiency - when Requiem is drawn, someone meets Final Death.

The blade whispers to Viktor sometimes, urging him toward violence. He has learned
to channel these urges productively.""",
            "power_level": 4,
            "background_cost": 4,
            "is_cursed": True,
            "is_unique": True,
            "requires_blood": True,
            "powers": """- Inflicts aggravated damage to Kindred and werewolves
- Wounds inflicted heal at half the normal rate
- The blade absorbs 1 blood point from each victim, granting it to the wielder
- Viktor can spend 1 blood point to add +2 damage for one strike
- The blade hungers - Viktor must make a Willpower roll to sheathe it after drawing""",
            "history": """Forged by a German occultist during WWI, the blade was intended
to kill monsters. Its Kindred creator found the irony amusing. The weapon has been
in Viktor's possession since 1985 and has executed over forty Kindred.""",
        },
    )
    if created:
        print(f"  Created Vampire Artifact: {sheriff_blade.name}")

    # Stake Collection
    blessed_stakes, created = VampireArtifact.objects.get_or_create(
        name="The Scourge's Stakes",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A set of six wooden stakes treated with alchemical solutions
and blessed through unknown rites. The Scourge uses these stakes to immobilize
Kindred who have violated the Masquerade or been sentenced to destruction.

Each stake is carved from different sacred woods - oak, ash, rowan, hawthorn,
yew, and elder. The set was created by a hunter organization and captured by
the Camarilla decades ago. Their effectiveness against Kindred is unmatched.

The stakes seem to sense Kindred nearby, growing warm in the presence of vampiric
vitae. This makes them invaluable for detecting hidden Kindred.""",
            "power_level": 3,
            "background_cost": 3,
            "is_cursed": False,
            "is_unique": True,
            "requires_blood": False,
            "powers": """- Staked Kindred cannot spend blood to break free; must be removed manually
- Stakes grow warm within 10 feet of Kindred blood
- Successful staking forces the victim into torpor rather than simple immobilization
- The stakes cannot be destroyed by fire while staking a Kindred""",
            "history": """Created by the Society of Leopold in the early 1900s. The
set was captured when a Camarilla coterie ambushed the hunters who carried them.
They have served the Scourge of Seattle since 1952.""",
        },
    )
    if created:
        print(f"  Created Vampire Artifact: {blessed_stakes.name}")

    # =========================================================================
    # VAMPIRE ARTIFACTS - SABBAT/ENEMY ITEMS
    # =========================================================================

    # Sabbat Ritual Item (captured)
    sabbat_chalice, created = VampireArtifact.objects.get_or_create(
        name="The Vaulderie Chalice",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A silver chalice inscribed with Sabbat symbols, captured during
a raid on a Sabbat pack several years ago. The chalice is used in the Vaulderie
ritual, creating the blood bonds that unite Sabbat packs.

The Tremere keep the chalice secured in the chantry, studying it to understand
Sabbat blood magic. Attempts to destroy the artifact have failed - the chalice
seems to repair itself over time, and those who try to damage it suffer nightmares.

Some Kindred argue the chalice should be destroyed. Others want to use it as
bait for Sabbat incursions. It remains locked away, a reminder of the enemy.""",
            "power_level": 3,
            "background_cost": 3,
            "is_cursed": True,
            "is_unique": False,
            "requires_blood": True,
            "powers": """- Required for proper Vaulderie ritual
- Blood placed in the chalice mixes mystically, ensuring equal distribution
- Creates stronger Vinculum bonds than normal Vaulderie
- Non-Sabbat handling the chalice experience disturbing visions of sect rituals""",
            "history": """Created by a Sabbat Tzimisce priest in Mexico City during the
1970s. The chalice served a pack that operated in the Pacific Northwest until
their destruction in 2015. The surviving artifact was claimed by the Tremere.""",
        },
    )
    if created:
        print(f"  Created Vampire Artifact: {sabbat_chalice.name}")

    print("Vampire items populated successfully.")

    return {
        "court_treasures": [princes_scepter, keepers_ledger, sheriffs_badge],
        "clan_relics": [tremere_focus, toreador_painting, nosferatu_cache],
        "bloodstones": [princes_reserve, tremere_stones, anarch_cache],
        "weapons": [sheriff_blade, blessed_stakes],
        "captured": [sabbat_chalice],
    }


if __name__ == "__main__":
    populate_vampire_items()

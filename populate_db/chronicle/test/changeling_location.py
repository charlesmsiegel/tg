"""
Changeling location population script for Seattle Test Chronicle.

Creates Freeholds, Holdings, Trods, and other Dreaming-touched locations.
"""

from accounts.models import Profile
from game.models import Chronicle
from locations.models.changeling import Freehold, Holding, Trod
from locations.models.core import LocationModel


def populate_changeling_locations():
    """Create all Changeling locations for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # HOLDINGS
    # =========================================================================

    # Seattle Holding - Duke Rowan's Domain
    seattle_holding, created = Holding.objects.get_or_create(
        name="Duchy of the Emerald Crown",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Duke Rowan Thornwood's domain encompasses greater Seattle
and the surrounding counties. The Duchy has weathered the storms of the modern
age better than most, thanks to the vibrant creative community and the region's
natural beauty that feeds the Dreaming.

The Duke maintains careful balance between Seelie and Unseelie interests, though
his own heart belongs to the Seelie Court. Countess Lysandra rules the Unseelie
faction with his grudging acceptance, their cold war occasionally flaring into
open conflict before being suppressed for the greater good.

The Duchy's borders extend from the Canadian border to Portland's sphere of
influence, and from the Cascades to the Pacific. Within this vast territory,
numerous freeholds owe allegiance to the Emerald Crown.""",
            "rank": "duchy",
            "ruler_name": "Duke Rowan Thornwood",
            "ruler_title": "Duke of the Emerald Crown",
            "court": "seelie",
            "territory_description": "Greater Seattle metropolitan area and surrounding counties",
            "mundane_location": "Pacific Northwest, Washington State",
            "vassals": "Baron Ironwright, Countess Lysandra (Unseelie), various knights and squires",
            "liege": "Queen Aeron of the West",
            "freehold_count": 12,
            "major_freeholds": "The Emerald Court (Pike Place), Baron's Junkyard, The Underground Gallery",
            "population": "Several hundred changelings, numerous kinain and enchanted mortals",
            "military_strength": 3,
            "wealth": 4,
            "stability": 3,
            "political_situation": "Tense but stable balance between Seelie and Unseelie factions",
            "notable_laws": "Violence against dreamers is punishable by exile",
            "rival_holdings": "The Kingdom of Apples (to the south), various noble rivals within the West",
            "threats": ["Rising Banality", "Unseelie separatism", "Nunnehi territorial disputes"],
            "history": "Established after the Resurgence, built on foundations laid by indigenous Nunnehi",
        },
    )
    if created:
        print(f"  Created Holding: {seattle_holding.name}")

    # =========================================================================
    # FREEHOLDS
    # =========================================================================

    # The Emerald Court - Duke's Primary Freehold
    emerald_court, created = Freehold.objects.get_or_create(
        name="The Emerald Court",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Duke Rowan's primary freehold centers on Pike Place Market,
where the balefire burns in a hidden chamber beneath the market's oldest stalls.
The freehold draws power from the dreams of tourists, artists, and the creative
energy that has always defined this place.

The court chambers exist in a pocket of the Dreaming that overlaps the market's
physical structure. Mortals pass through unaware, though sensitive souls sometimes
feel a touch of wonder they cannot explain. The Duke holds formal court here,
adjudicating disputes and receiving vassals.

Multiple trods connect the Emerald Court to other freeholds in the Duchy and
beyond, making it a hub of fae travel and commerce.""",
            "archetype": "manor",
            "aspect": "The wonder of discovery and the joy of creation",
            "quirks": "Time flows strangely; visitors sometimes leave younger than they arrived",
            "balefire": 4,
            "size": 4,
            "sanctuary": 3,
            "resources": 4,
            "passages": 5,
            "powers": ["warning_call", "resonant_dreams"],
            "resource_description": "Glamour from tourist wonder, occasional dross from artistic breakthroughs",
            "passage_description": "Trods to Baron's Junkyard, Underground Gallery, Discovery Park Glen, and distant freeholds",
            "balefire_description": "A great hearth that appears as a brass brazier filled with green-gold flame",
            "parent": seattle_holding,
        },
    )
    if created:
        print(f"  Created Freehold: {emerald_court.name}")

    # Widget's Cafe Freehold
    widgets_cafe, created = Freehold.objects.get_or_create(
        name="Widget's Waystation",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Widget's indie game cafe serves excellent coffee and hosts
tabletop gaming nights, but its true purpose is providing safe haven for
changelings in need. The Boggan who runs it has created a place where dreamers
gather naturally, generating steady Glamour through their creative play.

The freehold occupies the cafe and the small apartment above it. The balefire
manifests as the perpetually lit pilot light of an ancient espresso machine that
somehow never breaks down. The cafe's regulars include several kinain and a few
enchanted mortals who don't quite realize why they feel so at home here.

Widget asks no questions and offers no judgment. Her waystation serves Seelie
and Unseelie alike, and she's been known to shelter childlings fleeing abusive
situations until proper arrangements can be made.""",
            "archetype": "hearth",
            "aspect": "The comfort of hospitality and the joy of play",
            "quirks": "Coffee sometimes tastes like childhood memories",
            "balefire": 2,
            "size": 2,
            "sanctuary": 1,
            "resources": 2,
            "passages": 2,
            "powers": ["warning_call"],
            "hearth_ability": "socialize",
            "resource_description": "Glamour from creative play, modest mundane income from cafe",
            "passage_description": "Trods to Emerald Court and Baron's Junkyard",
            "balefire_description": "The pilot light of an antique espresso machine that never goes out",
            "parent": seattle_holding,
        },
    )
    if created:
        print(f"  Created Freehold: {widgets_cafe.name}")

    # Baron Ironwright's Junkyard
    barons_junkyard, created = Freehold.objects.get_or_create(
        name="Baron Ironwright's Workshop",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """What appears to be an ordinary junkyard in South Seattle
conceals one of the region's most remarkable workshops. Baron Ironwright, a
Nocker of considerable skill and insufferable temperament, has transformed
this heap of discarded machinery into a forge of chimerical wonders.

The freehold's balefire burns in a furnace assembled from a hundred different
engines, producing heat that can shape both iron and dreams. Nocker apprentices
from throughout the West come here to study, enduring the Baron's temper for
the opportunity to learn his secrets.

The junkyard's defensive systems are legendary - chimerical guard dogs built
from car parts, automated turrets that fire rivets of cold iron, and traps
that would make any Seelie knight think twice about uninvited entry.""",
            "archetype": "workshop",
            "aspect": "The satisfaction of creation and the beauty of function",
            "quirks": "Machines sometimes animate briefly when no one is watching",
            "balefire": 3,
            "size": 4,
            "sanctuary": 4,
            "resources": 3,
            "passages": 3,
            "powers": ["warning_call", "glamour_to_dross"],
            "resource_description": "Chimerical components, occasional mundane salvage, commissioned work",
            "passage_description": "Trods to Emerald Court, Widget's Waystation, and a secret path to the Deep Dreaming",
            "balefire_description": "A roaring furnace built from a hundred different engines",
            "parent": seattle_holding,
        },
    )
    if created:
        print(f"  Created Freehold: {barons_junkyard.name}")

    # Lord Ashford's Bookshop
    ashfords_books, created = Freehold.objects.get_or_create(
        name="Ashford's Antiquarian Books",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Lord Ashford's antique bookshop in Capitol Hill serves as
both repository of knowledge and center of Sluagh intrigue. The Sidhe grump
who runs it remembers the Shattering, and his collection includes texts from
before the mundane world forgot magic was real.

The freehold occupies the shop and extends into a basement that is considerably
larger than the building above would suggest. The balefire burns in a fireplace
that exists only in the Dreaming, casting flickering light over shelves that
contain secrets worth killing for.

The Sluagh use this place as their informal headquarters, trading whispers
and gathering intelligence. Lord Ashford permits this in exchange for being
kept informed - there is little that happens in the Duchy that he does not
eventually learn.""",
            "archetype": "repository",
            "aspect": "The preservation of knowledge and the weight of secrets",
            "quirks": "Books sometimes rearrange themselves to reveal relevant passages",
            "balefire": 2,
            "size": 2,
            "sanctuary": 2,
            "resources": 3,
            "passages": 2,
            "powers": ["resonant_dreams"],
            "resource_description": "Rare books, forgotten lore, secrets traded for favors",
            "passage_description": "Trods to Emerald Court and the Underground Gallery",
            "balefire_description": "A fireplace that exists only in the Dreaming, burning with silver flame",
            "parent": seattle_holding,
        },
    )
    if created:
        print(f"  Created Freehold: {ashfords_books.name}")

    # The Underground Gallery - Unseelie Territory
    underground_gallery, created = Freehold.objects.get_or_create(
        name="The Underground Gallery",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Countess Lysandra's territory occupies the Dreaming-touched
spaces beneath Seattle - not the tourist underground, but deeper passages that
connect to the city's buried history. The Unseelie court here draws power from
darker dreams and forbidden desires.

The freehold's heart lies in a gallery that exists entirely in the Dreaming,
displaying art that mortal eyes would find disturbing but changelings recognize
as profound. The balefire burns black and silver, casting shadows that move
independently of their sources.

The Countess holds her own court here, a dark mirror of Duke Rowan's gatherings.
The two leaders maintain an uneasy peace, each watching for signs that the other
plans to upset the balance that keeps the Duchy functioning.""",
            "archetype": "stronghold",
            "aspect": "The liberation of shadow and the truth of dark dreams",
            "quirks": "Shadows occasionally whisper secrets to those who listen",
            "balefire": 3,
            "size": 4,
            "sanctuary": 4,
            "resources": 3,
            "passages": 4,
            "powers": ["warning_call", "dual_nature"],
            "dual_nature_archetype": "repository",
            "resource_description": "Glamour from dark creativity, tribute from Unseelie vassals",
            "passage_description": "Trods to the deep tunnels, Emerald Court (by treaty), and hidden paths to Shadow Court domains",
            "balefire_description": "Black and silver flames that cast animate shadows",
            "parent": seattle_holding,
        },
    )
    if created:
        print(f"  Created Freehold: {underground_gallery.name}")

    # =========================================================================
    # TRODS
    # =========================================================================

    # Pike Place Trod
    pike_place_trod, created = Trod.objects.get_or_create(
        name="Pike Place Trod",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The primary trod connecting the Emerald Court to other
market-area holdings. The path winds through the Dreaming-reflection of Pike
Place, where chimerical merchants sell impossible wares and buskers play music
that has never existed in the mortal world.

The trod is Glamour-rich and relatively safe, protected by the Duke's decree
and the general goodwill of market dreamers. Travelers sometimes encounter
strange beings - dreams given form, chimera seeking purpose, or the occasional
lost mortal who wandered too far into wonder.

The trod connects to Widget's Waystation, several smaller holdings, and
eventually to distant freeholds through a series of intermediate paths.""",
        },
    )
    if created:
        print(f"  Created Trod: {pike_place_trod.name}")

    # Underground Seattle Trod
    underground_trod, created = Trod.objects.get_or_create(
        name="Underground Seattle Trod",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A darker path running through the buried streets of old
Seattle, connecting to the Underground Gallery and Unseelie territories. The
trod is technically open to all changelings, but Seelie travelers are advised
to move quickly and not linger.

The Dreaming here remembers the fire, the buried dead, and the secrets that
wealthy pioneers thought they'd hidden forever. Chimerical echoes of the old
city sometimes manifest - ghostly saloons, phantom carriages, and the shadows
of those who died when Seattle burned.

The trod requires navigating complex protocols between Seelie and Unseelie
authority. Neutral travelers carry tokens of passage; those aligned with either
court must follow specific rules or risk diplomatic incidents.""",
        },
    )
    if created:
        print(f"  Created Trod: {underground_trod.name}")

    # Capitol Hill Art Walk Trod
    art_walk_trod, created = Trod.objects.get_or_create(
        name="Capitol Hill Art Walk Trod",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A seasonal trod that fully manifests during Capitol Hill's
monthly gallery openings, when creative energy saturates the neighborhood and
the boundary between art and dream grows thin. At other times, the trod exists
in diminished form, navigable but less stable.

During gallery nights, the trod transforms into a wonder of living art - paintings
that tell stories, sculptures that move, and installations that respond to
changeling presence. Artists sometimes sense the magic, creating works that
bridge both worlds without understanding why.

The trod connects Lord Ashford's bookshop, several artist studios that function
as minor holdings, and eventually the Emerald Court through Pike Place.""",
        },
    )
    if created:
        print(f"  Created Trod: {art_walk_trod.name}")

    # =========================================================================
    # GLENS AND OTHER LOCATIONS
    # =========================================================================

    # Washington Park Arboretum Glen
    arboretum_glen, created = LocationModel.objects.get_or_create(
        name="Arboretum Glen",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Wild Glamour pools in a hidden corner of Washington Park
Arboretum, where ancient trees remember when the land was young. The glen
exists at the boundary between urban and wild, drawing power from both the
careful cultivation of the gardens and the untamed nature struggling to reclaim
its territory.

Nunnehi sometimes visit here, honoring old agreements with the changeling courts.
The indigenous spirits remember treaties made before European contact, and they
expect those agreements to be honored. Wise changelings treat this place with
appropriate respect.

The glen provides natural Glamour for changelings who know how to harvest it,
and serves as neutral ground between the Kithain courts and the native spirits
who have never fully accepted their presence.""",
            "gauntlet": 5,
        },
    )
    if created:
        print(f"  Created Glen: {arboretum_glen.name}")

    # Discovery Park Glen
    discovery_glen, created = LocationModel.objects.get_or_create(
        name="Discovery Park Glen",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Discovery Park's wilderness areas contain another Nunnehi-
touched glen, older and wilder than the Arboretum. The boundary between the
Dreaming and the mortal world grows thin here, and unwary mortals sometimes
wander further than they intended.

The Nunnehi maintain active presence here, and changelings who wish to visit
must first seek permission. Rain Walker and Thunder Bear both use this place
for ceremonies, and their tolerance for Kithain intrusion varies with the
political climate.

The glen connects to deep paths into the Dreaming that most changelings dare
not travel. Those who return from such journeys are forever changed - sometimes
for the better, often not.""",
            "gauntlet": 4,
        },
    )
    if created:
        print(f"  Created Glen: {discovery_glen.name}")

    print("Changeling locations populated successfully.")

    return {
        "holdings": [seattle_holding],
        "freeholds": [
            emerald_court,
            widgets_cafe,
            barons_junkyard,
            ashfords_books,
            underground_gallery,
        ],
        "trods": [pike_place_trod, underground_trod, art_walk_trod],
        "glens": [arboretum_glen, discovery_glen],
    }


if __name__ == "__main__":
    populate_changeling_locations()

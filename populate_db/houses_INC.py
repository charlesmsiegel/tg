from characters.models.changeling.house import House
from characters.models.changeling.house_faction import HouseFaction

h = House.objects.get_or_create(
    name="House Aesin",
    court="unseelie",
    boon="Speak with forest animals",
    flaw="Cannot gain Glamour through Rapture",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 119)

hf = HouseFaction.objects.get_or_create(name="The Virtue Council")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Berserkers")[0]
h.factions.add(hf)

h = House.objects.get_or_create(
    name="House Ailil",
    court="unseelie",
    boon="-1 diff on manipulation",
    flaw="Willpower roll to admit being wrong, and +1 penalty to all Social rolls when they've lost face",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 120)

hf = HouseFaction.objects.get_or_create(name="The Guardians of the Silver Dragon")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="Les Amoureux")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Disinherited")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Lock-Keepers")[0]
h.factions.add(hf)


h = House.objects.get_or_create(
    name="House Balor",
    court="unseelie",
    boon="No Glamour loss from cold iron, can soak cold iron damage at diff 10.",
    flaw="Deformed",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 122)

hf = HouseFaction.objects.get_or_create(name="The Eyes of Balor")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="Masters of the Dance")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Old Firm")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Guardians of the Gates")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Riders of the Fell")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="Scarlet Eye Solutions")[0]
h.factions.add(hf)

# SEELIE HOUSES - COMPLETED

h = House.objects.get_or_create(
    name="House Beaumayn",
    court="seelie",
    boon="Inherent understanding of hauntings and supernatural phenomena; +1 difficulty to detect Beaumayn members through magical scrying",
    flaw="Plagued by guilt and paranoia; -1 to Willpower rolls when making morally questionable decisions",
)[0]
h.add_source("Changeling: the Dreaming 20th Anniversary Edition", 123)

hf = HouseFaction.objects.get_or_create(name="The Ghost Seer Circle")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Redeemers")[0]
h.factions.add(hf)

h = House.objects.get_or_create(
    name="House Dougal",
    court="seelie",
    boon="Physical transformation and crafting affinity; +1 die to any Crafts roll; can enhance tools through dedication and time",
    flaw="Body-focused and insecure; vulnerable to physical transformation-based cantrips; -1 difficulty for attackers to target Dougal specifically",
)[0]
h.add_source("Changeling: the Dreaming 20th Anniversary Edition", 127)

hf = HouseFaction.objects.get_or_create(name="The Smiths Guild")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Weavers")[0]
h.factions.add(hf)

h = House.objects.get_or_create(
    name="House Eiluned",
    court="seelie",
    boon="Magical insight and investigation skill; -1 difficulty on Gremayre and Investigation rolls; can sense lies with successful Perception + Empathy",
    flaw="Tendency toward dark secrets and hidden knowledge; -1 to mundane social rolls when keeping secrets",
)[0]
h.add_source("Changeling: the Dreaming 20th Anniversary Edition", 128)

hf = HouseFaction.objects.get_or_create(name="The Investigators")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Hidden Lore Keepers")[0]
h.factions.add(hf)

h = House.objects.get_or_create(
    name="House Fiona",
    court="seelie",
    boon="Fearless adventurers; +1 die to all rolls involving physical challenges or combat",
    flaw="Tempestuous nature; must succeed at Willpower roll (difficulty 7) to walk away from confrontation",
)[0]
h.add_source("Changeling: the Dreaming 20th Anniversary Edition", 129)

hf = HouseFaction.objects.get_or_create(name="The Storm Riders")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Wandering Warriors")[0]
h.factions.add(hf)

h = House.objects.get_or_create(
    name="House Gwydion",
    court="seelie",
    boon="Born leaders; +2 difficulty to resist Gwydion commands and suggestions; gain automatic success on Leadership rolls",
    flaw="Pride and quick temper; -2 to social rolls when insulted or disrespected; must make Willpower check to avoid confrontation with those of higher status",
)[0]
h.add_source("Changeling: the Dreaming 20th Anniversary Edition", 131)

hf = HouseFaction.objects.get_or_create(name="The Royal Guard")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Council of Wisdom")[0]
h.factions.add(hf)

h = House.objects.get_or_create(
    name="House Liam",
    court="seelie",
    boon="Advocates for the common folk and Kinain; +1 die to social rolls with mortals and non-Sidhe Changelings",
    flaw="Viewed with suspicion by pure-blooded nobility; -1 difficulty for other Sidhe houses to intimidate or manipulate Liam members",
)[0]
h.add_source("Changeling: the Dreaming 20th Anniversary Edition", 133)

hf = HouseFaction.objects.get_or_create(name="The Mortal Advocates")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Common Guard")[0]
h.factions.add(hf)

h = House.objects.get_or_create(
    name="House Scathach",
    court="seelie",
    boon="Mysterious warriors; +1 difficulty to identify or track Scathach members; +1 die to Stealth and Occult rolls",
    flaw="Bound by secretive pacts and oath; must keep at least one major secret; difficulty 8 Willpower to break silence on secrets",
)[0]
h.add_source("Changeling: the Dreaming 20th Anniversary Edition", 135)

hf = HouseFaction.objects.get_or_create(name="The Silent Watchers")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Oath Keepers")[0]
h.factions.add(hf)

# UNSEELIE HOUSES - COMPLETED

h = House.objects.get_or_create(
    name="House Danaan",
    court="unseelie",
    boon="Walkers between worlds; can sense nearby Dreaming thin-points and use Wayfare cantrips at -1 difficulty",
    flaw="Recently returned from Arcadia; difficulty adapting to modern Autumn World; -1 to all mundane technology-related rolls",
)[0]
h.add_source("Changeling: the Dreaming 20th Anniversary Edition", 124)

hf = HouseFaction.objects.get_or_create(name="The Dream Walkers")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Reality Explorers")[0]
h.factions.add(hf)

h = House.objects.get_or_create(
    name="House Daireann",
    court="unseelie",
    boon="Consummate hosts and poisoners; +2 to preparing and using poisons; gain +1 die to all entertainment and hospitality rolls",
    flaw="Addiction to pleasure and sensuality; must succeed at Willpower check (difficulty 7) to refuse indulgence",
)[0]
h.add_source("Changeling: the Dreaming 20th Anniversary Edition", 126)

hf = HouseFaction.objects.get_or_create(name="The Pleasure Keepers")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Poisoner's Cabal")[0]
h.factions.add(hf)

h = House.objects.get_or_create(
    name="House Leanhaun",
    court="unseelie",
    boon="Peerless artists with vampiric hunger for Glamour; +1 die to all Performance and Expression rolls; gain 1 extra Glamour when inspiring others",
    flaw="Must constantly feed on others' Glamour and creativity; if lacking Glamour source for a week, suffer -1 die to all rolls; relationships become toxic",
)[0]
h.add_source("Changeling: the Dreaming 20th Anniversary Edition", 132)

hf = HouseFaction.objects.get_or_create(name="The Artistic Circle")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Muse Hunters")[0]
h.factions.add(hf)

h = House.objects.get_or_create(
    name="House Varich",
    court="unseelie",
    boon="Cold strategists willing to bet everything; +1 die to gambling, negotiation, and tactical rolls; gain +1 to all deception-based cantrips",
    flaw="Gambler's curse; must make Willpower check (difficulty 8) to avoid high-stakes situations; can lose everything in a single roll",
)[0]
h.add_source("Changeling: the Dreaming 20th Anniversary Edition", 136)

hf = HouseFaction.objects.get_or_create(name="The Gambler's Syndicate")[0]
h.factions.add(hf)
hf = HouseFaction.objects.get_or_create(name="The Risk Takers")[0]
h.factions.add(hf)

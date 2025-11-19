from characters.models.vampire.clan import VampireClan
from characters.models.vampire.discipline import Discipline

from populate_db.vampire_disciplines import celerity, fortitude, potence, auspex, dominate, dementation, presence, animalism, protean, obfuscate, chimerstry, necromancy, obtenebration, quietus, serpentis, thaumaturgy, vicissitude

# Create the 13 Main Clans

assamite = VampireClan.objects.get_or_create(
    name="Assamite",
    nickname="Assassins",
    weakness="All non-Assamite vampire blood is poisonous (difficulty 6 to avoid vomiting it back up). "
    "If blood bond attempted with non-Assamite vitae, all 3 drinks required in 10 minutes or bond "
    "fails and blood rejected.",
    description="Guild of assassins bound by ancient Tremere curse (later broken). Middle Eastern, "
    "North African, or Mediterranean features common. Accept blood contracts and follow the Path of Blood. "
    "Also known as Banu Haqim.",
    is_bloodline=False
)[0]
assamite.disciplines.add(celerity, obfuscate, quietus)

brujah = VampireClan.objects.get_or_create(
    name="Brujah",
    nickname="Rebels, Rabble",
    weakness="Difficulty to resist frenzy reduced by 2 (minimum 3). Quick to anger and passionate.",
    description="Once philosopher-kings, now passionate rebels and idealists. Punk, biker, revolutionary "
    "aesthetics common. Quick to anger. Large presence in both Camarilla and Anarch Movement.",
    is_bloodline=False
)[0]
brujah.disciplines.add(celerity, potence, presence)

followers_of_set = VampireClan.objects.get_or_create(
    name="Followers of Set",
    nickname="Serpents, Snakes, Setites",
    weakness="Take double damage from sunlight; +1 difficulty to resist bright lights.",
    description="Worship Set; spread corruption and vice. Deal in forbidden pleasures and knowledge. "
    "Egyptian or Mediterranean features common. Some adopt snake-like modifications. Operate temples, "
    "nightclubs, and drug dens.",
    is_bloodline=False
)[0]
followers_of_set.disciplines.add(obfuscate, presence, serpentis)

gangrel = VampireClan.objects.get_or_create(
    name="Gangrel",
    nickname="Beasts, Animals",
    weakness="Each frenzy permanently adds one animal feature (visible trait: fur, fangs, eyes, "
    "ears, claws, tail, etc.). These features accumulate over time.",
    description="Nomadic loners close to animals and nature. Formerly Camarilla, left in modern nights. "
    "Often rugged and feral in appearance. Sleep in the earth. Distrust cities and politics.",
    is_bloodline=False
)[0]
gangrel.disciplines.add(animalism, fortitude, protean)

giovanni = VampireClan.objects.get_or_create(
    name="Giovanni",
    nickname="Necromancers",
    weakness="The Kiss causes excruciating pain instead of pleasure; causes double damage to mortals. "
    "This makes feeding difficult and dangerous.",
    description="Incestuous Italian merchant family who murdered the Cappadocians to steal Necromancy. "
    "Maintain mortal business empire alongside their dealings with the dead. Italian family resemblance "
    "common; business attire standard.",
    is_bloodline=False
)[0]
giovanni.disciplines.add(dominate, necromancy, potence)

lasombra = VampireClan.objects.get_or_create(
    name="Lasombra",
    nickname="Keepers, Magisters",
    weakness="Cast no reflection in mirrors or on cameras/recordings. May appear as shadow or blur in "
    "reflective surfaces and recordings.",
    description="Social Darwinists who manipulate through shadows and hierarchies. Pillar clan of the Sabbat. "
    "Diableried their own Antediluvian. Spanish and Italian features common; aristocratic bearing. "
    "Often found in churches and positions of authority.",
    is_bloodline=False
)[0]
lasombra.disciplines.add(dominate, obtenebration, potence)

malkavian = VampireClan.objects.get_or_create(
    name="Malkavian",
    nickname="Lunatics, Madmen",
    weakness="All Malkavians suffer from at least one incurable Derangement. This cannot be healed "
    "or removed by any means.",
    description="Gifted with insight and cursed with madness. Connected through the Malkavian Madness "
    "Network. Appearance varies from normal to obviously disturbed. Found in asylums, hospitals, and "
    "urban spaces. Trade in secrets and strange wisdom.",
    is_bloodline=False
)[0]
malkavian.disciplines.add(auspex, dementation, obfuscate)

nosferatu = VampireClan.objects.get_or_create(
    name="Nosferatu",
    nickname="Sewer Rats, Cleopatras",
    weakness="Appearance rating drops to 0; hideous and monstrous. Automatic Masquerade breach if seen "
    "by mortals. Grotesquely deformed with unique mutations.",
    description="Information brokers and master spies. Trade in secrets. Work together out of necessity. "
    "Live in sewers and abandoned tunnels beneath cities. Pale, hairless, corpse-like with unique mutations. "
    "Forced to rely on Obfuscate to move through mortal society.",
    is_bloodline=False
)[0]
nosferatu.disciplines.add(animalism, obfuscate, potence)

ravnos = VampireClan.objects.get_or_create(
    name="Ravnos",
    nickname="Deceivers, Gypsies",
    weakness="Each Ravnos has a specific vice they must indulge (Self-Control/Instinct roll difficulty 6 "
    "to resist). Failure means obsessive pursuit of that vice.",
    description="Wandering tricksters and illusionists. Romani and Indian features common. Each has a "
    "compulsion related to the clan curse. Nearly destroyed during the Week of Nightmares. Travel in "
    "caravans and temporary shelters.",
    is_bloodline=False
)[0]
ravnos.disciplines.add(animalism, chimerstry, fortitude)

toreador = VampireClan.objects.get_or_create(
    name="Toreador",
    nickname="Degenerates, Artistes",
    weakness="When encountering true beauty or creative expression, must roll Self-Control/Instinct "
    "(difficulty 6) or become entranced for the scene, unable to act.",
    description="Artists and aesthetes; patrons of the arts. Seek beauty and perfection. Some are true "
    "artists, others mere poseurs. Beautiful and fashionable. Found in museums, galleries, penthouses, "
    "and theaters. Active in Camarilla high society.",
    is_bloodline=False
)[0]
toreador.disciplines.add(auspex, celerity, presence)

tremere = VampireClan.objects.get_or_create(
    name="Tremere",
    nickname="Warlocks, Usurpers",
    weakness="Blood bond to clan elders forms one step more easily (2 drinks for full bond instead of 3). "
    "This reflects their hierarchical curse.",
    description="Former mortal mages who achieved vampirism through ritual. Destroyed the Salubri and "
    "stole Necromancy from Cappadocians. Hierarchical pyramid structure. Scholarly and formal appearance; "
    "often European features. Live in fortified chantries.",
    is_bloodline=False
)[0]
tremere.disciplines.add(auspex, dominate, thaumaturgy)

tzimisce = VampireClan.objects.get_or_create(
    name="Tzimisce",
    nickname="Fiends, Fleshcrafters",
    weakness="Must rest surrounded by at least 2 handfuls of soil from place of mortal birth or lose "
    "1 blood point per night. Cannot rest peacefully without native earth.",
    description="Transylvanian nobility and masters of fleshcrafting. Pillar clan of the Sabbat. Spiritual "
    "and alien in thinking. Appearance highly variable due to Vicissitude modifications. Old Clan Tzimisce "
    "lack Vicissitude but have Dominate instead. Found in ancestral estates.",
    is_bloodline=False
)[0]
tzimisce.disciplines.add(animalism, auspex, vicissitude)

ventrue = VampireClan.objects.get_or_create(
    name="Ventrue",
    nickname="Blue Bloods, Patricians",
    weakness="Each Ventrue can only feed from specific type of mortal (specific organization, blood type, "
    "demographic, etc.). Cannot gain sustenance from other blood. This restriction is unique to each Ventrue.",
    description="Leaders and nobility who claim rulership as birthright. Natural leaders and maintainers of "
    "the Masquerade. Well-groomed, professional, aristocratic appearance. Found in estates and corporate "
    "penthouses. Pillar of the Camarilla.",
    is_bloodline=False
)[0]
ventrue.disciplines.add(dominate, fortitude, presence)

# Caitiff (Clanless)
caitiff = VampireClan.objects.get_or_create(
    name="Caitiff",
    nickname="Clanless",
    weakness="Cannot take Status at creation; +2 difficulty all Social rolls with non-Caitiff until "
    "established in community. ALL Disciplines cost as out-of-clan (no in-clan discount). Social pariahs.",
    description="Clanless vampires, typically 13th+ Generation or of unknown lineage. Weakening of vampire "
    "blood or mysterious origins. Can learn any Discipline but all cost more. Pariahs of vampire society. "
    "No inherent clan weakness from parent bloodline but suffer severe social stigma.",
    is_bloodline=False
)[0]
# Caitiff have no set clan disciplines - they can learn any

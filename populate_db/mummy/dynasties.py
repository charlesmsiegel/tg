"""Populate Dynasties for Mummy: the Resurrection"""

from characters.models.mummy.dynasty import Dynasty

# Old Kingdom Dynasties
old_kingdom_1 = Dynasty.objects.get_or_create(
    name="First Dynasty",
    era="Old Kingdom",
    description="The earliest unified Egyptian dynasty, beginning with Narmer/Menes. "
    "Amenti from this era remember the first unification of Upper and Lower Egypt.",
    favored_hekau="Nomenclature",
)[0]

old_kingdom_4 = Dynasty.objects.get_or_create(
    name="Fourth Dynasty",
    era="Old Kingdom",
    description="The pyramid builders. Amenti from this golden age remember Khufu, Khafre, "
    "and the construction of the Great Pyramids at Giza.",
    favored_hekau="Effigy",
)[0]

# Middle Kingdom Dynasties
middle_kingdom_11 = Dynasty.objects.get_or_create(
    name="Eleventh Dynasty",
    era="Middle Kingdom",
    description="Reunification of Egypt after the First Intermediate Period. These Amenti "
    "remember bringing order from chaos.",
    favored_hekau="Judge",
)[0]

middle_kingdom_12 = Dynasty.objects.get_or_create(
    name="Twelfth Dynasty",
    era="Middle Kingdom",
    description="The classical age of Egyptian literature and art. Amenti from this peaceful "
    "era are often scholars and diplomats.",
    favored_hekau="Celestial",
)[0]

# New Kingdom Dynasties
new_kingdom_18 = Dynasty.objects.get_or_create(
    name="Eighteenth Dynasty",
    era="New Kingdom",
    description="The dynasty of Hatshepsut, Akhenaten, Tutankhamun, and great imperial expansion. "
    "These Amenti remember Egypt at its zenith.",
    favored_hekau="Ushabti",
)[0]

new_kingdom_19 = Dynasty.objects.get_or_create(
    name="Nineteenth Dynasty",
    era="New Kingdom",
    description="The Ramesside period, including Ramesses II the Great. Warriors and builders "
    "from an age of monumental construction.",
    favored_hekau="Phoenix",
)[0]

# Ptolemaic Dynasty
ptolemaic = Dynasty.objects.get_or_create(
    name="Ptolemaic Dynasty",
    era="Ptolemaic",
    description="Greek rulers of Egypt after Alexander. These Amenti bridge Egyptian and "
    "Hellenistic worlds, often multilingual and cosmopolitan.",
    favored_hekau="Alchemy",
)[0]

# Modern
modern = Dynasty.objects.get_or_create(
    name="Modern Awakened",
    era="Modern",
    description="Amenti who first awakened in the modern era, or who have fully adapted to "
    "contemporary society across many incarnations.",
    favored_hekau="Necromancy",
)[0]

"""Populate Titles for Mummy: the Resurrection"""

from characters.models.mummy.mummy_title import MummyTitle

# Leadership Titles
pharaoh = MummyTitle.objects.get_or_create(
    name="Pharaoh",
    rank_level=10,
    description="Supreme leader of an Amenti community. Rare and powerful.",
)[0]

high_priest = MummyTitle.objects.get_or_create(
    name="High Priest/Priestess",
    rank_level=8,
    description="Religious leader and keeper of ancient rites.",
)[0]

vizier = MummyTitle.objects.get_or_create(
    name="Vizier",
    rank_level=7,
    description="Chief administrator and advisor to higher-ranking Amenti.",
)[0]

# Web-Specific Titles
keeper_of_balance = MummyTitle.objects.get_or_create(
    name="Keeper of Balance",
    rank_level=6,
    description="Guardian of Ma'at and cosmic order. Associated with the Web of Ma'at.",
)[0]

judge_of_souls = MummyTitle.objects.get_or_create(
    name="Judge of Souls",
    rank_level=6,
    description="Weighs hearts and pronounces judgment. Associated with the Web of Osiris.",
)[0]

guardian = MummyTitle.objects.get_or_create(
    name="Guardian",
    rank_level=5,
    description="Protector of sacred places and fellow Amenti. Associated with the Web of Horus.",
)[0]

preserver = MummyTitle.objects.get_or_create(
    name="Preserver",
    rank_level=5,
    description="Keeper of knowledge and sacred objects. Associated with the Web of Isis.",
)[0]

lorekeeper = MummyTitle.objects.get_or_create(
    name="Lorekeeper",
    rank_level=5,
    description="Scholar and keeper of wisdom. Associated with the Web of Thoth.",
)[0]

# General Titles
elder = MummyTitle.objects.get_or_create(
    name="Elder",
    rank_level=4,
    description="Respected Amenti with many incarnations and much experience.",
)[0]

mentor = MummyTitle.objects.get_or_create(
    name="Mentor",
    rank_level=3,
    description="Teacher of newly awakened Amenti.",
)[0]

seeker = MummyTitle.objects.get_or_create(
    name="Seeker",
    rank_level=2,
    description="Amenti on a quest for knowledge or redemption.",
)[0]

neophyte = MummyTitle.objects.get_or_create(
    name="Neophyte",
    rank_level=1,
    description="Newly awakened Amenti, still learning their purpose.",
)[0]

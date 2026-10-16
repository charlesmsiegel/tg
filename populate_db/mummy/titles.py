"""Load Mummy titles while preserving the existing script exports."""

from pathlib import Path

from characters.models.mummy.mummy_title import MummyTitle
from core.seed_data import load_seed_records

_titles = load_seed_records(
    MummyTitle,
    Path(__file__).with_suffix(".json"),
    allowed_fields=frozenset({"name", "rank_level", "description"}),
    legacy_fields=frozenset({"name"}),
)

pharaoh = _titles["pharaoh"]
high_priest = _titles["high_priest"]
vizier = _titles["vizier"]
keeper_of_balance = _titles["keeper_of_balance"]
judge_of_souls = _titles["judge_of_souls"]
guardian = _titles["guardian"]
preserver = _titles["preserver"]
lorekeeper = _titles["lorekeeper"]
elder = _titles["elder"]
mentor = _titles["mentor"]
seeker = _titles["seeker"]
neophyte = _titles["neophyte"]

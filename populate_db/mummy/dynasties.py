"""Load Mummy dynasties while preserving the existing script exports."""

from pathlib import Path

from django.db import transaction

from characters.models.mummy.dynasty import Dynasty
from core.seed_data import load_seed_records

# Include export binding: a malformed catalogue must not commit a failed import.
with transaction.atomic():
    _dynasties = load_seed_records(
        Dynasty,
        Path(__file__).with_suffix(".json"),
        allowed_fields=frozenset({"name", "era", "description", "favored_hekau"}),
        legacy_fields=frozenset({"name"}),
    )

    old_kingdom_1 = _dynasties["old_kingdom_1"]
    old_kingdom_4 = _dynasties["old_kingdom_4"]
    middle_kingdom_11 = _dynasties["middle_kingdom_11"]
    middle_kingdom_12 = _dynasties["middle_kingdom_12"]
    new_kingdom_18 = _dynasties["new_kingdom_18"]
    new_kingdom_19 = _dynasties["new_kingdom_19"]
    ptolemaic = _dynasties["ptolemaic"]
    modern = _dynasties["modern"]

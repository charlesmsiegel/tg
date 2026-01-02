"""Service for organizing chronicle data by gameline."""

import itertools
from collections import OrderedDict
from datetime import datetime


class ChronicleDataService:
    """
    Service class for organizing and grouping chronicle data by gameline.

    Consolidates gameline grouping logic from ChronicleDetailView into
    a reusable, testable service class.
    """

    # Gameline ordering for consistent tab display
    GAMELINE_ORDER = ["wod", "vtm", "wta", "mta", "wto", "ctd", "htr", "mtr", "dtf"]

    # Short display names for gamelines (used in tabs)
    GAMELINE_SHORT_NAMES = {
        "wod": "All",
        "vtm": "Vampire",
        "wta": "Werewolf",
        "mta": "Mage",
        "wto": "Wraith",
        "ctd": "Changeling",
        "htr": "Hunter",
        "mtr": "Mummy",
        "dtf": "Demon",
    }

    # Character model to gameline mapping
    CHAR_GAMELINE_MAP = {
        "vtm": ["vtmhuman", "ghoul", "vampire", "revenant"],
        "wta": [
            "wtahuman",
            "kinfolk",
            "werewolf",
            "spiritcharacter",
            "fera",
            "fomor",
            "drone",
        ],
        "mta": ["mtahuman", "companion", "sorcerer", "mage"],
        "wto": ["wtohuman", "wraith"],
        "ctd": ["ctdhuman", "changeling", "nunnehi", "inanimae", "autumnperson"],
        "htr": ["htrhuman", "hunter"],
        "mtr": ["mtrhuman", "mummy"],
        "dtf": ["dtfhuman", "demon", "thrall", "earthbound"],
    }

    # Location model to gameline mapping (gameline-specific types only)
    LOC_GAMELINE_MAP = {
        "vtm": ["haven", "domain", "elysium", "rack", "tremerechantry", "barrens"],
        "wta": ["caern"],
        "mta": [
            "node",
            "sector",
            "library",
            "horizonrealm",
            "paradoxrealm",
            "chantry",
            "sanctum",
            "realityzone",
            "demesne",
        ],
        "wto": ["haunt", "necropolis", "citadel", "nihil", "byway", "wraithfreehold"],
        "ctd": ["freehold", "dreamrealm", "trod", "holding"],
        "dtf": ["bastion", "reliquary"],
        "htr": ["huntingground", "safehouse"],
        "mtr": ["tomb", "culttemple", "undergroundsanctuary"],
    }

    # Generic location types that appear in ALL gameline tabs
    GENERIC_LOC_TYPES = ["locationmodel", "city"]

    # Item model to gameline mapping
    ITEM_GAMELINE_MAP = {
        "vtm": ["bloodstone", "artifact"],
        "wta": ["fetish", "talen"],
        "mta": ["wonder", "grimoire", "device", "sorcererartifact"],
        "wto": ["relic", "wraithartifact", "memoriam"],
        "ctd": ["treasure", "dross"],
        "dtf": ["demonrelic"],
        "htr": ["hunterrelic", "gear"],
        "mtr": ["ushabti", "mummyrelic", "vessel"],
    }

    @classmethod
    def group_by_gameline(cls, queryset, gameline_attr="gameline"):
        """
        Group items by gameline, only including gamelines that have content.

        Returns an OrderedDict with 'wod' (All) first if there's content,
        followed by specific gamelines in GAMELINE_ORDER.

        Args:
            queryset: Django queryset to group
            gameline_attr: The attribute name to filter by (default: "gameline")

        Returns:
            OrderedDict with gameline codes as keys
        """
        result = OrderedDict()

        # 'wod' (All) shows everything if there's any content
        if queryset.exists():
            result["wod"] = {
                "name": cls.GAMELINE_SHORT_NAMES.get("wod", "All"),
                "items": queryset,
            }

        # Add specific gamelines that have content
        for gl_code in cls.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            filtered = queryset.filter(**{gameline_attr: gl_code})
            if filtered.exists():
                result[gl_code] = {
                    "name": cls.GAMELINE_SHORT_NAMES.get(gl_code, gl_code),
                    "items": filtered,
                }

        return result

    @classmethod
    def group_characters_by_gameline(cls, queryset):
        """
        Group characters by gameline based on polymorphic content type.

        Characters don't have a direct gameline field, so we filter by model type.

        Args:
            queryset: Character queryset to group

        Returns:
            OrderedDict with gameline codes as keys
        """
        result = OrderedDict()

        # All shows everything if there's any content
        if queryset.exists():
            result["wod"] = {
                "name": cls.GAMELINE_SHORT_NAMES.get("wod", "All"),
                "characters": queryset,
            }

        # Add specific gamelines that have content
        for gl_code in cls.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            model_names = cls.CHAR_GAMELINE_MAP.get(gl_code, [])
            if model_names:
                filtered = queryset.filter(polymorphic_ctype__model__in=model_names)
                if filtered.exists():
                    result[gl_code] = {
                        "name": cls.GAMELINE_SHORT_NAMES.get(gl_code, gl_code),
                        "characters": filtered,
                    }

        return result

    @classmethod
    def group_locations_by_gameline(cls, queryset):
        """
        Group locations by gameline based on polymorphic content type.

        Each gameline tab shows generic locations (Location, City) plus
        that gameline's specific locations, excluding other gamelines' locations.

        Args:
            queryset: Location queryset to group

        Returns:
            OrderedDict with gameline codes as keys
        """
        result = OrderedDict()

        # Collect all gameline-specific types for the "All" tab filter
        all_specific_types = []
        for types in cls.LOC_GAMELINE_MAP.values():
            all_specific_types.extend(types)
        all_allowed_types = cls.GENERIC_LOC_TYPES + all_specific_types

        # All shows everything if there's any content
        # Only show root locations (parent=None) - children handled by recursive template
        if queryset.exists():
            result["wod"] = {
                "name": cls.GAMELINE_SHORT_NAMES.get("wod", "All"),
                "locations": queryset.filter(parent=None),
                "allowed_types": all_allowed_types,
            }

        # Add specific gamelines - include generic types + that gameline's types
        for gl_code in cls.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            gameline_specific_types = cls.LOC_GAMELINE_MAP.get(gl_code, [])
            # Include generic types + this gameline's specific types
            allowed_types = cls.GENERIC_LOC_TYPES + gameline_specific_types
            filtered = queryset.filter(polymorphic_ctype__model__in=allowed_types)
            if filtered.exists():
                # Only show root locations - children handled by recursive template
                result[gl_code] = {
                    "name": cls.GAMELINE_SHORT_NAMES.get(gl_code, gl_code),
                    "locations": filtered.filter(parent=None),
                    "allowed_types": allowed_types,
                }

        return result

    @classmethod
    def group_items_by_gameline(cls, queryset):
        """
        Group items by gameline based on polymorphic content type.

        Args:
            queryset: Item queryset to group

        Returns:
            OrderedDict with gameline codes as keys
        """
        result = OrderedDict()

        # All shows everything if there's any content
        if queryset.exists():
            result["wod"] = {
                "name": cls.GAMELINE_SHORT_NAMES.get("wod", "All"),
                "items": queryset,
            }

        # Add specific gamelines that have content
        for gl_code in cls.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            model_names = cls.ITEM_GAMELINE_MAP.get(gl_code, [])
            if model_names:
                filtered = queryset.filter(polymorphic_ctype__model__in=model_names)
                if filtered.exists():
                    result[gl_code] = {
                        "name": cls.GAMELINE_SHORT_NAMES.get(gl_code, gl_code),
                        "items": filtered,
                    }

        return result

    @classmethod
    def group_scenes_by_month(cls, queryset):
        """
        Group scenes by year/month.

        Args:
            queryset: Scene queryset to group

        Returns:
            List of (date, scenes) tuples
        """
        scenes_list = list(queryset)
        if not scenes_list:
            return []

        return [
            (datetime(year=year, month=month, day=1), list(scenes_in_month))
            for (year, month), scenes_in_month in itertools.groupby(
                scenes_list,
                key=lambda x: (
                    (x.date_of_scene.year, x.date_of_scene.month) if x.date_of_scene else (1900, 1)
                ),
            )
        ]

    @classmethod
    def group_scenes_by_gameline(cls, queryset):
        """
        Group scenes by gameline.

        Scenes have a direct gameline field. Each gameline entry includes
        scenes grouped by month.

        Args:
            queryset: Scene queryset to group

        Returns:
            OrderedDict with gameline codes as keys
        """
        result = OrderedDict()

        # All shows everything if there's any content
        if queryset.exists():
            result["wod"] = {
                "name": cls.GAMELINE_SHORT_NAMES.get("wod", "All"),
                "scenes": queryset,
                "scenes_by_month": cls.group_scenes_by_month(queryset),
            }

        # Add specific gamelines that have content
        for gl_code in cls.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            filtered = queryset.filter(gameline=gl_code)
            if filtered.exists():
                result[gl_code] = {
                    "name": cls.GAMELINE_SHORT_NAMES.get(gl_code, gl_code),
                    "scenes": filtered,
                    "scenes_by_month": cls.group_scenes_by_month(filtered),
                }

        return result

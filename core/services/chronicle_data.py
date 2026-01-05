"""Service for organizing chronicle data by gameline."""

import itertools
from collections import OrderedDict
from datetime import datetime

from django.conf import settings


class ChronicleDataService:
    """
    Service class for organizing and grouping chronicle data by gameline.

    Consolidates gameline grouping logic from ChronicleDetailView into
    a reusable, testable service class.

    Groups polymorphic models by their `gameline` class attribute rather than
    hardcoded model name lists. Models with gameline='wod' appear in all tabs.
    """

    # Gameline ordering from settings (excluding orpheus which isn't fully implemented)
    GAMELINE_ORDER = [k for k in settings.GAMELINES.keys() if k != "orp"]

    @classmethod
    def get_display_name(cls, gameline_code):
        """
        Get display name for gameline tab.

        Derives tab labels from settings.GAMELINES rather than hardcoding.
        Special case: 'wod' returns 'All' for the combined view.
        """
        if gameline_code == "wod":
            return "All"
        gl = settings.GAMELINES.get(gameline_code, {})
        # Extract first word from name (e.g., "Vampire: the Masquerade" -> "Vampire")
        name = gl.get("name", gameline_code)
        return name.split(":")[0] if ":" in name else name

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
                "name": cls.get_display_name("wod"),
                "items": queryset,
            }

        # Add specific gamelines that have content
        for gl_code in cls.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            filtered = queryset.filter(**{gameline_attr: gl_code})
            if filtered.exists():
                result[gl_code] = {
                    "name": cls.get_display_name(gl_code),
                    "items": filtered,
                }

        return result

    @classmethod
    def group_characters_by_gameline(cls, queryset):
        """
        Group characters by gameline using the model's gameline attribute.

        Fetches all characters once and filters in Python by gameline.
        Models with gameline='wod' appear in all gameline tabs.

        Args:
            queryset: Character queryset to group

        Returns:
            OrderedDict with gameline codes as keys
        """
        result = OrderedDict()
        all_characters = list(queryset)

        if not all_characters:
            return result

        # All shows everything
        result["wod"] = {
            "name": cls.get_display_name("wod"),
            "characters": all_characters,
        }

        # Add specific gamelines - include generic (wod) models in each tab
        for gl_code in cls.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            filtered = [c for c in all_characters if c.gameline in (gl_code, "wod")]
            if filtered:
                result[gl_code] = {
                    "name": cls.get_display_name(gl_code),
                    "characters": filtered,
                }

        return result

    @classmethod
    def group_locations_by_gameline(cls, queryset):
        """
        Group locations by gameline using the model's gameline attribute.

        Fetches all locations once and filters in Python by gameline.
        Models with gameline='wod' (generic locations) appear in all tabs.
        Only root locations (parent=None) are returned; children are handled
        by recursive templates.

        Args:
            queryset: Location queryset to group

        Returns:
            OrderedDict with gameline codes as keys
        """
        result = OrderedDict()
        all_locations = list(queryset)

        if not all_locations:
            return result

        # All shows everything - only root locations
        root_locations = [loc for loc in all_locations if loc.parent is None]
        result["wod"] = {
            "name": cls.get_display_name("wod"),
            "locations": root_locations,
        }

        # Add specific gamelines - include generic (wod) models in each tab
        for gl_code in cls.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            # Filter by gameline, include generic locations, only roots
            filtered = [
                loc
                for loc in all_locations
                if loc.gameline in (gl_code, "wod") and loc.parent is None
            ]
            if filtered:
                result[gl_code] = {
                    "name": cls.get_display_name(gl_code),
                    "locations": filtered,
                }

        return result

    @classmethod
    def group_items_by_gameline(cls, queryset):
        """
        Group items by gameline using the model's gameline attribute.

        Fetches all items once and filters in Python by gameline.
        Models with gameline='wod' appear in all gameline tabs.

        Args:
            queryset: Item queryset to group

        Returns:
            OrderedDict with gameline codes as keys
        """
        result = OrderedDict()
        all_items = list(queryset)

        if not all_items:
            return result

        # All shows everything
        result["wod"] = {
            "name": cls.get_display_name("wod"),
            "items": all_items,
        }

        # Add specific gamelines - include generic (wod) models in each tab
        for gl_code in cls.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            filtered = [item for item in all_items if item.gameline in (gl_code, "wod")]
            if filtered:
                result[gl_code] = {
                    "name": cls.get_display_name(gl_code),
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
                "name": cls.get_display_name("wod"),
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
                    "name": cls.get_display_name(gl_code),
                    "scenes": filtered,
                    "scenes_by_month": cls.group_scenes_by_month(filtered),
                }

        return result

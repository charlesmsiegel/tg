import itertools
from collections import OrderedDict
from datetime import datetime

from characters.models.core import CharacterModel
from characters.models.core.character import Character
from core.constants import GameLine
from core.mixins import (
    CharacterOwnerOrSTMixin,
    EditPermissionMixin,
    MessageMixin,
    SpecialUserMixin,
    StorytellerRequiredMixin,
    ViewPermissionMixin,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.timezone import datetime
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from game.forms import (
    AddCharForm,
    ChronicleCharacterCreationForm,
    ChronicleItemCreationForm,
    ChronicleLocationCreationForm,
    JournalEntryForm,
    PostForm,
    SceneCreationForm,
    StoryForm,
    STResponseForm,
    WeeklyXPRequestForm,
)
from game.models import (
    Chronicle,
    Journal,
    JournalEntry,
    ObjectType,
    Post,
    Scene,
    SettingElement,
    Story,
    StoryXPRequest,
    Week,
    WeeklyXPRequest,
)
from items.models.core import ItemModel
from locations.models.core import LocationModel


class ChronicleDetailView(LoginRequiredMixin, DetailView):
    """View for displaying chronicle details. Requires authentication."""

    model = Chronicle
    template_name = "game/chronicle/detail.html"

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

    def get_queryset(self):
        return super().get_queryset().prefetch_related("storytellers", "allowed_objects")

    def _group_by_gameline(self, queryset, gameline_attr="gameline"):
        """
        Group items by gameline, only including gamelines that have content.
        Returns an OrderedDict with 'wod' (All) first if there's content,
        followed by specific gamelines in GAMELINE_ORDER.
        """
        result = OrderedDict()

        # 'wod' (All) shows everything if there's any content
        if queryset.exists():
            result["wod"] = {
                "name": self.GAMELINE_SHORT_NAMES.get("wod", "All"),
                "items": queryset,
            }

        # Add specific gamelines that have content
        for gl_code in self.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            filtered = queryset.filter(**{gameline_attr: gl_code})
            if filtered.exists():
                result[gl_code] = {
                    "name": self.GAMELINE_SHORT_NAMES.get(gl_code, gl_code),
                    "items": filtered,
                }

        return result

    def _group_characters_by_gameline(self, queryset):
        """
        Group characters by gameline based on polymorphic content type.
        Characters don't have a direct gameline field, so we filter by model type.
        """
        result = OrderedDict()

        # Character model to gameline mapping
        char_gameline_map = {
            "vtm": [
                "vtmhuman",
                "ghoul",
                "vampire",
                "revenant",
            ],
            "wta": [
                "wtahuman",
                "kinfolk",
                "werewolf",
                "spiritcharacter",
                "fera",
                "fomor",
                "drone",
            ],
            "mta": [
                "mtahuman",
                "companion",
                "sorcerer",
                "mage",
            ],
            "wto": [
                "wtohuman",
                "wraith",
            ],
            "ctd": [
                "ctdhuman",
                "changeling",
                "nunnehi",
                "inanimae",
                "autumnperson",
            ],
            "htr": [
                "htrhuman",
                "hunter",
            ],
            "mtr": [
                "mtrhuman",
                "mummy",
            ],
            "dtf": [
                "dtfhuman",
                "demon",
                "thrall",
                "earthbound",
            ],
        }

        # All shows everything if there's any content
        if queryset.exists():
            result["wod"] = {
                "name": self.GAMELINE_SHORT_NAMES.get("wod", "All"),
                "characters": queryset,
            }

        # Add specific gamelines that have content
        for gl_code in self.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            model_names = char_gameline_map.get(gl_code, [])
            if model_names:
                filtered = queryset.filter(polymorphic_ctype__model__in=model_names)
                if filtered.exists():
                    result[gl_code] = {
                        "name": self.GAMELINE_SHORT_NAMES.get(gl_code, gl_code),
                        "characters": filtered,
                    }

        return result

    def _group_locations_by_gameline(self, queryset):
        """
        Group locations by gameline based on polymorphic content type.
        Each gameline tab shows generic locations (Location, City) plus
        that gameline's specific locations, excluding other gamelines' locations.
        """
        result = OrderedDict()

        # Generic location types that appear in ALL gameline tabs
        generic_loc_types = ["locationmodel", "city"]

        # Location model to gameline mapping (gameline-specific types only)
        loc_gameline_map = {
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
            "wto": [
                "haunt",
                "necropolis",
                "citadel",
                "nihil",
                "byway",
                "wraithfreehold",
            ],
            "ctd": ["freehold", "dreamrealm", "trod", "holding"],
            "dtf": ["bastion", "reliquary"],
            "htr": ["huntingground", "safehouse"],
            "mtr": ["tomb", "culttemple", "undergroundsanctuary"],
        }

        # Collect all gameline-specific types for the "All" tab filter
        all_specific_types = []
        for types in loc_gameline_map.values():
            all_specific_types.extend(types)
        all_allowed_types = generic_loc_types + all_specific_types

        # All shows everything if there's any content
        # Only show root locations (parent=None) - children handled by recursive template
        if queryset.exists():
            result["wod"] = {
                "name": self.GAMELINE_SHORT_NAMES.get("wod", "All"),
                "locations": queryset.filter(parent=None),
                "allowed_types": all_allowed_types,
            }

        # Add specific gamelines - include generic types + that gameline's types
        for gl_code in self.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            gameline_specific_types = loc_gameline_map.get(gl_code, [])
            # Include generic types + this gameline's specific types
            allowed_types = generic_loc_types + gameline_specific_types
            filtered = queryset.filter(polymorphic_ctype__model__in=allowed_types)
            if filtered.exists():
                # Only show root locations - children handled by recursive template
                result[gl_code] = {
                    "name": self.GAMELINE_SHORT_NAMES.get(gl_code, gl_code),
                    "locations": filtered.filter(parent=None),
                    "allowed_types": allowed_types,
                }

        return result

    def _group_items_by_gameline(self, queryset):
        """
        Group items by gameline based on polymorphic content type.
        """
        result = OrderedDict()

        # Item model to gameline mapping
        item_gameline_map = {
            "vtm": ["bloodstone", "artifact"],
            "wta": ["fetish", "talen"],
            "mta": ["wonder", "grimoire", "device", "sorcererartifact"],
            "wto": ["relic", "wraithartifact", "memoriam"],
            "ctd": ["treasure", "dross"],
            "dtf": ["demonrelic"],
            "htr": ["hunterrelic", "gear"],
            "mtr": ["ushabti", "mummyrelic", "vessel"],
        }

        # All shows everything if there's any content
        if queryset.exists():
            result["wod"] = {
                "name": self.GAMELINE_SHORT_NAMES.get("wod", "All"),
                "items": queryset,
            }

        # Add specific gamelines that have content
        for gl_code in self.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            model_names = item_gameline_map.get(gl_code, [])
            if model_names:
                filtered = queryset.filter(polymorphic_ctype__model__in=model_names)
                if filtered.exists():
                    result[gl_code] = {
                        "name": self.GAMELINE_SHORT_NAMES.get(gl_code, gl_code),
                        "items": filtered,
                    }

        return result

    def _group_scenes_by_month(self, queryset):
        """
        Group scenes by year/month. Returns list of (date, scenes) tuples.
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

    def _group_scenes_by_gameline(self, queryset):
        """
        Group scenes by gameline. Scenes have a direct gameline field.
        Each gameline entry includes scenes grouped by month.
        """
        result = OrderedDict()

        # All shows everything if there's any content
        if queryset.exists():
            result["wod"] = {
                "name": self.GAMELINE_SHORT_NAMES.get("wod", "All"),
                "scenes": queryset,
                "scenes_by_month": self._group_scenes_by_month(queryset),
            }

        # Add specific gamelines that have content
        for gl_code in self.GAMELINE_ORDER:
            if gl_code == "wod":
                continue
            filtered = queryset.filter(gameline=gl_code)
            if filtered.exists():
                result[gl_code] = {
                    "name": self.GAMELINE_SHORT_NAMES.get(gl_code, gl_code),
                    "scenes": filtered,
                    "scenes_by_month": self._group_scenes_by_month(filtered),
                }

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chronicle = self.object

        # --- Common Knowledge (SettingElements) by gameline ---
        all_setting_elements = chronicle.common_knowledge_elements.all()
        setting_elements_by_gameline = self._group_by_gameline(
            all_setting_elements, gameline_attr="gameline"
        )

        # --- Locations ---
        top_locations = (
            LocationModel.objects.top_level().filter(chronicle=chronicle).order_by("name")
        )
        locations_by_gameline = self._group_locations_by_gameline(top_locations)

        # --- Characters by status ---
        active_characters = (
            Character.objects.active()
            .player_characters()
            .with_group_ordering()
            .filter(chronicle=chronicle)
        )
        retired_characters = (
            Character.objects.retired()
            .player_characters()
            .with_group_ordering()
            .filter(chronicle=chronicle)
        )
        deceased_characters = (
            Character.objects.deceased()
            .player_characters()
            .with_group_ordering()
            .filter(chronicle=chronicle)
        )
        npc_characters = (
            Character.objects.active().npcs().with_group_ordering().filter(chronicle=chronicle)
        )

        # --- Items ---
        all_items = ItemModel.objects.for_chronicle(chronicle).order_by("name")
        items_by_gameline = self._group_items_by_gameline(all_items)

        # --- Scenes by status ---
        all_scenes = Scene.objects.filter(chronicle=chronicle).order_by("-date_of_scene")
        active_scenes = all_scenes.filter(finished=False)
        completed_scenes = all_scenes.filter(finished=True)

        context.update(
            {
                # Common Knowledge
                "setting_elements_by_gameline": setting_elements_by_gameline,
                # Characters (base querysets for backward compatibility)
                "character_list": active_characters,
                "retired_characters": retired_characters,
                "deceased_characters": deceased_characters,
                "npc_characters": npc_characters,
                # Characters by gameline
                "active_by_gameline": self._group_characters_by_gameline(active_characters),
                "retired_by_gameline": self._group_characters_by_gameline(retired_characters),
                "deceased_by_gameline": self._group_characters_by_gameline(deceased_characters),
                "npc_by_gameline": self._group_characters_by_gameline(npc_characters),
                # Locations
                "top_locations": top_locations,
                "locations_by_gameline": locations_by_gameline,
                # Items
                "items": all_items,
                "items_by_gameline": items_by_gameline,
                # Scenes by status and gameline
                "all_scenes_by_gameline": self._group_scenes_by_gameline(all_scenes),
                "active_scenes_by_gameline": self._group_scenes_by_gameline(active_scenes),
                "completed_scenes_by_gameline": self._group_scenes_by_gameline(completed_scenes),
                # Forms and other
                "form": SceneCreationForm(chronicle=chronicle),
                "active_scenes": active_scenes,  # Keep for backward compatibility
                "story_form": StoryForm(),
                "header": chronicle.headings,
                # Creation forms for Characters, Locations, Items
                "char_form": ChronicleCharacterCreationForm(
                    chronicle=chronicle, user=self.request.user
                ),
                "loc_form": ChronicleLocationCreationForm(
                    chronicle=chronicle, user=self.request.user
                ),
                "item_form": ChronicleItemCreationForm(chronicle=chronicle, user=self.request.user),
            }
        )
        return context

    def _get_create_redirect_url(self, obj_type, type_name):
        """Get the redirect URL for creating an object of the given type."""
        obj = ObjectType.objects.get(name=type_name)
        gameline = obj.gameline

        # Map gameline codes to URL namespace paths
        gameline_url_map = {
            "wod": "",
            "vtm": "vampire:",
            "wta": "werewolf:",
            "mta": "mage:",
            "wto": "wraith:",
            "ctd": "changeling:",
            "dtf": "demon:",
            "htr": "hunter:",
            "mtr": "mummy:",
        }

        prefix = gameline_url_map.get(gameline, "")

        if obj_type == "char":
            return f"characters:{prefix}create:{type_name}"
        elif obj_type == "loc":
            return f"locations:{prefix}create:{type_name}"
        elif obj_type == "obj":
            return f"items:{prefix}create:{type_name}"

        return None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        chronicle = self.object

        # Handle character creation (redirects to create view)
        if "create_character" in request.POST and "char_type" in request.POST:
            type_name = request.POST["char_type"]
            redirect_url = self._get_create_redirect_url("char", type_name)
            if redirect_url:
                return redirect(redirect_url)

        # Handle location creation (redirects to create view)
        if "create_location" in request.POST and "loc_type" in request.POST:
            type_name = request.POST["loc_type"]
            redirect_url = self._get_create_redirect_url("loc", type_name)
            if redirect_url:
                return redirect(redirect_url)

        # Handle item creation (redirects to create view)
        if "create_item" in request.POST and "item_type" in request.POST:
            type_name = request.POST["item_type"]
            redirect_url = self._get_create_redirect_url("obj", type_name)
            if redirect_url:
                return redirect(redirect_url)

        # Story and scene creation require ST permissions
        create_story_flag = request.POST.get("create_story")
        create_scene_flag = request.POST.get("create_scene")

        if create_story_flag is not None or create_scene_flag is not None:
            # Check if user is a storyteller for story/scene creation
            if not request.user.profile.is_st() and not request.user.is_staff:
                messages.error(request, "Only storytellers can create stories and scenes.")
                raise PermissionDenied("Only storytellers can create stories and scenes")

            if create_story_flag is not None:
                story = Story.objects.create(name=request.POST["name"])
                messages.success(request, f"Story '{story.name}' created successfully!")

            if create_scene_flag is not None:
                location = get_object_or_404(LocationModel, pk=request.POST["location"])
                scene = chronicle.add_scene(
                    request.POST["name"],
                    location,
                    date_of_scene=request.POST["date_of_scene"],
                    gameline=request.POST.get("gameline", "wod"),
                )
                messages.success(request, f"Scene '{request.POST['name']}' created successfully!")
                return redirect(scene)

        return self.render_to_response(self.get_context_data())


class SceneDetailView(LoginRequiredMixin, DetailView):
    """View for displaying scene details. Requires authentication."""

    model = Scene
    template_name = "game/scene/detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("location", "chronicle")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scene = self.object
        user = self.request.user

        context["posts"] = Post.objects.for_scene_optimized(scene)

        if user.is_authenticated:
            add_char_form = AddCharForm(user=user, scene=scene)
            context.update(
                {
                    "add_char_form": add_char_form,
                    "num_chars": add_char_form.fields["character_to_add"].queryset.count(),
                    "num_logged_in_chars": scene.characters.owned_by(user).count(),
                    "first_char": scene.characters.owned_by(user).first(),
                    "post_form": PostForm(user=user, scene=scene),
                }
            )

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        scene = self.object

        if "close_scene" in request.POST.keys():
            # Only storytellers for THIS chronicle can close scenes
            is_admin = request.user.is_superuser or request.user.is_staff
            is_chronicle_st = False
            if scene.chronicle:
                is_chronicle_st = (
                    scene.chronicle.head_st == request.user
                    or scene.chronicle.storytellers.filter(pk=request.user.pk).exists()
                )
            if not (is_admin or is_chronicle_st):
                messages.error(request, "You are not a storyteller for this chronicle.")
                raise PermissionDenied("You are not a storyteller for this chronicle")
            scene.close()
            messages.success(request, f"Scene '{scene.name}' closed successfully!")
        elif "character_to_add" in request.POST.keys():
            c = get_object_or_404(CharacterModel, pk=request.POST["character_to_add"])
            # Check that user owns the character
            if c.owner != request.user:
                messages.error(request, "You can only add your own characters.")
                raise PermissionDenied("You can only add your own characters")
            scene.add_character(c)
            messages.success(request, f"Character '{c.name}' added to scene!")
        elif "message" in request.POST.keys():
            post_form = PostForm(request.POST, user=request.user, scene=scene)
            if post_form.is_valid():
                num_logged_in_chars = scene.characters.owned_by(request.user).count()
                if num_logged_in_chars == 1:
                    character = scene.characters.owned_by(request.user).first()
                else:
                    character = get_object_or_404(CharacterModel, pk=request.POST["character"])
                # Check that user owns the character
                if character.owner != request.user:
                    messages.error(request, "You can only post as your own characters.")
                    raise PermissionDenied("You can only post as your own characters")
                try:
                    message = self.straighten_quotes(request.POST["message"])
                    scene.add_post(character, request.POST["display_name"], message)
                    messages.success(request, "Post added successfully!")
                except ValueError:
                    messages.error(request, "Command does not match the expected format.")
            else:
                messages.error(request, "Failed to create post. Please check your input.")
        return redirect(reverse("game:scene", kwargs={"pk": scene.pk}))

    @staticmethod
    def straighten_quotes(s):
        # Define the Unicode code points for various quotation marks and apostrophes
        single_quote_chars = [
            0x2018,  # ‘ LEFT SINGLE QUOTATION MARK
            0x2019,  # ’ RIGHT SINGLE QUOTATION MARK
            0x201A,  # ‚ SINGLE LOW-9 QUOTATION MARK
            0x201B,  # ‛ SINGLE HIGH-REVERSED-9 QUOTATION MARK
            0x2032,  # ′ PRIME
            0x02B9,  # ʹ MODIFIER LETTER PRIME
            0x02BB,  # ʻ MODIFIER LETTER TURNED COMMA
            0x02BC,  # ʼ MODIFIER LETTER APOSTROPHE
            0x02BD,  # ʽ MODIFIER LETTER REVERSED COMMA
            0x275B,  # ❛ HEAVY SINGLE TURNED COMMA QUOTATION MARK ORNAMENT
            0x275C,  # ❜ HEAVY SINGLE COMMA QUOTATION MARK ORNAMENT
            0xFF07,  # ＇ FULLWIDTH APOSTROPHE
            0x00B4,  # ´ ACUTE ACCENT
            0x0060,  # ` GRAVE ACCENT
        ]

        double_quote_chars = [
            0x201C,  # “ LEFT DOUBLE QUOTATION MARK
            0x201D,  # ” RIGHT DOUBLE QUOTATION MARK
            0x201E,  # „ DOUBLE LOW-9 QUOTATION MARK
            0x201F,  # ‟ DOUBLE HIGH-REVERSED-9 QUOTATION MARK
            0x2033,  # ″ DOUBLE PRIME
            0x02BA,  # ʺ MODIFIER LETTER DOUBLE PRIME
            0x275D,  # ❝ HEAVY DOUBLE TURNED COMMA QUOTATION MARK ORNAMENT
            0x275E,  # ❞ HEAVY DOUBLE COMMA QUOTATION MARK ORNAMENT
            0xFF02,  # ＂ FULLWIDTH QUOTATION MARK
        ]

        # Create a translation table
        translation_table = {}
        for code_point in single_quote_chars:
            translation_table[code_point] = ord("'")
        for code_point in double_quote_chars:
            translation_table[code_point] = ord('"')

        # Translate the string using the translation table
        return s.translate(translation_table)


class CommandsView(LoginRequiredMixin, TemplateView):
    template_name = "game/scene/commands.html"


class JournalDetailView(SpecialUserMixin, ViewPermissionMixin, DetailView):
    model = Journal
    template_name = "game/journal/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_entry_form"] = JournalEntryForm(instance=self.object)
        context["st_response_forms"] = [
            STResponseForm(entry=e, prefix=f"entry-{e.pk}") for e in self.object.all_entries()
        ]
        context["is_approved_user"] = self.check_if_special_user(
            self.object.character, self.request.user
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        submit_entry = request.POST.get("submit_entry")
        submit_response = request.POST.get("submit_response")
        if submit_entry is not None:
            # Check that user owns the character/journal
            if self.object.character.owner != request.user:
                messages.error(request, "You can only add entries to your own journal.")
                raise PermissionDenied("You can only add entries to your own journal")
            f = JournalEntryForm(request.POST, instance=self.object)
            if f.is_valid():
                f.save()
                messages.success(request, "Journal entry added successfully!")
            else:
                messages.error(request, "Failed to add journal entry. Please check your input.")
        if submit_response is not None:
            # Check that user is a storyteller
            if not request.user.profile.is_st():
                messages.error(request, "Only storytellers can add ST responses.")
                raise PermissionDenied("Only storytellers can add ST responses")
            tmp = [x for x in request.POST.keys() if "entry" in x][0]
            tmp = tmp.split("-")[1]
            entry = get_object_or_404(JournalEntry, pk=tmp)
            f = STResponseForm(
                {"st_message": request.POST[f"entry-{tmp}-st_message"]},
                entry=entry,
            )
            if f.is_valid():
                f.save()
                messages.success(request, "ST response added successfully!")
            else:
                messages.error(request, "Failed to add ST response. Please check your input.")
        return render(request, "game/journal/detail.html", self.get_context_data(**kwargs))


class ChronicleListView(LoginRequiredMixin, ListView):
    model = Chronicle
    ordering = ["name"]
    template_name = "game/chronicle/list.html"


class SceneListView(LoginRequiredMixin, ListView):
    model = Scene
    ordering = ["-date_of_scene", "-date_played"]
    template_name = "game/scene/list.html"


class JournalListView(LoginRequiredMixin, ListView):
    model = Journal
    ordering = ["character__name"]
    template_name = "game/journal/list.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related("character", "character__owner")
        # Filter by ownership if requested
        filter_by = self.request.GET.get("filter")
        if filter_by == "mine":
            queryset = queryset.filter(character__owner=self.request.user)
        elif filter_by == "st":
            # Show journals for characters in chronicles where user is ST
            st_chronicles = Chronicle.objects.filter(
                models.Q(head_st=self.request.user) | models.Q(storytellers=self.request.user)
            )
            queryset = queryset.filter(character__chronicle__in=st_chronicles)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_filter"] = self.request.GET.get("filter", "all")
        # Annotate journals with entry count
        from django.db.models import Count, Max

        journals_with_stats = {}
        for journal in context["object_list"]:
            journals_with_stats[journal.pk] = {
                "entry_count": journal.journalentry_set.count(),
                "latest_entry": journal.journalentry_set.aggregate(Max("date"))["date__max"],
            }
        context["journal_stats"] = journals_with_stats
        return context


class StoryDetailView(LoginRequiredMixin, DetailView):
    model = Story
    template_name = "game/story/detail.html"


class StoryListView(LoginRequiredMixin, ListView):
    model = Story
    ordering = ["name"]
    template_name = "game/story/list.html"


class StoryCreateView(StorytellerRequiredMixin, MessageMixin, CreateView):
    model = Story
    fields = ["name"]
    template_name = "game/story/form.html"
    success_message = "Story '{name}' created successfully!"
    error_message = "Failed to create story. Please correct the errors below."

    def get_success_url(self):
        return reverse("game:story:detail", kwargs={"pk": self.object.pk})


class StoryUpdateView(StorytellerRequiredMixin, MessageMixin, UpdateView):
    model = Story
    fields = ["name"]
    template_name = "game/story/form.html"
    success_message = "Story '{name}' updated successfully!"
    error_message = "Failed to update story. Please correct the errors below."

    def get_success_url(self):
        return reverse("game:story:detail", kwargs={"pk": self.object.pk})


# Week Views
class WeekListView(LoginRequiredMixin, ListView):
    model = Week
    ordering = ["-end_date"]
    template_name = "game/week/list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_st"] = self.request.user.profile.is_st()
        return context


class WeekDetailView(LoginRequiredMixin, DetailView):
    model = Week
    template_name = "game/week/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_st"] = self.request.user.profile.is_st()
        context["finished_scenes"] = self.object.finished_scenes().with_location()
        context["weekly_characters"] = self.object.weekly_characters()

        # Get XP requests for this week
        context["xp_requests"] = WeeklyXPRequest.objects.filter(week=self.object).select_related(
            "character"
        )

        # Separate pending and approved requests
        context["pending_requests"] = context["xp_requests"].filter(approved=False)
        context["approved_requests"] = context["xp_requests"].filter(approved=True)

        return context


class WeekCreateView(StorytellerRequiredMixin, MessageMixin, CreateView):
    model = Week
    fields = ["end_date"]
    template_name = "game/week/form.html"
    success_message = "Week created successfully!"
    error_message = "Failed to create week. Please correct the errors below."

    def get_success_url(self):
        return reverse("game:week:detail", kwargs={"pk": self.object.pk})


class WeekUpdateView(StorytellerRequiredMixin, MessageMixin, UpdateView):
    model = Week
    fields = ["end_date"]
    template_name = "game/week/form.html"
    success_message = "Week updated successfully!"
    error_message = "Failed to update week. Please correct the errors below."

    def get_success_url(self):
        return reverse("game:week:detail", kwargs={"pk": self.object.pk})


# WeeklyXPRequest Views
class WeeklyXPRequestListView(LoginRequiredMixin, ListView):
    model = WeeklyXPRequest
    template_name = "game/weekly_xp_request/list.html"
    ordering = ["-week__end_date", "character__name"]
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset().select_related("character", "week")
        # If not ST, only show own character requests
        if not self.request.user.profile.is_st():
            qs = qs.filter(character__owner=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_st"] = self.request.user.profile.is_st()
        if context["is_st"]:
            context["pending_count"] = WeeklyXPRequest.objects.filter(approved=False).count()
        return context


class WeeklyXPRequestDetailView(CharacterOwnerOrSTMixin, DetailView):
    model = WeeklyXPRequest
    template_name = "game/weekly_xp_request/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_st"] = self.request.user.profile.is_st()
        context["is_owner"] = self.object.character.owner == self.request.user

        # Add approval form for STs
        if context["is_st"] and not self.object.approved:
            context["approval_form"] = WeeklyXPRequestForm(
                instance=self.object,
                character=self.object.character,
                week=self.object.week,
            )

        return context


class WeeklyXPRequestCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = WeeklyXPRequest
    form_class = WeeklyXPRequestForm
    template_name = "game/weekly_xp_request/form.html"
    success_message = "Weekly XP request submitted successfully!"
    error_message = "Failed to submit XP request. Please correct the errors below."

    def dispatch(self, request, *args, **kwargs):
        """Check that user owns the character before allowing access."""
        character = get_object_or_404(CharacterModel, pk=kwargs["character_pk"])

        # Allow admins and staff
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        # Check that user owns the character
        if character.owner != request.user:
            messages.error(request, "You can only submit requests for your own characters.")
            raise PermissionDenied("You can only submit requests for your own characters")

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = get_object_or_404(CharacterModel, pk=self.kwargs["character_pk"])
        kwargs["week"] = get_object_or_404(Week, pk=self.kwargs["week_pk"])
        return kwargs

    def form_valid(self, form):
        # Check if request already exists
        if WeeklyXPRequest.objects.filter(character=form.character, week=form.week).exists():
            messages.error(
                self.request,
                f"XP request already exists for {form.character.name} for this week.",
            )
            return redirect("game:week:detail", pk=form.week.pk)

        form.player_save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("game:week:detail", kwargs={"pk": self.object.week.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = get_object_or_404(CharacterModel, pk=self.kwargs["character_pk"])
        context["week"] = get_object_or_404(Week, pk=self.kwargs["week_pk"])
        return context


class WeeklyXPRequestApproveView(StorytellerRequiredMixin, View):
    """View for STs to approve/deny weekly XP requests."""

    def post(self, request, *args, **kwargs):
        xp_request = get_object_or_404(WeeklyXPRequest, pk=kwargs["pk"])

        if xp_request.approved:
            messages.warning(request, "This XP request has already been approved.")
            return redirect("game:weekly_xp_request:detail", pk=xp_request.pk)

        form = WeeklyXPRequestForm(
            request.POST,
            instance=xp_request,
            character=xp_request.character,
            week=xp_request.week,
        )

        if form.is_valid():
            form.st_save()
            messages.success(
                request,
                f"XP request for {xp_request.character.name} approved successfully! "
                f"{form.instance.total_xp()} XP awarded.",
            )
            return redirect("game:week:detail", pk=xp_request.week.pk)
        else:
            messages.error(request, "Failed to approve XP request. Please check the form.")
            return redirect("game:weekly_xp_request:detail", pk=xp_request.pk)


class WeeklyXPRequestBatchApproveView(StorytellerRequiredMixin, View):
    """View for STs to batch approve multiple weekly XP requests at once."""

    def post(self, request, *args, **kwargs):
        # Get list of request IDs from POST data
        request_ids = request.POST.getlist("request_ids")

        if not request_ids:
            messages.warning(request, "No requests selected for approval.")
            return redirect(request.META.get("HTTP_REFERER", "game:week:list"))

        # Fetch all pending requests
        pending_requests = WeeklyXPRequest.objects.filter(
            pk__in=request_ids, approved=False
        ).select_related("character", "week")

        if not pending_requests.exists():
            messages.warning(request, "No pending requests found to approve.")
            return redirect(request.META.get("HTTP_REFERER", "game:week:list"))

        # Track results
        approved_count = 0
        total_xp = 0
        week_pk = None

        for xp_request in pending_requests:
            # Approve the request as-is (using submitted XP categories)
            xp_request.approved = True

            # Calculate and award XP
            xp_increase = xp_request.total_xp()
            xp_request.character.xp += xp_increase
            xp_request.character.save()
            xp_request.save()

            approved_count += 1
            total_xp += xp_increase
            week_pk = xp_request.week.pk

        if approved_count > 0:
            messages.success(
                request,
                f"Successfully approved {approved_count} XP request{'s' if approved_count != 1 else ''}. "
                f"Total {total_xp} XP awarded.",
            )

        # Redirect back to week detail if we have the week pk
        if week_pk:
            return redirect("game:week:detail", pk=week_pk)
        return redirect("game:week:list")


# StoryXPRequest Views
class StoryXPRequestListView(LoginRequiredMixin, ListView):
    model = StoryXPRequest
    template_name = "game/story_xp_request/list.html"
    ordering = ["story__name", "character__name"]
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset().select_related("character", "story")
        # If not ST, only show own character requests
        if not self.request.user.profile.is_st():
            qs = qs.filter(character__owner=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_st"] = self.request.user.profile.is_st()
        return context


class StoryXPRequestDetailView(CharacterOwnerOrSTMixin, DetailView):
    model = StoryXPRequest
    template_name = "game/story_xp_request/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_st"] = self.request.user.profile.is_st()
        context["is_owner"] = self.object.character.owner == self.request.user
        return context


# SettingElement Views
class SettingElementListView(LoginRequiredMixin, ListView):
    model = SettingElement
    template_name = "game/setting_element/list.html"
    ordering = ["name"]
    paginate_by = 50


class SettingElementDetailView(LoginRequiredMixin, DetailView):
    model = SettingElement
    template_name = "game/setting_element/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_st"] = self.request.user.profile.is_st()
        # Find chronicles that use this setting element
        context["chronicles"] = Chronicle.objects.filter(common_knowledge_elements=self.object)
        return context


class SettingElementCreateView(StorytellerRequiredMixin, MessageMixin, CreateView):
    model = SettingElement
    fields = ["name", "description", "gameline"]
    template_name = "game/setting_element/form.html"
    success_message = "Setting element '{name}' created successfully!"
    error_message = "Failed to create setting element. Please correct the errors below."

    def get_success_url(self):
        return reverse("game:setting_element:detail", kwargs={"pk": self.object.pk})


class SettingElementUpdateView(StorytellerRequiredMixin, MessageMixin, UpdateView):
    model = SettingElement
    fields = ["name", "description", "gameline"]
    template_name = "game/setting_element/form.html"
    success_message = "Setting element '{name}' updated successfully!"
    error_message = "Failed to update setting element. Please correct the errors below."

    def get_success_url(self):
        return reverse("game:setting_element:detail", kwargs={"pk": self.object.pk})

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Max, OuterRef, Subquery
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from characters.models.core import CharacterModel
from characters.models.core.character import Character
from core.create_redirects import resolve_object_type_url
from core.mixins import (
    CharacterOwnerOrSTMixin,
    MessageMixin,
    OwnerRequiredMixin,
    SpecialUserMixin,
    StorytellerRequiredMixin,
    ViewPermissionMixin,
)
from core.permission_context import get_object_permissions, prepare_permission_objects
from core.permissions import Permission, PermissionManager
from core.services import ChronicleDataService
from game.forms import (
    AddCharForm,
    ChronicleCharacterCreationForm,
    ChronicleForm,
    ChronicleItemCreationForm,
    ChronicleLocationCreationForm,
    FreebieSpendingRecordForm,
    JournalEntryForm,
    PostForm,
    SceneCreationForm,
    SceneForm,
    StoryForm,
    StoryXPRequestForm,
    STResponseForm,
    WeeklyXPRequestForm,
    XPSpendingRequestApprovalForm,
    XPSpendingRequestForm,
)
from game.models import (
    Chronicle,
    FreebieSpendingRecord,
    Journal,
    JournalEntry,
    Post,
    Scene,
    SettingElement,
    Story,
    StoryXPRequest,
    STRelationship,
    Week,
    WeeklyXPRequest,
    XPSpendingRequest,
)
from game.security import (
    filter_private_records,
    filter_scenes,
    readable_chronicles,
    staffed_chronicles,
)
from game.spending_approval import (
    SpendingDecisionError,
    decide_spending_request,
    require_spending_approver,
)
from items.models.core import ItemModel
from locations.models.core import LocationModel


def _has_st_read_rows(request, rows):
    """A presentation flag for the prepared page, never approval authority."""
    if request.user.is_staff or request.user.is_superuser:
        return True
    return any(get_object_permissions(request, row).is_chronicle_st for row in rows)


class ChronicleDetailView(LoginRequiredMixin, DetailView):
    """View for displaying chronicle details. Requires authentication."""

    model = Chronicle
    template_name = "game/chronicle/detail.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("storytellers", "allowed_objects")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chronicle = self.object
        context["can_manage_chronicle"] = PermissionManager.can_manage_chronicle(
            self.request.user, chronicle, self.request
        )

        # --- Common Knowledge (SettingElements) by gameline ---
        all_setting_elements = chronicle.common_knowledge_elements.all()
        setting_elements_by_gameline = ChronicleDataService.group_by_gameline(
            all_setting_elements, gameline_attr="gameline"
        )

        # --- Locations ---
        top_locations = (
            LocationModel.objects.top_level().filter(chronicle=chronicle).order_by("name")
        )

        # --- Characters by status ---
        # Use select_related to prevent N+1 queries when accessing owner.username
        # and owner.profile in templates
        active_characters = (
            Character.objects.active()
            .player_characters()
            .with_group_ordering()
            .filter(chronicle=chronicle)
            .select_related("owner", "owner__profile")
        )
        retired_characters = (
            Character.objects.retired()
            .player_characters()
            .with_group_ordering()
            .filter(chronicle=chronicle)
            .select_related("owner", "owner__profile")
        )
        deceased_characters = (
            Character.objects.deceased()
            .player_characters()
            .with_group_ordering()
            .filter(chronicle=chronicle)
            .select_related("owner", "owner__profile")
        )
        npc_characters = (
            Character.objects.active()
            .npcs()
            .with_group_ordering()
            .filter(chronicle=chronicle)
            .select_related("owner", "owner__profile")
        )

        # --- Items ---
        all_items = ItemModel.objects.for_chronicle(chronicle).order_by("name")

        # These tables include owner, type, status and object relationships.
        # A chronicle player may open every object's public card elsewhere,
        # but only full readers may receive rows in this richer context.
        if not staffed_chronicles(self.request.user).filter(pk=chronicle.pk).exists():
            # Location rows recurse through children in the template, so a
            # filtered parent alone could still expose another owner's child.
            top_locations = top_locations.none()
            active_characters = active_characters.filter(owner=self.request.user)
            retired_characters = retired_characters.filter(owner=self.request.user)
            deceased_characters = deceased_characters.filter(owner=self.request.user)
            npc_characters = npc_characters.filter(owner=self.request.user)
            all_items = all_items.filter(owner=self.request.user)
        locations_by_gameline = ChronicleDataService.group_locations_by_gameline(top_locations)
        items_by_gameline = ChronicleDataService.group_items_by_gameline(all_items)

        # --- Scenes by status ---
        all_scenes = filter_scenes(
            Scene.objects.filter(chronicle=chronicle), self.request.user
        ).order_by("-date_of_scene")
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
                "active_by_gameline": ChronicleDataService.group_characters_by_gameline(
                    active_characters
                ),
                "retired_by_gameline": ChronicleDataService.group_characters_by_gameline(
                    retired_characters
                ),
                "deceased_by_gameline": ChronicleDataService.group_characters_by_gameline(
                    deceased_characters
                ),
                "npc_by_gameline": ChronicleDataService.group_characters_by_gameline(
                    npc_characters
                ),
                # Locations
                "top_locations": top_locations,
                "locations_by_gameline": locations_by_gameline,
                # Items
                "items": all_items,
                "items_by_gameline": items_by_gameline,
                # Scenes by status and gameline
                "all_scenes_by_gameline": ChronicleDataService.group_scenes_by_gameline(all_scenes),
                "active_scenes_by_gameline": ChronicleDataService.group_scenes_by_gameline(
                    active_scenes
                ),
                "completed_scenes_by_gameline": ChronicleDataService.group_scenes_by_gameline(
                    completed_scenes
                ),
                # Forms and other
                "form": SceneCreationForm(chronicle=chronicle, user=self.request.user),
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
        return resolve_object_type_url(obj_type, type_name)

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
            if create_story_flag is not None:
                if not PermissionManager.can_manage_chronicle(request.user, chronicle, request):
                    raise PermissionDenied("Chronicle head ST required")
                form = StoryForm(request.POST)
                if not form.is_valid():
                    return self.render_to_response(self.get_context_data())
                story = form.save()
                messages.success(request, f"Story '{story.name}' created successfully!")

            if create_scene_flag is not None:
                if not (
                    PermissionManager.can_manage_chronicle(request.user, chronicle, request)
                    or STRelationship.objects.filter(
                        user=request.user, chronicle=chronicle
                    ).exists()
                ):
                    raise PermissionDenied("Matching chronicle ST required")
                form = SceneCreationForm(request.POST, chronicle=chronicle, user=request.user)
                if not form.is_valid():
                    return self.render_to_response(self.get_context_data())
                gameline = form.cleaned_data["gameline"]
                if not PermissionManager.can_manage_scope(
                    request.user, chronicle, gameline, request
                ):
                    raise PermissionDenied("Matching chronicle ST required")
                location = form.cleaned_data["location"]
                scene = chronicle.add_scene(
                    form.cleaned_data["name"],
                    location,
                    date_of_scene=form.cleaned_data["date_of_scene"],
                    gameline=gameline,
                )
                messages.success(request, f"Scene '{scene.name}' created successfully!")
                return redirect(scene)

        return self.render_to_response(self.get_context_data())


class SceneDetailView(DetailView):
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
        if scene.finished:
            raise PermissionDenied("Finished scenes are read-only")

        if "close_scene" in request.POST.keys():
            if not PermissionManager.can_manage_scope(
                request.user, scene.chronicle, scene.gameline, request
            ):
                raise PermissionDenied("Matching chronicle ST required")
            scene.close()
            messages.success(request, f"Scene '{scene.name}' closed successfully!")
        elif "character_to_add" in request.POST.keys():
            character_pk = request.POST["character_to_add"]
            if (
                len(character_pk) > 20
                or not character_pk.isascii()
                or not character_pk.isdecimal()
                or int(character_pk) < 1
            ):
                return HttpResponseBadRequest("Invalid character")
            c = get_object_or_404(CharacterModel, pk=character_pk)
            if c.owner != request.user and not PermissionManager.can_manage_scope(
                request.user, scene.chronicle, scene.gameline, request
            ):
                raise PermissionDenied("Matching scene ST required to add another character")
            if c.chronicle_id != scene.chronicle_id:
                raise PermissionDenied("Character belongs to another chronicle")
            scene.add_character(c)
            messages.success(request, f"Character '{c.name}' added to scene!")
        elif "message" in request.POST.keys():
            post_form = PostForm(request.POST, user=request.user, scene=scene)
            if post_form.is_valid():
                num_logged_in_chars = scene.characters.owned_by(request.user).count()
                if num_logged_in_chars == 0:
                    raise PermissionDenied("No character in this scene")
                if num_logged_in_chars == 1:
                    character = scene.characters.owned_by(request.user).first()
                else:
                    character = post_form.cleaned_data["character"]
                # Check that user owns the character
                if character.owner != request.user:
                    messages.error(request, "You can only post as your own characters.")
                    raise PermissionDenied("You can only post as your own characters")
                if (
                    character.chronicle_id != scene.chronicle_id
                    or not scene.characters.filter(pk=character.pk).exists()
                ):
                    raise PermissionDenied("Character is not in this scene")
                try:
                    message = self.straighten_quotes(post_form.cleaned_data["message"])
                    scene.add_post(character, post_form.cleaned_data["display_name"], message)
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
            character = self.object.character
            if not PermissionManager.user_has_permission(
                request.user, character, Permission.EDIT_FULL, request=request
            ):
                raise PermissionDenied("Matching chronicle ST required")
            if (
                len(submit_response) > 20
                or not submit_response.isascii()
                or not submit_response.isdecimal()
                or int(submit_response) < 1
            ):
                raise Http404("Entry not found")
            entry = get_object_or_404(JournalEntry, pk=submit_response, journal=self.object)
            f = STResponseForm(
                {"st_message": request.POST.get(f"entry-{entry.pk}-st_message", "")},
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

    def get_queryset(self):
        return readable_chronicles(self.request.user).order_by("name")


class SceneListView(ListView):
    model = Scene
    ordering = ["-date_of_scene", "-date_played"]
    template_name = "game/scene/list.html"

    def get_queryset(self):
        # Pre-fetch related objects to prevent N+1 queries
        # location is accessed in Scene.__str__ when name is empty
        return filter_scenes(
            super().get_queryset().select_related("chronicle", "location"),
            self.request.user,
        )


class JournalListView(LoginRequiredMixin, ListView):
    model = Journal
    ordering = ["character__name"]
    template_name = "game/journal/list.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("character", "character__owner")
            .annotate(
                entry_count=Count("entries"),
                latest_entry=Max("entries__date"),
            )
        )
        queryset = filter_private_records(queryset, self.request.user)
        # Filter by ownership if requested
        filter_by = self.request.GET.get("filter")
        if filter_by == "mine":
            queryset = queryset.filter(character__owner=self.request.user)
        elif filter_by == "st":
            # Show journals for characters in chronicles where user is ST
            queryset = queryset.filter(
                character__chronicle__in=staffed_chronicles(self.request.user)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_filter"] = self.request.GET.get("filter", "all")
        context["show_chronicle_filter"] = staffed_chronicles(self.request.user).exists()
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
        from datetime import timedelta

        from django.db.models import Max

        context = super().get_context_data(**kwargs)
        context["can_manage_global_records"] = (
            self.request.user.is_staff or self.request.user.is_superuser
        )

        # Pre-compute finished scene counts for all weeks in the page to avoid N+1 queries
        # Get all finished scenes with their latest post dates in one query
        latest_post_subquery = (
            Post.objects.filter(scene=OuterRef("pk"))
            .values("scene")
            .annotate(latest_dt=Max("datetime_created"))
            .values("latest_dt")
        )

        finished_scenes = list(
            filter_scenes(Scene.objects.filter(finished=True), self.request.user)
            .annotate(latest_post_date=Subquery(latest_post_subquery))
            .values("pk", "latest_post_date")
        )

        # Attach scene counts to each week object to avoid N+1 queries in template
        for week in context["object_list"]:
            start_date = week.end_date - timedelta(days=7)
            week.cached_scene_count = sum(
                1
                for scene in finished_scenes
                if scene["latest_post_date"]
                and start_date <= scene["latest_post_date"].date() <= week.end_date
            )

        return context


class WeekDetailView(LoginRequiredMixin, DetailView):
    model = Week
    template_name = "game/week/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_manage_global_records"] = (
            self.request.user.is_staff or self.request.user.is_superuser
        )
        context["finished_scenes"] = filter_scenes(
            self.object.finished_scenes().with_location(), self.request.user
        )
        visible_scene_ids = context["finished_scenes"].values("pk")
        context["weekly_characters"] = (
            self.object.weekly_characters().filter(scenes__pk__in=visible_scene_ids).distinct()
        )

        # Get XP requests for this week
        context["xp_requests"] = filter_private_records(
            WeeklyXPRequest.objects.filter(week=self.object).select_related("character"),
            self.request.user,
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
        return filter_private_records(qs, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prepare_permission_objects(self.request, list(context["object_list"]))
        context["show_owner_column"] = _has_st_read_rows(self.request, context["object_list"])
        if context["show_owner_column"]:
            context["pending_count"] = self.get_queryset().filter(approved=False).count()
        return context


class WeeklyXPRequestDetailView(CharacterOwnerOrSTMixin, DetailView):
    model = WeeklyXPRequest
    template_name = "game/weekly_xp_request/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_perms"] = get_object_permissions(self.request, self.object.character)
        context["is_owner"] = self.object.character.owner == self.request.user

        # Add approval form for STs
        if context["object_perms"].can_approve_spending and not self.object.approved:
            context["approval_form"] = WeeklyXPRequestForm(
                instance=self.object,
                character=self.object.character,
                week=self.object.week,
            )

        return context


class WeeklyXPRequestCreateView(LoginRequiredMixin, OwnerRequiredMixin, MessageMixin, CreateView):
    model = WeeklyXPRequest
    form_class = WeeklyXPRequestForm
    template_name = "game/weekly_xp_request/form.html"
    success_message = "Weekly XP request submitted successfully!"
    error_message = "Failed to submit XP request. Please correct the errors below."

    # URL-based character ownership check
    owner_check_model = CharacterModel
    owner_check_kwarg = "character_pk"
    owner_check_attr = "character"
    owner_check_message = "You can only submit requests for your own characters."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = self.character  # Set by OwnerRequiredMixin
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
        context["character"] = self.character  # Set by OwnerRequiredMixin
        context["week"] = get_object_or_404(Week, pk=self.kwargs["week_pk"])
        return context


class WeeklyXPRequestApproveView(LoginRequiredMixin, View):
    """View for STs to approve/deny weekly XP requests."""

    def post(self, request, *args, **kwargs):
        xp_request = get_object_or_404(WeeklyXPRequest, pk=kwargs["pk"])

        require_spending_approver(request.user, xp_request.character)

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


class WeeklyXPRequestBatchApproveView(LoginRequiredMixin, View):
    """View for STs to batch approve multiple weekly XP requests at once."""

    def post(self, request, *args, **kwargs):
        # Get list of request IDs from POST data
        request_ids = request.POST.getlist("request_ids")

        if not request_ids:
            messages.warning(request, "No requests selected for approval.")
            return redirect(request.META.get("HTTP_REFERER", "game:week:list"))

        if len(request_ids) > 100 or any(
            not value.isascii() or not value.isdecimal() for value in request_ids
        ):
            return HttpResponseBadRequest("Invalid request IDs")
        requested = set(map(int, request_ids))

        # Fetch all pending requests
        pending_requests = WeeklyXPRequest.objects.filter(
            pk__in=requested, approved=False
        ).select_related("character", "week")

        pending_requests = list(pending_requests)
        if len(pending_requests) != len(requested) or any(
            not PermissionManager.user_has_permission(
                request.user, xp_request.character, Permission.VIEW_FULL, request=request
            )
            for xp_request in pending_requests
        ):
            return HttpResponse("Not found", status=404, content_type="text/plain")

        for xp_request in pending_requests:
            require_spending_approver(request.user, xp_request.character)

        # Track results
        approved_count = 0
        total_xp = 0
        week_pk = None

        # Use atomic transaction to ensure all approvals succeed or all fail
        with transaction.atomic():
            for xp_request in pending_requests:
                # Approve the request using model method
                xp_increase = xp_request.approve()

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
        return filter_private_records(qs, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prepare_permission_objects(self.request, list(context["object_list"]))
        context["show_owner_column"] = _has_st_read_rows(self.request, context["object_list"])
        return context


class StoryXPRequestDetailView(CharacterOwnerOrSTMixin, DetailView):
    model = StoryXPRequest
    template_name = "game/story_xp_request/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_perms"] = get_object_permissions(self.request, self.object.character)
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
        context["can_manage_global_records"] = (
            self.request.user.is_staff or self.request.user.is_superuser
        )
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


# XPSpendingRequest Views
class XPSpendingRequestListView(LoginRequiredMixin, ListView):
    model = XPSpendingRequest
    template_name = "game/xp_spending_request/list.html"
    ordering = ["-created_at"]
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset().select_related("character", "character__owner", "approved_by")
        return filter_private_records(qs, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prepare_permission_objects(self.request, list(context["object_list"]))
        context["show_owner_column"] = _has_st_read_rows(self.request, context["object_list"])
        if context["show_owner_column"]:
            context["pending_count"] = self.get_queryset().filter(approved="Pending").count()
        return context


class XPSpendingRequestDetailView(CharacterOwnerOrSTMixin, DetailView):
    model = XPSpendingRequest
    template_name = "game/xp_spending_request/detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("character", "character__owner", "approved_by")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_perms"] = get_object_permissions(self.request, self.object.character)
        context["is_owner"] = self.object.character.owner == self.request.user

        # Add approval form for STs
        if context["object_perms"].can_approve_spending and self.object.approved == "Pending":
            context["approval_form"] = XPSpendingRequestApprovalForm(instance=self.object)

        return context


class XPSpendingRequestCreateView(LoginRequiredMixin, OwnerRequiredMixin, MessageMixin, CreateView):
    model = XPSpendingRequest
    form_class = XPSpendingRequestForm
    template_name = "game/xp_spending_request/form.html"
    success_message = "XP spending request submitted successfully!"
    error_message = "Failed to submit XP spending request. Please correct the errors below."

    # URL-based character ownership check
    owner_check_model = CharacterModel
    owner_check_kwarg = "character_pk"
    owner_check_attr = "character"
    owner_check_message = "You can only submit requests for your own characters."

    def dispatch(self, request, *args, **kwargs):
        character = get_object_or_404(CharacterModel, pk=kwargs["character_pk"])
        if not PermissionManager.user_has_permission(
            request.user, character, Permission.SPEND_XP, request=request
        ):
            raise PermissionDenied("XP spending is unavailable for this character")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = self.character  # Set by OwnerRequiredMixin
        return kwargs

    def get_success_url(self):
        return reverse("game:xp_spending_request:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = self.character  # Set by OwnerRequiredMixin
        return context


class XPSpendingRequestUpdateView(CharacterOwnerOrSTMixin, MessageMixin, UpdateView):
    model = XPSpendingRequest
    form_class = XPSpendingRequestForm
    template_name = "game/xp_spending_request/form.html"
    success_message = "XP spending request updated successfully!"
    error_message = "Failed to update XP spending request. Please correct the errors below."

    def dispatch(self, request, *args, **kwargs):
        record = self.get_object()
        if not PermissionManager.user_has_permission(
            request.user, record.character, Permission.SPEND_XP, request=request
        ):
            raise PermissionDenied("XP spending is unavailable for this character")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset().select_related("character")
        # Only allow editing pending requests
        return qs.filter(approved="Pending")

    def get_success_url(self):
        return reverse("game:xp_spending_request:detail", kwargs={"pk": self.object.pk})


class XPSpendingRequestApproveView(View):
    """View for STs to approve/deny XP spending requests."""

    def post(self, request, *args, **kwargs):
        value = request.POST.get("approved")
        if value not in {"Approved", "Denied"}:
            return HttpResponseBadRequest("Invalid approval decision")
        xp_request = get_object_or_404(XPSpendingRequest, pk=kwargs["pk"])
        try:
            result = decide_spending_request(
                XPSpendingRequest,
                xp_request.character,
                xp_request.pk,
                request.user,
                "approve" if value == "Approved" else "deny",
            )
        except SpendingDecisionError as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, result.message)
        return redirect("game:xp_spending_request:list")


# FreebieSpendingRecord Views
class FreebieSpendingRecordListView(LoginRequiredMixin, ListView):
    model = FreebieSpendingRecord
    template_name = "game/freebie_spending_record/list.html"
    ordering = ["-created_at"]
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset().select_related("character", "character__owner")
        return filter_private_records(qs, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prepare_permission_objects(self.request, list(context["object_list"]))
        context["show_owner_column"] = _has_st_read_rows(self.request, context["object_list"])
        return context


class FreebieSpendingRecordDetailView(CharacterOwnerOrSTMixin, DetailView):
    model = FreebieSpendingRecord
    template_name = "game/freebie_spending_record/detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("character", "character__owner")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_perms"] = get_object_permissions(self.request, self.object.character)
        context["is_owner"] = self.object.character.owner == self.request.user
        return context


class FreebieSpendingRecordCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = FreebieSpendingRecord
    form_class = FreebieSpendingRecordForm
    template_name = "game/freebie_spending_record/form.html"
    success_message = "Freebie spending record created successfully!"
    error_message = "Failed to create freebie spending record. Please correct the errors below."

    def dispatch(self, request, *args, **kwargs):
        """Require a pending-spend authority before showing the form."""
        character = get_object_or_404(CharacterModel, pk=kwargs["character_pk"])
        if not PermissionManager.user_has_permission(
            request.user, character, Permission.SPEND_FREEBIES, request=request
        ):
            raise PermissionDenied("Freebie spending is unavailable for this character")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = get_object_or_404(CharacterModel, pk=self.kwargs["character_pk"])
        return kwargs

    def get_success_url(self):
        return reverse("game:freebie_spending_record:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = get_object_or_404(CharacterModel, pk=self.kwargs["character_pk"])
        return context


class FreebieSpendingRecordUpdateView(CharacterOwnerOrSTMixin, MessageMixin, UpdateView):
    model = FreebieSpendingRecord
    form_class = FreebieSpendingRecordForm
    template_name = "game/freebie_spending_record/form.html"
    success_message = "Freebie spending record updated successfully!"
    error_message = "Failed to update freebie spending record. Please correct the errors below."

    def dispatch(self, request, *args, **kwargs):
        record = self.get_object()
        if not PermissionManager.user_has_permission(
            request.user, record.character, Permission.SPEND_FREEBIES, request=request
        ):
            raise PermissionDenied("Freebie spending is unavailable for this character")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().select_related("character").filter(approved="Pending")

    def get_success_url(self):
        return reverse("game:freebie_spending_record:detail", kwargs={"pk": self.object.pk})


# StoryXPRequest Create/Update Views
class StoryXPRequestCreateView(StorytellerRequiredMixin, MessageMixin, CreateView):
    model = StoryXPRequest
    form_class = StoryXPRequestForm
    template_name = "game/story_xp_request/form.html"
    success_message = "Story XP request created successfully!"
    error_message = "Failed to create story XP request. Please correct the errors below."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = get_object_or_404(CharacterModel, pk=self.kwargs["character_pk"])
        return kwargs

    def get_success_url(self):
        return reverse("game:story_xp_request:detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = get_object_or_404(CharacterModel, pk=self.kwargs["character_pk"])
        return context


class StoryXPRequestUpdateView(StorytellerRequiredMixin, MessageMixin, UpdateView):
    model = StoryXPRequest
    form_class = StoryXPRequestForm
    template_name = "game/story_xp_request/form.html"
    success_message = "Story XP request updated successfully!"
    error_message = "Failed to update story XP request. Please correct the errors below."

    def get_queryset(self):
        return super().get_queryset().select_related("character", "story")

    def get_success_url(self):
        return reverse("game:story_xp_request:detail", kwargs={"pk": self.object.pk})


# Chronicle Create/Update Views
class ChronicleCreateView(StorytellerRequiredMixin, MessageMixin, CreateView):
    model = Chronicle
    form_class = ChronicleForm
    template_name = "game/chronicle/form.html"
    success_message = "Chronicle '{name}' created successfully!"
    error_message = "Failed to create chronicle. Please correct the errors below."

    def get_success_url(self):
        return reverse("game:chronicle", kwargs={"pk": self.object.pk})


class ChronicleUpdateView(StorytellerRequiredMixin, MessageMixin, UpdateView):
    model = Chronicle
    form_class = ChronicleForm
    template_name = "game/chronicle/form.html"
    success_message = "Chronicle '{name}' updated successfully!"
    error_message = "Failed to update chronicle. Please correct the errors below."

    def get_success_url(self):
        return reverse("game:chronicle", kwargs={"pk": self.object.pk})


# Scene Create/Update Views
class SceneCreateView(StorytellerRequiredMixin, MessageMixin, CreateView):
    model = Scene
    form_class = SceneForm
    template_name = "game/scene/form.html"
    success_message = "Scene created successfully!"
    error_message = "Failed to create scene. Please correct the errors below."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if "chronicle_pk" in self.kwargs:
            kwargs["chronicle"] = get_object_or_404(Chronicle, pk=self.kwargs["chronicle_pk"])
        return kwargs

    def form_valid(self, form):
        # Set chronicle from URL if provided
        if "chronicle_pk" in self.kwargs:
            form.instance.chronicle = get_object_or_404(Chronicle, pk=self.kwargs["chronicle_pk"])
        if not PermissionManager.can_manage_scope(
            self.request.user,
            form.instance.chronicle,
            form.cleaned_data["gameline"],
            self.request,
        ):
            raise PermissionDenied("Matching chronicle ST required")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("game:scene", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "chronicle_pk" in self.kwargs:
            context["chronicle"] = get_object_or_404(Chronicle, pk=self.kwargs["chronicle_pk"])
        return context


class SceneUpdateView(StorytellerRequiredMixin, MessageMixin, UpdateView):
    model = Scene
    form_class = SceneForm
    template_name = "game/scene/form.html"
    success_message = "Scene updated successfully!"
    error_message = "Failed to update scene. Please correct the errors below."

    def get_queryset(self):
        return super().get_queryset().select_related("chronicle", "location")

    def form_valid(self, form):
        if not PermissionManager.can_manage_scope(
            self.request.user,
            form.instance.chronicle,
            form.cleaned_data["gameline"],
            self.request,
        ):
            raise PermissionDenied("Matching chronicle ST required")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("game:scene", kwargs={"pk": self.object.pk})

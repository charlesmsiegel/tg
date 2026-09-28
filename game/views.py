from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Max, Q, Sum
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from characters.models.core import CharacterModel
from core.htmx import is_fragment_request, mark_fragment, vary_on_htmx
from core.models import HouseRule
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
from game import scene_chat, xp_spend
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
    StoryEditForm,
    StoryForm,
    StoryXPRequestForm,
    STResponseForm,
    WeeklyXPRequestForm,
    XPSpendingRequestApprovalForm,
    XPSpendingRequestForm,
    xp_spend_form_class,
)
from game.models import (
    Chronicle,
    FreebieSpendingRecord,
    Journal,
    Scene,
    SettingElement,
    STRelationship,
    Story,
    StoryXPRequest,
    UserSceneReadStatus,
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
from game.selectors import (
    annotate_week_scene_counts,
    chronicle_overview,
    scene_cast,
    scene_post_window,
    scene_read_marker,
    unread_divider,
)
from game.spending_approval import (
    SpendingDecisionError,
    decide_spending_request,
    require_spending_approver,
)
from game.text import straighten_quotes


def _has_st_read_rows(request, rows):
    """A presentation flag for the prepared page, never approval authority."""
    if request.user.is_staff or request.user.is_superuser:
        return True
    return any(get_object_permissions(request, row).is_chronicle_st for row in rows)


def can_create_scene(user, chronicle, request=None):
    """Chronicle managers and the chronicle's STs may open scenes from the chronicle page."""
    return PermissionManager.can_manage_chronicle(user, chronicle, request) or (
        STRelationship.objects.filter(user=user, chronicle=chronicle).exists()
    )


def current_week(today=None):
    """The Week whose span (``start_date`` through ``end_date``, inclusive) holds today."""
    today = today or timezone.localdate()
    return (
        Week.objects.filter(end_date__gte=today, end_date__lte=today + timedelta(days=7))
        .order_by("end_date")
        .first()
    )


def _line_key(groups, requested):
    """The game-line sub-tab to show: the requested one when it has rows, else the first."""
    if requested in groups:
        return requested
    return next(iter(groups), None)


class CharacterContextMixin:
    """Put the record's character, as its concrete class, in the context as ``character``.

    Journals and XP / freebie records reach their character through a plain foreign key,
    which yields the base CharacterModel; the concrete class carries the gameline the
    page's Spread cover is drawn in.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = getattr(self.object, "character", None)
        context["character"] = character.get_real_instance() if character else None
        return context


class ChronicleDetailView(LoginRequiredMixin, DetailView):
    """View for displaying chronicle details. Requires authentication.

    The page is tabbed by querystring (Spread M1): ``?tab=`` picks overview,
    characters, scenes, locations, items, common-knowledge or stories; ``status=``
    and ``line=`` pick the sub-tabs inside a tab, and ``new=scene|story`` opens that
    creation form. A creation action that fails re-renders this page with its bound
    form, and the form's tab opens with it.
    """

    model = Chronicle
    template_name = "game/chronicle/detail.html"
    TABS = ("overview", "characters", "scenes", "locations", "items", "common-knowledge", "stories")
    CHARACTER_STATUSES = ("active", "retired", "deceased", "npc")
    SCENE_STATUSES = ("all", "active", "completed")

    def get_queryset(self):
        return super().get_queryset().prefetch_related("storytellers", "allowed_objects")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chronicle = self.object
        user = self.request.user
        context["can_manage_chronicle"] = PermissionManager.can_manage_chronicle(
            user, chronicle, self.request
        )
        context["can_create_scene"] = can_create_scene(user, chronicle, self.request)

        context.update(chronicle_overview(chronicle, user))
        # A creation action re-renders this page with its bound form (Step 5).
        context.setdefault("form", SceneCreationForm(chronicle=chronicle, user=user))
        context.setdefault("story_form", StoryForm())
        context.update(
            {
                "header": chronicle.headings,
                # Creation forms for Characters, Locations, Items
                "char_form": ChronicleCharacterCreationForm(chronicle=chronicle, user=user),
                "loc_form": ChronicleLocationCreationForm(chronicle=chronicle, user=user),
                "item_form": ChronicleItemCreationForm(chronicle=chronicle, user=user),
            }
        )
        context.update(self.tab_context(context))
        return context

    def tab_context(self, context):
        """Which tab, sub-tabs and creation form the page shows, plus the cover facts."""
        query = self.request.GET
        chronicle = self.object
        scene_form, story_form = context["form"], context["story_form"]

        tab = query.get("tab")
        open_form = query.get("new")
        if scene_form.is_bound:
            tab, open_form = "scenes", "scene"
        elif story_form.is_bound:
            tab, open_form = "stories", "story"
        elif tab not in self.TABS:
            tab = "overview"

        status = query.get("status")
        character_status = status if status in self.CHARACTER_STATUSES else "active"
        scene_status = status if status in self.SCENE_STATUSES else "all"
        character_groups = context[f"{character_status}_by_gameline"]
        scene_groups = context[f"{scene_status}_scenes_by_gameline"]
        line = query.get("line")

        all_scenes = context["all_scenes_by_gameline"].get("wod")
        locations = context["locations_by_gameline"].get("wod")
        return {
            "tab": tab,
            "open_form": open_form,
            "character_status": character_status,
            "character_groups": character_groups,
            "character_line": _line_key(character_groups, line),
            "scene_status": scene_status,
            "scene_groups": scene_groups,
            "scene_line": _line_key(scene_groups, line),
            "location_line": _line_key(context["locations_by_gameline"], line),
            "item_line": _line_key(context["items_by_gameline"], line),
            "setting_line": _line_key(context["setting_elements_by_gameline"], line),
            "tab_counts": {
                "characters": context["character_list"].count(),
                "scenes": all_scenes["scenes"].count() if all_scenes else 0,
                "locations": len(locations["locations"]) if locations else 0,
                "items": context["items"].count(),
            },
            "live_scenes": context["active_scenes"].select_related("location"),
            "stories": chronicle.stories.order_by("xp_given", "name"),
            # Stories from before stories had a chronicle: the chronicle's managers
            # (the audience of "New story") still see them here; staff can assign them.
            "unassigned_stories": (
                Story.objects.filter(chronicle__isnull=True).order_by("xp_given", "name")
                if context["can_manage_chronicle"]
                else Story.objects.none()
            ),
            "current_week": current_week(),
            "house_rule_count": HouseRule.objects.filter(chronicle=chronicle).count(),
        }


class SceneDetailView(DetailView):
    """A scene's posts and, for an open scene, the live chat (Step 11).

    ``?before=<post id>`` shows the window of posts before that one: as a full
    page without JavaScript, and as the ``scene-posts`` fragment for htmx's
    "Show earlier posts".
    """

    model = Scene
    template_name = "game/scene/detail.html"
    fragment_template_name = "game/scene/_post_window.html"

    def get_queryset(self):
        return super().get_queryset().select_related("location", "chronicle")

    def is_posts_fragment(self):
        return is_fragment_request(self.request) and self.post_cursor() is not None

    def render_to_response(self, context, **response_kwargs):
        response = vary_on_htmx(super().render_to_response(context, **response_kwargs))
        if self.is_posts_fragment():
            response.template_name = self.fragment_template_name  # rendered lazily
            mark_fragment(response, "scene-posts")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scene = self.object
        user = self.request.user

        before = self.post_cursor()
        context["posts"], has_earlier = scene_post_window(scene, before=before)
        context["earlier_cursor"] = context["posts"][0].pk if has_earlier else None
        context["showing_earlier"] = before is not None
        context["viewer_id"] = user.pk if user.is_authenticated else None
        if self.is_posts_fragment():
            return context

        # An older window is history: it has no live updates to append to it.
        context["live"] = not scene.finished and before is None
        context["cast"] = scene_cast(scene)
        context["component_scripts"] = ("game/js/scene-chat.js",)
        if user.is_authenticated and before is None:
            context["unread"] = self.read_latest(
                user, context["posts"], has_earlier, context["cast"]
            )
        if user.is_authenticated and not scene.finished:
            context["post_characters"] = list(PostForm(user=user, scene=scene).character_queryset)
            context["add_characters"] = list(
                AddCharForm(user=user, scene=scene).fields["character_to_add"].queryset
            )
        return context

    def read_latest(self, user, posts, has_earlier, cast):
        """The unread divider for ``user``, who has now read up to the latest post.

        A player of the scene (``cast``) without a status row gets one here, so
        their divider works from their first visit on; other readers are not
        tracked. Writes only when the status changes.
        """
        scene = self.object
        tracked, read, marker = scene_read_marker(scene, user)
        divider = unread_divider(scene, posts, read=read, marker=marker, has_earlier=has_earlier)
        latest = posts[-1] if posts else None
        if tracked:
            if not read or (latest is not None and marker != latest.pk):
                UserSceneReadStatus.objects.mark_read(scene, user.pk, latest)
        elif any(character.owner_id == user.pk for character in cast):
            UserSceneReadStatus.objects.create(
                scene=scene, user=user, read=True, last_read_post=latest
            )
        return divider

    def post_cursor(self):
        """``?before=<post id>`` pages back through a long scene; junk is ignored."""
        return scene_chat.post_cursor(self.request.GET.get("before", "")) or None

    straighten_quotes = staticmethod(straighten_quotes)


class CommandsView(LoginRequiredMixin, TemplateView):
    template_name = "game/scene/commands.html"


class JournalDetailView(SpecialUserMixin, ViewPermissionMixin, CharacterContextMixin, DetailView):
    model = Journal
    template_name = "game/journal/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_entry_form"] = JournalEntryForm(instance=self.object)
        context["st_response_forms"] = [
            STResponseForm(entry=e, prefix=f"entry-{e.pk}") for e in self.object.all_entries()
        ]
        return context


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


def readable_chronicle_ids(user, chronicles):
    """The ids among ``chronicles`` that ``user`` may open (one query)."""
    ids = {chronicle.pk for chronicle in chronicles if chronicle is not None}
    if not ids:
        return set()
    return set(readable_chronicles(user).filter(pk__in=ids).values_list("pk", flat=True))


class StoryDetailView(LoginRequiredMixin, DetailView):
    model = Story
    template_name = "game/story/detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("chronicle")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The chronicle is named only to viewers who can open it.
        chronicle = self.object.chronicle
        context["story_chronicle"] = (
            chronicle
            if chronicle and readable_chronicle_ids(self.request.user, [chronicle])
            else None
        )
        return context


class StoryListView(LoginRequiredMixin, ListView):
    model = Story
    ordering = ["name"]
    template_name = "game/story/list.html"

    def get_queryset(self):
        return super().get_queryset().select_related("chronicle")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stories = list(context["object_list"])
        readable = readable_chronicle_ids(self.request.user, [s.chronicle for s in stories])
        for story in stories:
            story.visible_chronicle = story.chronicle if story.chronicle_id in readable else None
        context["object_list"] = stories
        return context


class StoryStaffRequiredMixin:
    """Stories are created and edited outside a chronicle page by staff only.

    StorytellerRequiredMixin would read the story's new ``chronicle`` and admit that
    chronicle's STs; this keeps the rule stories have always had. Chronicle managers
    create their stories from the chronicle page (game.actions.ChronicleStoryCreateView).
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Login required")
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Staff required")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("game:story:detail", kwargs={"pk": self.object.pk})


class StoryCreateView(StoryStaffRequiredMixin, MessageMixin, CreateView):
    model = Story
    form_class = StoryEditForm
    template_name = "game/story/form.html"
    success_message = "Story '{name}' created successfully!"
    error_message = "Failed to create story. Please correct the errors below."


class StoryUpdateView(StoryStaffRequiredMixin, MessageMixin, UpdateView):
    model = Story
    form_class = StoryEditForm
    template_name = "game/story/form.html"
    success_message = "Story '{name}' updated successfully!"
    error_message = "Failed to update story. Please correct the errors below."


# Week Views
class WeekListView(LoginRequiredMixin, ListView):
    model = Week
    ordering = ["-end_date"]
    template_name = "game/week/list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_manage_global_records"] = (
            self.request.user.is_staff or self.request.user.is_superuser
        )
        annotate_week_scene_counts(context["object_list"], self.request.user)
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

        # Week navigation on the cover
        end_date = self.object.end_date
        context["previous_week"] = (
            Week.objects.filter(end_date__lt=end_date).order_by("-end_date").first()
        )
        context["next_week"] = (
            Week.objects.filter(end_date__gt=end_date).order_by("end_date").first()
        )
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


class WeeklyXPRequestDetailView(CharacterOwnerOrSTMixin, CharacterContextMixin, DetailView):
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

        # player_save() only prepares the instance; ModelFormMixin saves it once.
        form.player_save(commit=False)
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


class StoryXPRequestDetailView(CharacterOwnerOrSTMixin, CharacterContextMixin, DetailView):
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


class XPSpendingRequestDetailView(CharacterOwnerOrSTMixin, CharacterContextMixin, DetailView):
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


class XPSpendingRequestCreateView(LoginRequiredMixin, OwnerRequiredMixin, FormView):
    """Spend XP (Spread M8): trait type → trait → preview, then the spend request.

    The selects re-ask this URL by GET (htmx, ``xp-spend`` fragment) for the next
    select's options and the preview; without JavaScript the "Preview" button posts
    the selection back. A spend goes through the character's XP service, as the sheet's
    own XP form does: the XP is deducted now and refunded if the Storyteller denies it.
    """

    template_name = "game/xp_spending_request/form.html"
    fragment_template_name = "game/xp_spending_request/_spend_fields.html"
    SELECTION = ("category", "example", "value", "note")

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

    def get_form_class(self):
        return xp_spend_form_class(self.character)  # Set by OwnerRequiredMixin

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop("files", None)
        kwargs["character"] = self.character
        if self.request.method == "GET" and any(key in self.request.GET for key in self.SELECTION):
            kwargs["data"] = self.request.GET
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.enable_htmx(self.request.path)
        return form

    def get(self, request, *args, **kwargs):
        return self.show_preview(self.get_form())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if request.POST.get("preview"):
            return self.show_preview(form)
        if not form.is_valid():
            return self.form_invalid(form)
        result = xp_spend.spend(self.character, form.cleaned_data)
        if not result.success:
            form.add_error(None, result.error)
            return self.form_invalid(form)
        messages.success(
            request, f"Requested {result.trait} for {result.cost} XP. A Storyteller will review it."
        )
        return redirect(request.path)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to submit XP spending request.")
        return self.render_page(form, preview=None)

    def show_preview(self, form):
        """The selection's preview; an unfinished selection shows no errors yet."""
        preview = None
        if form.is_bound:
            if form.is_valid():
                preview = xp_spend.preview(self.character, form.cleaned_data)
            form.quiet()
        return self.render_page(form, preview)

    def render_page(self, form, preview):
        context = self.get_context_data(form=form, preview=preview)
        if is_fragment_request(self.request):
            response = self.response_class(
                request=self.request, template=[self.fragment_template_name], context=context
            )
            return vary_on_htmx(mark_fragment(response, "xp-spend"))
        return vary_on_htmx(self.render_to_response(context))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = self.character
        totals = character.xp_spendings.aggregate(
            spent=Sum("cost", filter=Q(approved="Approved")),
            pending=Sum("cost", filter=Q(approved="Pending")),
        )
        context.update(
            character=character,
            spent_xp=totals["spent"] or 0,
            pending_xp=totals["pending"] or 0,
            component_scripts=("game/js/xp-spend.js",),
        )
        return context


class XPSpendingRequestUpdateView(
    CharacterOwnerOrSTMixin, MessageMixin, CharacterContextMixin, UpdateView
):
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


class FreebieSpendingRecordDetailView(CharacterOwnerOrSTMixin, CharacterContextMixin, DetailView):
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


class FreebieSpendingRecordUpdateView(
    CharacterOwnerOrSTMixin, MessageMixin, CharacterContextMixin, UpdateView
):
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


class StoryXPRequestUpdateView(
    StorytellerRequiredMixin, MessageMixin, CharacterContextMixin, UpdateView
):
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

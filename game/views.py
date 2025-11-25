import itertools

from characters.models.core import CharacterModel
from characters.models.core.character import Character
from core.mixins import (
    CharacterOwnerOrSTMixin,
    EditPermissionMixin,
    MessageMixin,
    StorytellerRequiredMixin,
    ViewPermissionMixin,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
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

    def get_queryset(self):
        return super().get_queryset().prefetch_related('storytellers', 'allowed_objects')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chronicle = self.object

        top_locations = (
            LocationModel.objects.top_level()
            .filter(chronicle=chronicle)
            .order_by("name")
        )
        characters = (
            Character.objects.active().player_characters().with_group_ordering()
        )

        context.update({
            "character_list": characters.filter(chronicle=chronicle),
            "items": ItemModel.objects.for_chronicle(chronicle).order_by("name"),
            "form": SceneCreationForm(chronicle=chronicle),
            "top_locations": top_locations,
            "active_scenes": Scene.objects.active_for_chronicle(chronicle),
            "story_form": StoryForm(),
            "header": chronicle.headings,
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        chronicle = self.object

        # Check if user is a storyteller for this chronicle
        if not request.user.profile.is_st():
            messages.error(request, "Only storytellers can create stories and scenes.")
            raise PermissionDenied("Only storytellers can create stories and scenes")

        create_story_flag = request.POST.get("create_story")
        create_scene_flag = request.POST.get("create_scene")
        if create_story_flag is not None:
            story = Story.objects.create(name=request.POST["name"])
            messages.success(request, f"Story '{story.name}' created successfully!")
        if create_scene_flag is not None:
            location = get_object_or_404(LocationModel, pk=request.POST["location"])
            scene = chronicle.add_scene(
                request.POST["name"],
                location,
                date_of_scene=request.POST["date_of_scene"],
            )
            messages.success(
                request, f"Scene '{request.POST['name']}' created successfully!"
            )
            return redirect(scene)
        return self.render_to_response(self.get_context_data())


class SceneDetailView(LoginRequiredMixin, DetailView):
    """View for displaying scene details. Requires authentication."""

    model = Scene
    template_name = "game/scene/detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related('location', 'chronicle')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scene = self.object
        user = self.request.user

        context["posts"] = Post.objects.for_scene_optimized(scene)

        if user.is_authenticated:
            add_char_form = AddCharForm(user=user, scene=scene)
            context.update({
                "add_char_form": add_char_form,
                "num_chars": add_char_form.fields["character_to_add"].queryset.count(),
                "num_logged_in_chars": scene.characters.owned_by(user).count(),
                "first_char": scene.characters.owned_by(user).first(),
                "post_form": PostForm(user=user, scene=scene),
            })

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        scene = self.object

        if "close_scene" in request.POST.keys():
            # Only storytellers can close scenes
            if not request.user.profile.is_st():
                messages.error(request, "Only storytellers can close scenes.")
                raise PermissionDenied("Only storytellers can close scenes")
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
                    character = get_object_or_404(
                        CharacterModel, pk=request.POST["character"]
                    )
                # Check that user owns the character
                if character.owner != request.user:
                    messages.error(request, "You can only post as your own characters.")
                    raise PermissionDenied("You can only post as your own characters")
                try:
                    message = self.straighten_quotes(request.POST["message"])
                    scene.add_post(character, request.POST["display_name"], message)
                    messages.success(request, "Post added successfully!")
                except ValueError:
                    messages.error(
                        request, "Command does not match the expected format."
                    )
            else:
                messages.error(
                    request, "Failed to create post. Please check your input."
                )
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


class ChronicleScenesDetailView(LoginRequiredMixin, DetailView):
    """View for displaying chronicle scenes. Requires authentication."""

    model = Chronicle
    template_name = "game/scenes/detail.html"
    context_object_name = "chronicle"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chronicle = self.object

        scenes = Scene.objects.for_chronicle(chronicle).with_location()

        # Group scenes by year and month
        scenes_grouped = [
            (datetime(year=year, month=month, day=1), list(scenes_in_month))
            for (year, month), scenes_in_month in itertools.groupby(
                scenes, key=lambda x: (x.date_of_scene.year, x.date_of_scene.month)
            )
        ]

        context["scenes_grouped"] = scenes_grouped
        return context


class CommandsView(LoginRequiredMixin, TemplateView):
    template_name = "game/scene/commands.html"


class JournalDetailView(ViewPermissionMixin, DetailView):
    model = Journal
    template_name = "game/journal/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_entry_form"] = JournalEntryForm(instance=self.object)
        context["st_response_forms"] = [
            STResponseForm(entry=e, prefix=f"entry-{e.pk}")
            for e in self.object.all_entries()
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
                messages.error(
                    request, "Failed to add journal entry. Please check your input."
                )
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
                messages.error(
                    request, "Failed to add ST response. Please check your input."
                )
        return render(
            request, "game/journal/detail.html", self.get_context_data(**kwargs)
        )


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
        context["xp_requests"] = WeeklyXPRequest.objects.filter(
            week=self.object
        ).select_related("character")

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
            context["pending_count"] = WeeklyXPRequest.objects.filter(
                approved=False
            ).count()
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
            messages.error(
                request, "You can only submit requests for your own characters."
            )
            raise PermissionDenied(
                "You can only submit requests for your own characters"
            )

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = get_object_or_404(
            CharacterModel, pk=self.kwargs["character_pk"]
        )
        kwargs["week"] = get_object_or_404(Week, pk=self.kwargs["week_pk"])
        return kwargs

    def form_valid(self, form):
        # Check if request already exists
        if WeeklyXPRequest.objects.filter(
            character=form.character, week=form.week
        ).exists():
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
        context["character"] = get_object_or_404(
            CharacterModel, pk=self.kwargs["character_pk"]
        )
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
            messages.error(
                request, "Failed to approve XP request. Please check the form."
            )
            return redirect("game:weekly_xp_request:detail", pk=xp_request.pk)


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
        context["chronicles"] = Chronicle.objects.filter(
            common_knowledge_elements=self.object
        )
        return context


class SettingElementCreateView(StorytellerRequiredMixin, MessageMixin, CreateView):
    model = SettingElement
    fields = ["name", "description"]
    template_name = "game/setting_element/form.html"
    success_message = "Setting element '{name}' created successfully!"
    error_message = "Failed to create setting element. Please correct the errors below."

    def get_success_url(self):
        return reverse("game:setting_element:detail", kwargs={"pk": self.object.pk})


class SettingElementUpdateView(StorytellerRequiredMixin, MessageMixin, UpdateView):
    model = SettingElement
    fields = ["name", "description"]
    template_name = "game/setting_element/form.html"
    success_message = "Setting element '{name}' updated successfully!"
    error_message = "Failed to update setting element. Please correct the errors below."

    def get_success_url(self):
        return reverse("game:setting_element:detail", kwargs={"pk": self.object.pk})

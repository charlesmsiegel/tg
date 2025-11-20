import itertools

from characters.models.core import CharacterModel
from characters.models.core.character import Character
from core.views.approved_user_mixin import SpecialUserMixin
from core.views.message_mixin import MessageMixin
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
)
from game.models import Chronicle, Journal, JournalEntry, Post, Scene, Story
from items.models.core import ItemModel
from locations.models.core import LocationModel


class StorytellerRequiredMixin(UserPassesTestMixin):
    """Mixin that requires the user to be a storyteller."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.is_st()


class ChronicleDetailView(LoginRequiredMixin, View):
    """View for displaying chronicle details. Requires authentication."""

    def get_context(self, pk):
        chronicle = get_object_or_404(Chronicle, pk=pk)
        top_locations = LocationModel.objects.filter(
            chronicle=chronicle, parent=None
        ).order_by("name")
        CharacterGroup = Character.group_set.through

        # Subquery to get the first group id for each character
        first_group_id = Subquery(
            CharacterGroup.objects.filter(character_id=OuterRef("pk"))
            .order_by(
                "group_id"
            )  # Assuming ordering by 'group_id', adjust if different
            .values("group_id")[:1]
        )

        # Annotating the queryset with the first group id
        characters = (
            Character.objects.exclude(status__in=["Dec", "Ret"])
            .exclude(npc=True)
            .annotate(first_group_id=first_group_id)
            .select_related("chronicle")
            .order_by("chronicle__id", "-first_group_id", "name")
        )

        return {
            "object": chronicle,
            "character_list": characters.filter(chronicle=chronicle),
            "items": ItemModel.objects.filter(chronicle=chronicle).order_by("name"),
            "form": SceneCreationForm(chronicle=chronicle),
            "top_locations": top_locations,
            "active_scenes": Scene.objects.filter(chronicle=chronicle, finished=False),
            "story_form": StoryForm(),
            "header": chronicle.headings,
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context(kwargs["pk"])
        return render(request, "game/chronicle/detail.html", context)

    def post(self, request, *args, **kwargs):
        context = self.get_context(kwargs["pk"])
        chronicle = context["object"]

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
            messages.success(request, f"Scene '{request.POST['name']}' created successfully!")
            return redirect(scene)
        return render(request, "game/chronicle/detail.html", context)


class SceneDetailView(LoginRequiredMixin, View):
    """View for displaying scene details. Requires authentication."""

    def get_context(self, pk, user):
        scene = get_object_or_404(Scene, pk=pk)
        if user is not None and user.is_authenticated:
            a = AddCharForm(user=user, scene=scene)
            num_chars = (a.fields["character_to_add"].queryset).count()
            return {
                "object": scene,
                "posts": Post.objects.filter(scene=scene).select_related("character"),
                "add_char_form": a,
                "num_chars": num_chars,
                "num_logged_in_chars": scene.characters.filter(owner=user).count(),
                "first_char": scene.characters.filter(owner=user).first(),
                "post_form": PostForm,
            }
        return {
            "object": scene,
            "posts": Post.objects.filter(scene=scene).select_related("character"),
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context(kwargs["pk"], request.user)
        if request.user.is_authenticated:
            context["post_form"] = context["post_form"](
                user=request.user, scene=context["object"]
            )
        return render(request, "game/scene/detail.html", context)

    def post(self, request, *args, **kwargs):
        context = self.get_context(kwargs["pk"], request.user)
        scene = context["object"]

        if "close_scene" in request.POST.keys():
            # Only storytellers can close scenes
            if not request.user.profile.is_st():
                messages.error(request, "Only storytellers can close scenes.")
                raise PermissionDenied("Only storytellers can close scenes")
            context["post_form"] = context["post_form"](user=request.user, scene=scene)
            scene.close()
            messages.success(request, f"Scene '{scene.name}' closed successfully!")
        elif "character_to_add" in request.POST.keys():
            c = get_object_or_404(CharacterModel, pk=request.POST["character_to_add"])
            # Check that user owns the character
            if c.owner != request.user:
                messages.error(request, "You can only add your own characters.")
                raise PermissionDenied("You can only add your own characters")
            context["post_form"] = context["post_form"](user=request.user, scene=scene)
            scene.add_character(c)
            messages.success(request, f"Character '{c.name}' added to scene!")
        elif "message" in request.POST.keys():
            context["post_form"] = context["post_form"](
                request.POST, user=request.user, scene=scene
            )
            if context["post_form"].is_valid():
                if context["num_logged_in_chars"] == 1:
                    character = context["first_char"]
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
                    context["post_form"] = PostForm(user=request.user, scene=scene)
                except ValueError:
                    context["post_form"].add_error(
                        None, "Command does not match the expected format."
                    )
                    messages.error(request, "Command does not match the expected format.")
            else:
                messages.error(request, "Failed to create post. Please check your input.")
        context = self.get_context(kwargs["pk"], request.user)
        context["post_form"] = context["post_form"](
            user=request.user, scene=context["object"]
        )
        return redirect(reverse("game:scene", kwargs={"pk": context["object"].pk}))

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


class ChronicleScenesDetailView(LoginRequiredMixin, View):
    """View for displaying chronicle scenes. Requires authentication."""

    def get(self, request, *args, **kwargs):
        chronicle = get_object_or_404(Chronicle, pk=kwargs["pk"])
        scenes = Scene.objects.filter(chronicle=chronicle).select_related("location")

        # Group scenes by year and month
        scenes_grouped = [
            (datetime(year=year, month=month, day=1), list(scenes_in_month))
            for (year, month), scenes_in_month in itertools.groupby(
                scenes, key=lambda x: (x.date_of_scene.year, x.date_of_scene.month)
            )
        ]

        context = {
            "chronicle": chronicle,
            "scenes_grouped": scenes_grouped,
        }
        return render(request, "game/scenes/detail.html", context)


class CommandsView(TemplateView):
    template_name = "game/scene/commands.html"


class JournalDetailView(SpecialUserMixin, DetailView):
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
            f = JournalEntryForm(request.POST, instance=self.object)
            if f.is_valid():
                f.save()
                messages.success(request, "Journal entry added successfully!")
            else:
                messages.error(request, "Failed to add journal entry. Please check your input.")
        if submit_response is not None:
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
        return render(
            request, "game/journal/detail.html", self.get_context_data(**kwargs)
        )


class ChronicleListView(ListView):
    model = Chronicle
    ordering = ["name"]
    template_name = "game/chronicle/list.html"


class SceneListView(ListView):
    model = Scene
    ordering = ["-date_of_scene", "-date_played"]
    template_name = "game/scene/list.html"


class JournalListView(ListView):
    model = Journal
    ordering = ["character__name"]
    template_name = "game/journal/list.html"


class StoryDetailView(DetailView):
    model = Story
    template_name = "game/story/detail.html"


class StoryListView(ListView):
    model = Story
    ordering = ["name"]
    template_name = "game/story/list.html"


class StoryCreateView(MessageMixin, CreateView):
    model = Story
    fields = ["name"]
    template_name = "game/story/form.html"
    success_message = "Story '{name}' created successfully!"
    error_message = "Failed to create story. Please correct the errors below."

    def get_success_url(self):
        return reverse("game:story:detail", kwargs={"pk": self.object.pk})


class StoryUpdateView(MessageMixin, UpdateView):
    model = Story
    fields = ["name"]
    template_name = "game/story/form.html"
    success_message = "Story '{name}' updated successfully!"
    error_message = "Failed to update story. Please correct the errors below."

    def get_success_url(self):
        return reverse("game:story:detail", kwargs={"pk": self.object.pk})

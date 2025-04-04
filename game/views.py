import itertools

from characters.models.core import CharacterModel
from characters.models.core.character import Character
from core.views.approved_user_mixin import SpecialUserMixin
from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.timezone import datetime
from django.views import View
from django.views.generic import DetailView, TemplateView
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


class ChronicleDetailView(View):
    def get_context(self, pk):
        chronicle = Chronicle.objects.get(pk=pk)
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
        create_story_flag = request.POST.get("create_story")
        create_scene_flag = request.POST.get("create_scene")
        if create_story_flag is not None:
            Story.objects.create(name=request.POST["name"])
        if create_scene_flag is not None:
            return redirect(
                context["object"].add_scene(
                    request.POST["name"],
                    LocationModel.objects.get(pk=request.POST["location"]),
                    date_of_scene=request.POST["date_of_scene"],
                )
            )
        return render(request, "game/chronicle/detail.html", context)


class SceneDetailView(View):
    def get_context(self, pk, user):
        if not user.is_authenticated:
            user = None
        scene = Scene.objects.get(pk=pk)
        if user is not None:
            a = AddCharForm(user=user, scene=scene)
            num_chars = (a.fields["character_to_add"].queryset).count()
            return {
                "object": scene,
                "posts": Post.objects.filter(scene=scene),
                "add_char_form": a,
                "num_chars": num_chars,
                "num_logged_in_chars": scene.characters.filter(owner=user).count(),
                "first_char": scene.characters.filter(owner=user).first(),
                "post_form": PostForm,
            }
        return {
            "object": scene,
            "posts": Post.objects.filter(scene=scene),
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
        if "close_scene" in request.POST.keys():
            context["post_form"] = context["post_form"](
                user=request.user, scene=context["object"]
            )
            context["object"].close()
        elif "character_to_add" in request.POST.keys():
            c = CharacterModel.objects.get(pk=request.POST["character_to_add"])
            context["post_form"] = context["post_form"](
                user=request.user, scene=context["object"]
            )
            context["object"].add_character(c)
        elif "message" in request.POST.keys():
            context["post_form"] = context["post_form"](
                request.POST, user=request.user, scene=context["object"]
            )
            if context["post_form"].is_valid():
                if context["num_logged_in_chars"] == 1:
                    character = context["first_char"]
                else:
                    character = CharacterModel.objects.get(pk=request.POST["character"])
                try:
                    message = self.straighten_quotes(request.POST["message"])
                    context["object"].add_post(
                        character, request.POST["display_name"], message
                    )
                    context["post_form"] = PostForm(
                        user=request.user, scene=context["object"]
                    )
                except ValueError:
                    context["post_form"].add_error(
                        None, "Command does not match the expected format."
                    )
        context = self.get_context(kwargs["pk"], request.user)
        context["post_form"] = context["post_form"](
            user=request.user, scene=context["object"]
        )
        # return render(request, "game/scene/detail.html", context)
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


class ChronicleScenesDetailView(View):
    def get(self, request, *args, **kwargs):
        chronicle = get_object_or_404(Chronicle, pk=kwargs["pk"])
        scenes = Scene.objects.filter(chronicle=chronicle)

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
        if submit_response is not None:
            tmp = [x for x in request.POST.keys() if "entry" in x][0]
            tmp = tmp.split("-")[1]
            f = STResponseForm(
                {"st_message": request.POST[f"entry-{tmp}-st_message"]},
                entry=JournalEntry.objects.get(pk=tmp),
            )
            if f.is_valid():
                f.save()
        return render(
            request, "game/journal/detail.html", self.get_context_data(**kwargs)
        )

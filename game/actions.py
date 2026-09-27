"""Scene, journal and chronicle actions: one URL, permission and call each."""

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect

from characters.services.result import ServiceResult
from core.actions import ActionFailed, ObjectActionView
from core.permissions import Permission, PermissionManager
from game.forms import (
    AddCharForm,
    JournalEntryForm,
    PostForm,
    SceneCreationForm,
    StoryForm,
    STResponseForm,
)
from game.models import Chronicle, Journal, JournalEntry, Scene, STRelationship
from game.security import can_read_private_record, can_view_scene, readable_chronicles
from game.text import straighten_quotes
from game.views import ChronicleDetailView

# Scenes -------------------------------------------------------------------


class SceneActionView(ObjectActionView):
    """A scene the user can read; restricted scenes are 404 like missing ones."""

    model = Scene

    def get_queryset(self):
        return Scene.objects.select_related("chronicle", "location")

    def can_see(self, subject):
        return can_view_scene(self.request.user, subject)

    def has_permission(self, subject):
        # Finished scenes are read-only for every action except closing.
        return not subject.finished


class SceneCloseView(SceneActionView):
    lock = True

    def has_permission(self, subject):
        return PermissionManager.can_manage_scope(
            self.request.user, subject.chronicle, subject.gameline, self.request
        )

    def perform(self, form):
        if self.object.finished:
            raise ActionFailed(f"Scene '{self.object.name}' is already closed.")
        self.object.close()
        return ServiceResult.ok(f"Scene '{self.object.name}' closed successfully!")


class SceneAddCharacterView(SceneActionView):
    """Enroll a character of this chronicle; players may enroll only their own."""

    form_class = AddCharForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop("files")
        kwargs.update(user=self.request.user, scene=self.object)
        return kwargs

    def perform(self, form):
        character = form.cleaned_data["character_to_add"]
        self.object.add_character(character)
        return ServiceResult.ok(f"Character '{character.name}' added to scene!")


class ScenePostView(SceneActionView):
    """Post as one of the user's characters in this scene (the chat's fallback)."""

    form_class = PostForm

    def has_permission(self, subject):
        return super().has_permission(subject) and (
            subject.characters.owned_by(self.request.user).exists()
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop("files")
        kwargs.update(user=self.request.user, scene=self.object)
        return kwargs

    def form_invalid(self, form):
        fragment = self.fragment_response(form=form)
        if fragment is not None:
            return fragment
        # The chat form shows one summary line, as it always has.
        messages.error(self.request, "Failed to create post. Please check your input.")
        return redirect(self.get_failure_url())

    def perform(self, form):
        # PostForm offers only the user's own characters in this scene.
        own = form.character_queryset
        character = own.first() if own.count() == 1 else form.cleaned_data["character"]
        message = straighten_quotes(form.cleaned_data["message"])
        try:
            self.object.add_post(character, form.cleaned_data["display_name"], message)
        except ValueError as exc:
            raise ActionFailed("Command does not match the expected format.") from exc
        return ServiceResult.ok("Post added successfully!")


# Journals -----------------------------------------------------------------


class JournalActionView(ObjectActionView):
    """Journals have no public card: unreadable ones are 404."""

    model = Journal

    def get_queryset(self):
        return Journal.objects.select_related("character")

    def can_see(self, subject):
        return can_read_private_record(self.request.user, subject)


class JournalEntryCreateView(JournalActionView):
    form_class = JournalEntryForm
    success_message = "Journal entry added successfully!"

    def has_permission(self, subject):
        return subject.character.owner_id == self.request.user.pk

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop("files")
        kwargs["instance"] = self.object
        return kwargs

    def perform(self, form):
        form.save()


class JournalResponseView(JournalActionView):
    """A scoped storyteller answers one entry of this journal."""

    form_class = STResponseForm
    success_message = "ST response added successfully!"

    def has_permission(self, subject):
        return PermissionManager.user_has_permission(
            self.request.user, subject.character, Permission.APPROVE, request=self.request
        )

    def get_form_kwargs(self):
        entry = get_object_or_404(JournalEntry, pk=self.kwargs["entry_pk"], journal=self.object)
        kwargs = super().get_form_kwargs()
        kwargs.pop("files")
        kwargs.update(entry=entry, prefix=f"entry-{entry.pk}")
        return kwargs

    def perform(self, form):
        form.save()


# Chronicles ---------------------------------------------------------------


class ChronicleActionView(ObjectActionView):
    model = Chronicle

    def can_see(self, subject):
        return readable_chronicles(self.request.user).filter(pk=subject.pk).exists()

    host_view_class = ChronicleDetailView


class ChronicleStoryCreateView(ChronicleActionView):
    form_class = StoryForm
    host_form_context_name = "story_form"

    def has_permission(self, subject):
        return PermissionManager.can_manage_chronicle(self.request.user, subject, self.request)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop("files")
        return kwargs

    def perform(self, form):
        story = form.save()
        return ServiceResult.ok(f"Story '{story.name}' created successfully!", obj=story)


class ChronicleSceneCreateView(ChronicleActionView):
    form_class = SceneCreationForm

    def has_permission(self, subject):
        user = self.request.user
        return PermissionManager.can_manage_chronicle(user, subject, self.request) or (
            STRelationship.objects.filter(user=user, chronicle=subject).exists()
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop("files")
        kwargs.update(chronicle=self.object, user=self.request.user)
        return kwargs

    def perform(self, form):
        gameline = form.cleaned_data["gameline"]
        if not PermissionManager.can_manage_scope(
            self.request.user, self.object, gameline, self.request
        ):
            raise PermissionDenied("Matching chronicle ST required")
        scene = self.object.add_scene(
            form.cleaned_data["name"],
            form.cleaned_data["location"],
            date_of_scene=form.cleaned_data["date_of_scene"],
            gameline=gameline,
        )
        return ServiceResult.ok(f"Scene '{scene.name}' created successfully!", obj=scene)

    def get_success_url(self, result=None):
        if result is not None:
            return result.object.get_absolute_url()
        return super().get_success_url()

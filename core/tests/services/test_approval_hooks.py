"""Opt-in submission and revision hooks in ApprovalService.transition_object."""

from unittest import mock

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.core.human import Human
from core.services import ApprovalService
from game.models import Chronicle
from locations.models.core.location import LocationModel


class TransitionHookTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("hook_owner")
        self.staff = users.objects.create_user("hook_staff", is_staff=True)
        self.chronicle = Chronicle.objects.create(name="Hook chronicle")
        self.location = LocationModel.objects.create(
            name="Hooked", owner=self.owner, chronicle=self.chronicle, status="Un"
        )

    def test_submission_errors_block_submit_with_every_reason(self):
        with mock.patch.object(
            LocationModel,
            "submission_errors",
            create=True,
            new=lambda self: ["First problem", "Second problem"],
        ):
            with self.assertRaises(ValidationError) as caught:
                ApprovalService.transition_object("location", self.location.pk, self.owner, "Sub")
        self.assertEqual(caught.exception.messages, ["First problem; Second problem"])
        self.location.refresh_from_db()
        self.assertEqual(self.location.status, "Un")

    def test_empty_submission_errors_allow_submit(self):
        with mock.patch.object(
            LocationModel, "submission_errors", create=True, new=lambda self: []
        ):
            obj = ApprovalService.transition_object("location", self.location.pk, self.owner, "Sub")
        self.assertEqual(obj.status, "Sub")
        self.location.refresh_from_db()
        self.assertEqual(self.location.status, "Sub")

    def test_return_hook_fields_are_saved(self):
        self.location.status = "Sub"
        self.location.creation_status = 7
        self.location.save()

        def reset(obj):
            obj.creation_status = 1
            return ["creation_status"]

        with mock.patch.object(LocationModel, "on_returned_for_revision", create=True, new=reset):
            ApprovalService.transition_object("location", self.location.pk, self.staff, "Rev")
        self.location.refresh_from_db()
        self.assertEqual(self.location.status, "Rev")
        self.assertEqual(self.location.creation_status, 1)

    def test_submit_does_not_call_return_hook(self):
        called = []
        with mock.patch.object(
            LocationModel,
            "on_returned_for_revision",
            create=True,
            new=lambda self: called.append(True) or [],
        ):
            ApprovalService.transition_object("location", self.location.pk, self.owner, "Sub")
        self.assertEqual(called, [])

    def test_models_without_hooks_are_unaffected(self):
        self.assertFalse(hasattr(Human, "submission_errors"))
        self.assertFalse(hasattr(Human, "on_returned_for_revision"))
        character = Human.objects.create(
            name="Plain", owner=self.owner, chronicle=self.chronicle, status="Un"
        )
        ApprovalService.transition_object("character", character.pk, self.owner, "Sub")
        character.refresh_from_db()
        self.assertEqual(character.status, "Sub")
        ApprovalService.transition_object("character", character.pk, self.staff, "Rev")
        character.refresh_from_db()
        self.assertEqual(character.status, "Rev")
        self.assertFalse(hasattr(LocationModel, "submission_errors"))
        location_obj = ApprovalService.transition_object(
            "location", self.location.pk, self.owner, "Sub"
        )
        self.assertEqual(location_obj.status, "Sub")

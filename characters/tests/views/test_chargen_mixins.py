"""Tests for ChargenProgressMixin."""

from django.test import TestCase

from characters.views.core.chargen_mixins import ChargenProgressMixin


class FakeBase:
    def get_context_data(self, **kwargs):
        return dict(kwargs)


class FakeView(ChargenProgressMixin, FakeBase):
    chargen_step_labels = [
        (1, "Attributes"),
        (2, "Abilities"),
        (3, "Backgrounds"),
    ]


class FakeCharacter:
    def __init__(self, creation_status):
        self.creation_status = creation_status


class TestChargenProgressMixin(TestCase):
    def get_steps(self, creation_status, view_class=FakeView):
        view = view_class()
        view.object = FakeCharacter(creation_status)
        return view.get_context_data().get("chargen_steps")

    def test_first_step_current(self):
        steps = self.get_steps(1)
        self.assertEqual(
            [s["status"] for s in steps], ["current", "pending", "pending"]
        )

    def test_middle_step(self):
        steps = self.get_steps(2)
        self.assertEqual(
            [s["status"] for s in steps], ["completed", "current", "pending"]
        )

    def test_last_step(self):
        steps = self.get_steps(3)
        self.assertEqual(
            [s["status"] for s in steps], ["completed", "completed", "current"]
        )

    def test_past_last_step_all_completed(self):
        steps = self.get_steps(4)
        self.assertEqual(
            [s["status"] for s in steps], ["completed", "completed", "completed"]
        )

    def test_grouped_statuses(self):
        class GroupedView(ChargenProgressMixin, FakeBase):
            chargen_step_labels = [(1, "Stats"), (4, "Powers"), (6, "Details")]

        # Status 5 falls inside the "Powers" group (4-5)
        steps = self.get_steps(5, GroupedView)
        self.assertEqual(
            [s["status"] for s in steps], ["completed", "current", "pending"]
        )

    def test_labels_included(self):
        steps = self.get_steps(1)
        self.assertEqual(
            [s["label"] for s in steps], ["Attributes", "Abilities", "Backgrounds"]
        )

    def test_no_labels_no_context(self):
        class NoLabelsView(ChargenProgressMixin, FakeBase):
            pass

        view = NoLabelsView()
        view.object = FakeCharacter(1)
        self.assertNotIn("chargen_steps", view.get_context_data())

    def test_no_object_no_context(self):
        view = FakeView()
        self.assertNotIn("chargen_steps", view.get_context_data())


class TestHumanChargenStepSync(TestCase):
    """HUMAN_CHARGEN_STEPS must cover exactly the view_mapping steps."""

    def test_step_labels_match_view_mapping(self):
        from characters.views.core.human import (
            HUMAN_CHARGEN_STEPS,
            HumanCharacterCreationView,
        )

        step_numbers = {start for start, _ in HUMAN_CHARGEN_STEPS}
        mapping_numbers = set(HumanCharacterCreationView.view_mapping.keys())
        self.assertEqual(step_numbers, mapping_numbers)

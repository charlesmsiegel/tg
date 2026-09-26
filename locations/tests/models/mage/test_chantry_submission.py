"""Chantry.submission_errors and Chantry.on_returned_for_revision."""

from django.test import TestCase

from characters.models.core.background_block import Background
from characters.models.mage.effect import Effect
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.services.chantry_points import affordable_effects, has_affordable_effect


def finished_chantry(**overrides):
    """A chantry that passes every submission check: 2 points, all spent on Allies."""
    fields = {"name": "Finished", "total_points": 2, "creation_status": 7, "status": "Un"}
    fields.update(overrides)
    chantry = Chantry.objects.create(**fields)
    allies = Background.objects.get_or_create(name="Allies", property_name="allies")[0]
    ChantryBackgroundRating.objects.create(chantry=chantry, bg=allies, rating=1, complete=True)
    return chantry


class AffordableEffectTests(TestCase):
    def setUp(self):
        self.chantry = Chantry.objects.create(
            name="Effects", total_points=30, integrated_effects_score=1
        )  # rank 3, 4 IE points
        self.cheap = Effect.objects.create(name="Cheap", forces=2)
        self.too_costly = Effect.objects.create(name="Costly", forces=3, prime=2)
        self.too_high = Effect.objects.create(name="High", forces=4)
        self.empty = Effect.objects.create(name="Empty")

    def test_only_affordable_unowned_effects_within_rank(self):
        self.assertEqual(list(affordable_effects(self.chantry)), [self.cheap])
        self.assertTrue(has_affordable_effect(self.chantry))

    def test_owned_effects_are_not_offered(self):
        self.chantry.integrated_effects.add(self.cheap)
        self.assertFalse(has_affordable_effect(self.chantry))


class SubmissionErrorsTests(TestCase):
    def test_finished_chantry_has_no_errors(self):
        self.assertEqual(finished_chantry().submission_errors(), [])

    def test_unfinished_wizard(self):
        chantry = finished_chantry(creation_status=6)
        self.assertEqual(
            chantry.submission_errors(),
            ["Finish every creation step (the chantry is on step 6 of 6)."],
        )

    def test_overspent_points(self):
        chantry = finished_chantry(total_points=1)
        self.assertIn("1 more point spent than the chantry has.", chantry.submission_errors())

    def test_affordable_purchase_left(self):
        chantry = finished_chantry(total_points=4)
        self.assertIn(
            "2 unspent points can still buy a background or Integrated Effects dot.",
            chantry.submission_errors(),
        )

    def test_integrated_effects_overcommitted(self):
        chantry = finished_chantry()
        chantry.integrated_effects.add(Effect.objects.create(name="Bolt", forces=1))
        self.assertIn(
            "Integrated effects cost 1 more point than the Integrated Effects score allows.",
            chantry.submission_errors(),
        )

    def test_affordable_effect_left(self):
        chantry = finished_chantry(total_points=4, integrated_effects_score=1)
        Effect.objects.create(name="Bolt", forces=1)
        self.assertIn(
            "4 Integrated Effects points can still buy an effect.",
            chantry.submission_errors(),
        )

    def test_background_not_allowed(self):
        chantry = finished_chantry(total_points=1002)
        avatar = Background.objects.get_or_create(name="Avatar", property_name="avatar")[0]
        ChantryBackgroundRating.objects.create(chantry=chantry, bg=avatar, rating=1)
        self.assertIn("Avatar is not a chantry background.", chantry.submission_errors())

    def test_rating_out_of_range(self):
        chantry = finished_chantry(total_points=12)
        chantry.backgrounds.update(rating=6)
        self.assertIn("Allies must be rated 1 to 5.", chantry.submission_errors())

    def test_incomplete_resource(self):
        chantry = finished_chantry()
        chantry.backgrounds.update(complete=False)
        self.assertIn("Allies has not been set up yet.", chantry.submission_errors())

    def test_incomplete_non_resource_background_is_fine(self):
        chantry = finished_chantry(total_points=4)
        cult = Background.objects.get_or_create(name="Cult", property_name="cult")[0]
        ChantryBackgroundRating.objects.create(chantry=chantry, bg=cult, rating=1)
        self.assertEqual(chantry.submission_errors(), [])

    def test_null_bg_rating_lists_a_reason_instead_of_crashing(self):
        chantry = finished_chantry(total_points=4)
        ChantryBackgroundRating.objects.create(chantry=chantry, bg=None, rating=1)
        self.assertIn(
            "A deleted background is not a chantry background.", chantry.submission_errors()
        )


class ReturnedForRevisionTests(TestCase):
    def test_resets_to_first_step_and_names_the_field(self):
        chantry = finished_chantry(status="Sub")
        self.assertEqual(chantry.on_returned_for_revision(), ["creation_status"])
        self.assertEqual(chantry.creation_status, 1)

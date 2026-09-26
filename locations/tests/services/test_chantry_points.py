"""Tests for the chantry points service (M20 chantry costs and caps)."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.core.background_block import Background
from characters.tests.utils import mage_setup
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.services import chantry_points as svc


class ChantryPointsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        mage_setup()
        cls.allies = Background.objects.get(property_name="allies")
        cls.node = Background.objects.get(property_name="node")
        cls.resources = Background.objects.get(property_name="resources")
        cls.requisitions = Background.objects.get(property_name="requisitions")
        cls.sanctum = Background.objects.get(property_name="sanctum")
        cls.library = Background.objects.get(property_name="library")
        cls.fame = Background.objects.get(property_name="fame")

    def make_chantry(self, total_points=20, **kwargs):
        return Chantry.objects.create(name="Test Chantry", total_points=total_points, **kwargs)

    def rate(self, chantry, bg, rating):
        return ChantryBackgroundRating.objects.create(chantry=chantry, bg=bg, rating=rating)


class TestCostsAndCaps(ChantryPointsTestCase):
    def test_every_cost_tier(self):
        chantry = self.make_chantry(total_points=100)
        for bg, cost in [
            (self.allies, 2),
            (self.node, 3),
            (self.resources, 3),
            (self.requisitions, 4),
            (self.sanctum, 5),
        ]:
            with self.subTest(bg=bg.property_name):
                self.assertEqual(svc.next_dot_cost(chantry, bg), cost)
                before = chantry.points
                svc.buy_background_dot(chantry, bg)
                self.assertEqual(before - chantry.points, cost)
        before = chantry.points
        svc.buy_ie_dot(chantry)
        self.assertEqual(before - chantry.points, 2)

    def test_only_allowed_backgrounds(self):
        chantry = self.make_chantry()
        self.assertFalse(svc.can_buy_background(chantry, self.fame))
        with self.assertRaises(ValidationError):
            svc.buy_background_dot(chantry, self.fame)
        self.assertFalse(chantry.backgrounds.exists())

    def test_five_dot_cap(self):
        chantry = self.make_chantry(total_points=100)
        self.rate(chantry, self.allies, 5)
        self.assertFalse(svc.can_buy_background(chantry, self.allies))
        with self.assertRaises(ValidationError):
            svc.buy_background_dot(chantry, self.allies)

    def test_ie_cap_of_ten(self):
        chantry = self.make_chantry(total_points=100, integrated_effects_score=10)
        self.assertFalse(svc.can_buy_ie(chantry))
        with self.assertRaises(ValidationError):
            svc.buy_ie_dot(chantry)
        chantry.refresh_from_db()
        self.assertEqual(chantry.integrated_effects_score, 10)

    def test_insufficient_points(self):
        chantry = self.make_chantry(total_points=4)
        self.assertTrue(svc.can_buy_background(chantry, self.requisitions))
        self.assertFalse(svc.can_buy_background(chantry, self.sanctum))
        with self.assertRaises(ValidationError):
            svc.buy_background_dot(chantry, self.sanctum)
        chantry.total_points = 1
        chantry.save()
        self.assertFalse(svc.can_buy_ie(chantry))
        with self.assertRaises(ValidationError):
            svc.buy_ie_dot(chantry)

    def test_buy_creates_then_increments_one_rating(self):
        chantry = self.make_chantry()
        first = svc.buy_background_dot(chantry, self.allies, note="Friends", display_alt_name=True)
        self.assertEqual((first.rating, first.note, first.display_alt_name), (1, "Friends", True))
        second = svc.buy_background_dot(chantry, self.allies)
        self.assertEqual(second.pk, first.pk)
        self.assertEqual(second.rating, 2)
        self.assertEqual(chantry.backgrounds.count(), 1)

    def test_purchase_rechecks_the_locked_row(self):
        chantry = self.make_chantry(total_points=10)
        stale = Chantry.objects.get(pk=chantry.pk)
        Chantry.objects.filter(pk=chantry.pk).update(total_points=0)
        # ``stale`` still says 10 points; the service must trust the locked row.
        self.assertEqual(stale.total_points, 10)
        with self.assertRaises(ValidationError):
            svc.buy_background_dot(stale, self.allies)
        with self.assertRaises(ValidationError):
            svc.buy_ie_dot(stale)
        self.assertFalse(ChantryBackgroundRating.objects.filter(chantry=chantry).exists())

    def test_sequential_double_spend_is_refused(self):
        chantry = self.make_chantry(total_points=2)
        first_view = Chantry.objects.get(pk=chantry.pk)
        second_view = Chantry.objects.get(pk=chantry.pk)
        svc.buy_background_dot(first_view, self.allies)
        with self.assertRaises(ValidationError):
            svc.buy_background_dot(second_view, self.node)
        chantry.refresh_from_db()
        self.assertEqual(chantry.points, 0)


class TestHasAffordablePurchase(ChantryPointsTestCase):
    def test_true_with_points_to_spend(self):
        self.assertTrue(svc.has_affordable_purchase(self.make_chantry(total_points=2)))

    def test_false_with_one_point(self):
        self.assertFalse(svc.has_affordable_purchase(self.make_chantry(total_points=1)))

    def test_false_when_everything_affordable_is_capped(self):
        chantry = self.make_chantry(total_points=200, integrated_effects_score=10)
        for property_name in Chantry.allowed_backgrounds:
            bg, _ = Background.objects.get_or_create(
                property_name=property_name, defaults={"name": property_name.title()}
            )
            self.rate(chantry, bg, 5)
        self.assertGreater(chantry.points, 0)
        self.assertFalse(svc.has_affordable_purchase(chantry))

    def test_affordable_backgrounds_splits_new_and_existing(self):
        chantry = self.make_chantry(total_points=5)  # 3 left after Allies 1
        allies = self.rate(chantry, self.allies, 1)
        new, existing = svc.affordable_backgrounds(chantry)
        self.assertEqual(existing, [allies])
        self.assertIn(self.node, new)
        self.assertNotIn(self.allies, new)
        self.assertNotIn(self.sanctum, new)
        self.assertNotIn(self.fame, new)

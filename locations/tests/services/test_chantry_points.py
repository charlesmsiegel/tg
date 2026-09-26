"""Tests for the chantry points service (M20 chantry costs and caps)."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.core.background_block import Background
from characters.models.core.human import Human
from characters.models.mage.effect import Effect
from characters.tests.utils import mage_setup
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.models.mage.library import Library
from locations.models.mage.node import Node
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

    def test_skips_allowed_background_with_no_background_row(self):
        """An allowed background name can lack a Background row without crashing."""
        chantry = self.make_chantry(total_points=5)
        self.node.delete()
        new, existing = svc.affordable_backgrounds(chantry)
        self.assertNotIn(self.node, new)
        self.assertIn(self.allies, new)
        self.assertTrue(svc.has_affordable_purchase(chantry))


class TestRemoval(ChantryPointsTestCase):
    def test_refund_one_dot(self):
        chantry = self.make_chantry()
        rating = self.rate(chantry, self.node, 2)
        points = chantry.points
        result = svc.remove_background_dot(rating)
        self.assertEqual(result.rating, 1)
        self.assertEqual(chantry.points, points + 3)

    def test_rating_deleted_at_zero(self):
        chantry = self.make_chantry()
        rating = self.rate(chantry, self.allies, 1)
        self.assertIsNone(svc.remove_background_dot(rating))
        self.assertFalse(ChantryBackgroundRating.objects.filter(pk=rating.pk).exists())

    def test_removal_detaches_linked_node(self):
        chantry = self.make_chantry()
        node = Node.objects.create(name="Well", rank=2)
        chantry.add_node(node)
        rating = self.rate(chantry, self.node, 2)
        rating.linked_object = node
        rating.note = "Well"
        rating.url = node.get_absolute_url()
        rating.complete = True
        rating.save()

        svc.remove_background_dot(rating)

        rating.refresh_from_db()
        self.assertEqual(rating.rating, 1)
        self.assertIsNone(rating.linked_object)
        self.assertEqual((rating.note, rating.url, rating.complete), ("", "", False))
        self.assertFalse(chantry.nodes.filter(pk=node.pk).exists())
        self.assertTrue(Node.objects.filter(pk=node.pk).exists())

    def test_removal_detaches_linked_library(self):
        chantry = self.make_chantry()
        library = Library.objects.create(name="Stacks", rank=1)
        chantry.chantry_library = library
        chantry.save()
        library.contained_within.add(chantry)
        rating = self.rate(chantry, self.library, 1)
        rating.linked_object = library
        rating.complete = True
        rating.save()

        self.assertIsNone(svc.remove_background_dot(rating))

        chantry.refresh_from_db()
        self.assertIsNone(chantry.chantry_library)
        self.assertFalse(library.contained_within.filter(pk=chantry.pk).exists())
        self.assertTrue(Library.objects.filter(pk=library.pk).exists())

    def test_removal_unlinks_ally_without_deleting_it(self):
        chantry = self.make_chantry()
        ally = Human.objects.create(name="Friendly Face")
        rating = self.rate(chantry, self.allies, 2)
        rating.linked_object = ally
        rating.complete = True
        rating.save()

        svc.remove_background_dot(rating)

        rating.refresh_from_db()
        self.assertIsNone(rating.linked_object)
        self.assertFalse(rating.complete)
        self.assertTrue(Human.objects.filter(pk=ally.pk).exists())

    def test_ie_removal_refused_when_effects_would_overcommit(self):
        chantry = self.make_chantry(integrated_effects_score=2)  # 8 IE points
        effect = Effect.objects.create(name="Big Ward", forces=3, prime=2)  # rote_cost 5
        chantry.integrated_effects.add(effect)
        with self.assertRaises(ValidationError):
            svc.remove_ie_dot(chantry)  # IE 1 allows only 4
        chantry.refresh_from_db()
        self.assertEqual(chantry.integrated_effects_score, 2)

        svc.remove_effect(chantry, effect)
        self.assertEqual(svc.remove_ie_dot(chantry), 1)
        chantry.refresh_from_db()
        self.assertEqual(chantry.integrated_effects_score, 1)

    def test_ie_removal_refused_at_zero(self):
        chantry = self.make_chantry()
        with self.assertRaises(ValidationError):
            svc.remove_ie_dot(chantry)

    def test_remove_effect_not_chosen_is_refused(self):
        chantry = self.make_chantry()
        effect = Effect.objects.create(name="Loose", forces=1)
        with self.assertRaises(ValidationError):
            svc.remove_effect(chantry, effect)

    def test_removal_of_a_vanished_rating_is_refused(self):
        """A concurrent remove already deleted the rating; no bare DoesNotExist leaks out."""
        chantry = self.make_chantry()
        rating = self.rate(chantry, self.allies, 1)
        ChantryBackgroundRating.objects.filter(pk=rating.pk).delete()
        with self.assertRaises(ValidationError):
            svc.remove_background_dot(rating)

    def test_removal_of_an_orphaned_rating_is_refused(self):
        """The rating's chantry was deleted (SET_NULL); no bare AttributeError leaks out."""
        chantry = self.make_chantry()
        rating = self.rate(chantry, self.allies, 1)
        chantry.delete()
        rating.refresh_from_db()
        self.assertIsNone(rating.chantry_id)
        with self.assertRaises(ValidationError):
            svc.remove_background_dot(rating)


class TestLibraryTypeRule(ChantryPointsTestCase):
    def test_apply_type_grants_creates_free_library_dots(self):
        chantry = self.make_chantry(total_points=10, chantry_type="library")
        rating = svc.apply_type_grants(chantry)
        self.assertEqual((rating.bg, rating.rating), (self.library, 3))
        self.assertEqual(chantry.points, 10)

    def test_apply_type_grants_raises_to_floor_and_keeps_more(self):
        chantry = self.make_chantry(total_points=10, chantry_type="library")
        rating = self.rate(chantry, self.library, 1)
        svc.apply_type_grants(chantry)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 3)
        rating.rating = 4
        rating.save()
        svc.apply_type_grants(chantry)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 4)
        self.assertEqual(chantry.backgrounds.count(), 1)

    def test_apply_type_grants_ignores_other_types(self):
        chantry = self.make_chantry(chantry_type="war")
        self.assertIsNone(svc.apply_type_grants(chantry))
        self.assertFalse(chantry.backgrounds.exists())

    def test_dots_above_floor_are_paid_and_capped(self):
        chantry = self.make_chantry(total_points=10, chantry_type="library")
        svc.apply_type_grants(chantry)
        self.assertEqual(svc.next_dot_cost(chantry, self.library), 2)
        svc.buy_background_dot(chantry, self.library)
        svc.buy_background_dot(chantry, self.library)
        self.assertEqual(chantry.points, 6)
        with self.assertRaises(ValidationError):
            svc.buy_background_dot(chantry, self.library)

    def test_floor_cannot_be_removed(self):
        chantry = self.make_chantry(total_points=10, chantry_type="library")
        rating = svc.apply_type_grants(chantry)
        svc.buy_background_dot(chantry, self.library)
        rating.refresh_from_db()
        svc.remove_background_dot(rating)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 3)
        with self.assertRaises(ValidationError):
            svc.remove_background_dot(rating)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 3)

    def test_dots_become_paid_when_type_changes(self):
        chantry = self.make_chantry(total_points=10, chantry_type="library")
        svc.apply_type_grants(chantry)
        chantry.chantry_type = "war"
        chantry.save()
        self.assertEqual(chantry.points, 4)

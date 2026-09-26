"""ChantryBackgroundRating.linked_object: one link across two polymorphic trees."""

from django.test import TestCase

from characters.models.core.background_block import Background
from characters.models.core.human import Human
from items.models.mage.grimoire import Grimoire
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.models.mage.node import Node


class TestChantryRatingLinkedObject(TestCase):
    def setUp(self):
        self.chantry = Chantry.objects.create(name="Linked Chantry", total_points=10)
        self.node_bg, _ = Background.objects.get_or_create(
            property_name="node", defaults={"name": "Node"}
        )
        self.rating = ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=self.node_bg, rating=2
        )

    def test_defaults_to_none(self):
        self.assertIsNone(self.rating.linked_object)

    def test_links_a_location_and_returns_the_concrete_class(self):
        node = Node.objects.create(name="Spring", rank=2)
        self.rating.linked_object = node
        self.rating.save()
        rating = ChantryBackgroundRating.objects.get(pk=self.rating.pk)
        self.assertIsInstance(rating.linked_object, Node)
        self.assertEqual(rating.linked_object.pk, node.pk)
        self.assertIsNone(rating.linked_character)

    def test_links_a_character(self):
        ally = Human.objects.create(name="Ally")
        self.rating.linked_object = ally
        self.rating.save()
        rating = ChantryBackgroundRating.objects.get(pk=self.rating.pk)
        self.assertEqual(rating.linked_object.pk, ally.pk)
        self.assertIsNone(rating.linked_location)

    def test_relinking_replaces_the_other_tree(self):
        self.rating.linked_object = Human.objects.create(name="Ally")
        self.rating.linked_object = Node.objects.create(name="Spring", rank=2)
        self.assertIsNone(self.rating.linked_character)
        self.rating.linked_object = None
        self.assertIsNone(self.rating.linked_location)

    def test_rejects_other_objects(self):
        with self.assertRaises(TypeError):
            self.rating.linked_object = Grimoire.objects.create(name="Book")

    def test_deleting_the_linked_node_clears_the_link(self):
        node = Node.objects.create(name="Doomed", rank=2)
        self.rating.linked_object = node
        self.rating.note = "Doomed"
        self.rating.save()
        node.delete()
        self.rating.refresh_from_db()
        self.assertIsNone(self.rating.linked_object)
        self.assertEqual(self.rating.note, "Doomed")

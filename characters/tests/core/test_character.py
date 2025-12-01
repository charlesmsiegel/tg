from characters.models.core import Character, Human
from django.contrib.auth.models import User
from django.test import TestCase


class TestCharacter(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.character = Character.objects.create(owner=self.player, name="Test Character")

    def test_has_name(self):
        self.assertFalse(self.character.has_name())
        self.character.set_name("Test")
        self.assertTrue(self.character.has_name())

    def test_set_name(self):
        self.assertEqual(self.character.name, "")
        self.assertTrue(self.character.set_name("Test"))
        self.assertNotEqual(self.character.name, "")

    def test_has_concept(self):
        self.assertFalse(self.character.has_concept())
        self.character.set_concept("Test")
        self.assertTrue(self.character.has_concept())

    def test_set_concept(self):
        self.assertEqual(self.character.concept, "")
        self.assertTrue(self.character.set_concept("Test"))
        self.assertNotEqual(self.character.concept, "")

    def test_absolute_url(self):
        self.assertEqual(
            self.character.get_absolute_url(), f"/characters/{self.character.id}/"
        )


class TestGenericCharacterDetailViews(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="Test")
        self.character = Character.objects.create(
            name="Test Char", owner=self.player, status="App"
        )
        self.human = Human.objects.create(
            name="Test Human", owner=self.player, status="App"
        )

    def test_character_detail_view_templates(self):
        response = self.client.get(self.character.get_absolute_url())
        self.assertTemplateUsed(response, "characters/core/character/detail.html")
        response = self.client.get(self.human.get_absolute_url())
        self.assertTemplateUsed(response, "characters/core/human/detail.html")

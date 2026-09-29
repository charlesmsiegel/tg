"""Chronicle launch links keep their context through selection and creation."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from game.models import Chronicle, ObjectType
from items.models.core.item import ItemModel


class ChronicleCreationContextTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("chronicle_creator")
        self.chronicle = Chronicle.objects.create(name="Origin Chronicle", head_st=self.user)
        self.client.force_login(self.user)

    def test_type_selector_keeps_chronicle_for_characters_and_items(self):
        ObjectType.objects.create(name="mage", type="char", gameline="mta")
        for kind, field, value, gameline in (
            ("character", "char_type", "mage", "mta"),
            ("item", "item_type", "item", "wod"),
        ):
            with self.subTest(kind=kind):
                response = self.client.get(
                    reverse(
                        "core:object_type_redirect",
                        kwargs={"kind": kind, "action": "create"},
                    ),
                    {field: value, "gameline": gameline, "chronicle": self.chronicle.pk},
                )
                self.assertEqual(response.status_code, 302)
                self.assertIn(f"chronicle={self.chronicle.pk}", response.url)

    def test_mage_creation_selects_requested_chronicle(self):
        response = self.client.get(
            reverse("characters:mage:create:mage"), {"chronicle": self.chronicle.pk}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["form"]["chronicle"].value()), str(self.chronicle.pk))

    def test_generic_character_create_view_selects_requested_chronicle(self):
        response = self.client.get(
            reverse("characters:create:character"), {"chronicle": self.chronicle.pk}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["form"]["chronicle"].value()), str(self.chronicle.pk))

    def test_unreadable_chronicle_is_not_preselected(self):
        other = Chronicle.objects.create(name="Other Chronicle")
        response = self.client.get(reverse("characters:mage:create:mage"), {"chronicle": other.pk})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(str(response.context["form"]["chronicle"].value()), str(other.pk))

    def test_item_without_chronicle_field_uses_launch_chronicle(self):
        response = self.client.post(
            f"{reverse('items:create:item')}?chronicle={self.chronicle.pk}",
            {"name": "Chronicle Relic", "description": "A clue"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ItemModel.objects.get(name="Chronicle Relic").chronicle, self.chronicle)

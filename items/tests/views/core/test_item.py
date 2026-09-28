from django.contrib.auth import get_user_model
from django.test import TestCase

from game.models import ObjectType
from items.models.core.item import ItemModel


class TestItemIndexView(TestCase):
    def setUp(self) -> None:
        self.url = "/items/index/"
        ObjectType.objects.get_or_create(name="item", type="obj", gameline="wod")[0]
        return super().setUp()

    def test_index_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_template(self):
        self.client.force_login(
            get_user_model().objects.create_user("__legacy_auth_staff", is_staff=True)
        )
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/index.html")

    def test_index_content(self):
        self.client.force_login(
            get_user_model().objects.create_user("__legacy_auth_staff", is_staff=True)
        )
        for i in range(10):
            ItemModel.objects.create(
                name=f"Item {i}",
            )
        response = self.client.get(self.url)
        for i in range(10):
            self.assertContains(response, f"Item {i}")


class TestItemIndexGrouping(TestCase):
    """Spread M3: ?chronicle= picks the chronicle, ?line= the gameline, tables by group."""

    @classmethod
    def setUpTestData(cls):
        from game.models import Chronicle
        from items.models.mage import Grimoire, Wonder
        from items.models.werewolf import Fetish

        cls.staff = get_user_model().objects.create_user("st", is_staff=True)
        cls.chronicle = Chronicle.objects.create(name="Ashes of Hyde Park")
        Wonder.objects.create(name="Astrolabe", rank=3, chronicle=cls.chronicle)
        Grimoire.objects.create(name="Book of Streets", rank=4, chronicle=cls.chronicle)
        Fetish.objects.create(name="Crow-Feather Knife", rank=2, chronicle=cls.chronicle)
        ItemModel.objects.create(name="Hidden", chronicle=cls.chronicle, display=False)
        ItemModel.objects.create(name="Loose Item")

    def setUp(self):
        self.client.force_login(self.staff)

    def test_defaults_to_first_chronicle_with_items_and_groups_them(self):
        response = self.client.get("/items/index/")
        self.assertEqual(response.context["selected_chronicle"], self.chronicle)
        groups = [
            (g["label"], [i.name for i in g["items"]]) for g in response.context["item_groups"]
        ]
        self.assertEqual(
            groups,
            [
                ("Wonders", ["Astrolabe"]),
                ("Grimoires", ["Book of Streets"]),
                ("Fetishes & Talens", ["Crow-Feather Knife"]),
            ],
        )
        self.assertNotContains(response, "Hidden")
        self.assertNotContains(response, "Loose Item")

    def test_line_filter_and_counts(self):
        response = self.client.get(f"/items/index/?chronicle={self.chronicle.pk}&line=wta")
        self.assertEqual(response.context["selected_line"], "wta")
        self.assertEqual(
            [(t["key"], t["count"]) for t in response.context["line_tabs"]],
            [("all", 3), ("wta", 1), ("mta", 2)],
        )
        self.assertEqual(
            [g["label"] for g in response.context["item_groups"]], ["Fetishes & Talens"]
        )

    def test_unknown_line_shows_all_and_no_chronicle_is_selectable(self):
        response = self.client.get("/items/index/?chronicle=none&line=bogus")
        self.assertIsNone(response.context["selected_chronicle"])
        self.assertEqual(response.context["selected_line"], "all")
        self.assertContains(response, "Loose Item")
        self.assertEqual([g["label"] for g in response.context["item_groups"]], ["Other items"])

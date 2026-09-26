"""Public discovery uses route policy, independently of private list mixins."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from items.models.core import Weapon
from items.models.mage import Talisman, Wonder
from locations.models.core import City
from locations.models.vampire import Barrens, TremereChantry


class PublicListDiscoveryTests(TestCase):
    models_and_routes = (
        (Weapon, "items:list:weapon"),
        (Wonder, "items:mage:list:wonder"),
        (Talisman, "items:mage:list:talisman"),
        (City, "locations:list:city"),
        (TremereChantry, "locations:vampire:list:tremere_chantry"),
        (Barrens, "locations:vampire:list:barrens"),
    )

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("public-list-reader")
        cls.rows = []
        for model, route in cls.models_and_routes:
            public = model.objects.create(
                name=f"Published {model.__name__}",
                visibility="PUB",
                public_info="Allowlisted public information",
                st_notes="SECRET FULL SHEET",
            )
            private = model.objects.create(
                name=f"Unlisted {model.__name__}",
                visibility="PRI",
                st_notes="SECRET FULL SHEET",
            )
            cls.rows.append((route, public, private))

    def assert_public_discovery(self):
        for route, public, private in self.rows:
            with self.subTest(route=route):
                self.assertIsNone(public.owner_id)
                self.assertIsNone(public.chronicle_id)
                response = self.client.get(reverse(route))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "core/public_object_list.html")
                self.assertContains(response, public.name)
                self.assertNotContains(response, private.name)
                self.assertNotContains(response, "SECRET FULL SHEET")
                self.assertNotIn("object_list", response.context)
                for row in response.context["public_objects"]:
                    self.assertEqual(set(row), {"name", "public_info", "image_url", "url"})
                # A directly reachable card is not full/private read authority.
                detail = self.client.get(private.get_absolute_url())
                self.assertEqual(detail.status_code, 200)
                self.assertTemplateUsed(detail, "core/public_object_detail.html")
                self.assertContains(detail, private.name)
                self.assertNotContains(detail, "SECRET FULL SHEET")
                self.assertNotIn("object", detail.context)

    def test_anonymous_discovers_unowned_public_cards(self):
        self.assert_public_discovery()

    def test_nonstaff_discovers_unowned_public_cards(self):
        self.client.force_login(self.user)
        self.assert_public_discovery()

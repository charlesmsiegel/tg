"""Spread reference pages (C7 card grid, M12 table, M13 / C15 detail) and their list queries."""

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from characters.models.core import MeritFlaw
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage import Effect, Practice, Rote
from characters.models.mage.faction import MageFaction
from characters.models.mage.sorcerer import LinearMagicPath, LinearMagicRitual
from characters.models.werewolf.gift import Gift, GiftPermission
from game.models import ObjectType

User = get_user_model()


class ReferencePageTestCase(TestCase):
    def setUp(self):
        cache.clear()  # several reference views are cache_page'd
        self.staff = User.objects.create_user("keeper", password="pw", is_staff=True)
        self.strength = Attribute.objects.create(name="Strength", property_name="strength")
        self.occult = Ability.objects.create(name="Occult", property_name="occult")
        self.practice = Practice.objects.create(name="High Ritual Magick")

    def make_rote(self, name, **spheres):
        effect = Effect.objects.create(name=f"{name} effect", **spheres)
        return Rote.objects.create(
            name=name,
            effect=effect,
            practice=self.practice,
            attribute=self.strength,
            ability=self.occult,
            description=f"{name} description.",
        )

    def count_queries(self, url, client=None):
        cache.clear()
        with CaptureQueriesContext(connection) as queries:
            response = (client or self.client).get(url)
        self.assertEqual(response.status_code, 200)
        return len(queries)


class RoteListTests(ReferencePageTestCase):
    url = reverse("characters:mage:list:rote")

    def setUp(self):
        super().setUp()
        self.client.force_login(self.staff)

    def test_cards_keep_filter_attributes_and_count(self):
        self.make_rote("Ward of Closed Doors", prime=2, correspondence=2)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/tl/reference_list.html")
        self.assertContains(response, "data-filter-count")
        self.assertContains(response, "1 of 1 shown")
        self.assertContains(response, 'data-filterable-list="rotes"')
        self.assertContains(response, "data-filterable-item")
        self.assertContains(response, 'data-prime="2"')
        self.assertContains(response, 'data-filter-max="correspondence"')
        self.assertContains(response, "data-filter-clear")
        self.assertContains(response, reverse("characters:mage:create:rote"))

    def test_query_count_does_not_grow_with_rotes(self):
        self.make_rote("One", life=1)
        few = self.count_queries(self.url)
        for name in ("Two", "Three", "Four"):
            self.make_rote(name, mind=2)
        self.assertEqual(self.count_queries(self.url), few)

    def test_empty_list_shows_empty_state(self):
        response = self.client.get(self.url)
        self.assertContains(response, "No rotes yet.")
        self.assertNotContains(response, "data-filter-no-results")


class RoteDetailTests(ReferencePageTestCase):
    def test_spheres_section_shows_only_spheres_above_zero(self):
        rote = self.make_rote("Ward of Closed Doors", prime=2, correspondence=2)
        self.client.force_login(self.staff)
        response = self.client.get(rote.get_absolute_url())
        self.assertTemplateUsed(response, "characters/tl/reference_detail.html")
        self.assertContains(response, "Rote cost")
        self.assertContains(response, "Prime</span>")
        self.assertContains(response, "Correspondence</span>")
        self.assertNotContains(response, "Entropy</span>")
        self.assertContains(response, "Strength + Occult")
        self.assertContains(response, rote.effect.get_absolute_url())


class GiftListTests(ReferencePageTestCase):
    url = reverse("characters:werewolf:list:gift")

    def make_gift(self, name, *conditions):
        gift = Gift.objects.create(name=name, rank=1, description="A gift.")
        for condition in conditions:
            perm, _ = GiftPermission.objects.get_or_create(shifter="werewolf", condition=condition)
            gift.allowed.add(perm)
        return gift

    def test_public_without_create_link(self):
        self.make_gift("Spirit Speech", "Theurge", "Uktena")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-filter-match="token"')
        self.assertContains(response, "Werewolf (Theurge)")
        self.assertNotContains(response, reverse("characters:werewolf:create:gift"))

    def test_query_count_does_not_grow_with_gifts(self):
        self.make_gift("One", "Theurge")
        few = self.count_queries(self.url)
        for name in ("Two", "Three", "Four"):
            self.make_gift(name, "Theurge", "Ahroun")
        self.assertEqual(self.count_queries(self.url), few)

    def test_detail_is_public_with_cover_facts(self):
        gift = self.make_gift("Spirit Speech", "Theurge")
        response = self.client.get(gift.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Available to")
        self.assertContains(response, reverse("characters:werewolf:list:gift"))
        self.assertNotContains(response, ">Edit<")


class MeritFlawListTests(ReferencePageTestCase):
    url = reverse("characters:list:meritflaw")

    def test_line_codes_type_and_negative_rating(self):
        mage, _ = ObjectType.objects.get_or_create(
            name="mage", defaults={"type": "char", "gameline": "mta"}
        )
        merit = MeritFlaw.objects.create(name="Avatar Companion")
        merit.add_ratings([1, 2, 3])
        merit.allowed_types.add(mage)
        flaw = MeritFlaw.objects.create(name="Nightmares")
        flaw.add_rating(-1)

        response = self.client.get(self.url)
        by_name = {mf.name: mf for mf in response.context["object_list"]}
        self.assertEqual(by_name["Avatar Companion"].line_codes, ["mta"])
        self.assertEqual(by_name["Nightmares"].line_codes, [])
        self.assertNotIn("wod", response.context["gamelines"])
        self.assertContains(response, 'data-lines="mta"')
        self.assertContains(response, 'class="tl-num is-neg"')
        self.assertContains(response, "+1 – +3")

    def test_query_count_does_not_grow_with_entries(self):
        mage, _ = ObjectType.objects.get_or_create(
            name="mage", defaults={"type": "char", "gameline": "mta"}
        )
        MeritFlaw.objects.create(name="One").allowed_types.add(mage)
        few = self.count_queries(self.url)
        for name in ("Two", "Three", "Four"):
            MeritFlaw.objects.create(name=name).allowed_types.add(mage)
        self.assertEqual(self.count_queries(self.url), few)


class RitualListTests(ReferencePageTestCase):
    url = reverse("characters:mage:list:ritual")

    def test_query_count_does_not_grow_with_rituals(self):
        path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        LinearMagicRitual.objects.create(name="One", path=path, level=1)
        few = self.count_queries(self.url)
        for i in range(3):
            other = LinearMagicPath.objects.create(name=f"Path {i}", numina_type="psychic")
            LinearMagicRitual.objects.create(name=f"Ritual {i}", path=other, level=2)
        self.assertEqual(self.count_queries(self.url), few)


class MageFactionDetailTests(ReferencePageTestCase):
    def test_founded_and_ended_years_read_their_own_dates(self):
        faction = MageFaction.objects.create(name="Old Order", founded=-300, ended=1450)
        response = self.client.get(faction.get_absolute_url())
        self.assertEqual(response.context["year"], 300)
        self.assertEqual(response.context["ended_year"], 1450)
        self.assertContains(response, "300 BC")
        self.assertContains(response, "1450 AD")

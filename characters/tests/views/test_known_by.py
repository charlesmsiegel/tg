"""Known by (Spread M13, 03) on reference detail pages.

The list shows only characters whose full sheet the viewer can already read (own
characters, characters in chronicles the viewer staffs, everything for staff), grouped
by chronicle, with bounded queries, and never through a URL-only page cache.
"""

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import connection
from django.test import TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from characters.models.core import Human, MeritFlaw
from characters.models.core.merit_flaw_block import MeritFlawRating
from characters.models.demon import Demon
from characters.models.demon.earthbound import Earthbound
from characters.models.demon.lore import Lore
from characters.models.demon.ritual import Ritual as DemonRitual
from characters.models.hunter import Edge, Hunter
from characters.models.mage import Mage, Sphere
from characters.models.mage.companion import Advantage, AdvantageRating, Companion
from characters.models.mage.sorcerer import LinearMagicPath, PathRating, Sorcerer
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.vampire import Vampire
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.gift import Gift
from characters.models.werewolf.rite import Rite
from characters.models.wraith.arcanos import Arcanos
from characters.models.wraith.thorn import Thorn
from characters.models.wraith.wraith import ThornRating, Wraith
from characters.views.core.known_by import known_by
from game.models import Chronicle

User = get_user_model()

LOCMEM = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}


class KnownByTestCase(TestCase):
    def setUp(self):
        cache.clear()  # Discipline, Gift, Sphere, Arcanos and Merit pages are cache_page'd
        self.addCleanup(cache.clear)
        self.mira = User.objects.create_user("mira", password="pw")
        self.jpark = User.objects.create_user("jpark", password="pw")
        self.st = User.objects.create_user("storyteller", password="pw")
        self.outsider = User.objects.create_user("outsider", password="pw")
        self.staff = User.objects.create_user("keeper", password="pw", is_staff=True)
        self.cedar = Chronicle.objects.create(name="The Cedar Sept", head_st=self.st)
        self.ash = Chronicle.objects.create(name="Ashfall")
        self.potence = Discipline.objects.create(
            name="Potence", property_name="potence", description="Unnatural strength."
        )
        self.url = reverse("characters:vampire:discipline", kwargs={"pk": self.potence.pk})
        self.aurelio = Vampire.objects.create(
            name="Aurelio Brandt", owner=self.mira, chronicle=self.cedar, potence=3
        )
        self.bianca = Vampire.objects.create(
            name="Bianca", owner=self.jpark, chronicle=self.cedar, potence=2
        )
        self.cato = Vampire.objects.create(
            name="Cato", owner=self.outsider, chronicle=self.ash, potence=1
        )
        # Holds no Potence, so never listed.
        Vampire.objects.create(name="Dara", owner=self.mira, chronicle=self.cedar)

    def get(self, user=None, url=None):
        cache.clear()
        self.client.logout()
        if user is not None:
            self.client.force_login(user)
        response = self.client.get(url or self.url)
        self.assertEqual(response.status_code, 200)
        return response

    def names(self, response):
        known = response.context["known_by"]
        if known is None:
            return None
        return [row["name"] for group in known["groups"] for row in group["rows"]]


class KnownByVisibilityTests(KnownByTestCase):
    def test_owner_sees_only_their_own_characters(self):
        response = self.get(self.mira)
        self.assertEqual(self.names(response), ["Aurelio Brandt"])
        self.assertContains(response, 'id="known-by"')
        self.assertContains(response, "Known by")
        self.assertNotContains(response, "Bianca")

    def test_other_player_in_the_chronicle_does_not_see_the_owners_character(self):
        # A chronicle-mate only reaches the public card (VIEW_PARTIAL), not ratings.
        response = self.get(self.jpark)
        self.assertEqual(self.names(response), ["Bianca"])
        self.assertNotContains(response, "Aurelio Brandt")

    def test_storyteller_sees_every_character_in_their_chronicle(self):
        response = self.get(self.st)
        self.assertEqual(self.names(response), ["Aurelio Brandt", "Bianca"])
        self.assertNotContains(response, "Cato")

    def test_game_storyteller_and_st_relationship_count_as_staffing(self):
        self.ash.game_storytellers.add(self.jpark)
        self.assertEqual(self.names(self.get(self.jpark)), ["Cato", "Bianca"])

    def test_staff_see_every_character(self):
        self.assertEqual(self.names(self.get(self.staff)), ["Cato", "Aurelio Brandt", "Bianca"])

    def test_anonymous_viewers_get_no_section(self):
        response = self.get()
        self.assertIsNone(response.context["known_by"])
        self.assertNotContains(response, 'id="known-by"')
        self.assertNotContains(response, "Aurelio Brandt")

    def test_viewer_without_visible_holders_gets_the_empty_state(self):
        response = self.get(User.objects.create_user("newcomer", password="pw"))
        self.assertEqual(response.context["known_by"]["groups"], [])
        self.assertContains(response, "None of the characters you can see know this yet.")

    def test_hidden_characters_are_left_out(self):
        self.bianca.display = False
        self.bianca.save()
        self.assertEqual(self.names(self.get(self.st)), ["Aurelio Brandt"])


class KnownByLayoutTests(KnownByTestCase):
    def test_rows_are_grouped_by_chronicle_with_rating(self):
        response = self.get(self.staff)
        groups = response.context["known_by"]["groups"]
        self.assertEqual([group["chronicle"] for group in groups], [self.ash, self.cedar])
        content = response.content.decode()
        self.assertLess(
            content.index(f'data-known-by-chronicle="{self.ash.pk}"'),
            content.index(f'data-known-by-chronicle="{self.cedar.pk}"'),
        )
        self.assertContains(response, self.cedar.get_absolute_url())
        self.assertContains(
            response,
            f'<a class="tl-row__name tl-row__name--acc" href="'
            f'{reverse("characters:character", kwargs={"pk": self.aurelio.pk})}">Aurelio Brandt</a>',
            html=False,
        )
        self.assertContains(response, "Vampire · mira")
        self.assertContains(response, 'aria-label="Rating 3"')
        self.assertContains(response, 'aria-label="3 of 5"')

    def test_characters_without_a_chronicle_come_last(self):
        Vampire.objects.create(name="Eamon", owner=self.mira, potence=4)
        response = self.get(self.mira)
        groups = response.context["known_by"]["groups"]
        self.assertEqual([group["chronicle"] for group in groups], [self.cedar, None])
        self.assertContains(response, "No chronicle")

    def test_known_by_follows_the_other_sections(self):
        content = self.get(self.mira).content.decode()
        self.assertLess(content.index("Description"), content.index('id="known-by"'))

    def test_list_is_capped(self):
        known = known_by(self.potence, self.staff, limit=2)
        self.assertEqual(known["count"], 2)
        self.assertTrue(known["truncated"])


class KnownByQueryTests(KnownByTestCase):
    def count_queries(self, user):
        cache.clear()
        self.client.force_login(user)
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        return len(queries)

    def test_query_count_stays_flat_as_holders_grow(self):
        few = self.count_queries(self.st)
        for index in range(6):
            owner = User.objects.create_user(f"player{index}", password="pw")
            Vampire.objects.create(
                name=f"Holder {index}", owner=owner, chronicle=self.cedar, potence=2
            )
        self.assertEqual(self.count_queries(self.st), few)
        self.assertEqual(len(self.names(self.client.get(self.url))), 8)

    def test_merit_query_count_stays_flat(self):
        merit = MeritFlaw.objects.create(name="Iron Will")
        url = reverse("characters:meritflaw", kwargs={"pk": merit.pk})
        MeritFlawRating.objects.create(character=self.aurelio, mf=merit, rating=3)
        cache.clear()
        self.client.force_login(self.st)
        with CaptureQueriesContext(connection) as few:
            self.client.get(url)
        for index in range(5):
            human = Human.objects.create(
                name=f"Mortal {index}", owner=self.mira, chronicle=self.cedar
            )
            MeritFlawRating.objects.create(character=human, mf=merit, rating=1)
        cache.clear()
        with CaptureQueriesContext(connection) as many:
            response = self.client.get(url)
        self.assertEqual(len(many), len(few))
        self.assertEqual(len(self.names(response)), 6)


@override_settings(CACHES=LOCMEM)
class KnownByCacheTests(KnownByTestCase):
    """Per-user rows never come from, or go into, a URL-only cache entry."""

    def fetch(self, user=None):
        self.client.logout()
        if user is not None:
            self.client.force_login(user)
        return self.client.get(self.url)

    def test_signed_in_response_varies_on_cookie_and_is_private(self):
        response = self.fetch(self.mira)
        self.assertIn("Cookie", response["Vary"])
        self.assertIn("private", response["Cache-Control"])

    def test_anonymous_response_varies_on_cookie(self):
        response = self.fetch()
        self.assertIn("Cookie", response["Vary"])
        self.assertNotIn("private", response.get("Cache-Control", ""))

    def test_cached_anonymous_page_is_not_served_to_a_signed_in_viewer(self):
        cache.clear()
        self.assertNotContains(self.fetch(), "Aurelio Brandt")
        self.assertContains(self.fetch(self.mira), "Aurelio Brandt")

    def test_a_viewers_page_is_not_served_to_the_next_viewer(self):
        cache.clear()
        self.assertContains(self.fetch(self.mira), "Aurelio Brandt")
        self.assertNotContains(self.fetch(), "Aurelio Brandt")
        response = self.fetch(self.jpark)
        self.assertNotContains(response, "Aurelio Brandt")
        self.assertContains(response, "Bianca")


class KnownBySourceTests(TestCase):
    """Each covered reference type finds its holders."""

    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.user = User.objects.create_user("mira", password="pw")
        self.client.force_login(self.user)

    def names(self, url):
        cache.clear()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        known = response.context["known_by"]
        self.assertIsNotNone(known, url)
        return [(row["name"], row["rating"]) for group in known["groups"] for row in group["rows"]]

    def test_gift_lists_werewolves_without_a_rating(self):
        gift = Gift.objects.create(name="Spirit Speech", rank=1)
        garou = Werewolf.objects.create(name="Aurelio Brandt", owner=self.user)
        garou.gifts.add(gift)
        Werewolf.objects.create(name="Giftless", owner=self.user)
        url = reverse("characters:werewolf:gift", kwargs={"pk": gift.pk})
        self.assertEqual(self.names(url), [("Aurelio Brandt", None)])
        self.assertContains(self.client.get(url), "Werewolf · mira")

    def test_sphere(self):
        forces = Sphere.objects.create(name="Forces", property_name="forces")
        Mage.objects.create(name="Marisol", owner=self.user, arete=3, forces=2)
        url = reverse("characters:mage:sphere", kwargs={"pk": forces.pk})
        self.assertEqual(self.names(url), [("Marisol", 2)])

    def test_lore_matches_its_short_property_name(self):
        flame = Lore.objects.create(name="Lore of Flame", property_name="flame")
        Demon.objects.create(name="Ahrimel", owner=self.user, lore_of_flame=2)
        url = reverse("characters:demon:lore", kwargs={"pk": flame.pk})
        self.assertEqual(self.names(url), [("Ahrimel", 2)])

    def test_edge_matches_its_field_by_name(self):
        edge = Edge.objects.create(name="Discern", virtue="conviction", level=1)
        Hunter.objects.create(name="Ruth", owner=self.user, discern=1)
        url = reverse("characters:hunter:edge", kwargs={"pk": edge.pk})
        self.assertEqual(self.names(url), [("Ruth", 1)])

    def test_arcanos_power_needs_its_level(self):
        argos = Arcanos.objects.create(name="Argos", description="Travel.")
        flicker = Arcanos.objects.create(
            name="Flicker", level=3, parent_arcanos=argos, description="Blink."
        )
        Wraith.objects.create(name="Novice", owner=self.user, argos=2)
        Wraith.objects.create(name="Adept", owner=self.user, argos=3)
        parent_url = reverse("characters:wraith:arcanos", kwargs={"pk": argos.pk})
        power_url = reverse("characters:wraith:arcanos", kwargs={"pk": flicker.pk})
        self.assertEqual(self.names(parent_url), [("Adept", 3), ("Novice", 2)])
        self.assertEqual(self.names(power_url), [("Adept", 3)])

    def test_merit_and_flaw_ratings_show_as_signed_numbers(self):
        flaw = MeritFlaw.objects.create(name="Nightmares")
        human = Human.objects.create(name="Tess", owner=self.user)
        MeritFlawRating.objects.create(character=human, mf=flaw, rating=-2)
        url = reverse("characters:meritflaw", kwargs={"pk": flaw.pk})
        self.assertEqual(self.names(url), [("Tess", -2)])
        self.assertContains(self.client.get(url), 'class="tl-knownby__rating tl-rubric">-2<')

    def test_reference_without_a_source_has_no_section(self):
        clan = VampireClan.objects.create(name="Brujah")
        response = self.client.get(reverse("characters:vampire:clan", kwargs={"pk": clan.pk}))
        self.assertNotContains(response, 'id="known-by"')

    def test_rite_lists_its_holders(self):
        rite = Rite.objects.create(name="Rite of Passage", level=1)
        garou = Werewolf.objects.create(name="Aurelio Brandt", owner=self.user)
        garou.rites_known.add(rite)
        url = reverse("characters:werewolf:rite", kwargs={"pk": rite.pk})
        self.assertEqual(self.names(url), [("Aurelio Brandt", None)])

    def test_demon_ritual_lists_its_holders(self):
        ritual = DemonRitual.objects.create(name="Summon the Storm")
        demon = Demon.objects.create(name="Ahrimel", owner=self.user)
        demon.rituals.add(ritual)
        earthbound = Earthbound.objects.create(name="The Drowned King", owner=self.user)
        earthbound.rituals.add(ritual)
        url = reverse("characters:demon:ritual", kwargs={"pk": ritual.pk})
        self.assertEqual(self.names(url), [("Ahrimel", None), ("The Drowned King", None)])

    def test_thorn_path_and_advantage_ratings(self):
        thorn = Thorn.objects.create(name="Shadow Life")
        wraith = Wraith.objects.create(name="Novice", owner=self.user)
        ThornRating.objects.create(wraith=wraith, thorn=thorn, rating=2)
        path = LinearMagicPath.objects.create(name="Divination")
        sorcerer = Sorcerer.objects.create(name="Hedge", owner=self.user)
        PathRating.objects.create(character=sorcerer, path=path, rating=3)
        advantage = Advantage.objects.create(name="Armor")
        companion = Companion.objects.create(name="Fetch", owner=self.user)
        AdvantageRating.objects.create(character=companion, advantage=advantage, rating=1)
        for route, obj, expected in (
            ("characters:wraith:thorn", thorn, [("Novice", 2)]),
            ("characters:mage:path", path, [("Hedge", 3)]),
            ("characters:mage:advantage", advantage, [("Fetch", 1)]),
        ):
            with self.subTest(route=route):
                self.assertEqual(self.names(reverse(route, kwargs={"pk": obj.pk})), expected)

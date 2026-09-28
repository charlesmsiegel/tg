"""Spend XP (Spread M8): the chained trait selects, the preview and the spend itself."""

from django.contrib.auth.models import User
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.mage.mage import Mage
from characters.models.mage.sphere import Sphere
from game.models import Chronicle, Gameline, ObjectType, STRelationship, XPSpendingRequest
from game.xp_spend import dot_states, rule_text

HTMX = {"HTTP_HX_REQUEST": "true"}


class SpendXPTestBase(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("spender", password="pw")
        self.other = User.objects.create_user("bystander", password="pw")
        self.st = User.objects.create_user("spend_st", password="pw")
        self.staff = User.objects.create_user("spend_staff", password="pw", is_staff=True)
        self.chronicle = Chronicle.objects.create(name="Spending", head_st=self.st)
        STRelationship.objects.create(
            user=self.st, chronicle=self.chronicle, gameline=Gameline.objects.create(name="WoD")
        )
        self.strength = Attribute.objects.create(name="Strength", property_name="strength")
        self.alertness = Ability.objects.create(name="Alertness", property_name="alertness")
        self.character = Human.objects.create(
            name="Spender",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            xp=20,
            strength=2,
            willpower=3,
        )
        self.url = reverse(
            "game:xp_spending_request:create", kwargs={"character_pk": self.character.pk}
        )

    def get(self, query="", user=None, **headers):
        self.client.force_login(user or self.owner)
        return self.client.get(self.url + query, **headers)


class SpendPageTests(SpendXPTestBase):
    def test_page_offers_the_characters_rated_trait_types(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="xp-spend-fields"')
        self.assertContains(response, 'data-tg-expect="xp-spend"')
        values = [value for value, _ in response.context["form"].fields["category"].choices]
        self.assertEqual(values, ["", "Attribute", "Ability", "Background", "Willpower"])
        # Every select asks this page again, with the selection but never the CSRF token.
        self.assertContains(response, f'hx-get="{self.url}"', count=1)
        self.assertContains(response, 'hx-include="#xp-spend-fields"', count=1)
        self.assertContains(response, "game/js/xp-spend.js")
        self.assertContains(response, "vendor/htmx/")

    def test_cover_shows_spent_pending_and_unspent(self):
        XPSpendingRequest.objects.create(
            character=self.character,
            trait_name="Wits",
            trait_type="attribute",
            trait_value=3,
            cost=8,
            approved="Approved",
        )
        XPSpendingRequest.objects.create(
            character=self.character,
            trait_name="Alertness",
            trait_type="ability",
            trait_value=1,
            cost=3,
        )
        response = self.get()
        self.assertEqual(response.context["spent_xp"], 8)
        self.assertEqual(response.context["pending_xp"], 3)
        self.assertInHTML(
            '<div class="tl-bignum"><span class="tl-cover__eyebrow">Pending</span><b>3</b></div>',
            response.content.decode(),
        )
        self.assertInHTML(
            '<div class="tl-bignum"><span class="tl-cover__eyebrow">Unspent</span><b>20</b></div>',
            response.content.decode(),
        )

    def test_history_query_count_does_not_grow(self):
        def count():
            self.client.force_login(self.owner)
            with CaptureQueriesContext(connection) as queries:
                self.assertEqual(self.client.get(self.url).status_code, 200)
            return len(queries)

        XPSpendingRequest.objects.create(
            character=self.character, trait_name="A", trait_type="x", trait_value=1, cost=1
        )
        count()  # warm the per-process caches (content types, reference rows)
        few = count()
        for index in range(6):
            XPSpendingRequest.objects.create(
                character=self.character,
                trait_name=f"T{index}",
                trait_type="x",
                trait_value=1,
                cost=1,
            )
        self.assertEqual(count(), few)

    def test_experience_tab_links_the_owner_to_the_spend_page(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.character.get_absolute_url() + "?tab=experience")
        self.assertContains(response, f'href="{self.url}"')
        self.client.force_login(self.st)
        response = self.client.get(self.character.get_absolute_url() + "?tab=experience")
        self.assertNotContains(response, f'href="{self.url}"')


class ChainingEndpointTests(SpendXPTestBase):
    def test_fragment_lists_the_traits_of_the_chosen_type(self):
        response = self.get("?category=Attribute", **HTMX)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["TG-Fragment"], "xp-spend")
        self.assertIn("HX-Request", response["Vary"])
        body = response.content.decode()
        self.assertNotIn("<html", body)
        self.assertInHTML(f'<option value="{self.strength.pk}">Strength</option>', body)
        self.assertEqual(body.count(f'hx-get="{self.url}"'), 2)
        # An unfinished selection is not an error yet.
        self.assertNotIn("is-invalid", body)
        self.assertNotIn("Choose a trait.", body)
        self.assertIsNone(response.context["preview"])

    def test_unaffordable_traits_are_not_offered(self):
        self.character.xp = 7  # Strength 2 → 3 costs 8
        self.character.save()
        response = self.get("?category=Attribute", **HTMX)
        self.assertNotContains(response, ">Strength<")

    def test_non_owners_get_no_options(self):
        for user, status in ((self.other, 403), (self.st, 403)):
            with self.subTest(user=user.username):
                self.assertEqual(
                    self.get("?category=Attribute", user=user, **HTMX).status_code, status
                )
        self.client.logout()
        self.assertEqual(self.client.get(self.url + "?category=Attribute", **HTMX).status_code, 401)

    def test_staff_may_use_it(self):
        self.assertEqual(self.get("?category=Attribute", user=self.staff, **HTMX).status_code, 200)

    def test_a_stale_trait_does_not_block_a_single_trait_type(self):
        response = self.get(f"?category=Willpower&example={self.strength.pk}", **HTMX)
        preview = response.context["preview"]
        self.assertEqual((preview.current, preview.new, preview.cost), (3, 4, 3))


class PreviewTests(SpendXPTestBase):
    def test_attribute_preview(self):
        response = self.get(f"?category=Attribute&example={self.strength.pk}", **HTMX)
        preview = response.context["preview"]
        self.assertEqual((preview.current, preview.new, preview.cost), (2, 3, 8))
        self.assertEqual(preview.unspent_after, 12)
        self.assertEqual(preview.rule, "Current rating × 4.")
        body = response.content.decode()
        self.assertEqual(body.count('class="tl-dot is-on"'), 2)
        self.assertEqual(body.count('class="tl-dot is-on is-new"'), 1)
        self.assertEqual(body.count('class="tl-dot"'), 2)
        self.assertIn('aria-label="2 to 3 of 5"', body)
        self.assertIn("2 → 3", body)
        self.assertInHTML("<b>8</b>", body)
        self.assertIn("After this request: 12 XP unspent.", body)

    def test_preview_changes_nothing(self):
        self.get(f"?category=Attribute&example={self.strength.pk}", **HTMX)
        self.character.refresh_from_db()
        self.assertEqual(self.character.xp, 20)
        self.assertEqual(self.character.strength, 2)
        self.assertFalse(XPSpendingRequest.objects.exists())

    def test_new_ability_is_a_flat_price(self):
        response = self.get(f"?category=Ability&example={self.alertness.pk}", **HTMX)
        preview = response.context["preview"]
        self.assertEqual((preview.current, preview.new, preview.cost), (0, 1, 3))
        self.assertEqual(preview.rule, "A new trait: a flat price.")

    def test_background_multiplier_comes_from_the_service(self):
        contacts = Background.objects.create(
            name="Contacts", property_name="contacts", multiplier=2
        )
        rating = BackgroundRating.objects.create(char=self.character, bg=contacts, rating=2)
        response = self.get(f"?category=Background&example=br_{rating.pk}", **HTMX)
        preview = response.context["preview"]
        # 3 × current × the background's multiplier, as the XP service charges it.
        self.assertEqual((preview.current, preview.new, preview.cost), (2, 3, 12))
        self.assertContains(response, 'name="note"')

    def test_merit_needs_a_rating_then_prices_the_change(self):
        human_type, _ = ObjectType.objects.get_or_create(
            name="human", defaults={"type": "char", "gameline": "wod"}
        )
        merit = MeritFlaw.objects.create(name="Acute Senses", max_rating=3)
        for value in (1, 2, 3):
            merit.ratings.create(value=value)
        merit.allowed_types.add(human_type)

        response = self.get(f"?category=MeritFlaw&example={merit.pk}", **HTMX)
        self.assertIsNone(response.context["preview"])
        self.assertInHTML('<option value="2">2</option>', response.content.decode())

        response = self.get(f"?category=MeritFlaw&example={merit.pk}&value=2", **HTMX)
        preview = response.context["preview"]
        self.assertEqual((preview.current, preview.new, preview.cost), (0, 2, 6))
        self.assertEqual(preview.rule, "3 XP per point of change.")
        self.assertEqual(preview.dots, ("new", "new", "off", "off", "off"))

    def test_mage_affinity_sphere(self):
        forces = Sphere.objects.create(name="Forces", property_name="forces")
        mage = Mage.objects.create(
            name="Adept",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            arete=3,
            xp=20,
            forces=1,
            affinity_sphere=forces,
        )
        url = reverse("game:xp_spending_request:create", kwargs={"character_pk": mage.pk})
        self.client.force_login(self.owner)
        response = self.client.get(url)
        values = [value for value, _ in response.context["form"].fields["category"].choices]
        self.assertIn("Sphere", values)
        self.assertNotIn("Rote", values)
        response = self.client.get(f"{url}?category=Sphere&example={forces.pk}", **HTMX)
        preview = response.context["preview"]
        self.assertEqual((preview.current, preview.new, preview.cost), (1, 2, 7))
        self.assertEqual(preview.rule, "Current rating × 7.")

    def test_dot_states_and_rules(self):
        self.assertEqual(dot_states(1, 2), ("on", "new", "off", "off", "off"))
        self.assertEqual(len(dot_states(6, 7)), 7)
        self.assertEqual(dot_states(3, 1), ("on", "off", "off", "off", "off"))
        self.assertEqual(dot_states(-2, 0), ())
        self.assertEqual(rule_text("Willpower", 3, 4, 3), "Current rating × 1.")
        self.assertEqual(rule_text("MeritFlaw", -2, 0, 6), "3 XP per point of change.")


class SpendRoundTripTests(SpendXPTestBase):
    def post(self, data, user=None):
        self.client.force_login(user or self.owner)
        return self.client.post(self.url, data)

    def test_spend_files_a_priced_pending_request_and_approval_applies_it(self):
        response = self.post({"category": "Attribute", "example": self.strength.pk})
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        spend = XPSpendingRequest.objects.get(character=self.character)
        self.assertEqual(
            (spend.trait_name, spend.trait_type, spend.trait_value, spend.cost, spend.approved),
            ("Strength", "attribute", 3, 8, "Pending"),
        )
        self.character.refresh_from_db()
        self.assertEqual(self.character.xp, 12)
        page = self.get()
        self.assertEqual(page.context["pending_xp"], 8)
        self.assertContains(page, "Strength")

        self.client.force_login(self.st)
        self.client.post(
            reverse("game:xp_spending_request:approve", kwargs={"pk": spend.pk}),
            {"approved": "Approved"},
        )
        spend.refresh_from_db()
        self.character.refresh_from_db()
        self.assertEqual(spend.approved, "Approved")
        self.assertEqual(self.character.strength, 3)

    def test_preview_button_does_not_spend(self):
        response = self.post({"category": "Attribute", "example": self.strength.pk, "preview": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["preview"].cost, 8)
        self.assertFalse(XPSpendingRequest.objects.exists())

    def test_missing_trait_is_an_error_and_spends_nothing(self):
        response = self.post({"category": "Attribute"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choose a trait.")
        self.assertFalse(XPSpendingRequest.objects.exists())

    def test_a_trait_not_on_offer_is_refused(self):
        self.character.xp = 7
        self.character.save()
        response = self.post({"category": "Attribute", "example": self.strength.pk})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(XPSpendingRequest.objects.exists())
        self.character.refresh_from_db()
        self.assertEqual(self.character.xp, 7)

    def test_non_owner_cannot_spend(self):
        response = self.post({"category": "Willpower"}, user=self.other)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(XPSpendingRequest.objects.exists())

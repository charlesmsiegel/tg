"""Freebie spending record pages: a filed record is paid from the pool; its cost is fixed."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.core.human import Human
from game.models import Chronicle, FreebieSpendingRecord


class FreebieSpendingRecordPagesTests(TestCase):
    def setUp(self):
        self.player = User.objects.create_user("player", password="pw")
        self.char = Human.objects.create(
            name="Draft",
            owner=self.player,
            chronicle=Chronicle.objects.create(name="Ashes"),
            status="Un",
            freebies=15,
        )
        self.create_url = reverse(
            "game:freebie_spending_record:create", kwargs={"character_pk": self.char.pk}
        )
        self.client.force_login(self.player)

    def file(self, cost):
        return self.client.post(
            self.create_url,
            {"trait_name": "Strength", "trait_type": "attribute", "trait_value": 3, "cost": cost},
        )

    def test_filing_deducts_the_cost(self):
        response = self.file(5)
        self.assertRedirects(
            response,
            reverse("game:freebie_spending_record:list"),
            fetch_redirect_response=False,
        )
        record = FreebieSpendingRecord.objects.get(character=self.char)
        self.assertEqual((record.cost, record.approved), (5, "Pending"))
        self.char.refresh_from_db()
        self.assertEqual(self.char.freebies, 10)

    def test_a_cost_over_the_pool_is_refused(self):
        response = self.file(16)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Only 15 freebie points left to spend.", response.context["form"].errors["cost"]
        )
        self.assertFalse(FreebieSpendingRecord.objects.exists())
        self.char.refresh_from_db()
        self.assertEqual(self.char.freebies, 15)

    def test_a_negative_cost_is_refused(self):
        response = self.file(-7)
        self.assertEqual(response.status_code, 200)
        self.assertIn("cost", response.context["form"].errors)
        self.assertFalse(FreebieSpendingRecord.objects.exists())
        self.char.refresh_from_db()
        self.assertEqual(self.char.freebies, 15)

    def test_editing_cannot_change_the_cost(self):
        self.file(5)
        record = FreebieSpendingRecord.objects.get(character=self.char)
        response = self.client.post(
            reverse("game:freebie_spending_record:update", kwargs={"pk": record.pk}),
            {"trait_name": "Dexterity", "trait_type": "attribute", "trait_value": 3, "cost": 0},
        )
        self.assertEqual(response.status_code, 302)
        record.refresh_from_db()
        self.assertEqual((record.trait_name, record.cost), ("Dexterity", 5))
        self.char.refresh_from_db()
        self.assertEqual(self.char.freebies, 10)

    def test_edit_form_has_no_cost_field(self):
        self.file(5)
        record = FreebieSpendingRecord.objects.get(character=self.char)
        response = self.client.get(
            reverse("game:freebie_spending_record:update", kwargs={"pk": record.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("cost", response.context["form"].fields)

    def test_other_players_cannot_file(self):
        self.client.force_login(User.objects.create_user("other", password="pw"))
        self.assertEqual(self.file(1).status_code, 403)
        self.assertFalse(FreebieSpendingRecord.objects.exists())

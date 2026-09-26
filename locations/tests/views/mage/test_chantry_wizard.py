"""The chantry URL routes an unfinished chantry's editor into the creation wizard."""

from django.test import TestCase

from locations.models.mage.chantry import Chantry
from locations.tests.views.mage.chantry_fixtures import add_chantry_actors


class ChantryRoutingTests(TestCase):
    def setUp(self):
        add_chantry_actors(self)
        self.chantry = Chantry.objects.create(
            name="Routed", owner=self.player, chronicle=self.chronicle, total_points=10
        )
        self.url = self.chantry.get_absolute_url()

    def set_state(self, status, creation_status):
        Chantry.objects.filter(pk=self.chantry.pk).update(
            status=status, creation_status=creation_status
        )

    def test_owner_of_a_draft_gets_the_step_for_its_creation_status(self):
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/mage/chantry/locgen.html")
        self.assertTemplateUsed(response, "locations/mage/chantry/point_spend_form.html")
        self.set_state("Un", 2)
        self.assertTemplateUsed(
            self.client.get(self.url), "locations/mage/chantry/effects_form.html"
        )

    def test_returned_chantry_re_enters_the_wizard(self):
        self.set_state("Rev", 1)
        self.client.force_login(self.player)
        self.assertTemplateUsed(
            self.client.get(self.url), "locations/mage/chantry/point_spend_form.html"
        )

    def test_finished_draft_shows_the_detail_page(self):
        self.set_state("Un", 7)
        self.client.force_login(self.player)
        self.assertTemplateUsed(self.client.get(self.url), "locations/mage/chantry/detail.html")

    def test_submitted_and_approved_chantries_show_the_detail_page(self):
        self.client.force_login(self.player)
        for status in ("Sub", "App"):
            with self.subTest(status=status):
                self.set_state(status, 1)
                response = self.client.get(self.url)
                self.assertTemplateUsed(response, "locations/mage/chantry/detail.html")
                self.assertTemplateNotUsed(response, "locations/mage/chantry/locgen.html")

    def test_non_owner_gets_the_public_card_or_404(self):
        self.client.force_login(self.other_st)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/public_object_detail.html")
        self.assertTemplateNotUsed(response, "locations/mage/chantry/locgen.html")
        self.assertEqual(self.client.post(self.url, {}).status_code, 404)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.creation_status, 1)

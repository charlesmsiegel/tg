"""Tests for the Reliquary detail page."""

from django.contrib.auth.models import User
from django.test import TestCase

from locations.models.demon.reliquary import Reliquary


class TestReliquaryDetailDamageBar(TestCase):
    """The Health cell shows a damage bar once the reliquary is damaged."""

    def setUp(self):
        self.staff = User.objects.create_user("staff", "s@test.com", "password", is_staff=True)
        self.client.force_login(self.staff)

    def test_damaged_reliquary_shows_damage_bar(self):
        reliquary = Reliquary.objects.create(
            name="Cracked Idol", max_health_levels=20, current_health_levels=15
        )
        response = self.client.get(reliquary.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "15/20")
        self.assertContains(response, 'class="progress-bar bg-danger"')
        self.assertContains(response, 'aria-valuenow="25.0"')
        self.assertContains(response, "25% damaged")

    def test_undamaged_reliquary_has_no_damage_bar(self):
        reliquary = Reliquary.objects.create(
            name="Pristine Idol", max_health_levels=20, current_health_levels=20
        )
        response = self.client.get(reliquary.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "20/20")
        self.assertNotContains(response, "progress-bar")
        self.assertNotContains(response, "% damaged")


class TestReliquaryDetailPowerHelpText(TestCase):
    """The Pervasiveness/Manifestation cells carry their help sentences
    (formerly only in the deleted orphan health.html include)."""

    def setUp(self):
        self.staff = User.objects.create_user("staff", "s@test.com", "password", is_staff=True)
        self.client.force_login(self.staff)

    def test_pervasiveness_and_manifestation_help_shown_when_true(self):
        reliquary = Reliquary.objects.create(
            name="Aware Idol",
            has_pervasiveness=True,
            has_manifestation=True,
        )
        response = self.client.get(reliquary.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Earthbound can sense everything within this location.")
        self.assertContains(response, "The demon can manifest its apocalyptic form here.")

    def test_help_sentences_hidden_when_power_absent(self):
        reliquary = Reliquary.objects.create(
            name="Inert Idol",
            has_pervasiveness=False,
            has_manifestation=False,
        )
        response = self.client.get(reliquary.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response, "The Earthbound can sense everything within this location."
        )
        self.assertNotContains(response, "The demon can manifest its apocalyptic form here.")

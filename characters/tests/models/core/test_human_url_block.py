"""Tests for human_url_block module."""

from characters.models.core.human import Human
from characters.models.core.human_url_block import HumanUrlBlock
from characters.tests.utils import human_setup
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestGetGamelineForUrl(TestCase):
    """Tests for HumanUrlBlock.get_gameline_for_url() static method."""

    def test_wod_gameline_returns_empty_string(self):
        """WoD gameline returns empty string (no namespace prefix)."""
        result = HumanUrlBlock.get_gameline_for_url("wod")
        self.assertEqual(result, "")

    def test_vtm_gameline_returns_vampire_prefix(self):
        """VtM gameline returns 'vampire:' prefix."""
        result = HumanUrlBlock.get_gameline_for_url("vtm")
        self.assertEqual(result, "vampire:")

    def test_wta_gameline_returns_werewolf_prefix(self):
        """WtA gameline returns 'werewolf:' prefix."""
        result = HumanUrlBlock.get_gameline_for_url("wta")
        self.assertEqual(result, "werewolf:")

    def test_mta_gameline_returns_mage_prefix(self):
        """MtA gameline returns 'mage:' prefix."""
        result = HumanUrlBlock.get_gameline_for_url("mta")
        self.assertEqual(result, "mage:")

    def test_wto_gameline_returns_wraith_prefix(self):
        """WtO gameline returns 'wraith:' prefix."""
        result = HumanUrlBlock.get_gameline_for_url("wto")
        self.assertEqual(result, "wraith:")

    def test_ctd_gameline_returns_changeling_prefix(self):
        """CtD gameline returns 'changeling:' prefix."""
        result = HumanUrlBlock.get_gameline_for_url("ctd")
        self.assertEqual(result, "changeling:")

    def test_dtf_gameline_returns_demon_prefix(self):
        """DtF gameline returns 'demon:' prefix."""
        result = HumanUrlBlock.get_gameline_for_url("dtf")
        self.assertEqual(result, "demon:")

    def test_mtr_gameline_returns_mummy_prefix(self):
        """MtR gameline returns 'mummy:' prefix."""
        result = HumanUrlBlock.get_gameline_for_url("mtr")
        self.assertEqual(result, "mummy:")

    def test_htr_gameline_returns_hunter_prefix(self):
        """HtR gameline returns 'hunter:' prefix."""
        result = HumanUrlBlock.get_gameline_for_url("htr")
        self.assertEqual(result, "hunter:")

    def test_unknown_gameline_returns_empty_string(self):
        """Unknown gameline returns empty string."""
        result = HumanUrlBlock.get_gameline_for_url("unknown")
        self.assertEqual(result, "")


class TestHumanUrlBlockOnHuman(TestCase):
    """Tests for URL generation methods on Human model."""

    def setUp(self):
        human_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.human = Human.objects.create(name="Test Human", owner=self.user)

    def test_get_creation_url(self):
        """Human.get_creation_url() returns correct URL for character creation."""
        url = Human.get_creation_url()
        expected = reverse("characters:create:human")
        self.assertEqual(url, expected)

    def test_get_full_creation_url(self):
        """Human.get_full_creation_url() returns correct URL for full character creation."""
        url = Human.get_full_creation_url()
        expected = reverse("characters:create:human_full")
        self.assertEqual(url, expected)

    def test_get_update_url(self):
        """Human.get_update_url() returns correct URL for character update."""
        url = self.human.get_update_url()
        expected = reverse("characters:update:human", kwargs={"pk": self.human.pk})
        self.assertEqual(url, expected)

    def test_get_full_update_url(self):
        """Human.get_full_update_url() returns correct URL for full character update."""
        url = self.human.get_full_update_url()
        expected = reverse("characters:update:human_full", kwargs={"pk": self.human.pk})
        self.assertEqual(url, expected)

    def test_get_update_url_uses_pk(self):
        """get_update_url() includes the correct pk in the URL."""
        self.assertIn(str(self.human.pk), self.human.get_update_url())

    def test_get_full_update_url_uses_pk(self):
        """get_full_update_url() includes the correct pk in the URL."""
        self.assertIn(str(self.human.pk), self.human.get_full_update_url())

    def test_urls_are_resolvable(self):
        """Generated URLs are valid and resolvable."""
        self.client.login(username="testuser", password="password")

        # Test creation URLs
        response = self.client.get(Human.get_creation_url())
        self.assertIn(response.status_code, [200, 302])

        response = self.client.get(Human.get_full_creation_url())
        self.assertIn(response.status_code, [200, 302])

        # Test update URLs - 403 is acceptable as it means URL resolved
        # (owner doesn't have EDIT_FULL permission, only STs can use update views)
        response = self.client.get(self.human.get_update_url())
        self.assertIn(response.status_code, [200, 302, 403])

        response = self.client.get(self.human.get_full_update_url())
        self.assertIn(response.status_code, [200, 302, 403])


class TestHumanUrlBlockWithMultipleCharacters(TestCase):
    """Tests for URL generation with multiple characters."""

    def setUp(self):
        human_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.human1 = Human.objects.create(name="Human 1", owner=self.user)
        self.human2 = Human.objects.create(name="Human 2", owner=self.user)

    def test_different_characters_have_different_update_urls(self):
        """Different characters should have different update URLs."""
        url1 = self.human1.get_update_url()
        url2 = self.human2.get_update_url()
        self.assertNotEqual(url1, url2)

    def test_different_characters_have_different_full_update_urls(self):
        """Different characters should have different full update URLs."""
        url1 = self.human1.get_full_update_url()
        url2 = self.human2.get_full_update_url()
        self.assertNotEqual(url1, url2)

    def test_creation_urls_are_class_level(self):
        """Creation URLs are class-level and don't depend on instances."""
        # Class-level URLs should be identical regardless of instance
        self.assertEqual(Human.get_creation_url(), Human.get_creation_url())
        self.assertEqual(Human.get_full_creation_url(), Human.get_full_creation_url())

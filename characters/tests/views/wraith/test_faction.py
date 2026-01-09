"""Tests for WraithFaction views."""

from characters.models.wraith.faction import WraithFaction
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestWraithFactionDetailView(TestCase):
    """Test WraithFactionDetailView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.faction = WraithFaction.objects.create(
            name="The Iron Legion",
            description="Warriors of the Underworld",
            faction_type="legion",
            owner=self.user,
        )

    def test_detail_view_accessible_when_logged_in(self):
        """Test that faction detail view is accessible when logged in."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.faction.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.faction.get_absolute_url())
        self.assertTemplateUsed(response, "characters/wraith/faction/detail.html")

    def test_detail_view_shows_subfactions(self):
        """Test that detail view shows subfactions if they exist."""
        subfaction = WraithFaction.objects.create(
            name="Subfaction",
            faction_type="legion",
            parent=self.faction,
            owner=self.user,
        )
        self.client.login(username="user", password="password")
        response = self.client.get(self.faction.get_absolute_url())
        self.assertContains(response, "Subfaction")


class TestWraithFactionListView(TestCase):
    """Test WraithFactionListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_list_view_accessible_when_logged_in(self):
        """Test that faction list view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:list:faction")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_factions(self):
        """Test that list view shows factions."""
        faction = WraithFaction.objects.create(
            name="Silent Legion", faction_type="legion", owner=self.user
        )
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:list:faction")
        response = self.client.get(url)
        self.assertContains(response, "Silent Legion")


class TestWraithFactionCreateView(TestCase):
    """Test WraithFactionCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_create_view_accessible(self):
        """Test that faction create view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:create:faction")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:create:faction")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/faction/form.html")

    def test_create_faction_successfully(self):
        """Test creating a faction successfully."""
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:create:faction")
        data = {
            "name": "New Legion",
            "description": "A new faction",
            "faction_type": "legion",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(WraithFaction.objects.filter(name="New Legion").exists())


class TestWraithFactionUpdateView(TestCase):
    """Test WraithFactionUpdateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.faction = WraithFaction.objects.create(
            name="Iron Legion", faction_type="legion", owner=self.user
        )

    def test_update_view_accessible(self):
        """Test that faction update view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = self.faction.get_update_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        url = self.faction.get_update_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/faction/form.html")

    def test_update_faction_successfully(self):
        """Test updating a faction successfully."""
        self.client.login(username="user", password="password")
        url = self.faction.get_update_url()
        data = {
            "name": "Updated Legion",
            "description": "Updated description",
            "faction_type": "heretic",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.faction.refresh_from_db()
        self.assertEqual(self.faction.name, "Updated Legion")


class TestWraithFaction404Handling(TestCase):
    """Test 404 error handling for faction views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_faction_detail_returns_404_for_invalid_pk(self):
        """Test that faction detail returns 404 for non-existent faction."""
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("characters:wraith:faction", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_faction_update_returns_404_for_invalid_pk(self):
        """Test that faction update returns 404 for non-existent faction."""
        self.client.login(username="user", password="password")
        response = self.client.get(
            reverse("characters:wraith:update:faction", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

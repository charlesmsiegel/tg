"""Tests for ApocalypticFormTrait views."""

from characters.models.demon.apocalyptic_form import ApocalypticFormTrait
from characters.models.demon.house import DemonHouse
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestApocalypticFormTraitDetailView(TestCase):
    """Test ApocalypticFormTraitDetailView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", owner=self.user
        )
        self.trait = ApocalypticFormTrait.objects.create(
            name="Enhanced Senses",
            description="Your senses are sharpened.",
            cost=1,
            house=self.house,
            owner=self.user,
        )

    def test_detail_view_accessible_when_logged_in(self):
        """Test that trait detail view is accessible when logged in."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.trait.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.trait.get_absolute_url())
        self.assertTemplateUsed(response, "characters/demon/apocalyptic_trait/detail.html")


class TestApocalypticFormTraitListView(TestCase):
    """Test ApocalypticFormTraitListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_list_view_accessible_when_logged_in(self):
        """Test that trait list view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:apocalyptic_trait")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_traits(self):
        """Test that list view shows traits."""
        trait = ApocalypticFormTrait.objects.create(name="Wings", cost=2, owner=self.user)
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:apocalyptic_trait")
        response = self.client.get(url)
        self.assertContains(response, "Wings")

    def test_list_view_uses_select_related(self):
        """Test that get_queryset uses select_related for house."""
        from characters.views.demon.apocalyptic_trait import (
            ApocalypticFormTraitListView,
        )

        view = ApocalypticFormTraitListView()
        view.request = None
        queryset = view.get_queryset()
        # Check that select_related is used
        self.assertIn("house", str(queryset.query).lower())


class TestApocalypticFormTraitCreateView(TestCase):
    """Test ApocalypticFormTraitCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_create_view_requires_login(self):
        """Test that create view requires login."""
        url = reverse("characters:demon:create:apocalyptic_trait")
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 401, 403])

    def test_create_view_accessible_when_logged_in(self):
        """Test that trait create view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:create:apocalyptic_trait")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:create:apocalyptic_trait")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/demon/apocalyptic_trait/form.html")

    def test_create_trait_successfully(self):
        """Test creating a trait successfully."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:create:apocalyptic_trait")
        data = {
            "name": "Claws",
            "description": "Sharp claws for combat.",
            "cost": 2,
            "high_torment_only": False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ApocalypticFormTrait.objects.filter(name="Claws").exists())


class TestApocalypticFormTraitUpdateView(TestCase):
    """Test ApocalypticFormTraitUpdateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.trait = ApocalypticFormTrait.objects.create(name="Wings", cost=2, owner=self.user)

    def test_update_view_requires_login(self):
        """Test that update view requires login."""
        url = self.trait.get_update_url()
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 401, 403])

    def test_update_view_accessible_when_logged_in(self):
        """Test that trait update view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = self.trait.get_update_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        url = self.trait.get_update_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/demon/apocalyptic_trait/form.html")

    def test_update_trait_successfully(self):
        """Test updating a trait successfully."""
        self.client.login(username="user", password="password")
        url = self.trait.get_update_url()
        data = {
            "name": "Updated Wings",
            "description": "Updated description.",
            "cost": 3,
            "high_torment_only": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.trait.refresh_from_db()
        self.assertEqual(self.trait.name, "Updated Wings")


class TestApocalypticFormTrait404Handling(TestCase):
    """Test 404 error handling for trait views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_trait_detail_returns_404_for_invalid_pk(self):
        """Test that trait detail returns 404 for non-existent trait."""
        self.client.login(username="user", password="password")
        response = self.client.get(
            reverse("characters:demon:apocalyptic_trait", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_trait_update_returns_404_for_invalid_pk(self):
        """Test that trait update returns 404 for non-existent trait."""
        self.client.login(username="user", password="password")
        response = self.client.get(
            reverse("characters:demon:update:apocalyptic_trait", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

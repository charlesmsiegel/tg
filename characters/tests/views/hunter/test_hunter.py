"""Tests for Hunter views."""

from characters.forms.core.limited_edit import LimitedHunterEditForm
from characters.models.hunter import Hunter
from characters.models.hunter.creed import Creed
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from game.models import Chronicle


class TestHunterDetailView(TestCase):
    """Test the Hunter detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player", password="password")
        self.creed = Creed.objects.create(name="Avenger", primary_virtue="zeal")
        self.hunter = Hunter.objects.create(
            name="Test Hunter",
            owner=self.player,
            creed=self.creed,
            discern=2,
            illuminate=1,
        )
        self.url = self.hunter.get_absolute_url()

    def test_detail_view_status_code(self):
        """Owner can view their own character."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Detail view uses correct template."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/hunter/hunter/detail.html")

    def test_detail_view_edges_context(self):
        """Detail view includes edges in context."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)

        self.assertIn("edges", response.context)
        edges = response.context["edges"]
        self.assertEqual(edges["conviction"]["discern"], 2)
        self.assertEqual(edges["vision"]["illuminate"], 1)
        self.assertEqual(edges["zeal"], {})  # No zeal edges set


class TestHunterCreateView(TestCase):
    """Test the Hunter create view."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player", password="password")
        self.url = reverse("characters:hunter:create:hunter")

    def test_create_view_status_code(self):
        """Logged in user can access create view."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Create view uses correct template."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/hunter/hunter/form.html")

    def test_create_view_url_resolves(self):
        """Create view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/hunter/create/hunter/")


class TestHunterUpdateView(TestCase):
    """Test the Hunter update view with permission checks."""

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.other_user = User.objects.create_user(username="other", password="password")
        self.st = User.objects.create_user(username="st", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.hunter = Hunter.objects.create(
            name="Test Hunter", owner=self.owner, chronicle=self.chronicle
        )
        self.url = reverse("characters:hunter:update:hunter", args=[self.hunter.id])

    def test_st_can_access_update_view(self):
        """ST should be able to access update view with full form."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].fields)

    def test_owner_gets_limited_form(self):
        """Owner should get limited form when character is approved."""
        self.hunter.status = "App"  # Approved status
        self.hunter.save()
        self.client.login(username="owner", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Limited form should be used
        self.assertIsInstance(response.context["form"], LimitedHunterEditForm)

    def test_other_user_cannot_access(self):
        """Non-owner/non-ST should not be able to access update view."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_view_template(self):
        """Update view uses correct template."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/hunter/hunter/form.html")


class TestHunterListView(TestCase):
    """Test the Hunter list view."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player", password="password")
        self.creed = Creed.objects.create(name="Judge", primary_virtue="conviction")
        self.url = reverse("characters:hunter:list:hunter")

    def test_list_url_resolves(self):
        """List view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/hunter/list/hunter/")

    def test_list_view_status_code(self):
        """List view is accessible."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """List view uses correct template."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/hunter/hunter/list.html")

    def test_list_view_queryset_ordering(self):
        """List view orders by name and includes related objects."""
        Hunter.objects.create(
            name="Zebra Hunter", owner=self.player, creed=self.creed
        )
        Hunter.objects.create(
            name="Alpha Hunter", owner=self.player, creed=self.creed
        )

        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)

        hunters = list(response.context["hunters"])
        self.assertEqual(hunters[0].name, "Alpha Hunter")
        self.assertEqual(hunters[1].name, "Zebra Hunter")

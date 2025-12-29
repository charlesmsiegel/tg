"""Tests for MtRHuman views."""

from characters.forms.core.limited_edit import LimitedMtRHumanEditForm
from characters.models.mummy.mtr_human import MtRHuman
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from game.models import Chronicle


class TestMtRHumanDetailView(TestCase):
    """Test the MtRHuman detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player", password="password")
        self.human = MtRHuman.objects.create(name="Test Human", owner=self.player)
        self.url = self.human.get_absolute_url()

    def test_detail_view_status_code(self):
        """Owner can view their own character."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Detail view uses correct template."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/mtrhuman/detail.html")


class TestMtRHumanCreateView(TestCase):
    """Test the MtRHuman create view."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player", password="password")
        self.url = reverse("characters:mummy:create:mtrhuman")

    def test_create_view_status_code(self):
        """Logged in user can access create view."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Create view uses correct template."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/mtrhuman/form.html")

    def test_create_view_form_has_user(self):
        """Create view passes user to form."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.context["form"].user, self.player)

    def test_create_view_url_resolves(self):
        """Create view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/mummy/create/mtrhuman/")


class TestMtRHumanUpdateView(TestCase):
    """Test the MtRHuman update view with permission checks."""

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.other_user = User.objects.create_user(username="other", password="password")
        self.st = User.objects.create_user(username="st", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.human = MtRHuman.objects.create(
            name="Test Human", owner=self.owner, chronicle=self.chronicle
        )
        self.url = reverse("characters:mummy:update:mtrhuman", args=[self.human.id])

    def test_st_can_access_update_view(self):
        """ST should be able to access update view with full form."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].fields)

    def test_owner_gets_limited_form(self):
        """Owner should get limited form when character is approved."""
        self.human.status = "App"  # Approved status
        self.human.save()
        self.client.login(username="owner", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Limited form should be used
        self.assertIsInstance(response.context["form"], LimitedMtRHumanEditForm)

    def test_other_user_cannot_access(self):
        """Non-owner/non-ST should not be able to access update view."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_view_template(self):
        """Update view uses correct template."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/mtrhuman/form.html")


class TestMtRHumanListView(TestCase):
    """Test the MtRHuman list view."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player", password="password")
        self.url = reverse("characters:mummy:list:mtrhuman")

    def test_list_url_resolves(self):
        """List view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/mummy/list/mtrhuman/")

    def test_list_view_status_code(self):
        """List view is accessible."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """List view uses correct template."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/mtrhuman/list.html")

    def test_list_view_queryset_ordering(self):
        """List view orders by name and includes related objects."""
        MtRHuman.objects.create(name="Zebra Human", owner=self.player)
        MtRHuman.objects.create(name="Alpha Human", owner=self.player)

        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)

        humans = list(response.context["humans"])
        self.assertEqual(humans[0].name, "Alpha Human")
        self.assertEqual(humans[1].name, "Zebra Human")

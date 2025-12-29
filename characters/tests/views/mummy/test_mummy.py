"""Tests for Mummy views."""

from characters.forms.core.limited_edit import LimitedMummyEditForm
from characters.models.mummy.dynasty import Dynasty
from characters.models.mummy.mummy import Mummy
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from game.models import Chronicle


class TestMummyDetailView(TestCase):
    """Test the Mummy detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player", password="password")
        self.dynasty = Dynasty.objects.create(
            name="Test Dynasty", era="Middle Kingdom"
        )
        self.mummy = Mummy.objects.create(
            name="Test Mummy",
            owner=self.player,
            dynasty=self.dynasty,
            alchemy=3,
            necromancy=2,
        )
        self.url = self.mummy.get_absolute_url()

    def test_detail_view_status_code(self):
        """Owner can view their own character."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Detail view uses correct template."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/mummy/detail.html")

    def test_detail_view_hekau_context(self):
        """Detail view includes hekau in context."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)

        self.assertIn("hekau", response.context)
        hekau = response.context["hekau"]
        self.assertEqual(hekau["Alchemy"], 3)
        self.assertEqual(hekau["Necromancy"], 2)
        self.assertNotIn("Celestial", hekau)  # No celestial set

    def test_detail_view_dynasty_context(self):
        """Detail view includes dynasty in context."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)

        self.assertIn("dynasty", response.context)
        self.assertEqual(response.context["dynasty"], self.dynasty)

    def test_detail_view_without_dynasty(self):
        """Detail view works without a dynasty."""
        mummy_no_dynasty = Mummy.objects.create(
            name="No Dynasty Mummy",
            owner=self.player,
        )
        self.client.login(username="Player", password="password")
        response = self.client.get(mummy_no_dynasty.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("dynasty", response.context)


class TestMummyCreateView(TestCase):
    """Test the Mummy create view."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player", password="password")
        self.url = reverse("characters:mummy:create:mummy")

    def test_create_view_status_code(self):
        """Logged in user can access create view."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Create view uses correct template."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/mummy/form.html")

    def test_create_view_form_has_user(self):
        """Create view passes user to form."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.context["form"].user, self.player)

    def test_create_view_url_resolves(self):
        """Create view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/mummy/create/mummy/")


class TestMummyUpdateView(TestCase):
    """Test the Mummy update view with permission checks."""

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.other_user = User.objects.create_user(username="other", password="password")
        self.st = User.objects.create_user(username="st", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.mummy = Mummy.objects.create(
            name="Test Mummy", owner=self.owner, chronicle=self.chronicle
        )
        self.url = reverse("characters:mummy:update:mummy", args=[self.mummy.id])

    def test_st_can_access_update_view(self):
        """ST should be able to access update view with full form."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].fields)

    def test_owner_gets_limited_form(self):
        """Owner should get limited form when character is approved."""
        self.mummy.status = "App"  # Approved status
        self.mummy.save()
        self.client.login(username="owner", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Limited form should be used
        self.assertIsInstance(response.context["form"], LimitedMummyEditForm)

    def test_other_user_cannot_access(self):
        """Non-owner/non-ST should not be able to access update view."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_view_template(self):
        """Update view uses correct template."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/mummy/form.html")


class TestMummyListView(TestCase):
    """Test the Mummy list view."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player", password="password")
        self.dynasty = Dynasty.objects.create(name="Test Dynasty")
        self.url = reverse("characters:mummy:list:mummy")

    def test_list_url_resolves(self):
        """List view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/mummy/list/mummy/")

    def test_list_view_status_code(self):
        """List view is accessible."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """List view uses correct template."""
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/mummy/list.html")

    def test_list_view_queryset_ordering(self):
        """List view orders by name and includes related objects."""
        Mummy.objects.create(
            name="Zebra Mummy", owner=self.player, dynasty=self.dynasty
        )
        Mummy.objects.create(
            name="Alpha Mummy", owner=self.player, dynasty=self.dynasty
        )

        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)

        mummies = list(response.context["mummies"])
        self.assertEqual(mummies[0].name, "Alpha Mummy")
        self.assertEqual(mummies[1].name, "Zebra Mummy")

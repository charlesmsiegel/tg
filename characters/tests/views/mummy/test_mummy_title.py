"""Tests for MummyTitle views."""

from characters.models.mummy.mummy_title import MummyTitle
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestMummyTitleDetailView(TestCase):
    """Test the MummyTitle detail view."""

    def setUp(self):
        self.title = MummyTitle.objects.create(
            name="Test Title",
            rank_level=3,
            description="A test title",
        )
        self.url = self.title.get_absolute_url()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )

    def test_detail_view_requires_auth(self):
        """MummyTitle detail view requires authentication."""
        response = self.client.get(self.url)
        # Should redirect to login or return unauthorized
        self.assertIn(response.status_code, [302, 401, 403])

    def test_detail_view_status_code(self):
        """MummyTitle detail view is accessible when authenticated."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Detail view uses correct template."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/title/detail.html")


class TestMummyTitleCreateView(TestCase):
    """Test the MummyTitle create view."""

    def setUp(self):
        self.url = reverse("characters:mummy:create:title")
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )

    def test_create_view_status_code(self):
        """Create view is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/title/form.html")

    def test_create_view_url_resolves(self):
        """Create view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/mummy/create/title/")

    def test_create_view_success_url(self):
        """Create view redirects to title detail after successful creation."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            self.url,
            data={
                "name": "New Title",
                "rank_level": 5,
                "description": "A newly created title",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        title = MummyTitle.objects.get(name="New Title")
        self.assertEqual(response.redirect_chain[-1][0], title.get_absolute_url())


class TestMummyTitleUpdateView(TestCase):
    """Test the MummyTitle update view."""

    def setUp(self):
        self.title = MummyTitle.objects.create(
            name="Test Title",
            rank_level=3,
        )
        self.url = reverse("characters:mummy:update:title", args=[self.title.id])

    def test_update_view_status_code(self):
        """Update view is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/title/form.html")


class TestMummyTitleListView(TestCase):
    """Test the MummyTitle list view."""

    def setUp(self):
        self.url = reverse("characters:mummy:list:title")

    def test_list_url_resolves(self):
        """List view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/mummy/list/title/")

    def test_list_view_status_code(self):
        """List view is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """List view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/title/list.html")

    def test_list_view_queryset_ordering(self):
        """List view orders by rank_level, then name."""
        MummyTitle.objects.create(name="Zebra Title", rank_level=1)
        MummyTitle.objects.create(name="Alpha Title", rank_level=3)
        MummyTitle.objects.create(name="Beta Title", rank_level=1)

        response = self.client.get(self.url)

        titles = list(response.context["mummytitle_list"])
        # Ordered by rank_level first, then name
        self.assertEqual(titles[0].name, "Beta Title")  # rank 1
        self.assertEqual(titles[1].name, "Zebra Title")  # rank 1
        self.assertEqual(titles[2].name, "Alpha Title")  # rank 3

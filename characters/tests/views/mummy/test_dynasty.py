"""Tests for Dynasty views."""

from django.test import TestCase
from django.urls import reverse

from characters.models.mummy.dynasty import Dynasty


class TestDynastyDetailView(TestCase):
    """Test the Dynasty detail view."""

    def setUp(self):
        self.dynasty = Dynasty.objects.create(
            name="Test Dynasty",
            era="Middle Kingdom",
            description="A test dynasty",
        )
        self.url = self.dynasty.get_absolute_url()

    def test_detail_view_status_code(self):
        """Dynasty detail view is publicly accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/dynasty/detail.html")


class TestDynastyCreateView(TestCase):
    """Test the Dynasty create view."""

    def setUp(self):
        self.url = reverse("characters:mummy:create:dynasty")

    def test_create_view_status_code(self):
        """Create view is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/dynasty/form.html")

    def test_create_view_url_resolves(self):
        """Create view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/mummy/create/dynasty/")

    def test_create_view_success_url(self):
        """Create view redirects to dynasty detail after successful creation."""
        response = self.client.post(
            self.url,
            data={
                "name": "New Dynasty",
                "era": "New Kingdom",
                "description": "A newly created dynasty",
                "favored_hekau": "alchemy",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        dynasty = Dynasty.objects.get(name="New Dynasty")
        self.assertEqual(response.redirect_chain[-1][0], dynasty.get_absolute_url())


class TestDynastyUpdateView(TestCase):
    """Test the Dynasty update view."""

    def setUp(self):
        self.dynasty = Dynasty.objects.create(
            name="Test Dynasty",
            era="Middle Kingdom",
        )
        self.url = reverse("characters:mummy:update:dynasty", args=[self.dynasty.id])

    def test_update_view_status_code(self):
        """Update view is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/dynasty/form.html")


class TestDynastyListView(TestCase):
    """Test the Dynasty list view."""

    def setUp(self):
        self.url = reverse("characters:mummy:list:dynasty")

    def test_list_url_resolves(self):
        """List view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/mummy/list/dynasty/")

    def test_list_view_status_code(self):
        """List view is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """List view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/dynasty/list.html")

    def test_list_view_queryset_ordering(self):
        """List view orders by name."""
        Dynasty.objects.create(name="Zebra Dynasty")
        Dynasty.objects.create(name="Alpha Dynasty")

        response = self.client.get(self.url)

        dynasties = list(response.context["dynasty_list"])
        self.assertEqual(dynasties[0].name, "Alpha Dynasty")
        self.assertEqual(dynasties[1].name, "Zebra Dynasty")

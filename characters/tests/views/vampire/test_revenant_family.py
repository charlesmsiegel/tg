"""Tests for the RevenantFamily views."""

from django.test import TestCase
from django.urls import reverse

from characters.models.vampire.revenant import RevenantFamily


class TestRevenantFamilyListView(TestCase):
    """The revenant family list is public reference data like the clan list."""

    def setUp(self):
        RevenantFamily.objects.create(name="Zantosa")
        RevenantFamily.objects.create(name="Bratovich")
        self.url = reverse("characters:vampire:list:revenant_family")

    def test_list_url_resolves(self):
        self.assertEqual(self.url, "/characters/vampire/list/revenant_family/")

    def test_list_is_public(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/vampire/revenant_family/list.html")

    def test_list_shows_families_in_name_order(self):
        response = self.client.get(self.url)
        self.assertEqual(
            [family.name for family in response.context["object_list"]],
            ["Bratovich", "Zantosa"],
        )
        self.assertContains(response, "Zantosa")

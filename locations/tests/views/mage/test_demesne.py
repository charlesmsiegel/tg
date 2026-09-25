"""Tests for the Demesne create and update pages."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from locations.models.mage.demesne import Demesne


class DemesneFormPagesTest(TestCase):
    """The shared form include used to load the uninstalled widget_tweaks library (500)."""

    def setUp(self):
        self.user = User.objects.create_user("demesne_owner", password="pw-12345")
        self.client.force_login(self.user)

    def test_create_page_renders(self):
        response = self.client.get(reverse("locations:mage:create:demesne"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/mage/demesne/form_include.html")
        self.assertContains(response, 'name="rank"')

    def test_owner_update_page_renders_while_unfinished(self):
        demesne = Demesne.objects.create(name="Quiet Garden", owner=self.user, status="Un")

        response = self.client.get(
            reverse("locations:mage:update:demesne", kwargs={"pk": demesne.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/mage/demesne/form_include.html")
        self.assertContains(response, "Quiet Garden")

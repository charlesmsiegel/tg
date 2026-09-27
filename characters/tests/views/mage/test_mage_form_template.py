"""The Mage create/edit template reads model data from the object, not the form."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.core.specialty import Specialty
from characters.models.mage.faction import MageFaction
from characters.models.mage.mage import Mage


class MageFormTemplateTest(TestCase):
    def setUp(self):
        self.st = User.objects.create_superuser("st", "st@example.com", "pw")
        self.client.force_login(self.st)

    def edit(self, mage):
        return self.client.get(reverse("characters:mage:update:mage_full", kwargs={"pk": mage.pk}))

    def test_technocracy_labels_follow_the_affiliation(self):
        union = MageFaction.objects.create(name="Technocratic Union")
        mage = Mage.objects.create(name="Agent", owner=self.st, affiliation=union)
        response = self.edit(mage)
        self.assertContains(response, "Cloaking")
        self.assertContains(response, "Laboratory")
        self.assertNotContains(response, ">Sanctum<")

    def test_traditions_keep_the_default_labels(self):
        mage = Mage.objects.create(name="Hermetic", owner=self.st)
        response = self.edit(mage)
        self.assertContains(response, "Sanctum")
        self.assertNotContains(response, "Laboratory")

    def test_ability_rows_show_specialties(self):
        mage = Mage.objects.create(name="Seer", owner=self.st, alertness=4)
        mage.specialties.add(Specialty.objects.create(name="Keen Ears", stat="alertness"))
        response = self.edit(mage)
        self.assertEqual(len(response.context["ability_rows"]), 11)
        self.assertContains(response, "(Keen Ears)")

    def test_create_page_renders_without_an_object(self):
        response = self.client.get(reverse("characters:mage:create:mage_full"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["technocratic"])

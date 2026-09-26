"""The Mage chargen template renders Chantry at step 20 and Specialties at 21."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.background_block import Background, BackgroundRating
from characters.models.mage.mage import Mage


class TestMageChargenTemplateNumbering(TestCase):
    """The Mage template renders Chantry at 20 and Specialties at 21."""

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.client.login(username="owner", password="password")

    def test_chantry_block_not_rendered_at_mentor_step(self):
        mentor_bg, _ = Background.objects.get_or_create(
            property_name="mentor", defaults={"name": "Mentor"}
        )
        mage = Mage.objects.create(
            name="Mentor Step Mage", owner=self.owner, creation_status=17, arete=1
        )
        BackgroundRating.objects.create(char=mage, bg=mentor_bg, rating=1)
        response = self.client.get(mage.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Chantry Background")

    def test_specialties_block_rendered_at_step_21(self):
        mage = Mage.objects.create(
            name="Specialty Step Mage", owner=self.owner, creation_status=21, arete=1
        )
        response = self.client.get(mage.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choose Specialties")

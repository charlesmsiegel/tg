"""Tests that chargen pages render the client-side validation hooks."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.human import Human
from characters.tests.utils import human_setup


class TestChargenValidationRendering(TestCase):
    """The validation include and shared utilities must reach the page."""

    def setUp(self):
        human_setup()
        self.owner = User.objects.create_user(username="owner", password="password")

    def test_abilities_step_renders_validation(self):
        char = Human.objects.create(
            name="Ability Human", owner=self.owner, creation_status=2
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(char.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "abilities-validation-status")
        self.assertContains(response, "TG.validation")

    def test_backgrounds_step_renders_validation(self):
        # The plain-Human step 3 template (core/human/chargen.html) has no
        # backgrounds block (pre-existing gap), so exercise a flow whose
        # template includes background_block/form.html: the Wraith human.
        from characters.models.wraith.wtohuman import WtOHuman

        char = WtOHuman.objects.create(
            name="Background Human", owner=self.owner, creation_status=3
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(char.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "backgrounds-validation-status")
        self.assertContains(response, "TG.validation")

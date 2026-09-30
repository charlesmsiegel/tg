"""The template picker is reachable between Basics and step 1 (U14)."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.core.archetype import Archetype
from characters.models.mage.mtahuman import MtAHuman
from characters.views.mage.mtahuman import CharacterTemplateSelectionForm
from core.models import CharacterTemplate


class TemplateSelectionFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="player", password="password")
        cls.other = User.objects.create_user(username="other", password="password")
        cls.archetype = Archetype.objects.create(name="Visionary")
        # As populate_db seeds it: official and public, status left at the default.
        cls.seeded = CharacterTemplate.objects.create(
            name="Hedge Scholar",
            gameline="mta",
            character_type="mage",
            attributes={"intelligence": 4},
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_basics_leads_to_the_template_picker(self):
        response = self.client.post(
            reverse("characters:mage:create:mta_human"),
            {
                "name": "Newcomer",
                "nature": self.archetype.pk,
                "demeanor": self.archetype.pk,
                "concept": "Student",
            },
        )
        character = MtAHuman.objects.get(name="Newcomer")
        picker = reverse("characters:mage:mtahuman_template", kwargs={"pk": character.pk})
        self.assertRedirects(response, picker, fetch_redirect_response=False)
        self.assertEqual(character.creation_status, 0)

        response = self.client.get(picker)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.seeded, response.context["available_templates"])

        response = self.client.post(picker, {"template": self.seeded.pk})
        self.assertEqual(response.status_code, 302)
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 1)
        self.assertEqual(character.intelligence, 4)

    def test_router_sends_an_unstarted_owner_back_to_the_picker(self):
        character = MtAHuman.objects.create(name="Paused", owner=self.user, creation_status=0)
        response = self.client.get(character.get_absolute_url())
        self.assertRedirects(
            response,
            reverse("characters:mage:mtahuman_template", kwargs={"pk": character.pk}),
            fetch_redirect_response=False,
        )

    def test_router_does_not_send_others_to_the_picker(self):
        character = MtAHuman.objects.create(name="Paused", owner=self.user, creation_status=0)
        self.client.force_login(self.other)
        response = self.client.get(character.get_absolute_url())
        self.assertNotIn("/template/", response.get("Location", ""))

    def test_picker_denies_another_user(self):
        character = MtAHuman.objects.create(name="Paused", owner=self.user, creation_status=0)
        self.client.force_login(self.other)
        response = self.client.get(
            reverse("characters:mage:mtahuman_template", kwargs={"pk": character.pk})
        )
        self.assertEqual(response.status_code, 404)


class TemplateSelectionFormTests(TestCase):
    def test_offers_approved_and_official_templates_only(self):
        owner = User.objects.create_user(username="author")
        character = MtAHuman.objects.create(name="Chooser", owner=owner)
        common = {"gameline": "mta", "character_type": "mage"}
        seeded = CharacterTemplate.objects.create(name="Seeded", **common)
        approved = CharacterTemplate.objects.create(
            name="Approved", is_official=False, status="App", **common
        )
        CharacterTemplate.objects.create(name="Draft", is_official=False, owner=owner, **common)
        CharacterTemplate.objects.create(name="Retired", status="Ret", **common)
        CharacterTemplate.objects.create(name="Private", is_public=False, **common)
        CharacterTemplate.objects.create(name="Vampire", gameline="vtm", character_type="vampire")

        form = CharacterTemplateSelectionForm(character=character)

        self.assertEqual(list(form.fields["template"].queryset), [approved, seeded])

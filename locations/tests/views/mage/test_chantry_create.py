"""Chantry creation entry points: the wizard for players, the direct form for STs."""

from django.test import TestCase
from django.urls import reverse

from characters.models.core.background_block import Background
from game.models import Chronicle
from locations.models.mage.chantry import Chantry
from locations.tests.views.mage.chantry_fixtures import add_chantry_actors

WIZARD_URL = reverse("locations:mage:create:chantry")
DIRECT_URL = reverse("locations:mage:create:chantry_direct")


class ChantryBasicsTests(TestCase):
    def setUp(self):
        add_chantry_actors(self)

    def test_create_chantry_goes_to_the_wizard(self):
        self.assertEqual(Chantry.get_creation_url(), WIZARD_URL)
        self.client.force_login(self.player)
        response = self.client.get(WIZARD_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/mage/chantry/basics.html")

    def test_anonymous_is_refused(self):
        self.assertEqual(self.client.get(WIZARD_URL).status_code, 401)

    def test_basics_creates_an_unfinished_player_owned_chantry(self):
        self.client.force_login(self.player)
        response = self.client.post(
            WIZARD_URL,
            {
                "name": "Player Chantry",
                "chronicle": self.chronicle.pk,
                "total_points": 12,
                "gauntlet": 5,
                "shroud": 5,
                "dimension_barrier": 5,
            },
        )
        chantry = Chantry.objects.get(name="Player Chantry")
        self.assertRedirects(response, chantry.get_absolute_url(), fetch_redirect_response=False)
        self.assertEqual(chantry.owner, self.player)
        self.assertEqual(chantry.chronicle, self.chronicle)
        self.assertEqual(chantry.status, "Un")
        self.assertEqual(chantry.creation_status, 1)
        self.assertEqual(chantry.total_points, 12)

    def test_basics_applies_library_type_grants(self):
        Background.objects.get_or_create(name="Library", property_name="library")
        self.client.force_login(self.player)
        self.client.post(
            WIZARD_URL,
            {
                "name": "Stacks",
                "chantry_type": "library",
                "total_points": 10,
                "gauntlet": 5,
                "shroud": 5,
                "dimension_barrier": 5,
            },
        )
        chantry = Chantry.objects.get(name="Stacks")
        self.assertEqual(chantry.backgrounds.get(bg__property_name="library").rating, 3)

    def test_list_links_to_both_forms_for_staff(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("locations:mage:list:chantry"))
        self.assertContains(response, WIZARD_URL)
        self.assertContains(response, DIRECT_URL)

    def test_create_directly_link_only_for_storytellers(self):
        self.client.force_login(self.player)
        self.assertNotContains(self.client.get(WIZARD_URL), DIRECT_URL)
        self.client.force_login(self.st)
        self.assertContains(self.client.get(WIZARD_URL), DIRECT_URL)


class ChantryDirectCreateTests(TestCase):
    def setUp(self):
        add_chantry_actors(self)
        self.data = {
            "name": "Direct",
            "total_points": 30,
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
        }

    def test_player_is_refused(self):
        self.client.force_login(self.player)
        self.assertEqual(self.client.get(DIRECT_URL).status_code, 403)
        response = self.client.post(DIRECT_URL, {**self.data, "chronicle": self.chronicle.pk})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Chantry.objects.filter(name="Direct").exists())

    def test_st_of_another_gameline_is_refused(self):
        self.client.force_login(self.vampire_st)
        self.assertEqual(self.client.get(DIRECT_URL).status_code, 403)

    def test_scoped_st_sees_only_their_chronicles(self):
        self.client.force_login(self.st)
        response = self.client.get(DIRECT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/mage/chantry/form.html")
        self.assertEqual(
            list(response.context["form"].fields["chronicle"].queryset), [self.chronicle]
        )

    def test_scoped_st_creates_in_their_chronicle(self):
        self.client.force_login(self.st)
        response = self.client.post(DIRECT_URL, {**self.data, "chronicle": self.chronicle.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Chantry.objects.get(name="Direct").chronicle, self.chronicle)

    def test_wrong_chronicle_st_is_refused(self):
        self.client.force_login(self.other_st)
        response = self.client.post(DIRECT_URL, {**self.data, "chronicle": self.chronicle.pk})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Chantry.objects.filter(name="Direct").exists())

    def test_head_st_qualifies(self):
        self.other_chronicle.head_st = self.player
        self.other_chronicle.save()
        self.client.force_login(self.player)
        response = self.client.post(DIRECT_URL, {**self.data, "chronicle": self.other_chronicle.pk})
        self.assertEqual(response.status_code, 302)

    def test_staff_sees_every_chronicle_and_may_leave_it_blank(self):
        self.client.force_login(self.staff)
        response = self.client.get(DIRECT_URL)
        self.assertEqual(
            set(response.context["form"].fields["chronicle"].queryset),
            set(Chronicle.objects.all()),
        )
        self.assertEqual(self.client.post(DIRECT_URL, self.data).status_code, 302)
        self.assertIsNone(Chantry.objects.get(name="Direct").chronicle)

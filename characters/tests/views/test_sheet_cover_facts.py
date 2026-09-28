"""Demon host cover (C19) and Garou deed name (C13): sheet cover, basics and edit round trips."""

from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from characters.models.demon import Demon
from characters.models.werewolf.garou import Werewolf
from game.models import Chronicle

User = get_user_model()


def form_data(form, **changes):
    """POST data that resubmits every field of an unbound form as it was rendered."""
    data = {}
    for name, field in form.fields.items():
        if isinstance(field, forms.FileField):
            continue
        value = form[name].value()
        if value is None:
            continue
        if isinstance(value, bool):
            if value:
                data[name] = "on"
        elif isinstance(value, list | tuple):
            data[name] = [str(item) for item in value]
        else:
            data[name] = value
    data.update(changes)
    return data


class CoverFactsTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("jpark", password="pw")
        self.st = User.objects.create_user("storyteller", password="pw")
        self.chronicle = Chronicle.objects.create(name="The Burning Year", head_st=self.st)


class DemonHostTests(CoverFactsTestCase):
    """A Demon's name is its mortal host's (C19): the cover is titled with the celestial
    name, with "Host: name, concept" under it and a Host fact."""

    def setUp(self):
        super().setUp()
        self.demon = Demon.objects.create(
            name="Daniel Okoro",
            celestial_name="Ahrimel",
            concept="ER nurse",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_cover_is_titled_with_the_celestial_name_and_names_the_host(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.demon.get_absolute_url())
        name = response.content.decode().split('class="tl-cover__name', 1)[1].split("</h1>", 1)[0]
        self.assertIn("Ahrimel", name)
        self.assertContains(response, "Host: Daniel Okoro, ER nurse")
        self.assertContains(response, '<span class="tl-facts__k">Host</span>', html=False)

    def test_without_a_celestial_name_the_cover_is_the_plain_sheet(self):
        demon = Demon.objects.create(
            name="Nameless", concept="Drifter", owner=self.owner, status="App"
        )
        self.client.force_login(self.owner)
        response = self.client.get(demon.get_absolute_url())
        self.assertNotContains(response, '<span class="tl-facts__k">Host</span>', html=False)
        self.assertNotContains(response, "Host:")
        self.assertContains(response, '<span class="tl-cover__sub">Drifter</span>', html=False)


class GarouDeedNameTests(CoverFactsTestCase):
    def setUp(self):
        super().setUp()
        self.garou = Werewolf.objects.create(
            name="Aurelio Brandt",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            deed_name="Stands-Against-Storm",
            concept="Sept warder",
        )

    def test_sheet_shows_the_deed_name_under_the_name(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.garou.get_absolute_url())
        self.assertContains(
            response,
            "“Stands-Against-Storm” · Sept warder",
        )

    def test_basics_step_saves_the_deed_name(self):
        self.client.force_login(self.owner)
        url = reverse("characters:werewolf:create:werewolf")
        response = self.client.get(url)
        self.assertContains(response, 'name="deed_name"')
        response = self.client.post(
            url,
            form_data(
                response.context["form"],
                name="Mira Runs-Far",
                deed_name="Runs-Far",
                concept="Scout",
            ),
        )
        self.assertEqual(response.status_code, 302, getattr(response, "context", None))
        self.assertEqual(Werewolf.objects.get(name="Mira Runs-Far").deed_name, "Runs-Far")

    def test_storyteller_edit_round_trip(self):
        self.client.force_login(self.st)
        url = reverse("characters:werewolf:update:werewolf_full", kwargs={"pk": self.garou.pk})
        response = self.client.get(url)
        self.assertContains(response, 'name="deed_name"')
        self.assertContains(response, 'value="Stands-Against-Storm"')
        response = self.client.post(
            url, form_data(response.context["form"], deed_name="Breaks-The-Storm")
        )
        self.assertEqual(
            response.status_code, 302, response.context and response.context["form"].errors
        )
        self.garou.refresh_from_db()
        self.assertEqual(self.garou.deed_name, "Breaks-The-Storm")

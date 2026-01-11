from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.vampire import Coterie, Vampire, VampireClan


class TestCoterieDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.coterie = Coterie.objects.create(name="Test Coterie")
        self.url = self.coterie.get_absolute_url()

    def test_coterie_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_coterie_detail_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/coterie/detail.html")

    def test_coterie_detail_view_url(self):
        expected_url = reverse("characters:vampire:coterie", kwargs={"pk": self.coterie.pk})
        self.assertEqual(self.url, expected_url)


class TestCoterieCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "New Coterie",
            "description": "A new vampire coterie",
        }
        self.url = Coterie.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/coterie/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Coterie.objects.count(), 1)
        self.assertEqual(Coterie.objects.first().name, "New Coterie")


class TestCoterieUpdateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.coterie = Coterie.objects.create(name="Test Coterie")
        self.valid_data = {
            "name": "Updated Coterie",
            "description": "Updated description",
        }
        self.url = self.coterie.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/coterie/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.coterie.refresh_from_db()
        self.assertEqual(self.coterie.name, "Updated Coterie")


class TestCoterieListView(TestCase):
    def setUp(self):
        self.coterie1 = Coterie.objects.create(name="Coterie Alpha")
        self.coterie2 = Coterie.objects.create(name="Coterie Beta")
        self.url = reverse("characters:vampire:list:coterie")

    def test_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/coterie/list.html")

    def test_list_view_contains_coteries(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Coterie Alpha")
        self.assertContains(response, "Coterie Beta")

    def test_list_view_ordering(self):
        response = self.client.get(self.url)
        coteries = response.context["object_list"]
        self.assertEqual(list(coteries), [self.coterie1, self.coterie2])


class TestCoterieModel(TestCase):
    def setUp(self):
        self.coterie = Coterie.objects.create(name="Test Coterie")

    def test_coterie_type(self):
        self.assertEqual(self.coterie.type, "coterie")

    def test_coterie_gameline(self):
        self.assertEqual(self.coterie.gameline, "vtm")

    def test_coterie_get_heading(self):
        self.assertEqual(self.coterie.get_heading(), "vtm_heading")

    def test_coterie_verbose_name(self):
        self.assertEqual(Coterie._meta.verbose_name, "Coterie")
        self.assertEqual(Coterie._meta.verbose_name_plural, "Coteries")


class TestCoterieWithMembers(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.clan = VampireClan.objects.create(name="Test Clan")
        self.vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            clan=self.clan,
        )
        self.coterie = Coterie.objects.create(name="Test Coterie")
        self.coterie.members.add(self.vampire)
        self.coterie.leader = self.vampire
        self.coterie.save()

    def test_coterie_with_leader(self):
        self.assertEqual(self.coterie.leader, self.vampire)

    def test_coterie_with_members(self):
        self.assertIn(self.vampire, self.coterie.members.all())

    def test_coterie_detail_shows_members(self):
        response = self.client.get(self.coterie.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Vampire")

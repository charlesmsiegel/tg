from characters.models.mage.cabal import Cabal
from characters.models.mage.mage import Mage
from characters.tests.utils import mage_setup
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestCabal(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.character = Mage.objects.create(name="Test Mage", owner=self.player)
        mage_setup()
        for i in range(4):
            Mage.objects.create(name=f"Character {i}", owner=self.player)

    def test_cabal_creation(self):
        cabal = Cabal.objects.create(name="Cabal 1")
        cabal.members.set(Mage.objects.all())
        cabal.leader = Mage.objects.first()
        cabal.save()
        self.assertEqual(cabal.members.count(), 5)
        self.assertIsNotNone(cabal.leader)

    def test_str(self):
        cabal = Cabal.objects.create(name="Cabal 1")
        self.assertEqual(str(cabal), "Cabal 1")


class TestCabalDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.cabal = Cabal.objects.create(name="Test Cabal")
        self.url = self.cabal.get_absolute_url()

    def test_cabal_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_cabal_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/cabal/detail.html")


class TestCabalCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Cabal",
            "description": "Test",
            "public_info": "Tetst",
        }
        self.url = Cabal.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/cabal/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cabal.objects.count(), 1)
        self.assertEqual(Cabal.objects.first().name, "Test Cabal")


class TestCabalUpdateView(TestCase):
    def setUp(self):
        self.cabal = Cabal.objects.create(name="Test Cabal", description="Test")
        self.valid_data = {
            "name": "Test Cabal Updated",
            "description": "Test",
            "public_info": "Tetst",
        }
        self.url = self.cabal.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/cabal/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.cabal.refresh_from_db()
        self.assertEqual(self.cabal.name, "Test Cabal Updated")
        self.assertEqual(self.cabal.description, "Test")


class TestCabalListView(TestCase):
    def setUp(self):
        self.cabal1 = Cabal.objects.create(name="Cabal Alpha")
        self.cabal2 = Cabal.objects.create(name="Cabal Beta")
        self.url = reverse("characters:mage:list:cabal")

    def test_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/cabal/list.html")

    def test_list_view_contains_cabals(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Cabal Alpha")
        self.assertContains(response, "Cabal Beta")

    def test_list_view_ordering(self):
        response = self.client.get(self.url)
        cabals = response.context["object_list"]
        self.assertEqual(list(cabals), [self.cabal1, self.cabal2])

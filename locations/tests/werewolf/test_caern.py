from django.test import TestCase
from locations.models.werewolf.caern import Caern


class TestCaern(TestCase):
    def test_gauntlet(self):
        caern_1 = Caern.objects.create(name="Test Caern 1", rank=1)
        self.assertEqual(caern_1.gauntlet, 4)
        caern_2 = Caern.objects.create(name="Test Caern 2", rank=2)
        self.assertEqual(caern_2.gauntlet, 4)
        caern_3 = Caern.objects.create(name="Test Caern 3", rank=3)
        self.assertEqual(caern_3.gauntlet, 3)
        caern_4 = Caern.objects.create(name="Test Caern 4", rank=4)
        self.assertEqual(caern_4.gauntlet, 3)
        caern_5 = Caern.objects.create(name="Test Caern 5", rank=5)
        self.assertEqual(caern_5.gauntlet, 2)


class TestCaernDetailView(TestCase):
    def setUp(self) -> None:
        self.caern = Caern.objects.create(name="Test Caern")
        self.url = self.caern.get_absolute_url()

    def test_caern_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_caern_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/werewolf/caern/detail.html")


class TestCaernCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Caern",
            "description": "Test",
            "rank": 2,
            "caern_type": "wyld",
        }
        self.url = Caern.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/werewolf/caern/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Caern.objects.count(), 1)
        self.assertEqual(Caern.objects.first().name, "Caern")


class TestCaernUpdateView(TestCase):
    def setUp(self):
        self.caern = Caern.objects.create(
            name="Test Caern",
            description="Test description",
        )
        self.valid_data = {
            "name": "Caern Updated",
            "description": "Test",
            "rank": 2,
            "caern_type": "wyld",
        }
        self.url = self.caern.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/werewolf/caern/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.caern.refresh_from_db()
        self.assertEqual(self.caern.name, "Caern Updated")
        self.assertEqual(self.caern.description, "Test")

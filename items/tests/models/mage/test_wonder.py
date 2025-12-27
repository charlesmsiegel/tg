from characters.models.mage import Resonance
from django.test import TestCase
from items.models.mage import Wonder


class TestWonder(TestCase):
    def setUp(self):
        for i in range(5):
            Resonance.objects.get_or_create(name="Resonance {i}")
        self.wonder = Wonder.objects.create(name="Test Wonder")

    def test_set_rank(self):
        g = Wonder.objects.create(name="")
        self.assertFalse(g.has_rank())
        self.assertTrue(g.set_rank(3))
        self.assertEqual(g.rank, 3)

    def test_has_rank(self):
        g = Wonder.objects.create(name="")
        self.assertFalse(g.has_rank())
        g.set_rank(3)
        self.assertTrue(g.has_rank())

    def test_add_resonance(self):
        res = Resonance.objects.create(name="Test Resonance")
        self.wonder.add_resonance(res)
        self.assertEqual(self.wonder.resonance_rating(res), 1)

    def test_resonance_rating(self):
        res = Resonance.objects.create(name="Test Resonance")
        self.wonder.add_resonance(res)
        self.assertEqual(self.wonder.resonance_rating(res), 1)

    def test_filter_resonance(self):
        res1 = Resonance.objects.create(name="Test Resonance 1")
        res2 = Resonance.objects.create(name="Test Resonance 2")
        res3 = Resonance.objects.create(name="Test Resonance 3")
        self.wonder.add_resonance(res1)
        self.wonder.add_resonance(res2)
        self.wonder.add_resonance(res2)
        self.wonder.add_resonance(res3)
        self.wonder.add_resonance(res3)
        self.wonder.add_resonance(res3)
        res_filtered = self.wonder.filter_resonance(minimum=2, maximum=4)
        self.assertIn(res2, res_filtered)
        self.assertIn(res3, res_filtered)
        self.assertEqual(res_filtered.count(), 2)

    def test_total_resonance(self):
        res1 = Resonance.objects.create(name="Test Resonance 1")
        res2 = Resonance.objects.create(name="Test Resonance 2")
        res3 = Resonance.objects.create(name="Test Resonance 3")
        self.wonder.add_resonance(res1)
        self.wonder.add_resonance(res2)
        self.wonder.add_resonance(res3)
        self.assertEqual(self.wonder.total_resonance(), 3)

    def test_has_resonance(self):
        self.wonder.rank = 2
        self.assertFalse(self.wonder.has_resonance())
        res1 = Resonance.objects.create(name="Test Resonance 1")
        self.wonder.add_resonance(res1)
        self.assertFalse(self.wonder.has_resonance())
        res2 = Resonance.objects.create(name="Test Resonance 2")
        self.wonder.add_resonance(res2)
        self.assertTrue(self.wonder.has_resonance())


class TestWonderDetailView(TestCase):
    def setUp(self) -> None:
        self.wonder = Wonder.objects.create(name="Test Wonder")
        self.url = self.wonder.get_absolute_url()

    def test_object_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_object_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/wonder/detail.html")


class TestWonderCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Wonder",
            "description": "A test description for the wonder.",
            "rank": 2,
            "background_cost": 3,
            "quintessence_max": 5,
        }
        self.url = Wonder.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/wonder/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Wonder.objects.count(), 1)
        self.assertEqual(Wonder.objects.first().name, "Test Wonder")


class TestWonderUpdateView(TestCase):
    def setUp(self):
        self.wonder = Wonder.objects.create(
            name="Test Wonder",
            description="Test description",
        )
        self.valid_data = {
            "name": "Test Wonder Updated",
            "description": "A test description for the wonder.",
            "rank": 2,
            "background_cost": 3,
            "quintessence_max": 5,
        }
        self.url = self.wonder.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/wonder/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.wonder.refresh_from_db()
        self.assertEqual(self.wonder.name, "Test Wonder Updated")
        self.assertEqual(self.wonder.description, "A test description for the wonder.")

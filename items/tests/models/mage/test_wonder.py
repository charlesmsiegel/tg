from characters.models.mage import Resonance
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
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
        self.user = User.objects.create_user(username="testuser", password="password")
        self.wonder = Wonder.objects.create(
            name="Test Wonder",
            owner=self.user,
            status="App",
        )
        self.url = self.wonder.get_absolute_url()

    def test_object_detail_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_object_detail_view_templates(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/wonder/detail.html")


class TestWonderCreateView(TestCase):
    """Test Wonder create view GET requests.

    Note: POST tests for Wonder creation require complex form data with
    resonance formsets and effect formsets which is beyond the scope of
    basic CRUD view tests. The GET tests verify the view is accessible.
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.url = Wonder.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/wonder/form.html")


class TestWonderUpdateView(TestCase):
    """Test Wonder update view GET requests.

    Note: POST tests for Wonder updates require complex form data with
    resonance formsets and effect formsets which is beyond the scope of
    basic CRUD view tests. The GET tests verify the view is accessible.
    """

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.wonder = Wonder.objects.create(
            name="Test Wonder",
            description="Test description",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )
        self.url = self.wonder.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/wonder/form.html")

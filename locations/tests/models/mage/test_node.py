import unittest

from characters.models.core import MeritFlaw
from characters.models.mage import Resonance
from characters.tests.utils import mage_setup
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from locations.models.mage import Node, NodeMeritFlawRating, NodeResonanceRating


class TestNode(TestCase):
    def setUp(self):
        mage_setup()
        self.node = Node.objects.create(name="Test Node")

    def test_add_resonance(self):
        res = Resonance.objects.order_by("?").first()
        self.assertEqual(self.node.resonance_rating(res), 0)
        self.assertTrue(self.node.add_resonance(res))
        self.assertEqual(self.node.resonance_rating(res), 1)

    def test_filter_resonance(self):
        self.assertEqual(len(self.node.filter_resonance()), 65)
        for res in Resonance.objects.order_by("?")[:3]:
            self.assertTrue(self.node.add_resonance(res))
        self.assertEqual(len(self.node.filter_resonance(maximum=0)), 62)

    def test_total_resonance(self):
        resonance = Resonance.objects.order_by("?")[:2]
        for res in resonance:
            self.node.add_resonance(res)
            self.node.add_resonance(res)
        self.assertEqual(self.node.total_resonance(), 4)
        self.assertNotEqual(self.node.total_resonance(), 5)
        self.node.add_resonance(resonance[1])
        self.assertEqual(self.node.total_resonance(), 5)

    def test_check_resonance(self):
        r = Resonance.objects.create(name="Test Res")
        self.assertTrue(self.node.check_resonance(r))
        self.node.add_resonance(r)
        self.node.add_resonance(r)
        self.node.add_resonance(r)
        self.node.add_resonance(r)
        self.node.add_resonance(r)
        self.assertFalse(self.node.check_resonance(r))
        r2 = Resonance.objects.create(name="Test Res 2", forces=True)
        self.assertFalse(self.node.check_resonance(r2, sphere="life"))
        self.assertTrue(self.node.check_resonance(r2, sphere="forces"))
        self.assertTrue(self.node.check_resonance(r2))
        self.node.add_resonance(r2)
        self.node.add_resonance(r2)
        self.node.add_resonance(r2)
        self.node.add_resonance(r2)
        self.node.add_resonance(r2)
        self.assertFalse(self.node.check_resonance(r2, sphere="forces"))

    def test_has_resonance(self):
        self.node.rank = 1
        resonance = Resonance.objects.create(name="Test Resonance")
        self.node.add_resonance(resonance)
        self.assertTrue(self.node.has_resonance())

    def test_resonance_rating(self):
        resonance = Resonance.objects.create(name="Test Resonance")
        rating = 3
        NodeResonanceRating.objects.create(node=self.node, resonance=resonance, rating=rating)
        self.assertEqual(self.node.resonance_rating(resonance), rating)

    def test_set_rank(self):
        self.assertEqual(self.node.rank, 0)
        self.assertTrue(self.node.set_rank(3))
        self.assertEqual(self.node.rank, 3)
        self.assertEqual(self.node.points, 9)

    def test_resonance_postprocessing(self):
        merit1 = MeritFlaw.objects.create(name="Corrupted")
        merit1.add_rating(0)
        merit2 = MeritFlaw.objects.create(name="Sphere Attuned (Forces)")
        merit2.add_rating(0)
        Resonance.objects.create(name="Corrupted")
        Resonance.objects.create(
            name="Sphered",
            correspondence=True,
            entropy=True,
            forces=True,
            matter=True,
            life=True,
            time=True,
            prime=True,
            spirit=True,
            mind=True,
        )
        self.node.merits_and_flaws.add(merit1)
        self.node.merits_and_flaws.add(merit2)
        self.node.save()
        self.node.resonance_postprocessing()
        self.assertEqual(self.node.total_resonance(), 3)
        self.assertIn("Corrupted", [x.name for x in self.node.resonance.all()])
        self.assertGreaterEqual(len([x for x in self.node.resonance.all() if x.forces]), 1)

    def test_add_mf(self):
        num = self.node.total_mf()
        self.assertFalse(self.node.add_mf(MeritFlaw.objects.get(name="Node Merit 3"), 4))
        self.assertTrue(self.node.add_mf(MeritFlaw.objects.get(name="Node Merit 3"), 3))
        self.assertEqual(self.node.total_mf(), num + 3)

    def test_filter_mf(self):
        self.assertEqual(len(self.node.filter_mf()), 10)
        self.assertEqual(len(self.node.filter_mf(minimum=0)), 5)
        for mf in MeritFlaw.objects.all():
            if "Merit" in mf.name:
                self.node.add_mf(mf, mf.min_rating)
        self.assertEqual(len(self.node.filter_mf()), 5)
        self.assertEqual(len(self.node.filter_mf(maximum=0)), 5)
        for mf in MeritFlaw.objects.all():
            if "Flaw" in mf.name:
                self.node.add_mf(mf, mf.min_rating)
        self.assertEqual(len(self.node.filter_mf()), 0)

    def test_total_mf(self):
        self.assertEqual(self.node.total_mf(), 0)
        self.node.add_mf(MeritFlaw.objects.get(name="Node Merit 3"), 3)
        self.assertEqual(self.node.total_mf(), 3)
        self.node.add_mf(MeritFlaw.objects.get(name="Node Flaw 2"), -2)
        self.assertEqual(self.node.total_mf(), 1)

    def test_mf_rating(self):
        mf = MeritFlaw.objects.create(name="Test MF")
        mf.add_ratings([1, 2, 3])
        rating = 2
        NodeMeritFlawRating.objects.create(node=self.node, mf=mf, rating=rating)
        self.assertEqual(self.node.mf_rating(mf), rating)

    def test_set_size(self):
        self.assertEqual(self.node.size, 0)
        self.assertEqual(self.node.get_size_display(), "Average Room")
        self.assertTrue(self.node.set_size(2))
        self.assertEqual(self.node.size, 2)
        self.assertEqual(self.node.get_size_display(), "Large Building")
        self.assertTrue(self.node.set_size(-2))
        self.assertEqual(self.node.size, -2)
        self.assertEqual(self.node.get_size_display(), "Household Object")

    def test_set_ratio(self):
        self.assertEqual(self.node.ratio, 0)
        self.assertEqual(self.node.get_ratio_display(), "0.5")
        self.assertTrue(self.node.set_ratio(2))
        self.assertEqual(self.node.ratio, 2)
        self.assertEqual(self.node.get_ratio_display(), "1.0")
        self.assertTrue(self.node.set_ratio(-2))
        self.assertEqual(self.node.ratio, -2)
        self.assertEqual(self.node.get_ratio_display(), "0.0")

    def test_update_output(self):
        self.node.set_rank(2)
        self.assertEqual(self.node.ratio, 0)
        self.node.update_output()
        self.assertEqual(self.node.quintessence_per_week, 3)
        self.assertEqual(self.node.tass_per_week, 3)
        self.node.set_ratio(1)
        self.assertEqual(self.node.ratio, 1)
        self.node.update_output()
        self.assertEqual(self.node.quintessence_per_week, 4)
        self.assertEqual(self.node.tass_per_week, 2)

    def test_has_output_forms(self):
        self.assertFalse(self.node.has_output_forms())
        self.node.set_output_forms("Quintessence", "Tass")
        self.assertTrue(self.node.has_output_forms())

    def test_set_output_forms(self):
        self.assertFalse(self.node.has_output_forms())
        self.assertTrue(self.node.set_output_forms("Quintessence", "Tass"))
        self.assertTrue(self.node.has_output_forms())

    def test_has_output(self):
        self.node.set_rank(3)
        self.assertFalse(self.node.has_output())
        self.node.update_output()
        self.assertTrue(self.node.has_output())


class TestNodeDetailView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="password")
        self.location = Node.objects.create(
            name="Test Node",
            owner=self.user,
            status="App",
        )
        self.url = self.location.get_absolute_url()

    def test_location_detail_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_location_detail_view_templates(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/node/detail.html")


class TestNodeCreateView(TestCase):
    """Test Node create view GET requests."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.url = Node.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/node/form.html")


class TestNodeUpdateView(TestCase):
    """Test Node update view GET requests.

    Note: POST tests require complex setup with ObjectType and other dependencies
    which is beyond the scope of basic CRUD view tests. GET tests verify accessibility.
    """

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.node = Node.objects.create(
            name="Test Node",
            description="Test description",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )
        self.url = self.node.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/node/form.html")

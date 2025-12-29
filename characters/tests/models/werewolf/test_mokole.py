"""Tests for Mokole (weresaurian) module."""

from characters.models.werewolf.mokole import Mokole
from django.contrib.auth.models import User
from django.test import TestCase


class TestMokole(TestCase):
    """Tests for Mokole model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.mokole = Mokole.objects.create(name="Test Mokole", owner=self.player)

    def test_mokole_creation(self):
        """Test basic Mokole creation."""
        self.assertEqual(self.mokole.name, "Test Mokole")
        self.assertEqual(self.mokole.type, "mokole")

    def test_mokole_default_values(self):
        """Test default values for Mokole."""
        self.assertEqual(self.mokole.gnosis, 0)
        self.assertEqual(self.mokole.rage, 0)
        self.assertEqual(self.mokole.valor, 0)
        self.assertEqual(self.mokole.harmony, 0)
        self.assertEqual(self.mokole.wisdom, 0)
        self.assertEqual(self.mokole.mnesis, 1)

    def test_set_breed_homid(self):
        """Test setting homid breed."""
        self.assertTrue(self.mokole.set_breed("homid"))
        self.assertEqual(self.mokole.breed, "homid")
        self.assertEqual(self.mokole.gnosis, 3)
        self.assertTrue(
            self.mokole.gift_permissions.filter(shifter="mokole", condition="homid").exists()
        )

    def test_set_breed_metis(self):
        """Test setting metis breed."""
        self.assertTrue(self.mokole.set_breed("metis"))
        self.assertEqual(self.mokole.breed, "metis")
        self.assertEqual(self.mokole.gnosis, 5)

    def test_set_breed_suchid(self):
        """Test setting suchid (reptile) breed."""
        self.assertTrue(self.mokole.set_breed("suchid"))
        self.assertEqual(self.mokole.breed, "suchid")
        self.assertEqual(self.mokole.gnosis, 7)

    def test_has_stream(self):
        """Test stream check."""
        self.assertFalse(self.mokole.has_stream())
        self.mokole.stream = "makara"
        self.assertTrue(self.mokole.has_stream())

    def test_set_stream_makara(self):
        """Test setting Makara stream."""
        self.assertTrue(self.mokole.set_stream("makara"))
        self.assertEqual(self.mokole.stream, "makara")
        self.assertTrue(
            self.mokole.gift_permissions.filter(shifter="mokole", condition="makara").exists()
        )

    def test_set_all_streams(self):
        """Test setting each Mokole stream."""
        streams = ["makara", "zhong_lung", "gumagan", "mokolembembe", "decorated"]
        for stream in streams:
            mokole = Mokole.objects.create(name=f"Test {stream}", owner=self.player)
            self.assertTrue(mokole.set_stream(stream))
            self.assertEqual(mokole.stream, stream)

    def test_has_auspice(self):
        """Test auspice check."""
        self.assertFalse(self.mokole.has_auspice())
        self.mokole.auspice = "rising_sun"
        self.assertTrue(self.mokole.has_auspice())

    def test_set_auspice_rising_sun(self):
        """Test setting rising sun auspice."""
        self.assertTrue(self.mokole.set_auspice("rising_sun"))
        self.assertEqual(self.mokole.auspice, "rising_sun")
        self.assertEqual(self.mokole.rage, 5)
        self.assertTrue(
            self.mokole.gift_permissions.filter(shifter="mokole", condition="rising_sun").exists()
        )

    def test_set_auspice_noonday_sun(self):
        """Test setting noonday sun auspice."""
        self.assertTrue(self.mokole.set_auspice("noonday_sun"))
        self.assertEqual(self.mokole.auspice, "noonday_sun")
        self.assertEqual(self.mokole.rage, 4)

    def test_set_auspice_setting_sun(self):
        """Test setting setting sun auspice."""
        self.assertTrue(self.mokole.set_auspice("setting_sun"))
        self.assertEqual(self.mokole.auspice, "setting_sun")
        self.assertEqual(self.mokole.rage, 3)

    def test_set_auspice_midnight_sun(self):
        """Test setting midnight sun auspice."""
        self.assertTrue(self.mokole.set_auspice("midnight_sun"))
        self.assertEqual(self.mokole.auspice, "midnight_sun")
        self.assertEqual(self.mokole.rage, 2)

    def test_mnesis_unique_field(self):
        """Test Mokole unique mnesis field."""
        self.assertEqual(self.mokole.mnesis, 1)
        self.mokole.mnesis = 5
        self.mokole.save()
        self.mokole.refresh_from_db()
        self.assertEqual(self.mokole.mnesis, 5)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/mokole/{self.mokole.pk}/"
        self.assertEqual(self.mokole.get_absolute_url(), expected_url)

    def test_breeds_list(self):
        """Test available breeds."""
        breeds = dict(Mokole.BREEDS)
        self.assertIn("homid", breeds)
        self.assertIn("suchid", breeds)
        self.assertIn("metis", breeds)

    def test_streams_list(self):
        """Test available streams."""
        streams = dict(Mokole.STREAMS)
        self.assertEqual(len(streams), 5)
        self.assertIn("makara", streams)
        self.assertIn("zhong_lung", streams)

    def test_auspices_list(self):
        """Test available auspices."""
        auspices = dict(Mokole.AUSPICES)
        self.assertIn("rising_sun", auspices)
        self.assertIn("noonday_sun", auspices)
        self.assertIn("setting_sun", auspices)
        self.assertIn("midnight_sun", auspices)


class TestMokoleDetailView(TestCase):
    """Tests for Mokole detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.mokole = Mokole.objects.create(
            name="Test Mokole",
            owner=self.player,
            status="App",
        )

    def test_mokole_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.mokole.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_mokole_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.mokole.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")

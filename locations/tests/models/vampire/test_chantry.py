"""Tests for Tremere Chantry model."""

from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from locations.models.vampire.chantry import TremereChantry


class TestTremereChantryModel(TestCase):
    """Test TremereChantry model methods and properties."""

    def setUp(self):
        self.chantry = TremereChantry.objects.create(name="Test Chantry")

    def test_chantry_type(self):
        """Test chantry type is correctly set."""
        self.assertEqual(self.chantry.type, "tremere_chantry")

    def test_chantry_gameline(self):
        """Test chantry gameline is vtm."""
        self.assertEqual(self.chantry.gameline, "vtm")

    def test_get_heading(self):
        """Test get_heading returns vtm_heading."""
        self.assertEqual(self.chantry.get_heading(), "vtm_heading")

    def test_default_size(self):
        """Test default size is 1."""
        self.assertEqual(self.chantry.size, 1)

    def test_default_security_level(self):
        """Test default security level is 1."""
        self.assertEqual(self.chantry.security_level, 1)

    def test_default_library_rating(self):
        """Test default library rating is 0."""
        self.assertEqual(self.chantry.library_rating, 0)

    def test_default_ritual_rooms(self):
        """Test default ritual rooms is 1."""
        self.assertEqual(self.chantry.ritual_rooms, 1)

    def test_default_blood_vault_capacity(self):
        """Test default blood vault capacity is 10."""
        self.assertEqual(self.chantry.blood_vault_capacity, 10)

    def test_default_has_wards(self):
        """Test default has_wards is True."""
        self.assertTrue(self.chantry.has_wards)

    def test_default_pyramid_level(self):
        """Test default pyramid level is 1."""
        self.assertEqual(self.chantry.pyramid_level, 1)


class TestTremereChantryTotalRating(TestCase):
    """Test calculate_total_rating method."""

    def test_basic_rating_calculation(self):
        """Test basic rating calculation."""
        chantry = TremereChantry.objects.create(
            name="Test", size=3, security_level=2, library_rating=1
        )
        # With has_wards=True (default), total = 3+2+1+1 = 7
        self.assertEqual(chantry.total_rating, 7)

    def test_rating_with_sanctum(self):
        """Test rating increases with sanctum (+2)."""
        chantry = TremereChantry.objects.create(
            name="Test",
            size=3,
            security_level=2,
            library_rating=1,
            has_sanctum=True,
        )
        # 3+2+1+2(sanctum)+1(wards) = 9
        self.assertEqual(chantry.total_rating, 9)

    def test_rating_without_wards(self):
        """Test rating without wards."""
        chantry = TremereChantry.objects.create(
            name="Test",
            size=3,
            security_level=2,
            library_rating=1,
            has_wards=False,
        )
        # 3+2+1 = 6
        self.assertEqual(chantry.total_rating, 6)

    def test_rating_with_blood_forge(self):
        """Test rating increases with blood forge."""
        chantry = TremereChantry.objects.create(
            name="Test",
            size=3,
            security_level=2,
            library_rating=1,
            has_blood_forge=True,
        )
        # 3+2+1+1(blood_forge)+1(wards) = 8
        self.assertEqual(chantry.total_rating, 8)

    def test_rating_with_scrying_chamber(self):
        """Test rating increases with scrying chamber."""
        chantry = TremereChantry.objects.create(
            name="Test",
            size=3,
            security_level=2,
            library_rating=1,
            has_scrying_chamber=True,
        )
        # 3+2+1+1(scrying)+1(wards) = 8
        self.assertEqual(chantry.total_rating, 8)

    def test_rating_with_gargoyle_guardians(self):
        """Test rating increases with gargoyle guardians."""
        chantry = TremereChantry.objects.create(
            name="Test",
            size=3,
            security_level=2,
            library_rating=1,
            has_gargoyle_guardians=True,
        )
        # 3+2+1+1(gargoyles)+1(wards) = 8
        self.assertEqual(chantry.total_rating, 8)

    def test_rating_with_all_features(self):
        """Test rating with all special features."""
        chantry = TremereChantry.objects.create(
            name="Test",
            size=5,
            security_level=5,
            library_rating=5,
            has_wards=True,
            has_sanctum=True,
            has_blood_forge=True,
            has_scrying_chamber=True,
            has_gargoyle_guardians=True,
        )
        # 5+5+5+1(wards)+2(sanctum)+1(forge)+1(scrying)+1(gargoyles) = 21
        self.assertEqual(chantry.total_rating, 21)

    def test_save_recalculates_rating(self):
        """Test save method recalculates total rating."""
        chantry = TremereChantry.objects.create(
            name="Test", size=1, security_level=1, library_rating=0
        )
        # Initial: 1+1+0+1(wards) = 3
        self.assertEqual(chantry.total_rating, 3)
        chantry.size = 3
        chantry.library_rating = 3
        chantry.save()
        # After: 3+1+3+1(wards) = 8
        self.assertEqual(chantry.total_rating, 8)


class TestTremereChantryViews(TestCase):
    """Test TremereChantry views."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.chantry = TremereChantry.objects.create(
            name="Test Chantry",
            owner=self.user,
            status="App",
        )

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.chantry.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.chantry.get_absolute_url())
        self.assertTemplateUsed(response, "locations/vampire/chantry/detail.html")

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(TremereChantry.get_creation_url())
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(TremereChantry.get_creation_url())
        self.assertTemplateUsed(response, "locations/vampire/chantry/form.html")


class TestTremereChantryUpdateView(TestCase):
    """Test TremereChantry update view."""

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.chantry = TremereChantry.objects.create(
            name="Test Chantry",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.chantry.get_update_url())
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.chantry.get_update_url())
        self.assertTemplateUsed(response, "locations/vampire/chantry/form.html")

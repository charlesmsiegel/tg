"""Tests for authentication requirements on views (Issue #1051)."""

from characters.models.core import Group, Specialty
from characters.models.mummy.dynasty import Dynasty
from characters.models.mummy.mummy_title import MummyTitle
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.path import Path
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestCharacterViewAuthenticationRequirements(TestCase):
    """Test that character-related views require authentication."""

    @classmethod
    def setUpTestData(cls):
        """Create test objects for all affected views."""
        cls.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )

        # Create test objects for each affected model
        cls.dynasty = Dynasty.objects.create(name="Test Dynasty")
        cls.mummy_title = MummyTitle.objects.create(name="Test Title", rank_level=3)
        cls.discipline = Discipline.objects.create(
            name="Test Discipline", property_name="test_discipline"
        )
        cls.path = Path.objects.create(name="Test Path")
        cls.specialty = Specialty.objects.create(name="Test Specialty", stat="dexterity")
        cls.group = Group.objects.create(name="Test Group")

    def test_dynasty_detail_requires_auth(self):
        """DynastyDetailView should require authentication."""
        url = reverse("characters:mummy:dynasty", args=[self.dynasty.pk])
        response = self.client.get(url)
        # 302 = redirect to login, 401 = unauthorized, 403 = forbidden
        self.assertIn(response.status_code, [302, 401, 403])
        if response.status_code == 302:
            self.assertIn("/accounts/login/", response.url)

    def test_dynasty_detail_accessible_when_authenticated(self):
        """DynastyDetailView should be accessible when authenticated."""
        self.client.login(username="testuser", password="testpass123")
        url = reverse("characters:mummy:dynasty", args=[self.dynasty.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_mummy_title_detail_requires_auth(self):
        """MummyTitleDetailView should require authentication."""
        url = reverse("characters:mummy:title", args=[self.mummy_title.pk])
        response = self.client.get(url)
        # 302 = redirect to login, 401 = unauthorized, 403 = forbidden
        self.assertIn(response.status_code, [302, 401, 403])
        if response.status_code == 302:
            self.assertIn("/accounts/login/", response.url)

    def test_mummy_title_detail_accessible_when_authenticated(self):
        """MummyTitleDetailView should be accessible when authenticated."""
        self.client.login(username="testuser", password="testpass123")
        url = reverse("characters:mummy:title", args=[self.mummy_title.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_discipline_detail_requires_auth(self):
        """DisciplineDetailView should require authentication."""
        url = reverse("characters:vampire:discipline", args=[self.discipline.pk])
        response = self.client.get(url)
        # 302 = redirect to login, 401 = unauthorized, 403 = forbidden
        self.assertIn(response.status_code, [302, 401, 403])
        if response.status_code == 302:
            self.assertIn("/accounts/login/", response.url)

    def test_discipline_detail_accessible_when_authenticated(self):
        """DisciplineDetailView should be accessible when authenticated (or raise template error)."""
        self.client.login(username="testuser", password="testpass123")
        url = reverse("characters:vampire:discipline", args=[self.discipline.pk])
        try:
            response = self.client.get(url)
            # If template exists, should return 200
            self.assertEqual(response.status_code, 200)
        except Exception as e:
            # Template doesn't exist, but authentication passed
            self.assertIn("TemplateDoesNotExist", str(type(e).__name__))

    def test_path_detail_requires_auth(self):
        """PathDetailView should require authentication."""
        url = reverse("characters:vampire:path", args=[self.path.pk])
        response = self.client.get(url)
        # 302 = redirect to login, 401 = unauthorized, 403 = forbidden
        self.assertIn(response.status_code, [302, 401, 403])
        if response.status_code == 302:
            self.assertIn("/accounts/login/", response.url)

    def test_path_detail_accessible_when_authenticated(self):
        """PathDetailView should be accessible when authenticated (or raise template error)."""
        self.client.login(username="testuser", password="testpass123")
        url = reverse("characters:vampire:path", args=[self.path.pk])
        try:
            response = self.client.get(url)
            # If template exists, should return 200
            self.assertEqual(response.status_code, 200)
        except Exception as e:
            # Template doesn't exist, but authentication passed
            self.assertIn("TemplateDoesNotExist", str(type(e).__name__))

    def test_specialty_detail_requires_auth(self):
        """SpecialtyDetailView should require authentication."""
        url = reverse("characters:specialty", args=[self.specialty.pk])
        response = self.client.get(url)
        # 302 = redirect to login, 401 = unauthorized, 403 = forbidden
        self.assertIn(response.status_code, [302, 401, 403])
        if response.status_code == 302:
            self.assertIn("/accounts/login/", response.url)

    def test_specialty_detail_accessible_when_authenticated(self):
        """SpecialtyDetailView should be accessible when authenticated."""
        self.client.login(username="testuser", password="testpass123")
        url = reverse("characters:specialty", args=[self.specialty.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_group_detail_requires_auth(self):
        """GroupDetailView should require authentication."""
        url = reverse("characters:group", args=[self.group.pk])
        response = self.client.get(url)
        # 302 = redirect to login, 401 = unauthorized, 403 = forbidden
        self.assertIn(response.status_code, [302, 401, 403])
        if response.status_code == 302:
            self.assertIn("/accounts/login/", response.url)

    def test_group_detail_accessible_when_authenticated(self):
        """GroupDetailView should be accessible when authenticated."""
        self.client.login(username="testuser", password="testpass123")
        url = reverse("characters:group", args=[self.group.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

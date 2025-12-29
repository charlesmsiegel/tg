"""Tests for LinearMagicPath and LinearMagicRitual views."""

from characters.models.mage.sorcerer import LinearMagicPath, LinearMagicRitual
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestPathListView(TestCase):
    """Test PathListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.path_hedge = LinearMagicPath.objects.create(
            name="Alchemy",
            numina_type="hedge_magic",
        )
        self.path_psychic = LinearMagicPath.objects.create(
            name="Telepathy",
            numina_type="psychic",
        )

    def test_list_view_accessible_without_login(self):
        """Test that path list view is accessible without login."""
        response = self.client.get(reverse("characters:mage:list:path"))
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        """Test that correct template is used for path list view."""
        response = self.client.get(reverse("characters:mage:list:path"))
        self.assertTemplateUsed(response, "characters/mage/linear_magic_path/list.html")

    def test_list_view_contains_paths(self):
        """Test that list view contains created paths."""
        response = self.client.get(reverse("characters:mage:list:path"))
        self.assertContains(response, "Alchemy")
        self.assertContains(response, "Telepathy")


class TestPathDetailView(TestCase):
    """Test PathDetailView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.path = LinearMagicPath.objects.create(
            name="Alchemy",
            numina_type="hedge_magic",
            description="The art of transmutation",
        )

    def test_detail_view_accessible_without_login(self):
        """Test that path detail view is accessible without login."""
        response = self.client.get(self.path.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used for path detail view."""
        response = self.client.get(self.path.get_absolute_url())
        self.assertTemplateUsed(response, "characters/mage/linear_magic_path/detail.html")

    def test_detail_view_contains_path_info(self):
        """Test that detail view contains path information."""
        response = self.client.get(self.path.get_absolute_url())
        self.assertContains(response, "Alchemy")
        self.assertContains(response, "Hedge Magic")


class TestPathCreateView(TestCase):
    """Test PathCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_create_view_accessible_when_logged_in(self):
        """Test that path create view is accessible when logged in."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:mage:create:path"))
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that correct template is used for path create view."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:mage:create:path"))
        self.assertTemplateUsed(response, "characters/mage/linear_magic_path/form.html")

    def test_create_view_can_create_path(self):
        """Test that path can be created through the view."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("characters:mage:create:path"),
            {
                "name": "Test Path",
                "description": "A test path",
                "numina_type": "hedge_magic",
            },
        )
        self.assertTrue(LinearMagicPath.objects.filter(name="Test Path").exists())


class TestPathUpdateView(TestCase):
    """Test PathUpdateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.path = LinearMagicPath.objects.create(
            name="Alchemy",
            numina_type="hedge_magic",
        )

    def test_update_view_accessible_when_logged_in(self):
        """Test that path update view is accessible when logged in."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:mage:update:path", kwargs={"pk": self.path.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that correct template is used for path update view."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:mage:update:path", kwargs={"pk": self.path.pk})
        )
        self.assertTemplateUsed(response, "characters/mage/linear_magic_path/form.html")

    def test_update_view_can_update_path(self):
        """Test that path can be updated through the view."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("characters:mage:update:path", kwargs={"pk": self.path.pk}),
            {
                "name": "Updated Alchemy",
                "description": "Updated description",
                "numina_type": "hedge_magic",
            },
        )
        self.path.refresh_from_db()
        self.assertEqual(self.path.name, "Updated Alchemy")


class TestRitualListView(TestCase):
    """Test RitualListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.path = LinearMagicPath.objects.create(
            name="Alchemy",
            numina_type="hedge_magic",
        )
        self.ritual1 = LinearMagicRitual.objects.create(
            name="Purify Water",
            path=self.path,
            level=1,
        )
        self.ritual2 = LinearMagicRitual.objects.create(
            name="Transmute Gold",
            path=self.path,
            level=3,
        )

    def test_list_view_accessible_without_login(self):
        """Test that ritual list view is accessible without login."""
        response = self.client.get(reverse("characters:mage:list:ritual"))
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        """Test that correct template is used for ritual list view."""
        response = self.client.get(reverse("characters:mage:list:ritual"))
        self.assertTemplateUsed(response, "characters/mage/linear_magic_ritual/list.html")

    def test_list_view_contains_rituals(self):
        """Test that list view contains created rituals."""
        response = self.client.get(reverse("characters:mage:list:ritual"))
        self.assertContains(response, "Purify Water")
        self.assertContains(response, "Transmute Gold")

    def test_list_view_context_contains_paths(self):
        """Test that list view context contains paths for filtering."""
        response = self.client.get(reverse("characters:mage:list:ritual"))
        self.assertIn("paths", response.context)
        self.assertIn(self.path, response.context["paths"])


class TestRitualDetailView(TestCase):
    """Test RitualDetailView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.path = LinearMagicPath.objects.create(
            name="Alchemy",
            numina_type="hedge_magic",
        )
        self.ritual = LinearMagicRitual.objects.create(
            name="Purify Water",
            path=self.path,
            level=1,
            description="Purifies a quantity of water",
        )

    def test_detail_view_accessible_without_login(self):
        """Test that ritual detail view is accessible without login."""
        response = self.client.get(self.ritual.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used for ritual detail view."""
        response = self.client.get(self.ritual.get_absolute_url())
        self.assertTemplateUsed(response, "characters/mage/linear_magic_ritual/detail.html")

    def test_detail_view_contains_ritual_info(self):
        """Test that detail view contains ritual information."""
        response = self.client.get(self.ritual.get_absolute_url())
        self.assertContains(response, "Purify Water")
        self.assertContains(response, "Alchemy")


class TestRitualCreateView(TestCase):
    """Test RitualCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.path = LinearMagicPath.objects.create(
            name="Alchemy",
            numina_type="hedge_magic",
        )

    def test_create_view_accessible_when_logged_in(self):
        """Test that ritual create view is accessible when logged in."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:mage:create:ritual"))
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that correct template is used for ritual create view."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:mage:create:ritual"))
        self.assertTemplateUsed(response, "characters/mage/linear_magic_ritual/form.html")

    def test_create_view_can_create_ritual(self):
        """Test that ritual can be created through the view."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("characters:mage:create:ritual"),
            {
                "name": "Test Ritual",
                "description": "A test ritual",
                "path": self.path.pk,
                "level": 2,
            },
        )
        self.assertTrue(LinearMagicRitual.objects.filter(name="Test Ritual").exists())


class TestRitualUpdateView(TestCase):
    """Test RitualUpdateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.path = LinearMagicPath.objects.create(
            name="Alchemy",
            numina_type="hedge_magic",
        )
        self.ritual = LinearMagicRitual.objects.create(
            name="Purify Water",
            path=self.path,
            level=1,
        )

    def test_update_view_accessible_when_logged_in(self):
        """Test that ritual update view is accessible when logged in."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:mage:update:ritual", kwargs={"pk": self.ritual.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that correct template is used for ritual update view."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:mage:update:ritual", kwargs={"pk": self.ritual.pk})
        )
        self.assertTemplateUsed(response, "characters/mage/linear_magic_ritual/form.html")

    def test_update_view_can_update_ritual(self):
        """Test that ritual can be updated through the view."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("characters:mage:update:ritual", kwargs={"pk": self.ritual.pk}),
            {
                "name": "Updated Purify Water",
                "description": "Updated description",
                "path": self.path.pk,
                "level": 2,
            },
        )
        self.ritual.refresh_from_db()
        self.assertEqual(self.ritual.name, "Updated Purify Water")
        self.assertEqual(self.ritual.level, 2)

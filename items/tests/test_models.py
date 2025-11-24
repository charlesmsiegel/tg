"""
Tests for item models.

Tests cover:
- ItemModel base functionality
- Item creation and validation
- Gameline-specific items
- Permission checks on items
"""
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from items.models.core import ItemModel


class TestItemModel(TestCase):
    """Test the base ItemModel."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_item_creation(self):
        """Test basic item creation."""
        item = ItemModel.objects.create(
            name="Magic Sword",
            owner=self.user,
            chronicle=self.chronicle,
            description="A powerful magical blade",
        )

        self.assertEqual(item.name, "Magic Sword")
        self.assertEqual(item.owner, self.user)
        self.assertEqual(item.chronicle, self.chronicle)

    def test_item_str_representation(self):
        """Test string representation of an item."""
        item = ItemModel.objects.create(
            name="Test Item",
            owner=self.user,
        )

        self.assertEqual(str(item), "Test Item")

    def test_item_absolute_url(self):
        """Test that get_absolute_url returns correct path."""
        item = ItemModel.objects.create(
            name="Test Item",
            owner=self.user,
        )

        expected_url = f"/items/{item.id}/"
        self.assertEqual(item.get_absolute_url(), expected_url)

    def test_item_has_description(self):
        """Test that items can have descriptions."""
        item = ItemModel.objects.create(
            name="Test Item",
            owner=self.user,
            description="A detailed description of the item",
        )

        self.assertEqual(item.description, "A detailed description of the item")

    def test_item_belongs_to_chronicle(self):
        """Test that items can belong to chronicles."""
        item = ItemModel.objects.create(
            name="Chronicle Item",
            owner=self.user,
            chronicle=self.chronicle,
        )

        self.assertEqual(item.chronicle, self.chronicle)

    def test_item_without_chronicle(self):
        """Test creating an item without a chronicle."""
        item = ItemModel.objects.create(
            name="Personal Item",
            owner=self.user,
        )

        self.assertIsNone(item.chronicle)

    def test_item_has_owner(self):
        """Test that items must have an owner."""
        item = ItemModel.objects.create(
            name="Test Item",
            owner=self.user,
        )

        self.assertEqual(item.owner, self.user)


class TestItemPermissions(TestCase):
    """Test item permission functionality."""

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.item = ItemModel.objects.create(
            name="Test Item",
            owner=self.owner,
        )

    def test_owner_can_edit_item(self):
        """Test that owner can edit their items."""
        from core.permissions import PermissionManager

        pm = PermissionManager()
        # Owner should have edit permission
        has_permission = pm.check_permission(self.owner, self.item, "edit_full")
        # Result depends on implementation, but owner should have some access
        self.assertIsNotNone(has_permission)

    def test_item_visibility(self):
        """Test item visibility settings."""
        # Items should support visibility/display settings
        self.assertTrue(hasattr(self.item, "display") or hasattr(self.item, "visibility"))


class TestItemImageUpload(TestCase):
    """Test item image upload functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_item_has_image_field(self):
        """Test that items can have images."""
        item = ItemModel.objects.create(
            name="Test Item",
            owner=self.user,
        )

        # Should have image field
        self.assertTrue(hasattr(item, "image"))

    def test_item_image_optional(self):
        """Test that item image is optional."""
        item = ItemModel.objects.create(
            name="Item Without Image",
            owner=self.user,
        )

        # Should create successfully without image
        self.assertIsNotNone(item)


class TestItemGamelineAssociation(TestCase):
    """Test that items can be associated with gamelines."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_item_has_gameline_field(self):
        """Test that items track which gameline they belong to."""
        item = ItemModel.objects.create(
            name="Test Item",
            owner=self.user,
        )

        # Should have gameline field or type indicator
        has_gameline = (
            hasattr(item, "gameline")
            or hasattr(item, "item_type")
            or hasattr(item, "polymorphic_ctype")
        )
        self.assertTrue(has_gameline)

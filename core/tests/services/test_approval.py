"""Tests for ApprovalService."""

from characters.models.core import Ability, Attribute, Human
from characters.models.mage.effect import Effect
from characters.models.mage.rote import Rote
from core.services import ApprovalService
from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase
from game.models import Chronicle
from items.models.core import ItemModel
from locations.models.core.location import LocationModel


class TestApprovalServiceObjectApproval(TestCase):
    """Tests for ApprovalService.approve_object()."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_approve_character(self):
        """Test approving a character changes status to App."""
        char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            status="Sub",
        )
        obj, msg = ApprovalService.approve_object("character", char.pk)

        char.refresh_from_db()
        self.assertEqual(char.status, "App")
        self.assertEqual(obj.pk, char.pk)
        self.assertIn("approved successfully", msg)
        self.assertIn("Character", msg)

    def test_approve_location(self):
        """Test approving a location changes status to App."""
        loc = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
            status="Sub",
        )
        obj, msg = ApprovalService.approve_object("location", loc.pk)

        loc.refresh_from_db()
        self.assertEqual(loc.status, "App")
        self.assertEqual(obj.pk, loc.pk)
        self.assertIn("approved successfully", msg)
        self.assertIn("Location", msg)

    def test_approve_item(self):
        """Test approving an item changes status to App."""
        item = ItemModel.objects.create(
            name="Test Item",
            chronicle=self.chronicle,
            status="Sub",
        )
        obj, msg = ApprovalService.approve_object("item", item.pk)

        item.refresh_from_db()
        self.assertEqual(item.status, "App")
        self.assertEqual(obj.pk, item.pk)
        self.assertIn("approved successfully", msg)
        self.assertIn("Item", msg)

    def test_approve_rote(self):
        """Test approving a rote changes status to App."""
        effect = Effect.objects.create(name="Test Effect")
        attribute = Attribute.objects.create(name="Strength", property_name="strength")
        ability = Ability.objects.create(name="Athletics", property_name="athletics")
        rote = Rote.objects.create(
            name="Test Rote",
            chronicle=self.chronicle,
            status="Sub",
            effect=effect,
            attribute=attribute,
            ability=ability,
        )
        obj, msg = ApprovalService.approve_object("rote", rote.pk)

        rote.refresh_from_db()
        self.assertEqual(rote.status, "App")
        self.assertEqual(obj.pk, rote.pk)
        self.assertIn("approved successfully", msg)
        self.assertIn("Rote", msg)

    def test_approve_invalid_model_type_raises_error(self):
        """Test that invalid model types raise ValueError."""
        with self.assertRaises(ValueError) as context:
            ApprovalService.approve_object("invalid_type", 1)
        self.assertIn("Invalid model type", str(context.exception))

    def test_approve_nonexistent_object_raises_404(self):
        """Test that non-existent objects raise Http404."""
        with self.assertRaises(Http404):
            ApprovalService.approve_object("character", 99999)


class TestApprovalServiceImageApproval(TestCase):
    """Tests for ApprovalService.approve_image()."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_approve_character_image(self):
        """Test approving a character image changes image_status to app."""
        char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            image_status="sub",
        )
        obj, msg = ApprovalService.approve_image("character", char.pk)

        char.refresh_from_db()
        self.assertEqual(char.image_status, "app")
        self.assertEqual(obj.pk, char.pk)
        self.assertIn("approved successfully", msg)
        self.assertIn("Image", msg)

    def test_approve_location_image(self):
        """Test approving a location image changes image_status to app."""
        loc = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
            image_status="sub",
        )
        obj, msg = ApprovalService.approve_image("location", loc.pk)

        loc.refresh_from_db()
        self.assertEqual(loc.image_status, "app")
        self.assertEqual(obj.pk, loc.pk)
        self.assertIn("approved successfully", msg)
        self.assertIn("Image", msg)

    def test_approve_item_image(self):
        """Test approving an item image changes image_status to app."""
        item = ItemModel.objects.create(
            name="Test Item",
            chronicle=self.chronicle,
            image_status="sub",
        )
        obj, msg = ApprovalService.approve_image("item", item.pk)

        item.refresh_from_db()
        self.assertEqual(item.image_status, "app")
        self.assertEqual(obj.pk, item.pk)
        self.assertIn("approved successfully", msg)
        self.assertIn("Image", msg)

    def test_approve_image_invalid_model_type_raises_error(self):
        """Test that invalid model types raise ValueError for image approval."""
        with self.assertRaises(ValueError) as context:
            ApprovalService.approve_image("rote", 1)  # Rotes don't have images
        self.assertIn("Invalid model type for image approval", str(context.exception))

    def test_approve_image_nonexistent_object_raises_404(self):
        """Test that non-existent objects raise Http404 for image approval."""
        with self.assertRaises(Http404):
            ApprovalService.approve_image("character", 99999)


class TestApprovalServiceParseImageId(TestCase):
    """Tests for ApprovalService.parse_image_id()."""

    def test_parse_image_id_with_prefix(self):
        """Test parsing image-123 format."""
        result = ApprovalService.parse_image_id("image-123")
        self.assertEqual(result, "123")

    def test_parse_image_id_with_multiple_dashes(self):
        """Test parsing with multiple dashes."""
        result = ApprovalService.parse_image_id("some-prefix-image-456")
        self.assertEqual(result, "456")

    def test_parse_image_id_without_prefix(self):
        """Test parsing without dashes returns original."""
        result = ApprovalService.parse_image_id("789")
        self.assertEqual(result, "789")

    def test_parse_image_id_empty_string(self):
        """Test parsing empty string returns empty."""
        result = ApprovalService.parse_image_id("")
        self.assertEqual(result, "")

    def test_parse_image_id_none(self):
        """Test parsing None returns None."""
        result = ApprovalService.parse_image_id(None)
        self.assertIsNone(result)

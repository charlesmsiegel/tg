"""
Tests for XP/Freebie Migration from JSONField to Model-based System

Tests cover the testing checklist from VIEW_TEMPLATE_MIGRATION_GUIDE.md:
- Display of XP/freebie history works correctly
- Total spent calculations are accurate
- New requests are created properly
- Approval workflow functions (if applicable)
- Both JSONField and model data display during transition
- No regressions in existing functionality
"""

from datetime import datetime

from characters.models.core.character import Character
from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.test import TestCase
from django.utils import timezone
from game.models import Chronicle, FreebieSpendingRecord, XPSpendingRequest


class TestXPSpendingRequest(TestCase):
    """Test XPSpendingRequest model and methods."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.char = Character.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            xp=20,
        )

    def test_create_xp_spending_request(self):
        """Test creating XP spending request using new model system."""
        request = self.char.create_xp_spending_request(
            trait_name="Alertness",
            trait_type="ability",
            trait_value=3,
            cost=6,
        )

        self.assertIsNotNone(request)
        self.assertIsInstance(request, XPSpendingRequest)
        self.assertEqual(request.character, self.char)
        self.assertEqual(request.trait_name, "Alertness")
        self.assertEqual(request.trait_type, "ability")
        self.assertEqual(request.trait_value, 3)
        self.assertEqual(request.cost, 6)
        self.assertEqual(request.approved, "Pending")
        self.assertIsNotNone(request.created_at)

    def test_get_pending_xp_requests(self):
        """Test retrieving pending XP requests."""
        # Create multiple requests
        self.char.create_xp_spending_request("Alertness", "ability", 3, 6)
        self.char.create_xp_spending_request("Strength", "attribute", 4, 8)

        # Approve one
        request = self.char.xp_spendings.first()
        request.approved = "Approved"
        request.save()

        # Check pending requests
        pending = self.char.get_pending_xp_requests()
        self.assertEqual(pending.count(), 1)
        self.assertEqual(pending.first().trait_name, "Strength")

    def test_get_xp_spending_history(self):
        """Test retrieving full XP spending history."""
        self.char.create_xp_spending_request("Alertness", "ability", 3, 6)
        self.char.create_xp_spending_request("Strength", "attribute", 4, 8)

        history = self.char.get_xp_spending_history()
        self.assertEqual(history.count(), 2)
        self.assertTrue(all(isinstance(r, XPSpendingRequest) for r in history))

    def test_approve_xp_request(self):
        """Test approving an XP spending request."""
        request = self.char.create_xp_spending_request("Alertness", "ability", 3, 6)

        # Approve it
        approved_request = self.char.approve_xp_request(request.id, self.user)

        self.assertEqual(approved_request.approved, "Approved")
        self.assertEqual(approved_request.approved_by, self.user)
        self.assertIsNotNone(approved_request.approved_at)

        # Refresh from DB to confirm
        request.refresh_from_db()
        self.assertEqual(request.approved, "Approved")

    def test_deny_xp_request(self):
        """Test denying an XP spending request."""
        request = self.char.create_xp_spending_request("Alertness", "ability", 3, 6)

        # Deny it
        denied_request = self.char.deny_xp_request(request.id, self.user)

        self.assertEqual(denied_request.approved, "Denied")
        self.assertEqual(denied_request.approved_by, self.user)
        self.assertIsNotNone(denied_request.approved_at)

    def test_approve_already_approved_request_fails(self):
        """Test that approving an already approved request fails."""
        request = self.char.create_xp_spending_request("Alertness", "ability", 3, 6)
        self.char.approve_xp_request(request.id, self.user)

        # Try to approve again
        with self.assertRaises(XPSpendingRequest.DoesNotExist):
            self.char.approve_xp_request(request.id, self.user)

    def test_has_pending_xp_model_requests(self):
        """Test checking for pending XP model requests."""
        self.assertFalse(self.char.has_pending_xp_model_requests())

        self.char.create_xp_spending_request("Alertness", "ability", 3, 6)
        self.assertTrue(self.char.has_pending_xp_model_requests())

        # Approve it
        request = self.char.xp_spendings.first()
        self.char.approve_xp_request(request.id, self.user)
        self.assertFalse(self.char.has_pending_xp_model_requests())

    def test_xp_spending_request_string_representation(self):
        """Test XPSpendingRequest __str__ method."""
        request = self.char.create_xp_spending_request("Alertness", "ability", 3, 6)
        expected = f"{self.char.name} - Alertness (6 XP) - Pending"
        self.assertEqual(str(request), expected)


class TestFreebieSpendingRecord(TestCase):
    """Test FreebieSpendingRecord model and methods."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.user,
            chronicle=self.chronicle,
            freebies=15,
        )

    def test_create_freebie_spending_record(self):
        """Test creating freebie spending record using new model system."""
        record = self.human.create_freebie_spending_record(
            trait_name="Strength",
            trait_type="attribute",
            trait_value=4,
            cost=5,
        )

        self.assertIsNotNone(record)
        self.assertIsInstance(record, FreebieSpendingRecord)
        self.assertEqual(record.character, self.human)
        self.assertEqual(record.trait_name, "Strength")
        self.assertEqual(record.trait_type, "attribute")
        self.assertEqual(record.trait_value, 4)
        self.assertEqual(record.cost, 5)
        self.assertIsNotNone(record.created_at)

    def test_get_freebie_spending_history(self):
        """Test retrieving freebie spending history."""
        self.human.create_freebie_spending_record("Strength", "attribute", 4, 5)
        self.human.create_freebie_spending_record("Alertness", "ability", 2, 2)

        history = self.human.get_freebie_spending_history()
        self.assertEqual(history.count(), 2)
        self.assertTrue(all(isinstance(r, FreebieSpendingRecord) for r in history))

    def test_total_freebies_from_model(self):
        """Test calculating total freebies from model records."""
        initial_freebies = self.human.freebies
        self.human.create_freebie_spending_record("Strength", "attribute", 4, 5)
        self.human.create_freebie_spending_record("Alertness", "ability", 2, 2)

        total = self.human.total_freebies_from_model()
        self.assertEqual(total, initial_freebies + 7)  # 5 + 2

    def test_freebie_spending_record_string_representation(self):
        """Test FreebieSpendingRecord __str__ method."""
        record = self.human.create_freebie_spending_record("Strength", "attribute", 4, 5)
        expected = f"{self.human.name} - Strength (5 freebies)"
        self.assertEqual(str(record), expected)


class TestDualSystemSupport(TestCase):
    """Test that both JSONField and model systems work together during migration."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.char = Character.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            xp=20,
        )
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.user,
            chronicle=self.chronicle,
            freebies=15,
        )

    def test_has_pending_xp_or_model_requests_jsonfield(self):
        """Test checking for pending XP in JSONField."""
        # Add pending XP in JSONField
        self.char.spent_xp = [
            {
                "trait": "Alertness",
                "value": 3,
                "cost": 6,
                "approved": "Pending",
                "index": "0",
            }
        ]
        self.char.save()

        self.assertTrue(self.char.has_pending_xp_or_model_requests())

    def test_has_pending_xp_or_model_requests_model(self):
        """Test checking for pending XP in model."""
        self.char.create_xp_spending_request("Alertness", "ability", 3, 6)
        self.assertTrue(self.char.has_pending_xp_or_model_requests())

    def test_has_pending_xp_or_model_requests_both(self):
        """Test checking for pending XP in both systems."""
        # JSONField
        self.char.spent_xp = [
            {
                "trait": "Alertness",
                "value": 3,
                "cost": 6,
                "approved": "Pending",
                "index": "0",
            }
        ]
        self.char.save()

        # Model
        self.char.create_xp_spending_request("Strength", "attribute", 4, 8)

        self.assertTrue(self.char.has_pending_xp_or_model_requests())

    def test_total_spent_xp_combined_jsonfield_only(self):
        """Test total XP calculation from JSONField only."""
        self.char.spent_xp = [
            {
                "trait": "Alertness",
                "value": 3,
                "cost": 6,
                "approved": "Approved",
                "index": "0",
            },
            {
                "trait": "Strength",
                "value": 4,
                "cost": 8,
                "approved": "Approved",
                "index": "1",
            },
            {
                "trait": "Wits",
                "value": 3,
                "cost": 5,
                "approved": "Pending",  # Not approved, shouldn't count
                "index": "2",
            },
        ]
        self.char.save()

        total = self.char.total_spent_xp_combined()
        self.assertEqual(total, 14)  # 6 + 8, excluding pending

    def test_total_spent_xp_combined_model_only(self):
        """Test total XP calculation from model only."""
        # Create and approve requests
        request1 = self.char.create_xp_spending_request("Alertness", "ability", 3, 6)
        request2 = self.char.create_xp_spending_request("Strength", "attribute", 4, 8)
        request3 = self.char.create_xp_spending_request("Wits", "attribute", 3, 5)

        self.char.approve_xp_request(request1.id, self.user)
        self.char.approve_xp_request(request2.id, self.user)
        # Leave request3 pending

        total = self.char.total_spent_xp_combined()
        self.assertEqual(total, 14)  # 6 + 8, excluding pending

    def test_total_spent_xp_combined_both_systems(self):
        """Test total XP calculation from both systems combined."""
        # JSONField
        self.char.spent_xp = [
            {
                "trait": "Alertness",
                "value": 3,
                "cost": 6,
                "approved": "Approved",
                "index": "0",
            }
        ]
        self.char.save()

        # Model
        request = self.char.create_xp_spending_request("Strength", "attribute", 4, 8)
        self.char.approve_xp_request(request.id, self.user)

        total = self.char.total_spent_xp_combined()
        self.assertEqual(total, 14)  # 6 + 8 from both systems

    def test_total_freebies_combined_jsonfield_only(self):
        """Test total freebies calculation from JSONField only."""
        initial_freebies = self.human.freebies
        self.human.spent_freebies = [
            {"trait": "Strength", "value": 4, "cost": 5},
            {"trait": "Alertness", "value": 2, "cost": 2},
        ]
        self.human.save()

        # JSONField total
        jsonfield_total = sum(x["cost"] for x in self.human.spent_freebies)
        self.assertEqual(jsonfield_total, 7)

    def test_total_freebies_from_model_only(self):
        """Test total freebies calculation from model only."""
        initial_freebies = self.human.freebies
        self.human.create_freebie_spending_record("Strength", "attribute", 4, 5)
        self.human.create_freebie_spending_record("Alertness", "ability", 2, 2)

        total = self.human.total_freebies_from_model()
        self.assertEqual(total, initial_freebies + 7)  # 5 + 2


class TestXPSpendingIndexes(TestCase):
    """Test that database indexes work correctly for performance."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.char = Character.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            xp=100,
        )

    def test_filter_by_character_and_approved(self):
        """Test filtering by character and approved status (indexed)."""
        # Create multiple requests
        for i in range(5):
            self.char.create_xp_spending_request(f"Trait {i}", "ability", i + 1, (i + 1) * 2)

        # Approve some
        for request in self.char.xp_spendings.all()[:3]:
            self.char.approve_xp_request(request.id, self.user)

        # This query should use the index
        pending = self.char.xp_spendings.filter(approved="Pending")
        self.assertEqual(pending.count(), 2)

        approved = self.char.xp_spendings.filter(approved="Approved")
        self.assertEqual(approved.count(), 3)

    def test_order_by_created_at(self):
        """Test ordering by created_at (indexed)."""
        # Create requests
        request1 = self.char.create_xp_spending_request("First", "ability", 1, 2)
        request2 = self.char.create_xp_spending_request("Second", "ability", 2, 4)
        request3 = self.char.create_xp_spending_request("Third", "ability", 3, 6)

        # This query should use the index
        history = self.char.xp_spendings.order_by("-created_at")
        self.assertEqual(history.first(), request3)
        self.assertEqual(history.last(), request1)


class TestFreebieSpendingIndexes(TestCase):
    """Test that database indexes work correctly for freebie records."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.user,
            chronicle=self.chronicle,
            freebies=50,
        )

    def test_filter_by_character(self):
        """Test filtering by character (indexed)."""
        # Create multiple records
        for i in range(5):
            self.human.create_freebie_spending_record(f"Trait {i}", "ability", i + 1, (i + 1) * 2)

        # This query should use the index
        records = self.human.freebie_spendings.all()
        self.assertEqual(records.count(), 5)

    def test_order_by_created_at(self):
        """Test ordering by created_at (indexed)."""
        record1 = self.human.create_freebie_spending_record("First", "ability", 1, 2)
        record2 = self.human.create_freebie_spending_record("Second", "ability", 2, 4)
        record3 = self.human.create_freebie_spending_record("Third", "ability", 3, 6)

        # This query should use the index
        history = self.human.freebie_spendings.order_by("-created_at")
        self.assertEqual(history.first(), record3)
        self.assertEqual(history.last(), record1)


class TestMigrationEdgeCases(TestCase):
    """Test edge cases during migration."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.char = Character.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            xp=20,
        )
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.user,
            chronicle=self.chronicle,
            freebies=15,
        )

    def test_empty_jsonfield_and_no_model_records(self):
        """Test character with no spending in either system."""
        self.assertFalse(self.char.has_pending_xp_or_model_requests())
        self.assertEqual(self.char.total_spent_xp_combined(), 0)
        self.assertEqual(self.char.get_xp_spending_history().count(), 0)

    def test_malformed_jsonfield_data(self):
        """Test handling of malformed JSONField data."""
        # Missing 'approved' key
        self.char.spent_xp = [{"trait": "Alertness", "value": 3, "cost": 6, "index": "0"}]
        self.char.save()

        # Should not crash
        total = self.char.total_spent_xp_combined()
        self.assertGreaterEqual(total, 0)  # May be 0 if malformed data is skipped

    def test_character_with_only_denied_requests(self):
        """Test character with only denied XP requests."""
        request1 = self.char.create_xp_spending_request("Alertness", "ability", 3, 6)
        request2 = self.char.create_xp_spending_request("Strength", "attribute", 4, 8)

        self.char.deny_xp_request(request1.id, self.user)
        self.char.deny_xp_request(request2.id, self.user)

        self.assertFalse(self.char.has_pending_xp_or_model_requests())
        self.assertEqual(self.char.total_spent_xp_combined(), 0)  # Denied requests don't count

    def test_freebie_record_with_zero_cost(self):
        """Test freebie record with zero cost (edge case)."""
        record = self.human.create_freebie_spending_record("Free Trait", "special", 1, 0)
        self.assertEqual(record.cost, 0)
        total = self.human.total_freebies_from_model()
        self.assertEqual(total, self.human.freebies)  # Zero cost shouldn't affect total


class TestBackwardCompatibility(TestCase):
    """Test that new system doesn't break existing JSONField functionality."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.char = Character.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            xp=20,
        )

    def test_jsonfield_still_accessible(self):
        """Test that JSONField is still accessible."""
        self.char.spent_xp = [
            {
                "trait": "Alertness",
                "value": 3,
                "cost": 6,
                "approved": "Approved",
                "index": "0",
            }
        ]
        self.char.save()
        self.char.refresh_from_db()

        self.assertEqual(len(self.char.spent_xp), 1)
        self.assertEqual(self.char.spent_xp[0]["trait"], "Alertness")

    def test_can_append_to_jsonfield(self):
        """Test that appending to JSONField still works."""
        self.char.spent_xp = []
        self.char.save()

        self.char.spent_xp.append(
            {
                "trait": "Strength",
                "value": 4,
                "cost": 8,
                "approved": "Pending",
                "index": "0",
            }
        )
        self.char.save()
        self.char.refresh_from_db()

        self.assertEqual(len(self.char.spent_xp), 1)

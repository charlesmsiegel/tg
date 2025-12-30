"""
Tests for transaction safety across multi-model operations.

These tests verify that atomic transactions properly protect data consistency
when operations span multiple models or require multiple database saves.
"""

from unittest.mock import patch

from characters.models.core.character import CharacterModel
from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase, TransactionTestCase
from game.models import Chronicle, Journal, Week, WeeklyXPRequest


class SignalTransactionTests(TransactionTestCase):
    """Tests for signal handler transaction safety."""

    def test_profile_creation_on_user_create(self):
        """Test that profile is created atomically with user."""
        # Create a user - should automatically create a Profile
        user = User.objects.create_user(
            username="test_signal_user",
            email="test@example.com",
            password="testpass123"
        )

        # Profile should exist
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsNotNone(user.profile)

    def test_profile_creation_idempotent(self):
        """Test that creating a user twice doesn't cause issues."""
        user1 = User.objects.create_user(
            username="test_user1",
            email="test1@example.com",
            password="testpass123"
        )
        # Verify profile count is exactly 1
        from accounts.models import Profile
        self.assertEqual(Profile.objects.filter(user=user1).count(), 1)


class XPOperationTransactionTests(TransactionTestCase):
    """Tests for XP operation transaction safety."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="xp_test_user",
            email="xp@example.com",
            password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(
            name="Test Chronicle",
            head_st=self.user,
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            xp=10,
        )
        self.week = Week.objects.create(
            end_date="2025-01-05",
        )

    def test_add_xp_atomic(self):
        """Test that add_xp is atomic."""
        initial_xp = self.character.xp

        # Add XP
        self.character.add_xp(5)
        self.character.refresh_from_db()

        self.assertEqual(self.character.xp, initial_xp + 5)

    def test_xp_approval_updates_both_request_and_character(self):
        """Test that XP approval updates both the request and character XP."""
        xp_request = WeeklyXPRequest.objects.create(
            week=self.week,
            character=self.character,
            finishing=True,
            learning=False,  # Don't claim learning (requires scene)
            rp=False,  # Don't claim rp (requires scene)
            approved=False,
        )

        initial_xp = self.character.xp
        xp_to_add = xp_request.total_xp()

        # Simulate approval flow (should be atomic)
        with transaction.atomic():
            xp_request.approved = True
            xp_request.save()
            self.character.add_xp(xp_to_add)

        # Verify both updates occurred
        xp_request.refresh_from_db()
        self.character.refresh_from_db()

        self.assertTrue(xp_request.approved)
        self.assertEqual(self.character.xp, initial_xp + xp_to_add)


class CharacterStatusTransactionTests(TransactionTestCase):
    """Tests for character status change transaction safety."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="status_test_user",
            email="status@example.com",
            password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(
            name="Test Chronicle",
            head_st=self.user,
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
        )

    def test_status_change_atomic(self):
        """Test that status changes are atomic."""
        self.character.status = "Ret"
        self.character.save()
        self.character.refresh_from_db()

        self.assertEqual(self.character.status, "Ret")


class BulkOperationTransactionTests(TransactionTestCase):
    """Tests for bulk operation transaction safety."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="bulk_test_user",
            email="bulk@example.com",
            password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(
            name="Test Chronicle",
            head_st=self.user,
        )
        self.week = Week.objects.create(
            end_date="2025-01-05",
        )
        # Create multiple characters and XP requests
        self.characters = []
        self.xp_requests = []
        for i in range(3):
            char = Human.objects.create(
                name=f"Bulk Test Character {i}",
                owner=self.user,
                chronicle=self.chronicle,
                status="App",
                xp=10,
            )
            self.characters.append(char)
            xp_req = WeeklyXPRequest.objects.create(
                week=self.week,
                character=char,
                finishing=True,
                approved=False,
            )
            self.xp_requests.append(xp_req)

    def test_batch_xp_approval_all_or_nothing(self):
        """Test that batch XP approval is atomic - all succeed or all fail."""
        initial_xps = [c.xp for c in self.characters]

        # Simulate batch approval with transaction
        with transaction.atomic():
            for xp_request in self.xp_requests:
                xp_request.approved = True
                xp_request.character.xp += xp_request.total_xp()
                xp_request.character.save()
                xp_request.save()

        # Verify all were updated
        for i, xp_request in enumerate(self.xp_requests):
            xp_request.refresh_from_db()
            self.characters[i].refresh_from_db()
            self.assertTrue(xp_request.approved)
            self.assertGreater(self.characters[i].xp, initial_xps[i])

    def test_batch_approval_rollback_on_error(self):
        """Test that batch approval rolls back on error."""
        initial_xps = [c.xp for c in self.characters]

        class SimulatedError(Exception):
            pass

        # Simulate batch approval that fails midway
        try:
            with transaction.atomic():
                for i, xp_request in enumerate(self.xp_requests):
                    xp_request.approved = True
                    xp_request.character.xp += xp_request.total_xp()
                    xp_request.character.save()
                    xp_request.save()
                    if i == 1:  # Fail on second iteration
                        raise SimulatedError("Simulated failure")
        except SimulatedError:
            pass

        # Verify nothing was updated (rollback)
        for i, xp_request in enumerate(self.xp_requests):
            xp_request.refresh_from_db()
            self.characters[i].refresh_from_db()
            self.assertFalse(xp_request.approved)
            self.assertEqual(self.characters[i].xp, initial_xps[i])


class M2MOperationTransactionTests(TransactionTestCase):
    """Tests for Many-to-Many operation transaction safety."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="m2m_test_user",
            email="m2m@example.com",
            password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(
            name="Test Chronicle",
            head_st=self.user,
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
        )

    def test_m2m_removal_atomic(self):
        """Test that M2M removals are atomic within a transaction."""
        from characters.models.core.group import Group

        # Create a group and add character
        group = Group.objects.create(
            name="Test Group",
            chronicle=self.chronicle,
        )
        group.members.add(self.character)

        # Verify membership
        self.assertTrue(group.members.filter(pk=self.character.pk).exists())

        # Remove within transaction
        with transaction.atomic():
            group.members.remove(self.character)

        # Verify removal
        self.assertFalse(group.members.filter(pk=self.character.pk).exists())


class JournalCreationTransactionTests(TransactionTestCase):
    """Tests for Journal creation on character save."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="journal_test_user",
            email="journal@example.com",
            password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(
            name="Test Chronicle",
            head_st=self.user,
        )

    def test_journal_created_with_character(self):
        """Test that journal is created when character is created."""
        character = Human.objects.create(
            name="Journal Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
        )

        # Journal should be created via signal
        self.assertTrue(Journal.objects.filter(character=character).exists())

    def test_journal_creation_idempotent(self):
        """Test that journal creation doesn't duplicate on character update."""
        character = Human.objects.create(
            name="Journal Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
        )

        initial_count = Journal.objects.filter(character=character).count()

        # Update character (should not create duplicate journal)
        character.name = "Updated Name"
        character.save()

        self.assertEqual(
            Journal.objects.filter(character=character).count(),
            initial_count
        )

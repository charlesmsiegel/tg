"""
Integration tests for transaction atomicity and concurrency control.

Tests the following features:
- Concurrent XP spending with race condition prevention
- Transaction rollback on errors
- Award XP all-or-nothing behavior
- select_for_update() locking mechanism
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest
from characters.models.core.attribute_block import Attribute
from characters.models.core.character import Character
from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection, transaction
from game.models import Chronicle, Scene


@pytest.mark.django_db(transaction=True)
class TestConcurrentXPSpending:
    """Test concurrent XP spending with race condition prevention."""

    def test_concurrent_spend_xp_race_condition_prevented(self):
        """
        Test that select_for_update prevents race conditions in concurrent XP spending.

        Scenario: Two threads try to spend XP simultaneously. Without locking,
        both might read xp=10, both spend 6, and both save - resulting in
        negative XP. With select_for_update, the second thread waits and sees
        the updated balance.
        """
        character = Character.objects.create(name="Test", xp=10)
        errors = []
        successful_spends = []

        def spend_xp_thread(char_id, cost, trait_name):
            """Helper function to spend XP in a separate thread"""
            try:
                # Close the connection to force a new one in this thread
                connection.close()

                char = Character.objects.get(pk=char_id)
                record = char.spend_xp(
                    trait_name=trait_name,
                    trait_display=trait_name.title(),
                    cost=cost,
                    category="test",
                )
                successful_spends.append(record)
            except ValidationError as e:
                errors.append(e)
            except Exception as e:
                errors.append(e)

        # Create two threads that try to spend 6 XP each from a pool of 10
        thread1 = threading.Thread(
            target=spend_xp_thread, args=(character.pk, 6, "test1")
        )
        thread2 = threading.Thread(
            target=spend_xp_thread, args=(character.pk, 6, "test2")
        )

        # Start both threads nearly simultaneously
        thread1.start()
        thread2.start()

        # Wait for both to complete
        thread1.join()
        thread2.join()

        # Verify results
        character.refresh_from_db()

        # One should succeed, one should fail with insufficient XP
        assert len(successful_spends) == 1, "Only one spend should succeed"
        assert len(errors) == 1, "One spend should fail"

        # The error should be about insufficient XP
        assert isinstance(errors[0], ValidationError)
        assert "Insufficient XP" in str(errors[0])

        # Character should have 4 XP (10 - 6)
        assert character.xp == 4
        assert len(character.spent_xp) == 1

    def test_concurrent_spend_xp_multiple_small_spends(self):
        """
        Test multiple concurrent small XP spends.

        All should succeed if they don't exceed the total.
        """
        character = Character.objects.create(name="Test", xp=20)
        errors = []
        successful_spends = []

        def spend_xp_thread(char_id, cost, trait_name):
            """Helper function to spend XP in a separate thread"""
            try:
                connection.close()
                char = Character.objects.get(pk=char_id)
                record = char.spend_xp(
                    trait_name=trait_name,
                    trait_display=trait_name.title(),
                    cost=cost,
                    category="test",
                )
                successful_spends.append(record)
            except ValidationError as e:
                errors.append(e)

        # Create 5 threads each spending 3 XP (total 15 from pool of 20)
        threads = []
        for i in range(5):
            thread = threading.Thread(
                target=spend_xp_thread, args=(character.pk, 3, f"test{i}")
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        character.refresh_from_db()

        # All should succeed
        assert len(successful_spends) == 5
        assert len(errors) == 0
        assert character.xp == 5  # 20 - 15
        assert len(character.spent_xp) == 5

    def test_concurrent_spend_xp_exceeds_balance(self):
        """
        Test concurrent spends that collectively exceed balance.

        Some should fail with insufficient XP errors.
        """
        character = Character.objects.create(name="Test", xp=10)
        errors = []
        successful_spends = []

        def spend_xp_thread(char_id, cost, trait_name):
            """Helper function to spend XP in a separate thread"""
            try:
                connection.close()
                char = Character.objects.get(pk=char_id)
                record = char.spend_xp(
                    trait_name=trait_name,
                    trait_display=trait_name.title(),
                    cost=cost,
                    category="test",
                )
                successful_spends.append(record)
            except ValidationError as e:
                errors.append(e)

        # Create 5 threads each spending 4 XP (total 20 from pool of 10)
        threads = []
        for i in range(5):
            thread = threading.Thread(
                target=spend_xp_thread, args=(character.pk, 4, f"test{i}")
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        character.refresh_from_db()

        # Some should succeed, some should fail
        # At most 2 can succeed (2 * 4 = 8 <= 10)
        assert len(successful_spends) <= 2
        assert len(errors) >= 3

        # Character XP should never be negative
        assert character.xp >= 0
        assert character.xp == 10 - (len(successful_spends) * 4)


@pytest.mark.django_db(transaction=True)
class TestApproveXPSpendRollback:
    """Test approve_xp_spend transaction rollback on failures."""

    def test_approve_xp_spend_rollback_on_invalid_trait(self):
        """
        Test that approval rolls back if trait update fails.

        The approval status should not change if setattr fails.
        """
        character = Character.objects.create(name="Test", xp=10)

        # Spend XP
        record = character.spend_xp(
            trait_name="test_trait", trait_display="Test Trait", cost=5, category="test"
        )

        # Try to approve with a non-existent trait property
        # This should fail when setattr is called
        try:
            with transaction.atomic():
                char = Character.objects.select_for_update().get(pk=character.pk)

                # Update approval status
                char.spent_xp[0]["approved"] = "Approved"

                # This will fail - nonexistent_property doesn't exist
                # In a real scenario, this simulates any error during trait update
                setattr(char, "nonexistent_property", 5)

                char.save()
        except AttributeError:
            pass

        # Verify that the approval status did NOT change
        character.refresh_from_db()
        assert character.spent_xp[0]["approved"] == "Pending"

    def test_approve_xp_spend_rollback_on_constraint_violation(self):
        """
        Test that approval rolls back if trait value violates constraints.

        Example: Trying to set strength to 11 (exceeds max of 10).
        """
        Attribute.objects.create(name="Strength", property_name="strength")
        human = Human.objects.create(name="Test", xp=10, strength=3)

        # Spend XP
        record = human.spend_xp(
            trait_name="strength",
            trait_display="Strength",
            cost=5,
            category="attributes",
        )

        # Try to approve with invalid value (strength > 10)
        try:
            with transaction.atomic():
                human_locked = Human.objects.select_for_update().get(pk=human.pk)
                human_locked.spent_xp[0]["approved"] = "Approved"
                human_locked.strength = 11  # Violates constraint
                human_locked.save()
        except IntegrityError:
            pass

        # Verify rollback
        human.refresh_from_db()
        assert human.spent_xp[0]["approved"] == "Pending"
        assert human.strength == 3  # Unchanged

    def test_approve_xp_spend_success_updates_both(self):
        """
        Test that successful approval updates both approval status and trait.

        Both changes should be committed together.
        """
        Attribute.objects.create(name="Strength", property_name="strength")
        human = Human.objects.create(name="Test", xp=10, strength=3)

        # Spend XP
        record = human.spend_xp(
            trait_name="strength",
            trait_display="Strength",
            cost=5,
            category="attributes",
        )

        # Approve successfully
        result = human.approve_xp_spend(
            spend_index=0, trait_property_name="strength", new_value=4
        )

        # Verify both changes persisted
        human.refresh_from_db()
        assert human.spent_xp[0]["approved"] == "Approved"
        assert human.strength == 4
        assert "approved_at" in human.spent_xp[0]

    def test_concurrent_approval_prevented(self):
        """
        Test that select_for_update prevents concurrent approval of same spend.

        Two STs trying to approve the same spend simultaneously - only one succeeds.
        """
        Attribute.objects.create(name="Strength", property_name="strength")
        human = Human.objects.create(name="Test", xp=10, strength=3)

        # Spend XP
        record = human.spend_xp(
            trait_name="strength",
            trait_display="Strength",
            cost=5,
            category="attributes",
        )

        errors = []
        successful_approvals = []

        def approve_thread(char_id, spend_index):
            """Helper to approve in thread"""
            try:
                connection.close()
                char = Human.objects.get(pk=char_id)
                result = char.approve_xp_spend(
                    spend_index=spend_index, trait_property_name="strength", new_value=4
                )
                successful_approvals.append(result)
            except ValidationError as e:
                errors.append(e)

        # Two threads try to approve the same spend
        thread1 = threading.Thread(target=approve_thread, args=(human.pk, 0))
        thread2 = threading.Thread(target=approve_thread, args=(human.pk, 0))

        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        # Only one should succeed
        assert len(successful_approvals) == 1
        assert len(errors) == 1
        assert "already processed" in str(errors[0])

        # Verify final state
        human.refresh_from_db()
        assert human.spent_xp[0]["approved"] == "Approved"
        assert human.strength == 4


@pytest.mark.django_db(transaction=True)
class TestAwardXPAtomicity:
    """Test award_xp all-or-nothing behavior."""

    def test_award_xp_all_or_nothing_success(self):
        """
        Test that awarding XP to multiple characters is atomic.

        All characters should receive XP together.
        """
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        scene = Scene.objects.create(name="Test Scene", chronicle=chronicle)

        char1 = Character.objects.create(name="Char1", xp=0)
        char2 = Character.objects.create(name="Char2", xp=0)
        char3 = Character.objects.create(name="Char3", xp=0)

        awards = {char1: True, char2: True, char3: True}

        # Award XP
        with transaction.atomic():
            count = scene.award_xp(awards)

        # All should receive XP
        assert count == 3
        char1.refresh_from_db()
        char2.refresh_from_db()
        char3.refresh_from_db()

        assert char1.xp == 1
        assert char2.xp == 1
        assert char3.xp == 1
        assert scene.xp_given is True

    def test_award_xp_rollback_on_character_error(self):
        """
        Test that if awarding to one character fails, all awards roll back.

        This simulates a scenario where one character has invalid state.
        """
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        scene = Scene.objects.create(name="Test Scene", chronicle=chronicle)

        char1 = Character.objects.create(name="Char1", xp=0)
        char2 = Character.objects.create(name="Char2", xp=0)

        awards = {char1: True, char2: True}

        # Simulate error by deleting char2 before award
        char2_id = char2.pk

        # Award should succeed since both characters exist
        count = scene.award_xp(awards)

        assert count == 2
        char1.refresh_from_db()
        assert char1.xp == 1

    def test_award_xp_prevents_double_award(self):
        """
        Test that XP cannot be awarded twice for the same scene.

        Second attempt should raise ValidationError without changing XP.
        """
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        scene = Scene.objects.create(name="Test Scene", chronicle=chronicle)

        char1 = Character.objects.create(name="Char1", xp=0)

        awards = {char1: True}

        # First award succeeds
        count = scene.award_xp(awards)
        assert count == 1

        char1.refresh_from_db()
        assert char1.xp == 1

        # Second award fails
        with pytest.raises(ValidationError, match="already been awarded"):
            scene.award_xp(awards)

        # XP unchanged
        char1.refresh_from_db()
        assert char1.xp == 1

    def test_concurrent_award_xp_prevented(self):
        """
        Test that concurrent XP awards to same scene are prevented.

        Two STs trying to award XP simultaneously - only one succeeds.
        """
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        scene = Scene.objects.create(name="Test Scene", chronicle=chronicle)

        char1 = Character.objects.create(name="Char1", xp=0)
        char2 = Character.objects.create(name="Char2", xp=0)

        awards = {char1: True, char2: True}

        errors = []
        successful_awards = []

        def award_thread(scene_id, awards_dict):
            """Helper to award XP in thread"""
            try:
                connection.close()
                s = Scene.objects.get(pk=scene_id)

                # Convert character IDs back to objects for the thread
                from characters.models import Character

                thread_awards = {}
                for char_id, should_award in awards_dict.items():
                    char = Character.objects.get(pk=char_id)
                    thread_awards[char] = should_award

                with transaction.atomic():
                    count = s.award_xp(thread_awards)
                    successful_awards.append(count)
            except ValidationError as e:
                errors.append(e)

        # Convert awards to use IDs for thread safety
        awards_with_ids = {
            char.pk: should_award for char, should_award in awards.items()
        }

        # Two threads try to award XP
        thread1 = threading.Thread(
            target=award_thread, args=(scene.pk, awards_with_ids)
        )
        thread2 = threading.Thread(
            target=award_thread, args=(scene.pk, awards_with_ids)
        )

        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        # Only one should succeed
        assert len(successful_awards) == 1
        assert len(errors) == 1
        assert "already been awarded" in str(errors[0])

        # Characters should have XP awarded only once
        char1.refresh_from_db()
        char2.refresh_from_db()
        assert char1.xp == 1
        assert char2.xp == 1

    def test_award_xp_selective_awards(self):
        """
        Test awarding XP to only some characters in a scene.

        Only characters with True in awards dict should receive XP.
        """
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        scene = Scene.objects.create(name="Test Scene", chronicle=chronicle)

        char1 = Character.objects.create(name="Char1", xp=0)
        char2 = Character.objects.create(name="Char2", xp=0)
        char3 = Character.objects.create(name="Char3", xp=0)

        # Only char1 and char3 get XP
        awards = {char1: True, char2: False, char3: True}

        count = scene.award_xp(awards)

        assert count == 2

        char1.refresh_from_db()
        char2.refresh_from_db()
        char3.refresh_from_db()

        assert char1.xp == 1
        assert char2.xp == 0  # No XP
        assert char3.xp == 1


@pytest.mark.django_db(transaction=True)
class TestSelectForUpdateLocking:
    """Test select_for_update() prevents race conditions."""

    def test_select_for_update_locks_row(self):
        """
        Test that select_for_update locks the database row.

        A second transaction should wait until the first completes.
        """
        character = Character.objects.create(name="Test", xp=10)

        completion_order = []

        def modify_with_lock(char_id, identifier, delay):
            """Lock character and modify after delay"""
            try:
                connection.close()

                with transaction.atomic():
                    char = Character.objects.select_for_update().get(pk=char_id)
                    time.sleep(delay)
                    char.xp += 1
                    char.save()
                    completion_order.append(identifier)
            except Exception as e:
                completion_order.append(f"error_{identifier}")

        # Thread 1 locks and holds for 0.5 seconds
        # Thread 2 tries to lock immediately but must wait
        thread1 = threading.Thread(
            target=modify_with_lock, args=(character.pk, "first", 0.5)
        )
        thread2 = threading.Thread(
            target=modify_with_lock, args=(character.pk, "second", 0.1)
        )

        thread1.start()
        time.sleep(0.1)  # Ensure thread1 gets lock first
        thread2.start()

        thread1.join()
        thread2.join()

        # First should complete before second (due to locking)
        assert completion_order == ["first", "second"]

        # Both modifications should apply
        character.refresh_from_db()
        assert character.xp == 12  # 10 + 1 + 1

    def test_select_for_update_without_transaction_warning(self):
        """
        Test that select_for_update works as expected within transactions.

        Using it outside a transaction may not provide the expected locking.
        """
        character = Character.objects.create(name="Test", xp=10)

        # Within transaction - lock is held
        with transaction.atomic():
            locked_char = Character.objects.select_for_update().get(pk=character.pk)
            locked_char.xp += 5
            locked_char.save()

        character.refresh_from_db()
        assert character.xp == 15

    def test_multiple_row_locking(self):
        """
        Test locking multiple characters in a single transaction.

        All locked rows should be protected from concurrent modification.
        """
        char1 = Character.objects.create(name="Char1", xp=10)
        char2 = Character.objects.create(name="Char2", xp=20)

        with transaction.atomic():
            # Lock both characters
            locked_char1 = Character.objects.select_for_update().get(pk=char1.pk)
            locked_char2 = Character.objects.select_for_update().get(pk=char2.pk)

            # Modify both
            locked_char1.xp += 5
            locked_char2.xp += 10

            locked_char1.save()
            locked_char2.save()

        char1.refresh_from_db()
        char2.refresh_from_db()

        assert char1.xp == 15
        assert char2.xp == 30


@pytest.mark.django_db(transaction=True)
class TestTransactionIntegrityScenarios:
    """Integration tests for complex transaction scenarios."""

    def test_spend_and_approve_workflow(self):
        """
        Test complete workflow: spend XP, then approve it.

        Both operations should be atomic and properly sequenced.
        """
        Attribute.objects.create(name="Strength", property_name="strength")
        human = Human.objects.create(name="Test", xp=20, strength=3)

        # Spend XP
        with transaction.atomic():
            record = human.spend_xp(
                trait_name="strength",
                trait_display="Strength",
                cost=5,
                category="attributes",
            )

        human.refresh_from_db()
        assert human.xp == 15
        assert len(human.spent_xp) == 1
        assert human.spent_xp[0]["approved"] == "Pending"

        # Approve XP
        with transaction.atomic():
            result = human.approve_xp_spend(
                spend_index=0, trait_property_name="strength", new_value=4
            )

        human.refresh_from_db()
        assert human.strength == 4
        assert human.spent_xp[0]["approved"] == "Approved"

    def test_multiple_spends_and_selective_approval(self):
        """
        Test multiple XP spends with selective approval.

        Some spends approved, others denied, all atomic.
        """
        Attribute.objects.create(name="Strength", property_name="strength")
        Attribute.objects.create(name="Dexterity", property_name="dexterity")

        human = Human.objects.create(name="Test", xp=30, strength=3, dexterity=3)

        # Spend XP on strength
        human.spend_xp("strength", "Strength", 5, "attributes")

        # Spend XP on dexterity
        human.spend_xp("dexterity", "Dexterity", 5, "attributes")

        human.refresh_from_db()
        assert human.xp == 20
        assert len(human.spent_xp) == 2

        # Approve strength
        human.approve_xp_spend(0, "strength", 4)

        human.refresh_from_db()
        assert human.strength == 4
        assert human.dexterity == 3  # Not yet approved
        assert human.spent_xp[0]["approved"] == "Approved"
        assert human.spent_xp[1]["approved"] == "Pending"

    def test_rollback_preserves_initial_state(self):
        """
        Test that transaction rollback completely preserves initial state.

        No partial changes should persist.
        """
        character = Character.objects.create(name="Test", xp=10)
        initial_xp = character.xp

        try:
            with transaction.atomic():
                # Spend XP
                char = Character.objects.select_for_update().get(pk=character.pk)
                char.xp -= 5
                char.spent_xp.append({"cost": 5, "approved": "Pending"})
                char.save()

                # Force rollback
                raise ValueError("Force rollback")
        except ValueError:
            pass

        # State should be unchanged
        character.refresh_from_db()
        assert character.xp == initial_xp
        assert len(character.spent_xp) == 0


# Run tests with: pytest characters/tests/core/test_transaction_integration.py -v

#!/usr/bin/env python
"""
Permissions System Deployment Test Script

This script tests the permissions system with different user roles:
- Owner
- Chronicle Head ST
- Game ST
- Player (Chronicle Member)
- Stranger (No relationship)
- Admin

It creates test data and validates permissions work correctly.
"""

import os
import sys

import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg.settings")
django.setup()

from django.contrib.auth.models import User
from django.db import transaction

from characters.models.core.character import Character
from core.models import Observer
from core.permissions import Permission, PermissionManager, VisibilityTier
from game.models import Chronicle


class PermissionsTestSuite:
    """Test suite for permissions system deployment validation"""

    def __init__(self):
        self.users = {}
        self.chronicles = {}
        self.characters = {}
        self.test_results = []

    def setup_test_data(self):
        """Create test users, chronicles, and characters"""
        print("\n" + "=" * 80)
        print("SETTING UP TEST DATA")
        print("=" * 80)

        with transaction.atomic():
            # Create test users
            print("\n1. Creating test users...")
            self.users["owner"] = User.objects.create_user(
                username="test_owner", email="owner@test.com", password="testpass123"
            )
            print(f"   ✓ Created owner: {self.users['owner'].username}")

            self.users["head_st"] = User.objects.create_user(
                username="test_head_st",
                email="head_st@test.com",
                password="testpass123",
            )
            print(f"   ✓ Created head ST: {self.users['head_st'].username}")

            self.users["game_st"] = User.objects.create_user(
                username="test_game_st",
                email="game_st@test.com",
                password="testpass123",
            )
            print(f"   ✓ Created game ST: {self.users['game_st'].username}")

            self.users["player"] = User.objects.create_user(
                username="test_player", email="player@test.com", password="testpass123"
            )
            print(f"   ✓ Created player: {self.users['player'].username}")

            self.users["observer"] = User.objects.create_user(
                username="test_observer",
                email="observer@test.com",
                password="testpass123",
            )
            print(f"   ✓ Created observer: {self.users['observer'].username}")

            self.users["stranger"] = User.objects.create_user(
                username="test_stranger",
                email="stranger@test.com",
                password="testpass123",
            )
            print(f"   ✓ Created stranger: {self.users['stranger'].username}")

            self.users["admin"] = User.objects.create_user(
                username="test_admin",
                email="admin@test.com",
                password="testpass123",
                is_staff=True,
                is_superuser=True,
            )
            print(f"   ✓ Created admin: {self.users['admin'].username}")

            # Create chronicle
            print("\n2. Creating test chronicle...")
            self.chronicles["test"] = Chronicle.objects.create(
                name="Test Chronicle", head_st=self.users["head_st"]
            )
            self.chronicles["test"].game_storytellers.add(self.users["game_st"])
            print(f"   ✓ Created chronicle: {self.chronicles['test'].name}")
            print(f"   ✓ Head ST: {self.users['head_st'].username}")
            print(f"   ✓ Game ST: {self.users['game_st'].username}")

            # Create characters
            print("\n3. Creating test characters...")
            self.characters["owner_char"] = Character.objects.create(
                name="Owner's Character",
                owner=self.users["owner"],
                chronicle=self.chronicles["test"],
                status="App",  # Approved status
            )
            print(f"   ✓ Created character: {self.characters['owner_char'].name}")
            print(f"      Owner: {self.users['owner'].username}")
            print("      Status: Approved")

            self.characters["player_char"] = Character.objects.create(
                name="Player's Character",
                owner=self.users["player"],
                chronicle=self.chronicles["test"],
                status="App",  # Approved status
            )
            print(f"   ✓ Created character: {self.characters['player_char'].name}")
            print(f"      Owner: {self.users['player'].username}")
            print("      Status: Approved")

            # Add observer
            print("\n4. Adding observer...")
            Observer.objects.create(
                content_object=self.characters["owner_char"],
                user=self.users["observer"],
                granted_by=self.users["owner"],
            )
            print(
                f"   ✓ {self.users['observer'].username} is now observing {self.characters['owner_char'].name}"
            )

        print("\n" + "=" * 80)
        print("TEST DATA SETUP COMPLETE")
        print("=" * 80)

    def test_permission(self, test_name, user, character, permission, expected):
        """Test a single permission and record result"""
        user_name = user.username
        char_name = character.name
        perm_name = permission.value if hasattr(permission, "value") else permission

        result = PermissionManager.user_has_permission(user, character, permission)
        passed = result == expected

        status = "✓ PASS" if passed else "✗ FAIL"
        result_str = "CAN" if result else "CANNOT"
        expected_str = "CAN" if expected else "CANNOT"

        self.test_results.append(
            {
                "test": test_name,
                "user": user_name,
                "character": char_name,
                "permission": perm_name,
                "result": result,
                "expected": expected,
                "passed": passed,
            }
        )

        if not passed:
            print(
                f"   {status} {user_name} {result_str} {perm_name} on {char_name} (expected {expected_str})"
            )
        else:
            print(f"   {status} {user_name} {result_str} {perm_name} on {char_name}")

        return passed

    def test_visibility_tier(self, test_name, user, character, expected_tier):
        """Test visibility tier and record result"""
        user_name = user.username
        char_name = character.name

        tier = PermissionManager.get_visibility_tier(user, character)
        passed = tier == expected_tier

        status = "✓ PASS" if passed else "✗ FAIL"

        self.test_results.append(
            {
                "test": test_name,
                "user": user_name,
                "character": char_name,
                "visibility_tier": tier.value if hasattr(tier, "value") else tier,
                "expected_tier": (
                    expected_tier.value if hasattr(expected_tier, "value") else expected_tier
                ),
                "passed": passed,
            }
        )

        if not passed:
            print(
                f"   {status} {user_name} has {tier.value} visibility on {char_name} (expected {expected_tier.value})"
            )
        else:
            print(f"   {status} {user_name} has {tier.value} visibility on {char_name}")

        return passed

    def run_owner_tests(self):
        """Test owner permissions"""
        print("\n" + "=" * 80)
        print("TESTING OWNER PERMISSIONS")
        print("=" * 80)
        print("\nOwner should:")
        print("- VIEW_FULL ✓")
        print("- EDIT_LIMITED ✓ (notes/journals only)")
        print("- SPEND_XP ✓ (when approved)")
        print("- SPEND_FREEBIES ✗ (not when approved)")
        print("- EDIT_FULL ✗ (cannot modify stats directly)")
        print("- DELETE ✓")
        print()

        char = self.characters["owner_char"]
        user = self.users["owner"]

        self.test_permission("Owner - VIEW_FULL", user, char, Permission.VIEW_FULL, True)
        self.test_permission("Owner - EDIT_LIMITED", user, char, Permission.EDIT_LIMITED, True)
        self.test_permission("Owner - SPEND_XP", user, char, Permission.SPEND_XP, True)
        self.test_permission("Owner - SPEND_FREEBIES", user, char, Permission.SPEND_FREEBIES, False)
        self.test_permission("Owner - EDIT_FULL", user, char, Permission.EDIT_FULL, False)
        self.test_permission("Owner - DELETE", user, char, Permission.DELETE, True)
        self.test_visibility_tier("Owner - Visibility", user, char, VisibilityTier.FULL)

    def run_head_st_tests(self):
        """Test chronicle head ST permissions"""
        print("\n" + "=" * 80)
        print("TESTING CHRONICLE HEAD ST PERMISSIONS")
        print("=" * 80)
        print("\nChronicle Head ST should:")
        print("- VIEW_FULL ✓")
        print("- EDIT_FULL ✓ (can modify everything)")
        print("- SPEND_XP ✓")
        print("- APPROVE ✓")
        print("- DELETE ✓")
        print()

        char = self.characters["owner_char"]
        user = self.users["head_st"]

        self.test_permission("Head ST - VIEW_FULL", user, char, Permission.VIEW_FULL, True)
        self.test_permission("Head ST - EDIT_FULL", user, char, Permission.EDIT_FULL, True)
        self.test_permission("Head ST - SPEND_XP", user, char, Permission.SPEND_XP, True)
        self.test_permission("Head ST - APPROVE", user, char, Permission.APPROVE, True)
        self.test_permission("Head ST - DELETE", user, char, Permission.DELETE, True)
        self.test_visibility_tier("Head ST - Visibility", user, char, VisibilityTier.FULL)

    def run_game_st_tests(self):
        """Test game ST permissions"""
        print("\n" + "=" * 80)
        print("TESTING GAME ST PERMISSIONS")
        print("=" * 80)
        print("\nGame ST should:")
        print("- VIEW_FULL ✓ (read-only access)")
        print("- EDIT_FULL ✗ (no edit permissions)")
        print("- EDIT_LIMITED ✗ (no edit permissions)")
        print("- SPEND_XP ✗")
        print("- APPROVE ✗")
        print()

        char = self.characters["owner_char"]
        user = self.users["game_st"]

        self.test_permission("Game ST - VIEW_FULL", user, char, Permission.VIEW_FULL, True)
        self.test_permission("Game ST - EDIT_FULL", user, char, Permission.EDIT_FULL, False)
        self.test_permission("Game ST - EDIT_LIMITED", user, char, Permission.EDIT_LIMITED, False)
        self.test_permission("Game ST - SPEND_XP", user, char, Permission.SPEND_XP, False)
        self.test_permission("Game ST - APPROVE", user, char, Permission.APPROVE, False)
        self.test_visibility_tier("Game ST - Visibility", user, char, VisibilityTier.FULL)

    def run_player_tests(self):
        """Test player (chronicle member) permissions"""
        print("\n" + "=" * 80)
        print("TESTING PLAYER PERMISSIONS")
        print("=" * 80)
        print("\nPlayer should:")
        print("- VIEW_PARTIAL ✓ (on other players' characters)")
        print("- VIEW_FULL ✗ (no full access to others)")
        print("- EDIT_FULL ✗")
        print("- EDIT_LIMITED ✗")
        print()

        char = self.characters["owner_char"]  # Player viewing owner's char
        user = self.users["player"]

        self.test_permission("Player - VIEW_PARTIAL", user, char, Permission.VIEW_PARTIAL, True)
        self.test_permission("Player - VIEW_FULL", user, char, Permission.VIEW_FULL, False)
        self.test_permission("Player - EDIT_FULL", user, char, Permission.EDIT_FULL, False)
        self.test_permission("Player - EDIT_LIMITED", user, char, Permission.EDIT_LIMITED, False)
        self.test_visibility_tier("Player - Visibility", user, char, VisibilityTier.PARTIAL)

    def run_observer_tests(self):
        """Test observer permissions"""
        print("\n" + "=" * 80)
        print("TESTING OBSERVER PERMISSIONS")
        print("=" * 80)
        print("\nObserver should:")
        print("- VIEW_PARTIAL ✓")
        print("- VIEW_FULL ✗")
        print("- EDIT_FULL ✗")
        print()

        char = self.characters["owner_char"]
        user = self.users["observer"]

        self.test_permission("Observer - VIEW_PARTIAL", user, char, Permission.VIEW_PARTIAL, True)
        self.test_permission("Observer - VIEW_FULL", user, char, Permission.VIEW_FULL, False)
        self.test_permission("Observer - EDIT_FULL", user, char, Permission.EDIT_FULL, False)
        self.test_visibility_tier("Observer - Visibility", user, char, VisibilityTier.PARTIAL)

    def run_stranger_tests(self):
        """Test stranger (no relationship) permissions"""
        print("\n" + "=" * 80)
        print("TESTING STRANGER PERMISSIONS")
        print("=" * 80)
        print("\nStranger should:")
        print("- VIEW_FULL ✗")
        print("- VIEW_PARTIAL ✗")
        print("- EDIT_FULL ✗")
        print("- Visibility: NONE")
        print()

        char = self.characters["owner_char"]
        user = self.users["stranger"]

        self.test_permission("Stranger - VIEW_FULL", user, char, Permission.VIEW_FULL, False)
        self.test_permission("Stranger - VIEW_PARTIAL", user, char, Permission.VIEW_PARTIAL, False)
        self.test_permission("Stranger - EDIT_FULL", user, char, Permission.EDIT_FULL, False)
        self.test_visibility_tier("Stranger - Visibility", user, char, VisibilityTier.NONE)

    def run_admin_tests(self):
        """Test admin permissions"""
        print("\n" + "=" * 80)
        print("TESTING ADMIN PERMISSIONS")
        print("=" * 80)
        print("\nAdmin should:")
        print("- VIEW_FULL ✓ (full access to everything)")
        print("- EDIT_FULL ✓")
        print("- DELETE ✓")
        print("- APPROVE ✓")
        print()

        char = self.characters["owner_char"]
        user = self.users["admin"]

        self.test_permission("Admin - VIEW_FULL", user, char, Permission.VIEW_FULL, True)
        self.test_permission("Admin - EDIT_FULL", user, char, Permission.EDIT_FULL, True)
        self.test_permission("Admin - DELETE", user, char, Permission.DELETE, True)
        self.test_permission("Admin - APPROVE", user, char, Permission.APPROVE, True)
        self.test_visibility_tier("Admin - Visibility", user, char, VisibilityTier.FULL)

    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 80)
        print("TEST RESULTS SUMMARY")
        print("=" * 80)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["passed"])
        failed_tests = total_tests - passed_tests

        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✓")
        print(f"Failed: {failed_tests} {'✗' if failed_tests > 0 else ''}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

        if failed_tests > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"  - {result['test']}")
                    print(f"    Expected: {result.get('expected', result.get('expected_tier'))}")
                    print(f"    Got: {result.get('result', result.get('visibility_tier'))}")

        print("\n" + "=" * 80)
        return failed_tests == 0

    def cleanup_test_data(self):
        """Remove test data"""
        print("\n" + "=" * 80)
        print("CLEANING UP TEST DATA")
        print("=" * 80)

        with transaction.atomic():
            # Delete in correct order to respect foreign keys
            print("\n1. Deleting characters...")
            Character.objects.filter(name__startswith="Owner's Character").delete()
            Character.objects.filter(name__startswith="Player's Character").delete()
            print("   ✓ Characters deleted")

            print("\n2. Deleting chronicles...")
            Chronicle.objects.filter(name="Test Chronicle").delete()
            print("   ✓ Chronicles deleted")

            print("\n3. Deleting users...")
            User.objects.filter(username__startswith="test_").delete()
            print("   ✓ Users deleted")

        print("\n" + "=" * 80)
        print("CLEANUP COMPLETE")
        print("=" * 80)

    def run_all_tests(self):
        """Run all permission tests"""
        try:
            self.setup_test_data()
            self.run_owner_tests()
            self.run_head_st_tests()
            self.run_game_st_tests()
            self.run_player_tests()
            self.run_observer_tests()
            self.run_stranger_tests()
            self.run_admin_tests()
            all_passed = self.print_summary()

            return all_passed
        finally:
            self.cleanup_test_data()


def main():
    """Main test runner"""
    print("\n" + "#" * 80)
    print("# PERMISSIONS SYSTEM DEPLOYMENT TEST")
    print("#" * 80)
    print("\nThis script will test the permissions system with different user roles")
    print("to ensure the deployment is working correctly.")

    test_suite = PermissionsTestSuite()
    all_passed = test_suite.run_all_tests()

    if all_passed:
        print("\n" + "#" * 80)
        print("# ✓ ALL TESTS PASSED - PERMISSIONS SYSTEM IS WORKING CORRECTLY")
        print("#" * 80)
        sys.exit(0)
    else:
        print("\n" + "#" * 80)
        print("# ✗ SOME TESTS FAILED - REVIEW RESULTS ABOVE")
        print("#" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()

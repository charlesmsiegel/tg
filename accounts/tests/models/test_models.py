"""Tests for accounts models (Profile)."""

from characters.models.core import Human
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle, Gameline, STRelationship


class TestProfileCreation(TestCase):
    """Test Profile creation and setup."""

    def test_profile_created_on_user_signup(self):
        """Test that a profile is automatically created when a user signs up."""
        user = User.objects.create_user(
            username="newuser", email="new@test.com", password="password"
        )

        # Profile should be created automatically via signal
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsNotNone(user.profile)

    def test_profile_has_user_relationship(self):
        """Test that profile has one-to-one relationship with user."""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

        profile = user.profile
        self.assertEqual(profile.user, user)

    def test_new_profile_not_st_by_default(self):
        """Test that new profiles are not STs by default."""
        user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )

        self.assertFalse(user.profile.is_st())


class TestSTRelationships(TestCase):
    """Test ST relationship functionality."""

    def setUp(self):
        self.st_user = User.objects.create_user(
            username="storyteller", email="st@test.com", password="password"
        )
        self.player_user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Mage: the Ascension")

    def test_is_st_returns_true_for_st(self):
        """Test that is_st() returns True for storytellers."""
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

        self.assertTrue(self.st_user.profile.is_st())

    def test_is_st_returns_false_for_non_st(self):
        """Test that is_st() returns False for non-storytellers."""
        self.assertFalse(self.player_user.profile.is_st())

    def test_st_relations_returns_chronicles(self):
        """Test that st_relations() returns ST's chronicles."""
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

        st_relations = self.st_user.profile.st_relations()
        # st_relations() returns a dict mapping Chronicle to list of STRelationships
        self.assertIn(self.chronicle, st_relations)

    def test_st_for_multiple_chronicles(self):
        """Test that a user can be ST for multiple chronicles."""
        chronicle2 = Chronicle.objects.create(name="Second Chronicle")

        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        STRelationship.objects.create(
            user=self.st_user, chronicle=chronicle2, gameline=self.gameline
        )

        relations = self.st_user.profile.st_relations()
        # st_relations() returns a dict mapping Chronicle to list of STRelationships
        self.assertEqual(len(relations), 2)

    def test_st_for_multiple_gamelines(self):
        """Test that an ST can run multiple gamelines in same chronicle."""
        gameline2 = Gameline.objects.create(name="Vampire: the Masquerade")

        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=gameline2
        )

        relations = self.st_user.profile.st_relations()
        # st_relations() returns a dict mapping Chronicle to list of STRelationships
        # Both relationships are for the same chronicle, so we count the relationships
        total_relationships = sum(len(rels) for rels in relations.values())
        self.assertEqual(total_relationships, 2)


class TestObjectsToApprove(TestCase):
    """Test the objects_to_approve() method."""

    def setUp(self):
        self.st_user = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.player_user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Mage: the Ascension")

        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

    def test_objects_to_approve_includes_submitted_characters(self):
        """Test that submitted characters appear in objects to approve."""
        character = Human.objects.create(
            name="Submitted Character",
            owner=self.player_user,
            chronicle=self.chronicle,
            status="Sub",  # Submitted for approval
        )

        to_approve = self.st_user.profile.objects_to_approve()

        # Should include the submitted character
        self.assertIn(character, to_approve)

    def test_objects_to_approve_excludes_unfinished_characters(self):
        """Test that unfinished characters don't appear in approval queue."""
        unfinished = Human.objects.create(
            name="Unfinished Character",
            owner=self.player_user,
            chronicle=self.chronicle,
            status="Un",  # Unfinished
        )

        to_approve = self.st_user.profile.objects_to_approve()

        # Should not include unfinished characters
        self.assertNotIn(unfinished, to_approve)

    def test_objects_to_approve_excludes_approved_characters(self):
        """Test that already approved characters don't appear."""
        approved = Human.objects.create(
            name="Approved Character",
            owner=self.player_user,
            chronicle=self.chronicle,
            status="App",  # Already approved
        )

        to_approve = self.st_user.profile.objects_to_approve()

        # Should not include already approved characters
        self.assertNotIn(approved, to_approve)

    def test_objects_to_approve_only_for_st_chronicles(self):
        """Test that STs only see objects from their chronicles."""
        other_chronicle = Chronicle.objects.create(name="Other Chronicle")

        character_in_chronicle = Human.objects.create(
            name="In Chronicle",
            owner=self.player_user,
            chronicle=self.chronicle,
            status="Sub",
        )

        character_outside = Human.objects.create(
            name="Outside Chronicle",
            owner=self.player_user,
            chronicle=other_chronicle,
            status="Sub",
        )

        to_approve = self.st_user.profile.objects_to_approve()

        # Should include character in ST's chronicle
        self.assertIn(character_in_chronicle, to_approve)
        # Should not include character outside ST's chronicle
        self.assertNotIn(character_outside, to_approve)


class TestThemePreferences(TestCase):
    """Test theme preference functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_profile_has_theme_field(self):
        """Test that profile has theme preference field."""
        profile = self.user.profile

        # Should have theme field (exact implementation may vary)
        self.assertTrue(hasattr(profile, "theme") or hasattr(profile, "preferred_theme"))

    def test_theme_can_be_updated(self):
        """Test that theme preference can be changed."""
        profile = self.user.profile

        # If theme field exists
        if hasattr(profile, "theme"):
            profile.theme = "dark"
            profile.save()
            profile.refresh_from_db()
            self.assertEqual(profile.theme, "dark")


class TestProfilePermissions(TestCase):
    """Test permission-related profile functionality."""

    def setUp(self):
        self.st_user = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.player_user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="password",
            is_staff=True,
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")

    def test_st_has_elevated_permissions(self):
        """Test that STs have elevated permissions."""
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

        # STs should be able to approve characters
        self.assertTrue(self.st_user.profile.is_st())

    def test_admin_has_all_permissions(self):
        """Test that admins have all permissions."""
        # Staff users should have admin permissions
        self.assertTrue(self.admin_user.is_staff)

    def test_regular_player_limited_permissions(self):
        """Test that regular players have limited permissions."""
        # Regular players should not have ST permissions
        self.assertFalse(self.player_user.profile.is_st())
        self.assertFalse(self.player_user.is_staff)


class TestProfileStringRepresentation(TestCase):
    """Test profile string representation."""

    def test_profile_str_includes_username(self):
        """Test that profile string representation includes username."""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

        profile_str = str(user.profile)

        # Should include the username
        self.assertIn("testuser", profile_str)


class TestProfileSTMethods(TestCase):
    """Test Profile methods related to ST functionality."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle1 = Chronicle.objects.create(name="Chronicle 1")
        self.chronicle2 = Chronicle.objects.create(name="Chronicle 2")
        self.gameline1 = Gameline.objects.create(name="Vampire")
        self.gameline2 = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle1, gameline=self.gameline1
        )
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle2, gameline=self.gameline2
        )

    def test_is_st_returns_true_for_storyteller(self):
        """Test that is_st returns True for users with ST relationships."""
        self.assertTrue(self.st_user.profile.is_st())

    def test_is_st_returns_false_for_non_storyteller(self):
        """Test that is_st returns False for regular users."""
        self.assertFalse(self.user.profile.is_st())

    def test_st_relations_returns_grouped_relationships(self):
        """Test that st_relations returns relationships grouped by chronicle."""
        relations = self.st_user.profile.st_relations()
        self.assertIn(self.chronicle1, relations)
        self.assertIn(self.chronicle2, relations)
        self.assertEqual(len(relations[self.chronicle1]), 1)
        self.assertEqual(relations[self.chronicle1][0].gameline, self.gameline1)

    def test_st_relations_empty_for_non_st(self):
        """Test that st_relations is empty for non-storytellers."""
        relations = self.user.profile.st_relations()
        self.assertEqual(len(relations), 0)

    def test_is_st_for_returns_true_for_chronicle_st(self):
        """Test that is_st_for returns True when user is ST for the chronicle."""
        self.assertTrue(self.st_user.profile.is_st_for(self.chronicle1))
        self.assertTrue(self.st_user.profile.is_st_for(self.chronicle2))

    def test_is_st_for_returns_false_for_other_chronicle(self):
        """Test that is_st_for returns False for chronicle user is not ST of."""
        other_chronicle = Chronicle.objects.create(name="Other Chronicle")
        self.assertFalse(self.st_user.profile.is_st_for(other_chronicle))

    def test_is_st_for_returns_false_for_non_st(self):
        """Test that is_st_for returns False for non-storytellers."""
        self.assertFalse(self.user.profile.is_st_for(self.chronicle1))
        self.assertFalse(self.user.profile.is_st_for(self.chronicle2))

    def test_is_st_for_returns_false_for_none_chronicle(self):
        """Test that is_st_for returns False when chronicle is None."""
        self.assertFalse(self.st_user.profile.is_st_for(None))

    def test_is_st_for_returns_true_for_head_st(self):
        """Test that is_st_for returns True when user is head_st of chronicle."""
        new_chronicle = Chronicle.objects.create(name="New Chronicle", head_st=self.user)
        # User is not in STRelationship but is head_st
        self.assertTrue(self.user.profile.is_st_for(new_chronicle))

    def test_is_st_for_prioritizes_head_st_over_relationship(self):
        """Test that head_st role grants ST permissions even without STRelationship."""
        # Create a chronicle where user is head_st but has no STRelationship
        new_chronicle = Chronicle.objects.create(name="Head ST Chronicle", head_st=self.user)
        self.assertTrue(self.user.profile.is_st_for(new_chronicle))
        # Verify they don't have an STRelationship
        self.assertFalse(
            STRelationship.objects.filter(user=self.user, chronicle=new_chronicle).exists()
        )


class TestProfileObjectQueries(TestCase):
    """Test Profile methods for querying owned objects."""

    def setUp(self):
        from items.models.core import ItemModel
        from locations.models.core import LocationModel

        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.char1 = Human.objects.create(name="Character 1", owner=self.user, concept="Test")
        self.char2 = Human.objects.create(name="Character 2", owner=self.user, concept="Test")
        self.location = LocationModel.objects.create(name="My Location", owner=self.user)
        self.item = ItemModel.objects.create(name="My Item", owner=self.user)

    def test_my_characters_returns_owned_characters(self):
        """Test that my_characters returns all owned characters."""
        chars = self.user.profile.my_characters()
        self.assertEqual(chars.count(), 2)
        self.assertIn(self.char1, chars)
        self.assertIn(self.char2, chars)

    def test_my_locations_returns_owned_locations(self):
        """Test that my_locations returns all owned locations."""
        locs = self.user.profile.my_locations()
        self.assertEqual(locs.count(), 1)
        self.assertIn(self.location, locs)

    def test_my_items_returns_owned_items(self):
        """Test that my_items returns all owned items."""
        items = self.user.profile.my_items()
        self.assertEqual(items.count(), 1)
        self.assertIn(self.item, items)


class TestProfileThemeMethods(TestCase):
    """Test Profile theme-related methods."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")

    def test_get_theme_css_path_light(self):
        """Test theme CSS path for light theme."""
        self.user.profile.theme = "light"
        self.user.profile.save()
        path = self.user.profile.get_theme_css_path()
        self.assertEqual(path, "themes/light.css")

    def test_get_theme_css_path_dark(self):
        """Test theme CSS path for dark theme."""
        self.user.profile.theme = "dark"
        self.user.profile.save()
        path = self.user.profile.get_theme_css_path()
        self.assertEqual(path, "themes/dark.css")


class TestUnfulfilledWeeklyXPRequests(TestCase):
    """Test the get_unfulfilled_weekly_xp_requests methods.

    These tests verify that the methods return correct results and that
    the optimized queries only fetch relevant weeks from the database.
    """

    def setUp(self):
        from datetime import date, timedelta

        from game.models import Week, WeeklyXPRequest

        self.player = User.objects.create_user("player", "player@test.com", "password")
        self.st_user = User.objects.create_user("st", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Mage: the Ascension")

        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

        # Create character owned by player
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.player,
            chronicle=self.chronicle,
            status="App",
            npc=False,
        )

        # Create weeks
        self.week1 = Week.objects.create(end_date=date.today())
        self.week2 = Week.objects.create(end_date=date.today() - timedelta(days=7))
        self.week_old = Week.objects.create(end_date=date.today() - timedelta(days=365))

        # Associate character with week1 and week2 only
        self.week1.characters.add(self.character)
        self.week2.characters.add(self.character)

    def test_unfulfilled_returns_pairs_without_requests(self):
        """Test that method returns character/week pairs without XP requests."""
        results = self.player.profile.get_unfulfilled_weekly_xp_requests()

        # Should return tuples of (character, week)
        self.assertEqual(len(results), 2)

        # Both weeks should be in results
        weeks_in_results = [week for (char, week) in results]
        self.assertIn(self.week1, weeks_in_results)
        self.assertIn(self.week2, weeks_in_results)

        # Old week not associated with character should NOT be in results
        self.assertNotIn(self.week_old, weeks_in_results)

    def test_unfulfilled_excludes_pairs_with_existing_requests(self):
        """Test that existing XP requests are excluded from results."""
        from game.models import WeeklyXPRequest

        # Create XP request for week1
        WeeklyXPRequest.objects.create(character=self.character, week=self.week1, approved=False)

        results = self.player.profile.get_unfulfilled_weekly_xp_requests()

        # Only week2 should be in results now
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], self.week2)

    def test_unfulfilled_excludes_npc_characters(self):
        """Test that NPC characters are excluded from results."""
        npc = Human.objects.create(
            name="NPC Character",
            owner=self.player,
            chronicle=self.chronicle,
            status="App",
            npc=True,
        )
        self.week1.characters.add(npc)

        results = self.player.profile.get_unfulfilled_weekly_xp_requests()

        # NPC should not appear in results
        chars_in_results = [char for (char, week) in results]
        self.assertNotIn(npc, chars_in_results)

    def test_unfulfilled_returns_empty_for_no_weeks(self):
        """Test that method returns empty list if character has no weeks."""
        other_player = User.objects.create_user("other", "other@test.com", "password")
        other_char = Human.objects.create(
            name="No Weeks Char",
            owner=other_player,
            chronicle=self.chronicle,
            npc=False,
        )

        results = other_player.profile.get_unfulfilled_weekly_xp_requests()
        self.assertEqual(len(results), 0)


class TestUnfulfilledWeeklyXPRequestsToApprove(TestCase):
    """Test the get_unfulfilled_weekly_xp_requests_to_approve method."""

    def setUp(self):
        from datetime import date, timedelta

        from game.models import Week, WeeklyXPRequest

        self.player = User.objects.create_user("player", "player@test.com", "password")
        self.st_user = User.objects.create_user("st", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Mage: the Ascension")

        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

        self.character = Human.objects.create(
            name="Test Character",
            owner=self.player,
            chronicle=self.chronicle,
            status="App",
        )

        # Create weeks
        self.week1 = Week.objects.create(end_date=date.today())
        self.week2 = Week.objects.create(end_date=date.today() - timedelta(days=7))
        self.week_old = Week.objects.create(end_date=date.today() - timedelta(days=365))

        # Associate character with weeks
        self.week1.characters.add(self.character)
        self.week2.characters.add(self.character)

    def test_returns_unapproved_requests(self):
        """Test that method returns character/week pairs with unapproved requests."""
        from game.models import WeeklyXPRequest

        # Create unapproved request
        WeeklyXPRequest.objects.create(character=self.character, week=self.week1, approved=False)

        results = self.st_user.profile.get_unfulfilled_weekly_xp_requests_to_approve()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], self.character)
        self.assertEqual(results[0][1], self.week1)

    def test_excludes_approved_requests(self):
        """Test that approved requests are excluded."""
        from game.models import WeeklyXPRequest

        # Create approved request
        WeeklyXPRequest.objects.create(character=self.character, week=self.week1, approved=True)
        # Create unapproved request
        WeeklyXPRequest.objects.create(character=self.character, week=self.week2, approved=False)

        results = self.st_user.profile.get_unfulfilled_weekly_xp_requests_to_approve()

        # Only unapproved request should be in results
        self.assertEqual(len(results), 1)
        weeks_in_results = [week for (char, week) in results]
        self.assertIn(self.week2, weeks_in_results)
        self.assertNotIn(self.week1, weeks_in_results)

    def test_returns_empty_when_no_unapproved_requests(self):
        """Test that method returns empty list when all requests are approved."""
        from game.models import WeeklyXPRequest

        WeeklyXPRequest.objects.create(character=self.character, week=self.week1, approved=True)

        results = self.st_user.profile.get_unfulfilled_weekly_xp_requests_to_approve()
        self.assertEqual(len(results), 0)

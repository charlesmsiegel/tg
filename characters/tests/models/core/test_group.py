from characters.models.core import Group
from characters.models.core.human import Human
from characters.models.core.specialty import Specialty
from characters.tests.utils import human_setup
from django.contrib.auth.models import User
from django.test import TestCase


class TestGroupDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.group = Group.objects.create(name="Test Group")
        self.url = self.group.get_absolute_url()

    def test_group_detail_view_status_code(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_group_detail_view_templates(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/group/detail.html")


class TestGroupCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Group",
            "description": "test",
        }
        self.url = Group.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/group/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.first().name, "Test Group")


class TestGroupUpdateView(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.group = Group.objects.create(name="Test Group")
        self.valid_data = {"name": "Test Group Updated", "description": "Test"}
        self.url = self.group.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/group/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.group.refresh_from_db()
        self.assertEqual(self.group.name, "Test Group Updated")


class TestGenericGroupDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="Test", password="12345")
        self.group = Group.objects.create(name="Group Test")

    def test_generic_group_detail_view_templates(self):
        self.client.login(username="Test", password="12345")
        response = self.client.get(self.group.get_absolute_url())
        self.assertTemplateUsed(response, "characters/core/group/detail.html")


class TestCharacterRetirementRemoval(TestCase):
    """Test that retiring or marking a character as deceased removes them from groups."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.player,
            status="App",  # Approved status
        )
        self.group = Group.objects.create(name="Test Group")
        # Add character to group
        self.group.members.add(self.character)
        # Set character as leader
        self.group.leader = self.character
        self.group.save()

    def test_character_removed_from_group_on_retirement(self):
        """Test that retiring a character removes them from group membership."""
        self.assertIn(self.character, self.group.members.all())
        self.assertEqual(self.group.leader, self.character)

        # Retire the character
        self.character.status = "Ret"
        self.character.save()

        # Refresh from database
        self.group.refresh_from_db()

        # Character should be removed from group
        self.assertNotIn(self.character, self.group.members.all())
        self.assertIsNone(self.group.leader)

    def test_character_removed_from_group_on_death(self):
        """Test that marking a character as deceased removes them from group membership."""
        self.assertIn(self.character, self.group.members.all())
        self.assertEqual(self.group.leader, self.character)

        # Mark character as deceased
        self.character.status = "Dec"
        self.character.save()

        # Refresh from database
        self.group.refresh_from_db()

        # Character should be removed from group
        self.assertNotIn(self.character, self.group.members.all())
        self.assertIsNone(self.group.leader)

    def test_character_removed_from_multiple_groups(self):
        """Test that retiring a character removes them from all groups."""
        group2 = Group.objects.create(name="Second Group")
        group2.members.add(self.character)
        group2.leader = self.character
        group2.save()

        # Retire the character
        self.character.status = "Ret"
        self.character.save()

        # Refresh from database
        self.group.refresh_from_db()
        group2.refresh_from_db()

        # Character should be removed from both groups
        self.assertNotIn(self.character, self.group.members.all())
        self.assertIsNone(self.group.leader)
        self.assertNotIn(self.character, group2.members.all())
        self.assertIsNone(group2.leader)

    def test_no_removal_for_other_status_changes(self):
        """Test that other status changes don't remove characters from groups."""
        # Create a fresh character in 'Un' status for this test
        new_char = Human.objects.create(
            name="Status Test Character",
            owner=self.player,
            status="Un",
        )

        # Add to group
        self.group.members.add(new_char)
        self.group.leader = new_char
        self.group.save()

        # Change to submitted (valid: Un -> Sub)
        new_char.status = "Sub"
        new_char.save()

        # Character should still be in group
        self.group.refresh_from_db()
        new_char.refresh_from_db()
        self.assertIn(new_char, self.group.members.all())
        self.assertEqual(self.group.leader.pk, new_char.pk)

        # Change to approved (valid: Sub -> App)
        new_char.status = "App"
        new_char.save()

        # Character should still be in group
        self.group.refresh_from_db()
        new_char.refresh_from_db()
        self.assertIn(new_char, self.group.members.all())
        self.assertEqual(self.group.leader.pk, new_char.pk)

    def test_already_retired_character_stays_removed(self):
        """Test that re-saving an already retired character doesn't cause errors."""
        # Retire the character
        self.character.status = "Ret"
        self.character.save()

        # Character should be removed
        self.group.refresh_from_db()
        self.assertNotIn(self.character, self.group.members.all())

        # Save again (should not cause errors)
        self.character.notes = "Updated notes"
        self.character.save()

        # Should still not be in group
        self.assertNotIn(self.character, self.group.members.all())

"""Group controls reflect creator authority, not a leader ownership shortcut."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from characters.models.core import Group, Human


class GroupPermissionContextTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.creator = get_user_model().objects.create_user("group-creator")
        cls.leader_owner = get_user_model().objects.create_user("leader-owner")
        cls.leader = Human.objects.create(name="Leader", owner=cls.leader_owner)

    def create_group(self):
        self.client.force_login(self.creator)
        response = self.client.post(
            reverse("characters:create:group"),
            {
                "name": "Created group",
                "description": "Description",
                "leader": self.leader.pk,
                "members": [self.leader.pk],
            },
        )
        self.assertEqual(response.status_code, 302)
        return Group.objects.get(name="Created group")

    def test_message_mixin_assigns_creator_and_allows_draft_edits(self):
        group = self.create_group()
        self.assertEqual(group.owner_id, self.creator.pk)
        self.assertEqual(group.status, "Un")
        self.assertEqual(self.client.get(group.get_update_url()).status_code, 200)
        response = self.client.get(group.get_absolute_url())
        self.assertTrue(response.context["object_perms"].can_edit)

    def test_leadership_does_not_bypass_the_existing_write_gate(self):
        group = self.create_group()
        self.client.force_login(self.leader_owner)
        self.assertEqual(self.client.get(group.get_update_url()).status_code, 403)
        response = self.client.post(group.get_update_url(), {"name": "Unauthorized"})
        self.assertEqual(response.status_code, 403)
        group.refresh_from_db()
        self.assertEqual(group.name, "Created group")

    def test_approved_creator_remains_read_only(self):
        group = self.create_group()
        group.status = "App"
        group.save(update_fields=["status"])
        self.assertEqual(self.client.get(group.get_update_url()).status_code, 403)
        response = self.client.get(group.get_absolute_url())
        self.assertTrue(response.context["object_perms"].can_view_full)
        self.assertFalse(response.context["object_perms"].can_edit)

    def test_edit_action_uses_capability_even_with_different_leader(self):
        group = self.create_group()
        edit_link = f'href="{group.get_update_url()}"'
        for user, allowed in ((self.creator, True), (self.leader_owner, False)):
            self.client.force_login(user)
            response = self.client.get(group.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(edit_link in response.content.decode(), allowed)

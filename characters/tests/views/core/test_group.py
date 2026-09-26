"""Group controls reflect creator authority, not a leader ownership shortcut."""

from pathlib import Path

from django.contrib.auth import get_user_model
from django.template import Context, Engine
from django.test import RequestFactory, TestCase
from django.urls import reverse

from characters.models.core import Group, Human
from core.permission_context import get_object_permissions


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

    def test_legacy_update_block_uses_capability_even_with_different_leader(self):
        group = self.create_group()
        # core/object.html currently has no update block. Exercise this legacy
        # block independently so restoring it cannot restore the unsafe rule.
        source = Path("characters/templates/characters/core/group/detail.html").read_text(
            encoding="utf-8"
        )
        engine = Engine(
            loaders=[
                (
                    "django.template.loaders.locmem.Loader",
                    {
                        "core/object.html": "{% block update %}{% endblock %}",
                        "group.html": source,
                    },
                )
            ]
        )
        for user, allowed in ((self.creator, True), (self.leader_owner, False)):
            request = RequestFactory().get("/")
            request.user = user
            output = engine.get_template("group.html").render(
                Context(
                    {
                        "user": user,
                        "object": group,
                        "object_perms": get_object_permissions(request, group),
                    }
                )
            )
            self.assertEqual(">Update</a>" in output, allowed)

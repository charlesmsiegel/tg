"""Tests for the user section of export_chronicle and its import."""

import json
import os
import tempfile
from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from characters.models.core.human import Human
from game.models import Chronicle


class ExportChronicleUsersTests(TestCase):
    def setUp(self):
        self.st = User.objects.create_user("st", email="st@example.com", password="st-pass")
        self.player = User.objects.create_user("player", password="player-pass")
        self.chronicle = Chronicle.objects.create(name="Exported")
        self.chronicle.storytellers.add(self.st)
        Human.objects.create(name="PC", owner=self.player, chronicle=self.chronicle)
        handle, self.path = tempfile.mkstemp(suffix=".json")
        os.close(handle)
        self.addCleanup(os.remove, self.path)

    def export(self):
        call_command(
            "export_chronicle",
            str(self.chronicle.pk),
            "--include-users",
            "--output",
            self.path,
            stdout=StringIO(),
        )
        with open(self.path) as handle:
            return json.load(handle)

    def test_users_exclude_password_hashes_and_flags(self):
        users = self.export()["users"]
        self.assertEqual({u["fields"]["username"] for u in users}, {"st", "player"})
        for user in users:
            self.assertEqual(set(user["fields"]), {"username", "email", "first_name", "last_name"})
        self.assertNotIn(self.st.password, json.dumps(users))

    def test_imported_users_have_unusable_passwords(self):
        data = self.export()
        User.objects.filter(username__in=["st", "player"]).delete()
        call_command("import_chronicle", self.path, stdout=StringIO())
        imported = User.objects.get(username="st")
        self.assertEqual(imported.email, "st@example.com")
        self.assertFalse(imported.has_usable_password())
        self.assertEqual(len(data["users"]), 2)

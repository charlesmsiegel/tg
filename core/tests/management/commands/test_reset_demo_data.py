"""Tests for the reset_demo_data management command."""

from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from game.models import Chronicle


class ResetDemoDataTests(TestCase):
    def run_command(self, *args):
        out = StringIO()
        call_command("reset_demo_data", *args, stdout=out)
        return out.getvalue()

    @override_settings(DEBUG=False)
    def test_refuses_without_debug(self):
        chronicle = Chronicle.objects.create(name="Real Chronicle")
        with self.assertRaises(CommandError):
            self.run_command("--confirm")
        self.assertTrue(Chronicle.objects.filter(pk=chronicle.pk).exists())

    @override_settings(DEBUG=False)
    def test_force_runs_without_debug(self):
        self.run_command("--confirm", "--force", "--password", "s3cret-pass")
        self.assertTrue(User.objects.filter(username="demo_st").exists())

    @override_settings(DEBUG=True)
    def test_demo_accounts_get_given_password(self):
        output = self.run_command("--confirm", "--password", "s3cret-pass")
        for username in ("demo_st", "demo_player"):
            user = User.objects.get(username=username)
            self.assertTrue(user.check_password("s3cret-pass"))
        self.assertTrue(Chronicle.objects.filter(storytellers__username="demo_st").exists())
        self.assertIn("s3cret-pass", output)

    @override_settings(DEBUG=True)
    def test_default_password_is_random_not_demo123(self):
        output = self.run_command("--confirm")
        user = User.objects.get(username="demo_st")
        self.assertFalse(user.check_password("demo123"))
        self.assertNotIn("demo123", output)
        password = output.split("Password for demo_st, demo_player: ")[1].split()[0]
        self.assertTrue(user.check_password(password))

    @override_settings(DEBUG=True)
    def test_existing_demo_account_keeps_password(self):
        User.objects.create_user("demo_st", password="kept-pass", is_superuser=True)
        self.run_command("--confirm", "--password", "new-pass")
        self.assertTrue(User.objects.get(username="demo_st").check_password("kept-pass"))

    @override_settings(DEBUG=True)
    def test_without_confirm_changes_nothing(self):
        chronicle = Chronicle.objects.create(name="Kept")
        self.run_command()
        self.assertTrue(Chronicle.objects.filter(pk=chronicle.pk).exists())

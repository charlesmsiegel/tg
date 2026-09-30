"""Tests for the options of sync_character_status."""

from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class SyncCharacterStatusOptionTests(TestCase):
    def test_fix_all_option_is_gone(self):
        # It iterated every character but could only ever change retired and deceased ones.
        with self.assertRaises(CommandError):
            call_command("sync_character_status", "--fix-all", stdout=StringIO())

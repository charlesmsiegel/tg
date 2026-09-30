"""Status checks of validate_data_integrity and monitor_validation."""

import json
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from characters.models.core.human import Human


class ReturnedForRevisionStatusTests(TestCase):
    """``Rev`` is a valid CharacterStatus and must survive both checks."""

    def setUp(self):
        self.character = Human.objects.create(name="Returned", status="Rev")

    def test_validate_data_integrity_fix_keeps_rev(self):
        out = StringIO()
        call_command("validate_data_integrity", "--fix", stdout=out)
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "Rev")
        self.assertIn("All characters have valid status", out.getvalue())

    def test_monitor_validation_counts_no_invalid_status(self):
        out = StringIO()
        call_command("monitor_validation", "--json", stdout=out)
        metrics = json.loads(out.getvalue())
        self.assertEqual(metrics["checks"]["data_integrity"]["invalid_status"], 0)

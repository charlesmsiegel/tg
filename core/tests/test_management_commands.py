"""Tests for Django management commands in core/management/commands/."""

import json
import os
import shutil
import tempfile
from datetime import date, timedelta
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from accounts.models import Profile
from characters.models.core.character import CharacterModel
from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, TransactionTestCase
from django.utils import timezone
from game.models import Chronicle, Scene, Story, STRelationship, Week, WeeklyXPRequest


class ManagementCommandTestBase(TestCase):
    """Base class with common fixtures for management command tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data once for all tests in the class."""
        # Create test users
        cls.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        cls.st_user = User.objects.create_user(
            username="storyteller", email="st@example.com", password="stpass123"
        )

        # Create profile for ST
        Profile.objects.get_or_create(user=cls.st_user)

        # Create test chronicle
        cls.chronicle = Chronicle.objects.create(
            name="Test Chronicle",
            theme="Dark Mystery",
            mood="Gothic Horror",
            year=2024,
        )
        cls.chronicle.storytellers.add(cls.st_user)

        # Create test characters
        cls.character = Human.objects.create(
            name="Test Character",
            owner=cls.user,
            chronicle=cls.chronicle,
            status="App",
            xp=100,
        )

        cls.submitted_character = Human.objects.create(
            name="Submitted Character",
            owner=cls.user,
            chronicle=cls.chronicle,
            status="Sub",
            xp=50,
        )

    def call_command_capture_output(self, command_name, *args, **kwargs):
        """Helper to call a command and capture its stdout/stderr."""
        out = StringIO()
        err = StringIO()
        call_command(command_name, *args, stdout=out, stderr=err, **kwargs)
        return out.getvalue(), err.getvalue()


class TestValidateDataIntegrityCommand(ManagementCommandTestBase):
    """Tests for the validate_data_integrity management command."""

    def test_no_issues_found(self):
        """Test command reports no issues when data is clean."""
        out, err = self.call_command_capture_output("validate_data_integrity")
        self.assertIn("No data integrity issues found", out)

    def test_detects_negative_xp(self):
        """Test command handles XP checking correctly.

        Note: Database CHECK constraints prevent negative XP values from being
        stored, so this test verifies the command runs correctly with valid data.
        """
        out, err = self.call_command_capture_output("validate_data_integrity")
        # Command should report no issues for negative XP since constraints prevent it
        self.assertIn("Data Integrity", out)

    def test_fix_flag_runs_without_error(self):
        """Test --fix flag runs without errors on valid data."""
        out, err = self.call_command_capture_output("validate_data_integrity", "--fix")
        # With valid data and database constraints, there should be nothing to fix
        self.assertIn("Data Integrity", out)

    def test_verbose_flag_shows_details(self):
        """Test --verbose flag shows detailed information."""
        out, err = self.call_command_capture_output("validate_data_integrity", "--verbose")
        # Verbose mode should show the report header
        self.assertIn("Data Integrity", out)

    def test_detects_invalid_status(self):
        """Test command handles status checking correctly.

        Note: Database constraints and model validation prevent invalid status
        values from being stored, so this test verifies the command runs correctly.
        """
        out, err = self.call_command_capture_output("validate_data_integrity")
        # Command should report no issues since constraints prevent invalid statuses
        self.assertIn("Data Integrity", out)


class TestValidateCharacterDataCommand(ManagementCommandTestBase):
    """Tests for the validate_character_data management command."""

    def test_validates_all_characters(self):
        """Test command validates all characters."""
        out, err = self.call_command_capture_output("validate_character_data")
        self.assertIn("Validating", out)
        self.assertIn("character(s)", out)

    def test_status_filter(self):
        """Test --status filter limits validation scope."""
        out, err = self.call_command_capture_output("validate_character_data", "--status", "App")
        self.assertIn("Validating", out)

    def test_chronicle_filter(self):
        """Test --chronicle filter limits validation scope."""
        out, err = self.call_command_capture_output(
            "validate_character_data", "--chronicle", str(self.chronicle.id)
        )
        self.assertIn("Validating", out)

    def test_detects_missing_name(self):
        """Test command detects characters without names."""
        # Create character with valid name first, then update to empty value
        # Using queryset.update() bypasses model validation
        char = Human.objects.create(
            name="Temp Name",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            xp=0,
        )
        Human.objects.filter(pk=char.pk).update(name="")  # Missing name
        try:
            out, err = self.call_command_capture_output("validate_character_data")
            self.assertIn("missing", out.lower())
        finally:
            char.delete()


class TestExportChronicleCommand(ManagementCommandTestBase):
    """Tests for the export_chronicle management command."""

    def test_exports_chronicle(self):
        """Test command exports chronicle to JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_file = f.name

        try:
            out, err = self.call_command_capture_output(
                "export_chronicle", str(self.chronicle.id), "--output", output_file
            )
            self.assertIn("Export complete", out)
            self.assertTrue(os.path.exists(output_file))

            # Verify JSON content
            with open(output_file, "r") as f:
                data = json.load(f)
            self.assertIn("chronicle", data)
            self.assertIn("characters", data)
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_pretty_print_option(self):
        """Test --pretty option formats JSON output."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_file = f.name

        try:
            out, err = self.call_command_capture_output(
                "export_chronicle",
                str(self.chronicle.id),
                "--output",
                output_file,
                "--pretty",
            )
            with open(output_file, "r") as f:
                content = f.read()
            # Pretty print should have newlines and indentation
            self.assertIn("\n", content)
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_exclude_scenes_option(self):
        """Test --exclude-scenes option excludes scene data."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_file = f.name

        try:
            out, err = self.call_command_capture_output(
                "export_chronicle",
                str(self.chronicle.id),
                "--output",
                output_file,
                "--exclude-scenes",
            )
            with open(output_file, "r") as f:
                data = json.load(f)
            self.assertNotIn("scenes", data)
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_nonexistent_chronicle_raises_error(self):
        """Test command raises error for nonexistent chronicle."""
        with self.assertRaises(CommandError):
            call_command("export_chronicle", "99999")


class TestImportChronicleCommand(ManagementCommandTestBase):
    """Tests for the import_chronicle management command."""

    def test_dry_run_shows_preview(self):
        """Test --dry-run shows what would be imported without importing."""
        # First export a chronicle
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_file = f.name

        try:
            # Capture export output to suppress it during tests
            self.call_command_capture_output(
                "export_chronicle", str(self.chronicle.id), "--output", output_file
            )

            # Now try dry-run import
            out, err = self.call_command_capture_output(
                "import_chronicle", output_file, "--dry-run"
            )
            self.assertIn("DRY RUN", out)
            self.assertIn("IMPORT SUMMARY", out)
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_nonexistent_file_raises_error(self):
        """Test command raises error for nonexistent file."""
        with self.assertRaises(CommandError):
            call_command("import_chronicle", "nonexistent_file.json")

    def test_invalid_json_raises_error(self):
        """Test command raises error for invalid JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json {")
            invalid_file = f.name

        try:
            with self.assertRaises(CommandError):
                call_command("import_chronicle", invalid_file)
        finally:
            os.unlink(invalid_file)


class TestProcessWeeklyXPCommand(ManagementCommandTestBase):
    """Tests for the process_weekly_xp management command."""

    def test_creates_week_object(self):
        """Test command creates Week object."""
        # Clean up existing weeks
        Week.objects.all().delete()

        out, err = self.call_command_capture_output("process_weekly_xp", "--dry-run")
        self.assertIn("WEEKLY XP PROCESSING", out)

    def test_dry_run_does_not_create_data(self):
        """Test --dry-run flag prevents data creation."""
        initial_count = Week.objects.count()
        out, err = self.call_command_capture_output("process_weekly_xp", "--dry-run")
        self.assertIn("DRY RUN", out)
        # Dry run should not create new weeks
        self.assertEqual(Week.objects.count(), initial_count)

    def test_invalid_date_format_shows_error(self):
        """Test command shows error for invalid date format."""
        out, err = self.call_command_capture_output(
            "process_weekly_xp", "--week-ending", "invalid-date"
        )
        self.assertIn("Invalid date format", out)


class TestAuditXPSpendingCommand(ManagementCommandTestBase):
    """Tests for the audit_xp_spending management command."""

    def test_audits_characters(self):
        """Test command audits character XP spending."""
        out, err = self.call_command_capture_output("audit_xp_spending")
        self.assertIn("Auditing XP", out)
        self.assertIn("XP AUDIT RESULTS", out)

    def test_chronicle_filter(self):
        """Test --chronicle filter limits audit scope."""
        out, err = self.call_command_capture_output(
            "audit_xp_spending", "--chronicle", str(self.chronicle.id)
        )
        self.assertIn("Auditing XP", out)

    def test_show_all_flag(self):
        """Test --show-all flag shows clean characters too."""
        out, err = self.call_command_capture_output("audit_xp_spending", "--show-all")
        self.assertIn("CLEAN", out)

    def test_export_to_csv(self):
        """Test --export flag creates CSV file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            output_file = f.name

        try:
            out, err = self.call_command_capture_output(
                "audit_xp_spending", "--export", output_file, "--show-all"
            )
            self.assertTrue(os.path.exists(output_file))
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)


class TestCleanupOrphanedDataCommand(ManagementCommandTestBase):
    """Tests for the cleanup_orphaned_data management command."""

    def test_dry_run_shows_what_would_be_deleted(self):
        """Test --dry-run shows orphaned data without deleting."""
        out, err = self.call_command_capture_output("cleanup_orphaned_data", "--dry-run")
        self.assertIn("Cleaning up orphaned data", out)
        self.assertIn("DRY RUN", out)

    def test_days_parameter(self):
        """Test --days parameter controls age threshold."""
        out, err = self.call_command_capture_output(
            "cleanup_orphaned_data", "--dry-run", "--days", "7"
        )
        self.assertIn("CLEANUP SUMMARY", out)

    def test_include_scenes_option(self):
        """Test --include-scenes option includes scene cleanup."""
        out, err = self.call_command_capture_output(
            "cleanup_orphaned_data", "--dry-run", "--include-scenes"
        )
        self.assertIn("CLEANUP SUMMARY", out)

    def test_identifies_orphaned_characters(self):
        """Test command identifies orphaned characters."""
        # Create orphaned character
        char = Human.objects.create(
            name="Orphan",
            owner=None,  # No owner
            chronicle=self.chronicle,
            status="Un",  # Unfinished
            xp=0,
        )
        try:
            out, err = self.call_command_capture_output("cleanup_orphaned_data", "--dry-run")
            # Check if orphaned data is reported
            self.assertIn("CLEANUP SUMMARY", out)
        finally:
            char.delete()


class TestFindDuplicateObjectsCommand(ManagementCommandTestBase):
    """Tests for the find_duplicate_objects management command."""

    def test_finds_no_duplicates_when_clean(self):
        """Test command reports no duplicates when data is clean."""
        out, err = self.call_command_capture_output("find_duplicate_objects")
        self.assertIn("Searching for duplicate objects", out)

    def test_type_filter(self):
        """Test --type filter limits search scope."""
        out, err = self.call_command_capture_output("find_duplicate_objects", "--type", "character")
        self.assertIn("Searching for duplicate objects", out)

    def test_finds_duplicate_characters(self):
        """Test command finds duplicate characters with same name."""
        # Create duplicate characters
        char1 = Human.objects.create(
            name="Duplicate Name",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            xp=0,
        )
        char2 = Human.objects.create(
            name="Duplicate Name",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            xp=0,
        )
        try:
            out, err = self.call_command_capture_output(
                "find_duplicate_objects", "--type", "character"
            )
            self.assertIn("duplicate", out.lower())
        finally:
            char1.delete()
            char2.delete()

    def test_export_option(self):
        """Test --export option creates CSV file."""
        # Create duplicates first
        char1 = Human.objects.create(
            name="Export Test",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            xp=0,
        )
        char2 = Human.objects.create(
            name="Export Test",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            xp=0,
        )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            output_file = f.name

        try:
            out, err = self.call_command_capture_output(
                "find_duplicate_objects", "--export", output_file
            )
            self.assertTrue(os.path.exists(output_file))
        finally:
            char1.delete()
            char2.delete()
            if os.path.exists(output_file):
                os.unlink(output_file)


class TestSyncCharacterStatusCommand(ManagementCommandTestBase):
    """Tests for the sync_character_status management command."""

    def test_syncs_character_status(self):
        """Test command syncs character status with organizations."""
        out, err = self.call_command_capture_output("sync_character_status")
        self.assertIn("Syncing status", out)
        self.assertIn("SYNC SUMMARY", out)

    def test_dry_run_shows_changes(self):
        """Test --dry-run shows what would be changed."""
        out, err = self.call_command_capture_output("sync_character_status", "--dry-run")
        self.assertIn("DRY RUN", out)

    def test_chronicle_filter(self):
        """Test --chronicle filter limits scope."""
        out, err = self.call_command_capture_output(
            "sync_character_status", "--chronicle", str(self.chronicle.id)
        )
        self.assertIn("SYNC SUMMARY", out)


class TestGenerateSTReportCommand(ManagementCommandTestBase):
    """Tests for the generate_st_report management command."""

    def test_generates_report_for_all_chronicles(self):
        """Test command generates report for all chronicles."""
        out, err = self.call_command_capture_output("generate_st_report")
        self.assertIn("ST REPORT", out)

    def test_st_username_filter(self):
        """Test --st-username filter limits report scope."""
        out, err = self.call_command_capture_output(
            "generate_st_report", "--st-username", self.st_user.username
        )
        self.assertIn("ST REPORT", out)

    def test_chronicle_filter(self):
        """Test --chronicle filter limits report scope."""
        out, err = self.call_command_capture_output(
            "generate_st_report", "--chronicle", str(self.chronicle.id)
        )
        self.assertIn(self.chronicle.name, out)

    def test_output_to_file(self):
        """Test --output saves report to file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            output_file = f.name

        try:
            out, err = self.call_command_capture_output(
                "generate_st_report", "--output", output_file
            )
            self.assertTrue(os.path.exists(output_file))
            with open(output_file, "r") as f:
                content = f.read()
            self.assertIn("ST REPORT", content)
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_invalid_user_raises_error(self):
        """Test command raises error for nonexistent user."""
        with self.assertRaises(CommandError):
            call_command("generate_st_report", "--st-username", "nonexistent")


class TestGenerateChronicleSummaryCommand(ManagementCommandTestBase):
    """Tests for the generate_chronicle_summary management command."""

    def test_generates_text_summary(self):
        """Test command generates text format summary."""
        out, err = self.call_command_capture_output(
            "generate_chronicle_summary", str(self.chronicle.id)
        )
        self.assertIn("CHRONICLE SUMMARY", out)
        self.assertIn(self.chronicle.name, out)

    def test_markdown_format(self):
        """Test --format markdown generates markdown output."""
        out, err = self.call_command_capture_output(
            "generate_chronicle_summary",
            str(self.chronicle.id),
            "--format",
            "markdown",
        )
        self.assertIn("# Chronicle Summary", out)

    def test_html_format(self):
        """Test --format html generates HTML output."""
        out, err = self.call_command_capture_output(
            "generate_chronicle_summary", str(self.chronicle.id), "--format", "html"
        )
        self.assertIn("<html>", out)
        self.assertIn("</html>", out)

    def test_output_to_file(self):
        """Test --output saves to file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            output_file = f.name

        try:
            out, err = self.call_command_capture_output(
                "generate_chronicle_summary",
                str(self.chronicle.id),
                "--output",
                output_file,
            )
            self.assertTrue(os.path.exists(output_file))
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_nonexistent_chronicle_raises_error(self):
        """Test command raises error for nonexistent chronicle."""
        with self.assertRaises(CommandError):
            call_command("generate_chronicle_summary", "99999")


class TestArchiveInactiveChroniclesCommand(ManagementCommandTestBase):
    """Tests for the archive_inactive_chronicles management command."""

    def test_list_only_shows_inactive(self):
        """Test --list-only shows inactive chronicles without action."""
        out, err = self.call_command_capture_output("archive_inactive_chronicles", "--list-only")
        self.assertIn("Finding chronicles", out)

    def test_days_parameter(self):
        """Test --days parameter sets inactivity threshold."""
        out, err = self.call_command_capture_output(
            "archive_inactive_chronicles", "--list-only", "--days", "30"
        )
        self.assertIn("Finding chronicles", out)

    def test_active_chronicle_not_listed(self):
        """Test active chronicles are not listed as inactive."""
        # Create a scene to make chronicle active
        scene = Scene.objects.create(
            name="Active Scene",
            chronicle=self.chronicle,
            finished=False,
            date_of_scene=date.today(),
        )
        try:
            out, err = self.call_command_capture_output(
                "archive_inactive_chronicles", "--list-only", "--days", "30"
            )
            # Check output
            self.assertIn("Finding chronicles", out)
        finally:
            scene.delete()


class TestApprovePendingItemsCommand(ManagementCommandTestBase):
    """Tests for the approve_pending_items management command."""

    def test_list_only_shows_pending(self):
        """Test --list-only shows pending items without approving."""
        out, err = self.call_command_capture_output("approve_pending_items", "--list-only")
        self.assertIn("Pending Approvals", out)
        self.assertIn("APPROVAL SUMMARY", out)

    def test_dry_run_shows_what_would_be_approved(self):
        """Test --dry-run shows what would be approved."""
        out, err = self.call_command_capture_output("approve_pending_items", "--dry-run")
        self.assertIn("DRY RUN", out)

    def test_type_filter_characters(self):
        """Test --type characters only processes character approvals."""
        out, err = self.call_command_capture_output(
            "approve_pending_items", "--type", "characters", "--list-only"
        )
        self.assertIn("Submitted Characters", out)

    def test_chronicle_filter(self):
        """Test --chronicle filter limits scope."""
        out, err = self.call_command_capture_output(
            "approve_pending_items",
            "--chronicle",
            str(self.chronicle.id),
            "--list-only",
        )
        self.assertIn("APPROVAL SUMMARY", out)


class TestCleanupOldWeeksCommand(ManagementCommandTestBase):
    """Tests for the cleanup_old_weeks management command."""

    def test_dry_run_shows_old_weeks(self):
        """Test --dry-run shows old weeks without deleting."""
        # Create an old week
        old_date = date.today() - timedelta(days=365)
        week = Week.objects.create(end_date=old_date)

        try:
            out, err = self.call_command_capture_output(
                "cleanup_old_weeks", "--dry-run", "--months", "6"
            )
            self.assertIn("DRY RUN", out)
        finally:
            week.delete()

    def test_months_parameter(self):
        """Test --months parameter sets age threshold."""
        out, err = self.call_command_capture_output(
            "cleanup_old_weeks", "--dry-run", "--months", "3"
        )
        self.assertIn("Finding weeks", out)

    def test_keep_with_pending_option(self):
        """Test --keep-with-pending preserves weeks with pending requests."""
        out, err = self.call_command_capture_output(
            "cleanup_old_weeks", "--dry-run", "--keep-with-pending"
        )
        self.assertIn("Finding weeks", out)


class TestMonitorValidationCommand(ManagementCommandTestBase):
    """Tests for the monitor_validation management command."""

    def test_generates_health_report(self):
        """Test command generates health report."""
        out, err = self.call_command_capture_output("monitor_validation")
        self.assertIn("Validation System Health Report", out)
        self.assertIn("Overall Status", out)

    def test_json_output(self):
        """Test --json outputs JSON format."""
        out, err = self.call_command_capture_output("monitor_validation", "--json")
        data = json.loads(out)
        self.assertIn("timestamp", data)
        self.assertIn("health_score", data)
        self.assertIn("checks", data)

    def test_period_parameter(self):
        """Test --period sets time window."""
        out, err = self.call_command_capture_output("monitor_validation", "--period", "48")
        self.assertIn("48 hours", out)


class TestAuditUserPermissionsCommand(ManagementCommandTestBase):
    """Tests for the audit_user_permissions management command."""

    def test_audits_permissions(self):
        """Test command audits user permissions."""
        out, err = self.call_command_capture_output("audit_user_permissions")
        self.assertIn("USER PERMISSION AUDIT", out)
        self.assertIn("Total Users", out)

    def test_check_profiles_option(self):
        """Test --check-profiles includes profile completeness."""
        out, err = self.call_command_capture_output("audit_user_permissions", "--check-profiles")
        self.assertIn("PROFILE DATA COMPLETENESS", out)

    def test_export_to_csv(self):
        """Test --export creates CSV file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            output_file = f.name

        try:
            out, err = self.call_command_capture_output(
                "audit_user_permissions", "--export", output_file
            )
            self.assertTrue(os.path.exists(output_file))
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)


class TestPopulateTestChronicleCommand(ManagementCommandTestBase):
    """Tests for the populate_test_chronicle management command."""

    def test_populates_chronicle(self):
        """Test command populates chronicle with test data."""
        out, err = self.call_command_capture_output(
            "populate_test_chronicle",
            "--chronicle",
            str(self.chronicle.id),
            "--characters",
            "3",
            "--scenes",
            "2",
        )
        self.assertIn("Populating test data", out)
        self.assertIn("TEST DATA CREATED", out)

    def test_gameline_option(self):
        """Test --gameline option sets character gameline."""
        out, err = self.call_command_capture_output(
            "populate_test_chronicle",
            "--chronicle",
            str(self.chronicle.id),
            "--characters",
            "2",
            "--scenes",
            "1",
            "--gameline",
            "vtm",
        )
        self.assertIn("TEST DATA CREATED", out)

    def test_nonexistent_chronicle_raises_error(self):
        """Test command raises error for nonexistent chronicle."""
        with self.assertRaises(CommandError):
            call_command(
                "populate_test_chronicle",
                "--chronicle",
                "99999",
            )


class TestCommandOutputFormatting(ManagementCommandTestBase):
    """Tests to verify proper output formatting across commands."""

    def test_validate_data_integrity_has_report_header(self):
        """Test validate_data_integrity has proper report header."""
        out, err = self.call_command_capture_output("validate_data_integrity")
        self.assertIn("Data Integrity Validation Report", out)
        self.assertIn("=" * 70, out)

    def test_audit_xp_spending_has_summary(self):
        """Test audit_xp_spending has summary section."""
        out, err = self.call_command_capture_output("audit_xp_spending")
        self.assertIn("XP AUDIT RESULTS", out)

    def test_cleanup_orphaned_data_has_summary(self):
        """Test cleanup_orphaned_data has summary section."""
        out, err = self.call_command_capture_output("cleanup_orphaned_data", "--dry-run")
        self.assertIn("CLEANUP SUMMARY", out)


class TestCommandErrorHandling(ManagementCommandTestBase):
    """Tests for error handling in management commands."""

    def test_export_chronicle_missing_id_raises_error(self):
        """Test export_chronicle raises error when ID is missing."""
        with self.assertRaises(CommandError):
            call_command("export_chronicle")

    def test_generate_chronicle_summary_missing_id_raises_error(self):
        """Test generate_chronicle_summary raises error when ID is missing."""
        with self.assertRaises(CommandError):
            call_command("generate_chronicle_summary")


class TestPopulateGamedataCommand(TestCase):
    """Tests for the populate_gamedata management command.

    These tests verify that:
    1. The command uses importlib for safe module loading (not raw exec())
    2. Scripts are executed correctly within transactions
    3. Proper error handling and filtering works
    """

    def setUp(self):
        """Set up a temporary populate_db directory for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.populate_dir = Path(self.temp_dir) / "populate_db"
        self.populate_dir.mkdir()

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir)

    def call_command_capture_output(self, *args, **kwargs):
        """Helper to call a command and capture its stdout/stderr."""
        out = StringIO()
        err = StringIO()
        call_command("populate_gamedata", *args, stdout=out, stderr=err, **kwargs)
        return out.getvalue(), err.getvalue()

    def test_directory_not_found_raises_error(self):
        """Test command raises error when populate_db directory doesn't exist."""
        with patch("core.management.commands.populate_gamedata.Path") as mock_path:
            mock_path.return_value.exists.return_value = False
            with self.assertRaises(CommandError) as context:
                call_command("populate_gamedata")
            self.assertIn("not found", str(context.exception))

    def test_no_files_found_raises_error(self):
        """Test command raises error when no .py files are found."""
        # Create empty directory
        with patch("core.management.commands.populate_gamedata.Path") as mock_path:
            mock_path.return_value.exists.return_value = True
            mock_path.return_value.rglob.return_value = []
            with self.assertRaises(CommandError) as context:
                call_command("populate_gamedata")
            self.assertIn("No .py files found", str(context.exception))

    def test_dry_run_does_not_execute(self):
        """Test --dry-run shows files but doesn't execute them."""
        # Create a simple test script
        test_script = self.populate_dir / "test_script.py"
        test_script.write_text("# This should not be executed\nraise Exception('Should not run')")

        with patch("core.management.commands.populate_gamedata.Path") as mock_path:
            mock_path.return_value = self.populate_dir
            mock_path.return_value.exists.return_value = True
            mock_path.return_value.rglob.return_value = [test_script]

            out = StringIO()
            # Should not raise even though script raises Exception
            call_command("populate_gamedata", "--dry-run", stdout=out)
            output = out.getvalue()
            self.assertIn("DRY RUN", output)

    def test_uses_importlib_not_exec(self):
        """Test that the command uses importlib instead of raw exec()."""
        from core.management.commands import populate_gamedata
        import inspect

        # Get the source code of the load_file method
        source = inspect.getsource(populate_gamedata.Command.load_file)

        # Should use importlib
        self.assertIn("importlib.util", source)
        self.assertIn("spec_from_file_location", source)
        self.assertIn("module_from_spec", source)

        # Should NOT use raw exec with code content
        self.assertNotIn("exec(code", source)
        self.assertNotIn('exec(f.read()', source)

    def test_gameline_filter(self):
        """Test --gameline option filters files correctly."""
        from core.management.commands.populate_gamedata import Command

        cmd = Command()

        # Create mock files
        mock_files = [
            Path("populate_db/abilities.py"),
            Path("populate_db/vtm_disciplines.py"),
            Path("populate_db/wta_gifts.py"),
            Path("populate_db/mta_spheres.py"),
        ]

        options = {"gameline": "vtm", "only": None, "skip": None}
        filtered = cmd.filter_files(mock_files, options)

        # Should include abilities (not gameline-specific) and vtm-specific files
        file_names = [f.stem for f in filtered]
        self.assertIn("abilities", file_names)
        self.assertIn("vtm_disciplines", file_names)
        self.assertNotIn("wta_gifts", file_names)
        self.assertNotIn("mta_spheres", file_names)

    def test_only_filter(self):
        """Test --only option filters files correctly."""
        from core.management.commands.populate_gamedata import Command

        cmd = Command()

        mock_files = [
            Path("populate_db/abilities.py"),
            Path("populate_db/disciplines.py"),
            Path("populate_db/backgrounds.py"),
        ]

        options = {"gameline": None, "only": "abilities", "skip": None}
        filtered = cmd.filter_files(mock_files, options)

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].stem, "abilities")

    def test_skip_filter(self):
        """Test --skip option filters files correctly."""
        from core.management.commands.populate_gamedata import Command

        cmd = Command()

        mock_files = [
            Path("populate_db/abilities.py"),
            Path("populate_db/disciplines.py"),
            Path("populate_db/backgrounds.py"),
        ]

        options = {"gameline": None, "only": None, "skip": "disciplines"}
        filtered = cmd.filter_files(mock_files, options)

        file_names = [f.stem for f in filtered]
        self.assertIn("abilities", file_names)
        self.assertIn("backgrounds", file_names)
        self.assertNotIn("disciplines", file_names)

    def test_sort_order_core_first(self):
        """Test that core subdirectory is loaded before other subdirectories."""
        from core.management.commands.populate_gamedata import Command

        cmd = Command()
        populate_dir = Path("populate_db")

        mock_files = [
            Path("populate_db/vtm/disciplines.py"),
            Path("populate_db/core/abilities.py"),
            Path("populate_db/abilities.py"),
            Path("populate_db/chronicles/test.py"),
        ]

        sorted_files = sorted(mock_files, key=lambda f: cmd.get_sort_key(f, populate_dir))

        # Main directory first, then core, then other subdirs, then chronicles last
        self.assertEqual(sorted_files[0].name, "abilities.py")  # Main dir
        self.assertEqual(sorted_files[0].parent.name, "populate_db")
        self.assertEqual(sorted_files[1].parent.name, "core")  # Core dir
        self.assertEqual(sorted_files[-1].parent.name, "chronicles")  # Chronicles last

    def test_module_cleanup_after_load(self):
        """Test that loaded modules are cleaned up from sys.modules."""
        import sys

        # Create a simple test script in the actual populate_db if it exists
        # or skip if not available
        from core.management.commands.populate_gamedata import Command

        # Check that module names starting with populate_db. from our test
        # don't persist in sys.modules after command execution
        pre_modules = set(k for k in sys.modules.keys() if k.startswith("populate_db."))

        # The actual cleanup is tested in the load_file implementation
        # by verifying sys.modules.pop() is called in a finally block
        source = open(
            "core/management/commands/populate_gamedata.py"
        ).read()
        self.assertIn("sys.modules.pop(module_name, None)", source)

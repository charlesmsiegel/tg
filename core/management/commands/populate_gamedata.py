"""
Management command to populate the database with game data from populate_db/ directory.

This command replaces the setup_db.sh script and provides more control over data loading.
"""
import os
import sys
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Populate database with World of Darkness game data from populate_db/ scripts"

    def add_arguments(self, parser):
        parser.add_argument(
            "--gameline",
            type=str,
            help="Only load data for specific gameline (vtm, wta, mta, wto, ctd, dtf)",
        )
        parser.add_argument(
            "--only",
            type=str,
            help="Only load specific data type (e.g., abilities, backgrounds, disciplines)",
        )
        parser.add_argument(
            "--skip",
            type=str,
            help="Skip specific data type (e.g., books, resonance)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be loaded without actually loading it",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Show detailed output for each file",
        )

    def handle(self, *args, **options):
        populate_dir = Path("populate_db")

        if not populate_dir.exists():
            raise CommandError(f"Directory {populate_dir} not found")

        # Get all .py files in populate_db directory
        all_files = sorted(populate_dir.glob("*.py"))

        if not all_files:
            raise CommandError(f"No .py files found in {populate_dir}")

        # Filter files based on options
        files_to_load = self.filter_files(all_files, options)

        if not files_to_load:
            self.stdout.write(
                self.style.WARNING("No files match the specified filters")
            )
            return

        # Display what will be loaded
        self.stdout.write(
            self.style.SUCCESS(f"\nFound {len(files_to_load)} file(s) to load:")
        )
        for file in files_to_load:
            self.stdout.write(f"  - {file.name}")

        if options["dry_run"]:
            self.stdout.write(
                self.style.WARNING("\n[DRY RUN] No data was actually loaded")
            )
            return

        # Load each file
        self.stdout.write(self.style.SUCCESS("\nLoading data...\n"))

        success_count = 0
        error_count = 0

        for file in files_to_load:
            try:
                self.load_file(file, options["verbose"])
                success_count += 1
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f"✗ {file.name}: {str(e)}")
                )
                if options["verbose"]:
                    import traceback
                    self.stdout.write(traceback.format_exc())

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(
            self.style.SUCCESS(f"Successfully loaded: {success_count} file(s)")
        )
        if error_count > 0:
            self.stdout.write(
                self.style.ERROR(f"Failed to load: {error_count} file(s)")
            )
        self.stdout.write("=" * 60 + "\n")

    def filter_files(self, files, options):
        """Filter files based on command-line options."""
        filtered = list(files)

        # Filter by gameline
        if options["gameline"]:
            gameline = options["gameline"].lower()
            filtered = [
                f for f in filtered
                if gameline in f.stem.lower() or not self.is_gameline_specific(f)
            ]

        # Filter by --only option
        if options["only"]:
            only = options["only"].lower()
            filtered = [f for f in filtered if only in f.stem.lower()]

        # Filter by --skip option
        if options["skip"]:
            skip = options["skip"].lower()
            filtered = [f for f in filtered if skip not in f.stem.lower()]

        return filtered

    def is_gameline_specific(self, file):
        """Check if a file is specific to a gameline."""
        gamelines = ["vampire", "werewolf", "mage", "wraith", "changeling", "demon",
                     "vtm", "wta", "mta", "wto", "ctd", "dtf"]
        stem = file.stem.lower()
        return any(gl in stem for gl in gamelines)

    def load_file(self, file, verbose=False):
        """Execute a populate script file."""
        if verbose:
            self.stdout.write(f"Loading {file.name}...", ending="")

        # Read and execute the file
        with open(file, "r") as f:
            code = f.read()

        # Execute in a transaction for safety
        with transaction.atomic():
            exec(code, {"__name__": "__main__"})

        if verbose:
            self.stdout.write(self.style.SUCCESS(" ✓"))
        else:
            self.stdout.write(f"✓ {file.name}")

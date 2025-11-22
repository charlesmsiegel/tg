"""
Management command to populate the database with game data from populate_db/ directory.

This command recursively searches populate_db/ and all subdirectories for .py scripts
and provides more control over data loading.
"""
import os
import sys
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Populate database with World of Darkness game data from populate_db/ scripts (searches recursively)"

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

    def get_sort_key(self, file, populate_dir):
        """
        Generate a sort key for files to ensure proper loading order:
        1. Main directory files first
        2. Then 'core' subdirectory
        3. Then other subdirectories alphabetically
        4. Then 'chronicles' subdirectory last
        Within each category, sort files alphabetically
        """
        relative_path = file.relative_to(populate_dir)
        parts = relative_path.parts

        # Files in the main directory (no subdirectory)
        if len(parts) == 1:
            return (0, relative_path.name)

        # Files in subdirectories
        subdir = parts[0].lower()

        # Assign priority: core=1, chronicles=999, others=500
        if subdir == "core":
            priority = 1
        elif subdir == "chronicles":
            priority = 999
        else:
            priority = 500

        # Return tuple: (priority, subdirectory name, file path)
        # This ensures proper ordering within each priority level
        return (priority, subdir, str(relative_path))

    def handle(self, *args, **options):
        populate_dir = Path("populate_db")

        if not populate_dir.exists():
            raise CommandError(f"Directory {populate_dir} not found")

        # Get all .py files in populate_db directory (recursively)
        all_files = sorted(
            populate_dir.rglob("*.py"), key=lambda f: self.get_sort_key(f, populate_dir)
        )

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
            # Show relative path from populate_db for better context
            relative_path = file.relative_to(populate_dir)
            self.stdout.write(f"  - {relative_path}")

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
                self.load_file(file, populate_dir, options["verbose"])
                success_count += 1
            except Exception as e:
                error_count += 1
                relative_path = file.relative_to(populate_dir)
                self.stdout.write(self.style.ERROR(f"✗ {relative_path}: {str(e)}"))
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
                f
                for f in filtered
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
        gamelines = [
            "vampire",
            "werewolf",
            "mage",
            "wraith",
            "changeling",
            "demon",
            "vtm",
            "wta",
            "mta",
            "wto",
            "ctd",
            "dtf",
        ]
        stem = file.stem.lower()
        return any(gl in stem for gl in gamelines)

    def load_file(self, file, populate_dir, verbose=False):
        """Execute a populate script file."""
        relative_path = file.relative_to(populate_dir)

        if verbose:
            self.stdout.write(f"Loading {relative_path}...", ending="")

        # Read and execute the file
        with open(file, "r") as f:
            code = f.read()

        # Execute in a transaction for safety
        with transaction.atomic():
            exec(code, {"__name__": "__main__"})

        if verbose:
            self.stdout.write(self.style.SUCCESS(" ✓"))
        else:
            self.stdout.write(f"✓ {relative_path}")

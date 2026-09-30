"""
Management command to populate the database with game data from populate_db/ directory.

This command recursively searches populate_db/ and all subdirectories for .py scripts
and provides more control over data loading.
"""

import logging
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

logger = logging.getLogger(__name__)


def gameline_words():
    """Map each gameline code to the words that mark a file as its own.

    A code matches itself and its ``app_name`` (``vtm`` -> ``vtm``, ``vampire``), which is
    also the name of its folder under ``populate_db/``. ``wod`` is shared data.
    """
    return {
        code: {code, info["app_name"]} for code, info in settings.GAMELINES.items() if code != "wod"
    }


class Command(BaseCommand):
    help = "Populate database with World of Darkness game data from populate_db/ scripts (searches recursively)"

    def add_arguments(self, parser):
        """Define command-line arguments for the populate_gamedata command."""
        parser.add_argument(
            "--gameline",
            type=str,
            help=(
                "Only load shared data plus one gameline's data; takes a code or name "
                "(vtm or vampire, wta or werewolf, mta or mage, ...)"
            ),
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
        """Execute the populate_gamedata command.

        Discovers and executes Python scripts in populate_db/ directory,
        respecting filters and loading order.
        """
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
        files_to_load = self.filter_files(all_files, options, populate_dir)

        if not files_to_load:
            self.stdout.write(self.style.WARNING("No files match the specified filters"))
            return

        # Display what will be loaded
        self.stdout.write(self.style.SUCCESS(f"\nFound {len(files_to_load)} file(s) to load:"))
        for file in files_to_load:
            # Show relative path from populate_db for better context
            relative_path = file.relative_to(populate_dir)
            self.stdout.write(f"  - {relative_path}")

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING("\n[DRY RUN] No data was actually loaded"))
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
                logger.error(f"Failed to load game data file {relative_path}: {e}", exc_info=True)
                if options["verbose"]:
                    import traceback

                    self.stdout.write(traceback.format_exc())

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS(f"Successfully loaded: {success_count} file(s)"))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f"Failed to load: {error_count} file(s)"))
        self.stdout.write("=" * 60 + "\n")

        if error_count > 0:
            raise CommandError(f"{error_count} populate_db script(s) failed")

    def resolve_gameline(self, value):
        """Return the gameline code for a code or name, or raise CommandError."""
        words = gameline_words()
        value = value.lower()
        for code, names in words.items():
            if value in names:
                return code
        valid = ", ".join(sorted(words))
        raise CommandError(f"Unknown gameline {value!r}; use a code ({valid}) or its name")

    def filter_files(self, files, options, populate_dir):
        """Filter files based on command-line options."""
        filtered = list(files)

        # Filter by gameline: keep shared files and the chosen gameline's files
        if options["gameline"]:
            gameline = self.resolve_gameline(options["gameline"])
            filtered = [
                f
                for f in filtered
                if not (gamelines := self.file_gamelines(f, populate_dir)) or gameline in gamelines
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

    def file_gamelines(self, file, populate_dir):
        """Gameline codes a file belongs to: by its folder, or a word of its name.

        ``vampire/linear_magic_path.py`` and ``character_templates/vampire_templates.py``
        are both ``vtm``; ``abilities.py`` names no gameline and is shared.
        """
        parts = file.relative_to(populate_dir).parts
        words = set(re.split(r"[^a-z0-9]+", file.stem.lower()))
        if len(parts) > 1:
            words.add(parts[0].lower())
        return {code for code, names in gameline_words().items() if words & names}

    def load_file(self, file, populate_dir, verbose=False):
        """Execute a populate script file."""
        relative_path = file.relative_to(populate_dir)

        if verbose:
            self.stdout.write(f"Loading {relative_path}...", ending="")

        # Read and execute the file
        with open(file) as f:
            code = f.read()

        # Execute in a transaction for safety
        with transaction.atomic():
            exec(code, {"__name__": "__main__"})

        if verbose:
            self.stdout.write(self.style.SUCCESS(" ✓"))
        else:
            self.stdout.write(f"✓ {relative_path}")

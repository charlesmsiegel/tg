#!/usr/bin/env python
"""
Debug script to run any populate_db script with full traceback and error reporting.

Usage:
    python scripts/debug/debug_populate.py populate_db/rotes.py
    python scripts/debug/debug_populate.py populate_db/merits_and_flaws.py

Security: Uses importlib for controlled module loading instead of raw exec().
"""
import importlib.util
import os
import sys
import traceback
from pathlib import Path

import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg.settings")
django.setup()


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/debug/debug_populate.py <path_to_populate_script>")
        print("\nExample:")
        print("    python scripts/debug/debug_populate.py populate_db/rotes.py")
        print("    python scripts/debug/debug_populate.py populate_db/merits_and_flaws.py")
        sys.exit(1)

    script_path = Path(sys.argv[1])

    if not script_path.exists():
        print(f"Error: Script not found: {script_path}")
        sys.exit(1)

    if not script_path.suffix == ".py":
        print(f"Error: File must be a Python script (.py): {script_path}")
        sys.exit(1)

    try:
        print(f"Running {script_path}...")
        print("=" * 70)

        # Use importlib for safer module loading instead of raw exec()
        module_name = f"debug_populate_{script_path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        if spec is None or spec.loader is None:
            print(f"Error: Could not load spec for {script_path}")
            sys.exit(1)

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        finally:
            # Clean up sys.modules
            sys.modules.pop(module_name, None)

        print("=" * 70)
        print("✓ Script completed successfully!")

    except Exception as e:
        print("\n" + "=" * 70)
        print("ERROR FOUND:")
        print("=" * 70)
        print(f"\nError Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print("\nFull Traceback:")
        print("-" * 70)
        traceback.print_exc()
        print("-" * 70)

        # Try to extract the line number from the traceback
        tb = sys.exc_info()[2]
        script_name = script_path.name

        while tb.tb_next:
            frame = tb.tb_frame
            if script_name in frame.f_code.co_filename:
                print(f"\n>>> Error occurs at line {tb.tb_lineno} in {script_name}")
                print(f">>> In context: {frame.f_code.co_name}")
            tb = tb.tb_next

        sys.exit(1)


if __name__ == "__main__":
    main()

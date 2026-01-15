#!/usr/bin/env python3
"""
M20 Rules Reference Lookup

Usage:
    python lookup.py <json_file> <key>           # Get value for key
    python lookup.py <json_file> <key1> <key2>   # Get multiple keys
    python lookup.py <json_file> --keys          # List all keys
    python lookup.py <json_file> --all           # Dump entire file
    python lookup.py <json_file> --find <term>   # Find keys/values containing term

Examples:
    python lookup.py references/practice-abilities.json "High Ritual Magick"
    python lookup.py references/faction-practices.json "Order of Hermes" "Verbena"
    python lookup.py references/practice-abilities.json --find Occult
"""

import json
import sys
from pathlib import Path


def load_json(filepath: str) -> dict:
    path = Path(filepath)
    if not path.exists():
        # Try relative to script location
        script_dir = Path(__file__).parent.parent
        path = script_dir / filepath
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return json.load(f)

def format_value(value) -> str:
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    if isinstance(value, dict):
        # For sphere levels: "1: desc, 2: desc, ..."
        # For effects: "spheres: X, category: Y"
        parts = []
        for k, v in value.items():
            if isinstance(v, list):
                v = ", ".join(v)
            parts.append(f"{k}: {v}")
        return " | ".join(parts)
    return str(value)

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    json_file = sys.argv[1]
    data = load_json(json_file)

    # Handle flags
    if sys.argv[2] == "--keys":
        keys = [k for k in data.keys() if not k.startswith("_")]
        print("\n".join(sorted(keys)))
        return

    if sys.argv[2] == "--all":
        for key, value in sorted(data.items()):
            if not key.startswith("_"):
                print(f"{key}: {format_value(value)}")
        return

    if sys.argv[2] == "--find":
        if len(sys.argv) < 4:
            print("Error: --find requires a search term", file=sys.stderr)
            sys.exit(1)
        term = sys.argv[3].lower()
        for key, value in data.items():
            if key.startswith("_"):
                continue
            val_str = format_value(value).lower()
            if term in key.lower() or term in val_str:
                print(f"{key}: {format_value(value)}")
        return

    # Regular key lookups
    keys = sys.argv[2:]
    for key in keys:
        if key in data:
            print(f"{key}: {format_value(data[key])}")
        else:
            # Try case-insensitive match
            matches = [k for k in data.keys() if k.lower() == key.lower()]
            if matches:
                k = matches[0]
                print(f"{k}: {format_value(data[k])}")
            else:
                print(f"{key}: NOT FOUND", file=sys.stderr)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Parse XLSX file with game data into a pandas DataFrame.

Expected columns in first sheet:
- Title
- Game Line
- Edition
- (additional columns as present in the file)
"""

import pandas as pd
import sys
from pathlib import Path


def parse_game_data_xlsx(filepath):
    """
    Parse an XLSX file's first sheet into a pandas DataFrame.

    Args:
        filepath: Path to the XLSX file

    Returns:
        pandas.DataFrame with the parsed data
    """
    # Read the first sheet (sheet_name=0)
    df = pd.read_excel(filepath, sheet_name=0)

    # Verify expected columns are present
    expected_columns = ["Title", "Game Line", "Edition"]
    missing_columns = [col for col in expected_columns if col not in df.columns]

    if missing_columns:
        print(f"Warning: Missing expected columns: {missing_columns}")
        print(f"Available columns: {list(df.columns)}")

    return df


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python parse_xlsx.py <path_to_xlsx_file>")
        print("\nExample: python parse_xlsx.py game_data.xlsx")
        sys.exit(1)

    filepath = Path(sys.argv[1])

    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    if filepath.suffix.lower() not in ['.xlsx', '.xls']:
        print(f"Warning: File does not have .xlsx or .xls extension: {filepath}")

    # Parse the file
    print(f"Parsing {filepath}...")
    df = parse_game_data_xlsx(filepath)

    # Display basic information
    print(f"\nSuccessfully parsed {len(df)} rows")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head())

    # Display summary statistics
    print(f"\nDataFrame shape: {df.shape}")
    print(f"\nData types:")
    print(df.dtypes)

    return df


if __name__ == "__main__":
    df = main()

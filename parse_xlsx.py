#!/usr/bin/env python3
"""
Parse XLSX file with game data into a pandas DataFrame and generate Django ORM statements.

Expected columns in first sheet:
- Title
- Game Line
- Edition
- (additional columns as present in the file)
"""

import pandas as pd
import sys
from pathlib import Path


# Gameline mappings to 3-letter abbreviations
GAMELINE_MAP = {
    "Vampire: the Masquerade": "vtm",
    "Werewolf: the Apocalypse": "wta",
    "Mage: the Ascension": "mta",
    "Wraith: the Oblivion": "wto",
    "Changeling: the Dreaming": "ctd",
    "Demon: the Fallen": "dtf",
}

# Edition mappings to standardized format
EDITION_MAP = {
    "1st": "1e",
    "1st Edition": "1e",
    "First": "1e",
    "First Edition": "1e",
    "2nd": "2e",
    "2nd Edition": "2e",
    "Second": "2e",
    "Second Edition": "2e",
    "Revised": "Rev",
    "Revised Edition": "Rev",
    "20th Anniversary": "20th",
    "20th": "20th",
}


def normalize_gameline(gameline):
    """
    Normalize gameline to 3-letter abbreviation.

    Args:
        gameline: Full gameline name

    Returns:
        3-letter abbreviation or original value if not found
    """
    if pd.isna(gameline):
        return gameline

    gameline_str = str(gameline).strip()

    # Direct lookup
    if gameline_str in GAMELINE_MAP:
        return GAMELINE_MAP[gameline_str]

    # Case-insensitive lookup
    for key, value in GAMELINE_MAP.items():
        if key.lower() == gameline_str.lower():
            return value

    # Return original if no mapping found
    print(f"Warning: No mapping found for gameline '{gameline_str}'")
    return gameline_str


def normalize_edition(edition):
    """
    Normalize edition to standardized format (1e, 2e, Rev, 20th).

    Args:
        edition: Edition string

    Returns:
        Normalized edition string or original value if not found
    """
    if pd.isna(edition):
        return edition

    edition_str = str(edition).strip()

    # Direct lookup
    if edition_str in EDITION_MAP:
        return EDITION_MAP[edition_str]

    # Case-insensitive lookup
    for key, value in EDITION_MAP.items():
        if key.lower() == edition_str.lower():
            return value

    # Return original if no mapping found
    print(f"Warning: No mapping found for edition '{edition_str}'")
    return edition_str


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


def transform_dataframe(df):
    """
    Transform the dataframe by normalizing gamelines and editions.

    Args:
        df: Input DataFrame

    Returns:
        Transformed DataFrame
    """
    df_transformed = df.copy()

    if "Game Line" in df_transformed.columns:
        df_transformed["Game Line"] = df_transformed["Game Line"].apply(normalize_gameline)

    if "Edition" in df_transformed.columns:
        df_transformed["Edition"] = df_transformed["Edition"].apply(normalize_edition)

    return df_transformed


def generate_django_statements(df, output_file="tmp.py"):
    """
    Generate Django ORM get_or_create statements and write to file.

    Args:
        df: DataFrame with Title, Game Line, and Edition columns
        output_file: Path to output file (default: tmp.py)
    """
    output_lines = []

    for _, row in df.iterrows():
        title = row.get("Title", "")
        gameline = row.get("Game Line", "")
        edition = row.get("Edition", "")

        # Skip rows with missing required data
        if pd.isna(title) or pd.isna(gameline) or pd.isna(edition):
            print(f"Warning: Skipping row with missing data: {row.to_dict()}")
            continue

        # Escape single quotes in title
        title_escaped = str(title).replace("'", "\\'")

        # Generate the statement
        statement = f"Book.objects.get_or_create(name='{title_escaped}', gameline='{gameline}', edition='{edition}')"
        output_lines.append(statement)

    # Write to file
    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))

    print(f"\nGenerated {len(output_lines)} Django ORM statements in {output_file}")
    return output_lines


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

    # Transform the data
    print("\nTransforming data...")
    df_transformed = transform_dataframe(df)

    print("\nFirst few rows after transformation:")
    print(df_transformed[["Title", "Game Line", "Edition"]].head())

    # Generate Django ORM statements
    generate_django_statements(df_transformed)

    return df_transformed


if __name__ == "__main__":
    df = main()

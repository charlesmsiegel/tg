# Django Management Commands

This document describes the custom Django management commands available in this project.

## Database Management & Seeding

### populate_gamedata

Populate the database with World of Darkness game data from the `populate_db/` directory.

**Replaces**: `setup_db.sh` script

**Usage**:
```bash
# Load all game data
python manage.py populate_gamedata

# Load only specific gameline data
python manage.py populate_gamedata --gameline vtm
python manage.py populate_gamedata --gameline mta

# Load only specific data type
python manage.py populate_gamedata --only abilities
python manage.py populate_gamedata --only disciplines

# Skip specific data
python manage.py populate_gamedata --skip books

# Dry run to see what would be loaded
python manage.py populate_gamedata --dry-run

# Verbose output
python manage.py populate_gamedata --verbose
```

**Benefits**:
- Idempotent (can run multiple times safely)
- Selective loading by gameline or data type
- Better error handling than shell script
- Progress tracking

---

## Character & Data Maintenance

### validate_character_data

Validate character data integrity and report issues.

**Usage**:
```bash
# Validate all characters
python manage.py validate_character_data

# Validate only approved characters
python manage.py validate_character_data --status App

# Validate characters in specific chronicle
python manage.py validate_character_data --chronicle 1

# Attempt to fix issues automatically
python manage.py validate_character_data --fix

# Verbose output showing all issues
python manage.py validate_character_data --verbose
```

**Checks for**:
- Attribute bounds (typically 1-10, flags >15)
- XP calculation consistency
- Required fields based on status
- Orphaned spent_xp entries
- Status inconsistencies (e.g., deceased in active scenes)

---

### audit_xp_spending

Audit XP spending and detect discrepancies.

**Usage**:
```bash
# Audit all characters
python manage.py audit_xp_spending

# Audit specific chronicle
python manage.py audit_xp_spending --chronicle 1

# Flag pending spends older than 60 days
python manage.py audit_xp_spending --pending-days 60

# Show all characters, even those without issues
python manage.py audit_xp_spending --show-all

# Export results to CSV
python manage.py audit_xp_spending --export xp_audit.csv
```

**Detects**:
- Negative XP situations
- Excessive pending XP spends
- Unapproved XP requests
- Orphaned XP request objects

---

### find_duplicate_objects

Find duplicate objects (characters, items, locations, effects, etc.).

**Usage**:
```bash
# Find all duplicates
python manage.py find_duplicate_objects

# Find only character duplicates
python manage.py find_duplicate_objects --type character

# Find duplicates in specific chronicle
python manage.py find_duplicate_objects --chronicle 1

# Find duplicates for specific owner
python manage.py find_duplicate_objects --owner username

# Delete empty unfinished duplicates
python manage.py find_duplicate_objects --delete-empty

# Auto-merge exact duplicates (USE WITH CAUTION)
python manage.py find_duplicate_objects --auto-merge

# Export to CSV
python manage.py find_duplicate_objects --export duplicates.csv
```

**Works with**:
- Characters
- Items
- Locations
- Effects
- Any object inheriting from `core.models.Model`

---

## Chronicle & Campaign Management

### export_chronicle

Export a chronicle and all related data to JSON.

**Usage**:
```bash
# Export chronicle
python manage.py export_chronicle 1

# Custom output filename
python manage.py export_chronicle 1 --output my_chronicle.json

# Include user data (for migration)
python manage.py export_chronicle 1 --include-users

# Exclude scene data (for large chronicles)
python manage.py export_chronicle 1 --exclude-scenes

# Pretty-print JSON
python manage.py export_chronicle 1 --pretty
```

**Exports**:
- Chronicle metadata
- Characters
- Items
- Locations
- Scenes and stories
- Journals
- XP requests
- Setting elements
- Optionally: user data

---

### import_chronicle

Import a chronicle from JSON export.

**Usage**:
```bash
# Import chronicle
python manage.py import_chronicle chronicle_export.json

# Dry run to preview import
python manage.py import_chronicle chronicle_export.json --dry-run

# Skip user import (use existing users)
python manage.py import_chronicle chronicle_export.json --skip-users

# Remap usernames
python manage.py import_chronicle chronicle_export.json --remap-users user_mapping.json
```

**User mapping format** (`user_mapping.json`):
```json
{
  "old_username": "new_username",
  "john_old": "john_new"
}
```

**Note**: Full import of polymorphic models requires manual review. The command provides a framework for import but may need customization for your specific needs.

---

## XP & Approval Workflows

### process_weekly_xp

Process weekly XP for characters who participated in finished scenes.

**Usage**:
```bash
# Process XP for last week
python manage.py process_weekly_xp

# Process XP for specific week
python manage.py process_weekly_xp --week-ending 2025-11-24

# Auto-approve all requests
python manage.py process_weekly_xp --auto-approve

# Dry run to preview
python manage.py process_weekly_xp --dry-run

# Send notifications to STs (requires email setup)
python manage.py process_weekly_xp --notify
```

**What it does**:
1. Creates or finds Week object for the specified period
2. Identifies characters who participated in finished scenes during that week
3. Creates WeeklyXPRequest objects for each character
4. Optionally auto-approves and awards XP
5. Can send notifications to Storytellers

---

## Common Workflows

### Initial Database Setup
```bash
# 1. Run migrations
python manage.py migrate

# 2. Load all game data
python manage.py populate_gamedata

# 3. Create superuser
python manage.py createsuperuser
```

### Weekly Maintenance
```bash
# 1. Process weekly XP
python manage.py process_weekly_xp

# 2. Audit XP spending
python manage.py audit_xp_spending --chronicle YOUR_CHRONICLE_ID

# 3. Validate character data
python manage.py validate_character_data --status App
```

### Data Cleanup
```bash
# 1. Find duplicates
python manage.py find_duplicate_objects

# 2. Delete empty duplicates
python manage.py find_duplicate_objects --delete-empty

# 3. Validate remaining data
python manage.py validate_character_data
```

### Chronicle Backup
```bash
# Export chronicle with all data
python manage.py export_chronicle CHRONICLE_ID --pretty --include-users --output backup_$(date +%Y%m%d).json
```

---

## Tips

- Always use `--dry-run` first when making bulk changes
- Export data before running destructive operations
- Use `--verbose` when debugging issues
- Combine commands in shell scripts for routine maintenance
- Set up cron jobs for automated weekly XP processing

---

## Troubleshooting

**Command not found**:
- Make sure you're in the project directory
- Verify Django is installed: `python -c "import django; print(django.VERSION)"`

**Import errors**:
- Activate your virtual environment
- Install requirements: `pip install -r requirements.txt`

**Permission errors**:
- Ensure you have write permissions for output files
- Check database permissions

**Data integrity issues**:
- Run `validate_character_data` to identify problems
- Use `audit_xp_spending` to find XP discrepancies
- Check application logs for detailed error messages

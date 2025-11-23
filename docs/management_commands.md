# Django Management Commands

This document describes the custom Django management commands available in this project.

## Quick Reference

**Database Management & Seeding**
- `populate_gamedata` - Load game data from populate_db/
- `reset_demo_data` - Reset to demo/test state ⚠️
- `populate_test_chronicle` - Create test data for chronicle

**Character & Data Maintenance**
- `validate_character_data` - Validate character integrity
- `audit_xp_spending` - Audit XP calculations
- `find_duplicate_objects` - Find duplicate objects
- `sync_character_status` - Sync status with organizations
- `cleanup_orphaned_data` - Remove orphaned data
- `cleanup_old_weeks` - Clean up old Week objects

**Chronicle & Campaign Management**
- `export_chronicle` - Export chronicle to JSON
- `import_chronicle` - Import chronicle from JSON
- `archive_inactive_chronicles` - Identify/archive inactive chronicles
- `generate_chronicle_summary` - Generate statistics report

**XP & Approval Workflows**
- `process_weekly_xp` - Process weekly XP awards
- `approve_pending_items` - Bulk approve pending items

**Reporting & Analytics**
- `generate_st_report` - Generate ST dashboard report
- `audit_user_permissions` - Audit user permissions

---

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

### sync_character_status

Sync character status and remove retired/deceased from organizations.

**Usage**:
```bash
# Sync all retired/deceased characters
python manage.py sync_character_status

# Sync characters in specific chronicle
python manage.py sync_character_status --chronicle 1

# Also remove from active scenes
python manage.py sync_character_status --remove-from-scenes

# Fix all characters regardless of status
python manage.py sync_character_status --fix-all

# Dry run to preview changes
python manage.py sync_character_status --dry-run
```

**Removes from**:
- Groups and leadership positions
- Chantry memberships and roles
- Ambassador/investigator/guardian/teacher positions
- Optionally: active scenes

---

### approve_pending_items

Bulk approve pending items for storytellers.

**Usage**:
```bash
# List all pending items
python manage.py approve_pending_items --list-only

# Approve all pending items
python manage.py approve_pending_items

# Approve only characters
python manage.py approve_pending_items --type characters

# Approve only images
python manage.py approve_pending_items --type images

# Approve items in specific chronicle
python manage.py approve_pending_items --chronicle 1

# Approve items from specific user
python manage.py approve_pending_items --owner username

# Auto-approve all images
python manage.py approve_pending_items --auto-approve-images

# Dry run
python manage.py approve_pending_items --dry-run
```

**Approves**:
- Characters (Sub → App)
- Images
- Freebie spends
- XP spends
- Weekly/Story XP requests

---

### cleanup_orphaned_data

Clean up orphaned and unused data.

**Usage**:
```bash
# Clean up orphaned objects (default: 30 days old)
python manage.py cleanup_orphaned_data

# Custom age threshold
python manage.py cleanup_orphaned_data --days 60

# Also clean empty scenes
python manage.py cleanup_orphaned_data --include-scenes

# Also clean unused setting elements
python manage.py cleanup_orphaned_data --include-setting-elements

# Dry run
python manage.py cleanup_orphaned_data --dry-run
```

**Removes**:
- Orphaned characters/items/locations (no owner, unfinished, old)
- Empty scenes (no posts, no participants)
- Unused setting elements
- Orphaned XP requests

---

### archive_inactive_chronicles

Identify and archive inactive chronicles.

**Usage**:
```bash
# List inactive chronicles (default: 90 days)
python manage.py archive_inactive_chronicles --list-only

# Custom inactivity threshold
python manage.py archive_inactive_chronicles --days 180

# Export before archiving
python manage.py archive_inactive_chronicles --export-before-archive

# Mark as archived
python manage.py archive_inactive_chronicles --mark-inactive
```

**Considers inactive if**:
- No scenes for X days
- No active scenes
- No active characters

---

### generate_chronicle_summary

Generate comprehensive chronicle statistics and summary.

**Usage**:
```bash
# Generate text summary
python manage.py generate_chronicle_summary 1

# Save to file
python manage.py generate_chronicle_summary 1 --output summary.txt

# Generate HTML report
python manage.py generate_chronicle_summary 1 --format html --output report.html

# Generate Markdown
python manage.py generate_chronicle_summary 1 --format markdown --output summary.md
```

**Includes**:
- Scene statistics
- Character participation rates
- XP statistics
- Player engagement metrics
- Top active characters

---

### cleanup_old_weeks

Clean up old Week objects to prevent unbounded growth.

**Usage**:
```bash
# Delete weeks older than 6 months
python manage.py cleanup_old_weeks

# Custom threshold
python manage.py cleanup_old_weeks --months 12

# Keep weeks with pending XP requests
python manage.py cleanup_old_weeks --keep-with-pending

# Dry run
python manage.py cleanup_old_weeks --dry-run
```

---

### audit_user_permissions

Audit user permissions and ST relationships.

**Usage**:
```bash
# Basic audit
python manage.py audit_user_permissions

# Include profile data check
python manage.py audit_user_permissions --check-profiles

# Export to CSV
python manage.py audit_user_permissions --export user_audit.csv
```

**Reports on**:
- ST relationships by chronicle
- STs with no active chronicles
- Profile data completeness (lines/veils/discord)

---

### generate_st_report

Generate dashboard-style report for Storytellers.

**Usage**:
```bash
# Report for all chronicles
python manage.py generate_st_report

# Report for specific ST
python manage.py generate_st_report --st-username username

# Report for specific chronicle
python manage.py generate_st_report --chronicle 1

# Save to file
python manage.py generate_st_report --output st_report.txt
```

**Shows**:
- Pending approvals count
- Active scenes
- Recent XP requests
- Character status breakdown

---

## Development & Testing

### reset_demo_data

Reset database to demo/test state. **WARNING: Deletes existing data!**

**Usage**:
```bash
# Reset with confirmation
python manage.py reset_demo_data --confirm

# Preserve user accounts
python manage.py reset_demo_data --confirm --preserve-users
```

**Creates**:
- Demo ST user (demo_st / demo123)
- Demo player user (demo_player / demo123)
- Demo chronicle

---

### populate_test_chronicle

Populate a test chronicle with realistic data.

**Usage**:
```bash
# Populate with defaults (10 characters, 15 scenes)
python manage.py populate_test_chronicle --chronicle 1

# Custom amounts
python manage.py populate_test_chronicle --chronicle 1 --characters 20 --scenes 30

# Specify gameline
python manage.py populate_test_chronicle --chronicle 1 --gameline mta
```

**Creates**:
- Test characters with various statuses
- Test scenes with participants
- Test user (test_player / test123)

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

# 3. Clean orphaned data
python manage.py cleanup_orphaned_data --include-scenes --include-setting-elements

# 4. Sync character statuses
python manage.py sync_character_status

# 5. Clean old weeks
python manage.py cleanup_old_weeks --months 6

# 6. Validate remaining data
python manage.py validate_character_data
```

### Chronicle Backup
```bash
# Export chronicle with all data
python manage.py export_chronicle CHRONICLE_ID --pretty --include-users --output backup_$(date +%Y%m%d).json
```

### Storyteller Workflow
```bash
# 1. Generate ST dashboard
python manage.py generate_st_report --st-username YOUR_USERNAME

# 2. Review pending approvals
python manage.py approve_pending_items --list-only

# 3. Approve characters
python manage.py approve_pending_items --type characters --chronicle YOUR_CHRONICLE_ID

# 4. Approve XP requests
python manage.py approve_pending_items --type xp-requests

# 5. Generate chronicle summary
python manage.py generate_chronicle_summary YOUR_CHRONICLE_ID --format html --output summary.html
```

### Monthly Maintenance
```bash
# 1. Archive inactive chronicles
python manage.py archive_inactive_chronicles --days 90 --list-only

# 2. Clean orphaned data
python manage.py cleanup_orphaned_data --days 60

# 3. Audit users
python manage.py audit_user_permissions --check-profiles --export user_audit.csv

# 4. Clean old weeks
python manage.py cleanup_old_weeks --months 6 --keep-with-pending
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

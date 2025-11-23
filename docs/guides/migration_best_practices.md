# Django Migration Best Practices

## Overview

This guide outlines best practices for managing Django migrations in the WoD Character Manager project. Following these practices ensures database changes are safe, reversible, and maintainable across development, staging, and production environments.

## Core Principles

1. **Never edit applied migrations** - Once a migration has been applied to production, it should never be modified
2. **Test migrations before deployment** - Always test both forward and reverse migrations
3. **Keep migrations small and focused** - One logical change per migration when possible
4. **Document complex migrations** - Add comments explaining non-obvious data transformations
5. **Maintain backward compatibility** - Plan multi-step migrations for breaking changes

## Data Migrations for Schema Changes

### When to Use Data Migrations

Create data migrations when you need to:
- Transform existing data during schema changes
- Populate new fields with calculated values
- Migrate data between models (e.g., JSONField to related models)
- Clean up or normalize existing data
- Set up initial data for new features

### Creating Data Migrations

**Generate an empty data migration:**
```bash
python manage.py makemigrations --empty --name migrate_data_description app_name
```

**Example: Adding a new required field with default data**

When adding a non-nullable field to a model with existing data, use a three-step process:

```python
# Step 1: Add field as nullable
class Migration(migrations.Migration):
    dependencies = [('characters', '0042_previous_migration')]

    operations = [
        migrations.AddField(
            model_name='character',
            name='generation',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
```

```python
# Step 2: Populate the field with data
def populate_generation(apps, schema_editor):
    """Set default generation based on character type."""
    Character = apps.get_model('characters', 'Character')

    # Use apps.get_model() to get historical model version
    for char in Character.objects.filter(character_type='vampire'):
        if char.generation is None:
            char.generation = 13  # Default for new vampires
            char.save(update_fields=['generation'])

def reverse_populate(apps, schema_editor):
    """Clear generation data for rollback."""
    Character = apps.get_model('characters', 'Character')
    Character.objects.update(generation=None)

class Migration(migrations.Migration):
    dependencies = [('characters', '0043_add_generation_nullable')]

    operations = [
        migrations.RunPython(
            populate_generation,
            reverse_populate,
        ),
    ]
```

```python
# Step 3: Make field non-nullable
class Migration(migrations.Migration):
    dependencies = [('characters', '0044_populate_generation')]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='generation',
            field=models.IntegerField(default=13),
        ),
    ]
```

### Data Migration Best Practices

**1. Use historical models from apps registry:**
```python
def migrate_data(apps, schema_editor):
    # CORRECT - uses historical model state
    Character = apps.get_model('characters', 'Character')

    # INCORRECT - uses current model which may have different fields
    from characters.models import Character  # Don't do this!
```

**2. Handle large datasets efficiently:**
```python
def migrate_large_dataset(apps, schema_editor):
    Character = apps.get_model('characters', 'Character')

    # Use iterator() to prevent loading all objects into memory
    for char in Character.objects.iterator(chunk_size=1000):
        char.new_field = calculate_value(char)
        char.save(update_fields=['new_field'])

    # Or use bulk operations when possible
    updates = []
    for char in Character.objects.iterator(chunk_size=1000):
        char.new_field = calculate_value(char)
        updates.append(char)

        if len(updates) >= 1000:
            Character.objects.bulk_update(updates, ['new_field'])
            updates = []

    if updates:
        Character.objects.bulk_update(updates, ['new_field'])
```

**3. Always provide reverse migrations:**
```python
def forward_migration(apps, schema_editor):
    """Transform data."""
    pass

def reverse_migration(apps, schema_editor):
    """Undo the transformation."""
    pass

operations = [
    migrations.RunPython(
        forward_migration,
        reverse_migration,  # Always provide reverse
    ),
]
```

**4. Add helpful comments and documentation:**
```python
def migrate_xp_to_models(apps, schema_editor):
    """
    Migrate XP tracking from JSONField to XPSpendingRequest model.

    This migration:
    - Reads spent_xp JSONField data
    - Creates XPSpendingRequest instances for each record
    - Preserves approval status and timestamps
    - Skips records that have already been migrated

    See docs/guides/jsonfield_migration.md for details.
    """
    Character = apps.get_model('characters', 'Character')
    XPSpendingRequest = apps.get_model('game', 'XPSpendingRequest')

    # Migration logic...
```

**5. Make migrations idempotent:**
```python
def migrate_data(apps, schema_editor):
    """Migration that can safely run multiple times."""
    Model = apps.get_model('app', 'Model')

    # Check if data already exists before creating
    if not Model.objects.filter(special_flag=True).exists():
        # Perform migration
        pass
```

## Migration Squashing

### Why Squash Migrations?

Over time, apps accumulate many migrations. Squashing provides:
- **Faster initial migrations** on new databases
- **Reduced complexity** when reviewing migration history
- **Smaller codebase** with fewer migration files
- **Easier debugging** with consolidated migration logic

### When to Squash

Squash migrations when:
- An app has 50+ migrations
- Migrations are all applied to production
- You're starting a new development cycle
- Old migrations contain outdated data transformations

**DO NOT** squash migrations that:
- Haven't been applied to all environments
- Are less than 6 months old
- Contain complex data migrations you may need to reference

### Squashing Process

**1. Identify the range to squash:**
```bash
# List all migrations for an app
python manage.py showmigrations characters

# Example output:
# characters
#  [X] 0001_initial
#  [X] 0002_add_attributes
#  ...
#  [X] 0050_final_old_migration
#  [ ] 0051_recent_migration
```

**2. Create the squashed migration:**
```bash
# Squash migrations 0001 through 0050
python manage.py squashmigrations characters 0001 0050

# Django creates: 0001_squashed_0050_auto_date.py
```

**3. Test the squashed migration:**
```bash
# On a fresh database (development)
python manage.py migrate characters 0001_squashed_0050_auto_date

# Verify all models are created correctly
python manage.py check

# Run tests
python manage.py test characters
```

**4. Deploy to production:**

The squashed migration is marked with `replaces = [...]` so Django knows it replaces the old migrations:

```python
class Migration(migrations.Migration):
    replaces = [
        ('characters', '0001_initial'),
        ('characters', '0002_add_attributes'),
        # ... all replaced migrations
        ('characters', '0050_final_old_migration'),
    ]
```

This allows:
- Existing databases to skip the squashed migration (they have the originals)
- New databases to use the squashed version

**5. Remove old migrations (after verification):**

After the squashed migration is in production for several weeks:

```bash
# Remove the old individual migration files
rm characters/migrations/0001_initial.py
rm characters/migrations/0002_add_attributes.py
# ... through 0050

# Remove the replaces attribute from squashed migration
# Edit 0001_squashed_0050_auto_date.py and remove:
#   replaces = [...]
```

### Squashing Best Practices

1. **Squash per app** - Don't squash across multiple apps
2. **Keep recent migrations** - Only squash migrations older than 6 months
3. **Document squashing** - Note in commit message what range was squashed
4. **Test thoroughly** - Verify on fresh database before deployment
5. **Keep data migration logic** - If squashing removes important data migration code, document it separately

### Example Squashing Schedule

For this project, consider squashing:
- **Annually** for core apps (characters, items, locations)
- **When exceeding 50 migrations** per app
- **Before major releases** to clean up development migrations

## Testing Migrations in CI/CD

### Why Test Migrations?

Migration tests catch:
- Migrations that fail on production-like data
- Missing reverse migrations
- Performance issues with large datasets
- Incompatible database changes
- Data loss during transformations

### Setting Up Migration Tests

**1. Add migration tests to your test suite:**

Create `characters/tests/test_migrations.py`:

```python
from django.test import TransactionTestCase
from django.core.management import call_command


class MigrationTestCase(TransactionTestCase):
    """Test migrations can be applied and reversed."""

    # Use TransactionTestCase for migration tests
    # (TestCase uses transactions which conflict with migrations)

    migrate_from = None
    migrate_to = None
    app_name = 'characters'

    def setUp(self):
        """Migrate to the starting point."""
        if self.migrate_from:
            call_command('migrate', self.app_name, self.migrate_from)
        super().setUp()

    def migrate(self, target):
        """Helper to run migrations."""
        call_command('migrate', self.app_name, target)

    def test_migration_forward_backward(self):
        """Test migration can be applied and reversed."""
        if not self.migrate_to or not self.migrate_from:
            self.skipTest("Migration range not specified")

        # Apply the migration forward
        self.migrate(self.migrate_to)

        # Reverse the migration
        self.migrate(self.migrate_from)


class TestGenerationMigration(MigrationTestCase):
    """Test the generation field migration."""

    migrate_from = '0042_before_generation'
    migrate_to = '0045_generation_complete'

    def test_generation_populated(self):
        """Test that generation field is populated correctly."""
        # Start at beginning state
        self.migrate(self.migrate_from)

        # Create test data in old state
        Character = self.apps.get_model('characters', 'Character')
        char = Character.objects.create(
            name='Test Vampire',
            character_type='vampire'
        )

        # Apply migration
        self.migrate(self.migrate_to)

        # Verify data transformed correctly
        char.refresh_from_db()
        self.assertEqual(char.generation, 13)

    def test_reverse_migration_safe(self):
        """Test reversing migration doesn't lose critical data."""
        self.migrate(self.migrate_to)

        Character = self.apps.get_model('characters', 'Character')
        char = Character.objects.create(
            name='Test Vampire',
            character_type='vampire',
            generation=10
        )

        # Reverse migration
        self.migrate(self.migrate_from)

        # Verify character still exists (generation field removed but data safe)
        char.refresh_from_db()
        self.assertEqual(char.name, 'Test Vampire')
```

**2. Add migration checks to CI/CD pipeline:**

Create `.github/workflows/migrations.yml`:

```yaml
name: Migration Tests

on:
  pull_request:
    paths:
      - '**/migrations/**'
      - '**/models.py'

jobs:
  test-migrations:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Check for migration conflicts
        run: |
          python manage.py makemigrations --check --dry-run

      - name: Test migrations forward
        run: |
          python manage.py migrate

      - name: Test migrations backward (last 3)
        run: |
          # Get current migration for each app
          # Migrate back 3 steps
          # Migrate forward again
          python manage.py migrate characters 0000
          python manage.py migrate characters

      - name: Run migration tests
        run: |
          python manage.py test --pattern="test_migrations.py"
```

**3. Add migration checks to pre-commit hooks:**

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Check for migration conflicts
python manage.py makemigrations --check --dry-run
if [ $? -ne 0 ]; then
    echo "❌ Migration conflicts detected. Run makemigrations first."
    exit 1
fi

echo "✅ No migration conflicts"
```

### Manual Migration Testing Checklist

Before deploying migrations to production:

- [ ] Migrations apply cleanly on fresh database
- [ ] Migrations apply cleanly on copy of production database
- [ ] Reverse migrations work without data loss
- [ ] No migrations are missing (makemigrations shows no changes)
- [ ] Data transformations preserve all important information
- [ ] Large tables migrate in reasonable time
- [ ] Related models maintain referential integrity
- [ ] Tests pass before and after migration

### Performance Testing Large Migrations

For migrations affecting tables with millions of rows:

```python
# Test migration performance on production-size dataset
def test_migration_performance(apps, schema_editor):
    """
    Performance test: Should complete in under 5 minutes for 1M rows.
    """
    import time
    start = time.time()

    # Run migration
    migrate_data(apps, schema_editor)

    elapsed = time.time() - start
    print(f"Migration completed in {elapsed:.2f} seconds")

    # Log to monitoring system
    if elapsed > 300:  # 5 minutes
        logger.warning(f"Slow migration: {elapsed}s for {Model.objects.count()} rows")
```

## Common Migration Patterns

### Pattern: Renaming a Field

**Preferred approach (preserves data):**

```python
# Step 1: Add new field
operations = [
    migrations.AddField('Model', 'new_name', field=...),
]

# Step 2: Copy data
operations = [
    migrations.RunPython(
        lambda apps, schema_editor: (
            apps.get_model('app', 'Model')
            .objects.update(new_name=F('old_name'))
        )
    ),
]

# Step 3: Remove old field
operations = [
    migrations.RemoveField('Model', 'old_name'),
]
```

**Django's rename operation (risky):**
```python
# Only safe if no code references the old field name
operations = [
    migrations.RenameField('Model', 'old_name', 'new_name'),
]
```

### Pattern: Changing Field Type

```python
# Step 1: Add new field with new type
operations = [
    migrations.AddField('Model', 'field_new', new_field_type),
]

# Step 2: Transform and copy data
def transform_data(apps, schema_editor):
    Model = apps.get_model('app', 'Model')
    for obj in Model.objects.iterator():
        obj.field_new = transform(obj.field_old)
        obj.save(update_fields=['field_new'])

operations = [
    migrations.RunPython(transform_data),
]

# Step 3: Remove old field
operations = [
    migrations.RemoveField('Model', 'field_old'),
]

# Step 4: Rename new field to original name
operations = [
    migrations.RenameField('Model', 'field_new', 'field_old'),
]
```

### Pattern: Splitting a Model

```python
def split_model(apps, schema_editor):
    """Split OldModel into Model and RelatedModel."""
    OldModel = apps.get_model('app', 'OldModel')
    Model = apps.get_model('app', 'Model')
    RelatedModel = apps.get_model('app', 'RelatedModel')

    for old in OldModel.objects.iterator():
        # Create main model
        new = Model.objects.create(
            name=old.name,
            # ... copy relevant fields
        )

        # Create related model
        related = RelatedModel.objects.create(
            model=new,
            # ... copy other fields
        )

operations = [
    # Create new models
    migrations.CreateModel('Model', ...),
    migrations.CreateModel('RelatedModel', ...),

    # Migrate data
    migrations.RunPython(split_model),

    # Remove old model
    migrations.DeleteModel('OldModel'),
]
```

## Troubleshooting

### Migration Conflicts

**Problem:** Multiple developers create migrations with the same number.

**Solution:**
```bash
# Django detects conflict
python manage.py makemigrations

# Output: "Conflicting migrations detected; multiple leaf nodes"
# Django creates a merge migration automatically
```

### Fake Migrations (Emergency Use Only)

**When to fake:** Production database is already in correct state but migrations are out of sync.

```bash
# Mark migration as applied without running it
python manage.py migrate app_name 0042_migration --fake

# Mark all migrations as applied
python manage.py migrate --fake
```

**⚠️ Warning:** Only use `--fake` when you're certain the database state matches the migration.

### Rolling Back a Bad Migration

```bash
# Rollback to previous migration
python manage.py migrate app_name 0041_previous_migration

# Fix the bad migration file
# Create new corrected migration
python manage.py makemigrations

# Apply the fix
python manage.py migrate
```

## Migration Checklist for This Project

Before creating a migration:
- [ ] Read related migration guides (jsonfield_migration.md, mage_migration.md, etc.)
- [ ] Check if change requires a multi-step migration for safety
- [ ] Plan data migration if schema change affects existing data
- [ ] Consider performance impact on large tables

Before committing:
- [ ] Migration name is descriptive
- [ ] Complex logic has comments explaining why
- [ ] Reverse migration is provided for RunPython operations
- [ ] Migration tested on development database

Before deploying:
- [ ] Tested on production database copy
- [ ] Verified migration performance on realistic dataset
- [ ] Documented in deployment guide if manual steps needed
- [ ] Notified team if migration requires downtime

## Additional Resources

- [Django Migrations Documentation](https://docs.djangoproject.com/en/5.1/topics/migrations/)
- [Project-specific migration guides](../guides/)
  - `jsonfield_migration.md` - Migrating JSONField to models
  - `mage_migration.md` - Mage-specific data migrations
  - `view_template_migration.md` - View refactoring during migrations
- [Deployment guides](../deployment/)
  - `permissions_deployment_guide.md` - Deploying permission changes
  - `VALIDATION_DEPLOYMENT_CHECKLIST.md` - Validation system deployment

## Summary

Good migration practices prevent data loss, reduce downtime, and make deployments safer:

1. **Use data migrations** for all schema changes affecting existing data
2. **Squash old migrations** annually to keep codebase maintainable
3. **Test migrations** in CI/CD and on production-like datasets
4. **Document complex migrations** so future developers understand the why
5. **Plan multi-step migrations** for breaking changes to maintain compatibility

Following these practices ensures the WoD Character Manager database evolves safely as the project grows.

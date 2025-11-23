# Validation System Staging Deployment Guide

This guide covers the deployment of the validation system (transaction protection and database constraints) to the staging environment.

## Overview

The validation system includes:
- **Database Constraints**: CheckConstraints for XP, attributes, abilities, willpower, and age
- **Transaction Protection**: @transaction.atomic for XP spending and scene XP awards
- **Model Validation**: clean() methods for status transitions and business logic
- **Row Locking**: select_for_update() to prevent race conditions

## Pre-Deployment Checklist

### 1. Review Implementation Status

Verify that all validation components are implemented:

- [x] **Character XP Constraints** (characters/models/core/character.py)
  - CheckConstraint: XP >= 0
  - clean(): Status transitions, XP balance
  - spend_xp(): Atomic transaction with select_for_update()
  - approve_xp_spend(): Atomic approval and trait increase

- [x] **Attribute Constraints** (characters/models/core/attribute_block.py)
  - CheckConstraint: All 9 attributes in range 1-10
  - MinValueValidator/MaxValueValidator on fields

- [x] **Ability Constraints** (characters/models/core/ability_block.py)
  - CheckConstraint: All abilities in range 0-10
  - MinValueValidator/MaxValueValidator on fields

- [x] **Willpower Constraints** (characters/models/core/human.py)
  - CheckConstraint: Willpower 1-10, temp willpower 0-10
  - CheckConstraint: temp_willpower <= willpower
  - clean(): Cross-field validation

- [x] **Age Constraints** (characters/models/core/human.py)
  - CheckConstraint: Age 0-500
  - CheckConstraint: Apparent age 0-200

- [x] **Scene XP Awards** (game/models.py)
  - award_xp(): Atomic transaction with select_for_update()
  - Idempotency check (xp_given flag)

- [x] **STRelationship Uniqueness** (game/models.py)
  - UniqueConstraint: (user, chronicle, gameline)

- [x] **Comprehensive Tests** (characters/tests/core/test_validation_constraints.py)
  - 89 test methods covering all constraints
  - Transaction atomicity tests
  - Concurrency prevention tests

### 2. Data Validation

Before deploying, validate that existing data won't violate constraints:

```bash
# Run data integrity check
python manage.py validate_data_integrity --verbose

# If issues found, fix them
python manage.py validate_data_integrity --fix

# Verify all issues resolved
python manage.py validate_data_integrity
```

Expected output:
```
======================================================================
Data Integrity Validation Report
======================================================================

1. Checking for negative XP...
   ✓ No characters with negative XP

2. Checking for invalid status values...
   ✓ All characters have valid status

3. Checking attribute ranges (1-10)...
   ✓ All attributes in valid range (1-10)

4. Checking ability ranges (0-10)...
   ✓ All abilities in valid range (0-10)

5. Checking willpower constraints...
   ✓ All willpower values valid

6. Checking age constraints...
   ✓ All age values valid

7. Checking for duplicate ST relationships...
   ✓ No duplicate ST relationships

8. Checking scene XP integrity...
   ℹ X scenes have XP awarded
   ℹ Y finished scenes awaiting XP

======================================================================
✓ No data integrity issues found!
Database is ready for validation constraints.
======================================================================
```

## Staging Deployment Steps

### Step 1: Backup Database

```bash
# Create backup before deployment
pg_dump your_database > backup_pre_validation_$(date +%Y%m%d_%H%M%S).sql

# Or if using Django's dumpdata
python manage.py dumpdata > backup_pre_validation_$(date +%Y%m%d_%H%M%S).json
```

### Step 2: Pull Latest Code

```bash
# On staging server
cd /path/to/tg
git fetch origin
git checkout claude/deploy-validation-staging-013V3YCrnPRoKSA3SJz5Tvnq
git pull origin claude/deploy-validation-staging-013V3YCrnPRoKSA3SJz5Tvnq
```

### Step 3: Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install any new dependencies (if requirements.txt changed)
pip install -r requirements.txt
```

### Step 4: Run Data Validation

```bash
# Validate existing data
python manage.py validate_data_integrity --verbose

# Fix any issues found
python manage.py validate_data_integrity --fix
```

### Step 5: Run Migrations

```bash
# Check which migrations will be applied
python manage.py showmigrations

# Apply migrations (this adds the constraints to the database)
python manage.py migrate

# Expected output:
# Running migrations:
#   Applying characters.XXXX_add_xp_constraints... OK
#   Applying characters.XXXX_add_attribute_constraints... OK
#   Applying characters.XXXX_add_ability_constraints... OK
#   Applying characters.XXXX_add_willpower_constraints... OK
#   Applying characters.XXXX_add_age_constraints... OK
#   Applying game.XXXX_add_st_relationship_constraint... OK
```

### Step 6: Verify Constraints

```bash
# Test that constraints are active by attempting to create invalid data
python manage.py shell

>>> from characters.models import Character, Human
>>> from django.db import IntegrityError

# Test XP constraint
>>> c = Character.objects.create(name="Test", xp=-1)
# Should raise: IntegrityError: CHECK constraint failed: characters_character_xp_non_negative

# Test attribute constraint
>>> h = Human.objects.create(name="Test", strength=0)
# Should raise: IntegrityError: CHECK constraint failed: characters_human_strength_range

# Test willpower constraint
>>> h = Human.objects.create(name="Test", willpower=5, temporary_willpower=6)
# Should raise: IntegrityError: CHECK constraint failed: characters_human_temp_not_exceeds_max
```

### Step 7: Run Test Suite

```bash
# Run all validation tests
pytest characters/tests/core/test_validation_constraints.py -v

# Run all tests to ensure nothing broke
pytest --tb=short

# Expected: All tests passing
```

### Step 8: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 9: Restart Application

```bash
# Restart gunicorn/uwsgi (example for systemd)
sudo systemctl restart tg-web

# Or if using supervisor
sudo supervisorctl restart tg

# Or if using Docker
docker-compose restart web
```

## Post-Deployment Verification

### 1. Health Check

```bash
# Test application is responding
curl -I http://staging.yoursite.com/

# Expected: HTTP 200 OK
```

### 2. Test XP Spending Workflow

1. **Login as a player**
   - Navigate to a character
   - Attempt to spend XP on a trait
   - Verify transaction succeeds

2. **Login as a storyteller**
   - Navigate to XP approval page
   - Approve an XP spend
   - Verify atomic approval (status + trait change)

3. **Test concurrent XP spending** (if possible)
   - Open two browser windows
   - Attempt to spend XP simultaneously
   - Verify one succeeds, one fails gracefully

### 3. Test Scene XP Awards

1. **Login as storyteller**
   - Navigate to a finished scene
   - Award XP to participants
   - Verify all characters receive XP atomically

2. **Test idempotency**
   - Attempt to award XP again to same scene
   - Verify error: "XP has already been awarded for this scene"

### 4. Test Constraint Violations

1. **Attempt to create invalid character** (via admin or API)
   - Set XP to -100
   - Expected: Error message about XP constraint

2. **Attempt to set invalid attribute**
   - Set Strength to 15
   - Expected: Error message about attribute range

3. **Attempt to exceed willpower**
   - Set temporary_willpower > willpower
   - Expected: Error message about willpower constraint

### 5. Monitor Logs

```bash
# Watch application logs for errors
tail -f /var/log/tg/application.log

# Look for:
# - IntegrityError exceptions (constraint violations)
# - ValidationError exceptions (model validation failures)
# - Transaction rollback messages
# - Performance issues (slow transactions)
```

## Monitoring and Alerts

### 1. Database Monitoring

Set up alerts for:
- **CheckConstraint violations**: Any IntegrityError with constraint name
- **Transaction rollbacks**: Monitor rollback rate
- **Deadlocks**: Monitor for row locking conflicts
- **Slow queries**: Transactions taking > 1 second

### 2. Application Monitoring

Monitor:
- **Error rate**: Should not increase after deployment
- **Response time**: XP operations should be < 200ms
- **XP spending success rate**: Should be > 95%
- **Scene XP award success rate**: Should be 100%

### 3. Log Aggregation

Set up structured logging for validation events:

```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/tg/validation.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/tg/validation_errors.log',
            'maxBytes': 10485760,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'characters.models': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
        },
        'game.models': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
        },
    },
}
```

### 4. Metrics to Track

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| **XP Spend Success Rate** | > 95% | < 90% |
| **XP Spend Response Time** | < 200ms | > 500ms |
| **Scene XP Award Success Rate** | 100% | < 99% |
| **Constraint Violations** | 0/day | > 10/day |
| **Transaction Rollbacks** | < 1% | > 5% |
| **Database Deadlocks** | 0/day | > 1/day |

## Rollback Plan

If critical issues are discovered:

### Emergency Rollback

```bash
# 1. Stop application
sudo systemctl stop tg-web

# 2. Restore database backup
psql your_database < backup_pre_validation_TIMESTAMP.sql

# 3. Revert code
git checkout previous_stable_branch
git pull

# 4. Run migrations (will remove constraints)
python manage.py migrate characters XXXX_migration_before_constraints
python manage.py migrate game XXXX_migration_before_constraints

# 5. Restart application
sudo systemctl start tg-web
```

### Graceful Rollback (Keep Transactions, Remove Constraints)

If transactions work but constraints cause issues:

```bash
# Create migration to remove constraints
python manage.py makemigrations --empty characters --name remove_validation_constraints

# Edit migration to remove constraints only
# Then apply
python manage.py migrate

# This keeps transaction protection but removes DB constraints
```

## Common Issues and Solutions

### Issue 1: Constraint Violation on Existing Data

**Symptom**: Migration fails with "CHECK constraint failed"

**Solution**:
```bash
# Run data fix script before migration
python manage.py validate_data_integrity --fix

# Then retry migration
python manage.py migrate
```

### Issue 2: Performance Degradation

**Symptom**: XP operations slow after deployment

**Cause**: Row locking causing waits

**Solution**:
- Check for long-running transactions
- Monitor for deadlocks
- Consider adding database indexes on frequently locked fields

### Issue 3: Deadlock Detected

**Symptom**: "deadlock detected" errors in logs

**Cause**: Multiple transactions trying to lock same resources

**Solution**:
- Ensure consistent lock ordering in code
- Consider shorter transaction scope
- Add retry logic for transient deadlocks

### Issue 4: Constraint Too Restrictive

**Symptom**: Valid operations being rejected

**Example**: Age constraint rejects 1000-year-old vampire

**Solution**:
```bash
# Create migration to relax constraint
python manage.py makemigrations --empty characters --name relax_age_constraint

# Edit migration to update constraint
# Apply migration
python manage.py migrate
```

## Success Criteria

Deployment is successful when:

- [✓] All migrations applied without errors
- [✓] All tests passing (89/89)
- [✓] Data integrity check shows 0 issues
- [✓] XP spending workflow works correctly
- [✓] Scene XP awards work correctly
- [✓] Constraint violations are caught and reported clearly
- [✓] No performance degradation (< 10% increase in response time)
- [✓] No increase in error rate
- [✓] Monitoring and alerts configured
- [✓] Team trained on new validation behavior

## Next Steps After Staging

1. **Monitor for 1 week** - Watch for any edge cases or issues
2. **Collect metrics** - Verify performance and error rates are acceptable
3. **User acceptance testing** - Have STs and players test all workflows
4. **Fix any issues** - Address edge cases discovered in staging
5. **Document lessons learned** - Update this guide with any new findings
6. **Prepare production deployment** - Create production deployment plan
7. **Schedule production window** - Coordinate with team for production deployment

## Production Deployment Readiness

Before deploying to production:

- [ ] All staging issues resolved
- [ ] No critical bugs in 1 week of staging
- [ ] Performance metrics meet targets
- [ ] User acceptance testing complete
- [ ] Team trained on new behavior
- [ ] Monitoring and alerts tested
- [ ] Rollback plan tested in staging
- [ ] Production backup verified
- [ ] Maintenance window scheduled
- [ ] Communication sent to users

## Contact and Support

For issues during deployment:

- **Development Team**: [contact info]
- **Database Admin**: [contact info]
- **DevOps**: [contact info]
- **On-Call**: [contact info]

## References

- [Data Validation Design](../design/data_validation.md) - Complete design document
- [Test Suite](../../characters/tests/core/test_validation_constraints.py) - Validation tests
- [Character Model](../../characters/models/core/character.py) - Implementation
- [Scene Model](../../game/models.py) - XP award implementation

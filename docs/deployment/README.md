# Deployment Documentation

This directory contains all documentation and tools for deploying major features to staging and production environments.

## Overview

The validation system adds comprehensive data integrity protection through:
- **Database Constraints**: Prevents invalid data at the database level
- **Transaction Protection**: Ensures atomic operations for XP spending and awards
- **Model Validation**: Enforces business rules and status transitions
- **Row Locking**: Prevents race conditions in concurrent operations

## Quick Start

### For Staging Deployment

```bash
# 1. Validate existing data
python manage.py validate_data_integrity --verbose

# 2. Fix any issues
python manage.py validate_data_integrity --fix

# 3. Run migrations
python manage.py migrate

# 4. Verify constraints
python manage.py validate_data_integrity

# 5. Monitor health
python manage.py monitor_validation
```

### For Production Deployment

Follow the complete checklist:
- [VALIDATION_DEPLOYMENT_CHECKLIST.md](VALIDATION_DEPLOYMENT_CHECKLIST.md)

## Documentation

### Permissions System Deployment

1. **[permissions_deployment_guide.md](permissions_deployment_guide.md)** - Comprehensive deployment guide
   - Prerequisites and system requirements
   - Development, staging, and production deployment
   - Testing procedures (automated and manual)
   - Rollback plans
   - Monitoring and troubleshooting

2. **[permissions_staging_checklist.md](permissions_staging_checklist.md)** - Quick reference checklist
   - Step-by-step deployment checklist
   - Manual testing scenarios
   - Sign-off procedures

3. **[permissions_deployment_summary.md](permissions_deployment_summary.md)** - Executive summary
   - Deployment status and readiness
   - Test results
   - Risk assessment

### Validation System Deployment

1. **[VALIDATION_STAGING_DEPLOYMENT.md](VALIDATION_STAGING_DEPLOYMENT.md)** - Comprehensive staging deployment guide
   - Pre-deployment checklist
   - Step-by-step deployment instructions
   - Post-deployment verification
   - Monitoring setup
   - Rollback procedures
   - Troubleshooting

2. **[VALIDATION_DEPLOYMENT_CHECKLIST.md](VALIDATION_DEPLOYMENT_CHECKLIST.md)** - Complete deployment checklist
   - Development tasks
   - Staging deployment tasks
   - Production deployment tasks
   - Sign-off procedures

### Design Documentation

- **[../design/data_validation.md](../design/data_validation.md)** - Complete validation system design
  - Implementation patterns
  - Code examples
  - Performance considerations
  - Testing strategies

## Management Commands

### validate_data_integrity

Pre-deployment data validation and fixing:

```bash
# Check for issues
python manage.py validate_data_integrity --verbose

# Automatically fix issues
python manage.py validate_data_integrity --fix

# Standard check
python manage.py validate_data_integrity
```

**Checks performed:**
- Characters with negative XP
- Characters with invalid status
- Attributes out of range (1-10)
- Abilities out of range (0-10)
- Willpower constraint violations
- Age constraint violations
- Duplicate ST relationships
- Scene XP integrity

### monitor_validation

Post-deployment health monitoring:

```bash
# Standard health report
python manage.py monitor_validation

# JSON output for monitoring tools
python manage.py monitor_validation --json

# Send alerts if issues detected
python manage.py monitor_validation --alert

# Analyze last 48 hours
python manage.py monitor_validation --period 48
```

**Metrics tracked:**
- Data integrity issues
- XP spending activity and approval rates
- Scene XP award patterns
- Character statistics
- Overall health score (0-100)

## Validation System Components

### Database Constraints

**Characters** (`characters/models/core/character.py`):
- XP >= 0
- Valid status values

**Attributes** (`characters/models/core/attribute_block.py`):
- All 9 attributes: 1-10 range
- MinValueValidator/MaxValueValidator

**Abilities** (`characters/models/core/ability_block.py`):
- All abilities: 0-10 range
- MinValueValidator/MaxValueValidator

**Willpower** (`characters/models/core/human.py`):
- Willpower: 1-10 range
- Temporary willpower: 0-10 range
- Temporary <= Permanent

**Age** (`characters/models/core/human.py`):
- Age: 0-500
- Apparent age: 0-200

**STRelationship** (`game/models.py`):
- Unique (user, chronicle, gameline)

### Transaction Protection

**Character XP** (`characters/models/core/character.py`):
```python
@transaction.atomic
def spend_xp(self, trait_name, trait_display, cost, category):
    """Atomically spend XP and record transaction."""
    char = Character.objects.select_for_update().get(pk=self.pk)
    # ... atomic operations ...

@transaction.atomic
def approve_xp_spend(self, spend_index, trait_property_name, new_value):
    """Atomically approve XP and apply trait increase."""
    char = Character.objects.select_for_update().get(pk=self.pk)
    # ... atomic operations ...
```

**Scene XP Awards** (`game/models.py`):
```python
@transaction.atomic
def award_xp(self, character_awards):
    """Atomically award XP to all scene participants."""
    scene = Scene.objects.select_for_update().get(pk=self.pk)
    # ... atomic operations ...
```

### Model Validation

**Character** (`characters/models/core/character.py`):
```python
def clean(self):
    """Validate status transitions and business rules."""
    # Status transition state machine
    # XP balance validation
    # Cross-field validation
```

## Test Suite

**Location**: `characters/tests/core/test_validation_constraints.py`

**Coverage**: 89 test methods covering:
- Database constraint violations
- Transaction atomicity
- Model validation
- Status transitions
- Concurrent access prevention
- Integration tests

**Run tests:**
```bash
# All validation tests
python manage.py test characters.tests.core.test_validation_constraints --verbosity=2

# Specific test class
python manage.py test characters.tests.core.test_validation_constraints.TestXPTransactions

# All tests
python manage.py test
```

## Deployment Timeline

### Phase 1: Staging (Week 1)

1. **Day 1**: Deploy to staging
   - Run data validation
   - Apply migrations
   - Verify constraints

2. **Days 2-7**: Monitor and test
   - Daily health checks
   - User acceptance testing
   - Performance monitoring
   - Bug fixes

### Phase 2: Production (Week 2)

1. **Pre-deployment**:
   - Staging sign-off
   - Schedule maintenance window
   - Prepare rollback plan
   - Backup database

2. **Deployment**:
   - Apply migrations
   - Verify constraints
   - Health checks

3. **Post-deployment**:
   - 24-hour active monitoring
   - 1-week soak period
   - Metrics collection

## Success Criteria

### Staging

- [✓] All migrations applied without errors
- [✓] All tests passing (89/89)
- [✓] Data integrity check shows 0 issues
- [ ] XP workflows tested and working
- [ ] Scene XP awards tested and working
- [ ] Constraint violations handled gracefully
- [ ] No performance degradation
- [ ] No increase in error rate

### Production

- [ ] 1 week in staging with no critical issues
- [ ] All staging success criteria met
- [ ] User acceptance testing complete
- [ ] Team training complete
- [ ] Monitoring and alerts configured
- [ ] Rollback plan tested

## Monitoring and Alerts

### Metrics to Monitor

| Metric | Target | Alert Threshold | Action |
|--------|--------|-----------------|--------|
| Health Score | 100 | < 90 | Investigate |
| XP Spend Success | > 95% | < 90% | Review errors |
| XP Spend Time | < 200ms | > 500ms | Performance review |
| Scene XP Award Success | 100% | < 99% | Immediate fix |
| Constraint Violations | 0/day | > 10/day | Data audit |
| Transaction Rollbacks | < 1% | > 5% | Code review |
| Database Deadlocks | 0/day | > 1/day | Lock analysis |

### Monitoring Setup

**Cron job** (run hourly):
```bash
0 * * * * cd /path/to/tg && python manage.py monitor_validation --json >> /var/log/tg/validation.log
```

**Daily report** (run at 9am):
```bash
0 9 * * * cd /path/to/tg && python manage.py monitor_validation --alert --period 24
```

**Continuous monitoring**:
- Integrate with application monitoring (New Relic, Datadog, etc.)
- Set up database query monitoring
- Configure error tracking (Sentry, Rollbar, etc.)

## Rollback Procedures

### Emergency Rollback

If critical issues occur:

```bash
# 1. Stop application
sudo systemctl stop tg-web

# 2. Restore database
psql db_name < backup_TIMESTAMP.sql

# 3. Revert code
git checkout PREVIOUS_STABLE_TAG
python manage.py migrate characters XXXX
python manage.py migrate game XXXX

# 4. Restart
sudo systemctl start tg-web
```

### Partial Rollback

If constraints too restrictive but transactions work:

```bash
# Remove constraints, keep transactions
python manage.py makemigrations --empty characters --name remove_constraints
# Edit migration to remove CheckConstraints
python manage.py migrate
```

## Troubleshooting

### Common Issues

**Issue**: Migration fails with "CHECK constraint failed"
**Solution**:
```bash
python manage.py validate_data_integrity --fix
python manage.py migrate
```

**Issue**: Performance degradation
**Solution**:
- Check for long-running transactions
- Monitor for deadlocks
- Review database indexes
- Consider transaction scope reduction

**Issue**: Constraint too restrictive
**Solution**:
- Review constraint definition
- Check for edge cases
- Consider relaxing constraint
- Create migration to update constraint

### Getting Help

- Review [data_validation.md](../design/data_validation.md) for design details
- Check test suite for expected behavior
- Run `python manage.py monitor_validation --verbose` for detailed status
- Review application logs for specific errors

## References

### Documentation
- [Data Validation Design](../design/data_validation.md) - Complete design document
- [Staging Deployment Guide](VALIDATION_STAGING_DEPLOYMENT.md) - Step-by-step guide
- [Deployment Checklist](VALIDATION_DEPLOYMENT_CHECKLIST.md) - Complete checklist

### Code
- [Character Model](../../characters/models/core/character.py) - XP transactions
- [Attribute Block](../../characters/models/core/attribute_block.py) - Attribute constraints
- [Ability Block](../../characters/models/core/ability_block.py) - Ability constraints
- [Human Model](../../characters/models/core/human.py) - Willpower/age constraints
- [Scene Model](../../game/models.py) - Scene XP awards
- [Test Suite](../../characters/tests/core/test_validation_constraints.py) - Validation tests

### Tools
- [validate_data_integrity.py](../../core/management/commands/validate_data_integrity.py) - Data validation
- [monitor_validation.py](../../core/management/commands/monitor_validation.py) - Health monitoring

## Next Steps

1. **Review this documentation** - Ensure understanding of all components
2. **Run tests locally** - Verify all tests pass
3. **Test migrations locally** - Apply migrations to dev database
4. **Schedule staging deployment** - Coordinate with team
5. **Follow staging deployment guide** - Execute deployment
6. **Monitor for 1 week** - Collect metrics and feedback
7. **Schedule production deployment** - After staging sign-off

## Redis Cache Setup

Production caching is configured in `tg/settings/production.py` using Redis.

### Requirements

```bash
pip install django-redis redis
```

### Configuration

Set the `REDIS_URL` environment variable:

```bash
# Local Redis
export REDIS_URL="redis://127.0.0.1:6379/1"

# Redis with authentication
export REDIS_URL="redis://:password@hostname:6379/1"

# Redis Sentinel
export REDIS_URL="redis://sentinel-host:26379/mymaster/1"
```

### Features Enabled

- **View caching**: Use `@cache_page(60 * 15)` on expensive views
- **Session storage**: Sessions stored in Redis for horizontal scaling
- **Connection pooling**: Up to 50 connections with retry on timeout
- **Compression**: ZLib compression for cache values
- **Graceful degradation**: `IGNORE_EXCEPTIONS=True` prevents crashes if Redis is down

### Verification

```bash
# Test Redis connection
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'value', 60)
>>> cache.get('test')
'value'
```

---

## Contact

For questions or issues during deployment:
- Development Team: [contact info]
- Database Admin: [contact info]
- DevOps: [contact info]
- On-Call: [contact info]

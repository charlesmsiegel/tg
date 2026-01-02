# Validation System Staging Deployment Guide

This guide provides detailed instructions for deploying the validation system to the staging environment.

## Purpose

The staging deployment validates that:
1. Data integrity commands work correctly with production-like data
2. Database constraints don't break existing functionality
3. XP workflows continue to operate normally
4. Performance impact is acceptable (< 10% degradation)

## Prerequisites

### System Requirements
- Staging server with PostgreSQL 13+
- Python 3.10+ with Django 5.1.7
- Redis for caching (optional but recommended)
- Minimum 2GB RAM, 10GB disk space

### Access Requirements
- SSH access to staging server
- Database admin privileges
- Git repository access

## Deployment Steps

### Phase 1: Preparation (Day 1)

#### 1.1 Notify Team
Send notification to development team about upcoming deployment:
- Deployment date/time
- Expected duration (1-2 hours)
- Services affected

#### 1.2 Verify Current State
```bash
# Connect to staging server
ssh staging-server

# Check current branch and commits
cd /var/www/tg
git log --oneline -5
git status

# Verify services running
sudo systemctl status gunicorn nginx postgresql redis
```

#### 1.3 Create Backup
```bash
# Create timestamped backup
pg_dump -Fc staging_db > /backups/staging_pre_validation_$(date +%Y%m%d_%H%M%S).dump

# Verify backup integrity
pg_restore --list /backups/staging_pre_validation_*.dump | head -30
```

### Phase 2: Initial Validation (Day 1)

#### 2.1 Run Data Integrity Check
```bash
# Activate virtual environment
source /var/www/tg/venv/bin/activate

# Run validation in report-only mode
python manage.py validate_data_integrity --verbose

# Save results
python manage.py validate_data_integrity --verbose > /var/log/tg/validation_initial.log 2>&1
```

#### 2.2 Analyze Results
Review the validation report for:
- Negative XP values
- Invalid status values
- Attribute/ability range violations
- Willpower constraint violations
- Duplicate ST relationships

#### 2.3 Fix Issues (if needed)
```bash
# Run with --fix flag to auto-correct issues
python manage.py validate_data_integrity --fix --verbose

# Verify fixes applied
python manage.py validate_data_integrity
```

### Phase 3: Migration Deployment (Day 1)

#### 3.1 Check Pending Migrations
```bash
# List all migrations
python manage.py showmigrations

# Check for unapplied migrations
python manage.py showmigrations | grep "\[ \]"
```

#### 3.2 Apply Migrations
```bash
# Apply all pending migrations
python manage.py migrate

# Verify migrations applied
python manage.py showmigrations | grep -E "^\[X\]"
```

#### 3.3 Post-Migration Validation
```bash
# Run full validation suite
python manage.py validate_data_integrity
python manage.py validate_character_data

# Generate health report
python manage.py monitor_validation --json > /var/log/tg/health_post_migration.json
```

### Phase 4: Functional Testing (Days 1-2)

#### 4.1 Core Functionality Tests
Test the following workflows manually:

**Character Management**
- [ ] Create new character
- [ ] Edit existing character attributes
- [ ] Change character status (Un -> Sub -> App)
- [ ] Delete character

**XP System**
- [ ] Award XP to character
- [ ] Create XP spending request
- [ ] Approve XP spending request
- [ ] Deny XP spending request
- [ ] Verify XP totals calculate correctly

**Scene Management**
- [ ] Create new scene
- [ ] Add characters to scene
- [ ] Mark scene as finished
- [ ] Award scene XP

#### 4.2 Edge Case Testing
- [ ] Character with maximum XP (9999)
- [ ] Attribute at boundary (1 and 10)
- [ ] Ability at boundary (0 and 10)
- [ ] Willpower at maximum temporary value

### Phase 5: Monitoring Period (Days 2-8)

#### 5.1 Daily Monitoring Script
Create a cron job for daily monitoring:
```bash
# Add to crontab
0 8 * * * /var/www/tg/venv/bin/python /var/www/tg/manage.py monitor_validation --json >> /var/log/tg/daily_validation.log 2>&1
```

#### 5.2 Daily Review Checklist
- [ ] Check `/var/log/tg/daily_validation.log` for health score
- [ ] Review application error logs for constraint violations
- [ ] Verify no user-reported issues related to data entry
- [ ] Check database query performance metrics

#### 5.3 Sample Monitoring Commands
```bash
# Daily health check
python manage.py monitor_validation --period 24

# Generate detailed report
python manage.py monitor_validation --period 24 --json | jq '.checks.data_integrity'

# Check specific issues
python manage.py validate_data_integrity --verbose | grep -E "✗|⚠"
```

### Phase 6: Performance Assessment (Day 7-8)

#### 6.1 Measure Response Times
```bash
# Run performance test on key endpoints
ab -n 100 -c 10 https://staging.example.com/characters/
ab -n 100 -c 10 https://staging.example.com/xp/spend/
```

#### 6.2 Database Query Analysis
```bash
# Check for slow queries (if query logging enabled)
grep "duration:" /var/log/postgresql/postgresql-*.log | sort -t: -k2 -rn | head -20
```

#### 6.3 Performance Criteria
- Page load times within 10% of baseline
- No new slow queries (> 500ms)
- No memory leaks observed
- CPU utilization stable

## Troubleshooting

### Common Issues

#### Issue: Validation command hangs
```bash
# Check database connections
psql -c "SELECT count(*) FROM pg_stat_activity WHERE datname = 'staging_db';"

# Restart if needed
sudo systemctl restart postgresql
```

#### Issue: Constraint violation errors
```bash
# Identify violating records
python manage.py validate_data_integrity --verbose

# Fix specific issues
python manage.py shell
>>> from characters.models.core.human import Human
>>> Human.objects.filter(xp__lt=0).update(xp=0)
```

#### Issue: Performance degradation
```bash
# Check database indexes
python manage.py dbshell
\di  -- List all indexes

# Analyze slow queries
EXPLAIN ANALYZE SELECT * FROM characters_character WHERE xp < 0;
```

### Rollback Procedure

If critical issues are found:

```bash
# 1. Revert migrations
python manage.py migrate <app> <previous_migration_number>

# 2. Restore database backup
pg_restore -Fc -d staging_db /backups/staging_pre_validation_*.dump

# 3. Restart services
sudo systemctl restart gunicorn
```

## Sign-off Checklist

Before proceeding to production deployment, confirm:

### Technical Requirements
- [ ] All validation checks pass
- [ ] Health score >= 90 maintained for 7 days
- [ ] No constraint violations in logs
- [ ] Performance within acceptable range

### Functional Requirements
- [ ] All XP workflows tested and working
- [ ] Character creation/editing functional
- [ ] Status transitions work correctly
- [ ] No user-reported issues

### Documentation
- [ ] Deployment steps documented
- [ ] Issues encountered and resolutions noted
- [ ] Performance baseline established

### Approvals
- [ ] Technical Lead sign-off
- [ ] QA sign-off
- [ ] Product Owner sign-off

## Next Steps

After successful staging validation:
1. Schedule production deployment window
2. Notify all users of upcoming maintenance
3. Review production-specific concerns
4. Prepare production rollback plan

See [VALIDATION_DEPLOYMENT_CHECKLIST.md](VALIDATION_DEPLOYMENT_CHECKLIST.md) for production deployment steps.

# Validation System Deployment Checklist

This checklist covers all steps required to deploy the validation system to staging and production environments.

## Overview

The validation system provides:
- Data integrity checks via `validate_data_integrity` command
- Health monitoring via `monitor_validation` command
- Character data validation via `validate_character_data` command

## Pre-Deployment Requirements

### Environment Readiness
- [ ] PostgreSQL database running and accessible
- [ ] Redis cache configured (for performance monitoring)
- [ ] Sufficient disk space for database backups
- [ ] Team notified of deployment schedule

### Code Readiness
- [ ] All validation tests passing
- [ ] No pending migrations affecting core models
- [ ] Management commands available:
  - `validate_data_integrity`
  - `monitor_validation`
  - `validate_character_data`

## Staging Deployment

### Step 1: Backup and Validate Existing Data
```bash
# Create database backup
pg_dump staging_db > backup_staging_$(date +%Y%m%d_%H%M%S).sql

# Run validation check (report only)
python manage.py validate_data_integrity --verbose

# Review results before proceeding
```

### Step 2: Fix Data Issues (if any)
```bash
# Automatically fix issues where safe
python manage.py validate_data_integrity --fix

# Re-run validation to confirm fixes
python manage.py validate_data_integrity
```

### Step 3: Apply Migrations
```bash
# Check pending migrations
python manage.py showmigrations

# Apply migrations
python manage.py migrate
```

### Step 4: Verify Constraints
```bash
# Run full validation suite
python manage.py validate_data_integrity
python manage.py validate_character_data

# Check system health
python manage.py monitor_validation
```

### Step 5: Functional Testing
- [ ] XP spending workflow works correctly
- [ ] Character creation validates properly
- [ ] Status transitions work as expected
- [ ] ST approval workflows function

## Production Deployment

### Pre-Production Checklist
- [ ] Staging validation passed
- [ ] 1-week monitoring in staging completed
- [ ] No constraint violations observed
- [ ] Performance degradation < 10%
- [ ] Rollback plan documented and tested

### Step 1: Schedule Maintenance Window
- Notify users 48 hours in advance
- Schedule 2-hour window minimum
- Have rollback script ready

### Step 2: Production Backup
```bash
# Create full database backup
pg_dump production_db > backup_production_$(date +%Y%m%d_%H%M%S).sql

# Verify backup
pg_restore --list backup_production_*.sql | head -20
```

### Step 3: Enable Maintenance Mode
```bash
touch /var/www/tg/maintenance.flag
```

### Step 4: Deploy and Validate
```bash
# Pull latest code
git fetch origin && git checkout main && git pull

# Install dependencies
pip install -r requirements.txt

# Run validation (should show no issues after staging work)
python manage.py validate_data_integrity

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Step 5: Post-Deployment Verification
```bash
# Remove maintenance mode
rm /var/www/tg/maintenance.flag

# Check health
python manage.py monitor_validation

# Verify key functionality
curl -I https://your-domain.com/
```

## Rollback Procedure

If issues are detected after deployment:

```bash
# 1. Enable maintenance mode
touch /var/www/tg/maintenance.flag

# 2. Stop application
sudo systemctl stop gunicorn

# 3. Revert migrations (if needed)
python manage.py migrate <app> <previous_migration>

# 4. Restore database (if needed)
dropdb production_db
createdb production_db
psql production_db < backup_production_TIMESTAMP.sql

# 5. Revert code
git checkout <previous_commit>

# 6. Restart services
sudo systemctl start gunicorn
sudo systemctl restart nginx

# 7. Disable maintenance mode
rm /var/www/tg/maintenance.flag
```

## Monitoring Schedule

### Daily (First Week)
```bash
python manage.py monitor_validation --period 24
```

### Weekly (Ongoing)
```bash
python manage.py monitor_validation --period 168
```

### On-Demand (After Issues)
```bash
python manage.py monitor_validation --json > /var/log/tg/validation_$(date +%Y%m%d).json
```

## Success Criteria

The deployment is considered successful when:

1. **Data Integrity**: `validate_data_integrity` reports no issues
2. **Health Score**: `monitor_validation` reports health score >= 90
3. **Performance**: No noticeable degradation in response times
4. **Functionality**: All XP workflows operate correctly
5. **Stability**: No constraint violations for 7 consecutive days

## Contacts

- **Technical Lead**: [Contact info]
- **Database Admin**: [Contact info]
- **On-Call Engineer**: [Contact info]

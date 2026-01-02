# Permissions System Deployment Guide

## Overview

This guide covers deploying the centralized permissions system for the World of Darkness application. The system provides role-based access control for characters, items, and locations.

## Prerequisites

- Python 3.10+
- Django 5.1.7
- All migrations applied
- Test database available

## Pre-Deployment Steps

### 1. Verify Current State

```bash
# Check for pending migrations
python manage.py migrate --check

# Run system checks
python manage.py check --deploy

# Verify test database
python manage.py test core.tests.permissions --verbosity=0
```

### 2. Review Changes

Key files in this deployment:

| File | Purpose |
|------|---------|
| `core/permissions.py` | PermissionManager, Role, Permission enums |
| `core/mixins.py` | View permission mixins |
| `core/templatetags/permissions.py` | Template permission tags |
| `core/tests/permissions/` | Test coverage |

### 3. Database Considerations

The permissions system uses existing models:
- `Observer` model for observer relationships
- `Chronicle` for storyteller relationships
- `Character.status` for status-based restrictions

No new migrations required for core permissions.

## Deployment Steps

### Step 1: Deploy to Staging

```bash
# 1. Pull latest code
git pull origin main

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations (if any)
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Restart application server
sudo systemctl restart gunicorn  # or your WSGI server
```

### Step 2: Run Deployment Tests

```bash
# Run deployment-specific tests
python manage.py test core.tests.permissions.test_permissions_deployment -v 2

# Expected: 37 tests, all passing
```

### Step 3: Verify Functionality

Complete the staging checklist at `docs/deployment/permissions_staging_checklist.md`.

### Step 4: Deploy to Production

After staging verification:

```bash
# 1. Create database backup
pg_dump -h $DB_HOST -U $DB_USER $DB_NAME > backup_$(date +%Y%m%d).sql

# 2. Deploy code
git pull origin main

# 3. Run migrations
python manage.py migrate

# 4. Restart services
sudo systemctl restart gunicorn
sudo systemctl restart celery  # if using Celery
```

## Post-Deployment Monitoring

### Error Monitoring

Watch for these error patterns in logs:

```
PermissionDenied: *
Http404: Object not found
AttributeError: 'NoneType' object has no attribute 'owner'
```

### Key Metrics

| Metric | Threshold | Action |
|--------|-----------|--------|
| Permission denied rate | > 1% | Investigate |
| 404 rate | > 5% increase | Review visibility |
| Average response time | > 500ms | Profile queries |

### Health Check Endpoints

If implemented, verify these endpoints:

```bash
curl https://your-domain.com/health/
curl https://your-domain.com/api/status/
```

## Rollback Procedure

If issues are detected:

### Quick Rollback (Code Only)

```bash
# 1. Revert to previous commit
git checkout <previous-commit-hash>

# 2. Restart services
sudo systemctl restart gunicorn
```

### Full Rollback (With Database)

```bash
# 1. Revert code
git checkout <previous-commit-hash>

# 2. Restore database (if schema changed)
psql -h $DB_HOST -U $DB_USER $DB_NAME < backup_YYYYMMDD.sql

# 3. Restart services
sudo systemctl restart gunicorn
```

## Troubleshooting

### Common Issues

**Issue**: Users seeing 404 for characters they should access
- **Cause**: `filter_queryset_for_user` filtering too aggressively
- **Solution**: Check user roles, verify chronicle membership

**Issue**: Owners cannot edit their characters
- **Cause**: Character status preventing edits
- **Solution**: Check `character.status` matches expected state

**Issue**: Template permission tags returning False
- **Cause**: Object missing `user_can_*` methods
- **Solution**: Verify model inherits from proper base class

### Debug Commands

```python
# In Django shell
from core.permissions import PermissionManager, Permission, Role

# Check user roles
roles = PermissionManager.get_user_roles(user, character)
print(f"User roles: {[r.value for r in roles]}")

# Check specific permission
can_edit = PermissionManager.user_has_permission(
    user, character, Permission.EDIT_FULL
)
print(f"Can edit: {can_edit}")

# Check visibility tier
tier = PermissionManager.get_visibility_tier(user, character)
print(f"Visibility: {tier.value}")
```

## Support

For issues with the permissions system:

1. Check logs for error messages
2. Review test failures in CI/CD
3. Consult `docs/design/permissions_system.md` for architecture
4. Contact the development team

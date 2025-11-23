# Permissions System Deployment Guide

This guide provides step-by-step instructions for deploying the permissions system to development, staging, and production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Development Deployment](#development-deployment)
3. [Testing the Deployment](#testing-the-deployment)
4. [Staging Deployment](#staging-deployment)
5. [Production Deployment](#production-deployment)
6. [Rollback Plan](#rollback-plan)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Python**: 3.10+ (tested with 3.11)
- **Django**: 5.1.7
- **Database**: SQLite (dev) or PostgreSQL (production)
- **Dependencies**: See `requirements.txt`

### Required Knowledge

- Django migrations
- Git workflow
- Basic database administration
- Unix command line

---

## Development Deployment

### Step 1: Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows
```

### Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Note: If jsmin fails to install (TinyMCE dependency), you can skip it for development:
pip install Django==5.1.7 django-polymorphic==3.1.0 django-smart-selects==1.6.0 \
            requests==2.32.3 pillow pytest pytest-django bleach python-dotenv numpy==1.26.4
```

### Step 3: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# .env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Step 4: Create and Run Migrations

```bash
# Create migrations for all apps
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Expected output:
# - core.0001_initial (includes Observer model)
# - core.0002_initial (permissions system components)
# - characters, game, items, locations migrations
```

### Step 5: Create Superuser

```bash
# Create admin account for testing
python manage.py createsuperuser
```

### Step 6: Verify Installation

```bash
# Run the permissions test script
python test_permissions_deployment.py

# Expected output:
# Total Tests: 37
# Passed: 37 ✓
# Failed: 0
# Success Rate: 100.0%
```

### Step 7: Start Development Server

```bash
# Run development server
python manage.py runserver

# Access at: http://localhost:8000
```

---

## Testing the Deployment

### Automated Testing

Run the comprehensive permissions test script:

```bash
python test_permissions_deployment.py
```

This script tests:
- ✓ Owner permissions (view full, edit limited, spend XP/freebies)
- ✓ Chronicle Head ST permissions (full access)
- ✓ Game ST permissions (view-only)
- ✓ Player permissions (partial visibility)
- ✓ Observer permissions (partial visibility)
- ✓ Stranger permissions (no access)
- ✓ Admin permissions (full access)

### Manual Testing

Create test users with different roles:

#### 1. Test as Owner

```python
# In Django shell
from django.contrib.auth.models import User
from characters.models.core.character import Character
from game.models import Chronicle

# Create owner and character
owner = User.objects.create_user('owner_test', 'owner@test.com', 'password')
chronicle = Chronicle.objects.create(name="Test Chronicle")
char = Character.objects.create(name="Test Char", owner=owner, chronicle=chronicle, status='App')

# Test owner permissions
from core.permissions import PermissionManager, Permission
PermissionManager.user_has_permission(owner, char, Permission.VIEW_FULL)  # True
PermissionManager.user_has_permission(owner, char, Permission.EDIT_FULL)  # False (owners can't edit stats directly)
PermissionManager.user_has_permission(owner, char, Permission.SPEND_XP)   # True
```

#### 2. Test as Chronicle Head ST

```python
# Create head ST
head_st = User.objects.create_user('head_st_test', 'head_st@test.com', 'password')
chronicle.head_st = head_st
chronicle.save()

# Test head ST permissions
PermissionManager.user_has_permission(head_st, char, Permission.VIEW_FULL)  # True
PermissionManager.user_has_permission(head_st, char, Permission.EDIT_FULL)  # True
PermissionManager.user_has_permission(head_st, char, Permission.APPROVE)    # True
```

#### 3. Test as Game ST

```python
# Create game ST
game_st = User.objects.create_user('game_st_test', 'game_st@test.com', 'password')
chronicle.game_storytellers.add(game_st)

# Test game ST permissions
PermissionManager.user_has_permission(game_st, char, Permission.VIEW_FULL)  # True (read-only)
PermissionManager.user_has_permission(game_st, char, Permission.EDIT_FULL)  # False (no edit access)
```

#### 4. Test as Player

```python
# Create player with character in same chronicle
player = User.objects.create_user('player_test', 'player@test.com', 'password')
player_char = Character.objects.create(name="Player Char", owner=player, chronicle=chronicle, status='App')

# Test player permissions on other's character
PermissionManager.user_has_permission(player, char, Permission.VIEW_PARTIAL)  # True
PermissionManager.user_has_permission(player, char, Permission.VIEW_FULL)     # False
PermissionManager.get_visibility_tier(player, char)  # VisibilityTier.PARTIAL
```

#### 5. Test as Stranger

```python
# Create stranger (no relationship to chronicle)
stranger = User.objects.create_user('stranger_test', 'stranger@test.com', 'password')

# Test stranger permissions
PermissionManager.user_has_permission(stranger, char, Permission.VIEW_PARTIAL)  # False
PermissionManager.get_visibility_tier(stranger, char)  # VisibilityTier.NONE
```

### View Testing

Test the permissions in actual views:

1. **Login as owner**:
   - Navigate to character detail view
   - Should see full character sheet
   - Edit button should show limited form (notes/journals only)
   - Should see "Spend XP" button (if approved)

2. **Login as head ST**:
   - Navigate to character detail view
   - Should see full character sheet
   - Edit button should show full form (all fields)
   - Should see approval controls

3. **Login as game ST**:
   - Navigate to character detail view
   - Should see full character sheet (read-only)
   - No edit button should appear

4. **Login as player**:
   - Navigate to another player's character
   - Should see partial view (public info only)
   - No XP, notes, or secrets visible
   - No edit button

5. **Login as stranger**:
   - Try to access character detail
   - Should get 404 error (object not found)

---

## Staging Deployment

### Prerequisites

- Staging server with SSH access
- Database backup capability
- Reverse proxy (nginx/Apache) configured
- WSGI server (gunicorn/uwsgi) installed

### Step 1: Prepare Staging Environment

```bash
# SSH into staging server
ssh user@staging-server

# Navigate to project directory
cd /path/to/project

# Activate virtual environment
source venv/bin/activate
```

### Step 2: Pull Latest Code

```bash
# Fetch latest changes
git fetch origin

# Checkout the deployment branch
git checkout claude/deploy-permissions-system-01VmQQEaQuGQX8RgsTfnxLY4

# Pull changes
git pull origin claude/deploy-permissions-system-01VmQQEaQuGQX8RgsTfnxLY4
```

### Step 3: Update Dependencies

```bash
# Install/update dependencies
pip install -r requirements.txt --upgrade
```

### Step 4: Configure Environment

Update `.env` for staging:

```bash
# .env (staging)
SECRET_KEY=staging-secret-key-here
DEBUG=False
ALLOWED_HOSTS=staging.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/staging_db
STATIC_ROOT=/path/to/static
MEDIA_ROOT=/path/to/media
```

### Step 5: Database Backup

**CRITICAL**: Always backup before migrations!

```bash
# PostgreSQL backup
pg_dump -U user staging_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Or SQLite backup
cp db.sqlite3 db.sqlite3.backup_$(date +%Y%m%d_%H%M%S)
```

### Step 6: Run Migrations

```bash
# Check what migrations will run
python manage.py showmigrations

# Run migrations
python manage.py migrate

# Expected new migrations:
# - core: Observer model and permissions components
# - Other apps: Updated with permission fields
```

### Step 7: Collect Static Files

```bash
python manage.py collectstatic --no-input
```

### Step 8: Run Tests

```bash
# Run the deployment test script
python test_permissions_deployment.py

# All 37 tests should pass
```

### Step 9: Restart Application Server

```bash
# For gunicorn
sudo systemctl restart gunicorn

# OR for uwsgi
sudo systemctl restart uwsgi

# Restart nginx
sudo systemctl restart nginx
```

### Step 10: Verify Deployment

1. Check application logs:
   ```bash
   tail -f /var/log/gunicorn/error.log
   tail -f /var/log/nginx/error.log
   ```

2. Access staging URL and test manually
3. Monitor for any errors in logs

### Step 11: Load Testing (Optional)

```bash
# Use Apache Bench or similar
ab -n 1000 -c 10 https://staging.yourdomain.com/characters/1/

# Monitor database queries and performance
```

---

## Production Deployment

### Prerequisites Checklist

- [ ] All tests passing in staging
- [ ] User acceptance testing completed
- [ ] Database backup plan confirmed
- [ ] Rollback plan prepared
- [ ] Downtime window scheduled (if needed)
- [ ] Team notified of deployment
- [ ] Monitoring alerts configured

### Pre-Deployment

1. **Announce Maintenance Window** (if needed):
   - Email users about deployment
   - Set maintenance mode page

2. **Final Staging Verification**:
   ```bash
   python test_permissions_deployment.py
   ```

3. **Create Database Backup**:
   ```bash
   # PostgreSQL
   pg_dump -U user production_db > production_backup_$(date +%Y%m%d_%H%M%S).sql

   # Verify backup
   pg_restore --list production_backup_*.sql
   ```

### Deployment Steps

#### Step 1: Enable Maintenance Mode

```bash
# Create maintenance.html in static root
# Configure nginx to serve maintenance page
sudo systemctl reload nginx
```

#### Step 2: Pull Code

```bash
ssh user@production-server
cd /path/to/project
git fetch origin
git checkout claude/deploy-permissions-system-01VmQQEaQuGQX8RgsTfnxLY4
git pull origin claude/deploy-permissions-system-01VmQQEaQuGQX8RgsTfnxLY4
```

#### Step 3: Install Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

#### Step 4: Run Migrations

```bash
# Check migrations first
python manage.py showmigrations

# Run migrations
python manage.py migrate

# Verify migrations succeeded
python manage.py showmigrations | grep "\[X\]"
```

#### Step 5: Collect Static Files

```bash
python manage.py collectstatic --no-input
```

#### Step 6: Restart Application

```bash
# Graceful restart
sudo systemctl reload gunicorn

# Or full restart if needed
sudo systemctl restart gunicorn

# Restart web server
sudo systemctl restart nginx
```

#### Step 7: Disable Maintenance Mode

```bash
# Remove maintenance configuration
# Reload nginx
sudo systemctl reload nginx
```

#### Step 8: Smoke Test

1. Login as admin
2. Create test character
3. Test permissions as different users
4. Check error logs

### Post-Deployment Monitoring

**First 15 minutes**:
- Monitor error logs continuously
- Check application metrics
- Verify key functionality
- Test permissions with real accounts

**First hour**:
- Monitor database performance
- Check for any permission-related errors
- Verify all user types can access correctly

**First 24 hours**:
- Review error logs daily
- Monitor user feedback
- Track any permission-related issues

---

## Rollback Plan

If critical issues arise, follow this rollback procedure:

### Immediate Rollback (Code Only)

```bash
# SSH to server
ssh user@production-server
cd /path/to/project

# Checkout previous version
git log --oneline  # Find previous commit
git checkout <previous-commit-hash>

# Restart application
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Full Rollback (Code + Database)

```bash
# Stop application
sudo systemctl stop gunicorn

# Restore database backup
# PostgreSQL:
dropdb production_db
createdb production_db
pg_restore -d production_db production_backup_YYYYMMDD_HHMMSS.sql

# Rollback code
git checkout <previous-commit-hash>

# Run old migrations
python manage.py migrate <app-name> <previous-migration-number>

# Start application
sudo systemctl start gunicorn
sudo systemctl restart nginx
```

### Partial Rollback (Disable Permissions)

If permissions system causes issues but other features work:

1. Create a feature flag in settings:
   ```python
   # settings.py
   PERMISSIONS_ENABLED = False
   ```

2. Update views to check flag:
   ```python
   if settings.PERMISSIONS_ENABLED:
       # Use new permissions
   else:
       # Use old logic
   ```

---

## Monitoring

### Key Metrics to Monitor

1. **Application Errors**:
   - Permission denied errors
   - 404 errors (should increase for strangers)
   - 500 errors (should not increase)

2. **Database Performance**:
   - Query count per request
   - Slow query log
   - Connection pool usage

3. **User Experience**:
   - Page load times
   - Permission check latency
   - Failed login attempts

### Logging Configuration

Add to `settings.py`:

```python
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
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/permissions.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'core.permissions': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

### Alerts to Configure

1. **High 403/404 Rate**: May indicate permissions too restrictive
2. **Slow Queries**: Permission checks causing performance issues
3. **Error Spike**: Permissions system bugs
4. **Failed Migrations**: Database issues

---

## Troubleshooting

### Common Issues

#### Issue 1: Migrations Fail

**Symptoms**: `django.db.migrations.exceptions.NodeNotFoundError`

**Solution**:
```bash
# Delete migration files and recreate
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

#### Issue 2: Players Can't See Other Characters

**Symptoms**: Players get 404 on other players' characters

**Check**:
1. Verify Character.objects.filter(owner=user, chronicle=chronicle).exists()
2. Check chronicle is set on both characters
3. Verify characters have status='App' (approved)

**Solution**:
```python
# In Django shell
from characters.models.core.character import Character
from game.models import Chronicle

# Check player's characters
player_chars = Character.objects.filter(owner=player)
for char in player_chars:
    print(f"{char.name}: chronicle={char.chronicle}, status={char.status}")
```

#### Issue 3: Owners Can't Edit Characters

**Symptoms**: Owners see "Permission Denied"

**Check**:
1. Verify user is actual owner: `char.owner == user`
2. Check character status (submitted characters are locked)
3. Verify using limited form (not full form)

**Solution**:
```python
# Check ownership
from core.permissions import PermissionManager, Permission
PermissionManager.user_has_permission(user, char, Permission.EDIT_LIMITED)  # Should be True
PermissionManager.user_has_permission(user, char, Permission.EDIT_FULL)     # Should be False
```

#### Issue 4: Import Errors

**Symptoms**: `ImportError: cannot import name 'Character'`

**Solution**:
```python
# Use correct import
from characters.models.core.character import Character
# NOT: from characters.models import Character
```

#### Issue 5: Observer Model Not Found

**Symptoms**: `ImportError: cannot import name 'Observer'`

**Check**:
```bash
# Verify migrations ran
python manage.py showmigrations core
# Should show [X] core.0001_initial and [X] core.0002_initial
```

**Solution**:
```bash
python manage.py migrate core
```

---

## Success Criteria

The deployment is successful when:

- ✓ All 37 automated tests pass
- ✓ No errors in application logs
- ✓ Users can login and access their characters
- ✓ Owners have limited edit access (notes/journals only)
- ✓ Chronicle Head STs have full access
- ✓ Game STs have read-only access
- ✓ Players see partial views of other characters
- ✓ Strangers cannot access characters (404)
- ✓ Database performance is acceptable
- ✓ No user complaints about permissions

---

## Support Contacts

- **Development Team**: dev@yourdomain.com
- **Database Admin**: dba@yourdomain.com
- **Operations**: ops@yourdomain.com

---

## Appendix A: Permissions Matrix

| Role | VIEW_FULL | EDIT_FULL | EDIT_LIMITED | SPEND_XP | SPEND_FREEBIES | DELETE | APPROVE |
|------|-----------|-----------|--------------|----------|----------------|--------|---------|
| Owner | ✓ | ✗ | ✓ | ✓ | Status-dependent | ✓ | ✗ |
| Chronicle Head ST | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Game ST | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Player | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Observer | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Stranger | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Admin | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**Note**: Owner SPEND_FREEBIES permission depends on character status:
- Status 'Un' (Unfinished): ✓ Can spend freebies
- Status 'App' (Approved): ✗ Cannot spend freebies (use XP instead)

---

## Appendix B: Database Schema Changes

### New Tables

1. **core_observer**: Observer permissions
   - Columns: id, content_type_id, object_id, user_id, granted_by_id, granted_at, notes

### Modified Tables

1. **core_model**: Base model for characters/items/locations
   - Added: visibility field (PUB/PRI/CHR/CUS)

2. **game_chronicle**: Chronicle model
   - Added: head_st (ForeignKey to User)
   - Added: game_storytellers (ManyToMany to User)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-23
**Author**: Claude Code Deployment Team

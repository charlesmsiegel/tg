# Staging Deployment Checklist

Quick reference checklist for deploying the permissions system to staging environment.

## Pre-Deployment

- [ ] All development tests passing (37/37)
- [ ] Code review completed
- [ ] Database backup plan confirmed
- [ ] Staging environment accessible
- [ ] Team notified

---

## Deployment Steps

### 1. Backup Current State

```bash
# SSH to staging server
ssh user@staging-server
cd /path/to/project

# Backup database
pg_dump -U user staging_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup current code
git stash save "pre-deployment-backup-$(date +%Y%m%d_%H%M%S)"
```

**Status**: ☐ Complete

---

### 2. Pull Latest Code

```bash
# Fetch and checkout deployment branch
git fetch origin
git checkout claude/deploy-permissions-system-01VmQQEaQuGQX8RgsTfnxLY4
git pull origin claude/deploy-permissions-system-01VmQQEaQuGQX8RgsTfnxLY4
```

**Status**: ☐ Complete

---

### 3. Update Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt --upgrade
```

**Status**: ☐ Complete

---

### 4. Run Migrations

```bash
# Preview migrations
python manage.py showmigrations

# Apply migrations
python manage.py migrate

# Verify migrations
python manage.py showmigrations | grep -E "core|characters|game|items|locations"
```

**Expected migrations**:
- [ ] core.0001_initial
- [ ] core.0002_initial
- [ ] characters migrations with permission fields
- [ ] game migrations updated
- [ ] items migrations updated
- [ ] locations migrations updated

**Status**: ☐ Complete

---

### 5. Collect Static Files

```bash
python manage.py collectstatic --no-input
```

**Status**: ☐ Complete

---

### 6. Run Test Script

```bash
# Run comprehensive permissions test
python test_permissions_deployment.py
```

**Expected result**: All 37 tests pass ✓

**Status**: ☐ Complete

---

### 7. Restart Services

```bash
# Restart application server
sudo systemctl restart gunicorn

# Restart web server
sudo systemctl restart nginx
```

**Status**: ☐ Complete

---

## Post-Deployment Verification

### 8. Check Logs

```bash
# Check for errors
tail -n 100 /var/log/gunicorn/error.log
tail -n 100 /var/log/nginx/error.log
```

**Look for**:
- ☐ No migration errors
- ☐ No import errors
- ☐ No permission-related exceptions

**Status**: ☐ Complete

---

### 9. Manual Testing

#### Test as Owner

- [ ] Login as character owner
- [ ] Navigate to character detail view
- [ ] Verify can see full character sheet
- [ ] Click "Edit" button
- [ ] Verify form shows only limited fields (notes, description, etc.)
- [ ] Verify cannot see stat fields (Strength, Dexterity, etc.)
- [ ] Verify "Spend XP" button appears (if character is approved)

**Status**: ☐ Complete

---

#### Test as Chronicle Head ST

- [ ] Login as chronicle head ST
- [ ] Navigate to any character in chronicle
- [ ] Verify can see full character sheet
- [ ] Click "Edit" button
- [ ] Verify form shows ALL fields including stats
- [ ] Verify "Approve" button appears (if character is submitted)

**Status**: ☐ Complete

---

#### Test as Game ST

- [ ] Login as game ST
- [ ] Navigate to any character in chronicle
- [ ] Verify can see full character sheet (read-only)
- [ ] Verify NO "Edit" button appears
- [ ] Verify can view XP, notes, secrets (full visibility)
- [ ] Verify cannot modify anything

**Status**: ☐ Complete

---

#### Test as Player

- [ ] Login as player with character in chronicle
- [ ] Navigate to OWN character
- [ ] Verify can see full sheet and edit limited fields
- [ ] Navigate to ANOTHER player's character in same chronicle
- [ ] Verify can see character but with limited info
- [ ] Verify cannot see XP, spent XP, notes, secrets
- [ ] Verify NO "Edit" button appears

**Status**: ☐ Complete

---

#### Test as Stranger

- [ ] Login as user with NO characters in chronicle
- [ ] Try to access character detail URL directly
- [ ] Verify receives 404 error (not 403)
- [ ] Verify character does NOT appear in character list

**Status**: ☐ Complete

---

### 10. Performance Check

```bash
# Check database query count (should be minimal)
# Enable Django Debug Toolbar in staging if needed

# Test page load times
curl -w "@curl-format.txt" -o /dev/null -s https://staging.yourdomain.com/characters/1/
```

**Acceptable metrics**:
- [ ] Page load < 2 seconds
- [ ] Database queries < 20 per page
- [ ] No N+1 query warnings

**Status**: ☐ Complete

---

## Issue Tracking

### Issues Found

1. **Issue**: _________________________________________
   - **Severity**: ☐ Critical  ☐ High  ☐ Medium  ☐ Low
   - **Impact**: _________________________________________
   - **Resolution**: _________________________________________

2. **Issue**: _________________________________________
   - **Severity**: ☐ Critical  ☐ High  ☐ Medium  ☐ Low
   - **Impact**: _________________________________________
   - **Resolution**: _________________________________________

---

## Rollback Decision

If critical issues found:

- [ ] **ROLLBACK**: Critical bugs, data loss, or major functionality broken
- [ ] **FIX FORWARD**: Minor issues that can be patched quickly
- [ ] **PROCEED**: No issues found, ready for production

---

## Sign-Off

**Deployed by**: ________________________
**Date**: ________________________
**Time**: ________________________

**Tested by**: ________________________
**Date**: ________________________
**Time**: ________________________

**Approved for Production**: ☐ Yes  ☐ No  ☐ Needs fixes

**Notes**:
_______________________________________________________________
_______________________________________________________________
_______________________________________________________________

---

## Quick Rollback Procedure

If rollback needed:

```bash
# Stop services
sudo systemctl stop gunicorn

# Restore database
dropdb staging_db
createdb staging_db
pg_restore -d staging_db backup_YYYYMMDD_HHMMSS.sql

# Restore code
git stash pop  # Or git checkout <previous-commit>

# Start services
sudo systemctl start gunicorn
sudo systemctl restart nginx
```

---

## Next Steps

After successful staging deployment:

1. [ ] Schedule user acceptance testing (UAT)
2. [ ] Gather feedback from test users
3. [ ] Document any edge cases found
4. [ ] Update production deployment plan if needed
5. [ ] Schedule production deployment window
6. [ ] Notify stakeholders of staging success

---

## Reference Documents

- Full Deployment Guide: `DEPLOYMENT_GUIDE.md`
- Permissions System Design: `docs/design/permissions_system.md`
- Applying Permissions Guide: `docs/guides/applying_permissions.md`
- Test Script: `test_permissions_deployment.py`

---

**Checklist Version**: 1.0
**Last Updated**: 2025-11-23

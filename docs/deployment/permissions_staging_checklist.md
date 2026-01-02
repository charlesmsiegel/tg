# Permissions System Staging Checklist

This checklist must be completed before deploying the permissions system to production.

## Pre-Deployment Verification

### 1. Run Deployment Tests
```bash
python manage.py test core.tests.permissions.test_permissions_deployment -v 2
```
- [ ] All tests pass (expected: 39/39)
- [ ] No test failures or errors
- [ ] Test output reviewed for warnings

### 2. Run Full Permission Test Suite
```bash
python manage.py test core.tests.permissions -v 2
```
- [ ] All permission tests pass
- [ ] Template tag tests pass
- [ ] Integration tests pass

### 3. Verify Database State
```bash
python manage.py check
python manage.py migrate --check
```
- [ ] No pending migrations
- [ ] Database schema is current
- [ ] No integrity errors

## Functional Testing

### 4. Role Assignment Verification
Test each role type manually:

- [ ] **Anonymous User**: Cannot view private characters
- [ ] **Authenticated User**: Can only see own characters
- [ ] **Owner**: Can view/edit own characters, spend XP
- [ ] **Game ST**: Can view all chronicle characters (read-only)
- [ ] **Head ST**: Can view/edit all chronicle characters
- [ ] **Admin**: Full access to all objects

### 5. Status-Based Restrictions
Test permission changes based on character status:

- [ ] **Unfinished**: Owner can spend freebies, not XP
- [ ] **Submitted**: Owner cannot edit, ST can
- [ ] **Approved**: Owner can spend XP, not freebies
- [ ] **Retired**: Owner cannot make changes
- [ ] **Deceased**: Read-only except for ST/Admin

### 6. Visibility Tier Testing
- [ ] Full visibility for owner/ST shows all fields
- [ ] Partial visibility for players hides private data
- [ ] No visibility for strangers returns 404

### 7. Observer System
- [ ] Owner can add observers
- [ ] Observers can view with partial visibility
- [ ] Owner can remove observers
- [ ] Removed observers lose access

## Performance Testing

### 8. Query Performance
- [ ] List views load in < 2 seconds
- [ ] Detail views load in < 1 second
- [ ] No N+1 query issues detected
- [ ] `filter_queryset_for_user` optimized

### 9. Load Testing (Optional)
- [ ] Concurrent user simulation
- [ ] Permission checks under load
- [ ] No race conditions detected

## Security Review

### 10. Access Control Audit
- [ ] Review all views using permission mixins
- [ ] Verify no unprotected endpoints
- [ ] Check template permission checks
- [ ] Validate API endpoints (if any)

### 11. Edge Cases
- [ ] User with multiple roles (owner + ST)
- [ ] Character in chronicle where user is ST
- [ ] Objects without owner field
- [ ] Objects without chronicle field

## Rollback Preparation

### 12. Rollback Plan
- [ ] Database backup taken
- [ ] Previous code version identified
- [ ] Rollback procedure documented
- [ ] Team notified of deployment window

## Sign-Off

| Check | Verified By | Date |
|-------|-------------|------|
| Deployment tests pass | | |
| Functional tests pass | | |
| Performance acceptable | | |
| Security review complete | | |
| Rollback plan ready | | |

## Proceed to Production

When all checks are complete and signed off:

1. Create production deployment ticket
2. Schedule deployment window
3. Notify stakeholders
4. Execute deployment
5. Monitor for 24 hours post-deployment

# Validation System Deployment Checklist

Complete checklist for deploying the validation system from development → staging → production.

## Pre-Deployment (Development Environment)

### Code Review

- [x] **Review all constraint implementations**
  - Character XP constraints (characters/models/core/character.py)
  - Attribute constraints (characters/models/core/attribute_block.py)
  - Ability constraints (characters/models/core/ability_block.py)
  - Willpower constraints (characters/models/core/human.py)
  - Age constraints (characters/models/core/human.py)
  - STRelationship uniqueness (game/models.py)

- [x] **Review all transaction wrappers**
  - spend_xp() method
  - approve_xp_spend() method
  - award_xp() method (Scene)

- [x] **Review all model validation**
  - Character.clean() for status transitions
  - Human.clean() for cross-field validation

### Testing

- [x] **Run full test suite**
  ```bash
  pytest characters/tests/core/test_validation_constraints.py -v
  pytest --tb=short
  ```
  Expected: 89 tests passing

- [ ] **Manual testing of XP workflows**
  - Create character and spend XP
  - Approve XP as storyteller
  - Award scene XP
  - Test constraint violations (should fail gracefully)

- [ ] **Performance testing**
  ```bash
  pytest characters/tests/performance/test_xp_performance.py
  ```
  Expected: < 100ms per XP operation

### Documentation

- [x] **Deployment documentation created**
  - docs/deployment/VALIDATION_STAGING_DEPLOYMENT.md
  - docs/deployment/VALIDATION_DEPLOYMENT_CHECKLIST.md (this file)

- [x] **Management commands created**
  - core/management/commands/validate_data_integrity.py
  - core/management/commands/monitor_validation.py

- [ ] **User-facing documentation updated**
  - Update XP spending help text
  - Update storyteller guides
  - Create troubleshooting guide

## Staging Deployment

### Pre-Deployment

- [ ] **Backup staging database**
  ```bash
  pg_dump staging_db > backup_staging_$(date +%Y%m%d_%H%M%S).sql
  ```

- [ ] **Pull latest code**
  ```bash
  git checkout claude/deploy-validation-staging-013V3YCrnPRoKSA3SJz5Tvnq
  git pull origin claude/deploy-validation-staging-013V3YCrnPRoKSA3SJz5Tvnq
  ```

- [ ] **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```

### Data Validation

- [ ] **Run data integrity check**
  ```bash
  python manage.py validate_data_integrity --verbose
  ```
  Expected: 0 issues

- [ ] **Fix any issues found**
  ```bash
  python manage.py validate_data_integrity --fix
  python manage.py validate_data_integrity  # Verify fixed
  ```

### Migration

- [ ] **Review migrations**
  ```bash
  python manage.py showmigrations
  ```

- [ ] **Apply migrations**
  ```bash
  python manage.py migrate
  ```
  Expected: All constraint migrations applied successfully

- [ ] **Verify constraints active**
  ```bash
  python manage.py shell
  >>> from characters.models import Character
  >>> c = Character.objects.create(name="Test", xp=-1)
  # Should raise IntegrityError
  ```

### Post-Deployment Verification

- [ ] **Run test suite**
  ```bash
  pytest characters/tests/core/test_validation_constraints.py -v
  pytest
  ```

- [ ] **Collect static files**
  ```bash
  python manage.py collectstatic --noinput
  ```

- [ ] **Restart application**
  ```bash
  sudo systemctl restart tg-web
  ```

- [ ] **Health check**
  ```bash
  curl -I http://staging.yoursite.com/
  ```
  Expected: HTTP 200

### Functional Testing

- [ ] **Test XP spending workflow**
  - Login as player
  - Navigate to character
  - Spend XP on trait
  - Verify transaction succeeds

- [ ] **Test XP approval workflow**
  - Login as storyteller
  - Navigate to XP approvals
  - Approve pending XP spend
  - Verify atomic update (status + trait)

- [ ] **Test scene XP awards**
  - Login as storyteller
  - Navigate to finished scene
  - Award XP to participants
  - Verify all characters receive XP

- [ ] **Test constraint violations**
  - Attempt to set negative XP
  - Attempt to set invalid attribute
  - Attempt to exceed willpower
  - Verify friendly error messages

### Monitoring Setup

- [ ] **Configure monitoring**
  ```bash
  # Add to crontab
  0 * * * * cd /path/to/tg && python manage.py monitor_validation --json >> /var/log/tg/validation_monitor.log
  ```

- [ ] **Configure alerts**
  - Set up email alerts for health score < 90
  - Set up Slack webhook for critical issues
  - Configure PagerDuty for production incidents

- [ ] **Test monitoring**
  ```bash
  python manage.py monitor_validation
  python manage.py monitor_validation --json
  ```

### Staging Soak Period (1 Week)

- [ ] **Monitor daily for 1 week**
  - Check validation health report daily
  - Review error logs for constraint violations
  - Monitor performance metrics
  - Track user feedback

- [ ] **Collect metrics**
  | Metric | Target | Actual | Notes |
  |--------|--------|--------|-------|
  | XP Spend Success Rate | > 95% | ___% | |
  | XP Spend Response Time | < 200ms | ___ms | |
  | Scene XP Award Success | 100% | ___% | |
  | Constraint Violations | 0/day | ___ | |
  | Transaction Rollbacks | < 1% | ___% | |

- [ ] **Document issues found**
  - List all bugs discovered
  - Document workarounds
  - Create fix tasks

- [ ] **User acceptance testing**
  - Have 3+ STs test all workflows
  - Have 5+ players test XP spending
  - Collect feedback survey

## Production Deployment

### Pre-Deployment

- [ ] **Staging sign-off complete**
  - All critical bugs fixed
  - Performance metrics met
  - User acceptance complete
  - Team training complete

- [ ] **Schedule maintenance window**
  - Date: ________________
  - Time: ________________ (off-peak hours)
  - Duration: 2 hours
  - Communicated to users: Yes/No

- [ ] **Prepare rollback plan**
  - Test rollback procedure in staging
  - Document rollback steps
  - Identify rollback decision criteria
  - Assign rollback authority

- [ ] **Backup production database**
  ```bash
  pg_dump production_db > backup_production_$(date +%Y%m%d_%H%M%S).sql
  ```
  - Verify backup integrity
  - Store backup off-site
  - Document restore procedure

### Deployment

- [ ] **Enable maintenance mode**
  ```bash
  # Display maintenance page to users
  touch /var/www/tg/maintenance.flag
  ```

- [ ] **Pull production code**
  ```bash
  git checkout main  # or production branch
  git pull origin main
  ```

- [ ] **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Run data validation**
  ```bash
  python manage.py validate_data_integrity --verbose
  python manage.py validate_data_integrity --fix  # If needed
  ```

- [ ] **Apply migrations**
  ```bash
  python manage.py migrate
  ```

- [ ] **Collect static files**
  ```bash
  python manage.py collectstatic --noinput
  ```

- [ ] **Restart application**
  ```bash
  sudo systemctl restart tg-web
  ```

- [ ] **Verify application started**
  ```bash
  sudo systemctl status tg-web
  tail -f /var/log/tg/application.log
  ```

- [ ] **Disable maintenance mode**
  ```bash
  rm /var/www/tg/maintenance.flag
  ```

### Post-Deployment Verification

- [ ] **Smoke tests**
  - Homepage loads
  - Login works
  - Character list loads
  - Character detail loads

- [ ] **Functional tests**
  - Create new character
  - Spend XP
  - Approve XP (as ST)
  - Award scene XP

- [ ] **Health check**
  ```bash
  python manage.py monitor_validation
  ```
  Expected: Health score 100

- [ ] **Performance check**
  - Check response times
  - Monitor database queries
  - Check for slow transactions

### Monitoring (First 24 Hours)

- [ ] **Hour 1: Active monitoring**
  - Watch logs continuously
  - Monitor error rate
  - Check user activity
  - Be ready for immediate rollback

- [ ] **Hours 2-4: Frequent checks**
  - Check monitoring dashboard every 30 minutes
  - Review error logs
  - Check performance metrics

- [ ] **Hours 5-24: Regular monitoring**
  - Check dashboard every 2 hours
  - Run validation health check every 4 hours
  - Monitor user feedback channels

- [ ] **Metrics to track**
  | Time | Health Score | Errors | Performance | Notes |
  |------|-------------|--------|-------------|-------|
  | Hour 1 | ___ | ___ | ___ | |
  | Hour 2 | ___ | ___ | ___ | |
  | Hour 4 | ___ | ___ | ___ | |
  | Hour 8 | ___ | ___ | ___ | |
  | Hour 24 | ___ | ___ | ___ | |

### Production Soak Period (1 Week)

- [ ] **Daily health checks**
  ```bash
  python manage.py monitor_validation >> /var/log/tg/validation_daily.log
  ```

- [ ] **Weekly metrics review**
  - Compare to staging metrics
  - Identify any degradation
  - Track improvement trends

- [ ] **User feedback review**
  - Monitor support tickets
  - Check user forums/chat
  - Survey storytellers

## Rollback Procedures

### Emergency Rollback (Critical Issue)

- [ ] **Decision criteria met**
  - Data corruption detected
  - System unavailable
  - Critical functionality broken
  - Health score < 50

- [ ] **Execute rollback**
  ```bash
  # 1. Stop application
  sudo systemctl stop tg-web

  # 2. Restore database
  psql production_db < backup_production_TIMESTAMP.sql

  # 3. Revert code
  git checkout PREVIOUS_STABLE_TAG
  python manage.py migrate characters XXXX  # Previous migration
  python manage.py migrate game XXXX

  # 4. Restart application
  sudo systemctl start tg-web
  ```

- [ ] **Verify rollback**
  - System accessible
  - Data intact
  - Functionality restored

- [ ] **Post-mortem**
  - Document issue
  - Analyze root cause
  - Create fix plan
  - Schedule re-deployment

### Partial Rollback (Remove Constraints, Keep Transactions)

- [ ] **Decision criteria**
  - Constraints too restrictive
  - Performance degradation
  - Frequent false positives
  - Transactions working well

- [ ] **Execute partial rollback**
  ```bash
  # Create migration to remove constraints
  python manage.py makemigrations --empty characters --name remove_constraints

  # Edit migration to remove CheckConstraints only
  # Apply migration
  python manage.py migrate
  ```

- [ ] **Verify partial rollback**
  - Transactions still active
  - Constraints removed
  - Performance restored

## Sign-Off

### Staging Deployment

- [ ] **Technical Lead**: ________________ Date: ______
- [ ] **QA Lead**: ________________ Date: ______
- [ ] **Product Owner**: ________________ Date: ______

### Production Deployment

- [ ] **Technical Lead**: ________________ Date: ______
- [ ] **Operations Lead**: ________________ Date: ______
- [ ] **Product Owner**: ________________ Date: ______

### Post-Deployment Review (1 Week After Production)

- [ ] **Deployment successful**: Yes/No
- [ ] **All metrics met**: Yes/No
- [ ] **Issues encountered**: _________________________
- [ ] **Lessons learned**: _________________________
- [ ] **Documentation updated**: Yes/No

## Notes and Issues

Use this section to document any issues, workarounds, or deviations from the plan:

```
[DATE] [ISSUE] [RESOLUTION]
___________________________________________________________
___________________________________________________________
___________________________________________________________
___________________________________________________________
___________________________________________________________
```

## References

- [Staging Deployment Guide](VALIDATION_STAGING_DEPLOYMENT.md)
- [Data Validation Design](../design/data_validation.md)
- [Test Suite](../../characters/tests/core/test_validation_constraints.py)
- [Monitoring Command](../../core/management/commands/monitor_validation.py)
- [Data Integrity Command](../../core/management/commands/validate_data_integrity.py)

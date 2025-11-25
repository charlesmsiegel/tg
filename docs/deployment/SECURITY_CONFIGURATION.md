# Production Security Configuration

**Status**: ✅ **COMPLETE**
**Last Updated**: 2025-11-23

## Overview

The production security configuration for the Tellurian Games application has been successfully completed. All critical security settings are properly configured and follow Django's security best practices.

## Completed Configuration

### 1. Environment-Specific Settings ✅

Settings have been split into three modules in `tg/settings/`:

- **`base.py`**: Common settings shared across all environments
- **`development.py`**: Development-specific settings with DEBUG=True
- **`production.py`**: Production settings with all security features enabled

The correct environment is selected via the `DJANGO_ENVIRONMENT` environment variable (defaults to development).

### 2. SECRET_KEY Configuration ✅

**Development** (`tg/settings/development.py:14`):
```python
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-dev-key-change-this-in-production-8x7@k#f9$m2n!q5w"
)
```
- Includes fallback for local development
- Clearly marked as insecure default

**Production** (`tg/settings/production.py:14`):
```python
SECRET_KEY = os.environ["SECRET_KEY"]
```
- **REQUIRES** SECRET_KEY from environment variables
- Will raise `KeyError` if not set (fails fast)
- No insecure fallback allowed

### 3. Security Headers ✅

All critical security headers are configured in `tg/settings/production.py`:

#### HTTPS/SSL Configuration (lines 28-55)
- `SECURE_SSL_REDIRECT = True` - Force all traffic to HTTPS
- `SESSION_COOKIE_SECURE = True` - Secure session cookies
- `CSRF_COOKIE_SECURE = True` - Secure CSRF cookies
- `SECURE_PROXY_SSL_HEADER` - Proxy SSL header detection

#### HTTP Strict Transport Security (HSTS)
- `SECURE_HSTS_SECONDS = 31536000` (1 year)
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- `SECURE_HSTS_PRELOAD = True`

#### Content Security
- `SECURE_CONTENT_TYPE_NOSNIFF = True` - Prevent MIME sniffing
- `SECURE_BROWSER_XSS_FILTER = True` - Enable XSS protection
- `X_FRAME_OPTIONS = "DENY"` - Prevent clickjacking
- `SECURE_REFERRER_POLICY = "same-origin"` - Referrer policy

### 4. CSRF Protection ✅

CSRF settings are configured in `tg/settings/production.py:58-69`:

```python
CSRF_COOKIE_HTTPONLY = False  # Required for AJAX requests
CSRF_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_NAME = "csrftoken"
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
```

### 5. Session Security ✅

Session security settings in `tg/settings/production.py:72-85`:

```python
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 1209600  # 2 weeks default
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Configurable
```

### 6. Additional Security Features ✅

- **DEBUG Mode**: Always `False` in production
- **ALLOWED_HOSTS**: Required from environment variable (fails if not set)
- **Enhanced Logging**: Separate error logging for production
- **Admin Notifications**: Email notifications for admins on errors

## Environment Variables

A comprehensive `.env.example` file is provided in the project root with all required and optional environment variables documented.

### Required for Production

```bash
# REQUIRED - Must be set
DJANGO_ENVIRONMENT=production
SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=example.com,www.example.com

# RECOMMENDED - Configure for your deployment
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
```

### Generating a Secure SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Verification

To verify the production configuration:

1. **Check settings load correctly**:
   ```bash
   export DJANGO_ENVIRONMENT=production
   export SECRET_KEY="test-key"
   export DJANGO_ALLOWED_HOSTS="example.com"
   python manage.py check --deploy
   ```

2. **Run Django's deployment checklist**:
   ```bash
   python manage.py check --deploy
   ```

3. **Verify security headers** (after deployment):
   - Use [securityheaders.com](https://securityheaders.com)
   - Check for A+ rating

## Security Checklist

- ✅ SECRET_KEY properly configured from environment
- ✅ DEBUG = False in production
- ✅ ALLOWED_HOSTS required from environment
- ✅ HTTPS enforced via SECURE_SSL_REDIRECT
- ✅ Secure cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- ✅ HSTS configured (1 year, include subdomains, preload)
- ✅ Content security headers (X-Frame-Options, Content-Type-NoSniff, XSS-Filter)
- ✅ CSRF protection configured
- ✅ Session security configured
- ✅ Referrer policy set
- ✅ Environment-specific settings properly split
- ✅ .env.example file provided for documentation

## Next Steps

1. **Before Deployment**:
   - Generate a strong SECRET_KEY
   - Configure DJANGO_ALLOWED_HOSTS for your domain(s)
   - Set CSRF_TRUSTED_ORIGINS if needed for cross-origin requests
   - Configure email settings for admin notifications

2. **After Deployment**:
   - Run `python manage.py check --deploy` in production
   - Verify security headers using online tools
   - Monitor error logs for the first 24 hours
   - Test password reset and email functionality

3. **Optional Enhancements**:
   - Configure PostgreSQL/MySQL database (see production.py:98-128)
   - Set up Redis for caching (see production.py:182-193)
   - Configure AWS S3 for static/media files (see production.py:133-141)
   - Enable template caching (already configured in production.py:198-208)

## References

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)
- [Django Security Documentation](https://docs.djangoproject.com/en/5.1/topics/security/)
- [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)
- [HSTS Preload List](https://hstspreload.org/)

## Maintenance

This security configuration should be reviewed:
- After major Django version upgrades
- When adding new domains or subdomains
- When security advisories are published
- At least annually as part of security audit

---

**Configuration completed by**: Claude Code
**Verified**: 2025-11-23

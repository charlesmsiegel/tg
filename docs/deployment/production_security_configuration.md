# Production Security Configuration

This document describes the production security configuration implemented in the Tellurian Games Django application.

## Overview

The application now uses environment-specific settings modules to ensure proper security configuration in production while maintaining ease of development locally.

## Settings Structure

### Settings Modules

The settings are organized as follows:

```
tg/
├── settings/
│   ├── __init__.py        # Auto-loads appropriate settings based on DJANGO_ENVIRONMENT
│   ├── base.py            # Common settings shared across all environments
│   ├── development.py     # Development-specific settings (DEBUG=True, etc.)
│   └── production.py      # Production settings with full security configuration
```

### Environment Selection

The `DJANGO_ENVIRONMENT` environment variable determines which settings to load:

- `development` (default): Loads `tg.settings.development`
- `production`: Loads `tg.settings.production`

Set this in your `.env` file:

```bash
# For development (default)
DJANGO_ENVIRONMENT=development

# For production
DJANGO_ENVIRONMENT=production
```

## Production Security Features

### 1. SECRET_KEY Management

**Production Requirement**: The `SECRET_KEY` environment variable MUST be set in production. The application will raise an error if it's missing.

Generate a secure secret key:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Add to your production `.env`:

```bash
SECRET_KEY=your-generated-secret-key-here
```

### 2. HTTPS/SSL Configuration

Production settings enforce HTTPS:

```python
# Force all HTTP requests to redirect to HTTPS
SECURE_SSL_REDIRECT = True

# Use secure cookies (only transmitted over HTTPS)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

**Environment Variables**:

```bash
# Disable SSL redirect if behind a proxy that handles SSL termination
SECURE_SSL_REDIRECT=False

# Configure proxy SSL header
# Already set in production.py as: SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

### 3. HTTP Strict Transport Security (HSTS)

HSTS tells browsers to only access the site via HTTPS for a specified time period:

```python
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

**Environment Variables**:

```bash
# Configure HSTS duration (in seconds)
SECURE_HSTS_SECONDS=31536000

# Include all subdomains in HSTS policy
SECURE_HSTS_INCLUDE_SUBDOMAINS=True

# Enable HSTS preloading (see https://hstspreload.org/)
SECURE_HSTS_PRELOAD=True
```

**Warning**: Once HSTS is enabled with a long duration, browsers will refuse non-HTTPS connections even if you later disable HTTPS. Only enable HSTS after confirming HTTPS works correctly.

### 4. Content Security

```python
# Prevent browsers from guessing content types
SECURE_CONTENT_TYPE_NOSNIFF = True

# Enable browser XSS protection
SECURE_BROWSER_XSS_FILTER = True

# Prevent site from being framed (clickjacking protection)
X_FRAME_OPTIONS = "DENY"

# Control referrer information
SECURE_REFERRER_POLICY = "same-origin"
```

These settings are hardcoded in `production.py` and don't require environment variables.

### 5. CSRF Protection

```python
# CSRF cookie configuration
CSRF_COOKIE_HTTPONLY = False  # Must be False for AJAX requests
CSRF_COOKIE_SECURE = True     # Only transmit over HTTPS
CSRF_COOKIE_SAMESITE = "Strict"
```

**Cross-Origin Requests**: If you need to accept POST requests from other domains (e.g., mobile apps, API clients), configure trusted origins:

```bash
# In .env - comma-separated, must include protocol
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com,https://api.example.com
```

### 6. Session Security

```python
SESSION_COOKIE_HTTPONLY = True   # Prevent JavaScript access to session cookie
SESSION_COOKIE_SECURE = True     # Only transmit over HTTPS
SESSION_COOKIE_SAMESITE = "Lax"  # Some CSRF protection
```

**Environment Variables**:

```bash
# Session duration in seconds (default: 1209600 = 2 weeks)
SESSION_COOKIE_AGE=1209600

# Expire session when browser closes
SESSION_EXPIRE_AT_BROWSER_CLOSE=False
```

### 7. Allowed Hosts

**Production Requirement**: The `DJANGO_ALLOWED_HOSTS` environment variable MUST be set in production.

```bash
# Comma-separated list of allowed hostnames
DJANGO_ALLOWED_HOSTS=example.com,www.example.com,api.example.com
```

The application will raise an error if this is not configured in production.

### 8. Admin Error Notifications

Configure admin emails to receive error notifications:

```bash
# Comma-separated list of admin emails
# Format: email@example.com or Name <email@example.com>
ADMIN_EMAILS=admin@example.com,John Doe <john@example.com>
```

Errors will be logged to `error.log` and emailed to these addresses if email is configured.

## Database Configuration

For production, SQLite is not recommended. Uncomment the relevant database section in `tg/settings/production.py` and configure:

### PostgreSQL (Recommended)

```bash
DB_NAME=tg_db
DB_USER=tg_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_CONN_MAX_AGE=600
DB_SSLMODE=require
```

### MySQL/MariaDB

```bash
DB_NAME=tg_db
DB_USER=tg_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306
```

Then uncomment the appropriate `DATABASES` configuration in `tg/settings/production.py`.

## Static and Media Files

For production, consider using cloud storage (AWS S3, Google Cloud Storage, etc.) for static and media files.

### AWS S3 Configuration

1. Install dependencies:
   ```bash
   pip install django-storages boto3
   ```

2. Configure environment variables:
   ```bash
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_STORAGE_BUCKET_NAME=your_bucket_name
   AWS_S3_REGION_NAME=us-east-1
   ```

3. Uncomment the S3 configuration in `tg/settings/production.py`.

## Caching

For production performance, configure Redis caching:

1. Install dependencies:
   ```bash
   pip install django-redis redis
   ```

2. Configure environment variable:
   ```bash
   REDIS_URL=redis://127.0.0.1:6379/1
   ```

3. Uncomment the Redis configuration in `tg/settings/production.py`.

## Deployment Checklist

Before deploying to production:

- [ ] Set `DJANGO_ENVIRONMENT=production`
- [ ] Generate and set a secure `SECRET_KEY`
- [ ] Configure `DJANGO_ALLOWED_HOSTS` with your domain(s)
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure production database (PostgreSQL/MySQL)
- [ ] Set up email service (SMTP, SES, Mailgun, etc.)
- [ ] Configure `CSRF_TRUSTED_ORIGINS` if needed
- [ ] Set admin emails for error notifications
- [ ] Consider enabling caching (Redis)
- [ ] Consider using cloud storage for static/media files
- [ ] Run `python manage.py check --deploy` to verify security settings
- [ ] Test HTTPS redirect and security headers
- [ ] Verify HSTS is working before enabling long duration

## Testing Security Configuration

Run Django's deployment check:

```bash
python manage.py check --deploy
```

This command will warn you about any security settings that should be configured for production.

## Development vs Production

### Development (default)
- `DEBUG = True`
- Uses SQLite database
- Email prints to console
- Allows `localhost` and `127.0.0.1` connections
- No HTTPS requirements
- Permissive security settings for local development

### Production
- `DEBUG = False` (hardcoded, cannot be changed)
- Requires SECRET_KEY from environment (no default)
- Requires DJANGO_ALLOWED_HOSTS from environment
- Forces HTTPS with HSTS
- Secure cookies only
- Strict security headers
- Enhanced logging (errors logged to file)
- Recommended: PostgreSQL/MySQL, Redis, S3/cloud storage

## Migrating from Old Settings

The old `tg/settings.py` has been backed up to `tg/settings.py.backup`. The new settings structure is backward compatible:

- `manage.py` and `wsgi.py` still reference `tg.settings`
- The `tg/settings/__init__.py` module automatically loads the correct environment settings
- All existing code importing `from django.conf import settings` continues to work
- Environment variables from `.env` are still loaded via `python-dotenv`

## References

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)
- [Django Security Settings](https://docs.djangoproject.com/en/5.1/topics/security/)
- [HSTS Preload List](https://hstspreload.org/)
- [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)

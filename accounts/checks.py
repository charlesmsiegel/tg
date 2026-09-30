"""System checks for the account throttle (accounts.throttle)."""

from django.conf import settings
from django.core import checks

PER_PROCESS_CACHES = {
    "django.core.cache.backends.locmem.LocMemCache",
    "django.core.cache.backends.dummy.DummyCache",
}


@checks.register(checks.Tags.security, deploy=True)
def check_throttle_cache(app_configs, **kwargs):
    """The throttle counts in the default cache, which every worker must share."""
    backend = settings.CACHES.get("default", {}).get("BACKEND", "")
    if backend not in PER_PROCESS_CACHES:
        return []
    return [
        checks.Warning(
            "The default cache is per process, so each worker keeps its own log-in, "
            "sign-up and password-reset throttle counters.",
            hint="Use a shared cache such as Redis for CACHES['default'].",
            id="accounts.W001",
        )
    ]

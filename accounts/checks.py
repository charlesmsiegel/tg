"""System checks for the account throttle (accounts.throttle)."""

from django.conf import settings
from django.core import checks

from accounts.throttle import trusted_proxy_networks

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


@checks.register(checks.Tags.security, deploy=True)
def check_throttle_proxies(app_configs, **kwargs):
    """Require an explicit decision about forwarded client addresses at deployment."""
    if settings.AUTH_THROTTLE_TRUSTED_PROXIES is None:
        return [
            checks.Warning(
                "The authentication throttle proxy trust is not configured; forwarded headers are ignored.",
                hint="Set AUTH_THROTTLE_TRUSTED_PROXIES to proxy IPs/CIDRs, or an empty value for direct access.",
                id="accounts.W002",
            )
        ]
    try:
        trusted_proxy_networks()
    except (ValueError, TypeError):
        return [
            checks.Error(
                "AUTH_THROTTLE_TRUSTED_PROXIES must contain valid proxy IP addresses or CIDRs.",
                id="accounts.E001",
            )
        ]
    return []

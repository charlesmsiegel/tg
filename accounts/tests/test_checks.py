"""The deploy check that the throttle's cache is shared (accounts.checks)."""

from django.test import SimpleTestCase, override_settings

from accounts import checks
from accounts.checks import check_throttle_cache


def cache(backend):
    return {"default": {"BACKEND": backend}}


class ThrottleCacheCheckTests(SimpleTestCase):
    @override_settings(CACHES=cache("django.core.cache.backends.locmem.LocMemCache"))
    def test_per_process_cache_warns(self):
        self.assertEqual([m.id for m in check_throttle_cache(None)], ["accounts.W001"])

    @override_settings(CACHES=cache("django_redis.cache.RedisCache"))
    def test_shared_cache_passes(self):
        self.assertEqual(check_throttle_cache(None), [])


@override_settings(DEBUG=False)
class ThrottleProxyCheckTests(SimpleTestCase):
    @override_settings(AUTH_THROTTLE_TRUSTED_PROXIES=None)
    def test_unconfigured_production_proxy_trust_warns(self):
        self.assertEqual([m.id for m in checks.check_throttle_proxies(None)], ["accounts.W002"])

    @override_settings(AUTH_THROTTLE_TRUSTED_PROXIES=[])
    def test_explicit_direct_deployment_passes(self):
        self.assertEqual(checks.check_throttle_proxies(None), [])

    @override_settings(AUTH_THROTTLE_TRUSTED_PROXIES=["10.0.0.0/24", "2001:db8::/32"])
    def test_explicit_proxy_networks_pass(self):
        self.assertEqual(checks.check_throttle_proxies(None), [])

    @override_settings(AUTH_THROTTLE_TRUSTED_PROXIES=["anything"])
    def test_invalid_network_is_a_configuration_error(self):
        self.assertEqual([m.id for m in checks.check_throttle_proxies(None)], ["accounts.E001"])

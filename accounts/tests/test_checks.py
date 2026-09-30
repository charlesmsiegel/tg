"""The deploy check that the throttle's cache is shared (accounts.checks)."""

from django.test import SimpleTestCase, override_settings

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

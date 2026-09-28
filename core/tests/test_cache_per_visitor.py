"""Cached pages must not be served to a different visitor.

Pages render per-user markup (the nav's username, staff links, messages), so every
full-page cache keys on the visitor's cookies (core.cache.cache_page_per_visitor).
"""

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from characters.models.vampire.discipline import Discipline
from characters.models.vampire.path import Path

LOCMEM = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}


@override_settings(CACHES=LOCMEM)
class CachePerVisitorTest(TestCase):
    def setUp(self):
        cache.clear()
        User.objects.create_user("cached_staffer", password="pw", is_staff=True)

    def assert_not_shared(self, url):
        self.client.login(username="cached_staffer", password="pw")
        self.assertContains(self.client.get(url), "cached_staffer")
        self.client.logout()
        self.assertNotContains(self.client.get(url), "cached_staffer")

    def test_cached_detail_view(self):
        # DisciplineDetailView is a CachedDetailView.
        discipline = Discipline.objects.create(name="Auspex", property_name="auspex")
        self.assert_not_shared(discipline.get_absolute_url())

    def test_cache_page_decorated_view(self):
        path = Path.objects.create(name="Path of Blood")
        self.assert_not_shared(path.get_absolute_url())

    def test_home_page(self):
        self.assert_not_shared(reverse("core:home"))

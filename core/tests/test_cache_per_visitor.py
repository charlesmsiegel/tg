"""Cached pages must not be served to a different visitor.

Pages render per-user markup (the nav's username, staff links, messages), so every
full-page cache keys on the visitor's cookies (core.cache.cache_page_per_visitor).
"""

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.core.cache import cache
from django.db import connection
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.test import RequestFactory, TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View as DjangoView

from characters.models.vampire.discipline import Discipline
from characters.models.vampire.path import Path
from core.cache import cache_page_per_visitor

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


@override_settings(CACHES=LOCMEM)
class SharedAnonymousPageTest(TestCase):
    """Anonymous visitors share one cached copy of a page that holds nothing
    per-visitor; anything with a session, messages or a CSRF token is not shared."""

    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()
        self.calls = 0

    def view(self, body="page", csrf=False, cookie=False):
        @method_decorator(cache_page_per_visitor(60), name="dispatch")
        class View(DjangoView):
            def get(view, request):
                self.calls += 1
                response = HttpResponse(f"{body} {get_token(request) if csrf else ''}")
                if cookie:
                    response.set_cookie("flavour", "mint")
                return response

        return View.as_view()

    def get(self, view, cookies=None, **headers):
        cookie = "; ".join(f"{name}={value}" for name, value in (cookies or {}).items())
        request = self.factory.get("/reference/", headers=headers, HTTP_COOKIE=cookie)
        request.user = AnonymousUser()
        return view(request)

    def test_anonymous_visitors_share_one_copy(self):
        view = self.view()
        self.get(view)
        self.get(view, cookies={"csrftoken": "another-visitors-token"})
        self.assertEqual(self.calls, 1)
        self.assertIn("Cookie", self.get(view)["Vary"])

    def test_a_page_with_a_csrf_token_or_a_cookie_is_not_shared(self):
        for kwargs in ({"csrf": True}, {"cookie": True}):
            with self.subTest(**kwargs):
                cache.clear()
                self.calls = 0
                view = self.view(**kwargs)
                self.get(view)
                self.get(view)
                self.assertEqual(self.calls, 2)

    def test_a_visitor_with_a_session_or_messages_is_not_served_the_shared_copy(self):
        view = self.view()
        self.get(view)
        for cookie in (settings.SESSION_COOKIE_NAME, "messages"):
            with self.subTest(cookie=cookie):
                calls = self.calls
                self.get(view, cookies={cookie: "x"})
                self.assertEqual(self.calls, calls + 1)

    def test_htmx_fragments_are_cached_apart_from_pages(self):
        view = self.view()
        self.get(view)
        self.get(view, HX_Request="true")
        self.assertEqual(self.calls, 2)

    def test_reference_page_is_shared_between_anonymous_visitors(self):
        discipline = Discipline.objects.create(name="Auspex", property_name="auspex")
        url = discipline.get_absolute_url()
        first = self.client.get(url)
        self.assertNotContains(first, "csrfmiddlewaretoken")
        self.assertNotIn("csrftoken", first.cookies)
        self.client.cookies["csrftoken"] = "another-visitors-token"
        with CaptureQueriesContext(connection) as queries:
            self.assertContains(self.client.get(url), "Auspex")
        # Served from the shared copy: only the request's transaction savepoints.
        self.assertFalse([q["sql"] for q in queries if "SAVEPOINT" not in q["sql"]])

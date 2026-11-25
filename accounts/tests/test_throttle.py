"""Throttling of the log-in, sign-up and password-reset forms (accounts.throttle)."""

from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core import mail
from django.core.cache import cache
from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from accounts.throttle import THROTTLED_MESSAGE, attempt_throttled, over_limit


@override_settings(AUTH_THROTTLE_LIMIT=2, AUTH_THROTTLE_WINDOW=300)
class AuthThrottleTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.user = User.objects.create_user("player", "player@example.com", "right-password")

    def login(self, password="wrong-password", username="player", **extra):
        return self.client.post(
            reverse("login"), {"username": username, "password": password}, **extra
        )

    def assertThrottled(self, response):
        self.assertEqual(response.status_code, 429)
        self.assertIn(THROTTLED_MESSAGE, [str(m) for m in get_messages(response.wsgi_request)])
        self.assertFalse(response.context["form"].is_bound)

    def test_login_is_throttled_after_the_limit_even_with_the_right_password(self):
        self.assertEqual(self.login().status_code, 200)
        self.assertEqual(self.login().status_code, 200)
        response = self.login(password="right-password")
        self.assertThrottled(response)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_limit_is_per_username_and_per_client(self):
        self.login()
        self.login()
        self.assertEqual(self.login(username="someone-else").status_code, 200)
        self.assertEqual(self.login(username=" PLAYER ").status_code, 429)
        response = self.login(password="right-password", REMOTE_ADDR="203.0.113.9")
        self.assertEqual(response.status_code, 302)

    @override_settings(AUTH_THROTTLE_CLIENT_LIMIT=3)
    def test_rotating_usernames_hits_the_per_client_limit(self):
        for name in ("a", "b", "c"):
            self.assertEqual(self.login(username=name).status_code, 200)
        self.assertThrottled(self.login(username="d", password="right-password"))
        response = self.login(password="right-password", REMOTE_ADDR="203.0.113.9")
        self.assertEqual(response.status_code, 302)

    @override_settings(AUTH_THROTTLE_CLIENT_LIMIT=2)
    def test_rotating_emails_hits_the_per_client_limit_for_password_reset(self):
        for email in ("a@example.com", "b@example.com"):
            self.client.post(reverse("password_reset"), {"email": email})
        mail.outbox.clear()
        response = self.client.post(reverse("password_reset"), {"email": "player@example.com"})
        self.assertThrottled(response)
        self.assertEqual(mail.outbox, [])

    def test_limit_resets_with_the_next_window(self):
        with patch("accounts.throttle.time.time", return_value=1000.0):
            self.login()
            self.login()
            self.assertEqual(self.login().status_code, 429)
        with patch("accounts.throttle.time.time", return_value=1600.0):
            self.assertEqual(self.login(password="right-password").status_code, 302)

    def test_get_requests_are_not_counted(self):
        for _ in range(5):
            self.assertEqual(self.client.get(reverse("login")).status_code, 200)
        self.assertEqual(self.login(password="right-password").status_code, 302)

    def test_signup_is_throttled_per_client(self):
        def signup(name):
            return self.client.post(
                reverse("accounts:signup"),
                {
                    "username": name,
                    "email": f"{name}@example.com",
                    "password1": "testpass123!",
                    "password2": "testpass123!",
                },
            )

        self.assertEqual(signup("first").status_code, 302)
        self.assertEqual(signup("second").status_code, 302)
        self.assertThrottled(signup("third"))
        self.assertFalse(User.objects.filter(username="third").exists())

    def test_password_reset_is_throttled_per_email(self):
        url = reverse("password_reset")
        for _ in range(2):
            self.assertEqual(
                self.client.post(url, {"email": "player@example.com"}).status_code, 302
            )
        self.assertThrottled(self.client.post(url, {"email": "player@example.com"}))
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(self.client.post(url, {"email": "other@example.com"}).status_code, 302)

    def test_cache_outage_refuses_login_signup_and_reset_without_side_effects(self):
        with (
            patch("accounts.throttle.cache.incr", return_value=None),
            self.assertLogs("accounts.throttle", "ERROR"),
        ):
            self.assertThrottled(self.login(password="right-password"))
            self.assertNotIn("_auth_user_id", self.client.session)
            self.assertThrottled(
                self.client.post(
                    reverse("accounts:signup"),
                    {
                        "username": "outage",
                        "email": "outage@example.com",
                        "password1": "testpass123!",
                        "password2": "testpass123!",
                    },
                )
            )
            self.assertFalse(User.objects.filter(username="outage").exists())
            self.assertThrottled(
                self.client.post(reverse("password_reset"), {"email": "player@example.com"})
            )
            self.assertEqual(mail.outbox, [])


@override_settings(AUTH_THROTTLE_LIMIT=2, AUTH_THROTTLE_CLIENT_LIMIT=50, AUTH_THROTTLE_WINDOW=300)
class ThrottleCounterTests(SimpleTestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)

    def test_burst_across_boundary_does_not_get_a_fresh_limit(self):
        with patch("accounts.throttle.time.time", return_value=1199.99):
            self.assertFalse(over_limit("boundary", 2))
            self.assertFalse(over_limit("boundary", 2))
        with patch("accounts.throttle.time.time", return_value=1200.01):
            self.assertTrue(over_limit("boundary", 2))

    def test_previous_bucket_decays_and_eventually_expires(self):
        with patch("accounts.throttle.time.time", return_value=900.0):
            self.assertFalse(over_limit("decay", 2))
            self.assertFalse(over_limit("decay", 2))
        with patch("accounts.throttle.time.time", return_value=1350.0):
            self.assertFalse(over_limit("decay", 2))
            self.assertTrue(over_limit("decay", 2))
        with patch("accounts.throttle.time.time", return_value=1800.0):
            self.assertFalse(over_limit("decay", 2))

    def test_expired_counter_is_retried_once(self):
        with patch(
            "accounts.throttle.cache.incr", side_effect=[ValueError("missing"), 1]
        ) as increment:
            self.assertFalse(over_limit("retry", 2))
        self.assertEqual(increment.call_count, 2)

    def test_repeated_expiry_and_backend_exceptions_refuse_attempt(self):
        for failure in (ValueError("missing"), ConnectionError("cache down")):
            with (
                self.subTest(error=type(failure).__name__),
                patch("accounts.throttle.cache.incr", side_effect=failure),
                self.assertLogs("accounts.throttle", "ERROR"),
            ):
                self.assertTrue(over_limit("failure", 2))

    def test_failed_add_and_failed_previous_bucket_read_refuse_attempt(self):
        for method in ("add", "get"):
            with (
                self.subTest(method=method),
                patch(
                    f"accounts.throttle.cache.{method}", side_effect=ConnectionError("cache down")
                ),
                self.assertLogs("accounts.throttle", "ERROR"),
            ):
                self.assertTrue(over_limit("failure", 2))

    def test_suppressed_previous_bucket_read_failure_refuses_attempt(self):
        with (
            patch("accounts.throttle.cache.get", return_value=None),
            self.assertLogs("accounts.throttle", "ERROR"),
        ):
            self.assertTrue(over_limit("failure", 2))

    @override_settings(AUTH_THROTTLE_TRUSTED_PROXIES=[])
    def test_spoofed_forwarded_header_cannot_reset_counter(self):
        factory = RequestFactory()
        for forwarded in ("203.0.113.1", "203.0.113.2"):
            request = factory.post("/", HTTP_X_FORWARDED_FOR=forwarded)
            self.assertFalse(attempt_throttled("signup", request))
        self.assertTrue(
            attempt_throttled("signup", factory.post("/", HTTP_X_FORWARDED_FOR="203.0.113.3"))
        )

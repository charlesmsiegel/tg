"""Throttling of the log-in, sign-up and password-reset forms (accounts.throttle)."""

from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.throttle import THROTTLED_MESSAGE


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

    def test_limit_resets_with_the_next_window(self):
        with patch("accounts.throttle.time.time", return_value=1000.0):
            self.login()
            self.login()
            self.assertEqual(self.login().status_code, 429)
        with patch("accounts.throttle.time.time", return_value=1300.0):
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

    def test_cache_outage_fails_open(self):
        """With Redis down, django-redis's IGNORE_EXCEPTIONS makes incr return None."""
        with patch("accounts.throttle.cache.incr", return_value=None):
            for _ in range(3):
                self.assertEqual(self.login().status_code, 200)

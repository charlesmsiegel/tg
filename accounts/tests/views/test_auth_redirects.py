"""Login and logout redirect settings resolve; logout used to return a 500."""

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse


class AuthRedirectSettingsTest(TestCase):
    def test_redirect_settings_resolve_to_home(self):
        home = reverse("core:home")
        self.assertEqual(resolve_url(settings.LOGIN_REDIRECT_URL), home)
        self.assertEqual(resolve_url(settings.LOGOUT_REDIRECT_URL), home)

    def test_logout_redirects_home_and_ends_the_session(self):
        user = User.objects.create_user("logout_user", password="pw-12345")
        self.client.force_login(user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("core:home"), fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_still_lands_on_the_profile(self):
        # CustomLoginView overrides get_success_url; LOGIN_REDIRECT_URL is only its fallback.
        user = User.objects.create_user("login_user", password="pw-12345")

        response = self.client.post(
            reverse("login"), {"username": "login_user", "password": "pw-12345"}
        )

        self.assertRedirects(
            response, user.profile.get_absolute_url(), fetch_redirect_response=False
        )

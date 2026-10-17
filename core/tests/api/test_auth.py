"""Real CSRF, native login quota and session lifecycle for the auth facade."""

from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import Client, TestCase, override_settings

from game.models import Chronicle, Gameline, STRelationship

AUTH = "/api/v1/auth/"
PASSWORD = "right-password-123!"


@override_settings(AUTH_THROTTLE_LIMIT=10, AUTH_THROTTLE_CLIENT_LIMIT=50)
class SessionAuthTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.user = User.objects.create_user("native-player", password=PASSWORD)
        self.client = Client(enforce_csrf_checks=True)

    def token(self, client=None):
        response = (client or self.client).get(AUTH + "csrf/", secure=True)
        self.assertEqual(response.status_code, 200)
        return response.json()["csrf_token"]

    def login(self, client=None, token=None, username="native-player", password=PASSWORD, **extra):
        client = client or self.client
        token = token or self.token(client)
        return client.post(
            AUTH + "login/",
            urlencode({"username": username, "password": password}),
            content_type="application/x-www-form-urlencoded",
            secure=True,
            HTTP_X_CSRFTOKEN=token,
            HTTP_ORIGIN="https://testserver",
            **extra,
        )

    def test_anonymous_discovery_sets_cookie_without_identity_or_session(self):
        response = self.client.get(AUTH + "csrf/", secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.json()), {"authenticated", "csrf_token"})
        self.assertFalse(response.json()["authenticated"])
        self.assertIn(settings.CSRF_COOKIE_NAME, response.cookies)
        self.assertNotIn(settings.SESSION_COOKIE_NAME, response.cookies)
        self.assertIn("no-store", response["Cache-Control"])
        self.assertIn("Cookie", response.get("Vary", ""))

    def test_valid_login_verifies_session_and_safe_metadata(self):
        profile = self.user.profile
        profile.discord_id = "PRIVATE_DISCORD"
        profile.lines = "PRIVATE_LINES"
        profile.veils = "PRIVATE_VEILS"
        profile.save()
        response = self.login()
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["authenticated"])
        self.assertEqual(data["user"], {"id": self.user.pk, "username": self.user.username})
        self.assertEqual(set(data["profile"]), {"theme", "preferred_heading", "is_st"})
        self.assertFalse(data["profile"]["is_st"])
        self.assertEqual(set(data["session"]), {"cookie_age_seconds", "browser_close"})
        self.assertGreater(data["session"]["cookie_age_seconds"], 0)
        self.assertNotIn(b"PRIVATE_", response.content)
        self.assertNotIn(PASSWORD.encode(), response.content)
        session = self.client.get("/api/v1/session/", secure=True)
        self.assertEqual(session.status_code, 200)
        self.assertEqual(session.json()["user"]["id"], self.user.pk)
        self.assertEqual(self.client.get(AUTH + "csrf/", secure=True).json()["user"], data["user"])

    def test_login_rotates_session_and_csrf(self):
        session = self.client.session
        session["anonymous_state"] = "retained"
        session.save()
        old_key = session.session_key
        old_token = self.token()
        old_cookie = self.client.cookies[settings.CSRF_COOKIE_NAME].value
        response = self.login(token=old_token)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(old_key, self.client.session.session_key)
        self.assertNotEqual(old_cookie, self.client.cookies[settings.CSRF_COOKIE_NAME].value)
        self.assertEqual(self.client.session["anonymous_state"], "retained")
        stale = self.client.post(
            AUTH + "logout/",
            secure=True,
            HTTP_X_CSRFTOKEN=old_token,
            HTTP_ORIGIN="https://testserver",
        )
        self.assertEqual(stale.status_code, 403)
        self.assertEqual(self.client.get("/api/v1/session/", secure=True).status_code, 200)
        old_client = Client()
        old_client.cookies[settings.SESSION_COOKIE_NAME] = old_key
        self.assertEqual(old_client.get("/api/v1/session/").status_code, 401)

    def test_login_rejects_missing_cookie_token_and_foreign_origin(self):
        token = self.token()
        body = urlencode({"username": self.user.username, "password": PASSWORD})
        cases = [
            ({}, self.client),
            ({"HTTP_X_CSRFTOKEN": "invalid"}, self.client),
            ({"HTTP_X_CSRFTOKEN": token}, Client(enforce_csrf_checks=True)),
            ({"HTTP_X_CSRFTOKEN": token, "HTTP_ORIGIN": "https://evil.example"}, self.client),
            ({"HTTP_X_CSRFTOKEN": token, "HTTP_REFERER": "https://evil.example/"}, self.client),
        ]
        for headers, client in cases:
            headers = {"HTTP_ORIGIN": "https://testserver", **headers}
            if "HTTP_REFERER" in headers:
                headers.pop("HTTP_ORIGIN")
            with self.subTest(headers=headers):
                response = client.post(
                    AUTH + "login/",
                    body,
                    content_type="application/x-www-form-urlencoded",
                    secure=True,
                    **headers,
                )
                self.assertEqual(response.status_code, 403)
                self.assertNotIn("_auth_user_id", client.session)

    def test_invalid_inactive_and_missing_users_have_generic_identical_errors(self):
        responses = [self.login(password="wrong"), self.login(username="absent")]
        self.user.is_active = False
        self.user.save()
        responses.append(self.login())
        for response in responses:
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {"error": "invalid_credentials"})
            self.assertNotIn("_auth_user_id", self.client.session)
            self.assertIn("no-store", response["Cache-Control"])

    @override_settings(AUTH_THROTTLE_LIMIT=2)
    def test_native_and_api_share_normalized_account_throttle_both_directions(self):
        token = self.token()
        self.client.post(
            "/accounts/login/",
            {"username": " NATIVE-PLAYER ", "password": "wrong", "csrfmiddlewaretoken": token},
            secure=True,
            HTTP_ORIGIN="https://testserver",
        )
        self.assertEqual(self.login(password="wrong").status_code, 400)
        self.assertEqual(self.login().status_code, 429)
        cache.clear()
        self.assertEqual(self.login(password="wrong").status_code, 400)
        self.assertEqual(self.login(password="wrong").status_code, 400)
        native = self.client.post(
            "/accounts/login/",
            {
                "username": self.user.username,
                "password": PASSWORD,
                "csrfmiddlewaretoken": self.token(),
            },
            secure=True,
            HTTP_ORIGIN="https://testserver",
        )
        self.assertEqual(native.status_code, 429)
        self.assertNotIn("_auth_user_id", self.client.session)

    @override_settings(AUTH_THROTTLE_CLIENT_LIMIT=2)
    def test_rotating_usernames_hits_ip_limit_and_other_ip_remains_independent(self):
        self.assertEqual(self.login(username="first").status_code, 400)
        self.assertEqual(self.login(username="second").status_code, 400)
        self.assertEqual(self.login().status_code, 429)
        self.assertEqual(self.login(REMOTE_ADDR="203.0.113.7").status_code, 200)

    def test_json_multipart_and_unknown_duplicate_fields_are_rejected(self):
        token = self.token()
        for content_type, body, status in [
            (
                "application/json",
                '{"username":"native-player","password":"right-password-123!"}',
                415,
            ),
            ("text/plain", "anything", 415),
            (
                "application/x-www-form-urlencoded",
                urlencode({"username": self.user.username, "password": PASSWORD, "owner": "1"}),
                400,
            ),
            (
                "application/x-www-form-urlencoded",
                f"username={self.user.username}&username=other&password={PASSWORD}",
                400,
            ),
        ]:
            with self.subTest(content_type=content_type, body=body):
                response = self.client.post(
                    AUTH + "login/",
                    body,
                    content_type=content_type,
                    secure=True,
                    HTTP_X_CSRFTOKEN=token,
                    HTTP_ORIGIN="https://testserver",
                )
                self.assertEqual(response.status_code, status)
                self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post(
            AUTH + "login/",
            {"username": self.user.username, "password": PASSWORD},
            secure=True,
            HTTP_X_CSRFTOKEN=token,
            HTTP_ORIGIN="https://testserver",
        )
        self.assertEqual(response.status_code, 415)

    def test_logout_requires_csrf_flushes_server_session_and_repeated_logout_is_safe(self):
        self.assertEqual(self.login().status_code, 200)
        old_key = self.client.session.session_key
        self.assertEqual(self.client.post(AUTH + "logout/", secure=True).status_code, 403)
        response = self.client.post(
            AUTH + "logout/",
            secure=True,
            HTTP_X_CSRFTOKEN=self.token(),
            HTTP_ORIGIN="https://testserver",
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertIn("no-store", response["Cache-Control"])
        self.assertEqual(self.client.get("/api/v1/session/", secure=True).status_code, 401)
        old_client = Client()
        old_client.cookies[settings.SESSION_COOKIE_NAME] = old_key
        self.assertEqual(old_client.get("/api/v1/session/").status_code, 401)
        self.assertEqual(
            self.client.post(
                AUTH + "logout/",
                secure=True,
                HTTP_X_CSRFTOKEN=self.token(),
                HTTP_ORIGIN="https://testserver",
            ).status_code,
            204,
        )

    def test_method_contracts_and_no_get_logout(self):
        self.assertEqual(self.login().status_code, 200)
        token = self.token()
        for suffix, method in [
            ("login/", "get"),
            ("login/", "put"),
            ("logout/", "get"),
            ("logout/", "delete"),
            ("csrf/", "post"),
        ]:
            with self.subTest(suffix=suffix, method=method):
                response = getattr(self.client, method)(
                    AUTH + suffix,
                    secure=True,
                    HTTP_X_CSRFTOKEN=token,
                    HTTP_ORIGIN="https://testserver",
                )
                self.assertEqual(response.status_code, 405)
                self.assertIn("no-store", response["Cache-Control"])
        self.assertEqual(self.client.get("/api/v1/session/", secure=True).status_code, 200)

    @override_settings(
        SESSION_EXPIRE_AT_BROWSER_CLOSE=True,
        SESSION_COOKIE_SECURE=True,
        CSRF_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        CSRF_COOKIE_SAMESITE="Strict",
    )
    def test_production_cookie_flags_and_browser_close_metadata(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        cookie = response.cookies[settings.SESSION_COOKIE_NAME]
        self.assertTrue(cookie["secure"])
        self.assertTrue(cookie["httponly"])
        self.assertEqual(cookie["samesite"], "Lax")
        self.assertFalse(cookie["expires"])
        csrf = response.cookies[settings.CSRF_COOKIE_NAME]
        self.assertTrue(csrf["secure"])
        self.assertEqual(csrf["samesite"], "Strict")
        self.assertTrue(response.json()["session"]["browser_close"])
        self.assertNotIn("expires_at", response.json()["session"])

    def test_native_html_login_still_redirects_to_profile(self):
        token = self.token()
        response = self.client.post(
            "/accounts/login/",
            {
                "username": self.user.username,
                "password": PASSWORD,
                "csrfmiddlewaretoken": token,
                "next": "https://evil.example/",
            },
            secure=True,
            HTTP_ORIGIN="https://testserver",
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.user.profile.get_absolute_url())

    def test_session_discovery_exposes_cookie_policy_not_invented_sliding_expiry(self):
        self.assertEqual(self.login().status_code, 200)
        data = self.client.get(AUTH + "csrf/", secure=True).json()
        self.assertEqual(
            data["session"],
            {"browser_close": False, "cookie_age_seconds": settings.SESSION_COOKIE_AGE},
        )
        self.assertNotIn("expires_at", data["session"])
        self.assertNotIn("refresh_token", data)

    def test_password_change_and_deleted_session_revoke_discovery_and_api(self):
        self.assertEqual(self.login().status_code, 200)
        self.user.set_password("new-password-123!")
        self.user.save()
        self.assertFalse(self.client.get(AUTH + "csrf/", secure=True).json()["authenticated"])
        self.assertEqual(self.client.get("/api/v1/session/", secure=True).status_code, 401)
        self.assertEqual(self.login(password="new-password-123!").status_code, 200)
        session = self.client.session
        session.delete(session.session_key)
        self.assertFalse(self.client.get(AUTH + "csrf/", secure=True).json()["authenticated"])
        self.assertEqual(self.client.get("/api/v1/session/", secure=True).status_code, 401)

    def test_login_as_different_account_flushes_previous_session(self):
        other = User.objects.create_user("other-player", password=PASSWORD)
        self.assertEqual(self.login().status_code, 200)
        old_key = self.client.session.session_key
        response = self.login(username=other.username)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"]["id"], other.pk)
        self.assertNotEqual(old_key, self.client.session.session_key)
        old_client = Client()
        old_client.cookies[settings.SESSION_COOKIE_NAME] = old_key
        self.assertEqual(old_client.get("/api/v1/session/").status_code, 401)

    def test_missing_profile_has_safe_null_projection(self):
        self.user.profile.delete()
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()["profile"])

    def test_logout_foreign_origin_and_anonymous_without_csrf_rejected(self):
        self.assertEqual(
            self.client.post(
                AUTH + "logout/", secure=True, HTTP_ORIGIN="https://testserver"
            ).status_code,
            403,
        )
        self.assertEqual(self.login().status_code, 200)
        token = self.token()
        self.assertEqual(
            self.client.post(
                AUTH + "logout/",
                secure=True,
                HTTP_X_CSRFTOKEN=token,
                HTTP_ORIGIN="https://evil.example",
            ).status_code,
            403,
        )
        self.assertTrue(self.client.get(AUTH + "csrf/", secure=True).json()["authenticated"])

    def test_storyteller_summary_is_live_and_not_a_staff_or_game_st_grant(self):
        self.assertEqual(self.login().status_code, 200)
        chronicle = Chronicle.objects.create(name="Role test", head_st=self.user)
        self.assertTrue(self.client.get(AUTH + "csrf/", secure=True).json()["profile"]["is_st"])
        chronicle.head_st = None
        chronicle.save()
        chronicle.game_storytellers.add(self.user)
        self.assertFalse(self.client.get(AUTH + "csrf/", secure=True).json()["profile"]["is_st"])
        relation = STRelationship.objects.create(
            user=self.user, chronicle=chronicle, gameline=Gameline.objects.create(name="Mage")
        )
        self.assertTrue(self.client.get(AUTH + "csrf/", secure=True).json()["profile"]["is_st"])
        relation.delete()
        self.user.is_staff = True
        self.user.save()
        self.assertFalse(self.client.get(AUTH + "csrf/", secure=True).json()["profile"]["is_st"])

    def test_form_csrf_field_is_supported_and_sensitive_parameters_are_marked(self):
        token = self.token()
        response = self.client.post(
            AUTH + "login/",
            urlencode(
                {"username": self.user.username, "password": PASSWORD, "csrfmiddlewaretoken": token}
            ),
            content_type="application/x-www-form-urlencoded",
            secure=True,
            HTTP_ORIGIN="https://testserver",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.sensitive_post_parameters, "__ALL__")
        self.assertIn("no-store", response["Cache-Control"])

    def test_expired_session_is_anonymous_without_refresh(self):
        self.assertEqual(self.login().status_code, 200)
        session = self.client.session
        session.set_expiry(-1)
        session.save()
        response = self.client.get(AUTH + "csrf/", secure=True)
        self.assertEqual(set(response.json()), {"authenticated", "csrf_token"})
        self.assertFalse(response.json()["authenticated"])
        self.assertEqual(self.client.get("/api/v1/session/", secure=True).status_code, 401)

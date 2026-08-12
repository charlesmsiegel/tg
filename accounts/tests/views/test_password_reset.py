"""Regression tests for password-reset email delivery."""

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class PasswordResetEmailTests(TestCase):
    def test_password_reset_sends_plain_text_and_escaped_html(self):
        user = User.objects.create_user(
            username="<b>Unsafe Name</b>",
            email="unsafe@example.com",
            password="testpass",
        )

        self.client.post(reverse("password_reset"), {"email": user.email})

        message = mail.outbox[0]
        assert message.body.lstrip().startswith("Password Reset Request")
        assert "<b>Unsafe Name</b>" in message.body
        assert message.alternatives[0].mimetype == "text/html"
        assert "&lt;b&gt;Unsafe Name&lt;/b&gt;" in message.alternatives[0].content
        assert "/accounts/reset/" in message.body
        assert "/accounts/reset/" in message.alternatives[0].content

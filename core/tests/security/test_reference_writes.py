from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Book


class ReferenceWriteSecurityTests(TestCase):
    def test_anonymous_and_player_cannot_create_or_update_book(self):
        book = Book.objects.create(name="Public guide", edition="20th")
        player = get_user_model().objects.create_user("reference_player")
        for user in (None, player):
            with self.subTest(user=user):
                if user is None:
                    self.client.logout()
                else:
                    self.client.force_login(user)
                self.assertEqual(
                    self.client.get("/book/create/").status_code,
                    401 if user is None else 403,
                )
                self.assertEqual(
                    self.client.post(f"/book/update/{book.pk}/", {"name": "Tampered"}).status_code,
                    401 if user is None else 403,
                )
        book.refresh_from_db()
        self.assertEqual(book.name, "Public guide")

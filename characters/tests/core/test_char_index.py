from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import ObjectType


class TestCharacterIndexView(TestCase):
    def setUp(self) -> None:
        self.url = "/characters/index/"
        ObjectType.objects.get_or_create(name="human", type="char", gameline="wod")[0]
        return super().setUp()

    def test_index_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/charlist.html")

    def test_index_content(self):
        player = User.objects.create_user(username="User1", password="12345")
        for i in range(10):
            Human.objects.create(name=f"Human {i}", owner=player)
        response = self.client.get(self.url)
        for i in range(10):
            self.assertContains(response, f"Human {i}")

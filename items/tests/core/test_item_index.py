from django.test import TestCase
from game.models import ObjectType
from items.models.core.item import ItemModel


class TestItemIndexView(TestCase):
    def setUp(self) -> None:
        self.url = "/items/index/"
        ObjectType.objects.get_or_create(name="item", type="obj", gameline="wod")[0]
        return super().setUp()

    def test_index_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/index.html")

    def test_index_content(self):
        for i in range(10):
            ItemModel.objects.create(
                name=f"Item {i}",
            )
        response = self.client.get(self.url)
        for i in range(10):
            self.assertContains(response, f"Item {i}")

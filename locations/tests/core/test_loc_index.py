from django.test import TestCase
from game.models import ObjectType
from locations.models.core.location import LocationModel


class TestLocationIndexView(TestCase):
    def setUp(self) -> None:
        self.url = "/locations/index/"
        ObjectType.objects.get_or_create(name="location", type="loc", gameline="wod")[0]
        return super().setUp()

    def test_index_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/index.html")

    def test_index_content(self):
        for i in range(10):
            LocationModel.objects.create(
                name=f"Location {i}",
            )
        response = self.client.get(self.url)
        for i in range(10):
            self.assertContains(response, f"Location {i}")

from characters.models.mage import Effect
from django.test import TestCase
from django.urls import reverse


class TestEffect(TestCase):
    def setUp(self):
        self.effect = Effect.objects.create(
            name="Test Effect",
            correspondence=1,
            time=1,
            spirit=1,
            matter=1,
            forces=1,
            life=1,
            entropy=1,
            mind=1,
            prime=1,
        )

    def test_save(self):
        self.effect.save()
        self.assertEqual(self.effect.rote_cost, 9)
        self.assertEqual(self.effect.max_sphere, 1)


class TestEffectDetailView(TestCase):
    def setUp(self) -> None:
        self.effect = Effect.objects.create(name="Test Effect", description="Test")
        self.url = self.effect.get_absolute_url()

    def test_effect_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_effect_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/effect/detail.html")


class TestEffectCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Effect",
            "description": "Test",
            "correspondence": 0,
            "time": 0,
            "spirit": 0,
            "matter": 0,
            "life": 0,
            "forces": 3,
            "entropy": 0,
            "mind": 0,
            "prime": 2,
        }
        self.url = reverse("characters:mage:create:effect")

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/effect/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Effect.objects.count(), 1)
        self.assertEqual(Effect.objects.first().name, "Test Effect")


class TestEffectUpdateView(TestCase):
    def setUp(self):
        self.effect = Effect.objects.create(name="Test Effect", description="Test")
        self.valid_data = {
            "name": "Test Effect Updated",
            "description": "Test",
            "correspondence": 0,
            "time": 0,
            "spirit": 0,
            "matter": 0,
            "life": 0,
            "forces": 3,
            "entropy": 0,
            "mind": 0,
            "prime": 2,
        }
        self.url = self.effect.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/effect/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.effect.refresh_from_db()
        self.assertEqual(self.effect.name, "Test Effect Updated")
        self.assertEqual(self.effect.description, "Test")

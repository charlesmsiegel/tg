"""Tests for Sphere views."""

from django.test import TestCase

from characters.models.mage import Sphere


class TestSphereModel(TestCase):
    def setUp(self):
        self.sphere = Sphere.objects.create(
            name="Forces",
            property_name="forces",
        )

    def test_str(self):
        self.assertEqual(str(self.sphere), "Forces")

    def test_get_absolute_url(self):
        url = self.sphere.get_absolute_url()
        self.assertIn(f"/characters/mage/sphere/{self.sphere.pk}/", url)

    def test_get_update_url(self):
        expected_url = f"/characters/mage/update/sphere/{self.sphere.pk}/"
        self.assertEqual(self.sphere.get_update_url(), expected_url)

    def test_get_creation_url(self):
        expected_url = "/characters/mage/create/sphere/"
        self.assertEqual(Sphere.get_creation_url(), expected_url)

    def test_get_heading(self):
        self.assertEqual(self.sphere.get_heading(), "mta_heading")


class TestSphereDetailView(TestCase):
    def setUp(self):
        self.sphere = Sphere.objects.create(
            name="Forces",
            property_name="forces",
        )
        self.url = self.sphere.get_absolute_url()

    def test_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/sphere/detail.html")

    def test_detail_view_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["object"], self.sphere)


class TestSphereCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Entropy",
            "property_name": "entropy",
        }
        self.url = Sphere.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/sphere/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Sphere.objects.count(), 1)
        self.assertEqual(Sphere.objects.first().name, "Entropy")


class TestSphereUpdateView(TestCase):
    def setUp(self):
        self.sphere = Sphere.objects.create(
            name="Forces",
            property_name="forces",
        )
        self.valid_data = {
            "name": "Forces Updated",
            "property_name": "forces",
        }
        self.url = self.sphere.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/sphere/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.sphere.refresh_from_db()
        self.assertEqual(self.sphere.name, "Forces Updated")


class TestSphereListView(TestCase):
    def setUp(self):
        self.sphere1 = Sphere.objects.create(name="Correspondence", property_name="correspondence")
        self.sphere2 = Sphere.objects.create(name="Entropy", property_name="entropy")
        self.sphere3 = Sphere.objects.create(name="Forces", property_name="forces")
        self.url = "/characters/mage/list/spheres/"

    def test_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/sphere/list.html")

    def test_list_view_context(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["object_list"]), 3)

    def test_list_view_ordering(self):
        response = self.client.get(self.url)
        spheres = list(response.context["object_list"])
        self.assertEqual(spheres[0].name, "Correspondence")
        self.assertEqual(spheres[1].name, "Entropy")
        self.assertEqual(spheres[2].name, "Forces")

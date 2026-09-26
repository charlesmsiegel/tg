"""Routes for the Tremere Chantry and Barrens object types (seeded names)."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from core.create_redirects import resolve_object_type_url
from game.models import ObjectType
from locations.models.vampire import Barrens, TremereChantry
from locations.views.vampire import (
    BarrensListView,
    TremereChantryCreateView,
    TremereChantryListView,
)


class TestSeededVampireLocationRoutes(TestCase):
    """The index resolves seeded type names; these three used to 404."""

    def setUp(self):
        ObjectType.objects.create(name="tremere_chantry", type="loc", gameline="vtm")
        ObjectType.objects.create(name="barrens", type="loc", gameline="vtm")

    def test_tremere_chantry_create_resolves(self):
        url = resolve_object_type_url("loc", "tremere_chantry", "create")
        self.assertEqual(url, "/locations/vampire/create/tremere_chantry/")
        self.assertIs(resolve(url).func.view_class, TremereChantryCreateView)

    def test_old_chantry_create_name_still_resolves(self):
        url = reverse("locations:vampire:create:chantry")
        self.assertIs(resolve(url).func.view_class, TremereChantryCreateView)

    def test_tremere_chantry_list_resolves(self):
        url = resolve_object_type_url("loc", "tremere_chantry", "list")
        self.assertEqual(url, "/locations/vampire/list/tremere_chantry/")
        self.assertIs(resolve(url).func.view_class, TremereChantryListView)

    def test_barrens_list_resolves(self):
        url = resolve_object_type_url("loc", "barrens", "list")
        self.assertEqual(url, "/locations/vampire/list/barrens/")
        self.assertIs(resolve(url).func.view_class, BarrensListView)

    def test_index_create_redirects_to_tremere_chantry_form(self):
        user = User.objects.create_user("player", "p@test.com", "password")
        self.client.force_login(user)
        response = self.client.post(
            reverse("locations:index"),
            {"action": "create", "loc_type": "tremere_chantry", "gameline": "vtm"},
        )
        self.assertRedirects(
            response, "/locations/vampire/create/tremere_chantry/", fetch_redirect_response=False
        )


class TestTremereChantryAndBarrensListViews(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user("staff", "s@test.com", "password", is_staff=True)
        TremereChantry.objects.create(name="Vienna Chantry")
        Barrens.objects.create(name="Rust Belt")

    def test_staff_sees_tremere_chantry_list(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("locations:vampire:list:tremere_chantry"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/vampire/chantry/list.html")
        self.assertContains(response, "Vienna Chantry")

    def test_staff_sees_barrens_list(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("locations:vampire:list:barrens"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/vampire/barrens/list.html")
        self.assertContains(response, "Rust Belt")

    def test_anonymous_list_gets_public_projection(self):
        """Anonymous users get the allowlisted public projection, not the
        staff list template: a PUB-visibility object's name is shown, but
        the default-visibility (private) objects from setUp are hidden."""
        TremereChantry.objects.create(name="Open Chantry", visibility="PUB")
        Barrens.objects.create(name="Open Barrens", visibility="PUB")
        for name, private_name, public_name in (
            ("tremere_chantry", "Vienna Chantry", "Open Chantry"),
            ("barrens", "Rust Belt", "Open Barrens"),
        ):
            with self.subTest(name=name):
                response = self.client.get(reverse(f"locations:vampire:list:{name}"))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "core/public_object_list.html")
                self.assertContains(response, public_name)
                self.assertNotContains(response, private_name)

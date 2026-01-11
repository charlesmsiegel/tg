from django.contrib.auth.models import User
from django.test import TestCase

from game.models import Chronicle
from locations.models.core import LocationModel


class TestLocation(TestCase):
    def setUp(self) -> None:
        self.location = LocationModel.objects.create(name="Location 1")
        self.child = LocationModel.objects.create(name="Location 2")
        self.child.contained_within.add(self.location)

    def test_location_contained_within(self):
        self.assertIn(self.location, self.child.contained_within.all())
        self.assertIn(self.child, self.location.contains.all())


class TestLocationContainedWithinM2M(TestCase):
    """Tests for the contained_within ManyToManyField (Issue #1040)."""

    def setUp(self) -> None:
        self.parent1 = LocationModel.objects.create(name="Parent 1")
        self.parent2 = LocationModel.objects.create(name="Parent 2")
        self.child = LocationModel.objects.create(name="Child Location")

    def test_location_can_have_multiple_parents(self):
        """Test that a location can be contained within multiple parent locations."""
        self.child.contained_within.add(self.parent1)
        self.child.contained_within.add(self.parent2)

        self.assertEqual(self.child.contained_within.count(), 2)
        self.assertIn(self.parent1, self.child.contained_within.all())
        self.assertIn(self.parent2, self.child.contained_within.all())

    def test_parent_contains_multiple_children(self):
        """Test that a parent location can contain multiple child locations."""
        child2 = LocationModel.objects.create(name="Child 2")
        self.child.contained_within.add(self.parent1)
        child2.contained_within.add(self.parent1)

        self.assertEqual(self.parent1.contains.count(), 2)
        self.assertIn(self.child, self.parent1.contains.all())
        self.assertIn(child2, self.parent1.contains.all())

    def test_contains_reverse_relation(self):
        """Test that the 'contains' reverse relation works correctly."""
        self.child.contained_within.add(self.parent1)

        self.assertIn(self.child, self.parent1.contains.all())
        self.assertEqual(self.parent1.contains.count(), 1)

    def test_remove_from_contained_within(self):
        """Test that removing a parent from contained_within works correctly."""
        self.child.contained_within.add(self.parent1)
        self.child.contained_within.add(self.parent2)
        self.assertEqual(self.child.contained_within.count(), 2)

        self.child.contained_within.remove(self.parent1)

        self.assertEqual(self.child.contained_within.count(), 1)
        self.assertNotIn(self.parent1, self.child.contained_within.all())
        self.assertIn(self.parent2, self.child.contained_within.all())

    def test_clear_contained_within(self):
        """Test that clearing contained_within removes all parent relationships."""
        self.child.contained_within.add(self.parent1)
        self.child.contained_within.add(self.parent2)

        self.child.contained_within.clear()

        self.assertEqual(self.child.contained_within.count(), 0)


class TestLocationTopLevel(TestCase):
    """Tests for the top_level() queryset method."""

    def setUp(self) -> None:
        self.top_level_location = LocationModel.objects.create(name="Top Level")
        self.contained_location = LocationModel.objects.create(name="Contained")
        self.contained_location.contained_within.add(self.top_level_location)

    def test_top_level_returns_locations_without_parents(self):
        """Test that top_level() returns locations not contained within any other."""
        top_level_qs = LocationModel.objects.top_level()

        self.assertIn(self.top_level_location, top_level_qs)
        self.assertNotIn(self.contained_location, top_level_qs)

    def test_top_level_excludes_contained_locations(self):
        """Test that locations with any parent are excluded from top_level()."""
        another_top = LocationModel.objects.create(name="Another Top")

        top_level_qs = LocationModel.objects.top_level()

        self.assertEqual(top_level_qs.count(), 2)
        self.assertIn(self.top_level_location, top_level_qs)
        self.assertIn(another_top, top_level_qs)

    def test_location_with_cleared_parents_is_top_level(self):
        """Test that clearing parents makes a location top-level again."""
        self.contained_location.contained_within.clear()

        top_level_qs = LocationModel.objects.top_level()

        self.assertIn(self.contained_location, top_level_qs)

    def test_location_with_multiple_parents_not_top_level(self):
        """Test that a location with multiple parents is not top-level."""
        parent2 = LocationModel.objects.create(name="Parent 2")
        self.contained_location.contained_within.add(parent2)

        top_level_qs = LocationModel.objects.top_level()

        self.assertNotIn(self.contained_location, top_level_qs)


class TestLocationDetailView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="password")
        self.location = LocationModel.objects.create(
            name="Location 1",
            description="Test description",
            owner=self.user,
            status="App",
        )
        self.url = self.location.get_absolute_url()

    def test_location_detail_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_location_detail_view_templates(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/core/location/detail.html")

    def test_detail_view_content(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertContains(response, self.location.name)
        self.assertContains(response, self.location.description)
        self.assertContains(response, self.location.gauntlet)


class TestLocationCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.valid_data = {
            "name": "Test Name",
            "description": "Test Description",
            "gauntlet": 6,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        self.invalid_data = {"name": "", "description": ""}
        self.url = LocationModel.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/core/location/form.html")

    def test_create_view_successful_post(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LocationModel.objects.count(), 1)
        self.assertEqual(LocationModel.objects.first().name, "Test Name")


class TestLocationUpdateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.location = LocationModel.objects.create(
            name="Location 1",
            description="Test description",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )
        self.valid_data = {
            "name": "Test Name Updated",
            "description": "Test Description Updated",
            "gauntlet": 6,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        self.url = self.location.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/core/location/form.html")

    def test_update_view_successful_post(self):
        self.client.login(username="st_user", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.location.refresh_from_db()
        self.assertEqual(self.location.name, "Test Name Updated")
        self.assertEqual(self.location.description, "Test Description Updated")

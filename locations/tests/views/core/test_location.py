from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from game.models import Chronicle, ObjectType
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
        self.client.force_login(
            get_user_model().objects.create_user("__legacy_auth_staff", is_staff=True)
        )
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/index.html")

    def test_index_content(self):
        self.client.force_login(
            get_user_model().objects.create_user("__legacy_auth_staff", is_staff=True)
        )
        for i in range(10):
            LocationModel.objects.create(
                name=f"Location {i}",
            )
        response = self.client.get(self.url)
        for i in range(10):
            self.assertContains(response, f"Location {i}")


class TestLocationTypeNavigation(TestCase):
    """Choosing a location type is a GET to the typed endpoint (Step 5)."""

    def setUp(self):
        # Create object types for different gamelines
        ObjectType.objects.get_or_create(name="node", type="loc", gameline="mta")
        ObjectType.objects.get_or_create(name="caern", type="loc", gameline="wta")

    def url(self, action):
        return reverse("core:object_type_redirect", kwargs={"kind": "location", "action": action})

    def test_create_action_mta(self):
        """Test create action redirects to Mage location create."""
        self.client.force_login(User.objects.create_user(username="creator"))
        response = self.client.get(self.url("create"), {"loc_type": "node"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("mage", response.url)
        self.assertIn("create", response.url)

    def test_chronicle_context_survives_location_type_selection(self):
        self.client.force_login(User.objects.create_user(username="creator"))
        chronicle = Chronicle.objects.create(name="Selected Chronicle")
        response = self.client.get(
            self.url("create"),
            {"loc_type": "node", "gameline": "mta", "chronicle": chronicle.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(f"chronicle={chronicle.pk}", response.url)

    def test_created_location_belongs_to_selected_chronicle(self):
        user = User.objects.create_user(username="creator")
        chronicle = Chronicle.objects.create(name="Selected Chronicle")
        chronicle.storytellers.add(user)
        self.client.force_login(user)
        response = self.client.post(
            f"{reverse('locations:create:location')}?chronicle={chronicle.pk}",
            {"name": "New Sanctum", "gauntlet": 7, "shroud": 7, "dimension_barrier": 6},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LocationModel.objects.get(name="New Sanctum").chronicle, chronicle)

    def test_create_action_wta(self):
        """Test create action redirects to Werewolf location create."""
        self.client.force_login(User.objects.create_user(username="creator"))
        response = self.client.get(self.url("create"), {"loc_type": "caern"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("werewolf", response.url)
        self.assertIn("create", response.url)

    def test_list_action_mta(self):
        """Test list navigation redirects to the Mage location list."""
        response = self.client.get(self.url("list"), {"loc_type": "node"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("mage", response.url)

    def test_list_action_wta(self):
        """Test list navigation redirects to the Werewolf location list."""
        response = self.client.get(self.url("list"), {"loc_type": "caern"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("werewolf", response.url)

    def test_index_post_is_rejected(self):
        self.client.force_login(User.objects.create_user(username="creator"))
        response = self.client.post("/locations/index/", {"action": "create", "loc_type": "node"})
        self.assertEqual(response.status_code, 405)


class TestLocationIndexViewContext(TestCase):
    """Test context data in LocationIndexView."""

    def setUp(self):
        self.url = "/locations/index/"
        ObjectType.objects.get_or_create(name="location", type="loc", gameline="wod")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_context_contains_form(self):
        """Test context contains location creation form."""
        self.client.force_login(
            get_user_model().objects.create_user("__legacy_auth_staff", is_staff=True)
        )
        response = self.client.get(self.url)
        self.assertIn("form", response.context)

    def test_context_contains_location_tree(self):
        """Test context holds the selected chronicle's containment tree."""
        self.client.force_login(
            get_user_model().objects.create_user("__legacy_auth_staff", is_staff=True)
        )
        response = self.client.get(self.url)
        self.assertIn("location_tree", response.context)
        self.assertIn("line_filter", response.context)

    def test_context_header_for_anonymous_user(self):
        """Anonymous visitors receive only the safe public index context."""
        response = self.client.get(self.url)
        self.assertIn("public_objects", response.context)
        self.assertNotIn("location_tree", response.context)

    def test_context_header_for_authenticated_user(self):
        """Test header uses user's preferred heading."""
        user = User.objects.create_user(username="testuser", password="password", is_staff=True)
        user.profile.preferred_heading = "vtm_heading"
        user.profile.save()
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.context["header"], "vtm_heading")


class TestLocationIndexTree(TestCase):
    """The staff index (Spread M2): chronicle switch, gameline filter, containment tree."""

    url = "/locations/index/"

    def setUp(self):
        from locations.models.mage.node import Node
        from locations.models.werewolf.caern import Caern

        self.client.force_login(get_user_model().objects.create_user("staff", is_staff=True))
        self.ahp = Chronicle.objects.create(name="Ashes of Hyde Park")
        self.other = Chronicle.objects.create(name="Other Chronicle")
        self.city = LocationModel.objects.create(name="Chicago", chronicle=self.ahp)
        self.library = LocationModel.objects.create(name="Newberry Library", chronicle=self.ahp)
        self.library.contained_within.add(self.city)
        self.node = Node.objects.create(name="The Map Room", chronicle=self.ahp)
        self.node.contained_within.add(self.library)
        self.preserve = LocationModel.objects.create(name="Palos Preserve", chronicle=self.ahp)
        self.caern = Caern.objects.create(name="Sweetwater Bluff", chronicle=self.ahp)
        self.caern.contained_within.add(self.preserve)
        self.elsewhere = LocationModel.objects.create(name="Elsewhere", chronicle=self.other)

    @staticmethod
    def names(nodes):
        return [node["location"].name for node in nodes]

    def test_tree_nests_by_containment(self):
        response = self.client.get(self.url, {"chronicle": self.ahp.pk})
        tree = response.context["location_tree"]
        self.assertEqual(self.names(tree), ["Chicago", "Palos Preserve"])
        library = tree[0]["children"][0]
        self.assertEqual(library["location"], self.library)
        self.assertEqual(library["depth"], 1)
        self.assertEqual(self.names(library["children"]), ["The Map Room"])
        self.assertEqual(library["children"][0]["depth"], 2)
        self.assertNotContains(response, "Elsewhere")
        self.assertContains(response, 'class="tl-loctree__node" open')
        self.assertContains(response, "tl-indent-2")

    def test_first_chronicle_with_places_is_the_default(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["selected_chronicle"], self.ahp)
        self.assertEqual(response.context["place_count"], 5)

    def test_chronicle_switch(self):
        response = self.client.get(self.url, {"chronicle": self.other.pk})
        self.assertEqual(self.names(response.context["location_tree"]), ["Elsewhere"])
        switch = [entry["chronicle"] for entry in response.context["chronicle_switch"]]
        self.assertIn(self.ahp, switch)
        self.assertNotIn(self.other, switch)

    def test_line_filter_keeps_ancestors_of_matches(self):
        response = self.client.get(self.url, {"chronicle": self.ahp.pk, "line": "mta"})
        tree = response.context["location_tree"]
        self.assertEqual(self.names(tree), ["Chicago"])
        self.assertFalse(tree[0]["match"])
        node = tree[0]["children"][0]["children"][0]
        self.assertEqual(node["location"], self.node)
        self.assertTrue(node["match"])
        self.assertNotContains(response, "Sweetwater Bluff")
        counts = {entry["key"]: entry["count"] for entry in response.context["line_filter"]}
        self.assertEqual(counts, {"": 5, "wod": 3, "wta": 1, "mta": 1})

    def test_unknown_line_is_ignored(self):
        response = self.client.get(self.url, {"chronicle": self.ahp.pk, "line": "nope"})
        self.assertEqual(response.context["selected_line"], "")

    def test_containment_cycle_does_not_recurse_forever(self):
        loop_a = LocationModel.objects.create(name="Loop A", chronicle=self.ahp)
        loop_b = LocationModel.objects.create(name="Loop B", chronicle=self.ahp)
        loop_b.contained_within.add(loop_a)
        self.library.contained_within.add(loop_b)
        loop_a.contained_within.add(self.library)
        response = self.client.get(self.url, {"chronicle": self.ahp.pk})
        self.assertEqual(response.status_code, 200)

    def test_empty_chronicle(self):
        empty = Chronicle.objects.create(name="Empty")
        response = self.client.get(self.url, {"chronicle": empty.pk})
        self.assertContains(response, "No locations found for this chronicle.")


class TestGenericLocationDetailView(TestCase):
    """Test GenericLocationDetailView routing."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_invalid_location_returns_404(self):
        """Test non-existent location returns 404."""
        self.client.login(username="testuser", password="password")
        response = self.client.get("/locations/99999/")
        self.assertEqual(response.status_code, 404)

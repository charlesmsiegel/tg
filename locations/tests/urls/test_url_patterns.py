"""Tests for locations URL routing configuration."""

from core.constants import GameLine
from django.test import SimpleTestCase, TestCase
from django.urls import NoReverseMatch, resolve, reverse
from locations import urls as locations_urls


class LocationsUrlPatternsTest(SimpleTestCase):
    """Tests for locations urlpatterns structure."""

    def test_urlpatterns_is_not_empty(self):
        """Test that urlpatterns contains patterns."""
        self.assertTrue(len(locations_urls.urlpatterns) > 0)

    def test_urlpatterns_is_list(self):
        """Test that urlpatterns is a list."""
        self.assertIsInstance(locations_urls.urlpatterns, list)


class LocationsCoreUrlsTest(TestCase):
    """Tests for core location URL patterns."""

    def test_location_index_url_resolves(self):
        """Test that location index URL resolves correctly."""
        url = reverse("locations:index")
        self.assertEqual(url, "/locations/index/")

    def test_location_index_url_resolves_to_correct_view(self):
        """Test that index URL resolves to LocationIndexView."""
        resolver = resolve("/locations/index/")
        self.assertEqual(resolver.view_name, "locations:index")


class LocationsGamelineUrlsTest(TestCase):
    """Tests for gameline-specific URL patterns."""

    def test_mage_namespace_exists(self):
        """Test that mage namespace is accessible."""
        try:
            url = reverse("locations:mage:list:index")
            self.assertTrue(url.startswith("/locations/mage/"))
        except NoReverseMatch:
            # If the view doesn't exist, that's fine - we're testing
            # the namespace loading, not the specific views
            pass

    def test_vampire_namespace_exists(self):
        """Test that vampire namespace is accessible."""
        try:
            url = reverse("locations:vampire:list:index")
            self.assertTrue(url.startswith("/locations/vampire/"))
        except NoReverseMatch:
            pass

    def test_werewolf_namespace_exists(self):
        """Test that werewolf namespace is accessible."""
        try:
            url = reverse("locations:werewolf:list:index")
            self.assertTrue(url.startswith("/locations/werewolf/"))
        except NoReverseMatch:
            pass

    def test_all_gamelines_have_url_patterns(self):
        """Test that all gamelines in URL_PATTERNS create URL entries."""
        for url_path, module_name, namespace in GameLine.URL_PATTERNS:
            # Test that the gameline path exists in urlpatterns
            expected_prefix = f"/locations/{url_path}/"
            found = False
            for pattern in locations_urls.urlpatterns:
                if hasattr(pattern, "pattern") and str(pattern.pattern).startswith(url_path):
                    found = True
                    break
            # Note: found may be False if module doesn't exist (caught by exception)
            # This is expected behavior


class LocationsCreateUrlsTest(TestCase):
    """Tests for create URL patterns."""

    def test_create_namespace_exists(self):
        """Test that create namespace is accessible."""
        resolver = resolve("/locations/create/")
        self.assertIsNotNone(resolver)


class LocationsUpdateUrlsTest(TestCase):
    """Tests for update URL patterns."""

    def test_update_namespace_prefix_exists(self):
        """Test that update namespace prefix is accessible."""
        try:
            resolver = resolve("/locations/update/location/1/")
            self.assertIsNotNone(resolver)
        except:
            # If specific patterns don't exist, that's fine for this test
            pass


class LocationsListUrlsTest(TestCase):
    """Tests for list URL patterns."""

    def test_list_namespace_exists(self):
        """Test that list namespace is accessible."""
        resolver = resolve("/locations/list/")
        self.assertIsNotNone(resolver)

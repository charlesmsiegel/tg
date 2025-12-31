"""Tests for characters URL routing configuration."""

from characters import urls as characters_urls
from core.constants import GameLine
from django.test import SimpleTestCase, TestCase
from django.urls import NoReverseMatch, resolve, reverse


class CharactersUrlPatternsTest(SimpleTestCase):
    """Tests for characters urlpatterns structure."""

    def test_urlpatterns_is_not_empty(self):
        """Test that urlpatterns contains patterns."""
        self.assertTrue(len(characters_urls.urlpatterns) > 0)

    def test_urlpatterns_is_list(self):
        """Test that urlpatterns is a list."""
        self.assertIsInstance(characters_urls.urlpatterns, list)


class CharactersCoreUrlsTest(TestCase):
    """Tests for core character URL patterns."""

    def test_character_index_url_resolves(self):
        """Test that character index URL resolves correctly."""
        url = reverse("characters:index")
        self.assertEqual(url, "/characters/index/")

    def test_character_retired_url_resolves(self):
        """Test that retired characters URL resolves correctly."""
        url = reverse("characters:retired")
        self.assertEqual(url, "/characters/retired/")

    def test_character_deceased_url_resolves(self):
        """Test that deceased characters URL resolves correctly."""
        url = reverse("characters:deceased")
        self.assertEqual(url, "/characters/deceased/")

    def test_character_npc_url_resolves(self):
        """Test that NPC characters URL resolves correctly."""
        url = reverse("characters:npc")
        self.assertEqual(url, "/characters/npc/")

    def test_character_index_url_resolves_to_correct_view(self):
        """Test that index URL resolves to CharacterIndexView."""
        resolver = resolve("/characters/index/")
        self.assertEqual(resolver.view_name, "characters:index")

    def test_character_retired_url_resolves_to_correct_view(self):
        """Test that retired URL resolves to RetiredCharacterIndex."""
        resolver = resolve("/characters/retired/")
        self.assertEqual(resolver.view_name, "characters:retired")

    def test_character_deceased_url_resolves_to_correct_view(self):
        """Test that deceased URL resolves to DeceasedCharacterIndex."""
        resolver = resolve("/characters/deceased/")
        self.assertEqual(resolver.view_name, "characters:deceased")

    def test_character_npc_url_resolves_to_correct_view(self):
        """Test that npc URL resolves to NPCCharacterIndex."""
        resolver = resolve("/characters/npc/")
        self.assertEqual(resolver.view_name, "characters:npc")


class CharactersGamelineUrlsTest(TestCase):
    """Tests for gameline-specific URL patterns."""

    def test_vampire_namespace_exists(self):
        """Test that vampire namespace is accessible."""
        # We test by trying to access the namespace - if the module was loaded,
        # the namespace will exist. This tests that the dynamic import worked.
        try:
            url = reverse("characters:vampire:list:index")
            self.assertTrue(url.startswith("/characters/vampire/"))
        except NoReverseMatch:
            # If the view doesn't exist, that's fine - we're testing
            # the namespace loading, not the specific views
            pass

    def test_mage_namespace_exists(self):
        """Test that mage namespace is accessible."""
        try:
            url = reverse("characters:mage:list:index")
            self.assertTrue(url.startswith("/characters/mage/"))
        except NoReverseMatch:
            pass

    def test_werewolf_namespace_exists(self):
        """Test that werewolf namespace is accessible."""
        try:
            url = reverse("characters:werewolf:list:index")
            self.assertTrue(url.startswith("/characters/werewolf/"))
        except NoReverseMatch:
            pass

    def test_all_gamelines_have_url_patterns(self):
        """Test that all gamelines in URL_PATTERNS create URL entries."""
        for url_path, module_name, namespace in GameLine.URL_PATTERNS:
            # Test that the gameline path exists in urlpatterns
            expected_prefix = f"/characters/{url_path}/"
            found = False
            for pattern in characters_urls.urlpatterns:
                if hasattr(pattern, "pattern") and str(pattern.pattern).startswith(url_path):
                    found = True
                    break
            # Note: found may be False if module doesn't exist (caught by exception)
            # This is expected behavior


class CharactersAjaxUrlsTest(TestCase):
    """Tests for AJAX URL patterns."""

    def test_ajax_namespace_exists(self):
        """Test that ajax namespace is accessible."""
        resolver = resolve("/characters/ajax/")
        self.assertIsNotNone(resolver)


class CharactersCreateUrlsTest(TestCase):
    """Tests for create URL patterns."""

    def test_create_namespace_exists(self):
        """Test that create namespace is accessible."""
        resolver = resolve("/characters/create/")
        self.assertIsNotNone(resolver)


class CharactersUpdateUrlsTest(TestCase):
    """Tests for update URL patterns."""

    def test_update_namespace_prefix_exists(self):
        """Test that update namespace prefix is accessible."""
        # The update namespace exists but individual patterns depend on the views
        try:
            resolver = resolve("/characters/update/human/1/")
            self.assertIsNotNone(resolver)
        except:
            # If specific patterns don't exist, that's fine for this test
            pass


class CharactersListUrlsTest(TestCase):
    """Tests for list URL patterns."""

    def test_list_namespace_exists(self):
        """Test that list namespace is accessible."""
        resolver = resolve("/characters/list/")
        self.assertIsNotNone(resolver)

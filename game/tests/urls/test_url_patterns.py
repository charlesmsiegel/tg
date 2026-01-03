"""Tests for game URL routing configuration."""

from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from game import urls as game_urls


class GameUrlPatternsTest(SimpleTestCase):
    """Tests for game urlpatterns structure."""

    def test_urlpatterns_is_not_empty(self):
        """Test that urlpatterns contains patterns."""
        self.assertTrue(len(game_urls.urlpatterns) > 0)

    def test_urlpatterns_is_list(self):
        """Test that urlpatterns is a list."""
        self.assertIsInstance(game_urls.urlpatterns, list)


class GameCoreUrlsTest(TestCase):
    """Tests for core game URL patterns."""

    def test_chronicles_url_resolves(self):
        """Test that chronicles list URL resolves correctly."""
        url = reverse("game:chronicles")
        self.assertEqual(url, "/game/chronicles/")

    def test_chronicle_detail_url_has_trailing_slash(self):
        """Test that chronicle detail URL has trailing slash."""
        url = reverse("game:chronicle", kwargs={"pk": 1})
        self.assertEqual(url, "/game/chronicle/1/")
        self.assertTrue(url.endswith("/"))

    def test_scenes_url_resolves(self):
        """Test that scenes list URL resolves correctly."""
        url = reverse("game:scenes")
        self.assertEqual(url, "/game/scenes/")

    def test_scene_detail_url_has_trailing_slash(self):
        """Test that scene detail URL has trailing slash."""
        url = reverse("game:scene", kwargs={"pk": 1})
        self.assertEqual(url, "/game/scene/1/")
        self.assertTrue(url.endswith("/"))

    def test_journals_url_resolves(self):
        """Test that journals list URL resolves correctly."""
        url = reverse("game:journals")
        self.assertEqual(url, "/game/journals/")

    def test_journal_detail_url_has_trailing_slash(self):
        """Test that journal detail URL has trailing slash."""
        url = reverse("game:journal", kwargs={"pk": 1})
        self.assertEqual(url, "/game/journal/1/")
        self.assertTrue(url.endswith("/"))

    def test_commands_url_resolves(self):
        """Test that commands URL resolves correctly."""
        url = reverse("game:commands")
        self.assertEqual(url, "/game/commands/")


class GameStoryUrlsTest(TestCase):
    """Tests for story URL patterns."""

    def test_story_list_url_resolves(self):
        """Test that story list URL resolves correctly."""
        url = reverse("game:story:list")
        self.assertEqual(url, "/game/story/list/")

    def test_story_create_url_resolves(self):
        """Test that story create URL resolves correctly."""
        url = reverse("game:story:create")
        self.assertEqual(url, "/game/story/create/")

    def test_story_detail_url_resolves(self):
        """Test that story detail URL resolves correctly."""
        url = reverse("game:story:detail", kwargs={"pk": 1})
        self.assertEqual(url, "/game/story/1/")

    def test_story_update_url_resolves(self):
        """Test that story update URL resolves correctly."""
        url = reverse("game:story:update", kwargs={"pk": 1})
        self.assertEqual(url, "/game/story/1/update/")


class GameWeekUrlsTest(TestCase):
    """Tests for week URL patterns."""

    def test_week_list_url_resolves(self):
        """Test that week list URL resolves correctly."""
        url = reverse("game:week:list")
        self.assertEqual(url, "/game/week/list/")

    def test_week_create_url_resolves(self):
        """Test that week create URL resolves correctly."""
        url = reverse("game:week:create")
        self.assertEqual(url, "/game/week/create/")


class GameChronicleManageUrlsTest(TestCase):
    """Tests for chronicle management URL patterns."""

    def test_chronicle_create_url_resolves(self):
        """Test that chronicle create URL resolves correctly."""
        url = reverse("game:chronicle_manage:create")
        self.assertEqual(url, "/game/chronicle-manage/create/")

    def test_chronicle_update_url_resolves(self):
        """Test that chronicle update URL resolves correctly."""
        url = reverse("game:chronicle_manage:update", kwargs={"pk": 1})
        self.assertEqual(url, "/game/chronicle-manage/1/update/")


class GameSceneManageUrlsTest(TestCase):
    """Tests for scene management URL patterns."""

    def test_scene_create_url_resolves(self):
        """Test that scene create URL resolves correctly."""
        url = reverse("game:scene_manage:create")
        self.assertEqual(url, "/game/scene-manage/create/")

    def test_scene_update_url_resolves(self):
        """Test that scene update URL resolves correctly."""
        url = reverse("game:scene_manage:update", kwargs={"pk": 1})
        self.assertEqual(url, "/game/scene-manage/1/update/")

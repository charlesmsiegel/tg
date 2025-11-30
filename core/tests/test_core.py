import os
import time
from collections import Counter
from unittest import mock
from unittest.mock import Mock

from characters.models.core import CharacterModel, Human
from core.models import Language, NewsItem
from core.templatetags.dots import dots
from core.utils import dice, filepath
from django.contrib.auth.models import User
from django.test import LiveServerTestCase, TestCase
from django.utils.timezone import now
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

os.environ["MOZ_HEADLESS"] = "1"

MAX_WAIT = 10


class FunctionalTest(LiveServerTestCase):
    """Base case for Functional Tests"""

    def setUp(self) -> None:
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element("id", "id_character_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as exception:
                if time.time() - start_time > MAX_WAIT:
                    raise exception
                time.sleep(0.5)

    def clean_url(self, url):
        return url.replace(self.live_server_url + "/", "")


class TestHomeListView(TestCase):
    """Manages Tests for the HomeListView and Template"""

    def setUp(self) -> None:
        User.objects.create_user("Test User", "test@user.com", "testpass")
        User.objects.create_superuser("Test Admin", "admin@admin.com", "testadmin")

    def test_home_status_code(self):
        """Tests that the page exists"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_template(self):
        """Tests that the correct template is loaded"""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "core/index.html")

    def test_includes_patreon(self):
        """Tests site contains link to Patreon"""
        response = self.client.get("/")
        self.assertContains(response, "Patron")
        self.assertContains(response, "https://www.patreon.com/bePatron?u=62722820")

    def test_includes_storytellers_vault(self):
        """Tests site contains Stoyteller's Vault logo"""
        response = self.client.get("/")
        self.assertContains(response, "Storyteller's Vault")
        self.assertContains(response, "stv.png")

    def test_includes_dark_pack(self):
        """Tests site contains Dark Pack Logo"""
        response = self.client.get("/")
        self.assertContains(response, "Dark Pack")
        self.assertContains(response, "dark_pack.png")

        self.assertTemplateUsed(response, "core/index.html")

    def test_content_null_user(self):
        """Tests what users who are not logged in see on front page"""
        response = self.client.get("/")
        self.assertContains(response, "Tellurium Games")
        self.assertContains(response, "navbar")
        self.assertContains(response, "Log In")
        self.assertContains(response, "Sign Up")

    def test_content_logged_in(self):
        """Tests what logged in users see"""
        self.client.login(username="Test User", password="testpass")
        response = self.client.get("/")
        self.assertContains(response, "Tellurium Games")
        self.assertContains(response, "navbar")
        self.assertContains(response, "Log Out")
        self.assertContains(response, "Account")

    def test_content_staff(self):
        """Tests what admins see"""
        self.client.login(username="Test Admin", password="testadmin")
        response = self.client.get("/")
        self.assertContains(response, "Tellurium Games")
        self.assertContains(response, "navbar")
        self.assertContains(response, "Log Out")
        self.assertContains(response, "Admin")
        self.assertContains(response, "Account")


class NewUserTest(FunctionalTest):
    """Test creating a new user with interface"""

    def test_homepage_has_login(self):
        self.browser.get(self.live_server_url)
        links = self.browser.find_elements("tag name", "a")
        links = [
            (self.clean_url(link.get_attribute("href")), link.text) for link in links
        ]

        self.assertIn(("accounts/login/", ""), links)
        self.assertIn(("accounts/signup/", ""), links)

    def credential_creation_fail(self):
        self.browser.get(self.live_server_url + "/accounts/signup/")
        namebox = self.browser.find_element("id", "id_username")
        namebox.send_keys("test_user")
        pw1 = self.browser.find_element("id", "id_password1")
        pw1.send_keys("pw123456")
        pw2 = self.browser.find_element("id", "id_password2")
        pw2.send_keys("pw123454")
        submit_button = self.browser.find_element("id", "signup_button")
        submit_button.click()

    def credential_creation_succeed(self, username, password):
        self.browser.get(self.live_server_url + "/accounts/signup/")
        namebox = self.browser.find_element("id", "id_username")
        namebox.send_keys(username)
        pw1 = self.browser.find_element("id", "id_password1")
        pw1.send_keys(password)
        pw2 = self.browser.find_element("id", "id_password2")
        pw2.send_keys(password)
        submit_button = self.browser.find_element("id", "signup_button")
        submit_button.click()

    def test_create_account(self):

        self.browser.get(self.live_server_url)

        self.client.get("/accounts/signup/")
        self.assertTemplateUsed(
            self.client.get("/accounts/signup/"), "accounts/signup.html"
        )

        self.credential_creation_fail()

        username = "test_user"
        password = "pw123456"

        self.credential_creation_succeed(username, password)
        self.assertEqual(User.objects.count(), 1)

        self.browser.get(self.live_server_url + "/accounts/login/")
        namebox = self.browser.find_element("id", "id_username")
        namebox.send_keys(username)
        pw1 = self.browser.find_element("id", "id_password")
        pw1.send_keys(password)
        submit_button = self.browser.find_element("id", "login_button_id")
        submit_button.click()

        links = self.browser.find_elements("tag name", "a")
        links = [
            (self.clean_url(link.get_attribute("href")), link.text) for link in links
        ]


class TestHomepage(FunctionalTest):
    """Test seeing the appropriate content on Homepage"""

    def test_homepage_structure(self):
        self.browser.get(self.live_server_url)

        self.assertIn("Tellurium Games", self.browser.title)

        links = self.browser.find_elements("tag name", "a")
        links = [
            (self.clean_url(link.get_attribute("href")), link.text) for link in links
        ]

        self.assertIn(("accounts/login/", ""), links)
        self.assertIn(("accounts/signup/", ""), links)


class TestModel(TestCase):
    def setUp(self):
        # Use skip_validation to allow empty name for testing has_name/set_name methods
        self.model = CharacterModel(name="")
        self.model.save(skip_validation=True)
        self.user = User.objects.create_user(username="Test User")

    def test_has_name(self):
        self.assertFalse(self.model.has_name())
        self.model.set_name("Test")
        self.assertTrue(self.model.has_name())

    def test_set_name(self):
        self.assertFalse(self.model.has_name())
        self.assertTrue(self.model.set_name("Test"))
        self.assertTrue(self.model.has_name())

    def test_has_description(self):
        self.assertFalse(self.model.has_description())
        self.model.set_description("Test")
        self.assertTrue(self.model.has_description())

    def test_set_description(self):
        self.assertFalse(self.model.has_description())
        self.assertTrue(self.model.set_description("Test"))
        self.assertTrue(self.model.has_description())

    def test_has_owner(self):
        self.assertFalse(self.model.has_owner())
        self.model.set_owner(self.user)
        self.assertTrue(self.model.has_owner())

    def test_set_owner(self):
        self.assertFalse(self.model.has_owner())
        self.assertTrue(self.model.set_owner(self.user))
        self.assertTrue(self.model.has_owner())

    def test_update_status(self):
        self.assertEqual(self.model.status, "Un")
        self.assertEqual(self.model.get_status_display(), "Unapproved")
        self.assertTrue(self.model.update_status("App"))
        self.assertEqual(self.model.status, "App")
        self.assertEqual(self.model.get_status_display(), "Approved")

    def test_toggle_display(self):
        self.assertTrue(self.model.display)
        self.assertTrue(self.model.toggle_display())
        self.assertFalse(self.model.display)

    def test_has_source(self):
        self.assertFalse(self.model.has_source())
        self.model.add_source("Test Book", 1)
        self.assertTrue(self.model.has_source())

    def test_add_source(self):
        self.assertFalse(self.model.has_source())
        self.assertTrue(self.model.add_source("Test Book", 1))
        self.assertTrue(self.model.has_source())

    def test_get_gameline(self):
        m = Human.objects.create(name="Test Human from WoD")
        self.assertEqual(m.get_gameline(), "wod")


class TestDots(TestCase):
    def test_length(self):
        output_5 = dots(4)
        output_10 = dots(4, maximum=10)
        output_10_2 = dots(6)
        self.assertEqual(len(output_5), 5)
        self.assertEqual(len(output_10), 10)
        self.assertEqual(len(output_10_2), 10)

    def test_correct_ratio(self):
        self.assertEqual(Counter(dots(3))["●"], 3)
        self.assertEqual(Counter(dots(3))["○"], 2)
        self.assertEqual(Counter(dots(3, maximum=10))["●"], 3)
        self.assertEqual(Counter(dots(3, maximum=10))["○"], 7)
        self.assertEqual(Counter(dots(6))["●"], 6)
        self.assertEqual(Counter(dots(6))["○"], 4)


class TestDice(TestCase):
    """Manage tests for Diceroller"""

    def test_botch(self):
        mocker = Mock()
        mocker.side_effect = [1, 1, 3, 4, 5]
        with mock.patch("random.randint", mocker):
            _, successes = dice(5)
            self.assertEqual(successes, -2)

    def test_failure_with_1s(self):
        mocker = Mock()
        mocker.side_effect = [1, 1, 7, 4, 5]
        with mock.patch("random.randint", mocker):
            _, successes = dice(5)
            self.assertEqual(successes, 0)

    def test_failure(self):
        mocker = Mock()
        mocker.side_effect = [4, 2, 3, 4, 5]
        with mock.patch("random.randint", mocker):
            _, successes = dice(5)
            self.assertEqual(successes, 0)

    def test_success(self):
        mocker = Mock()
        mocker.side_effect = [6, 7, 3, 4, 5]
        with mock.patch("random.randint", mocker):
            _, successes = dice(5)
            self.assertEqual(successes, 2)

    def test_specialty(self):
        mocker = Mock()
        mocker.side_effect = [10, 10, 3, 6, 5]
        with mock.patch("random.randint", mocker):
            _, successes = dice(5, specialty=True)
            self.assertEqual(successes, 5)

    def test_difficulty(self):
        mocker = Mock()
        mocker.side_effect = [4, 2, 3, 4, 5]
        with mock.patch("random.randint", mocker):
            _, successes = dice(5, difficulty=5)
            self.assertEqual(successes, 1)


class TestNewsItemDetailView(TestCase):
    def setUp(self) -> None:
        self.news = NewsItem.objects.create(title="Test NewsItem", date=now())
        self.url = self.news.get_absolute_url()

    def test_newsitem_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_newsitem_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "core/newsitem/detail.html")


class TestNewsItemCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "title": "Test News",
            "content": "News Test Content.",
        }
        self.url = NewsItem.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "core/newsitem/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(NewsItem.objects.count(), 1)
        self.assertEqual(NewsItem.objects.first().title, "Test News")


class TestNewsItemUpdateView(TestCase):
    def setUp(self):
        self.newsitem = NewsItem.objects.create(
            title="Test Title",
            content="Test Content",
        )
        self.valid_data = {
            "title": "Test News 2",
            "content": "News Test Content 2.",
            "date": now(),
        }
        self.url = self.newsitem.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "core/newsitem/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.newsitem.refresh_from_db()
        self.assertEqual(self.newsitem.title, "Test News 2")
        self.assertEqual(self.newsitem.content, "News Test Content 2.")


class TestLanguageDetailView(TestCase):
    def setUp(self) -> None:
        self.language = Language.objects.create(name="Test Language")
        self.url = self.language.get_absolute_url()

    def test_location_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_location_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "core/language/detail.html")


class TestLanguageCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Language",
            "frequency": 1,
        }
        self.url = Language.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "core/language/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(Language.objects.first().name, "Test Language")


class TestLanguageUpdateView(TestCase):
    def setUp(self):
        self.language = Language.objects.create(
            name="Languge",
            frequency=2,
        )
        self.valid_data = {
            "name": "Test Language",
            "frequency": 1,
        }
        self.url = self.language.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "core/language/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.language.refresh_from_db()
        self.assertEqual(self.language.name, "Test Language")
        self.assertEqual(self.language.frequency, 1)


class TestFilePath(TestCase):
    def test_filepath_parsing(self):
        m = Human.objects.create(name="Test Human")
        self.assertEqual(
            filepath(m, "test.jpg"),
            "characters/core/human/human/test_human.jpg",
        )

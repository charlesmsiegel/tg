from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.mage.faction import MageFaction
from game.models import Chronicle
from items.models.mage.grimoire import Grimoire
from locations.models.mage.library import Library


class TestLibrary(TestCase):
    def setUp(self):
        self.grimoire_1 = Grimoire.objects.create(name="Grimoire 1", rank=1)
        self.grimoire_2 = Grimoire.objects.create(name="Grimoire 2", rank=2)
        self.grimoire_3 = Grimoire.objects.create(name="Grimoire 3", rank=3)
        self.grimoire_4 = Grimoire.objects.create(name="Grimoire 4", rank=4)
        self.grimoire_5 = Grimoire.objects.create(name="Grimoire 5", rank=5)
        self.library = Library.objects.create(name="Test Library")

    def test_set_rank(self):
        self.assertEqual(self.library.rank, 1)
        self.assertTrue(self.library.set_rank(3))
        self.assertEqual(self.library.rank, 3)

    def test_add_book(self):
        g = Grimoire.objects.create(name="Book To Add")
        count = self.library.num_books()
        self.assertTrue(self.library.add_book(g))
        self.assertEqual(self.library.num_books(), count + 1)

    def test_set_faction(self):
        faction = MageFaction.objects.create(name="Test Faction")
        self.assertFalse(self.library.has_faction())
        self.assertTrue(self.library.set_faction(faction))
        self.assertTrue(self.library.has_faction())

    def test_has_faction(self):
        faction = MageFaction.objects.create(name="Test Faction")
        self.assertFalse(self.library.has_faction())
        self.library.set_faction(faction)
        self.assertTrue(self.library.has_faction())

    def test_has_books(self):
        self.library.rank = 3
        self.assertEqual(self.library.books.count(), 0)
        self.library.books.add(self.grimoire_1)
        self.library.books.add(self.grimoire_2)
        self.library.books.add(self.grimoire_3)
        self.assertEqual(self.library.books.count(), 3)

    def test_num_books(self):
        self.assertEqual(self.library.num_books(), 0)
        self.library.rank = 3
        self.library.books.add(self.grimoire_1)
        self.assertEqual(self.library.num_books(), 1)
        self.library.books.add(self.grimoire_2)
        self.assertEqual(self.library.num_books(), 2)
        self.library.books.add(self.grimoire_3)
        self.assertEqual(self.library.num_books(), 3)

    def test_library_type(self):
        """Test library type is correctly set."""
        self.assertEqual(self.library.type, "library")

    def test_library_gameline(self):
        """Test library gameline is mta."""
        self.assertEqual(self.library.gameline, "mta")

    def test_get_heading(self):
        """Test get_heading returns mta_heading."""
        self.assertEqual(self.library.get_heading(), "mta_heading")


class TestLibraryIncreaseRank(TestCase):
    """Test Library increase_rank method."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.library = Library.objects.create(name="Test Library", rank=1, owner=self.user)

    def test_increase_rank_with_new_book(self):
        """Test increase_rank with a new book adds that book."""
        new_grimoire = Grimoire.objects.create(name="New Book", rank=1)
        initial_rank = self.library.rank
        self.library.increase_rank(book=new_grimoire)
        self.assertEqual(self.library.rank, initial_rank + 1)
        self.assertIn(new_grimoire, self.library.books.all())


class TestLibraryDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.library = Library.objects.create(
            name="Test Library",
            owner=self.user,
            status="App",
        )
        self.url = self.library.get_absolute_url()

    def test_library_detail_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_library_detail_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/library/detail.html")


class TestLibraryCreateView(TestCase):
    """Test Library create view GET requests.

    Note: POST tests require complex form data and create Grimoire objects
    which is beyond the scope of basic CRUD view tests. GET tests verify accessibility.
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.url = Library.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/library/form.html")


class TestLibraryUpdateView(TestCase):
    """Test Library update view GET requests.

    Note: POST tests require complex form data and create Grimoire objects
    which is beyond the scope of basic CRUD view tests. GET tests verify accessibility.
    """

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.library = Library.objects.create(
            name="Test Library",
            description="Test description",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )
        self.url = self.library.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/library/form.html")

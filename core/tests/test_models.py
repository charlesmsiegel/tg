"""
Tests for core models.

Tests cover:
- Book model creation and methods
- HouseRule model and chronicle association
- Language model CRUD operations
- NewsItem model ordering and display
"""

from core.models import Book, HouseRule, Language, NewsItem
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now
from game.models import Chronicle


class TestBook(TestCase):
    """Test the Book model."""

    def setUp(self):
        self.book = Book.objects.create(
            name="Mage: The Ascension 20th Anniversary Edition",
            abbreviation="M20",
        )

    def test_book_creation(self):
        """Test that books are created correctly."""
        self.assertEqual(self.book.name, "Mage: The Ascension 20th Anniversary Edition")
        self.assertEqual(self.book.abbreviation, "M20")

    def test_book_str_representation(self):
        """Test the string representation of a book."""
        self.assertEqual(str(self.book), "Mage: The Ascension 20th Anniversary Edition")

    def test_book_absolute_url(self):
        """Test that get_absolute_url returns the correct path."""
        expected_url = f"/books/{self.book.id}/"
        self.assertEqual(self.book.get_absolute_url(), expected_url)

    def test_book_update_url(self):
        """Test that get_update_url returns the correct path."""
        expected_url = f"/books/{self.book.id}/update/"
        self.assertEqual(self.book.get_update_url(), expected_url)


class TestHouseRule(TestCase):
    """Test the HouseRule model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.houserule = HouseRule.objects.create(
            name="XP Costs Modified",
            description="All XP costs are reduced by 1",
            chronicle=self.chronicle,
            owner=self.user,
        )

    def test_houserule_creation(self):
        """Test that house rules are created correctly."""
        self.assertEqual(self.houserule.name, "XP Costs Modified")
        self.assertEqual(self.houserule.description, "All XP costs are reduced by 1")
        self.assertEqual(self.houserule.chronicle, self.chronicle)
        self.assertEqual(self.houserule.owner, self.user)

    def test_houserule_str_representation(self):
        """Test the string representation of a house rule."""
        self.assertEqual(str(self.houserule), "XP Costs Modified")

    def test_houserule_absolute_url(self):
        """Test that get_absolute_url returns the correct path."""
        expected_url = f"/houserules/{self.houserule.id}/"
        self.assertEqual(self.houserule.get_absolute_url(), expected_url)

    def test_houserule_without_chronicle(self):
        """Test creating a house rule without a chronicle."""
        global_rule = HouseRule.objects.create(
            name="Global Rule",
            description="Applies to all chronicles",
            owner=self.user,
        )
        self.assertIsNone(global_rule.chronicle)


class TestLanguage(TestCase):
    """Test the Language model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.language = Language.objects.create(
            name="Ancient Greek",
            owner=self.user,
        )

    def test_language_creation(self):
        """Test that languages are created correctly."""
        self.assertEqual(self.language.name, "Ancient Greek")
        self.assertEqual(self.language.owner, self.user)

    def test_language_str_representation(self):
        """Test the string representation of a language."""
        self.assertEqual(str(self.language), "Ancient Greek")

    def test_language_absolute_url(self):
        """Test that get_absolute_url returns the correct path."""
        expected_url = f"/languages/{self.language.id}/"
        self.assertEqual(self.language.get_absolute_url(), expected_url)


class TestNewsItem(TestCase):
    """Test the NewsItem model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_newsitem_creation(self):
        """Test that news items are created correctly."""
        newsitem = NewsItem.objects.create(
            headline="Site Update",
            content="New features added!",
            author=self.user,
        )
        self.assertEqual(newsitem.headline, "Site Update")
        self.assertEqual(newsitem.content, "New features added!")
        self.assertEqual(newsitem.author, self.user)
        self.assertIsNotNone(newsitem.created_date)
        self.assertIsNotNone(newsitem.updated_date)

    def test_newsitem_str_representation(self):
        """Test the string representation of a news item."""
        newsitem = NewsItem.objects.create(
            headline="Test Headline",
            content="Test content",
            author=self.user,
        )
        self.assertEqual(str(newsitem), "Test Headline")

    def test_newsitem_ordering(self):
        """Test that news items are ordered by created date descending."""
        newsitem1 = NewsItem.objects.create(
            headline="Older News",
            content="Old content",
            author=self.user,
        )
        newsitem2 = NewsItem.objects.create(
            headline="Newer News",
            content="New content",
            author=self.user,
        )
        news_list = list(NewsItem.objects.all())
        # Newer items should come first
        self.assertEqual(news_list[0], newsitem2)
        self.assertEqual(news_list[1], newsitem1)

    def test_newsitem_absolute_url(self):
        """Test that get_absolute_url returns the correct path."""
        newsitem = NewsItem.objects.create(
            headline="Test",
            content="Test content",
            author=self.user,
        )
        expected_url = f"/newsitems/{newsitem.id}/"
        self.assertEqual(newsitem.get_absolute_url(), expected_url)

"""Tests for Guild model."""

from characters.models.wraith.guild import Guild
from django.test import TestCase


class TestGuildModel(TestCase):
    """Tests for Guild model creation and attributes."""

    def test_guild_creation(self):
        """Guild can be created with basic attributes."""
        guild = Guild.objects.create(
            name="Masquers",
            guild_type="greater",
            willpower=6,
            description="Masters of disguise and illusion.",
        )
        self.assertEqual(guild.name, "Masquers")
        self.assertEqual(guild.guild_type, "greater")
        self.assertEqual(guild.willpower, 6)

    def test_guild_default_values(self):
        """Guild has correct default values."""
        guild = Guild.objects.create(
            name="Test Guild",
            description="Test description",
        )
        self.assertEqual(guild.guild_type, "greater")
        self.assertEqual(guild.willpower, 5)

    def test_guild_type_choices(self):
        """Guild can have greater, lesser, or banned type."""
        greater = Guild.objects.create(
            name="Greater Guild",
            guild_type="greater",
            description="Greater guild",
        )
        lesser = Guild.objects.create(
            name="Lesser Guild",
            guild_type="lesser",
            description="Lesser guild",
        )
        banned = Guild.objects.create(
            name="Banned Guild",
            guild_type="banned",
            description="Banned guild",
        )
        self.assertEqual(greater.guild_type, "greater")
        self.assertEqual(lesser.guild_type, "lesser")
        self.assertEqual(banned.guild_type, "banned")

    def test_guild_gameline(self):
        """Guild has correct gameline."""
        guild = Guild.objects.create(name="Test", description="Test")
        self.assertEqual(guild.gameline, "wto")

    def test_guild_type_attribute(self):
        """Guild has correct type attribute."""
        guild = Guild.objects.create(name="Test", description="Test")
        self.assertEqual(guild.type, "guild")


class TestGuildUrls(TestCase):
    """Tests for Guild URL methods."""

    def setUp(self):
        self.guild = Guild.objects.create(
            name="Test Guild",
            description="Test description",
        )

    def test_get_absolute_url_method_exists(self):
        """Guild has get_absolute_url method."""
        self.assertTrue(hasattr(self.guild, "get_absolute_url"))
        self.assertTrue(callable(getattr(self.guild, "get_absolute_url")))

    def test_get_update_url_method_exists(self):
        """Guild has get_update_url method."""
        self.assertTrue(hasattr(self.guild, "get_update_url"))
        self.assertTrue(callable(getattr(self.guild, "get_update_url")))

    def test_get_creation_url_method_exists(self):
        """Guild has get_creation_url class method."""
        self.assertTrue(hasattr(Guild, "get_creation_url"))
        self.assertTrue(callable(getattr(Guild, "get_creation_url")))

    def test_get_heading(self):
        """Guild returns correct heading class."""
        self.assertEqual(self.guild.get_heading(), "wto_heading")


class TestGuildMetaOptions(TestCase):
    """Tests for Guild Meta options."""

    def test_verbose_name(self):
        """Guild has correct verbose_name."""
        self.assertEqual(Guild._meta.verbose_name, "Guild")

    def test_verbose_name_plural(self):
        """Guild has correct verbose_name_plural."""
        self.assertEqual(Guild._meta.verbose_name_plural, "Guilds")


class TestGuildStr(TestCase):
    """Tests for Guild string representation."""

    def test_guild_str(self):
        """Guild uses name for string representation."""
        guild = Guild.objects.create(
            name="Haunters",
            description="Masters of fear",
        )
        self.assertEqual(str(guild), "Haunters")

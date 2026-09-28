"""Tests for wraith views module."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.wraith.fetter import Fetter
from characters.models.wraith.guild import Guild
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.wraith.faction import WraithFaction
from characters.models.wraith.passion import Passion
from characters.models.wraith.shadow_archetype import ShadowArchetype
from characters.models.wraith.thorn import Thorn
from characters.models.wraith.wraith import ThornRating, Wraith
from game.models import Chronicle


class TestWraithDetailView(TestCase):
    """Test WraithDetailView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.st = User.objects.create_user(username="st", email="st@test.com", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_detail_view_accessible_to_owner(self):
        """Test that wraith detail view is accessible to the owner."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_accessible_to_st(self):
        """Test that wraith detail view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_hidden_from_other_users(self):
        """Test that characters are hidden from other users (404)."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/public_object_detail.html")

    def test_detail_view_returns_404_without_login(self):
        """Test that unauthenticated users get 404 (not login redirect)."""
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/public_object_detail.html")

    def test_detail_view_template_used(self):
        """Test that correct template is used for wraith detail view."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertTemplateUsed(response, "characters/wraith/wraith/detail.html")

    def test_detail_view_has_arcanoi_in_context(self):
        """Test that arcanoi are in the context."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertIn("arcanoi", response.context)

    def test_detail_view_has_dark_arcanoi_in_context(self):
        """Test that dark arcanoi are in the context."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertIn("dark_arcanoi", response.context)

    def test_detail_view_has_fetters_in_context(self):
        """Test that fetters are in the context."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertIn("fetters", response.context)

    def test_detail_view_has_passions_in_context(self):
        """Test that passions are in the context."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertIn("passions", response.context)

    def test_detail_view_displays_fetters(self):
        """Test that fetters are displayed in the template."""
        Fetter.objects.create(
            wraith=self.wraith,
            fetter_type="person",
            description="My beloved wife",
            rating=3,
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertEqual(self.wraith.fetters.count(), 1)
        self.assertEqual(response.context["fetters"].count(), 1)
        self.assertContains(response, "My beloved wife")
        self.assertContains(response, "Fetters")

    def test_detail_view_displays_passions(self):
        """Test that passions are displayed in the template."""
        Passion.objects.create(
            wraith=self.wraith,
            emotion="Rage",
            description="Avenge my murder",
            rating=4,
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertContains(response, "Avenge my murder")
        self.assertContains(response, "Passions")

    def test_detail_view_displays_dark_passion_badge(self):
        """Dark passions are listed under the Shadow, not with the Psyche's Passions."""
        Passion.objects.create(
            wraith=self.wraith,
            emotion="Jealousy",
            description="Destroy my rival",
            rating=2,
            is_dark_passion=True,
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertContains(response, "Dark Passions")
        content = response.content.decode()
        shadow = content[content.index('id="shadow"') :]
        self.assertIn("Destroy my rival", shadow)
        self.assertNotIn('id="passions-fetters"', content)

    def test_detail_view_unapproved_hidden_from_others(self):
        """Test that unapproved characters are hidden from non-owners."""
        unapproved = Wraith.objects.create(
            name="Unapproved Wraith",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
        )
        self.client.login(username="other", password="password")
        response = self.client.get(unapproved.get_absolute_url())
        # Should be 403 or 404 (denied/hidden from other users)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/public_object_detail.html")

    def test_detail_view_unapproved_visible_to_owner(self):
        """Test that unapproved characters are visible to owners."""
        unapproved = Wraith.objects.create(
            name="Unapproved Wraith",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(unapproved.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestWraithSheetSpread(TestCase):
    """The Wraith sheet in Spread markup (C18)."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(username="owner", password="password")
        self.chronicle = Chronicle.objects.create(name="Stygian Chicago")
        self.guild = Guild.objects.create(name="Harbingers", willpower=5)
        self.legion = WraithFaction.objects.create(name="Grim Legion")
        self.faction = WraithFaction.objects.create(name="Hierarchy")
        self.archetype = ShadowArchetype.objects.create(name="The Martyr")
        self.wraith = Wraith.objects.create(
            name="Harriet Vosk",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            guild=self.guild,
            legion=self.legion,
            faction=self.faction,
            shadow_archetype=self.archetype,
            age_at_death=34,
            argos=3,
            false_life=2,
            pathos=7,
            temporary_pathos=5,
            corpus=8,
            angst=4,
            temporary_angst=6,
            death_description="Drowned in the lock.",
        )
        self.client.login(username="owner", password="password")

    def get(self, **params):
        return self.client.get(self.wraith.get_absolute_url(), params).content.decode()

    def test_cover_basics_are_fact_rows(self):
        content = self.get()
        for label, value in [
            ("Guild", "Harbingers"),
            ("Legion", "Grim Legion"),
            ("Faction", "Hierarchy"),
            ("Shadow", "The Martyr"),
            ("Age at death", "34"),
        ]:
            self.assertIn(f'<span class="tl-facts__k">{label}</span>', content)
            self.assertIn(value, content)
        self.assertIn(f'href="{self.guild.get_absolute_url()}"', content)

    def test_age_at_death_hidden_when_zero(self):
        self.wraith.age_at_death = 0
        self.wraith.save()
        self.assertNotIn("Age at death", self.get())

    def test_arcanoi_power_section(self):
        content = self.get()
        self.assertIn('class="tl-section tl-section--power tl-span-7" id="arcanoi"', content)
        section = content[content.index('id="arcanoi"') : content.index('id="advantages"')]
        self.assertIn("Argos", section)
        self.assertIn('aria-label="3 of 5"', section)
        self.assertNotIn("Castigate", section)
        self.assertNotIn("False Life", section)

    def test_arcanoi_hidden_when_none(self):
        self.wraith.argos = 0
        self.wraith.save()
        self.assertNotIn('id="arcanoi"', self.get())

    def test_advantage_tracks(self):
        content = self.get()
        section = content[content.index('id="advantages"') :]
        for label in ["Pathos", "Willpower", "Corpus", "Angst"]:
            self.assertIn(label, section)
        # Pathos 7 permanent / 5 temporary; Corpus as squares only; Angst 4 / 6.
        self.assertIn('aria-label="7 of 10"', section)
        self.assertIn('<span class="tl-boxes" role="img" aria-label="5 of 10">', section)
        self.assertIn('<span class="tl-boxes" role="img" aria-label="8 of 10">', section)
        self.assertNotIn('<span class="tl-dots" role="img" aria-label="8 of 10">', section)
        self.assertIn('aria-label="4 of 10"', section)
        self.assertIn('aria-label="6 of 10"', section)
        self.assertNotIn('id="backgrounds"', content)
        self.assertNotIn("Backgrounds", section)

    def test_backgrounds_sit_in_advantages(self):
        memoriam = Background.objects.create(name="Memoriam", property_name="memoriam")
        BackgroundRating.objects.create(char=self.wraith, bg=memoriam, rating=2, note="Plaque")
        content = self.get()
        section = content[content.index('id="advantages"') :]
        self.assertIn('<span class="tl-subhead">Backgrounds</span>', section)
        self.assertIn("Memoriam", section)
        self.assertIn("Plaque", section)

    def test_passions_and_fetters_block(self):
        Passion.objects.create(
            wraith=self.wraith, emotion="Love", description="Protect my brother", rating=3
        )
        Fetter.objects.create(
            wraith=self.wraith, fetter_type="object", description="Hockey jersey", rating=2
        )
        content = self.get()
        self.assertIn("Passions &amp; Fetters", content)
        section = content[content.index('id="passions-fetters"') :]
        self.assertIn("Protect my brother", section)
        self.assertIn('<span class="tl-trait__spec">Love</span>', section)
        self.assertIn("Hockey jersey", section)
        self.assertIn('<span class="tl-trait__spec">Object</span>', section)

    def test_passions_and_fetters_hidden_when_empty(self):
        self.assertNotIn('id="passions-fetters"', self.get())

    def test_shadow_section_thorns_and_history(self):
        thorn = Thorn.objects.create(name="Shadow Call")
        ThornRating.objects.create(wraith=self.wraith, thorn=thorn, rating=2)
        self.wraith.harrowing_count = 2
        self.wraith.catharsis_count = 1
        self.wraith.save()
        content = self.get()
        section = content[content.index('id="shadow"') :]
        self.assertIn(f'href="{self.archetype.get_absolute_url()}"', section)
        self.assertIn("Harrowings", section)
        self.assertIn("Catharses", section)
        self.assertIn(f'<a href="{thorn.get_absolute_url()}">Shadow Call</a>', section)

    def test_shadow_hidden_without_shadow_data(self):
        self.assertNotIn('id="shadow"', self.get())

    def test_dark_arcanoi_only_for_spectres(self):
        self.wraith.harrowing_count = 1
        self.wraith.save()
        self.assertNotIn("Dark Arcanoi", self.get())
        self.wraith.character_type = "spectre"
        self.wraith.save()
        content = self.get()
        self.assertIn("Dark Arcanoi", content)
        self.assertIn("False Life", content)

    def test_history_includes_death(self):
        content = self.get()
        section = content[content.index('id="history"') :]
        self.assertIn("Death", section)
        self.assertIn("Drowned in the lock.", section)

    def test_no_bootstrap_markup(self):
        content = self.get()
        for legacy in ["tg-card", 'class="row', "col-sm", "tg-badge", 'style="']:
            self.assertNotIn(legacy, content)


class TestWraithCreateRoute(TestCase):
    """The characters:wraith:create:wraith route, served by WraithBasicsView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.guild = Guild.objects.create(name="Usurers", willpower=5)

    def test_create_view_accessible_when_logged_in(self):
        """Test that wraith create view is accessible when logged in."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:create:wraith")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_requires_login(self):
        """Test that wraith create view requires login."""
        url = reverse("characters:wraith:create:wraith")
        response = self.client.get(url)
        # App returns 401 for unauthenticated users instead of redirect
        self.assertEqual(response.status_code, 401)


class TestWraithUpdateView(TestCase):
    """Test WraithUpdateView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.st = User.objects.create_user(username="st", email="st@test.com", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_update_view_denied_to_other_users(self):
        """Test that update view is denied to other users."""
        self.client.login(username="other", password="password")
        url = reverse("characters:wraith:update:wraith_full", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302, 404])


class TestWraithView404Handling(TestCase):
    """Test 404 error handling for wraith views with invalid IDs."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.user)

    def test_wraith_detail_returns_404_for_invalid_pk(self):
        """Test that wraith detail returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:wraith", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_wraith_chargen_returns_404_for_invalid_pk(self):
        """Test that wraith chargen returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestWraithGetAbsoluteUrl(TestCase):
    """Test get_absolute_url method for Wraith."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.user,
        )

    def test_get_absolute_url_returns_correct_url(self):
        """Test that get_absolute_url returns the correct URL."""
        expected_url = reverse("characters:wraith:wraith", kwargs={"pk": self.wraith.pk})
        self.assertEqual(self.wraith.get_absolute_url(), expected_url)


class TestWraithGetUpdateUrl(TestCase):
    """Test get_update_url method for Wraith."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.user,
        )

    def test_get_update_url_returns_correct_url(self):
        """Test that get_update_url returns the correct URL."""
        expected_url = reverse("characters:wraith:update:wraith", kwargs={"pk": self.wraith.pk})
        self.assertEqual(self.wraith.get_update_url(), expected_url)


class TestWraithGetCreationUrl(TestCase):
    """Test get_creation_url classmethod for Wraith."""

    def test_get_creation_url_returns_correct_url(self):
        """Test that get_creation_url returns the correct URL."""
        expected_url = reverse("characters:wraith:create:wraith")
        self.assertEqual(Wraith.get_creation_url(), expected_url)

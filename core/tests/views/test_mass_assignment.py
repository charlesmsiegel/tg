"""
Security tests for mass assignment vulnerability (Issue #1345).

These tests verify that views with explicit field whitelists properly
reject attempts to modify fields not included in the whitelist.
"""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.core.human import Human
from characters.models.mage.companion import Companion
from core.models import Language, NewsItem
from game.models import Chronicle, Gameline, STRelationship
from items.models.core import Material, Medium


class TestMaterialMassAssignment(TestCase):
    """Test that Material views only accept whitelisted fields."""

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.create_user("material_staff", is_staff=True))
        self.material = Material.objects.create(name="Test Material", is_hard=True)

    def test_create_accepts_whitelisted_fields(self):
        """Test that create view accepts name and is_hard fields."""
        url = reverse("items:create:material")
        response = self.client.post(url, {"name": "New Material", "is_hard": False})
        self.assertEqual(response.status_code, 302)
        material = Material.objects.get(name="New Material")
        self.assertEqual(material.is_hard, False)

    def test_update_accepts_whitelisted_fields(self):
        """Test that update view accepts name and is_hard fields."""
        url = reverse("items:update:material", kwargs={"pk": self.material.pk})
        response = self.client.post(url, {"name": "Updated Material", "is_hard": False})
        self.assertEqual(response.status_code, 302)
        self.material.refresh_from_db()
        self.assertEqual(self.material.name, "Updated Material")
        self.assertEqual(self.material.is_hard, False)


class TestMediumMassAssignment(TestCase):
    """Test that Medium views only accept whitelisted fields."""

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.create_user("medium_staff", is_staff=True))
        self.medium = Medium.objects.create(
            name="Test Medium", length_modifier_type="/", length_modifier=1
        )

    def test_create_accepts_whitelisted_fields(self):
        """Test that create view accepts all Medium fields."""
        url = reverse("items:create:medium")
        response = self.client.post(
            url, {"name": "New Medium", "length_modifier_type": "*", "length_modifier": 2}
        )
        self.assertEqual(response.status_code, 302)
        medium = Medium.objects.get(name="New Medium")
        self.assertEqual(medium.length_modifier_type, "*")
        self.assertEqual(medium.length_modifier, 2)

    def test_update_accepts_whitelisted_fields(self):
        """Test that update view accepts all Medium fields."""
        url = reverse("items:update:medium", kwargs={"pk": self.medium.pk})
        response = self.client.post(
            url, {"name": "Updated Medium", "length_modifier_type": "*", "length_modifier": 3}
        )
        self.assertEqual(response.status_code, 302)
        self.medium.refresh_from_db()
        self.assertEqual(self.medium.name, "Updated Medium")


class TestLanguageMassAssignment(TestCase):
    """Test that Language views only accept whitelisted fields."""

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.create_user("language_staff", is_staff=True))
        self.language = Language.objects.create(name="Test Language", frequency=1)

    def test_create_accepts_whitelisted_fields(self):
        """Test that create view accepts name and frequency fields."""
        url = reverse("core:create_language")
        response = self.client.post(url, {"name": "New Language", "frequency": 5})
        self.assertEqual(response.status_code, 302)
        language = Language.objects.get(name="New Language")
        self.assertEqual(language.frequency, 5)

    def test_update_accepts_whitelisted_fields(self):
        """Test that update view accepts name and frequency fields."""
        url = reverse("core:update_language", kwargs={"pk": self.language.pk})
        response = self.client.post(url, {"name": "Updated Language", "frequency": 10})
        self.assertEqual(response.status_code, 302)
        self.language.refresh_from_db()
        self.assertEqual(self.language.name, "Updated Language")
        self.assertEqual(self.language.frequency, 10)


class TestNewsItemMassAssignment(TestCase):
    """Test that NewsItem views only accept whitelisted fields."""

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.create_user("news_staff", is_staff=True))
        self.newsitem = NewsItem.objects.create(title="Test News", content="Content here")

    def test_create_accepts_whitelisted_fields(self):
        """Test that create view accepts title, content, and date fields."""
        url = reverse("core:create_newsitem")
        response = self.client.post(
            url, {"title": "New News", "content": "New content", "date": "2024-01-01"}
        )
        self.assertEqual(response.status_code, 302)
        newsitem = NewsItem.objects.get(title="New News")
        self.assertEqual(newsitem.content, "New content")

    def test_update_accepts_whitelisted_fields(self):
        """Test that update view accepts title, content, and date fields."""
        url = reverse("core:update_newsitem", kwargs={"pk": self.newsitem.pk})
        response = self.client.post(
            url, {"title": "Updated News", "content": "Updated content", "date": "2024-01-02"}
        )
        self.assertEqual(response.status_code, 302)
        self.newsitem.refresh_from_db()
        self.assertEqual(self.newsitem.title, "Updated News")
        self.assertEqual(self.newsitem.content, "Updated content")


class TestCompanionMassAssignment(TestCase):
    """Test that Companion views protect sensitive fields from mass assignment."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.st = User.objects.create_user(username="st", email="st@test.com", password="password")
        self.attacker = User.objects.create_user(
            username="attacker", email="attacker@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        mage = Gameline.objects.create(name="Mage: the Ascension")
        STRelationship.objects.create(user=self.st, chronicle=self.chronicle, gameline=mage)

        self.companion = Companion.objects.create(
            name="Test Companion",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",  # Unfinished
            companion_type="familiar",
        )

    def test_owner_cannot_change_status_via_form(self):
        """Test that owners cannot change status field via form submission."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:mage:update:companion_full", kwargs={"pk": self.companion.pk})

        # Owner gets LimitedHumanEditForm which doesn't include status
        response = self.client.post(
            url,
            {
                "notes": "Some notes",
                "description": "A description",
                "public_info": "Public",
                "history": "History",
                "goals": "Goals",
                "status": "App",  # Try to set status to Approved
            },
        )

        self.companion.refresh_from_db()
        # Status should remain unchanged because it's not in the limited form
        self.assertEqual(self.companion.status, "Un")

    def test_owner_cannot_change_xp_via_form(self):
        """Test that owners cannot change xp field via form submission."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:mage:update:companion_full", kwargs={"pk": self.companion.pk})

        original_xp = self.companion.xp
        response = self.client.post(
            url,
            {
                "notes": "Some notes",
                "description": "A description",
                "public_info": "Public",
                "history": "History",
                "goals": "Goals",
                "xp": 1000,  # Try to set XP to 1000
            },
        )

        self.companion.refresh_from_db()
        # XP should remain unchanged
        self.assertEqual(self.companion.xp, original_xp)

    def test_owner_cannot_change_owner_via_form(self):
        """Test that owners cannot change owner field via form submission."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:mage:update:companion_full", kwargs={"pk": self.companion.pk})

        response = self.client.post(
            url,
            {
                "notes": "Some notes",
                "description": "A description",
                "public_info": "Public",
                "history": "History",
                "goals": "Goals",
                "owner": self.attacker.pk,  # Try to change owner
            },
        )

        self.companion.refresh_from_db()
        # Owner should remain unchanged
        self.assertEqual(self.companion.owner, self.owner)

    def test_owner_cannot_change_freebies_approved_via_form(self):
        """Test that owners cannot change freebies_approved field via form submission."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:mage:update:companion_full", kwargs={"pk": self.companion.pk})

        response = self.client.post(
            url,
            {
                "notes": "Some notes",
                "description": "A description",
                "public_info": "Public",
                "history": "History",
                "goals": "Goals",
                "freebies_approved": True,  # Try to approve own freebies
            },
        )

        self.companion.refresh_from_db()
        # freebies_approved should remain False
        self.assertEqual(self.companion.freebies_approved, False)

    def test_owner_cannot_change_st_notes_via_form(self):
        """Test that owners cannot change st_notes field via form submission."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:mage:update:companion_full", kwargs={"pk": self.companion.pk})

        response = self.client.post(
            url,
            {
                "notes": "Some notes",
                "description": "A description",
                "public_info": "Public",
                "history": "History",
                "goals": "Goals",
                "st_notes": "Hacked ST notes",  # Try to set ST notes
            },
        )

        self.companion.refresh_from_db()
        # st_notes should remain empty
        self.assertEqual(self.companion.st_notes, "")

    def _get_st_form_data(self, **overrides):
        """Helper to get base form data for ST edit tests."""
        data = {
            "name": self.companion.name,
            "companion_type": self.companion.companion_type,
            "willpower": self.companion.willpower,
            "visibility": "PRI",  # Private visibility
            "status": self.companion.status,
            "xp": self.companion.xp,
        }
        data.update(overrides)
        return data

    def test_st_cannot_change_status_through_update_form(self):
        """Status changes use the dedicated submission and review actions."""
        self.client.login(username="st", password="password")
        url = reverse("characters:mage:update:companion_full", kwargs={"pk": self.companion.pk})

        # Test valid status transition: Un -> Sub
        response = self.client.post(url, self._get_st_form_data(status="Sub"))

        self.assertEqual(response.status_code, 403)
        self.companion.refresh_from_db()
        self.assertEqual(self.companion.status, "Un")

    def test_st_cannot_change_xp_through_update_form(self):
        """XP must be awarded through its guarded service."""
        self.client.login(username="st", password="password")
        url = reverse("characters:mage:update:companion_full", kwargs={"pk": self.companion.pk})

        response = self.client.post(url, self._get_st_form_data(xp=100))

        self.assertEqual(response.status_code, 403)
        self.companion.refresh_from_db()
        self.assertEqual(self.companion.xp, 0)

    def test_st_cannot_approve_freebies_through_update_form(self):
        """Freebie approval must use its dedicated service."""
        self.client.login(username="st", password="password")
        url = reverse("characters:mage:update:companion_full", kwargs={"pk": self.companion.pk})

        response = self.client.post(url, self._get_st_form_data(freebies_approved=True))

        self.assertEqual(response.status_code, 403)
        self.companion.refresh_from_db()
        self.assertEqual(self.companion.freebies_approved, False)

    def test_st_can_modify_st_notes_field(self):
        """Test that STs have access to st_notes field via ST_EDIT_FIELDS."""
        self.client.login(username="st", password="password")
        url = reverse("characters:mage:update:companion_full", kwargs={"pk": self.companion.pk})

        response = self.client.post(
            url, self._get_st_form_data(st_notes="ST notes for this character")
        )

        if response.status_code == 200 and hasattr(response, "context") and response.context:
            form = response.context.get("form")
            if form and form.errors:
                self.fail(f"Form errors: {form.errors}")

        self.assertEqual(response.status_code, 302)
        self.companion.refresh_from_db()
        self.assertEqual(self.companion.st_notes, "ST notes for this character")


class TestCharacterMassAssignment(TestCase):
    """Test that Character views protect sensitive fields from mass assignment."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.st = User.objects.create_user(username="st", email="st@test.com", password="password")
        self.attacker = User.objects.create_user(
            username="attacker", email="attacker@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        self.human = Human.objects.create(
            name="Test Human",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
        )

    def test_owner_cannot_change_status_via_form(self):
        """Test that owners cannot change status field via form submission."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:update:human", kwargs={"pk": self.human.pk})

        response = self.client.post(
            url,
            {
                "notes": "Some notes",
                "description": "A description",
                "public_info": "Public",
                "history": "History",
                "goals": "Goals",
                "status": "App",  # Try to set status to Approved
            },
        )

        self.human.refresh_from_db()
        # Status should remain unchanged because it's not in the limited form
        self.assertEqual(self.human.status, "Un")

    def test_owner_cannot_change_xp_via_form(self):
        """Test that owners cannot change xp field via form submission."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:update:human", kwargs={"pk": self.human.pk})

        original_xp = self.human.xp
        response = self.client.post(
            url,
            {
                "notes": "Some notes",
                "description": "A description",
                "public_info": "Public",
                "history": "History",
                "goals": "Goals",
                "xp": 1000,  # Try to set XP to 1000
            },
        )

        self.human.refresh_from_db()
        # XP should remain unchanged
        self.assertEqual(self.human.xp, original_xp)

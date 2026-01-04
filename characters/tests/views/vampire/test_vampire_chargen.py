"""Tests for vampire_chargen module.

Tests cover:
- VampireBasicsView - Initial vampire creation
- VampireAttributeView - 7/5/3 attribute allocation
- VampireAbilityView - 13/9/5 ability allocation
- VampireBackgroundsView - Background selection
- VampireDisciplinesView - 3 dots on clan disciplines
- VampireVirtuesView - 7 dots on virtues
- VampireExtrasView - Description and history
- VampireFreebiesView - 15 freebie points
- VampireCharacterCreationView - Workflow routing
"""

from characters.models.core.archetype import Archetype
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.path import Path
from characters.models.vampire.sect import VampireSect
from characters.models.vampire.vampire import Vampire
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class VampireChargenTestCase(TestCase):
    """Base test case with common setup for Vampire chargen tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create archetypes
        cls.nature = Archetype.objects.create(name="Survivor")
        cls.demeanor = Archetype.objects.create(name="Caregiver")

        # Create disciplines
        cls.potence = Discipline.objects.create(name="Potence", property_name="potence")
        cls.celerity = Discipline.objects.create(name="Celerity", property_name="celerity")
        cls.fortitude = Discipline.objects.create(name="Fortitude", property_name="fortitude")
        cls.dominate = Discipline.objects.create(name="Dominate", property_name="dominate")
        cls.presence = Discipline.objects.create(name="Presence", property_name="presence")
        cls.auspex = Discipline.objects.create(name="Auspex", property_name="auspex")
        cls.animalism = Discipline.objects.create(name="Animalism", property_name="animalism")
        cls.obfuscate = Discipline.objects.create(name="Obfuscate", property_name="obfuscate")
        cls.protean = Discipline.objects.create(name="Protean", property_name="protean")

        # Create clans with disciplines
        cls.brujah = VampireClan.objects.create(
            name="Brujah",
            nickname="Rabble",
            weakness="Prone to frenzy",
        )
        cls.brujah.disciplines.add(cls.potence, cls.celerity, cls.presence)

        cls.ventrue = VampireClan.objects.create(
            name="Ventrue",
            nickname="Blue Bloods",
            weakness="Refined palate",
        )
        cls.ventrue.disciplines.add(cls.dominate, cls.fortitude, cls.presence)

        cls.gangrel = VampireClan.objects.create(
            name="Gangrel",
            nickname="Outlanders",
            weakness="Animal features",
        )
        cls.gangrel.disciplines.add(cls.animalism, cls.fortitude, cls.protean)

        # Create a sect
        cls.camarilla = VampireSect.objects.create(name="Camarilla")
        cls.sabbat = VampireSect.objects.create(name="Sabbat")

        # Create paths of enlightenment
        cls.path_of_caine = Path.objects.create(
            name="Path of Caine",
            requires_conviction=True,
            requires_instinct=True,
            ethics="Follow the ways of the First Vampire",
        )

        cls.path_of_cathari = Path.objects.create(
            name="Path of Cathari",
            requires_conviction=True,
            requires_instinct=False,  # Uses Self-Control
            ethics="Pursue pleasure and corruption",
        )

    def setUp(self):
        """Set up test user and client."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@test.com",
            password="testpassword",
        )
        self.st = User.objects.create_user(
            username="storyteller",
            email="st@test.com",
            password="testpassword",
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)


class TestVampireBasicsView(VampireChargenTestCase):
    """Test VampireBasicsView for initial vampire creation."""

    def test_basics_view_requires_login(self):
        """Test that basics view requires authentication."""
        url = reverse("characters:vampire:create:vampire")
        response = self.client.get(url)
        # App returns 401 for unauthenticated users instead of redirect
        self.assertEqual(response.status_code, 401)

    def test_basics_view_accessible_when_logged_in(self):
        """Test that basics view is accessible when logged in."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vampire")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_basics_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vampire")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/vampire/vampire/basics.html")

    def test_basics_view_creates_vampire(self):
        """Test that submitting form creates a vampire."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vampire")
        data = {
            "name": "Test Vampire",
            "chronicle": self.chronicle.pk,
            "nature": self.nature.pk,
            "demeanor": self.demeanor.pk,
            "clan": self.brujah.pk,
            "sect": self.camarilla.pk,
            "generation": 13,
            "concept": "Warrior",
        }
        response = self.client.post(url, data)
        # Should redirect to character page on success
        self.assertEqual(response.status_code, 302)
        # Vampire should be created
        vampire = Vampire.objects.get(name="Test Vampire")
        self.assertEqual(vampire.owner, self.user)
        self.assertEqual(vampire.clan, self.brujah)

    def test_basics_view_sets_initial_willpower(self):
        """Test that willpower is set to courage after creation."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vampire")
        data = {
            "name": "Test Vampire",
            "nature": self.nature.pk,
            "demeanor": self.demeanor.pk,
            "clan": self.brujah.pk,
            "concept": "Warrior",
        }
        self.client.post(url, data)
        vampire = Vampire.objects.get(name="Test Vampire")
        self.assertEqual(vampire.willpower, vampire.courage)

    def test_basics_view_handles_path_selection(self):
        """Test that path selection zeroes humanity."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vampire")
        data = {
            "name": "Path Follower",
            "nature": self.nature.pk,
            "demeanor": self.demeanor.pk,
            "clan": self.brujah.pk,
            "path": self.path_of_caine.pk,
            "concept": "Zealot",
        }
        self.client.post(url, data)
        vampire = Vampire.objects.get(name="Path Follower")
        self.assertEqual(vampire.humanity, 0)
        self.assertEqual(vampire.path, self.path_of_caine)

    def test_basics_view_no_path_zeroes_path_rating(self):
        """Test that without a path, path_rating is zeroed."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vampire")
        data = {
            "name": "Humanity Follower",
            "nature": self.nature.pk,
            "demeanor": self.demeanor.pk,
            "clan": self.brujah.pk,
            "concept": "Regular",
        }
        self.client.post(url, data)
        vampire = Vampire.objects.get(name="Humanity Follower")
        self.assertEqual(vampire.path_rating, 0)
        self.assertIsNone(vampire.path)

    def test_basics_view_context_has_storyteller_flag(self):
        """Test that context includes storyteller flag."""
        self.client.login(username="storyteller", password="testpassword")
        url = reverse("characters:vampire:create:vampire")
        response = self.client.get(url)
        self.assertTrue(response.context["storyteller"])

    def test_basics_view_storyteller_false_for_regular_user(self):
        """Test that storyteller flag is false for non-ST users."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vampire")
        response = self.client.get(url)
        self.assertFalse(response.context["storyteller"])


class TestVampireAttributeView(VampireChargenTestCase):
    """Test VampireAttributeView for 7/5/3 attribute allocation."""

    def setUp(self):
        super().setUp()
        self.vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            clan=self.brujah,
            creation_status=1,  # At attribute step
        )

    def test_attribute_view_accessible_to_owner(self):
        """Test that attribute view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_attribute_view_denied_to_other_users(self):
        """Test that attribute view is denied to non-owners."""
        self.client.login(username="otheruser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])

    def test_attribute_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/vampire/vampire/chargen.html")


class TestVampireAbilityView(VampireChargenTestCase):
    """Test VampireAbilityView for 13/9/5 ability allocation."""

    def setUp(self):
        super().setUp()
        self.vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            clan=self.brujah,
            creation_status=2,  # At ability step
            strength=4,
            dexterity=3,
            stamina=3,  # Physical: 7
            charisma=3,
            manipulation=3,
            appearance=2,  # Social: 5
            perception=2,
            intelligence=2,
            wits=2,  # Mental: 3
        )

    def test_ability_view_accessible_to_owner(self):
        """Test that ability view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestVampireDisciplinesView(VampireChargenTestCase):
    """Test VampireDisciplinesView for discipline allocation."""

    def setUp(self):
        super().setUp()
        self.vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            clan=self.brujah,
            creation_status=4,  # At disciplines step
        )

    def test_disciplines_view_accessible_to_owner(self):
        """Test that disciplines view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_disciplines_view_context_has_clan_disciplines(self):
        """Test that context includes clan disciplines."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        response = self.client.get(url)
        self.assertIn("clan_disciplines", response.context)

    def test_disciplines_view_accepts_valid_allocation(self):
        """Test that valid discipline allocation (3 dots) is accepted."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        # Brujah has Potence, Celerity, Presence
        data = {
            "potence": 1,
            "celerity": 1,
            "presence": 1,
            # All other disciplines set to 0
            "fortitude": 0,
            "auspex": 0,
            "dominate": 0,
            "dementation": 0,
            "animalism": 0,
            "protean": 0,
            "obfuscate": 0,
            "chimerstry": 0,
            "necromancy": 0,
            "obtenebration": 0,
            "quietus": 0,
            "serpentis": 0,
            "thaumaturgy": 0,
            "vicissitude": 0,
            "daimoinon": 0,
            "melpominee": 0,
            "mytherceria": 0,
            "obeah": 0,
            "temporis": 0,
            "thanatosis": 0,
            "valeren": 0,
            "visceratika": 0,
        }
        response = self.client.post(url, data)
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        # Vampire disciplines should be updated
        self.vampire.refresh_from_db()
        self.assertEqual(self.vampire.potence, 1)
        self.assertEqual(self.vampire.celerity, 1)
        self.assertEqual(self.vampire.presence, 1)
        # Creation status should advance
        self.assertEqual(self.vampire.creation_status, 5)

    def test_disciplines_view_rejects_too_many_dots(self):
        """Test that more than 3 dots is rejected."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        data = {
            "potence": 2,
            "celerity": 2,  # Total: 4 dots
            "presence": 0,
            "fortitude": 0,
            "auspex": 0,
            "dominate": 0,
            "dementation": 0,
            "animalism": 0,
            "protean": 0,
            "obfuscate": 0,
            "chimerstry": 0,
            "necromancy": 0,
            "obtenebration": 0,
            "quietus": 0,
            "serpentis": 0,
            "thaumaturgy": 0,
            "vicissitude": 0,
            "daimoinon": 0,
            "melpominee": 0,
            "mytherceria": 0,
            "obeah": 0,
            "temporis": 0,
            "thanatosis": 0,
            "valeren": 0,
            "visceratika": 0,
        }
        response = self.client.post(url, data)
        # Should stay on page with error
        self.assertEqual(response.status_code, 200)
        # Creation status should not advance
        self.vampire.refresh_from_db()
        self.assertEqual(self.vampire.creation_status, 4)

    def test_disciplines_view_rejects_too_few_dots(self):
        """Test that fewer than 3 dots is rejected."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        data = {
            "potence": 1,
            "celerity": 1,  # Total: 2 dots
            "presence": 0,
            "fortitude": 0,
            "auspex": 0,
            "dominate": 0,
            "dementation": 0,
            "animalism": 0,
            "protean": 0,
            "obfuscate": 0,
            "chimerstry": 0,
            "necromancy": 0,
            "obtenebration": 0,
            "quietus": 0,
            "serpentis": 0,
            "thaumaturgy": 0,
            "vicissitude": 0,
            "daimoinon": 0,
            "melpominee": 0,
            "mytherceria": 0,
            "obeah": 0,
            "temporis": 0,
            "thanatosis": 0,
            "valeren": 0,
            "visceratika": 0,
        }
        response = self.client.post(url, data)
        # Should stay on page with error
        self.assertEqual(response.status_code, 200)
        # Creation status should not advance
        self.vampire.refresh_from_db()
        self.assertEqual(self.vampire.creation_status, 4)

    def test_disciplines_view_rejects_non_clan_disciplines(self):
        """Test that non-clan disciplines are rejected during chargen."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        # Brujah doesn't have Dominate
        data = {
            "potence": 1,
            "celerity": 1,
            "dominate": 1,  # Not a Brujah discipline
            "presence": 0,
            "fortitude": 0,
            "auspex": 0,
            "dementation": 0,
            "animalism": 0,
            "protean": 0,
            "obfuscate": 0,
            "chimerstry": 0,
            "necromancy": 0,
            "obtenebration": 0,
            "quietus": 0,
            "serpentis": 0,
            "thaumaturgy": 0,
            "vicissitude": 0,
            "daimoinon": 0,
            "melpominee": 0,
            "mytherceria": 0,
            "obeah": 0,
            "temporis": 0,
            "thanatosis": 0,
            "valeren": 0,
            "visceratika": 0,
        }
        response = self.client.post(url, data)
        # Should stay on page with error
        self.assertEqual(response.status_code, 200)
        # Creation status should not advance
        self.vampire.refresh_from_db()
        self.assertEqual(self.vampire.creation_status, 4)


class TestVampireVirtuesView(VampireChargenTestCase):
    """Test VampireVirtuesView for virtue allocation."""

    def setUp(self):
        super().setUp()
        # Create vampire with Humanity (default virtues)
        self.vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            clan=self.brujah,
            creation_status=5,  # At virtues step
            has_conviction=False,
            has_instinct=False,
        )
        # Create vampire on a Path
        self.path_vampire = Vampire.objects.create(
            name="Path Vampire",
            owner=self.user,
            clan=self.brujah,
            creation_status=5,
            path=self.path_of_caine,
            has_conviction=True,
            has_instinct=True,
        )

    def test_virtues_view_accessible_to_owner(self):
        """Test that virtues view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_virtues_view_accepts_valid_allocation(self):
        """Test that valid virtue allocation (7 dots) is accepted."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        data = {
            "conscience": 3,
            "self_control": 2,
            "courage": 2,
            "conviction": 0,
            "instinct": 0,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.vampire.refresh_from_db()
        self.assertEqual(self.vampire.conscience, 3)
        self.assertEqual(self.vampire.self_control, 2)
        self.assertEqual(self.vampire.courage, 2)
        # Willpower should be set to Courage
        self.assertEqual(self.vampire.willpower, 2)
        # Humanity should be conscience + self_control
        self.assertEqual(self.vampire.humanity, 5)

    def test_virtues_view_rejects_wrong_total(self):
        """Test that wrong total (not 7) is rejected."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        data = {
            "conscience": 4,
            "self_control": 4,
            "courage": 4,  # Total: 12
            "conviction": 0,
            "instinct": 0,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Stays on form
        self.vampire.refresh_from_db()
        self.assertEqual(self.vampire.creation_status, 5)  # Not advanced

    def test_path_vampire_uses_path_rating(self):
        """Test that path vampires get path_rating instead of humanity."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.path_vampire.pk})
        data = {
            "conscience": 0,
            "self_control": 0,
            "conviction": 3,
            "instinct": 2,
            "courage": 2,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.path_vampire.refresh_from_db()
        # Path rating = conviction + instinct
        self.assertEqual(self.path_vampire.path_rating, 5)
        # Humanity should be 0 for path followers
        self.assertEqual(self.path_vampire.humanity, 0)

    def test_virtues_view_context_has_uses_path(self):
        """Test that context includes uses_path flag."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.path_vampire.pk})
        response = self.client.get(url)
        self.assertTrue(response.context["uses_path"])


class TestVampireExtrasView(VampireChargenTestCase):
    """Test VampireExtrasView for description and history."""

    def setUp(self):
        super().setUp()
        self.vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            clan=self.brujah,
            creation_status=6,  # At extras step
        )

    def test_extras_view_accessible_to_owner(self):
        """Test that extras view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_extras_view_accepts_optional_data(self):
        """Test that extras fields are optional."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        data = {
            "age": 150,
            "apparent_age": 25,
            "date_of_birth": "1850-01-01",
            "history": "",  # Optional
            "goals": "",  # Optional
            "notes": "",  # Optional
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.vampire.refresh_from_db()
        self.assertEqual(self.vampire.creation_status, 7)


class TestVampireFreebiesView(VampireChargenTestCase):
    """Test VampireFreebiesView for freebie point spending."""

    def setUp(self):
        super().setUp()
        self.vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            clan=self.brujah,
            creation_status=7,  # At freebies step
            freebies=15,
        )

    def test_freebies_view_accessible_to_owner(self):
        """Test that freebies view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": self.vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestVampireCharacterCreationView(VampireChargenTestCase):
    """Test VampireCharacterCreationView workflow routing."""

    def test_routes_to_attribute_view_at_step_1(self):
        """Test that step 1 routes to attribute view."""
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            creation_status=1,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_ability_view_at_step_2(self):
        """Test that step 2 routes to ability view."""
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            creation_status=2,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_backgrounds_at_step_3(self):
        """Test that step 3 routes to backgrounds view."""
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            creation_status=3,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_disciplines_at_step_4(self):
        """Test that step 4 routes to disciplines view."""
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            clan=self.brujah,
            creation_status=4,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_virtues_at_step_5(self):
        """Test that step 5 routes to virtues view."""
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            creation_status=5,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_extras_at_step_6(self):
        """Test that step 6 routes to extras view."""
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            creation_status=6,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_freebies_at_step_7(self):
        """Test that step 7 routes to freebies view."""
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            creation_status=7,
            freebies=15,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_denied_to_non_owners(self):
        """Test that chargen is denied to non-owners."""
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            creation_status=1,
        )
        self.client.login(username="otheruser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": vampire.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])

    def test_accessible_to_storyteller(self):
        """Test that chargen is accessible to storytellers."""
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            chronicle=self.chronicle,
            creation_status=1,
        )
        self.client.login(username="storyteller", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestVampireChargenViewsReturn404(VampireChargenTestCase):
    """Test 404 handling for non-existent vampires."""

    def test_chargen_returns_404_for_invalid_pk(self):
        """Test that chargen returns 404 for non-existent vampire."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestVampireClanSpecificDisciplines(VampireChargenTestCase):
    """Test that different clans show their specific disciplines."""

    def test_gangrel_gets_animalism_protean_fortitude(self):
        """Test that Gangrel can allocate Animalism, Protean, Fortitude."""
        vampire = Vampire.objects.create(
            name="Gangrel Test",
            owner=self.user,
            clan=self.gangrel,
            creation_status=4,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vampire_chargen", kwargs={"pk": vampire.pk})
        data = {
            "animalism": 1,
            "fortitude": 1,
            "protean": 1,
            # All other disciplines set to 0
            "potence": 0,
            "celerity": 0,
            "presence": 0,
            "auspex": 0,
            "dominate": 0,
            "dementation": 0,
            "obfuscate": 0,
            "chimerstry": 0,
            "necromancy": 0,
            "obtenebration": 0,
            "quietus": 0,
            "serpentis": 0,
            "thaumaturgy": 0,
            "vicissitude": 0,
            "daimoinon": 0,
            "melpominee": 0,
            "mytherceria": 0,
            "obeah": 0,
            "temporis": 0,
            "thanatosis": 0,
            "valeren": 0,
            "visceratika": 0,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        vampire.refresh_from_db()
        self.assertEqual(vampire.animalism, 1)
        self.assertEqual(vampire.fortitude, 1)
        self.assertEqual(vampire.protean, 1)


class TestVampireFreebiesFormTemplateStaticJS(TestCase):
    """Test that vampire freebies form template includes static JavaScript file."""

    def test_freebies_form_loads_static_vampire_freebies_js(self):
        """Vampire freebies_form.html loads vampire-freebies-form.js from static files."""
        from django.template import loader

        template = loader.get_template("characters/vampire/vampire/freebies_form.html")

        # Verify the template source contains the static file reference
        template_source = template.template.source
        self.assertIn("js/vampire-freebies-form.js", template_source)
        self.assertIn("{% static", template_source)

    def test_freebies_form_has_data_attributes(self):
        """Vampire freebies_form.html has data attributes for JavaScript configuration."""
        from django.template import loader

        template = loader.get_template("characters/vampire/vampire/freebies_form.html")
        template_source = template.template.source

        # The template should use data attributes for URLs
        self.assertIn("data-load-examples-url", template_source)
        self.assertIn("data-load-values-url", template_source)
        self.assertIn("data-object-id", template_source)
        self.assertIn("data-is-group-member", template_source)

    def test_freebies_form_does_not_contain_inline_script(self):
        """Vampire freebies_form.html does not contain inline AJAX URLs."""
        from django.template import loader

        template = loader.get_template("characters/vampire/vampire/freebies_form.html")
        template_source = template.template.source

        # The template should not have AJAX URLs embedded in JavaScript
        # This pattern was the problematic code we extracted
        self.assertNotIn("$.ajax({", template_source)
        self.assertNotIn("url: '{% url", template_source)

"""Tests for ghoul_chargen module.

Tests cover:
- GhoulBasicsView - Initial ghoul creation
- GhoulAttributeView - 6/4/3 attribute allocation
- GhoulAbilityView - 11/7/4 ability allocation
- GhoulBackgroundsView - Background selection
- GhoulDisciplinesView - 2 additional dots on available disciplines
- GhoulExtrasView - Description and history
- GhoulFreebiesView - 21 freebie points
- GhoulCharacterCreationView - Workflow routing
"""

from characters.models.core.archetype import Archetype
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.vampire import Vampire
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class GhoulChargenTestCase(TestCase):
    """Base test case with common setup for Ghoul chargen tests."""

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
        cls.obfuscate = Discipline.objects.create(name="Obfuscate", property_name="obfuscate")

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

        # Create a domitor for testing
        self.domitor = Vampire.objects.create(
            name="Test Domitor",
            owner=self.user,
            clan=self.brujah,
        )


class TestGhoulBasicsView(GhoulChargenTestCase):
    """Test GhoulBasicsView for initial ghoul creation."""

    def test_basics_view_requires_login(self):
        """Test that basics view requires authentication."""
        url = reverse("characters:vampire:create:ghoul")
        response = self.client.get(url)
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_basics_view_accessible_when_logged_in(self):
        """Test that basics view is accessible when logged in."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:ghoul")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_basics_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:ghoul")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/vampire/ghoul/basics.html")

    def test_basics_view_creates_ghoul(self):
        """Test that submitting form creates a ghoul."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:ghoul")
        data = {
            "name": "Test Ghoul",
            "chronicle": self.chronicle.pk,
            "nature": self.nature.pk,
            "demeanor": self.demeanor.pk,
            "concept": "Servant",
        }
        response = self.client.post(url, data)
        # Should redirect to character page on success
        self.assertEqual(response.status_code, 302)
        # Ghoul should be created
        ghoul = Ghoul.objects.get(name="Test Ghoul")
        self.assertEqual(ghoul.owner, self.user)

    def test_basics_view_sets_potence_one(self):
        """Test that ghoul starts with Potence 1."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:ghoul")
        data = {
            "name": "Test Ghoul",
            "nature": self.nature.pk,
            "demeanor": self.demeanor.pk,
            "concept": "Servant",
        }
        self.client.post(url, data)
        ghoul = Ghoul.objects.get(name="Test Ghoul")
        self.assertEqual(ghoul.potence, 1)

    def test_basics_view_sets_initial_willpower(self):
        """Test that willpower is set to courage after creation."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:ghoul")
        data = {
            "name": "Test Ghoul",
            "nature": self.nature.pk,
            "demeanor": self.demeanor.pk,
            "concept": "Servant",
        }
        self.client.post(url, data)
        ghoul = Ghoul.objects.get(name="Test Ghoul")
        self.assertEqual(ghoul.willpower, ghoul.courage)

    def test_basics_view_context_has_storyteller_flag(self):
        """Test that context includes storyteller flag."""
        self.client.login(username="storyteller", password="testpassword")
        url = reverse("characters:vampire:create:ghoul")
        response = self.client.get(url)
        self.assertTrue(response.context["storyteller"])

    def test_basics_view_storyteller_false_for_regular_user(self):
        """Test that storyteller flag is false for non-ST users."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:ghoul")
        response = self.client.get(url)
        self.assertFalse(response.context["storyteller"])


class TestGhoulAttributeView(GhoulChargenTestCase):
    """Test GhoulAttributeView for 6/4/3 attribute allocation."""

    def setUp(self):
        super().setUp()
        self.ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            creation_status=1,  # At attribute step
        )

    def test_attribute_view_accessible_to_owner(self):
        """Test that attribute view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_attribute_view_denied_to_other_users(self):
        """Test that attribute view is denied to non-owners."""
        self.client.login(username="otheruser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])

    def test_attribute_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/vampire/ghoul/chargen.html")


class TestGhoulAbilityView(GhoulChargenTestCase):
    """Test GhoulAbilityView for 11/7/4 ability allocation."""

    def setUp(self):
        super().setUp()
        self.ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            creation_status=2,  # At ability step
            strength=3,
            dexterity=3,
            stamina=3,  # Physical: 6
            charisma=2,
            manipulation=2,
            appearance=2,  # Social: 4
            perception=2,
            intelligence=2,
            wits=2,  # Mental: 3
        )

    def test_ability_view_accessible_to_owner(self):
        """Test that ability view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestGhoulDisciplinesView(GhoulChargenTestCase):
    """Test GhoulDisciplinesView for discipline allocation."""

    def setUp(self):
        super().setUp()
        # Ghoul with a domitor
        self.ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            domitor=self.domitor,
            creation_status=4,  # At disciplines step
        )
        # Independent ghoul
        self.independent_ghoul = Ghoul.objects.create(
            name="Independent Ghoul",
            owner=self.user,
            is_independent=True,
            creation_status=4,
        )

    def test_disciplines_view_accessible_to_owner(self):
        """Test that disciplines view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_disciplines_view_context_has_available_disciplines(self):
        """Test that context includes available disciplines."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        response = self.client.get(url)
        self.assertIn("available_disciplines", response.context)

    def test_disciplines_view_context_has_domitor_flag(self):
        """Test that context indicates if ghoul has a domitor."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        response = self.client.get(url)
        self.assertTrue(response.context["has_domitor"])

    def test_independent_ghoul_has_no_domitor(self):
        """Test that independent ghoul has no domitor in context."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse(
            "characters:vampire:ghoul_chargen", kwargs={"pk": self.independent_ghoul.pk}
        )
        response = self.client.get(url)
        self.assertFalse(response.context["has_domitor"])

    def test_disciplines_view_accepts_valid_allocation(self):
        """Test that valid discipline allocation (up to 2 dots) is accepted."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        # Brujah domitor has Potence, Celerity, Presence
        data = {
            "potence": 1,  # Already 1 from default
            "celerity": 1,
            "fortitude": 0,
            "auspex": 0,
            "dominate": 0,
            "obfuscate": 0,
            "presence": 1,
        }
        response = self.client.post(url, data)
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        self.ghoul.refresh_from_db()
        # Creation status should advance
        self.assertEqual(self.ghoul.creation_status, 5)

    def test_disciplines_view_rejects_more_than_2_additional_dots(self):
        """Test that more than 2 additional dots is rejected."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        data = {
            "potence": 1,
            "celerity": 2,
            "fortitude": 0,
            "auspex": 0,
            "dominate": 0,
            "obfuscate": 0,
            "presence": 1,  # Total additional: 3 (celerity 2 + presence 1)
        }
        response = self.client.post(url, data)
        # Should stay on page with error
        self.assertEqual(response.status_code, 200)
        self.ghoul.refresh_from_db()
        self.assertEqual(self.ghoul.creation_status, 4)  # Not advanced

    def test_disciplines_view_rejects_unavailable_disciplines(self):
        """Test that unavailable disciplines are rejected."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        # Brujah domitor doesn't have Dominate
        data = {
            "potence": 1,
            "celerity": 0,
            "fortitude": 0,
            "auspex": 0,
            "dominate": 1,  # Not available from Brujah
            "obfuscate": 0,
            "presence": 1,
        }
        response = self.client.post(url, data)
        # Should stay on page with error
        self.assertEqual(response.status_code, 200)
        self.ghoul.refresh_from_db()
        self.assertEqual(self.ghoul.creation_status, 4)


class TestGhoulExtrasView(GhoulChargenTestCase):
    """Test GhoulExtrasView for description and history."""

    def setUp(self):
        super().setUp()
        self.ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            creation_status=5,  # At extras step
        )

    def test_extras_view_accessible_to_owner(self):
        """Test that extras view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_extras_view_accepts_years_as_ghoul(self):
        """Test that years_as_ghoul field is available."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        data = {
            "age": 35,
            "apparent_age": 28,
            "date_of_birth": "1989-01-01",
            "years_as_ghoul": 7,
            "history": "Served my master faithfully.",
            "goals": "To please my domitor.",
            "notes": "",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.ghoul.refresh_from_db()
        self.assertEqual(self.ghoul.years_as_ghoul, 7)
        self.assertEqual(self.ghoul.creation_status, 6)


class TestGhoulFreebiesView(GhoulChargenTestCase):
    """Test GhoulFreebiesView for freebie point spending."""

    def setUp(self):
        super().setUp()
        self.ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            creation_status=6,  # At freebies step
            freebies=21,
        )

    def test_freebies_view_accessible_to_owner(self):
        """Test that freebies view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": self.ghoul.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestGhoulCharacterCreationView(GhoulChargenTestCase):
    """Test GhoulCharacterCreationView workflow routing."""

    def test_routes_to_attribute_view_at_step_1(self):
        """Test that step 1 routes to attribute view."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            creation_status=1,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": ghoul.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_ability_view_at_step_2(self):
        """Test that step 2 routes to ability view."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            creation_status=2,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": ghoul.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_backgrounds_at_step_3(self):
        """Test that step 3 routes to backgrounds view."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            creation_status=3,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": ghoul.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_disciplines_at_step_4(self):
        """Test that step 4 routes to disciplines view."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            creation_status=4,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": ghoul.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_extras_at_step_5(self):
        """Test that step 5 routes to extras view."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            creation_status=5,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": ghoul.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_freebies_at_step_6(self):
        """Test that step 6 routes to freebies view."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            creation_status=6,
            freebies=21,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": ghoul.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_denied_to_non_owners(self):
        """Test that chargen is denied to non-owners."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            creation_status=1,
        )
        self.client.login(username="otheruser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": ghoul.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])

    def test_accessible_to_storyteller(self):
        """Test that chargen is accessible to storytellers."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            chronicle=self.chronicle,
            creation_status=1,
        )
        self.client.login(username="storyteller", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": ghoul.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestGhoulChargenViewsReturn404(GhoulChargenTestCase):
    """Test 404 handling for non-existent ghouls."""

    def test_chargen_returns_404_for_invalid_pk(self):
        """Test that chargen returns 404 for non-existent ghoul."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:ghoul_chargen", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestGhoulDefaultValues(GhoulChargenTestCase):
    """Test that ghouls have correct default values."""

    def test_ghoul_max_blood_pool_is_2(self):
        """Test that ghouls have max blood pool of 2."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
        )
        self.assertEqual(ghoul.max_blood_pool, 2)

    def test_ghoul_potence_default_is_1(self):
        """Test that ghouls start with Potence 1."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
        )
        self.assertEqual(ghoul.potence, 1)

    def test_ghoul_freebie_step_is_6(self):
        """Test that ghoul freebie step is 6."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
        )
        self.assertEqual(ghoul.freebie_step, 6)

    def test_ghoul_type_is_ghoul(self):
        """Test that ghoul type is 'ghoul'."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
        )
        self.assertEqual(ghoul.type, "ghoul")


class TestGhoulDomitorRelationship(GhoulChargenTestCase):
    """Test ghoul-domitor relationship functionality."""

    def test_ghoul_can_have_domitor(self):
        """Test that ghouls can be assigned a domitor."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            domitor=self.domitor,
        )
        self.assertEqual(ghoul.domitor, self.domitor)

    def test_ghoul_available_disciplines_with_domitor(self):
        """Test that available disciplines match domitor's clan disciplines."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            domitor=self.domitor,
        )
        available = ghoul.get_available_disciplines()
        # Brujah has Potence, Celerity, Presence
        discipline_names = [d.name for d in available]
        self.assertIn("Potence", discipline_names)
        self.assertIn("Celerity", discipline_names)
        self.assertIn("Presence", discipline_names)

    def test_ghoul_available_disciplines_without_domitor(self):
        """Test that independent ghouls get physical disciplines."""
        ghoul = Ghoul.objects.create(
            name="Independent Ghoul",
            owner=self.user,
            is_independent=True,
        )
        available = ghoul.get_available_disciplines()
        discipline_names = [d.name for d in available]
        # Independent ghouls should get physical disciplines
        self.assertIn("Potence", discipline_names)
        self.assertIn("Celerity", discipline_names)
        self.assertIn("Fortitude", discipline_names)

    def test_ghoul_get_disciplines(self):
        """Test get_disciplines returns only non-zero disciplines."""
        ghoul = Ghoul.objects.create(
            name="Test Ghoul",
            owner=self.user,
            potence=1,  # Default
            celerity=2,
        )
        disciplines = ghoul.get_disciplines()
        self.assertEqual(disciplines, {"Potence": 1, "Celerity": 2})

    def test_domitor_ghouls_relation(self):
        """Test that domitor can access their ghouls."""
        ghoul1 = Ghoul.objects.create(
            name="Ghoul 1",
            owner=self.user,
            domitor=self.domitor,
        )
        ghoul2 = Ghoul.objects.create(
            name="Ghoul 2",
            owner=self.user,
            domitor=self.domitor,
        )
        self.assertEqual(self.domitor.ghouls.count(), 2)
        self.assertIn(ghoul1, self.domitor.ghouls.all())
        self.assertIn(ghoul2, self.domitor.ghouls.all())

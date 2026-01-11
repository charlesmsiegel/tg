"""Tests for Freebie spending service."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.mage.mage import Mage
from characters.models.vampire.vampire import Vampire
from characters.services.freebie_spending import (
    FreebieApplyResult,
    FreebieSpendingServiceFactory,
    FreebieSpendResult,
    HumanFreebieSpendingService,
    MageFreebieSpendingService,
    VampireFreebieSpendingService,
)
from game.models import Chronicle, FreebieSpendingRecord


class TestFreebieSpendResult(TestCase):
    """Test FreebieSpendResult dataclass."""

    def test_success_result(self):
        """Test successful result creation."""
        result = FreebieSpendResult(
            success=True,
            trait="Strength",
            cost=5,
            message="Spent 5 freebies on Strength",
        )
        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Strength")
        self.assertEqual(result.cost, 5)
        self.assertEqual(result.message, "Spent 5 freebies on Strength")
        self.assertIsNone(result.error)

    def test_failure_result(self):
        """Test failure result creation."""
        result = FreebieSpendResult(
            success=False,
            trait="Strength",
            cost=0,
            message="",
            error="Not enough freebies",
        )
        self.assertFalse(result.success)
        self.assertEqual(result.error, "Not enough freebies")


class TestFreebieApplyResult(TestCase):
    """Test FreebieApplyResult dataclass."""

    def test_success_result(self):
        """Test successful apply result creation."""
        result = FreebieApplyResult(
            success=True,
            trait="Strength",
            message="Approved Strength",
        )
        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Strength")
        self.assertEqual(result.message, "Approved Strength")
        self.assertIsNone(result.error)


class TestFreebieSpendingServiceFactory(TestCase):
    """Test FreebieSpendingServiceFactory."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_get_mage_service(self):
        """Test factory returns correct service for Mage."""
        mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
        )
        service = FreebieSpendingServiceFactory.get_service(mage)
        self.assertIsInstance(service, MageFreebieSpendingService)

    def test_get_vampire_service(self):
        """Test factory returns correct service for Vampire."""
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            chronicle=self.chronicle,
            freebies=15,
        )
        service = FreebieSpendingServiceFactory.get_service(vampire)
        self.assertIsInstance(service, VampireFreebieSpendingService)

    def test_get_categories(self):
        """Test factory can get available categories for a character."""
        mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
        )
        categories = FreebieSpendingServiceFactory.get_categories_for_character(mage)
        self.assertIn("Attribute", categories)
        self.assertIn("Ability", categories)
        self.assertIn("Sphere", categories)
        self.assertIn("Arete", categories)


class TestHumanFreebieSpendingService(TestCase):
    """Test HumanFreebieSpendingService attribute and ability spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
            strength=2,
            alertness=1,
        )
        self.strength = Attribute.objects.create(name="Strength", property_name="strength")
        self.alertness = Ability.objects.create(name="Alertness", property_name="alertness")

    def test_spend_on_attribute(self):
        """Test spending freebies on an attribute."""
        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("Attribute", self.strength)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Strength")
        self.assertEqual(result.cost, 5)  # Attribute cost is 5
        self.assertIn("freebies", result.message)

        # Verify attribute was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.strength, 3)

        # Verify freebies were deducted
        self.assertEqual(self.mage.freebies, 10)

        # Verify FreebieSpendingRecord was created
        record = FreebieSpendingRecord.objects.get(character=self.mage)
        self.assertEqual(record.trait_name, "Strength")
        self.assertEqual(record.trait_type, "attribute")
        self.assertEqual(record.cost, 5)
        self.assertEqual(record.approved, "Pending")

    def test_spend_on_attribute_insufficient_freebies(self):
        """Test spending on attribute with insufficient freebies."""
        self.mage.freebies = 2
        self.mage.save()

        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("Attribute", self.strength)

        self.assertFalse(result.success)
        self.assertIn("Not enough freebies", result.error)

    def test_spend_on_attribute_at_maximum(self):
        """Test spending on attribute already at maximum."""
        self.mage.strength = 5
        self.mage.save()

        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("Attribute", self.strength)

        self.assertFalse(result.success)
        self.assertIn("maximum", result.error)

    def test_spend_on_ability(self):
        """Test spending freebies on an ability."""
        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("Ability", self.alertness)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Alertness")
        self.assertEqual(result.cost, 2)  # Ability cost is 2

        # Verify ability was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.alertness, 2)

    def test_spend_on_willpower(self):
        """Test spending freebies on Willpower."""
        initial_willpower = self.mage.willpower

        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("Willpower")

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Willpower")
        self.assertEqual(result.cost, 1)  # Willpower cost is 1

        # Verify willpower was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.willpower, initial_willpower + 1)


class TestHumanFreebieSpendingBackgrounds(TestCase):
    """Test HumanFreebieSpendingService background spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
        )
        self.resources = Background.objects.create(name="Resources", property_name="resources")

    def test_spend_on_new_background(self):
        """Test spending freebies on a new background."""
        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("New Background", self.resources, note="Family wealth")

        self.assertTrue(result.success)
        self.assertIn("Resources", result.trait)
        self.assertIn("Family wealth", result.trait)

        # Verify background was created
        bg_rating = BackgroundRating.objects.get(char=self.mage, bg=self.resources)
        self.assertEqual(bg_rating.rating, 1)
        self.assertEqual(bg_rating.note, "Family wealth")

    def test_spend_on_existing_background(self):
        """Test spending freebies on an existing background."""
        bg_rating = BackgroundRating.objects.create(
            char=self.mage,
            bg=self.resources,
            rating=2,
            note="Inheritance",
        )

        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("Existing Background", bg_rating)

        self.assertTrue(result.success)

        # Verify background was increased
        bg_rating.refresh_from_db()
        self.assertEqual(bg_rating.rating, 3)


class TestMageFreebieSpendingService(TestCase):
    """Test MageFreebieSpendingService Mage-specific spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        # Arete must be higher than current sphere for add_sphere to work
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=3,
            freebies=30,
            forces=1,
        )
        from characters.models.mage.sphere import Sphere

        self.forces = Sphere.objects.filter(name="Forces").first()
        if not self.forces:
            self.forces = Sphere.objects.create(name="Forces", property_name="forces")

    def test_spend_on_sphere(self):
        """Test spending freebies on a Sphere."""
        service = MageFreebieSpendingService(self.mage)
        result = service.spend("Sphere", self.forces)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Forces")
        self.assertEqual(result.cost, 7)  # Sphere cost is 7

        # Verify sphere was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.forces, 2)

    def test_inherit_human_handlers(self):
        """Test that MageFreebieSpendingService inherits human handlers."""
        service = MageFreebieSpendingService(self.mage)
        categories = service.available_categories

        # Should have human categories
        self.assertIn("Attribute", categories)
        self.assertIn("Ability", categories)
        self.assertIn("Willpower", categories)

        # Should also have Mage categories
        self.assertIn("Sphere", categories)
        self.assertIn("Arete", categories)
        self.assertIn("Resonance", categories)


class TestFreebieApprovalDenial(TestCase):
    """Test freebie spending approval and denial."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.st_user = User.objects.create_user(
            username="storyteller", email="st@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
            strength=2,
        )
        self.strength = Attribute.objects.create(name="Strength", property_name="strength")

    def test_approve_freebie_spend(self):
        """Test approving a freebie spending request."""
        # First spend freebies to create a pending request
        service = MageFreebieSpendingService(self.mage)
        spend_result = service.spend("Attribute", self.strength)
        self.assertTrue(spend_result.success)

        # Get the pending request
        freebie_request = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")

        # Approve the request
        apply_result = service.apply(freebie_request, self.st_user)

        self.assertTrue(apply_result.success)
        self.assertIn("Approved", apply_result.message)

        # Verify request was marked approved
        freebie_request.refresh_from_db()
        self.assertEqual(freebie_request.approved, "Approved")
        self.assertEqual(freebie_request.approved_by, self.st_user)
        self.assertIsNotNone(freebie_request.approved_at)

    def test_deny_freebie_spend(self):
        """Test denying a freebie spending request reverts changes."""
        initial_strength = self.mage.strength
        initial_freebies = self.mage.freebies

        # Spend freebies
        service = MageFreebieSpendingService(self.mage)
        spend_result = service.spend("Attribute", self.strength)
        self.assertTrue(spend_result.success)

        # Verify trait increased and freebies deducted
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.strength, initial_strength + 1)
        self.assertEqual(self.mage.freebies, initial_freebies - 5)

        # Get the pending request
        freebie_request = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")

        # Deny the request
        deny_result = service.deny(freebie_request, self.st_user)

        self.assertTrue(deny_result.success)
        self.assertIn("Denied", deny_result.message)

        # Verify trait was reverted
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.strength, initial_strength)

        # Verify freebies were refunded
        self.assertEqual(self.mage.freebies, initial_freebies)

        # Verify request was marked denied
        freebie_request.refresh_from_db()
        self.assertEqual(freebie_request.approved, "Denied")


class TestUnknownCategory(TestCase):
    """Test handling of unknown freebie categories."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
        )

    def test_unknown_category_returns_error(self):
        """Test that spending on unknown category returns error."""
        service = MageFreebieSpendingService(self.mage)
        result = service.spend("Invalid Category")

        self.assertFalse(result.success)
        self.assertIn("Unknown freebie category", result.error)


class TestSphereAreteFreebiValidation(TestCase):
    """Test that sphere spending respects Arete limits."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        from characters.models.mage.sphere import Sphere

        self.forces = Sphere.objects.filter(name="Forces").first()
        if not self.forces:
            self.forces = Sphere.objects.create(name="Forces", property_name="forces")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=2,  # Arete is 2
            freebies=30,
            forces=2,  # Forces is already at Arete level
        )

    def test_sphere_cannot_exceed_arete(self):
        """Test that spending freebies on a sphere that would exceed Arete fails."""
        service = MageFreebieSpendingService(self.mage)
        result = service.spend("Sphere", self.forces)

        self.assertFalse(result.success)
        self.assertIn("cannot exceed Arete", result.error)

        # Verify sphere was NOT increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.forces, 2)

    def test_sphere_at_arete_cannot_increase(self):
        """Test sphere exactly at Arete limit cannot be increased further."""
        # Set Forces at Arete limit
        self.mage.forces = 2
        self.mage.arete = 2
        self.mage.save()

        service = MageFreebieSpendingService(self.mage)
        result = service.spend("Sphere", self.forces)

        self.assertFalse(result.success)
        self.assertIn("cannot exceed Arete", result.error)

    def test_sphere_below_arete_can_increase(self):
        """Test sphere below Arete limit can be increased."""
        self.mage.forces = 1
        self.mage.arete = 3  # Arete is 3, Forces is 1
        self.mage.save()

        service = MageFreebieSpendingService(self.mage)
        result = service.spend("Sphere", self.forces)

        self.assertTrue(result.success)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.forces, 2)

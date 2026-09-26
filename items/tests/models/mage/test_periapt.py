"""Tests for Periapt model."""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from game.models import Chronicle
from items.models.mage.periapt import Periapt


class TestPeriapt(TestCase):
    """Test Periapt model methods."""

    def setUp(self):
        self.periapt = Periapt.objects.create(
            name="Test Periapt",
            max_charges=5,
            current_charges=3,
        )

    def test_set_power(self):
        """Test setting a power on a periapt."""
        from characters.models.mage.effect import Effect

        effect = Effect.objects.create(name="Test Effect")
        self.assertFalse(self.periapt.has_power())
        self.assertTrue(self.periapt.set_power(effect))
        self.assertEqual(self.periapt.power, effect)

    def test_has_power(self):
        """Test checking if periapt has a power."""
        from characters.models.mage.effect import Effect

        self.assertFalse(self.periapt.has_power())
        effect = Effect.objects.create(name="Test Effect")
        self.periapt.power = effect
        self.periapt.save()
        self.assertTrue(self.periapt.has_power())

    def test_use_charge_success(self):
        """Test using a charge successfully."""
        initial_charges = self.periapt.current_charges
        result = self.periapt.use_charge()
        self.assertTrue(result)
        self.periapt.refresh_from_db()
        self.assertEqual(self.periapt.current_charges, initial_charges - 1)

    def test_use_charge_when_empty(self):
        """Test using a charge when periapt is empty."""
        self.periapt.current_charges = 0
        self.periapt.save()
        result = self.periapt.use_charge()
        self.assertFalse(result)
        self.periapt.refresh_from_db()
        self.assertEqual(self.periapt.current_charges, 0)

    def test_recharge_normal(self):
        """Test recharging the periapt."""
        self.periapt.current_charges = 2
        self.periapt.save()
        result = self.periapt.recharge(2)
        self.assertTrue(result)
        self.periapt.refresh_from_db()
        self.assertEqual(self.periapt.current_charges, 4)

    def test_recharge_capped_at_max(self):
        """Test recharging doesn't exceed max_charges."""
        self.periapt.current_charges = 4
        self.periapt.save()
        result = self.periapt.recharge(5)
        self.assertTrue(result)
        self.periapt.refresh_from_db()
        self.assertEqual(self.periapt.current_charges, self.periapt.max_charges)

    def test_is_depleted_true(self):
        """Test is_depleted returns True when charges are 0."""
        self.periapt.current_charges = 0
        self.periapt.save()
        self.assertTrue(self.periapt.is_depleted())

    def test_is_depleted_false(self):
        """Test is_depleted returns False when charges remain."""
        self.assertFalse(self.periapt.is_depleted())

    def test_charges_remaining(self):
        """Test charges_remaining returns current charges."""
        self.assertEqual(self.periapt.charges_remaining(), 3)


class TestPeriaptUrls(TestCase):
    """Test URL methods for Periapt."""

    def setUp(self):
        self.periapt = Periapt.objects.create(name="URL Test Periapt")

    def test_get_update_url(self):
        """Test get_update_url generates correct URL."""
        url = self.periapt.get_update_url()
        self.assertIn(str(self.periapt.id), url)
        self.assertIn("periapt", url)

    def test_get_creation_url(self):
        """Test get_creation_url generates correct URL."""
        url = Periapt.get_creation_url()
        self.assertIn("periapt", url)
        self.assertIn("create", url)

    def test_get_heading(self):
        """Test get_heading returns correct heading class."""
        self.assertEqual(self.periapt.get_heading(), "mta_heading")


class TestPeriaptDetailView(TestCase):
    """Test Periapt detail view."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.periapt = Periapt.objects.create(
            name="Test Periapt",
            owner=self.user,
            status="App",
        )
        self.url = self.periapt.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200 for logged in user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/periapt/detail.html")


class TestPeriaptCreateView(TestCase):
    """Test Periapt create view."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.url = Periapt.get_creation_url()

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/periapt/form.html")


class TestPeriaptUpdateView(TestCase):
    """Test Periapt update view."""

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.chronicle.head_st = self.st
        self.chronicle.save(update_fields=["head_st"])
        self.periapt = Periapt.objects.create(
            name="Test Periapt",
            description="Test description",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )
        self.url = self.periapt.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200 for ST."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/periapt/form.html")


class TestPeriaptConsumable(TestCase):
    """Test consumable behavior for Periapt."""

    def test_is_consumable_default_true(self):
        """Test is_consumable defaults to True."""
        periapt = Periapt.objects.create(name="Consumable Periapt")
        self.assertTrue(periapt.is_consumable)

    def test_is_consumable_can_be_false(self):
        """Test is_consumable can be set to False."""
        periapt = Periapt.objects.create(name="Permanent Periapt", is_consumable=False)
        self.assertFalse(periapt.is_consumable)


class TestPeriaptChargeManagement(TestCase):
    """Test charge management edge cases."""

    def test_use_all_charges(self):
        """Test using all charges sequentially."""
        periapt = Periapt.objects.create(name="Test", max_charges=3, current_charges=3)
        self.assertTrue(periapt.use_charge())
        self.assertTrue(periapt.use_charge())
        self.assertTrue(periapt.use_charge())
        self.assertFalse(periapt.use_charge())
        periapt.refresh_from_db()
        self.assertEqual(periapt.current_charges, 0)

    def test_recharge_from_empty(self):
        """Test recharging from empty state."""
        periapt = Periapt.objects.create(name="Test", max_charges=5, current_charges=0)
        periapt.recharge(3)
        periapt.refresh_from_db()
        self.assertEqual(periapt.current_charges, 3)

    def test_recharge_default_amount(self):
        """Test recharge with default amount of 1."""
        periapt = Periapt.objects.create(name="Test", max_charges=5, current_charges=2)
        periapt.recharge()
        periapt.refresh_from_db()
        self.assertEqual(periapt.current_charges, 3)


class TestPeriaptClean(TestCase):
    """Rules recovered from the deleted Periapt form: arete >= rank, charges <= max."""

    def test_arete_below_rank_is_rejected(self):
        periapt = Periapt(name="Weak", rank=3, arete=2)
        with self.assertRaises(ValidationError) as ctx:
            periapt.full_clean()
        self.assertIn("Periapt Arete rating must be at least equal to rank", ctx.exception.messages)

    def test_save_refuses_arete_below_rank(self):
        with self.assertRaises(ValidationError):
            Periapt.objects.create(name="Weak", rank=3, arete=2)
        self.assertFalse(Periapt.objects.filter(name="Weak").exists())

    def test_arete_equal_to_rank_is_valid(self):
        periapt = Periapt.objects.create(name="Balanced", rank=3, arete=3)
        self.assertEqual(periapt.arete, 3)

    def test_current_charges_above_max_is_rejected(self):
        periapt = Periapt(name="Overfull", max_charges=2, current_charges=3)
        with self.assertRaises(ValidationError) as ctx:
            periapt.full_clean()
        self.assertIn("Current charges cannot exceed maximum charges", ctx.exception.messages)

    def test_current_charges_equal_to_max_is_valid(self):
        periapt = Periapt.objects.create(name="Full", max_charges=2, current_charges=2)
        self.assertEqual(periapt.current_charges, 2)

    def test_both_rules_are_reported_together(self):
        periapt = Periapt(name="Broken", rank=2, arete=1, max_charges=1, current_charges=5)
        with self.assertRaises(ValidationError) as ctx:
            periapt.full_clean()
        self.assertEqual(len(ctx.exception.messages), 2)

    def test_create_view_shows_rule_as_form_error(self):
        user = User.objects.create_user(username="maker", password="password")
        self.client.force_login(user)
        response = self.client.post(
            Periapt.get_creation_url(),
            {
                "name": "Weak Periapt",
                "description": "Too little Arete",
                "rank": 3,
                "background_cost": 0,
                "quintessence_max": 0,
                "arete": 1,
                "max_charges": 1,
                "current_charges": 1,
                "is_consumable": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Periapt Arete rating must be at least equal to rank",
            response.context["form"].non_field_errors(),
        )
        self.assertContains(response, "Periapt Arete rating must be at least equal to rank")
        self.assertFalse(Periapt.objects.filter(name="Weak Periapt").exists())

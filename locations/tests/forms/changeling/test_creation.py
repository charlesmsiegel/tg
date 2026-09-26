"""Tests for the multi-step Freehold creation forms."""

from django.test import TestCase

from locations.forms.changeling.creation import FreeholdPowersForm
from locations.models.changeling.freehold import Freehold, PowerChoices


class TestFreeholdPowersForm(TestCase):
    """Step 3 offers PowerChoices as checkboxes and saves the chosen list."""

    def setUp(self):
        self.freehold = Freehold.objects.create(name="Step Three", archetype="homestead")

    def test_powers_field_offers_power_choices(self):
        form = FreeholdPowersForm(instance=self.freehold)
        self.assertEqual(list(form.fields["powers"].choices), list(PowerChoices.choices))
        self.assertFalse(form.fields["powers"].required)
        html = str(form["powers"])
        for value, _label in PowerChoices.choices:
            self.assertIn(f'value="{value}"', html)

    def test_chosen_powers_are_saved(self):
        form = FreeholdPowersForm(
            data={"powers": ["warning_call", "glamour_to_dross"]}, instance=self.freehold
        )
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.freehold.refresh_from_db()
        self.assertEqual(self.freehold.powers, ["warning_call", "glamour_to_dross"])
        self.assertTrue(self.freehold.has_power("glamour_to_dross"))

    def test_unknown_power_is_rejected(self):
        form = FreeholdPowersForm(data={"powers": ["not_a_power"]}, instance=self.freehold)
        self.assertFalse(form.is_valid())
        self.assertIn("powers", form.errors)

    def test_dual_nature_still_requires_second_archetype(self):
        form = FreeholdPowersForm(data={"powers": ["dual_nature"]}, instance=self.freehold)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Dual Nature power requires selecting a second archetype",
            form.non_field_errors(),
        )

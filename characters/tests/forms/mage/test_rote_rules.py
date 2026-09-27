"""RoteCreationForm.clean(): the rote choice rules, one case per message."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.mage.rote import RoteCreationForm
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage.focus import Practice
from characters.models.mage.mage import Mage, PracticeRating
from characters.models.mage.rote import Rote
from characters.services.rotes import learn_rote


class RoteRuleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="rote-rules")
        cls.attribute = Attribute.objects.create(name="Wits", property_name="wits")
        cls.ability = Ability.objects.create(name="Occult", property_name="occult")
        cls.practice = Practice.objects.create(name="Chaos Magick")
        cls.practice.abilities.add(cls.ability)

    def setUp(self):
        self.mage = Mage.objects.create(
            name="Rules Mage", owner=self.user, arete=3, forces=2, rote_points=6
        )
        PracticeRating.objects.create(mage=self.mage, practice=self.practice, rating=3)

    def complete(self, **overrides):
        data = {
            "select_or_create_rote": True,
            "select_or_create_effect": True,
            "name": "Spark",
            "practice": self.practice.pk,
            "attribute": self.attribute.pk,
            "ability": self.ability.pk,
            "description": "A small spark",
            "systems": "Forces 1",
            "forces": 1,
        }
        data.update(overrides)
        return {key: value for key, value in data.items() if value is not None}

    def errors(self, data):
        form = RoteCreationForm(data=data, instance=self.mage)
        self.assertFalse(form.is_valid())
        return form.non_field_errors()

    def test_complete_new_rote_is_valid(self):
        form = RoteCreationForm(data=self.complete(), instance=self.mage)
        self.assertTrue(form.is_valid(), form.errors)

    def test_each_missing_piece_reports_its_message_in_order(self):
        cases = [
            (self.complete(select_or_create_effect=None), "Must create or select an effect"),
            (self.complete(name=""), "Must choose rote name"),
            (self.complete(attribute=""), "Must choose rote Attribute"),
            (self.complete(ability=""), "Must choose rote Ability"),
            (self.complete(description=""), "Must choose rote description"),
            (self.complete(systems=""), "Must choose rote systems"),
            (self.complete(forces=0), "Effects must have sphere ratings"),
            (self.complete(name="", description=""), "Must choose rote name"),
        ]
        for data, message in cases:
            with self.subTest(message=message):
                self.assertEqual(self.errors(data), [message])

    def test_missing_practice_is_a_field_error(self):
        # The chained Ability choice depends on the Practice, so it fails first.
        form = RoteCreationForm(data=self.complete(practice=""), instance=self.mage)
        self.assertFalse(form.is_valid())
        self.assertIn("ability", form.errors)

    def test_learning_spends_rote_points_once(self):
        form = RoteCreationForm(data=self.complete(), instance=self.mage)
        self.assertTrue(form.is_valid(), form.errors)
        result = learn_rote(self.mage, form.cleaned_data)
        self.assertTrue(result.success)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.rote_points, 5)
        self.assertEqual(list(self.mage.rotes.values_list("name", flat=True)), ["Spark"])

    def test_learning_uses_the_locked_balance(self):
        form = RoteCreationForm(data=self.complete(forces=2), instance=self.mage)
        self.assertTrue(form.is_valid(), form.errors)
        # Another request spent the points after this form was bound.
        Mage.objects.filter(pk=self.mage.pk).update(rote_points=1)
        result = learn_rote(self.mage, form.cleaned_data)
        self.assertFalse(result.success)
        self.assertEqual(result.error, "Not enough Rote Points")
        self.assertFalse(Rote.objects.filter(name="Spark").exists())

    def test_selecting_a_rote_learned_meanwhile_charges_nothing(self):
        form = RoteCreationForm(data=self.complete(), instance=self.mage)
        self.assertTrue(form.is_valid(), form.errors)
        learn_rote(self.mage, form.cleaned_data)
        rote = Rote.objects.get(name="Spark")
        rote.status = "App"
        rote.save()
        other = Mage.objects.create(name="Other", owner=self.user, arete=3, forces=2)
        PracticeRating.objects.create(mage=other, practice=self.practice, rating=3)
        form = RoteCreationForm(data={"rote_options": rote.pk}, instance=other)
        self.assertTrue(form.is_valid(), form.errors)
        # A concurrent request taught the same rote after this form was bound.
        other.rotes.add(rote)
        result = learn_rote(other, form.cleaned_data)
        self.assertFalse(result.success)
        self.assertEqual(result.error, "Rote already known")
        other.refresh_from_db()
        self.assertEqual(other.rote_points, 6)

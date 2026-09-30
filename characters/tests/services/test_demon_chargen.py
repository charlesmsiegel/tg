"""Tests for characters.services.demon_chargen."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.demon.apocalyptic_form import ApocalypticForm, ApocalypticFormTrait
from characters.models.demon.demon import Demon
from characters.models.demon.visage import Visage
from characters.services.demon_chargen import apply_apocalyptic_form


class ApplyApocalypticFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="fallen_owner")
        self.traits = [ApocalypticFormTrait.objects.create(name=f"T{i}", cost=2) for i in range(10)]

    def apply(self, demon, low, high):
        apply_apocalyptic_form(demon, low, high)
        demon.save()
        return demon.apocalyptic_form

    def test_demons_with_the_same_name_get_separate_forms(self):
        first = Demon.objects.create(name="Azazel", owner=self.user)
        second = Demon.objects.create(name="Azazel", owner=self.user)
        first_form = self.apply(first, self.traits[:4], self.traits[4:8])
        second_form = self.apply(second, self.traits[2:6], self.traits[6:10])
        self.assertNotEqual(first_form.pk, second_form.pk)
        self.assertEqual(set(first_form.low_torment_traits.all()), set(self.traits[:4]))

    def test_reapplying_edits_the_demons_own_form(self):
        demon = Demon.objects.create(name="Belial", owner=self.user)
        form = self.apply(demon, self.traits[:4], self.traits[4:8])
        again = self.apply(demon, self.traits[2:6], self.traits[6:10])
        self.assertEqual(form.pk, again.pk)
        self.assertEqual(set(again.low_torment_traits.all()), set(self.traits[2:6]))
        self.assertEqual(ApocalypticForm.objects.count(), 1)

    def test_a_visage_default_form_is_never_edited(self):
        default = ApocalypticForm.objects.create(name="Default form")
        default.low_torment_traits.set(self.traits[:4])
        Visage.objects.create(name="Test Visage", default_apocalyptic_form=default)
        demon = Demon.objects.create(name="Lilith", owner=self.user, apocalyptic_form=default)
        form = self.apply(demon, self.traits[4:8], self.traits[:4])
        self.assertNotEqual(form.pk, default.pk)
        self.assertEqual(set(default.low_torment_traits.all()), set(self.traits[:4]))

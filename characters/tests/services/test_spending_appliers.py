"""Appliers for Arts, Realms, Virtues and Hekau paths.

These traits have no model of their own: Arts and Realms are ``Statistic`` rows and
Virtues and Hekau paths are built-in fields, so the appliers resolve the stored
display name themselves.
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.changeling.changeling import Changeling
from characters.models.core.statistic import Statistic
from characters.models.mummy.mummy import Mummy
from characters.models.vampire.vampire import Vampire
from characters.services.freebie_spending import FreebieSpendingServiceFactory
from characters.services.xp_spending import XPSpendingServiceFactory
from game.models import FreebieSpendingRecord, XPSpendingRequest

CASES = (
    # (model, trait type, stored display name, property, Statistic row needed)
    (Changeling, "art", "Chicanery", "chicanery", True),
    (Changeling, "realm", "Actor", "actor", True),
    (Vampire, "virtue", "Conscience", "conscience", False),
    (Mummy, "hekau", "Alchemy", "alchemy", False),
)


class SpendingApplierTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.player = User.objects.create_user(username="applier-player")
        cls.storyteller = User.objects.create_user(username="applier-st")
        for _, _, name, property_name, is_statistic in CASES:
            if is_statistic:
                Statistic.objects.create(name=name, property_name=property_name)

    def character(self, model, property_name, value):
        return model.objects.create(
            name=f"{model.__name__} spender",
            owner=self.player,
            xp=20,
            freebies=10,
            **{property_name: value},
        )

    def test_xp_apply_raises_the_trait(self):
        for model, trait_type, name, property_name, _ in CASES:
            with self.subTest(trait_type=trait_type):
                character = self.character(model, property_name, 1)
                request = XPSpendingRequest.objects.create(
                    character=character,
                    trait_name=name,
                    trait_type=trait_type,
                    trait_value=2,
                    cost=4,
                    approved="Pending",
                )
                result = XPSpendingServiceFactory.get_service(character).apply(
                    request, self.storyteller
                )
                self.assertTrue(result.success, result.error)
                character.refresh_from_db()
                request.refresh_from_db()
                self.assertEqual(getattr(character, property_name), 2)
                self.assertEqual(request.approved, "Approved")

    def test_freebie_deny_reverts_the_trait(self):
        for model, trait_type, name, property_name, _ in CASES:
            with self.subTest(trait_type=trait_type):
                character = self.character(model, property_name, 2)
                record = FreebieSpendingRecord.objects.create(
                    character=character,
                    trait_name=name,
                    trait_type=trait_type,
                    trait_value=2,
                    cost=5,
                    approved="Pending",
                )
                result = FreebieSpendingServiceFactory.get_service(character).deny(
                    record, self.storyteller
                )
                self.assertTrue(result.success, result.error)
                character.refresh_from_db()
                self.assertEqual(getattr(character, property_name), 1)

    def test_freebie_apply_marks_the_record_approved(self):
        for model, trait_type, name, property_name, _ in CASES:
            with self.subTest(trait_type=trait_type):
                character = self.character(model, property_name, 2)
                record = FreebieSpendingRecord.objects.create(
                    character=character,
                    trait_name=name,
                    trait_type=trait_type,
                    trait_value=2,
                    cost=5,
                    approved="Pending",
                )
                result = FreebieSpendingServiceFactory.get_service(character).apply(
                    record, self.storyteller
                )
                self.assertTrue(result.success, result.error)
                record.refresh_from_db()
                self.assertEqual(record.approved, "Approved")
                self.assertEqual(record.approved_by, self.storyteller)

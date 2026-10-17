from django.db import IntegrityError, transaction
from django.test import TestCase

from characters.models.mummy.dynasty import Dynasty


class DynastySeedIdentityTests(TestCase):
    def test_unseeded_dynasties_have_independent_null_keys(self):
        first = Dynasty.objects.create(name="First")
        second = Dynasty.objects.create(name="Second")
        self.assertIsNone(first.seed_key)
        self.assertIsNone(second.seed_key)

    def test_database_rejects_duplicate_seed_keys(self):
        Dynasty.objects.create(name="First", seed_key="mummy.dynasty.old_kingdom_1")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Dynasty.objects.create(name="Second", seed_key="mummy.dynasty.old_kingdom_1")

    def test_identity_is_not_editable_content(self):
        field = Dynasty._meta.get_field("seed_key")
        self.assertFalse(field.editable)
        self.assertTrue(field.null)
        self.assertEqual(field.max_length, 150)

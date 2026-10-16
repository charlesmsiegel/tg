from django.db import IntegrityError, transaction
from django.test import TestCase

from characters.models.mummy.mummy_title import MummyTitle


class MummyTitleSeedIdentityTests(TestCase):
    def test_unseeded_titles_have_independent_null_keys(self):
        first = MummyTitle.objects.create(name="First")
        second = MummyTitle.objects.create(name="Second")
        self.assertIsNone(first.seed_key)
        self.assertIsNone(second.seed_key)

    def test_database_rejects_duplicate_seed_keys(self):
        MummyTitle.objects.create(name="First", seed_key="mummy.title.pharaoh")
        with self.assertRaises(IntegrityError), transaction.atomic():
            MummyTitle.objects.create(name="Second", seed_key="mummy.title.pharaoh")

    def test_identity_is_not_editable_content(self):
        field = MummyTitle._meta.get_field("seed_key")
        self.assertFalse(field.editable)
        self.assertTrue(field.null)
        self.assertEqual(field.max_length, 150)

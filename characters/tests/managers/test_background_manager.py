"""Background totals retain allowed-name semantics without one query per name."""

from django.test import TestCase

from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human


class BackgroundManagerTotalsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.character = Human.objects.create(name="Background owner")
        foreign = Human.objects.create(name="Other character")
        contacts = Background.objects.create(name="Contacts", property_name="contacts")
        other_contacts = Background.objects.create(name="Other Contacts", property_name="contacts")
        resources = Background.objects.create(name="Resources", property_name="resources")
        unrelated = Background.objects.create(name="Unrelated", property_name="unrelated")
        BackgroundRating.objects.create(char=cls.character, bg=contacts, rating=3)
        BackgroundRating.objects.create(char=cls.character, bg=contacts, rating=2, note="Work")
        BackgroundRating.objects.create(char=cls.character, bg=other_contacts, rating=1)
        BackgroundRating.objects.create(char=cls.character, bg=resources, rating=0)
        BackgroundRating.objects.create(char=cls.character, bg=unrelated, rating=7)
        BackgroundRating.objects.create(char=foreign, bg=contacts, rating=9)

    def setUp(self):
        self.character.allowed_backgrounds = [
            "mentor",
            "contacts",
            "resources",
            "contacts",
            "absent",
        ]

    def test_totals_preserve_allowed_order_missing_zero_and_duplicate_names(self):
        totals = self.character.get_backgrounds()
        self.assertEqual(list(totals), ["mentor", "contacts", "resources", "absent"])
        self.assertEqual(totals, {"mentor": 0, "contacts": 6, "resources": 0, "absent": 0})

    def test_all_allowed_totals_use_one_query(self):
        with self.assertNumQueries(1):
            totals = self.character.get_backgrounds()
        self.assertEqual(totals["contacts"], 6)

    def test_empty_allowed_names_need_no_query(self):
        self.character.allowed_backgrounds = []
        with self.assertNumQueries(0):
            self.assertEqual(self.character.get_backgrounds(), {})

    def test_single_background_reader_still_includes_names_outside_allowed_list(self):
        self.assertEqual(self.character.total_background_rating("unrelated"), 7)
        self.assertEqual(self.character.total_background_rating("contacts"), 6)

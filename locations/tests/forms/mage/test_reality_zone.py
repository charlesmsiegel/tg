"""Shared zone form behavior preserves zone identities and independent names."""

from django.test import TestCase

from characters.models.mage.focus import Practice
from locations.forms.mage.demesne import DemesneForm
from locations.forms.mage.node import NodeForm
from locations.forms.mage.sanctum import SanctumForm
from locations.models.mage import Demesne, Node, Sanctum
from locations.models.mage.reality_zone import RealityZone, ZoneRating


class RealityZonePlaceFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.positive = Practice.objects.create(name="Positive Practice")
        cls.negative = Practice.objects.create(name="Negative Practice")

    def data(self, **changes):
        data = {
            "name": "Secret place name",
            "rank": 1,
            "description": "A private place",
            "size": 0,
            "ratio": 0,
            "accessibility": "moderate",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
            "resonance-TOTAL_FORMS": "1",
            "resonance-INITIAL_FORMS": "0",
            "resonance-0-resonance": "Dynamic",
            "resonance-0-rating": "1",
            "merit_flaw-TOTAL_FORMS": "0",
            "merit_flaw-INITIAL_FORMS": "0",
            "reality_zone-TOTAL_FORMS": "2",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-0-practice": self.positive.pk,
            "reality_zone-0-rating": "1",
            "reality_zone-1-practice": self.negative.pk,
            "reality_zone-1-rating": "-1",
        }
        data.update(changes)
        return data

    def test_new_zones_never_copy_place_names(self):
        for form_class in (NodeForm, SanctumForm, DemesneForm):
            with self.subTest(form=form_class):
                form = form_class(data=self.data())
                self.assertTrue(form.is_valid(), form.errors)
                place = form.save()
                self.assertEqual(place.reality_zone.name, "Reality Zone")
                self.assertEqual(ZoneRating.objects.filter(zone=place.reality_zone).count(), 2)

    def test_saving_places_preserves_staff_zone_name_and_shared_identity(self):
        for model, form_class in ((Node, NodeForm), (Sanctum, SanctumForm), (Demesne, DemesneForm)):
            with self.subTest(model=model):
                zone = RealityZone.objects.create(name="Staff's independent name")
                place = model.objects.create(name="Original place", rank=1, reality_zone=zone)
                shared = Sanctum.objects.create(name="Sharing place", reality_zone=zone)
                form = form_class(instance=place, data=self.data())
                self.assertTrue(form.is_valid(), form.errors)
                count = RealityZone.objects.count()
                saved = form.save()
                zone.refresh_from_db()
                shared.refresh_from_db()
                self.assertEqual(zone.name, "Staff's independent name")
                self.assertEqual(saved.reality_zone_id, zone.pk)
                self.assertEqual(shared.reality_zone_id, zone.pk)
                self.assertEqual(RealityZone.objects.count(), count)

    def test_commit_false_writes_no_zone_or_ratings(self):
        for form_class in (NodeForm, SanctumForm, DemesneForm):
            with self.subTest(form=form_class):
                form = form_class(data=self.data())
                self.assertTrue(form.is_valid(), form.errors)
                form.save(commit=False)
                self.assertFalse(RealityZone.objects.exists())
                self.assertFalse(ZoneRating.objects.exists())

    def test_rank_balance_error_names_the_actual_place_type(self):
        for form_class, label in (
            (NodeForm, "Node"),
            (SanctumForm, "Sanctum"),
            (DemesneForm, "Demesne"),
        ):
            with self.subTest(form=form_class):
                form = form_class(
                    data=self.data(**{"reality_zone-0-rating": "2", "reality_zone-1-rating": "-2"})
                )
                self.assertFalse(form.is_valid())
                self.assertIn(
                    f"Positive Reality Zone Ratings must sum to {label} rating",
                    form.non_field_errors(),
                )

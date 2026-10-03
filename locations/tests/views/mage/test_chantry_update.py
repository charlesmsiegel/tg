"""The direct chantry edit form: scoped-ST access and a lossless round trip."""

from unittest import mock

from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict, modelform_factory
from django.test import TestCase

from characters.models.core.background_block import Background
from characters.models.core.human import Human
from characters.models.mage.cabal import Cabal
from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from locations.forms.mage.chantry import funded
from locations.models.core.location import LocationModel
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.services import chantry_points
from locations.tests.views.mage.chantry_fixtures import add_chantry_actors, submitted_values
from locations.views.mage.chantry import ChantryUpdateView


class ChantryUpdateAccessTests(TestCase):
    def setUp(self):
        add_chantry_actors(self)
        self.chantry = Chantry.objects.create(
            name="Guarded",
            owner=self.player,
            chronicle=self.chronicle,
            status="Un",
            total_points=10,
        )
        self.url = self.chantry.get_update_url()

    def test_owner_of_a_draft_is_refused(self):
        self.client.force_login(self.player)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        response = self.client.post(self.url, {"name": "Guarded", "total_points": 99})
        self.assertEqual(response.status_code, 403)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.total_points, 10)

    def test_wrong_chronicle_and_wrong_gameline_sts_are_refused(self):
        for user in (self.other_st, self.vampire_st):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_scoped_st_and_staff_get_the_form(self):
        for user in (self.st, self.staff):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_changing_type_to_library_grants_library_dots(self):
        Background.objects.get_or_create(name="Library", property_name="library")
        self.client.force_login(self.st)
        data = submitted_values(self.client.get(self.url))
        data["chantry_type"] = ["library"]
        self.assertEqual(self.client.post(self.url, data).status_code, 302)
        self.assertEqual(self.chantry.backgrounds.get(bg__property_name="library").rating, 3)


class ChantryUpdateRoundTripTests(TestCase):
    """Regression: fields missing from form.html used to be blanked on save."""

    def setUp(self):
        add_chantry_actors(self)
        people = [Human.objects.create(name=f"Person {i}") for i in range(8)]
        self.chantry = Chantry.objects.create(
            name="Full",
            owner=self.player,
            chronicle=self.chronicle,
            status="App",
            description="Old stones",
            faction=MageFaction.objects.create(name="Order of Hermes"),
            leadership_type="democracy",
            season="spring",
            chantry_type="war",
            total_points=25,
            gauntlet=4,
            shroud=5,
            dimension_barrier=3,
            ambassador=people[0],
            node_tender=people[1],
        )
        self.chantry.contained_within.add(LocationModel.objects.create(name="City"))
        self.chantry.integrated_effects.add(Effect.objects.create(name="Ward", prime=1))
        self.chantry.leaders.add(people[2])
        self.chantry.members.add(people[3], people[4])
        self.chantry.cabals.add(Cabal.objects.create(name="Cabal"))
        self.chantry.investigator.add(people[5])
        self.chantry.guardian.add(people[6])
        self.chantry.teacher.add(people[7])
        self.url = self.chantry.get_update_url()

    def snapshot(self):
        chantry = Chantry.objects.get(pk=self.chantry.pk)
        values = model_to_dict(chantry, fields=ChantryUpdateView.fields)
        return {
            name: sorted(x.pk for x in value) if isinstance(value, list) else value
            for name, value in values.items()
        }

    def test_every_field_is_rendered_and_nothing_else(self):
        self.client.force_login(self.st)
        rendered = set(submitted_values(self.client.get(self.url)))
        self.assertEqual(rendered, set(ChantryUpdateView.fields))
        for name in ("gauntlet", "shroud", "dimension_barrier"):
            self.assertIn(name, ChantryUpdateView.fields)

    def test_saving_the_unchanged_form_keeps_every_field(self):
        before = self.snapshot()
        self.client.force_login(self.st)
        data = submitted_values(self.client.get(self.url))
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.snapshot(), before)


class ChantryUpdateFundingTests(TestCase):
    """The direct form may not lower ``total_points`` below what is already spent."""

    def setUp(self):
        add_chantry_actors(self)
        self.chantry = Chantry.objects.create(
            name="Funded",
            owner=self.player,
            chronicle=self.chronicle,
            status="Un",
            total_points=12,
        )
        sanctum, _ = Background.objects.get_or_create(
            property_name="sanctum", defaults={"name": "Sanctum"}
        )
        ChantryBackgroundRating.objects.create(chantry=self.chantry, bg=sanctum, rating=2)  # 10
        self.url = self.chantry.get_update_url()
        self.client.force_login(self.st)
        self.data = submitted_values(self.client.get(self.url))

    def test_a_total_below_the_spent_points_is_a_form_error(self):
        """Edited together with another field, the total is still checked and nothing saves."""
        self.data["total_points"] = ["9"]
        self.data["name"] = ["Renamed"]
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_points", response.context["form"].errors)
        self.chantry.refresh_from_db()
        self.assertEqual((self.chantry.name, self.chantry.total_points), ("Funded", 12))

    def test_a_total_equal_to_the_spent_points_is_saved(self):
        self.data["total_points"] = ["10"]
        self.assertEqual(self.client.post(self.url, self.data).status_code, 302)
        self.chantry.refresh_from_db()
        self.assertEqual((self.chantry.total_points, self.chantry.points), (10, 0))

    def test_a_negative_total_is_a_form_error(self):
        self.data["total_points"] = ["-1"]
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_points", response.context["form"].errors)

    def test_the_total_is_written_by_the_service_under_its_lock(self):
        """Points spent between validation and save are seen at save time."""
        form_class = funded(modelform_factory(Chantry, fields=ChantryUpdateView.fields))
        self.data["total_points"] = ["13"]
        form = form_class(
            {k: v[0] if len(v) == 1 else v for k, v in self.data.items()},
            instance=Chantry.objects.get(pk=self.chantry.pk),
        )
        self.assertTrue(form.is_valid(), form.errors)
        sanctum = Background.objects.get(property_name="sanctum")
        ChantryBackgroundRating.objects.get(chantry=self.chantry, bg=sanctum).delete()
        ChantryBackgroundRating.objects.create(chantry=self.chantry, bg=sanctum, rating=3)  # 15
        with self.assertRaises(ValidationError):
            form.save()
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.total_points, 12)

    def test_save_writes_only_the_form_fields(self):
        """update_fields: an attribute set on the instance outside the form is not persisted."""
        form_class = funded(modelform_factory(Chantry, fields=ChantryUpdateView.fields))
        self.data["name"] = ["Renamed"]
        form = form_class(
            {k: v[0] if len(v) == 1 else v for k, v in self.data.items()},
            instance=Chantry.objects.get(pk=self.chantry.pk),
        )
        self.assertTrue(form.is_valid(), form.errors)
        form.instance.creation_status = 5  # not a form field
        form.save()
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.name, "Renamed")  # a parent-table field
        self.assertEqual(
            self.chantry.gauntlet, int(self.data["gauntlet"][0])
        )  # a child-table field
        self.assertEqual(self.chantry.creation_status, 1)

    def test_a_total_matching_the_stored_one_never_reaches_the_service(self):
        """Only the ModelForm's update_fields write runs; total_points is not among them."""
        self.data["name"] = ["Renamed"]
        with mock.patch.object(chantry_points, "set_total_points") as set_total:
            self.assertEqual(self.client.post(self.url, self.data).status_code, 302)
        set_total.assert_not_called()
        self.chantry.refresh_from_db()
        self.assertEqual((self.chantry.name, self.chantry.total_points), ("Renamed", 12))

    def test_an_edited_total_is_absolute_and_replaces_a_concurrent_join(self):
        """Documented: an edit-the-total form cannot preserve points joined after page load."""
        chantry_points.add_points(self.chantry, 3)  # a character joined after the page loaded
        self.data["total_points"] = ["20"]
        self.assertEqual(self.client.post(self.url, self.data).status_code, 302)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.total_points, 20)

    def test_an_edited_total_is_written_by_the_service(self):
        self.data["total_points"] = ["30"]
        with mock.patch.object(
            chantry_points, "set_total_points", wraps=chantry_points.set_total_points
        ) as set_total:
            self.assertEqual(self.client.post(self.url, self.data).status_code, 302)
        set_total.assert_called_once()
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.total_points, 30)

    def test_an_unchanged_total_is_not_rechecked(self):
        """Pre-existing overspend blocks only an edit of the total, not unrelated edits."""
        Chantry.objects.filter(pk=self.chantry.pk).update(total_points=4)  # 10 spent
        self.data = submitted_values(self.client.get(self.url))
        self.data["name"] = ["Renamed"]
        self.assertEqual(self.client.post(self.url, self.data).status_code, 302)
        self.chantry.refresh_from_db()
        self.assertEqual((self.chantry.name, self.chantry.total_points), ("Renamed", 4))

    def test_a_funding_error_at_save_time_is_a_form_error_and_saves_nothing(self):
        self.data["total_points"] = ["20"]
        self.data["name"] = ["Renamed"]
        with mock.patch.object(
            chantry_points, "set_total_points", side_effect=ValidationError("Spent meanwhile.")
        ):
            response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Spent meanwhile.", response.context["form"].errors["total_points"])
        # The page's object shows the stored chantry, not the refused edits.
        self.assertEqual(response.context["object"].name, "Funded")
        self.assertEqual(response.context["object"].total_points, 12)
        self.chantry.refresh_from_db()
        self.assertEqual((self.chantry.name, self.chantry.total_points), ("Funded", 12))

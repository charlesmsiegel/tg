"""Reality zones must not disclose names copied from private places."""

from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ValidationError
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from characters.models.core.human import Human
from characters.models.mage.focus import CorruptedPractice, Practice, SpecializedPractice
from core.constants import CharacterStatus
from core.models import Observer
from core.permissions import Permission, PermissionManager
from game.models import Chronicle, Gameline, STRelationship
from locations.models.mage import Demesne, HorizonRealm, Node, Sanctum, Sector
from locations.models.mage.reality_zone import RealityZone, ZoneRating


class RealityZoneVisibilityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user("zone_owner")
        cls.other = User.objects.create_user("zone_other")
        cls.staff = User.objects.create_user("zone_staff", is_staff=True)
        cls.st = User.objects.create_user("zone_st")
        cls.wrong_st = User.objects.create_user("zone_wrong_st")
        cls.player = User.objects.create_user("zone_player")
        cls.observer = User.objects.create_user("zone_observer")
        cls.chronicle = Chronicle.objects.create(name="Private Chronicle")
        other_chronicle = Chronicle.objects.create(name="Other Chronicle")
        line = Gameline.objects.create(name="Mage: the Ascension")
        STRelationship.objects.create(user=cls.st, chronicle=cls.chronicle, gameline=line)
        STRelationship.objects.create(user=cls.wrong_st, chronicle=other_chronicle, gameline=line)
        Human.objects.create(name="Player", owner=cls.player, chronicle=cls.chronicle)
        cls.standalone = RealityZone.objects.create(name="Independent Zone")
        cls.list_url = reverse("locations:mage:list:reality_zone")

    def make_zone(self, model, **overrides):
        name = f"Private {model.__name__}"
        zone = RealityZone.objects.create(name=name, description="Private zone description")
        place = model.objects.create(
            name=name,
            owner=self.owner,
            chronicle=self.chronicle,
            status=CharacterStatus.UNAPPROVED,
            reality_zone=zone,
            **overrides,
        )
        return zone, place

    def test_anonymous_cannot_read_existing_copied_names_for_any_place_type(self):
        for model in (Node, Sanctum, Demesne, HorizonRealm, Sector):
            with self.subTest(model=model):
                zone, _ = self.make_zone(model)
                self.assertNotContains(self.client.get(self.list_url), zone.name)
                response = self.client.get(zone.get_absolute_url())
                self.assertEqual(response.status_code, 404)
                self.assertNotContains(response, zone.name, status_code=404)

    def test_standalone_zone_remains_public(self):
        self.assertContains(self.client.get(self.list_url), self.standalone.name)
        self.assertContains(
            self.client.get(self.standalone.get_absolute_url()), self.standalone.name
        )

    def test_public_parent_card_does_not_make_zone_private_fields_public(self):
        zone, _ = self.make_zone(Sanctum, visibility="PUB")
        self.assertEqual(self.client.get(zone.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(self.list_url), zone.name)

    def test_zone_list_detail_and_permission_agree_for_full_and_partial_audiences(self):
        zone, place = self.make_zone(Demesne)
        Observer.objects.create(content_object=place, user=self.observer)
        for user, allowed in (
            (self.owner, True),
            (self.st, True),
            (self.staff, True),
            (self.other, False),
            (self.wrong_st, False),
            (self.player, False),
            (self.observer, False),
        ):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                self.assertEqual(
                    PermissionManager.user_has_permission(user, zone, Permission.VIEW_FULL),
                    allowed,
                )
                self.assertEqual(
                    PermissionManager.filter_queryset_for_user(user, RealityZone.objects.all())
                    .filter(pk=zone.pk)
                    .exists(),
                    allowed,
                )
                detail = self.client.get(zone.get_absolute_url())
                self.assertEqual(detail.status_code, 200 if allowed else 404)
                listing = self.client.get(self.list_url)
                if allowed:
                    self.assertContains(detail, place.name)
                    self.assertContains(listing, zone.name)
                    self.assertEqual(list(detail.context["applied_locations"]), [place])
                else:
                    self.assertNotContains(listing, zone.name)

    def test_shared_zone_requires_full_access_to_every_linked_place(self):
        zone, _ = self.make_zone(Node)
        Sanctum.objects.create(name="Other private sanctum", owner=self.other, reality_zone=zone)
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(zone.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(self.list_url), zone.name)
        self.client.force_login(self.staff)
        self.assertContains(self.client.get(zone.get_absolute_url()), zone.name)

    def test_hidden_and_missing_zone_have_identical_responses(self):
        zone, _ = self.make_zone(Node)
        hidden = self.client.get(zone.get_absolute_url())
        missing = self.client.get(reverse("locations:mage:reality_zone", kwargs={"pk": 999999}))
        self.assertEqual(
            (hidden.status_code, hidden.content), (missing.status_code, missing.content)
        )

    def test_detail_denial_also_applies_to_head(self):
        zone, _ = self.make_zone(Sanctum)
        self.assertEqual(self.client.head(zone.get_absolute_url()).status_code, 404)

    def test_list_filter_does_not_add_queries_per_zone(self):
        self.make_zone(Node)
        with CaptureQueriesContext(connection) as first:
            self.client.get(self.list_url)
        for index in range(20):
            zone = RealityZone.objects.create(name=f"Private zone {index}")
            Demesne.objects.create(name=f"Private demesne {index}", reality_zone=zone)
        with CaptureQueriesContext(connection) as many:
            response = self.client.get(self.list_url)
        self.assertNotContains(response, "Private zone")
        self.assertEqual(len(first), len(many))
        self.assertLessEqual(len(many), 3)

    def test_detail_query_count_does_not_grow_with_applied_places(self):
        zone, _ = self.make_zone(Sanctum)
        self.client.force_login(self.owner)
        self.client.get(zone.get_absolute_url())  # Warm process-global content types.
        with CaptureQueriesContext(connection) as first:
            self.client.get(zone.get_absolute_url())
        for index in range(20):
            Sanctum.objects.create(
                name=f"Shared place {index}",
                owner=self.owner,
                chronicle=self.chronicle,
                reality_zone=zone,
            )
        with CaptureQueriesContext(connection) as many:
            response = self.client.get(zone.get_absolute_url())
        self.assertContains(response, "Shared place 19")
        self.assertEqual(len(response.context["applied_locations"]), 21)
        self.assertEqual(len(first), len(many))
        self.assertLessEqual(len(many), 16)

    def test_detail_query_count_does_not_grow_with_practice_ratings(self):
        self.client.force_login(self.owner)
        zone, _ = self.make_zone(Sanctum)
        for index, rating in enumerate((1, -1)):
            practice = Practice.objects.create(name=f"Initial practice {index}")
            ZoneRating.objects.create(zone=zone, practice=practice, rating=rating)
        self.client.get(zone.get_absolute_url())
        with CaptureQueriesContext(connection) as first:
            self.client.get(zone.get_absolute_url())
        for index in range(20):
            practice = Practice.objects.create(name=f"Shared practice {index}")
            ZoneRating.objects.create(zone=zone, practice=practice, rating=1 if index % 2 else -1)
        with CaptureQueriesContext(connection) as many:
            response = self.client.get(zone.get_absolute_url())
        self.assertContains(response, "Shared practice 19")
        self.assertEqual(len(first), len(many))
        self.assertLessEqual(len(many), 16)

    def test_zone_permission_queries_are_fresh_and_one_per_check(self):
        zone, _ = self.make_zone(Sanctum)
        with self.assertNumQueries(1):
            self.assertTrue(
                PermissionManager.user_has_permission(self.owner, zone, Permission.VIEW_FULL)
            )
        with self.assertNumQueries(1):
            self.assertFalse(
                PermissionManager.user_has_permission(self.other, zone, Permission.VIEW_FULL)
            )
        Sanctum.objects.create(name="Other private place", owner=self.other, reality_zone=zone)
        with self.assertNumQueries(1):
            self.assertFalse(
                PermissionManager.user_has_permission(self.owner, zone, Permission.VIEW_FULL)
            )

    def test_practice_join_preserves_existing_base_practice_links(self):
        specialized = SpecializedPractice.objects.create(name="A specialized practice")
        corrupted = CorruptedPractice.objects.create(name="A corrupted practice")
        ZoneRating.objects.create(zone=self.standalone, practice=specialized, rating=1)
        ZoneRating.objects.create(zone=self.standalone, practice=corrupted, rating=-1)
        response = self.client.get(self.standalone.get_absolute_url())
        # A ZoneRating FK uses a base Practice; keep its existing route even for
        # specialized/corrupted rows, whose base detail resolves polymorphically.
        for practice in (specialized, corrupted):
            self.assertContains(
                response,
                f'href="{reverse("characters:mage:practice", args=[practice.pk])}"',
            )

    def test_former_owner_cannot_read_player_zone_after_last_place_is_deleted(self):
        zone, place = self.make_zone(Sanctum)
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(zone.get_absolute_url()).status_code, 200)
        place.delete()
        self.assertEqual(self.client.get(zone.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(self.list_url), zone.name)

    def test_full_view_location_sql_matches_central_permissions(self):
        head = User.objects.create_user("zone_head")
        game_st = User.objects.create_user("zone_game_st")
        other_line_st = User.objects.create_user("zone_other_line_st")
        self.chronicle.head_st = head
        self.chronicle.save()
        self.chronicle.game_storytellers.add(game_st)
        other_line = Gameline.objects.create(name="Vampire: the Masquerade")
        STRelationship.objects.create(
            user=other_line_st, chronicle=self.chronicle, gameline=other_line
        )
        STRelationship.objects.create(user=self.st, chronicle=self.chronicle, gameline=other_line)
        for model in (Node, Sanctum, Demesne, HorizonRealm, Sector):
            zone, place = self.make_zone(model)
            Observer.objects.create(content_object=place, user=self.observer)
            for user in (
                AnonymousUser(),
                self.owner,
                self.other,
                self.st,
                self.wrong_st,
                self.player,
                self.observer,
                self.staff,
                head,
                game_st,
                other_line_st,
            ):
                with self.subTest(model=model, user=user):
                    expected = PermissionManager.user_has_permission(
                        user, place, Permission.VIEW_FULL
                    )
                    readable = PermissionManager.filter_full_view_locations_for_user(
                        user, model.objects.filter(pk=place.pk)
                    )
                    self.assertEqual(list(readable), [place] if expected else [])
                    self.assertEqual(
                        PermissionManager.user_has_permission(user, zone, Permission.VIEW_FULL),
                        expected,
                    )

    def test_sector_create_choices_hide_private_zones_and_reject_forged_selection(self):
        zone, _ = self.make_zone(Sanctum)
        # A previous name copied before the place was renamed distinguishes
        # the zone selector from other, unrelated location selectors.
        zone.name = "Historical private zone name"
        zone.save()
        self.client.force_login(self.other)
        response = self.client.get(reverse("locations:mage:create:sector"))
        self.assertNotContains(response, zone.name)
        self.assertContains(response, self.standalone.name)
        field = response.context["form"].fields["reality_zone"]
        with self.assertRaisesMessage(ValidationError, "Select a valid choice"):
            field.clean(zone.pk)

    def test_shared_zone_inline_display_cannot_disclose_another_private_place(self):
        zone = RealityZone.objects.create(name="Other owner secret place")
        Sanctum.objects.create(name=zone.name, owner=self.other, reality_zone=zone)
        for model in (Node, Sanctum, Demesne, HorizonRealm, Sector):
            with self.subTest(model=model):
                place = model.objects.create(name="My place", owner=self.owner, reality_zone=zone)
                self.client.force_login(self.owner)
                response = self.client.get(place.get_absolute_url())
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, zone.name)

    def test_anonymous_queryset_includes_only_standalone_zones(self):
        self.make_zone(Demesne)
        self.assertEqual(
            list(
                PermissionManager.filter_queryset_for_user(
                    AnonymousUser(), RealityZone.objects.all()
                )
            ),
            [self.standalone],
        )

    def test_shared_zone_form_is_read_only_and_rejects_forged_nested_edits(self):
        zone, place = self.make_zone(Sanctum)
        Sanctum.objects.create(name="Other private place", owner=self.other, reality_zone=zone)
        positive = Practice.objects.create(name="Private shared practice")
        negative = Practice.objects.create(name="Another shared practice")
        first = ZoneRating.objects.create(zone=zone, practice=positive, rating=1)
        second = ZoneRating.objects.create(zone=zone, practice=negative, rating=-1)
        self.client.force_login(self.owner)
        response = self.client.get(place.get_update_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, positive.name)
        self.assertNotContains(response, 'name="reality_zone-')
        self.assertContains(response, "shared reality zone")
        form = response.context["form"]
        self.assertIsNone(form.reality_zone_formset)
        self.assertTrue(form.fields["rank"].disabled)
        response = self.client.post(
            place.get_update_url(),
            {
                "name": place.name,
                "description": "Must not be partially saved",
                "rank": 2,
                "reality_zone-TOTAL_FORMS": 2,
                "reality_zone-INITIAL_FORMS": 2,
                "reality_zone-0-id": first.pk,
                "reality_zone-0-zone": zone.pk,
                "reality_zone-0-practice": positive.pk,
                "reality_zone-0-rating": 2,
                "reality_zone-1-id": second.pk,
                "reality_zone-1-zone": zone.pk,
                "reality_zone-1-practice": negative.pk,
                "reality_zone-1-rating": -2,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("read-only", str(response.context["form"].non_field_errors()))
        first.refresh_from_db()
        second.refresh_from_db()
        place.refresh_from_db()
        self.assertEqual((first.rating, second.rating), (1, -1))
        self.assertEqual(place.rank, 0)
        self.assertEqual(place.description, "")

    def test_owner_can_edit_parent_description_without_reading_shared_zone(self):
        zone, place = self.make_zone(Sanctum)
        other = Sanctum.objects.create(
            name="Other private place", owner=self.other, reality_zone=zone
        )
        practice = Practice.objects.create(name="Hidden shared practice")
        rating = ZoneRating.objects.create(zone=zone, practice=practice, rating=1)
        self.client.force_login(self.owner)
        response = self.client.post(
            place.get_update_url(), {"name": place.name, "description": "Edited description"}
        )
        self.assertEqual(response.status_code, 302)
        place.refresh_from_db()
        other.refresh_from_db()
        rating.refresh_from_db()
        self.assertEqual(place.description, "Edited description")
        self.assertEqual(place.rank, 0)
        self.assertEqual((place.reality_zone_id, other.reality_zone_id), (zone.pk, zone.pk))
        self.assertEqual(rating.rating, 1)

    def test_staff_can_edit_a_shared_zone_from_its_parent_form(self):
        zone, place = self.make_zone(Sanctum)
        Sanctum.objects.create(name="Other private place", owner=self.other, reality_zone=zone)
        positive = Practice.objects.create(name="Shared positive practice")
        negative = Practice.objects.create(name="Shared negative practice")
        first = ZoneRating.objects.create(zone=zone, practice=positive, rating=1)
        second = ZoneRating.objects.create(zone=zone, practice=negative, rating=-1)
        self.client.force_login(self.staff)
        response = self.client.get(place.get_update_url())
        self.assertContains(response, positive.name)
        self.assertFalse(response.context["form"].fields["rank"].disabled)
        response = self.client.post(
            place.get_update_url(),
            {
                "name": place.name,
                "rank": 2,
                "reality_zone-TOTAL_FORMS": 2,
                "reality_zone-INITIAL_FORMS": 2,
                "reality_zone-0-id": first.pk,
                "reality_zone-0-zone": zone.pk,
                "reality_zone-0-practice": positive.pk,
                "reality_zone-0-rating": 2,
                "reality_zone-1-id": second.pk,
                "reality_zone-1-zone": zone.pk,
                "reality_zone-1-practice": negative.pk,
                "reality_zone-1-rating": -2,
            },
        )
        self.assertEqual(response.status_code, 302)
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertEqual((first.rating, second.rating), (2, -2))

    def test_linking_a_staff_reference_classifies_it_without_automatic_declassification(self):
        zone = self.standalone
        self.assertContains(self.client.get(zone.get_absolute_url()), zone.name)
        place = Sanctum.objects.create(
            name="Private player place", owner=self.owner, reality_zone=zone
        )
        zone.refresh_from_db()
        self.assertTrue(zone.is_player_zone)
        self.assertEqual(self.client.get(zone.get_absolute_url()).status_code, 404)
        place.reality_zone = None
        place.save()
        zone.refresh_from_db()
        self.assertTrue(zone.is_player_zone)
        self.assertEqual(self.client.get(zone.get_absolute_url()).status_code, 404)
        self.client.force_login(self.staff)
        self.assertContains(self.client.get(zone.get_absolute_url()), zone.name)

    def test_deleted_last_place_does_not_publish_its_legacy_zone(self):
        zone, place = self.make_zone(Sanctum)
        place.delete()
        self.assertEqual(self.client.get(zone.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(self.list_url), zone.name)
        self.client.force_login(self.staff)
        self.assertContains(self.client.get(zone.get_absolute_url()), zone.name)

    def test_detaching_or_reassigning_last_place_keeps_old_zone_private(self):
        for reassign in (False, True):
            with self.subTest(reassign=reassign):
                zone, place = self.make_zone(Node)
                replacement = RealityZone.objects.create(name="New standalone reference")
                place.reality_zone = replacement if reassign else None
                place.save()
                self.assertEqual(self.client.get(zone.get_absolute_url()).status_code, 404)
                self.assertNotContains(self.client.get(self.list_url), zone.name)
                if reassign:
                    place.delete()
                    self.assertEqual(
                        self.client.get(replacement.get_absolute_url()).status_code, 404
                    )

    def test_old_zone_name_cannot_be_republished_through_stale_staff_save(self):
        stale = RealityZone.objects.get(pk=self.standalone.pk)
        place = Sanctum.objects.create(name="New private place", reality_zone=self.standalone)
        stale.description = "An independent staff edit"
        stale.save()
        place.delete()
        self.assertEqual(self.client.get(self.standalone.get_absolute_url()).status_code, 404)

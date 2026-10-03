"""Reality zones must not disclose names copied from private places."""

from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ValidationError
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from characters.models.core.human import Human
from characters.models.mage.focus import Practice
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

    def test_parent_zone_form_denies_read_and_write_for_a_shared_private_zone(self):
        zone, place = self.make_zone(Sanctum)
        Sanctum.objects.create(name="Other private place", owner=self.other, reality_zone=zone)
        positive = Practice.objects.create(name="Private shared practice")
        negative = Practice.objects.create(name="Another shared practice")
        first = ZoneRating.objects.create(zone=zone, practice=positive, rating=1)
        second = ZoneRating.objects.create(zone=zone, practice=negative, rating=-1)
        self.client.force_login(self.owner)
        response = self.client.get(place.get_update_url())
        self.assertEqual(response.status_code, 404)
        self.assertNotContains(response, positive.name, status_code=404)
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
        self.assertEqual(response.status_code, 404)
        first.refresh_from_db()
        second.refresh_from_db()
        place.refresh_from_db()
        self.assertEqual((first.rating, second.rating), (1, -1))
        self.assertEqual(place.rank, 0)

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

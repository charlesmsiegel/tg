"""OBJECT_ST_WRITE: the OBJECT_WRITE checks plus a scoped storyteller role."""

from unittest import mock

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase

from core.access_policy import authorize_route, route_name
from core.route_policy_manifest import VIEW_POLICIES
from game.models import Chronicle, Gameline, STRelationship
from locations.models.mage.chantry import Chantry


class _STWriteProbeView:
    """Stands in for a routed view declared OBJECT_ST_WRITE."""

    model = Chantry
    fields = ["name", "total_points"]


class ObjectSTWritePolicyTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("stw_owner")
        self.mage_st = users.objects.create_user("stw_mage_st")
        self.vampire_st = users.objects.create_user("stw_vampire_st")
        self.other_st = users.objects.create_user("stw_other_st")
        self.staff = users.objects.create_user("stw_staff", is_staff=True)
        self.chronicle = Chronicle.objects.create(name="Home")
        other = Chronicle.objects.create(name="Away")
        mage = Gameline.objects.get_or_create(name="Mage: the Ascension")[0]
        vampire = Gameline.objects.get_or_create(name="Vampire: the Masquerade")[0]
        STRelationship.objects.create(user=self.mage_st, chronicle=self.chronicle, gameline=mage)
        STRelationship.objects.create(
            user=self.vampire_st, chronicle=self.chronicle, gameline=vampire
        )
        STRelationship.objects.create(user=self.other_st, chronicle=other, gameline=mage)
        self.chantry = Chantry.objects.create(
            name="Probe", owner=self.owner, chronicle=self.chronicle, status="Un"
        )
        patcher = mock.patch.dict(VIEW_POLICIES, {route_name(_STWriteProbeView): "OBJECT_ST_WRITE"})
        patcher.start()
        self.addCleanup(patcher.stop)

    def authorize(self, user, method="get", data=None):
        request = getattr(RequestFactory(), method)("/", data or {})
        request.user = user
        return authorize_route(request, _STWriteProbeView, kwargs={"pk": self.chantry.pk})

    def test_scoped_st_and_staff_pass(self):
        for user in (self.mage_st, self.staff):
            with self.subTest(user=user.username):
                self.assertIsNone(self.authorize(user))
                self.assertIsNone(self.authorize(user, "post", {"name": "Renamed"}))

    def test_owner_of_a_draft_is_refused(self):
        with self.assertRaises(PermissionDenied):
            self.authorize(self.owner)
        with self.assertRaises(PermissionDenied):
            self.authorize(self.owner, "post", {"total_points": "99"})

    def test_wrong_gameline_and_wrong_chronicle_sts_are_refused(self):
        for user in (self.vampire_st, self.other_st):
            with self.subTest(user=user.username):
                with self.assertRaises(PermissionDenied):
                    self.authorize(user)

    def test_object_write_field_guard_still_applies(self):
        with self.assertRaises(PermissionDenied):
            self.authorize(self.mage_st, "post", {"name": "Probe", "status": "App"})

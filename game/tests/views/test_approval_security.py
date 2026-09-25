from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import TestCase

from characters.models.core.human import Human
from game.models import Chronicle, FreebieSpendingRecord, Gameline, STRelationship


class ApprovalSecurityTests(TestCase):
    def setUp(self):
        from game.spending_approval import decide_spending_request

        self.decide = decide_spending_request
        users = get_user_model()
        self.owner = users.objects.create_user("owner")
        self.st = users.objects.create_user("st")
        self.other_st = users.objects.create_user("other_st")
        self.chronicle = Chronicle.objects.create(name="Chronicle")
        wod = Gameline.objects.create(name="World of Darkness")
        vtm = Gameline.objects.create(name="Vampire: the Masquerade")
        STRelationship.objects.create(user=self.st, chronicle=self.chronicle, gameline=wod)
        STRelationship.objects.create(
            user=self.other_st, chronicle=self.chronicle, gameline=vtm
        )
        self.character = Human.objects.create(
            name="Hero", owner=self.owner, chronicle=self.chronicle
        )
        self.record = FreebieSpendingRecord.objects.create(
            character=self.character,
            trait_name="Trait",
            trait_type="custom",
            trait_value=1,
            cost=1,
        )

    def test_owner_and_wrong_gameline_st_cannot_approve(self):
        for user in (self.owner, self.other_st):
            with self.subTest(user=user.username):
                with self.assertRaises(PermissionDenied):
                    self.decide(FreebieSpendingRecord, self.character, self.record.pk, user, "approve")
        self.record.refresh_from_db()
        self.assertEqual(self.record.approved, "Pending")

    def test_matching_st_approves_once(self):
        result = self.decide(
            FreebieSpendingRecord, self.character, self.record.pk, self.st, "approve"
        )
        self.assertTrue(result.success)
        self.record.refresh_from_db()
        self.assertEqual(self.record.approved, "Approved")
        with self.assertRaises(Http404):
            self.decide(
                FreebieSpendingRecord, self.character, self.record.pk, self.st, "approve"
            )

    def test_st_can_self_approve_npc_only(self):
        self.character.owner = self.st
        self.character.npc = True
        self.character.save()
        result = self.decide(
            FreebieSpendingRecord, self.character, self.record.pk, self.st, "approve"
        )
        self.assertTrue(result.success)

    def test_st_cannot_self_approve_player_character(self):
        self.character.owner = self.st
        self.character.save()
        with self.assertRaises(PermissionDenied):
            self.decide(
                FreebieSpendingRecord, self.character, self.record.pk, self.st, "approve"
            )
        self.record.refresh_from_db()
        self.assertEqual(self.record.approved, "Pending")

    def test_staff_role_alone_does_not_allow_npc_self_approval(self):
        staff = get_user_model().objects.create_user("staff_owner", is_staff=True)
        self.character.owner = staff
        self.character.npc = True
        self.character.save()
        with self.assertRaises(PermissionDenied):
            self.decide(
                FreebieSpendingRecord, self.character, self.record.pk, staff, "approve"
            )

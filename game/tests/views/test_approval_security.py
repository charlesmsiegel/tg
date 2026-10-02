from unittest import mock

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from characters.models.core.human import Human
from game import spending_approval
from game.models import (
    Chronicle,
    FreebieSpendingRecord,
    Gameline,
    STRelationship,
    XPSpendingRequest,
)
from game.spending_approval import (
    SpendingAlreadyDecided,
    SpendingDecisionError,
    decide_spending_request,
)


class ApprovalSecurityTests(TestCase):
    def setUp(self):
        self.decide = decide_spending_request
        users = get_user_model()
        self.owner = users.objects.create_user("owner")
        self.st = users.objects.create_user("st")
        self.other_st = users.objects.create_user("other_st")
        self.chronicle = Chronicle.objects.create(name="Chronicle")
        wod = Gameline.objects.create(name="World of Darkness")
        vtm = Gameline.objects.create(name="Vampire: the Masquerade")
        STRelationship.objects.create(user=self.st, chronicle=self.chronicle, gameline=wod)
        STRelationship.objects.create(user=self.other_st, chronicle=self.chronicle, gameline=vtm)
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
                    self.decide(
                        FreebieSpendingRecord, self.character, self.record.pk, user, "approve"
                    )
        self.record.refresh_from_db()
        self.assertEqual(self.record.approved, "Pending")

    def test_matching_st_approves_once(self):
        result = self.decide(
            FreebieSpendingRecord, self.character, self.record.pk, self.st, "approve"
        )
        self.assertTrue(result.success)
        self.record.refresh_from_db()
        self.assertEqual(self.record.approved, "Approved")
        # A decided record is reported as such to an approver (Step 5, D1).
        with self.assertRaises(SpendingAlreadyDecided):
            self.decide(FreebieSpendingRecord, self.character, self.record.pk, self.st, "approve")

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
            self.decide(FreebieSpendingRecord, self.character, self.record.pk, self.st, "approve")
        self.record.refresh_from_db()
        self.assertEqual(self.record.approved, "Pending")

    def test_staff_role_alone_does_not_allow_npc_self_approval(self):
        staff = get_user_model().objects.create_user("staff_owner", is_staff=True)
        self.character.owner = staff
        self.character.npc = True
        self.character.save()
        with self.assertRaises(PermissionDenied):
            self.decide(FreebieSpendingRecord, self.character, self.record.pk, staff, "approve")

    def test_denial_refunds_onto_the_current_xp(self):
        """A spend that lands while a denial is being checked keeps its deduction: the
        refund is applied to the character as it is now, not as it was first read."""
        Human.objects.filter(pk=self.character.pk).update(xp=10)
        request = XPSpendingRequest.objects.create(
            character=self.character, trait_name="Trait", trait_type="custom", trait_value=1, cost=3
        )
        check = spending_approval.require_spending_approver

        def concurrent_spend(user, character):
            check(user, character)
            Human.objects.filter(pk=character.pk).update(xp=4)

        with mock.patch.object(spending_approval, "require_spending_approver", concurrent_spend):
            self.decide(XPSpendingRequest, self.character, request.pk, self.st, "deny")
        self.character.refresh_from_db()
        self.assertEqual(self.character.xp, 7)

    def test_freebie_denial_whose_revert_fails_raises_and_changes_nothing(self):
        """A revert the service cannot perform (here: no Attribute row named Charisma)
        is reported to the storyteller and leaves the record, trait and freebies as
        they were, so the player cannot keep both the refund and the dot."""
        Human.objects.filter(pk=self.character.pk).update(freebies=5, charisma=3)
        record = FreebieSpendingRecord.objects.create(
            character=self.character,
            trait_name="Charisma",
            trait_type="attribute",
            trait_value=3,
            cost=5,
        )
        with self.assertRaises(SpendingDecisionError):
            self.decide(FreebieSpendingRecord, self.character, record.pk, self.st, "deny")
        record.refresh_from_db()
        self.character.refresh_from_db()
        self.assertEqual(record.approved, "Pending")
        self.assertEqual(self.character.freebies, 5)
        self.assertEqual(self.character.charisma, 3)

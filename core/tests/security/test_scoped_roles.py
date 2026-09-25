from django.contrib.auth import get_user_model
from django.test import TestCase

from characters.models.core.human import Human
from core.permissions import Permission, PermissionManager
from game.models import Chronicle, Gameline, STRelationship


class ScopedPermissionTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user("owner")
        self.matching_st = user_model.objects.create_user("matching_st")
        self.other_gameline_st = user_model.objects.create_user("other_gameline_st")
        self.other_chronicle_st = user_model.objects.create_user("other_chronicle_st")
        self.head_st = user_model.objects.create_user("head_st")
        self.staff = user_model.objects.create_user("staff", is_staff=True)
        self.chronicle = Chronicle.objects.create(name="Home", head_st=self.head_st)
        self.other_chronicle = Chronicle.objects.create(name="Away")
        wod = Gameline.objects.create(name="World of Darkness")
        vampire = Gameline.objects.create(name="Vampire: the Masquerade")
        STRelationship.objects.create(
            user=self.matching_st, chronicle=self.chronicle, gameline=wod
        )
        STRelationship.objects.create(
            user=self.other_gameline_st, chronicle=self.chronicle, gameline=vampire
        )
        STRelationship.objects.create(
            user=self.other_chronicle_st, chronicle=self.other_chronicle, gameline=wod
        )
        self.character = Human.objects.create(
            name="Subject", owner=self.owner, chronicle=self.chronicle
        )

    def test_st_full_read_is_chronicle_scoped(self):
        for user in (self.matching_st, self.other_gameline_st, self.head_st, self.staff):
            with self.subTest(user=user.username):
                self.assertTrue(
                    PermissionManager.user_has_permission(
                        user, self.character, Permission.VIEW_FULL
                    )
                )
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.other_chronicle_st, self.character, Permission.VIEW_FULL
            )
        )

    def test_edit_and_approve_need_matching_gameline(self):
        for permission in (Permission.EDIT_FULL, Permission.APPROVE):
            with self.subTest(permission=permission):
                self.assertTrue(
                    PermissionManager.user_has_permission(
                        self.matching_st, self.character, permission
                    )
                )
                self.assertFalse(
                    PermissionManager.user_has_permission(
                        self.other_gameline_st, self.character, permission
                    )
                )

    def test_owner_can_edit_only_before_approval(self):
        for status, allowed in (("Un", True), ("Rev", True), ("Sub", False), ("App", False)):
            with self.subTest(status=status):
                self.character.status = status
                self.assertEqual(
                    PermissionManager.user_has_permission(
                        self.owner, self.character, Permission.EDIT_FULL
                    ),
                    allowed,
                )
                self.assertTrue(
                    PermissionManager.user_has_permission(
                        self.owner, self.character, Permission.VIEW_FULL
                    )
                )

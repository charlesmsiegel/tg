"""Field and authorization contracts for the shared character CRUD adapters."""

import hashlib
import json
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.utils.module_loading import import_string

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.hunter import HtRHuman
from characters.models.mage.mage import Mage
from characters.views.hunter.htrhuman import HtRHumanDetailView, HtRHumanUpdateView
from characters.views.mage.mage import MageDetailView
from core.permissions import Role
from game.models import Chronicle, Gameline, Scene, STRelationship

BASELINE = json.loads(Path(__file__).with_name("shared_character_crud_baseline.json").read_text())


class CharacterCRUDFieldContracts(SimpleTestCase):
    def test_all_migrated_details_share_character_actions_but_references_do_not(self):
        from characters.views.core.character import CharacterDetailView

        details = {
            "changeling.changeling": "ChangelingDetailView",
            "changeling.ctdhuman": "CtDHumanDetailView",
            "demon.demon": "DemonDetailView",
            "demon.dtfhuman": "DtFHumanDetailView",
            "demon.earthbound": "EarthboundDetailView",
            "demon.thrall": "ThrallDetailView",
            "hunter.htrhuman": "HtRHumanDetailView",
            "hunter.hunter": "HunterDetailView",
            "werewolf.drone": "DroneDetailView",
            "werewolf.fera": "FeraDetailView",
            "werewolf.fomor": "FomorDetailView",
            "werewolf.garou": "WerewolfDetailView",
            "werewolf.kinfolk": "KinfolkDetailView",
            "werewolf.spirit": "SpiritDetailView",
        }
        for module, name in details.items():
            with self.subTest(detail=name):
                self.assertTrue(
                    issubclass(
                        import_string(f"characters.views.{module}.{name}"), CharacterDetailView
                    )
                )
        for path in (
            "changeling.chimera.ChimeraDetailView",
            "werewolf.septposition.SeptPositionDetailView",
            "vampire.clan.VampireClanDetailView",
        ):
            with self.subTest(reference=path):
                self.assertFalse(
                    issubclass(import_string(f"characters.views.{path}"), CharacterDetailView)
                )

    def test_reviewed_field_order_is_preserved(self):
        for path, expected in BASELINE.items():
            if "fields_sha256" not in expected:
                continue
            with self.subTest(view=path):
                # The old Mage list repeated time; ModelForm already deduplicated it.
                fields = list(dict.fromkeys(import_string(path).fields))
                if (
                    path == "characters.views.vampire.vampire.VampireUpdateView"
                    and "current_willpower" not in fields
                ):
                    # The baseline included this nonexistent model field, which
                    # prevented the storyteller's form from being constructed.
                    fields.insert(fields.index("willpower") + 1, "current_willpower")
                self.assertEqual(len(fields), expected["field_count"])
                self.assertEqual(
                    hashlib.sha256("\n".join(fields).encode()).hexdigest(),
                    expected["fields_sha256"],
                )

    def test_all_selectors_preserve_limited_form_identity_and_full_model(self):
        for path, expected in BASELINE.items():
            if "limited_form" not in expected:
                continue
            cls = import_string(path)
            view = cls()
            view.setup(RequestFactory().get("/"))
            view.request.user = object()
            with patch.object(view, "get_object", return_value=cls.model()):
                for editor in (False, True):
                    with (
                        self.subTest(view=path, editor=editor),
                        patch(
                            "core.permissions.PermissionManager.user_has_scoped_editor_role",
                            return_value=editor,
                        ),
                        patch(
                            "core.permissions.PermissionManager.get_user_roles",
                            return_value={Role.ADMIN} if editor else {Role.OWNER},
                        ),
                    ):
                        form = view.get_form_class()
                        if editor:
                            self.assertIs(form._meta.model, cls.model)
                            if cls.fields is not None:
                                self.assertEqual(
                                    list(form.base_fields), list(dict.fromkeys(cls.fields))
                                )
                            else:
                                self.assertIs(form, cls.form_class)
                        else:
                            self.assertIs(
                                form,
                                import_string(
                                    "characters.forms.core.limited_edit." + expected["limited_form"]
                                ),
                            )
                            self.assertNotIn("st_notes", form.base_fields)
                            self.assertNotIn("owner", form.base_fields)
                            self.assertNotIn("status", form.base_fields)

    def test_vampire_full_form_has_only_existing_model_fields(self):
        from characters.views.vampire.vampire import VampireUpdateView

        view = VampireUpdateView()
        view.setup(RequestFactory().get("/"))
        view.request.user = object()
        with (
            patch.object(view, "get_object", return_value=VampireUpdateView.model()),
            patch(
                "core.permissions.PermissionManager.user_has_scoped_editor_role", return_value=True
            ),
        ):
            form = view.get_form_class()
        self.assertIn("willpower", form.base_fields)
        self.assertNotIn("current_willpower", form.base_fields)

    def test_mage_time_is_declared_once(self):
        from characters.views.mage.mage import MageCreateView, MageUpdateView

        self.assertEqual(MageCreateView.FORM_FIELDS.count("time"), 1)
        self.assertEqual(MageUpdateView.fields.count("time"), 1)


class CharacterCRUDSecurityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        users = get_user_model()
        cls.owner = users.objects.create_user("crud-owner")
        cls.st = users.objects.create_user("crud-st")
        cls.wrong_st = users.objects.create_user("crud-wrong-st")
        cls.chronicle = Chronicle.objects.create(name="CRUD chronicle")
        hunter = Gameline.objects.create(name="Hunter: the Reckoning")
        vampire = Gameline.objects.create(name="Vampire: the Masquerade")
        STRelationship.objects.create(user=cls.st, chronicle=cls.chronicle, gameline=hunter)
        STRelationship.objects.create(user=cls.wrong_st, chronicle=cls.chronicle, gameline=vampire)
        cls.character = HtRHuman.objects.create(
            name="Draft hunter", owner=cls.owner, chronicle=cls.chronicle
        )

    def setUp(self):
        self.factory = RequestFactory()
        cache.clear()

    def request(self, user, data=None):
        request = self.factory.get("/") if data is None else self.factory.post("/", data)
        request.user = user
        return request

    def test_owner_and_unrelated_storyteller_receive_limited_form(self):
        for user in (self.owner, self.wrong_st):
            with self.subTest(user=user.username):
                view = HtRHumanUpdateView()
                view.setup(self.request(user), pk=self.character.pk)
                self.assertIs(view.get_form_class(), LimitedHumanEditForm)
        view = HtRHumanUpdateView()
        view.setup(self.request(self.st), pk=self.character.pk)
        self.assertIn("strength", view.get_form_class().base_fields)

    def test_forged_owner_fields_cannot_change_authority_or_stats(self):
        response = HtRHumanUpdateView.as_view()(
            self.request(
                self.owner,
                {
                    "notes": "Draft revision",
                    "strength": "5",
                    "status": "App",
                    "owner": self.st.pk,
                    "st_notes": "Forged",
                    "xp": "999",
                },
            ),
            pk=self.character.pk,
        )
        self.assertEqual(response.status_code, 302)
        self.character.refresh_from_db()
        self.assertEqual(self.character.notes, "Draft revision")
        self.assertEqual(self.character.strength, 1)
        self.assertEqual(self.character.status, "Un")
        self.assertEqual(self.character.owner_id, self.owner.pk)
        self.assertEqual(self.character.st_notes, "")
        self.assertEqual(self.character.xp, 0)

    def test_unrelated_storyteller_cannot_update_direct_view(self):
        with self.assertRaises(PermissionDenied):
            HtRHumanUpdateView.as_view()(
                self.request(self.wrong_st, {"strength": "5"}), pk=self.character.pk
            )

    def test_vampire_family_rejects_locked_owner_and_unrelated_direct_writes(self):
        from characters.views.vampire.ghoul import GhoulUpdateView
        from characters.views.vampire.revenant import RevenantUpdateView
        from characters.views.vampire.vampire import VampireUpdateView

        for view in (GhoulUpdateView, RevenantUpdateView, VampireUpdateView):
            character = view.model.objects.create(
                name=view.__name__, owner=self.owner, status="App"
            )
            for user in (self.owner, self.st):
                with (
                    self.subTest(view=view.__name__, user=user.username),
                    self.assertRaises(PermissionDenied),
                ):
                    view.as_view()(self.request(user, {"notes": "Forbidden"}), pk=character.pk)
            character.refresh_from_db()
            self.assertEqual(character.notes, "")

    def test_owner_can_retire_through_gameline_detail(self):
        response = HtRHumanDetailView.as_view()(
            self.request(self.owner, {"retire": "1"}), pk=self.character.pk
        )
        self.assertEqual(response.status_code, 302)
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "Ret")

    def test_only_matching_storyteller_can_decease(self):
        HtRHuman.objects.filter(pk=self.character.pk).update(status="App")
        HtRHumanDetailView.as_view()(
            self.request(self.owner, {"decease": "1"}), pk=self.character.pk
        )
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "App")
        HtRHumanDetailView.as_view()(
            self.request(self.wrong_st, {"decease": "1"}), pk=self.character.pk
        )
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "App")
        HtRHumanDetailView.as_view()(self.request(self.st, {"decease": "1"}), pk=self.character.pk)
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "Dec")

    def test_deceased_mage_cannot_be_retired(self):
        mage = Mage.objects.create(name="Deceased mage", owner=self.owner, status="Dec")
        response = MageDetailView.as_view()(self.request(self.owner, {"retire": "1"}), pk=mage.pk)
        self.assertEqual(response.status_code, 302)
        mage.refresh_from_db()
        self.assertEqual(mage.status, "Dec")

    def test_unsupported_decease_action_is_hidden(self):
        for status in ("Un", "Sub", "Rev", "Ret", "Dec"):
            with self.subTest(status=status):
                HtRHuman.objects.filter(pk=self.character.pk).update(status=status)
                response = HtRHumanDetailView.as_view()(self.request(self.st), pk=self.character.pk)
                self.assertFalse(response.context_data["can_decease"])

    def test_unsupported_decease_post_leaves_status_unchanged(self):
        for status in ("Un", "Sub", "Rev", "Ret", "Dec"):
            with self.subTest(status=status):
                HtRHuman.objects.filter(pk=self.character.pk).update(status=status)
                response = HtRHumanDetailView.as_view()(
                    self.request(self.st, {"decease": "1"}), pk=self.character.pk
                )
                self.assertEqual(response.status_code, 302)
                self.character.refresh_from_db()
                self.assertEqual(self.character.status, status)

    def test_shared_scene_context_filters_current_audience_after_cache_warmup(self):
        visible = Scene.objects.create(
            name="Visible scene", chronicle=self.chronicle, visibility=Scene.Visibility.PUBLIC
        )
        other_chronicle = Chronicle.objects.create(name="Other chronicle")
        hidden = Scene.objects.create(
            name="Hidden scene", chronicle=other_chronicle, visibility=Scene.Visibility.PARTICIPANTS
        )
        visible.characters.add(self.character)
        hidden.characters.add(self.character)
        owner_response = HtRHumanDetailView.as_view()(
            self.request(self.owner), pk=self.character.pk
        )
        self.assertEqual(
            {scene.pk for scene in owner_response.context_data["scenes"]}, {visible.pk, hidden.pk}
        )
        st_response = HtRHumanDetailView.as_view()(self.request(self.st), pk=self.character.pk)
        self.assertEqual([scene.pk for scene in st_response.context_data["scenes"]], [visible.pk])

    def test_public_route_still_uses_safe_projection(self):
        HtRHuman.objects.filter(pk=self.character.pk).update(
            visibility="public", public_info="Public biography", st_notes="Secret storyteller notes"
        )
        response = self.client.get(self.character.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Public biography")
        self.assertNotContains(response, "Secret storyteller notes")
        self.assertNotIn("scenes", response.context)

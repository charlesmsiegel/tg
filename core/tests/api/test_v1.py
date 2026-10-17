"""Version-one native API: full-view audiences, safe writes and session CSRF."""

import json
from unittest.mock import patch

from django.test import Client, TestCase

from characters.models.core import Background, BackgroundRating, Human
from characters.models.mage import Mage
from core.api.views import CharacterUpdateView
from core.tests.action_audience import ActionAudienceMixin
from game.models import Chronicle, ObjectType

PREFIX = "/api/v1"


class NativeAPITests(ActionAudienceMixin, TestCase):
    gameline_code = "mta"

    def setUp(self):
        super().setUp()
        self.mage = Mage.objects.create(
            name="Private mage",
            owner=self.users["owner"],
            chronicle=self.chronicle,
            notes="Secret notes",
            arete=2,
            forces=2,
        )
        self.bg = Background.objects.create(name="Allies", property_name="allies")
        self.first = BackgroundRating.objects.create(
            char=self.mage, bg=self.bg, rating=2, note="Police"
        )
        self.second = BackgroundRating.objects.create(
            char=self.mage, bg=self.bg, rating=3, note="Mafia"
        )

    def test_all_read_routes_require_a_session(self):
        for path in [
            "session/",
            "chronicles/",
            f"chronicles/{self.chronicle.pk}/",
            f"chronicles/{self.chronicle.pk}/allowed-objects/",
            f"chronicles/{self.chronicle.pk}/characters/",
            f"characters/{self.mage.pk}/",
        ]:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(f"{PREFIX}/{path}").status_code, 401)

    def test_hidden_and_missing_character_have_identical_responses(self):
        self.login_as("player")
        hidden = self.client.get(f"{PREFIX}/characters/{self.mage.pk}/")
        missing = self.client.get(f"{PREFIX}/characters/999999/")
        self.assertEqual(hidden.status_code, 404)
        self.assertEqual(hidden.content, missing.content)
        self.assertNotIn(b"Secret notes", hidden.content)

    def test_polymorphic_projection_preserves_mage_and_repeated_backgrounds(self):
        self.login_as("owner")
        response = self.client.get(f"{PREFIX}/characters/{self.mage.pk}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["type"], "mage")
        self.assertEqual(data["mage"]["arete"], 2)
        self.assertEqual(data["mage"]["spheres"]["forces"], 2)
        self.assertEqual(
            [(r["id"], r["note"], r["rating"]) for r in data["human"]["backgrounds"]],
            [(self.first.pk, "Police", 2), (self.second.pk, "Mafia", 3)],
        )
        self.assertEqual(data["notes"], "Secret notes")
        self.assertEqual(response["Cache-Control"], "private, no-store")

    def test_chronicle_and_character_lists_are_scoped_and_paginated(self):
        self.login_as("owner")
        chronicles = self.client.get(f"{PREFIX}/chronicles/")
        self.assertEqual(chronicles.status_code, 200)
        self.assertEqual([r["id"] for r in chronicles.json()["results"]], [self.chronicle.pk])
        other = Human.objects.create(
            name="Other player", owner=self.users["player"], chronicle=self.chronicle
        )
        response = self.client.get(
            f"{PREFIX}/chronicles/{self.chronicle.pk}/characters/?page_size=1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual([r["id"] for r in response.json()["results"]], [self.mage.pk])
        self.assertNotIn(str(other.pk), [str(r["id"]) for r in response.json()["results"]])

    def test_unreadable_chronicle_routes_hide_existing_ids(self):
        self.login_as("player")
        for suffix in ["", "allowed-objects/", "characters/"]:
            hidden = self.client.get(f"{PREFIX}/chronicles/{self.chronicle.pk}/{suffix}")
            missing = self.client.get(f"{PREFIX}/chronicles/999999/{suffix}")
            self.assertEqual(hidden.status_code, 404)
            self.assertEqual(hidden.content, missing.content)

    def test_chronicle_projection_reports_native_allowed_objects_not_invented_modules(self):
        self.login_as("owner")
        allowed = ObjectType.objects.create(name="Mage", type="char", gameline="mta")
        self.chronicle.allowed_objects.add(allowed)
        data = self.client.get(f"{PREFIX}/chronicles/{self.chronicle.pk}/").json()
        self.assertEqual(data["name"], self.chronicle.name)
        self.assertNotIn("active_modules", data)
        response = self.client.get(f"{PREFIX}/chronicles/{self.chronicle.pk}/allowed-objects/")
        self.assertEqual(response.json()["results"][0]["id"], allowed.pk)

    def test_update_denial_audiences_and_no_writes(self):
        for who, status in [
            ("anonymous", 401),
            ("player", 404),
            ("other_chronicle_st", 404),
            ("other_line_st", 403),
        ]:
            self.login_as(who)
            response = self.client.post(
                f"{PREFIX}/characters/{self.mage.pk}/update/",
                data=json.dumps({"notes": "Changed"}),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, status, who)
            self.mage.refresh_from_db()
            self.assertEqual(self.mage.notes, "Secret notes")

    def test_owner_descriptive_update_preserves_polymorphic_values_and_relations(self):
        self.login_as("owner")
        response = self.client.post(
            f"{PREFIX}/characters/{self.mage.pk}/update/",
            data=json.dumps({"notes": "Edited", "history": "A history"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.notes, "Edited")
        self.assertEqual(self.mage.history, "A history")
        self.assertEqual(self.mage.forces, 2)
        self.assertEqual(self.mage.backgrounds.count(), 2)

    def test_protected_unknown_and_mechanical_fields_rejected_atomically(self):
        self.login_as("owner")
        for field, value in [
            ("owner", self.users["player"].pk),
            ("chronicle", self.other_chronicle.pk),
            ("status", "App"),
            ("xp", 99),
            ("arete", 5),
            ("traits", {}),
            ("extras", {}),
            ("bogus", "x"),
        ]:
            response = self.client.post(
                f"{PREFIX}/characters/{self.mage.pk}/update/",
                data=json.dumps({"notes": "Lost", field: value}),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 400, field)
            self.mage.refresh_from_db()
            self.assertEqual(self.mage.notes, "Secret notes")

    def test_invalid_json_and_non_text_values_do_not_write(self):
        self.login_as("owner")
        for data in ['{"notes":', "[]", '{"notes": {"nested": true}}', '{"notes": 123}']:
            response = self.client.post(
                f"{PREFIX}/characters/{self.mage.pk}/update/",
                data=data,
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 400)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.notes, "Secret notes")

    def test_update_is_post_only(self):
        self.login_as("owner")
        self.assertEqual(
            self.client.patch(
                f"{PREFIX}/characters/{self.mage.pk}/update/",
                data="{}",
                content_type="application/json",
            ).status_code,
            405,
        )

    def test_deeply_nested_json_is_rejected_without_writes(self):
        self.client.raise_request_exception = False
        before = Chronicle.objects.count()
        for who, path, field in [
            ("owner", f"characters/{self.mage.pk}/update/", "notes"),
            ("staff", "chronicles/create/", "name"),
        ]:
            with self.subTest(path=path):
                self.login_as(who)
                body = '{"' + field + '":' + "[" * 20000 + "0" + "]" * 20000 + "}"
                response = self.client.post(
                    f"{PREFIX}/{path}", data=body, content_type="application/json"
                )
                self.assertContains(response, "Malformed JSON.", status_code=400)
                self.mage.refresh_from_db()
                self.assertEqual(self.mage.notes, "Secret notes")
                self.assertEqual(Chronicle.objects.count(), before)

    def test_session_and_csrf_protect_updates(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.users["owner"])
        session = client.get(f"{PREFIX}/session/")
        self.assertEqual(session.status_code, 200)
        self.assertEqual(session.json()["user"]["id"], self.users["owner"].pk)
        path = f"{PREFIX}/characters/{self.mage.pk}/update/"
        self.assertEqual(
            client.post(
                path, data='{"notes":"Blocked"}', content_type="application/json"
            ).status_code,
            403,
        )
        response = client.post(
            path,
            data='{"notes":"Allowed"}',
            content_type="application/json",
            HTTP_X_CSRFTOKEN=session.json()["csrf_token"],
        )
        self.assertEqual(response.status_code, 200)

    def test_chronicle_create_requires_staff_and_rejects_supplied_head_st(self):
        for who, status in [
            ("anonymous", 401),
            ("owner", 403),
            ("st", 403),
            ("other_line_st", 403),
        ]:
            self.login_as(who)
            self.assertEqual(
                self.client.post(
                    f"{PREFIX}/chronicles/create/",
                    data='{"name":"Game"}',
                    content_type="application/json",
                ).status_code,
                status,
            )
        self.login_as("staff")
        before = Chronicle.objects.count()
        bad = self.client.post(
            f"{PREFIX}/chronicles/create/",
            data=json.dumps({"name": "Game", "head_st": self.users["owner"].pk}),
            content_type="application/json",
        )
        self.assertEqual(bad.status_code, 400)
        self.assertEqual(Chronicle.objects.count(), before)
        good = self.client.post(
            f"{PREFIX}/chronicles/create/",
            data='{"name":"New game","year":2026}',
            content_type="application/json",
        )
        self.assertEqual(good.status_code, 201)
        self.assertEqual(Chronicle.objects.get(pk=good.json()["id"]).head_st, self.users["staff"])

    def test_staff_create_also_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.users["staff"])
        self.assertEqual(
            client.post(
                f"{PREFIX}/chronicles/create/",
                data='{"name":"Game"}',
                content_type="application/json",
            ).status_code,
            403,
        )

    def test_full_sheet_list_matches_read_audience_and_excludes_observers(self):
        self.mage.add_observer(self.users["player"], self.users["staff"])
        Human.objects.create(
            name="Player membership", owner=self.users["player"], chronicle=self.chronicle
        )
        for who, contains in [
            ("owner", True),
            ("player", False),
            ("st", True),
            ("other_line_st", True),
            ("staff", True),
        ]:
            self.login_as(who)
            response = self.client.get(f"{PREFIX}/chronicles/{self.chronicle.pk}/characters/")
            self.assertEqual(response.status_code, 200, who)
            ids = [row["id"] for row in response.json()["results"]]
            self.assertEqual(self.mage.pk in ids, contains, who)

    def test_submitted_and_approved_owners_cannot_use_update_to_bypass_approval(self):
        self.login_as("owner")
        self.mage.status = "Sub"
        self.mage.save()
        for status in ["Sub", "App"]:
            if status == "App":
                self.mage.status = status
                self.mage.save()
            response = self.client.post(
                f"{PREFIX}/characters/{self.mage.pk}/update/",
                data='{"notes":"Bypassed"}',
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 403)
            self.mage.refresh_from_db()
            self.assertEqual(self.mage.notes, "Secret notes")

    def test_scoped_storyteller_can_edit_descriptions_but_not_mechanics(self):
        self.login_as("st")
        path = f"{PREFIX}/characters/{self.mage.pk}/update/"
        good = self.client.post(
            path, data='{"description":"Updated"}', content_type="application/json"
        )
        self.assertEqual(good.status_code, 200)
        bad = self.client.post(
            path, data='{"description":"Lost","forces":4}', content_type="application/json"
        )
        self.assertEqual(bad.status_code, 400)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.description, "Updated")
        self.assertEqual(self.mage.forces, 2)

    def test_create_validation_is_atomic_and_success_requires_valid_csrf(self):
        self.login_as("staff")
        before = Chronicle.objects.count()
        for body in ['{"name":""}', '{"name":"Game","year":99999}', "[]", '{"name":']:
            response = self.client.post(
                f"{PREFIX}/chronicles/create/", data=body, content_type="application/json"
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(Chronicle.objects.count(), before)
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.users["staff"])
        token = client.get(f"{PREFIX}/session/").json()["csrf_token"]
        response = client.post(
            f"{PREFIX}/chronicles/create/",
            data='{"name":"CSRF valid"}',
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, 201)

    def test_hidden_and_missing_update_actions_use_the_same_json_denial(self):
        self.login_as("player")
        responses = [
            self.client.post(
                f"{PREFIX}/characters/{pk}/update/",
                data='{"notes":"x"}',
                content_type="application/json",
            )
            for pk in [self.mage.pk, 999999]
        ]
        for response in responses:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(responses[0].content, responses[1].content)

    def test_owner_update_rechecks_status_after_lock(self):
        self.login_as("owner")
        original = CharacterUpdateView.lock_object

        def submit_before_lock(view, obj):
            changed = Mage.objects.get(pk=obj.pk)
            changed.status = "Sub"
            changed.save()
            return original(view, obj)

        with patch.object(CharacterUpdateView, "lock_object", submit_before_lock):
            response = self.client.post(
                f"{PREFIX}/characters/{self.mage.pk}/update/",
                data='{"notes":"Race write"}',
                content_type="application/json",
            )
        self.assertEqual(response.status_code, 403)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.notes, "Secret notes")

    def test_former_owner_cannot_write_after_transfer_before_lock(self):
        self.login_as("owner")
        original = CharacterUpdateView.lock_object

        def transfer_before_lock(view, obj):
            changed = Mage.objects.get(pk=obj.pk)
            changed.owner = self.users["player"]
            changed.save()
            return original(view, obj)

        with patch.object(CharacterUpdateView, "lock_object", transfer_before_lock):
            response = self.client.post(
                f"{PREFIX}/characters/{self.mage.pk}/update/",
                data='{"notes":"Race write"}',
                content_type="application/json",
            )
        self.assertEqual(response.status_code, 404)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.notes, "Secret notes")

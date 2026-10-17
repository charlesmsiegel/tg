"""Bounded native journal actions: audience, CSRF, canonical links and append races."""

import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest import skipUnless
from unittest.mock import patch

from django.db import OperationalError, close_old_connections, connection
from django.test import Client, TestCase, TransactionTestCase
from django.utils import timezone

from characters.models.mage import Mage
from core.api import journal_write, scene_journal
from core.api.journal_write import JournalAppendView, JournalFirstResponseView
from core.constants import CharacterStatus
from core.tests.action_audience import AUDIENCE, ActionAudienceMixin
from game.models import Journal, JournalEntry, STRelationship


class JournalWriteTests(ActionAudienceMixin, TestCase):
    gameline_code = "mta"

    def setUp(self):
        super().setUp()
        self.character = Mage.objects.create(
            name="Journal writer",
            owner=self.users["owner"],
            chronicle=self.chronicle,
            willpower=4,
            temporary_willpower=4,
        )
        self.journal = Journal.objects.get(character=self.character)
        self.entry = JournalEntry.objects.create(
            journal=self.journal, date=timezone.now(), message="Player prose"
        )
        self.append_url = f"/api/v1/journals/{self.journal.pk}/entries/append/"
        self.detail_url = f"/api/v1/journals/{self.journal.pk}/entries/{self.entry.pk}/"
        self.response_url = self.detail_url + "response/"

    def post(self, url=None, data=None, client=None, **headers):
        return (client or self.client).post(
            url or self.append_url,
            json.dumps(
                data if data is not None else {"date": "2026-10-17", "message": " A calm evening. "}
            ),
            content_type="application/json",
            **headers,
        )

    def test_append_exact_native_owner_audience(self):
        for who in AUDIENCE:
            self.login_as(who)
            before = JournalEntry.objects.count()
            response = self.post()
            expected = (
                201
                if who == "owner"
                else (
                    401
                    if who == "anonymous"
                    else 403 if who in {"st", "other_line_st", "staff"} else 404
                )
            )
            with self.subTest(who=who):
                self.assertEqual(response.status_code, expected)
                self.assertEqual(JournalEntry.objects.count(), before + (who == "owner"))

    def test_response_exact_native_approve_audience_and_owner_visible_read(self):
        for who in AUDIENCE:
            self.entry.st_message = ""
            self.entry.save()
            self.login_as(who)
            response = self.post(self.response_url, {"st_message": " ST response "})
            expected = (
                200
                if who in {"st", "staff"}
                else (
                    401 if who == "anonymous" else 403 if who in {"owner", "other_line_st"} else 404
                )
            )
            with self.subTest(who=who):
                self.assertEqual(response.status_code, expected)
                self.entry.refresh_from_db()
                self.assertEqual(self.entry.st_message, "ST response" if expected == 200 else "")
        self.login_as("st")
        self.assertEqual(
            self.post(self.response_url, {"st_message": "Owner-visible response"}).status_code, 200
        )
        for who in ("owner", "st", "other_line_st", "staff"):
            self.login_as(who)
            data = self.client.get(self.detail_url).json()
            self.assertEqual(data["st_message"], "Owner-visible response")
            self.assertNotIn("author", data)

    def test_public_character_does_not_make_journal_entry_public(self):
        self.character.visibility = "PUB"
        self.character.save()
        self.login_as("player")
        hidden = self.client.get(self.detail_url)
        missing = self.client.get(self.detail_url.replace(f"/{self.entry.pk}/", "/999999/"))
        self.assertEqual(hidden.status_code, 404)
        self.assertEqual(hidden.content, missing.content)
        self.assertEqual(self.post().status_code, 404)
        self.assertEqual(self.post(self.response_url, {"st_message": "No"}).status_code, 404)

    def test_real_session_csrf_required_for_both_actions(self):
        for who, url, data in [
            ("owner", self.append_url, {"date": "2026-10-17", "message": "Real csrf"}),
            ("st", self.response_url, {"st_message": "Response"}),
        ]:
            client = Client(enforce_csrf_checks=True)
            client.force_login(self.users[who])
            token = client.get("/api/v1/session/", secure=True).json()["csrf_token"]
            with self.subTest(who=who):
                self.assertEqual(
                    self.post(
                        url, data, client=client, secure=True, HTTP_ORIGIN="https://testserver"
                    ).status_code,
                    403,
                )
                self.assertEqual(
                    self.post(
                        url,
                        data,
                        client=client,
                        secure=True,
                        HTTP_X_CSRFTOKEN=token,
                        HTTP_ORIGIN="https://evil.example",
                    ).status_code,
                    403,
                )
                self.assertIn(
                    self.post(
                        url,
                        data,
                        client=client,
                        secure=True,
                        HTTP_X_CSRFTOKEN=token,
                        HTTP_ORIGIN="https://testserver",
                    ).status_code,
                    (200, 201),
                )

    def test_plain_prose_preserves_text_date_and_never_calls_native_commands(self):
        self.login_as("owner")
        message = "  Café [quote]hello[/quote]\nhttps://example.test/path #journal <b>text</b>  "
        with patch(
            "game.models.message_processing", side_effect=AssertionError("Parser must not run")
        ):
            response = self.post(data={"date": "2026-10-17", "message": message})
        self.assertEqual(response.status_code, 201)
        entry = JournalEntry.objects.get(pk=response.json()["id"])
        self.assertEqual(entry.message, message.strip())
        self.assertEqual(entry.date, timezone.make_aware(timezone.datetime(2026, 10, 17)))
        self.assertEqual(entry.st_message, "")
        self.character.refresh_from_db()
        self.assertEqual(self.character.temporary_willpower, 4)

    def test_all_reserved_native_commands_are_refused_without_side_effects(self):
        self.login_as("owner")
        commands = [
            "#WP",
            "#WP2",
            "#WP-2",
            "#Q3",
            "#Q-3",
            "#P2",
            "#P-2",
            "#2B",
            "#-2B",
            "#1L",
            "#1A",
            "/roll 2",
            "/rolls 2 rolls @ 2",
            "/extended 2 target 3",
            "/stat strength",
            "before#WPafter",
            "prefix/roll malformed",
            " /ROLL 2",
            "\n /StAt strength",
            " #wp",
            "#q3",
            "#p3",
            "#1b",
        ]
        before = JournalEntry.objects.count()
        for command in commands:
            with self.subTest(command=command):
                response = self.post(data={"date": "2026-10-17", "message": command})
                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.json()["errors"]["message"][0]["code"], "unsupported_command"
                )
                self.assertEqual(JournalEntry.objects.count(), before)
        self.character.refresh_from_db()
        self.assertEqual(self.character.temporary_willpower, 4)

    def test_scalar_allowlist_bounded_text_and_native_form_validation(self):
        self.login_as("owner")
        invalid = [
            {"date": "2026-02-30", "message": "x"},
            {"date": "10/17/2026", "message": "x"},
            {"date": "2026-10-17T00:00:00Z", "message": "x"},
            {"date": 123, "message": "x"},
            {"date": "2026-10-17", "message": True},
            {"date": "2026-10-17", "message": ["x"]},
            {"date": "2026-10-17", "message": " "},
            {"date": "2026-10-17", "message": "x" * 10001},
            {"date": "2026-10-17", "message": "x", "st_message": "forged"},
            {"date": "2026-10-17", "message": "x", "author": self.users["staff"].pk},
            {"date": "2026-10-17", "message": "x", "journal": 999},
            {},
            [],
            None,
        ]
        for data in invalid:
            with self.subTest(data=str(data)[:80]):
                response = self.client.post(
                    self.append_url, json.dumps(data), content_type="application/json"
                )
                self.assertEqual(response.status_code, 400)
                self.assertIn("errors", response.json())
        self.assertEqual(JournalEntry.objects.count(), 1)

    def test_duplicate_malformed_oversized_and_wrong_media_inputs(self):
        self.login_as("owner")
        for body in [
            "{",
            '{"date":"2026-10-17","message":"first","message":"second"}',
            '"not object"',
            " " * 65537,
        ]:
            response = self.client.post(self.append_url, body, content_type="application/json")
            self.assertEqual(response.status_code, 400)
            self.assertIn("errors", response.json())
        self.assertEqual(self.client.post(self.append_url, {"message": "form"}).status_code, 415)
        self.assertEqual(JournalEntry.objects.count(), 1)

    def test_first_response_only_prevents_overwrite_and_does_not_process_commands(self):
        self.login_as("st")
        self.assertEqual(
            self.post(self.response_url, {"st_message": "First #WP /roll text"}).status_code, 200
        )
        conflict = self.post(self.response_url, {"st_message": "Second response"})
        self.assertEqual(conflict.status_code, 409)
        self.assertEqual(conflict.json()["errors"]["st_message"][0]["code"], "already_answered")
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.st_message, "First #WP /roll text")
        self.assertEqual(self.entry.message, "Player prose")
        self.character.refresh_from_db()
        self.assertEqual(self.character.temporary_willpower, 4)

    def test_response_allowlist_does_not_write_player_prose_or_author(self):
        self.login_as("st")
        for data in [
            {"st_message": "x", "message": "replace"},
            {"st_message": "x", "journal": 999},
            {"st_message": {}},
            {"st_message": " "},
            {"st_message": "x" * 10001},
            {},
        ]:
            response = self.post(self.response_url, data)
            self.assertEqual(response.status_code, 400)
            self.assertIn("errors", response.json())
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.message, "Player prose")
        self.assertEqual(self.entry.st_message, "")

    def test_cross_journal_entry_is_hidden_for_get_and_post_even_staff(self):
        other_character = Mage.objects.create(
            name="Other", owner=self.users["player"], chronicle=self.other_chronicle
        )
        other_journal = Journal.objects.get(character=other_character)
        other = JournalEntry.objects.create(
            journal=other_journal, date=timezone.now(), message="Other private"
        )
        self.login_as("staff")
        detail = f"/api/v1/journals/{self.journal.pk}/entries/{other.pk}/"
        self.assertEqual(self.client.get(detail).status_code, 404)
        self.assertEqual(self.post(detail + "response/", {"st_message": "No"}).status_code, 404)
        other.refresh_from_db()
        self.assertEqual(other.st_message, "")

    def test_native_owner_append_and_approve_status_policy_remains_authoritative(self):
        for status, _label in CharacterStatus.CHOICES:
            self.character.status = status
            Mage.objects.filter(pk=self.character.pk).update(status=status)
            self.login_as("owner")
            with self.subTest(status=status):
                self.assertEqual(self.post().status_code, 201)
            self.login_as("st")
            self.entry.st_message = ""
            self.entry.save()
            self.assertEqual(
                self.post(self.response_url, {"st_message": f"Status {status}"}).status_code, 200
            )

    def test_action_methods_and_no_read_side_effects(self):
        self.login_as("owner")
        for url in (self.append_url, self.response_url):
            for method in ("get", "put", "patch", "delete"):
                self.assertEqual(getattr(self.client, method)(url).status_code, 405)
        self.login_as("st")
        for method in ("get", "head"):
            self.assertEqual(getattr(self.client, method)(self.detail_url).status_code, 200)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.st_message, "")
        self.assertEqual(JournalEntry.objects.count(), 1)

    def test_owner_transfer_before_lock_revokes_append(self):
        self.login_as("owner")
        original = JournalAppendView.lock_object

        def transfer(view, obj):
            Mage.objects.filter(pk=self.character.pk).update(owner=self.users["player"])
            return original(view, obj)

        with patch.object(JournalAppendView, "lock_object", transfer):
            self.assertEqual(self.post().status_code, 404)
        self.assertEqual(JournalEntry.objects.count(), 1)

    def test_reparented_journal_cannot_redirect_authorized_append(self):
        other_character = Mage.objects.create(name="Other", owner=self.users["owner"])
        Journal.objects.get(character=other_character).delete()
        self.login_as("owner")
        original = JournalAppendView.lock_object

        def reparent(view, obj):
            Journal.objects.filter(pk=obj.pk).update(character=other_character)
            return original(view, obj)

        with patch.object(JournalAppendView, "lock_object", reparent):
            self.assertEqual(self.post().status_code, 404)
        self.assertEqual(JournalEntry.objects.count(), 1)

    def test_revoked_scoped_role_with_read_only_role_cannot_answer(self):
        self.chronicle.game_storytellers.add(self.users["st"])
        self.login_as("st")
        original = JournalFirstResponseView.lock_object

        def revoke(view, obj):
            STRelationship.objects.filter(user=self.users["st"]).delete()
            return original(view, obj)

        with patch.object(JournalFirstResponseView, "lock_object", revoke):
            self.assertEqual(self.post(self.response_url, {"st_message": "No"}).status_code, 403)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.st_message, "")

    def test_entry_reparented_before_locked_lookup_cannot_be_answered(self):
        other_character = Mage.objects.create(
            name="Other", owner=self.users["player"], chronicle=self.other_chronicle
        )
        other_journal = Journal.objects.get(character=other_character)
        self.login_as("st")
        original = JournalFirstResponseView.lock_object

        def reparent(view, obj):
            JournalEntry.objects.filter(pk=self.entry.pk).update(journal=other_journal)
            return original(view, obj)

        with patch.object(JournalFirstResponseView, "lock_object", reparent):
            self.assertEqual(self.post(self.response_url, {"st_message": "No"}).status_code, 404)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.st_message, "")

    def test_staff_flag_revoked_before_lock_cannot_answer(self):
        self.login_as("staff")
        original = JournalFirstResponseView.lock_object

        def revoke(view, obj):
            type(self.users["staff"]).objects.filter(pk=self.users["staff"].pk).update(
                is_staff=False
            )
            return original(view, obj)

        with patch.object(JournalFirstResponseView, "lock_object", revoke):
            self.assertEqual(self.post(self.response_url, {"st_message": "No"}).status_code, 404)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.st_message, "")

    def test_response_arriving_after_client_read_is_preserved_with_conflict(self):
        self.login_as("st")
        self.assertEqual(self.client.get(self.detail_url).json()["st_message"], "")
        original = JournalFirstResponseView.get_object

        def competing(view):
            journal = original(view)
            JournalEntry.objects.filter(pk=self.entry.pk).update(
                st_message="Native concurrent response"
            )
            return journal

        with patch.object(JournalFirstResponseView, "get_object", competing):
            response = self.post(self.response_url, {"st_message": "Stale client response"})
        self.assertEqual(response.status_code, 409)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.st_message, "Native concurrent response")

    def test_head_st_game_st_and_orphan_native_policies(self):
        self.login_as("player")
        self.chronicle.game_storytellers.add(self.users["player"])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        self.assertEqual(self.post(self.response_url, {"st_message": "No"}).status_code, 403)
        self.chronicle.head_st = self.users["player"]
        self.chronicle.save()
        self.assertEqual(
            self.post(self.response_url, {"st_message": "Head reply"}).status_code, 200
        )
        self.character.chronicle = None
        self.character.save()
        self.login_as("owner")
        self.assertEqual(self.post().status_code, 201)
        self.assertEqual(self.client.get(self.detail_url).json()["st_message"], "Head reply")
        self.login_as("st")
        self.assertEqual(self.client.get(self.detail_url).status_code, 404)
        self.assertEqual(self.post(self.response_url, {"st_message": "No"}).status_code, 404)

    def test_deep_json_and_invalid_unicode_are_structured_errors_not_server_failures(self):
        self.login_as("owner")
        self.client.raise_request_exception = False
        for body in (
            '{"message":' + "[" * 20000 + "0" + "]" * 20000 + "}",
            '{"date":"2026-10-17","message":"\\ud800"}',
        ):
            with self.subTest(body=body[:60]):
                response = self.client.post(self.append_url, body, content_type="application/json")
                self.assertEqual(response.status_code, 400)
                self.assertIn("errors", response.json())

    def test_entry_detail_rechecks_reparent_owner_and_role_after_lookup(self):
        other_character = Mage.objects.create(
            name="Other", owner=self.users["player"], chronicle=self.other_chronicle
        )
        other_journal = Journal.objects.get(character=other_character)
        original = scene_journal.get_object_or_404
        for change in ("reparent", "owner", "role"):
            self.login_as("st" if change == "role" else "owner")

            def lookup(queryset, *args, change=change, **kwargs):
                result = original(queryset, *args, **kwargs)
                if isinstance(result, JournalEntry):
                    if change == "reparent":
                        JournalEntry.objects.filter(pk=result.pk).update(journal=other_journal)
                    elif change == "owner":
                        Mage.objects.filter(pk=self.character.pk).update(owner=self.users["player"])
                    else:
                        STRelationship.objects.filter(user=self.users["st"]).delete()
                return result

            with (
                self.subTest(change=change),
                patch("core.api.scene_journal.get_object_or_404", side_effect=lookup),
            ):
                self.assertEqual(self.client.get(self.detail_url).status_code, 404)
            JournalEntry.objects.filter(pk=self.entry.pk).update(journal=self.journal)
            Mage.objects.filter(pk=self.character.pk).update(owner=self.users["owner"])

    def test_native_status_change_during_append_keeps_owner_prose_policy(self):
        self.login_as("owner")
        original = JournalAppendView.lock_object

        def retire(view, obj):
            Mage.objects.filter(pk=self.character.pk).update(status=CharacterStatus.RETIRED)
            return original(view, obj)

        with patch.object(JournalAppendView, "lock_object", retire):
            self.assertEqual(self.post().status_code, 201)
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, CharacterStatus.RETIRED)
        self.assertEqual(self.character.temporary_willpower, 4)

    def test_missing_and_hidden_write_targets_match_before_payload_validation(self):
        self.login_as("player")
        hidden = self.client.post(self.append_url, "not json", content_type="application/json")
        missing = self.client.post(
            "/api/v1/journals/999999/entries/append/", "not json", content_type="application/json"
        )
        self.assertEqual(hidden.status_code, 404)
        self.assertEqual(hidden.content, missing.content)
        self.login_as("st")
        for entry_id in (0, 999999, 2**63):
            with self.subTest(entry_id=entry_id):
                path = f"/api/v1/journals/{self.journal.pk}/entries/{entry_id}/"
                self.assertEqual(self.client.get(path).status_code, 404)
                self.assertEqual(
                    self.post(path + "response/", {"st_message": "No"}).status_code, 404
                )

    def test_append_creates_independent_entries_without_overwriting_and_does_not_auto_deduplicate(
        self,
    ):
        self.login_as("owner")
        first = self.post().json()
        second = self.post().json()
        self.assertNotEqual(first["id"], second["id"])
        self.assertEqual(first["message"], second["message"])
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.message, "Player prose")
        self.assertEqual(JournalEntry.objects.count(), 3)

    def test_head_st_revocation_before_lock_cannot_answer(self):
        self.chronicle.head_st = self.users["player"]
        self.chronicle.save()
        self.login_as("player")
        original = JournalFirstResponseView.lock_object

        def revoke(view, obj):
            type(self.chronicle).objects.filter(pk=self.chronicle.pk).update(head_st=None)
            return original(view, obj)

        with patch.object(JournalFirstResponseView, "lock_object", revoke):
            self.assertEqual(self.post(self.response_url, {"st_message": "No"}).status_code, 404)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.st_message, "")

    def test_character_chronicle_transfer_before_lock_revokes_old_scope(self):
        self.login_as("st")
        original = JournalFirstResponseView.lock_object

        def transfer(view, obj):
            Mage.objects.filter(pk=self.character.pk).update(chronicle=self.other_chronicle)
            return original(view, obj)

        with patch.object(JournalFirstResponseView, "lock_object", transfer):
            self.assertEqual(self.post(self.response_url, {"st_message": "No"}).status_code, 404)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.st_message, "")

    def test_actor_deactivation_before_lock_cannot_append(self):
        self.login_as("owner")
        original = JournalAppendView.lock_object

        def deactivate(view, obj):
            type(self.users["owner"]).objects.filter(pk=self.users["owner"].pk).update(
                is_active=False
            )
            return original(view, obj)

        with patch.object(JournalAppendView, "lock_object", deactivate):
            self.assertEqual(self.post().status_code, 404)
        self.assertEqual(JournalEntry.objects.count(), 1)

    def test_native_read_acknowledgement_counts_as_an_existing_answer(self):
        self.entry.st_message = "Read"
        self.entry.save()
        self.login_as("owner")
        self.assertEqual(self.client.get(self.detail_url).json()["st_message"], "Read")
        self.login_as("st")
        self.assertEqual(self.post(self.response_url, {"st_message": "Overwrite"}).status_code, 409)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.st_message, "Read")

    def test_unrelated_database_error_is_not_misrepresented_as_edit_conflict(self):
        self.login_as("owner")
        with (
            patch(
                "core.api.journal_write.append_prose",
                side_effect=OperationalError("disk I/O error"),
            ),
            self.assertLogs("django.request", level="ERROR"),
        ):
            with self.assertRaises(OperationalError):
                self.post()
        self.assertEqual(JournalEntry.objects.count(), 1)

    def test_legacy_sqlite_lock_causes_return_structured_conflicts(self):
        self.login_as("owner")
        self.client.raise_request_exception = False
        for message in (
            "database is locked",
            "database table is locked: game_journalentry",
            "database schema is locked: main",
        ):

            def fail(*args, message=message, **kwargs):
                try:
                    raise sqlite3.OperationalError(message)
                except sqlite3.OperationalError as cause:
                    raise OperationalError(message) from cause

            with (
                self.subTest(message=message),
                patch("core.api.journal_write.append_prose", side_effect=fail),
            ):
                response = self.post()
                self.assertEqual(response.status_code, 409)
                self.assertEqual(
                    response.json()["errors"]["non_field_errors"][0]["code"], "write_conflict"
                )
        self.assertEqual(JournalEntry.objects.count(), 1)

    def test_legacy_sqlite_nonlock_error_is_not_disguised_as_conflict(self):
        self.login_as("owner")

        def fail(*args, **kwargs):
            try:
                raise sqlite3.OperationalError("disk I/O error")
            except sqlite3.OperationalError as cause:
                raise OperationalError("disk I/O error") from cause

        with (
            patch("core.api.journal_write.append_prose", side_effect=fail),
            self.assertLogs("django.request", level="ERROR"),
        ):
            with self.assertRaises(OperationalError):
                self.post()


@skipUnless(
    connection.vendor == "sqlite",
    "SQLite lock-upgrade conflict; row-locking databases serialize earlier",
)
class ConcurrentJournalTests(ActionAudienceMixin, TransactionTestCase):
    gameline_code = "mta"

    def test_simultaneous_first_responses_are_conflicts_not_server_errors(self):
        character = Mage.objects.create(
            name="Concurrent", owner=self.users["owner"], chronicle=self.chronicle
        )
        journal = Journal.objects.get(character=character)
        entry = JournalEntry.objects.create(
            journal=journal, date=timezone.now(), message="Original"
        )
        url = f"/api/v1/journals/{journal.pk}/entries/{entry.pk}/response/"
        clients = [Client(raise_request_exception=False), Client(raise_request_exception=False)]
        for client in clients:
            client.force_login(self.users["st"])
        barrier = Barrier(2)
        original = journal_write.first_response

        def simultaneous(entry, request):
            barrier.wait(timeout=15)
            return original(entry, request)

        def send(index):
            close_old_connections()
            try:
                response = clients[index].post(
                    url,
                    json.dumps({"st_message": f"Answer {index}"}),
                    content_type="application/json",
                )
                data = (
                    response.json()
                    if response.get("Content-Type", "").startswith("application/json")
                    else {}
                )
                return response.status_code, data
            finally:
                close_old_connections()

        with (
            patch("core.api.journal_write.first_response", side_effect=simultaneous),
            ThreadPoolExecutor(2) as executor,
        ):
            responses = list(executor.map(send, range(2)))
        statuses = [status for status, _data in responses]
        self.assertTrue(all(status in {200, 409} for status in statuses), statuses)
        self.assertLessEqual(statuses.count(200), 1)
        self.assertIn(409, statuses)
        for status, data in responses:
            if status == 409:
                self.assertIn("errors", data)
        entry.refresh_from_db()
        if 200 in statuses:
            winner = statuses.index(200)
            self.assertEqual(entry.st_message, f"Answer {winner}")
        else:
            # SQLite can abort both read-to-write upgrades. Neither may partially
            # write; a fresh explicit request can answer once after reconciliation.
            self.assertEqual(entry.st_message, "")
            self.assertEqual(
                clients[0]
                .post(
                    url, json.dumps({"st_message": "Reconciled"}), content_type="application/json"
                )
                .status_code,
                200,
            )
            entry.refresh_from_db()
            self.assertEqual(entry.st_message, "Reconciled")
        self.assertEqual(
            clients[1]
            .post(url, json.dumps({"st_message": "Overwrite"}), content_type="application/json")
            .status_code,
            409,
        )
        entry.refresh_from_db()
        self.assertNotEqual(entry.st_message, "Overwrite")
        self.assertEqual(entry.message, "Original")

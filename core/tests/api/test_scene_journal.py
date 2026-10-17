"""Native scene/journal read audiences and omission of private/ambiguous fields."""

from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from characters.models.core import Human
from core.api import scene_journal
from core.tests.action_audience import ActionAudienceMixin
from game.models import Journal, JournalEntry, Post, Scene, STRelationship, UserSceneReadStatus

PREFIX = "/api/v1"


class SceneJournalAPITests(ActionAudienceMixin, TestCase):
    gameline_code = "mta"

    def setUp(self):
        super().setUp()
        self.character = Human.objects.create(
            name="SECRET character",
            owner=self.users["owner"],
            chronicle=self.chronicle,
            notes="SECRET sheet",
            willpower=3,
        )
        self.other_character = Human.objects.create(
            name="Other", owner=self.users["player"], chronicle=self.chronicle
        )
        self.journal = Journal.objects.get(character=self.character)
        self.other_journal = Journal.objects.get(character=self.other_character)
        self.entry = JournalEntry.objects.create(
            journal=self.journal,
            message="/roll 4 @willpower Stored journal text",
            st_message="SECRET ST RESPONSE",
            date=timezone.now(),
        )
        self.scene = Scene.objects.create(
            name="Participant scene",
            visibility=Scene.Visibility.PARTICIPANTS,
            chronicle=self.chronicle,
            st_message="SECRET ST REQUEST",
            gameline="mta",
        )
        self.scene.characters.add(self.character)
        self.public_scene = Scene.objects.create(
            name="Public scene", visibility=Scene.Visibility.PUBLIC, chronicle=self.other_chronicle
        )
        self.chronicle_scene = Scene.objects.create(
            name="Chronicle scene", visibility=Scene.Visibility.CHRONICLE, chronicle=self.chronicle
        )
        self.post = Post.objects.create(
            scene=self.scene,
            character=self.character,
            display_name="Public alias",
            message="/stat strength Stored RP text",
            roll={"SECRET": "PRIVATE roll metadata"},
        )
        self.paths = [
            "scenes/",
            f"scenes/{self.scene.pk}/",
            f"scenes/{self.scene.pk}/posts/",
            "journals/",
            f"journals/{self.journal.pk}/",
            f"journals/{self.journal.pk}/entries/",
            f"characters/{self.character.pk}/journal/",
        ]

    def get(self, path):
        return self.client.get(f"{PREFIX}/{path}")

    def test_every_route_requires_session(self):
        for path in self.paths:
            with self.subTest(path=path):
                self.assertEqual(self.get(path).status_code, 401)

    def test_scene_list_and_details_follow_native_visibility_matrix(self):
        expected = {
            "owner": {self.scene.pk, self.chronicle_scene.pk, self.public_scene.pk},
            "player": {self.chronicle_scene.pk, self.public_scene.pk},
            "st": {self.scene.pk, self.chronicle_scene.pk, self.public_scene.pk},
            "other_line_st": {self.scene.pk, self.chronicle_scene.pk, self.public_scene.pk},
            "other_chronicle_st": {self.public_scene.pk},
            "staff": {self.scene.pk, self.chronicle_scene.pk, self.public_scene.pk},
        }
        for who, visible in expected.items():
            self.login_as(who)
            listed = self.get("scenes/")
            self.assertEqual(listed.status_code, 200)
            self.assertEqual({row["id"] for row in listed.json()["results"]}, visible, who)
            for scene in [self.scene, self.public_scene, self.chronicle_scene]:
                self.assertEqual(
                    self.get(f"scenes/{scene.pk}/").status_code,
                    200 if scene.pk in visible else 404,
                    who,
                )
                self.assertEqual(
                    self.get(f"scenes/{scene.pk}/posts/").status_code,
                    200 if scene.pk in visible else 404,
                    who,
                )

    def test_journal_list_detail_entries_and_character_lookup_have_same_audience(self):
        self.character.add_observer(self.users["player"], self.users["staff"])
        for who, allowed in [
            ("owner", True),
            ("player", False),
            ("st", True),
            ("other_line_st", True),
            ("other_chronicle_st", False),
            ("staff", True),
        ]:
            self.login_as(who)
            listed = self.get("journals/")
            self.assertEqual(listed.status_code, 200)
            self.assertEqual(
                self.journal.pk in [r["id"] for r in listed.json()["results"]], allowed, who
            )
            for path in [
                f"journals/{self.journal.pk}/",
                f"journals/{self.journal.pk}/entries/",
                f"characters/{self.character.pk}/journal/",
            ]:
                self.assertEqual(self.get(path).status_code, 200 if allowed else 404, (who, path))

    def test_hidden_and_missing_detail_and_nested_ids_have_identical_json(self):
        self.login_as("player")
        for template, pk in [
            ("scenes/{}/", self.scene.pk),
            ("scenes/{}/posts/", self.scene.pk),
            ("journals/{}/", self.journal.pk),
            ("journals/{}/entries/", self.journal.pk),
            ("characters/{}/journal/", self.character.pk),
        ]:
            hidden = self.get(template.format(pk))
            missing = self.get(template.format(999999))
            self.assertEqual(hidden.status_code, 404)
            self.assertEqual(hidden["Content-Type"], "application/json")
            self.assertEqual(
                (hidden.status_code, hidden.content), (missing.status_code, missing.content)
            )

    def test_st_fields_and_linked_character_private_values_never_serialize(self):
        for who in ["owner", "st", "other_line_st", "staff"]:
            self.login_as(who)
            for path in [
                "scenes/",
                f"scenes/{self.scene.pk}/",
                f"scenes/{self.scene.pk}/posts/",
                "journals/",
                f"journals/{self.journal.pk}/",
                f"journals/{self.journal.pk}/entries/",
                f"characters/{self.character.pk}/journal/",
            ]:
                response = self.get(path)
                self.assertEqual(response.status_code, 200)
                for sentinel in [
                    b"SECRET",
                    b"st_message",
                    b"PRIVATE roll metadata",
                    b"owner_id",
                    b"location_id",
                ]:
                    self.assertNotIn(sentinel, response.content, (who, path, sentinel))
            post = self.get(f"scenes/{self.scene.pk}/posts/").json()["results"][0]
            self.assertEqual(post["display_name"], "Public alias")
            self.assertEqual(post["message"], self.post.message)
            self.assertNotIn("character_id", post)
            self.assertNotIn("roll", post)
            entry = self.get(f"journals/{self.journal.pk}/entries/").json()["results"][0]
            self.assertEqual(entry["message"], self.entry.message)
            self.assertEqual(entry["id"], self.entry.pk)

    def test_get_and_head_do_not_process_commands_or_mark_scenes_read(self):
        self.login_as("owner")
        counts = [
            model.objects.count() for model in [Journal, JournalEntry, Post, UserSceneReadStatus]
        ]
        for path in self.paths:
            response = self.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response["Cache-Control"], "private, no-store")
            self.assertEqual(self.client.head(f"{PREFIX}/{path}").status_code, 200)
        self.assertEqual(
            [model.objects.count() for model in [Journal, JournalEntry, Post, UserSceneReadStatus]],
            counts,
        )
        self.character.refresh_from_db()
        self.assertEqual(
            (self.character.willpower, self.character.xp, self.character.freebies), (3, 0, 15)
        )
        self.entry.refresh_from_db()
        self.post.refresh_from_db()
        self.assertEqual(self.entry.message, "/roll 4 @willpower Stored journal text")
        self.assertEqual(self.post.message, "/stat strength Stored RP text")

    def test_unsafe_methods_are_not_implemented_on_any_read_route(self):
        self.login_as("owner")
        for path in self.paths:
            for method in ["post", "put", "patch", "delete"]:
                response = getattr(self.client, method)(
                    f"{PREFIX}/{path}",
                    data='{"message":"/spend 9","st_message":"secret"}',
                    content_type="application/json",
                )
                self.assertEqual(response.status_code, 405, (path, method))

    def test_collections_are_bounded_and_order_stable(self):
        self.login_as("owner")
        for n in range(105):
            Post.objects.create(scene=self.scene, display_name="Alias", message=str(n))
            JournalEntry.objects.create(
                journal=self.journal,
                message=str(n),
                date=self.entry.date,
                datetime_created=self.entry.datetime_created,
            )
        for path in [f"scenes/{self.scene.pk}/posts/", f"journals/{self.journal.pk}/entries/"]:
            first = self.get(path + "?page_size=100000")
            self.assertEqual(first.status_code, 200)
            self.assertEqual(first.json()["count"], 106)
            self.assertEqual(len(first.json()["results"]), 100)
            second = self.get(path + "?page_size=100000&page=2")
            self.assertEqual(len(second.json()["results"]), 6)
            first_ids = {r["id"] for r in first.json()["results"]}
            self.assertTrue(first_ids.isdisjoint(r["id"] for r in second.json()["results"]))
        scene_ids = [r["id"] for r in self.get("scenes/?page_size=1").json()["results"]]
        self.assertEqual(len(scene_ids), 1)
        self.assertEqual(self.get("scenes/?page=999999").status_code, 404)

    def test_query_identifiers_and_pagination_inputs_fail_closed(self):
        self.login_as("owner")
        for query in [
            "chronicle_id=0",
            "chronicle_id=-1",
            "chronicle_id=abc",
            "chronicle_id=999999999999999999999999",
            "page=0",
            "page=-1",
            "page=last",
            "page_size=0",
            "page_size=-1",
            "page_size=abc",
            "page=1&page=2",
            "include=st_message",
        ]:
            self.assertEqual(self.get("scenes/?" + query).status_code, 400, query)
        for template in [
            "scenes/{}/",
            "scenes/{}/posts/",
            "journals/{}/",
            "journals/{}/entries/",
            "characters/{}/journal/",
        ]:
            for pk in ["0", "-1", "abc", "999999999999999999999999999999"]:
                self.assertEqual(self.get(template.format(pk)).status_code, 404, (template, pk))

    def test_chronicle_filter_keeps_public_scene_visibility_without_leaking_hidden_ids(self):
        self.login_as("player")
        response = self.get(f"scenes/?chronicle_id={self.chronicle.pk}")
        self.assertEqual([r["id"] for r in response.json()["results"]], [self.chronicle_scene.pk])
        public = self.get(f"scenes/?chronicle_id={self.other_chronicle.pk}")
        self.assertEqual([r["id"] for r in public.json()["results"]], [self.public_scene.pk])
        empty = self.get("scenes/?chronicle_id=999999")
        self.assertEqual(empty.status_code, 200)
        self.assertEqual(empty.json()["count"], 0)
        journals = self.get(f"journals/?chronicle_id={self.other_chronicle.pk}")
        self.assertEqual(journals.json()["count"], 0)

    def test_scope_revocation_is_observed_on_following_requests(self):
        self.login_as("st")
        self.assertEqual(self.get(f"journals/{self.journal.pk}/entries/").status_code, 200)
        STRelationship.objects.filter(user=self.users["st"]).delete()
        self.assertEqual(self.get(f"journals/{self.journal.pk}/entries/").status_code, 404)
        self.assertEqual(self.get(f"scenes/{self.scene.pk}/posts/").status_code, 404)
        self.assertEqual(self.get("journals/").json()["count"], 0)
        self.login_as("owner")
        self.scene.characters.clear()
        self.assertEqual(self.get(f"scenes/{self.scene.pk}/posts/").status_code, 404)

    def test_owner_transfer_is_observed_across_all_journal_routes(self):
        self.login_as("owner")
        self.assertEqual(self.get(f"characters/{self.character.pk}/journal/").status_code, 200)
        self.character.owner = self.users["player"]
        self.character.save()
        self.assertEqual(self.get("journals/").json()["count"], 0)
        for path in [
            f"journals/{self.journal.pk}/",
            f"journals/{self.journal.pk}/entries/",
            f"characters/{self.character.pk}/journal/",
        ]:
            self.assertEqual(self.get(path).status_code, 404)

    def test_retired_and_deceased_characters_keep_native_full_read_permissions(self):
        self.login_as("owner")
        self.character.display = False
        self.character.status = "Ret"
        self.character.save()
        self.assertEqual(self.get(f"characters/{self.character.pk}/journal/").status_code, 200)
        self.character.status = "App"
        self.character.save()
        self.character.status = "Dec"
        self.character.save()
        self.assertEqual(self.get(f"journals/{self.journal.pk}/entries/").status_code, 200)
        self.assertEqual(self.get(f"scenes/{self.scene.pk}/").status_code, 200)
        self.login_as("player")
        self.assertEqual(self.get(f"journals/{self.journal.pk}/entries/").status_code, 404)

    def test_missing_journal_is_not_created_by_lookup(self):
        self.login_as("owner")
        self.journal.delete()
        before = Journal.objects.count()
        self.assertEqual(self.get(f"characters/{self.character.pk}/journal/").status_code, 404)
        self.assertEqual(Journal.objects.count(), before)

    def test_no_chronicle_and_game_storyteller_follow_native_read_rules(self):
        self.chronicle.game_storytellers.add(self.users["player"])
        self.login_as("player")
        self.assertEqual(self.get(f"scenes/{self.scene.pk}/posts/").status_code, 200)
        self.assertEqual(self.get(f"journals/{self.journal.pk}/entries/").status_code, 200)
        self.scene.chronicle = None
        self.scene.save()
        self.assertEqual(self.get(f"scenes/{self.scene.pk}/").status_code, 404)
        self.login_as("owner")
        self.assertEqual(self.get(f"scenes/{self.scene.pk}/").status_code, 200)
        self.character.chronicle = None
        self.character.save()
        self.assertEqual(self.get(f"journals/{self.journal.pk}/").status_code, 200)
        self.login_as("st")
        self.assertEqual(self.get(f"journals/{self.journal.pk}/").status_code, 404)
        self.login_as("staff")
        self.assertEqual(self.get(f"journals/{self.journal.pk}/").status_code, 200)

    def test_scene_visibility_is_rechecked_after_initial_lookup(self):
        self.login_as("player")
        original = scene_journal.get_object_or_404

        def fetch_then_hide(*args, **kwargs):
            obj = original(*args, **kwargs)
            if isinstance(obj, Scene):
                Scene.objects.filter(pk=obj.pk).update(visibility=Scene.Visibility.PARTICIPANTS)
            return obj

        with patch.object(scene_journal, "get_object_or_404", fetch_then_hide):
            response = self.get(f"scenes/{self.public_scene.pk}/posts/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Not found."})

    def test_scene_membership_is_rechecked_after_initial_lookup(self):
        self.login_as("owner")
        original = scene_journal.get_object_or_404

        def fetch_then_remove(*args, **kwargs):
            obj = original(*args, **kwargs)
            if isinstance(obj, Scene):
                obj.characters.clear()
            return obj

        with patch.object(scene_journal, "get_object_or_404", fetch_then_remove):
            response = self.get(f"scenes/{self.scene.pk}/")
        self.assertEqual(response.status_code, 404)

    def test_journal_owner_is_rechecked_after_initial_lookup(self):
        self.login_as("owner")
        original = scene_journal.get_object_or_404

        def fetch_then_transfer(*args, **kwargs):
            obj = original(*args, **kwargs)
            if isinstance(obj, Journal):
                Human.objects.filter(pk=obj.character_id).update(owner=self.users["player"])
            return obj

        with patch.object(scene_journal, "get_object_or_404", fetch_then_transfer):
            response = self.get(f"journals/{self.journal.pk}/entries/")
        self.assertEqual(response.status_code, 404)
        self.assertNotIn(b"Stored journal text", response.content)

    def test_journal_storyteller_scope_is_rechecked_after_initial_lookup(self):
        self.login_as("st")
        original = scene_journal.get_object_or_404

        def fetch_then_revoke(*args, **kwargs):
            obj = original(*args, **kwargs)
            if isinstance(obj, Journal):
                STRelationship.objects.filter(user=self.users["st"]).delete()
            return obj

        with patch.object(scene_journal, "get_object_or_404", fetch_then_revoke):
            response = self.get(f"characters/{self.character.pk}/journal/")
        self.assertEqual(response.status_code, 404)

    def test_reparented_journal_cannot_serve_another_characters_entries(self):
        self.login_as("owner")
        self.other_journal.delete()
        original = scene_journal.get_object_or_404

        def fetch_then_reparent(*args, **kwargs):
            obj = original(*args, **kwargs)
            if isinstance(obj, Journal):
                Journal.objects.filter(pk=obj.pk).update(character=self.other_character)
            return obj

        with patch.object(scene_journal, "get_object_or_404", fetch_then_reparent):
            response = self.get(f"journals/{self.journal.pk}/entries/")
        self.assertEqual(response.status_code, 404)
        self.assertNotIn(b"Stored journal text", response.content)

    def test_head_storyteller_and_nonstaff_superuser_have_native_read_access(self):
        user = self.users["other_chronicle_st"]
        self.chronicle.head_st = user
        self.chronicle.save()
        self.login_as("other_chronicle_st")
        self.assertEqual(self.get(f"journals/{self.journal.pk}/").status_code, 200)
        self.assertEqual(self.get(f"scenes/{self.scene.pk}/").status_code, 200)
        self.chronicle.head_st = None
        self.chronicle.save()
        self.assertEqual(self.get(f"journals/{self.journal.pk}/").status_code, 404)
        user.is_superuser = True
        user.save()
        self.login_as("other_chronicle_st")
        self.assertFalse(user.is_staff)
        self.assertEqual(self.get(f"journals/{self.journal.pk}/entries/").status_code, 200)
        self.assertEqual(self.get(f"scenes/{self.scene.pk}/posts/").status_code, 200)

    def test_orphan_chronicle_scene_stays_hidden_even_from_cast_owner(self):
        self.chronicle_scene.chronicle = None
        self.chronicle_scene.save()
        self.chronicle_scene.characters.add(self.character)
        self.login_as("owner")
        self.assertEqual(self.get(f"scenes/{self.chronicle_scene.pk}/").status_code, 404)
        self.assertNotIn(
            self.chronicle_scene.pk, [r["id"] for r in self.get("scenes/").json()["results"]]
        )
        self.login_as("staff")
        self.assertEqual(self.get(f"scenes/{self.chronicle_scene.pk}/").status_code, 200)

    def test_nested_query_cannot_replace_the_authorized_parent(self):
        self.login_as("player")
        scene = self.get(f"scenes/{self.public_scene.pk}/posts/?scene_id={self.scene.pk}")
        journal = self.get(
            f"journals/{self.other_journal.pk}/entries/?journal_id={self.journal.pk}"
        )
        self.assertEqual(scene.status_code, 400)
        self.assertEqual(journal.status_code, 400)
        self.assertNotIn(b"Stored RP text", scene.content)
        self.assertNotIn(b"Stored journal text", journal.content)

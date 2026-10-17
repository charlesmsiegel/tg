"""Exact native Human reads: public catalog facts, private rows, identity and snapshots."""

from unittest.mock import patch

from django.db import connection
from django.test import TestCase, override_settings
from django.test.utils import CaptureQueriesContext

from characters.models.core import (
    Archetype,
    Background,
    BackgroundRating,
    Derangement,
    Human,
    MeritFlaw,
    MeritFlawRating,
    Specialty,
)
from characters.models.mage import Mage
from core.api import human_read
from core.constants import CharacterStatus
from core.models import Book, BookReference, Language, Number
from core.tests.action_audience import AUDIENCE, ActionAudienceMixin
from game.models import ObjectType, STRelationship

BASE = "/api/v1/"
MANIFEST = BASE + "character-profiles/human-v1/"
CATALOG = BASE + "catalogs/human-v1/"


class HumanReadTests(ActionAudienceMixin, TestCase):
    gameline_code = "wod"

    def setUp(self):
        super().setUp()
        self.human = Human.objects.create(
            name="Native Human",
            owner=self.users["owner"],
            chronicle=self.chronicle,
            notes=None,
            history=None,
            goals=None,
            st_notes="PRIVATE_ST_NOTE",
            description="Description",
            public_info="Public",
            spent_freebies=[{"private": "LEGACY_SECRET"}],
        )
        self.url = f"{BASE}characters/{self.human.pk}/human-profile/"
        self.bg = Background.objects.create(
            name="Contacts", property_name="contacts", alternate_name="Friends"
        )
        self.rows = [
            BackgroundRating.objects.create(
                char=self.human,
                bg=self.bg,
                rating=rating,
                note="Same note",
                url="/private-target/",
                complete=True,
                pooled=True,
                display_alt_name=True,
            )
            for rating in (2, 3)
        ]
        self.merit = MeritFlaw.objects.create(
            name="Mixed Reference",
            description="PRIVATE_REFERENCE_DESCRIPTION",
            st_notes="PRIVATE_REFERENCE_ST",
        )
        self.merit.add_ratings([-3, 2])
        allowed = ObjectType.objects.create(name="Human", type="char", gameline="wod")
        self.merit.allowed_types.add(allowed)
        self.mf = MeritFlawRating.objects.create(character=self.human, mf=self.merit, rating=-3)
        self.specialty = Specialty.objects.create(
            name="Running", stat="athletics", st_notes="PRIVATE_SPECIALTY_ST"
        )
        self.language = Language.objects.create(name="English", frequency=1)
        self.derangement = Derangement.objects.create(
            name="Reference", st_notes="PRIVATE_DERANGEMENT_ST"
        )
        self.archetype = Archetype.objects.create(name="Survivor", st_notes="PRIVATE_ARCHETYPE_ST")
        self.human.nature = self.archetype
        self.human.specialties.add(self.specialty)
        self.human.languages.add(self.language)
        self.human.derangements.add(self.derangement)
        self.human.save()
        self.book = Book.objects.create(name="Reference book", edition="20th")
        self.source = BookReference.objects.create(book=self.book, page=0)
        self.human.sources.add(self.source)

    def test_all_routes_require_session_and_reject_mutating_methods(self):
        for url in (MANIFEST, CATALOG + "backgrounds/", self.url):
            self.assertEqual(self.client.get(url).status_code, 401)
        self.login_as("owner")
        for url in (MANIFEST, CATALOG + "backgrounds/", self.url):
            for method in ("post", "put", "patch", "delete"):
                with self.subTest(url=url, method=method):
                    self.assertEqual(getattr(self.client, method)(url).status_code, 405)

    def test_private_human_exact_native_audience(self):
        for who in AUDIENCE:
            self.login_as(who)
            expected = (
                200
                if who in {"owner", "st", "other_line_st", "staff"}
                else 401 if who == "anonymous" else 404
            )
            with self.subTest(who=who):
                self.assertEqual(self.client.get(self.url).status_code, expected)

    def test_public_character_does_not_expose_full_profile(self):
        self.human.visibility = "PUB"
        self.human.save()
        self.login_as("player")
        hidden = self.client.get(self.url)
        missing = self.client.get(f"{BASE}characters/999999/human-profile/")
        self.assertEqual(hidden.status_code, 404)
        self.assertEqual(hidden.content, missing.content)

    def test_authorized_subtypes_reject_instead_of_downcasting(self):
        mage = Mage.objects.create(
            name="Not a plain Human", owner=self.users["owner"], chronicle=self.chronicle
        )
        url = f"{BASE}characters/{mage.pk}/human-profile/"
        self.login_as("owner")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"], "unsupported_type")
        self.login_as("player")
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_profile_preserves_nullable_scalars_and_independent_relation_rows(self):
        self.login_as("owner")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["profile"], "tg-human-v1")
        self.assertFalse(data["complete"])
        self.assertEqual(data["identity"], {"kind": "character", "id": str(self.human.pk)})
        fields = data["character"]
        self.assertEqual(fields["type"], "human")
        self.assertEqual(fields["owner_id"], str(self.users["owner"].pk))
        self.assertEqual(fields["chronicle_id"], str(self.chronicle.pk))
        for key in ("notes", "history", "goals", "date_of_birth"):
            self.assertIsNone(fields[key])
        self.assertEqual(fields["nature_id"], str(self.archetype.pk))
        self.assertIsNone(fields["demeanor_id"])
        rows = data["relations"]["backgrounds"]
        self.assertEqual([row["id"] for row in rows], [str(row.pk) for row in self.rows])
        self.assertEqual([row["rating"] for row in rows], [2, 3])
        self.assertTrue(
            all(
                row["bg_id"] == str(self.bg.pk)
                and row["note"] == "Same note"
                and row["pooled"]
                and row["complete"]
                and row["display_alt_name"]
                and row["url"] == "/private-target/"
                for row in rows
            )
        )
        self.assertEqual(
            data["relations"]["merits_flaws"],
            [{"id": str(self.mf.pk), "mf_id": str(self.merit.pk), "rating": -3}],
        )
        self.assertEqual(data["relations"]["specialties"], [{"id": str(self.specialty.pk)}])
        self.assertEqual(data["relations"]["languages"], [{"id": str(self.language.pk)}])
        self.assertEqual(data["relations"]["derangements"], [{"id": str(self.derangement.pk)}])
        self.assertEqual(
            data["relations"]["sources"],
            [{"id": str(self.source.pk), "book_id": str(self.book.pk), "page": 0}],
        )
        self.assertIn("no-store", response["Cache-Control"])

    def test_fixed_redactions_and_read_only_capabilities_apply_even_to_staff(self):
        for who in ("owner", "st", "staff"):
            self.login_as(who)
            response = self.client.get(self.url)
            data = response.json()
            self.assertNotIn(b"PRIVATE_", response.content)
            self.assertNotIn(b"LEGACY_SECRET", response.content)
            self.assertNotIn("st_notes", data["character"])
            self.assertNotIn("spent_freebies", data["character"])
            self.assertIn("st_notes", data["redactions"])
            self.assertIn("image", data["redactions"])
            self.assertIn("spent_freebies", data["redactions"])
            self.assertEqual(
                data["capabilities"],
                {
                    "read": True,
                    "create": False,
                    "update": False,
                    "delete": False,
                    "compare_and_swap": False,
                },
            )

    def test_snapshot_stable_principal_bound_and_unaffected_by_hidden_fields(self):
        self.login_as("owner")
        first = self.client.get(self.url).json()["snapshot_token"]
        self.assertEqual(first, self.client.get(self.url).json()["snapshot_token"])
        Human.objects.filter(pk=self.human.pk).update(
            st_notes="DIFFERENT_SECRET", spent_freebies=[{"secret": "changed"}]
        )
        self.assertEqual(first, self.client.get(self.url).json()["snapshot_token"])
        self.login_as("st")
        self.assertNotEqual(first, self.client.get(self.url).json()["snapshot_token"])
        self.login_as("owner")
        self.rows[0].note = "Changed exposed row"
        self.rows[0].save()
        self.assertNotEqual(first, self.client.get(self.url).json()["snapshot_token"])

    def test_native_bounds_are_preserved_without_wod_base_clamping(self):
        Human.objects.filter(pk=self.human.pk).update(
            strength=0,
            dexterity=10,
            alertness=10,
            willpower=10,
            temporary_willpower=0,
            age=65535,
            apparent_age=0,
            freebies=-2,
            current_health_levels="ALLBBBB",
            max_health_levels=7,
        )
        self.login_as("owner")
        fields = self.client.get(self.url).json()["character"]
        self.assertEqual(fields["attributes"]["strength"], 0)
        self.assertEqual(fields["attributes"]["dexterity"], 10)
        self.assertEqual(fields["abilities"]["alertness"], 10)
        self.assertEqual(fields["temporary_willpower"], 0)
        self.assertEqual(fields["age"], 65535)
        self.assertEqual(fields["freebies"], -2)
        self.assertEqual(fields["current_health_levels"], "ALLBBBB")
        self.assertEqual(fields["wound_penalty"], -1000)
        manifest = self.client.get(MANIFEST).json()
        self.assertEqual(manifest["bounds"]["attributes"], {"min": 0, "max": 10})
        self.assertEqual(manifest["bounds"]["merit_flaw_rating"], {"min": -10, "max": 10})
        self.assertEqual(manifest["id_encoding"], "decimal-string")
        self.assertFalse(manifest["archive_complete"])

    def test_native_ids_beyond_javascript_precision_are_exact_strings(self):
        big = 2**53 + 7
        human = Human.objects.create(id=big, name="Large id", owner=self.users["owner"])
        bg = Background.objects.create(id=big, name="Large definition", property_name="contacts")
        row = BackgroundRating.objects.create(id=big, char=human, bg=bg, rating=1)
        self.login_as("owner")
        data = self.client.get(f"{BASE}characters/{human.pk}/human-profile/").json()
        self.assertEqual(data["identity"]["id"], str(big))
        self.assertEqual(data["relations"]["backgrounds"][0]["id"], str(row.pk))
        self.assertEqual(data["relations"]["backgrounds"][0]["bg_id"], str(bg.pk))
        rows = self.client.get(CATALOG + "backgrounds/").json()["results"]
        self.assertEqual(rows[-1]["id"], str(bg.pk))

    def test_deleted_nullable_references_remain_explicit_without_replacement(self):
        self.bg.delete()
        self.merit.delete()
        self.book.delete()
        self.login_as("owner")
        data = self.client.get(self.url).json()
        self.assertEqual(len(data["relations"]["backgrounds"]), 2)
        self.assertIsNone(data["relations"]["backgrounds"][0]["bg_id"])
        self.assertIsNone(data["relations"]["merits_flaws"][0]["mf_id"])
        self.assertIsNone(data["relations"]["sources"][0]["book_id"])

    def test_catalogs_only_expose_native_public_reference_facts(self):
        self.login_as("player")
        for kind in (
            "archetypes",
            "backgrounds",
            "merits-flaws",
            "specialties",
            "languages",
            "derangements",
            "books",
        ):
            with self.subTest(kind=kind):
                response = self.client.get(CATALOG + kind + "/")
                self.assertEqual(response.status_code, 200)
                self.assertNotIn(b"PRIVATE_", response.content)
                for row in response.json()["results"]:
                    self.assertNotIn("owner_id", row)
                    self.assertNotIn("chronicle_id", row)
                    self.assertNotIn("description", row)
                    self.assertNotIn("st_notes", row)
                    self.assertIsInstance(row["id"], str)
        merit = self.client.get(CATALOG + "merits-flaws/").json()["results"][0]
        self.assertEqual(merit["ratings"], [-3, 2])
        self.assertEqual(merit["allowed_types"][0]["type"], "char")
        self.assertEqual(merit["allowed_types"][0]["gameline"], "wod")

    def test_catalog_pagination_is_bounded_and_duplicate_names_keep_identity(self):
        for _ in range(105):
            Background.objects.create(name="Repeated", property_name="custom")
        self.login_as("owner")
        first = self.client.get(CATALOG + "backgrounds/?page_size=1000").json()
        second = self.client.get(CATALOG + "backgrounds/?page_size=1000&page=2").json()
        self.assertEqual(first["count"], 106)
        self.assertEqual(len(first["results"]), 100)
        self.assertEqual(len(second["results"]), 6)
        self.assertFalse(
            {row["id"] for row in first["results"]} & {row["id"] for row in second["results"]}
        )

    def test_unknown_queries_invalid_ids_and_catalog_kinds_fail_closed(self):
        self.login_as("owner")
        for url in (
            self.url + "?include=st_notes",
            MANIFEST + "?fields=all",
            CATALOG + "backgrounds/?page=0",
            CATALOG + "backgrounds/?page=1&page=2",
            CATALOG + "books/?owner=1",
        ):
            self.assertEqual(self.client.get(url).status_code, 400)
        self.assertEqual(self.client.get(CATALOG + "users/").status_code, 404)
        for pk in (0, 2**63, 999999):
            self.assertEqual(
                self.client.get(f"{BASE}characters/{pk}/human-profile/").status_code, 404
            )

    def interleave(self, change):
        original = human_read.human_projection
        calls = 0

        def project(character):
            nonlocal calls
            data = original(character)
            calls += 1
            if calls == 1:
                change()
            return data

        return patch.object(human_read, "human_projection", side_effect=project)

    def test_scalar_and_relation_changes_between_reads_reject_mixed_snapshot(self):
        self.login_as("owner")
        changes = (
            lambda: Human.objects.filter(pk=self.human.pk).update(name="Changed"),
            lambda: BackgroundRating.objects.filter(pk=self.rows[0].pk).update(note="Changed"),
            lambda: BackgroundRating.objects.create(char=self.human, bg=self.bg, rating=1),
            lambda: BackgroundRating.objects.filter(pk=self.rows[1].pk).delete(),
            lambda: self.human.sources.clear(),
            lambda: self.human.specialties.clear(),
        )
        for change in changes:
            with self.subTest(change=change), self.interleave(change):
                response = self.client.get(self.url)
            self.assertEqual(response.status_code, 409)
            self.assertEqual(response.json()["error"], "snapshot_changed")

    def test_owner_transfer_between_reads_rechecks_canonical_permission(self):
        self.login_as("owner")
        with self.interleave(
            lambda: Human.objects.filter(pk=self.human.pk).update(owner=self.users["player"])
        ):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertNotIn(b"Native Human", response.content)

    def test_st_role_revocation_between_reads_invalidates_cached_role(self):
        self.login_as("st")
        with self.interleave(lambda: STRelationship.objects.filter(user=self.users["st"]).delete()):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_actor_deactivation_and_staff_revocation_between_reads_deny(self):
        for field in ("is_active", "is_staff"):
            self.login_as("staff")
            with self.interleave(
                lambda field=field: type(self.users["staff"])
                .objects.filter(pk=self.users["staff"].pk)
                .update(**{field: False})
            ):
                response = self.client.get(self.url)
            self.assertEqual(response.status_code, 404)
            type(self.users["staff"]).objects.filter(pk=self.users["staff"].pk).update(
                is_active=True, is_staff=True
            )

    def test_hidden_scalar_change_between_reads_neither_conflicts_nor_changes_token(self):
        self.login_as("owner")
        token = self.client.get(self.url).json()["snapshot_token"]
        with self.interleave(
            lambda: Human.objects.filter(pk=self.human.pk).update(st_notes="Hidden mutation")
        ):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["snapshot_token"], token)

    def test_relation_limit_rejects_without_silently_truncating(self):
        BackgroundRating.objects.bulk_create(
            [BackgroundRating(char=self.human, bg=self.bg, rating=1) for _ in range(499)]
        )
        self.login_as("owner")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"error": "profile_limit", "field": "backgrounds"})
        self.assertNotIn("character", response.json())

    def test_catalog_native_policy_change_fails_closed(self):
        self.login_as("owner")
        cls = human_read.catalog_view("archetypes")
        name = f"{cls.__module__}.{cls.__name__}"
        with patch.dict(human_read.VIEW_POLICIES, {name: "ACCOUNT"}):
            self.assertEqual(self.client.get(CATALOG + "archetypes/").status_code, 404)
        with patch.object(cls, "access_policy", "ACCOUNT", create=True):
            self.assertEqual(self.client.get(CATALOG + "archetypes/").status_code, 404)

    def test_catalog_reuses_native_row_visibility_queryset(self):
        self.login_as("owner")
        cls = human_read.catalog_view("archetypes")
        with patch.object(cls, "get_queryset", return_value=Archetype.objects.none()):
            response = self.client.get(CATALOG + "archetypes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)
        self.assertEqual(response.json()["results"], [])

    def test_revoked_subtype_access_hides_diagnostic(self):
        mage = Mage.objects.create(name="Not Human", owner=self.users["owner"])
        self.login_as("owner")
        original = human_read.hidden_get
        changed = False

        def fetch(queryset, **kwargs):
            nonlocal changed
            row = original(queryset, **kwargs)
            if isinstance(row, Mage) and not changed:
                changed = True
                Mage.objects.filter(pk=mage.pk).update(owner=self.users["player"])
            return row

        with patch.object(human_read, "hidden_get", side_effect=fetch):
            response = self.client.get(f"{BASE}characters/{mage.pk}/human-profile/")
        self.assertEqual(response.status_code, 404)
        self.assertNotIn(b"unsupported_type", response.content)

    def test_manifest_catalog_fields_match_actual_projection(self):
        self.login_as("owner")
        manifest = self.client.get(MANIFEST).json()
        for kind, fields in manifest["catalogs"].items():
            data = self.client.get(CATALOG + kind + "/").json()["results"][0]
            self.assertEqual(set(fields), set(data), kind)
        nested = manifest["catalog_relations"]["merits-flaws"]["allowed_types"]
        self.assertEqual(nested["fields"], ["id", "name", "type", "gameline"])

    def test_relation_limit_diagnostic_also_rechecks_revoked_permission(self):
        self.login_as("owner")

        def project(character):
            Human.objects.filter(pk=self.human.pk).update(owner=self.users["player"])
            raise human_read.ProfileError("profile_limit", "backgrounds")

        with patch.object(human_read, "human_projection", side_effect=project):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertNotIn(b"profile_limit", response.content)

    def test_catalog_model_drift_fails_closed(self):
        self.login_as("owner")
        cls = human_read.catalog_view("archetypes")
        with patch.object(cls, "model", Specialty):
            self.assertEqual(self.client.get(CATALOG + "archetypes/").status_code, 404)
        with patch.object(cls, "get_queryset", return_value=Specialty.objects.all()):
            self.assertEqual(self.client.get(CATALOG + "archetypes/").status_code, 404)

    def test_all_native_statuses_and_unattached_owner_retain_read_access(self):
        self.login_as("owner")
        for status, _label in CharacterStatus.CHOICES:
            Human.objects.filter(pk=self.human.pk).update(status=status)
            with self.subTest(status=status):
                self.assertEqual(self.client.get(self.url).status_code, 200)
        Human.objects.filter(pk=self.human.pk).update(chronicle=None)
        self.assertEqual(self.client.get(self.url).status_code, 200)
        self.login_as("st")
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_relation_reparent_between_reads_conflicts(self):
        other = Human.objects.create(name="Other", owner=self.users["owner"])
        self.login_as("owner")
        with self.interleave(
            lambda: BackgroundRating.objects.filter(pk=self.rows[0].pk).update(char=other)
        ):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 409)

    @override_settings(ALLOWED_HOSTS=["testserver", "other.example"])
    def test_snapshot_is_bound_to_origin_and_profile_prefix(self):
        self.login_as("owner")
        token = self.client.get(self.url).json()["snapshot_token"]
        self.assertNotEqual(
            token, self.client.get(self.url, HTTP_HOST="other.example").json()["snapshot_token"]
        )
        self.assertNotEqual(token, self.client.get(self.url, secure=True).json()["snapshot_token"])

    def test_profile_get_head_do_not_mutate_and_relation_queries_do_not_scale_per_row(self):
        self.login_as("owner")
        before = Human.objects.filter(pk=self.human.pk).values().get()
        self.client.get(self.url)  # Warm only Django's global content-type cache.
        with CaptureQueriesContext(connection) as small:
            response = self.client.get(self.url)
        BackgroundRating.objects.bulk_create(
            [BackgroundRating(char=self.human, bg=self.bg, rating=1) for _ in range(25)]
        )
        with CaptureQueriesContext(connection) as large:
            enlarged = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(enlarged.status_code, 200)
        self.assertEqual(len(small), len(large))
        self.assertLessEqual(len(large), 35)
        self.assertEqual(self.client.head(self.url).status_code, 200)
        self.assertEqual(before, Human.objects.filter(pk=self.human.pk).values().get())
        self.assertEqual(BackgroundRating.objects.filter(char=self.human).count(), 27)

    def test_catalog_definition_expansion_is_bounded(self):
        from_values = range(501)
        numbers = [Number(value=value) for value in from_values]
        Number.objects.bulk_create(numbers)
        self.merit.ratings.set(numbers)
        self.login_as("owner")
        response = self.client.get(CATALOG + "merits-flaws/")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"], "profile_limit")

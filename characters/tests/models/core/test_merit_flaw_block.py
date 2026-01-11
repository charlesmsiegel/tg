from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase

from characters.models.core import MeritFlaw
from characters.models.core.merit_flaw_block import MeritFlawRating
from game.models import ObjectType


class TestMeritFlaw(TestCase):
    def setUp(self):
        human = ObjectType.objects.get_or_create(name="Human", type="char", gameline="wod")[0]
        garou = ObjectType.objects.get_or_create(name="Werewolf", type="char", gameline="wta")[0]
        changeling = ObjectType.objects.get_or_create(
            name="Changeling", type="char", gameline="ctd"
        )[0]
        self.merit_flaw = MeritFlaw.objects.get_or_create(name="Test Merit")[0]
        self.merit_flaw.add_ratings([1, 2, 3])
        self.merit_flaw.allowed_types.add(human)
        self.merit_flaw.allowed_types.add(garou)
        self.merit_flaw.allowed_types.add(changeling)

    def test_add_rating(self):
        self.merit_flaw.add_rating(4)
        self.assertEqual(self.merit_flaw.max_rating, 4)

    def test_get_ratings(self):
        self.assertEqual(self.merit_flaw.get_ratings(), [1, 2, 3])
        self.merit_flaw.add_rating(4)
        self.assertEqual(self.merit_flaw.get_ratings(), [1, 2, 3, 4])


class TestMeritFlawDetailView(TestCase):
    def setUp(self) -> None:
        cache.clear()  # Clear cache before each test
        self.user = User.objects.create_user(username="Test", password="password")
        self.mf = MeritFlaw.objects.create(name="Test MeritFlaw")
        self.mf.add_ratings([1, 2])
        self.url = self.mf.get_absolute_url()

    def test_mf_detail_view_status_code(self):
        self.client.login(username="Test", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_mf_detail_view_templates(self):
        self.client.login(username="Test", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/meritflaw/detail.html")


class TestMeritFlawCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test MeritFlaw",
            "description": "Test Description",
            "ratings": [],
            "allowed_types": [],
        }
        self.url = MeritFlaw.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/meritflaw/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MeritFlaw.objects.count(), 1)
        self.assertEqual(MeritFlaw.objects.first().name, "Test MeritFlaw")


class TestMeritFlawUpdateView(TestCase):
    def setUp(self):
        self.mf = MeritFlaw.objects.create(name="Test MeritFlaw")
        self.mf.add_ratings([1, 2])
        self.valid_data = {
            "name": "Test MeritFlaw 2",
            "description": "Test Description",
            "ratings": [],
            "allowed_types": [],
        }
        self.url = self.mf.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/meritflaw/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.mf.refresh_from_db()
        self.assertEqual(self.mf.name, "Test MeritFlaw 2")


class TestMeritFlawRatingRelatedNames(TestCase):
    """Test explicit related_name attributes on MeritFlawRating ForeignKey fields."""

    def setUp(self):
        from characters.models.core import Human

        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.human = ObjectType.objects.get_or_create(name="Human", type="char", gameline="wod")[0]
        self.merit_flaw = MeritFlaw.objects.create(name="Test Merit")
        self.merit_flaw.add_ratings([1, 2, 3])
        self.merit_flaw.allowed_types.add(self.human)

        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
        )
        # Add the merit/flaw to the character
        self.character.add_mf(self.merit_flaw, 2)

    def test_meritflawrating_character_related_name(self):
        """Test MeritFlawRating.character has related_name='merit_flaw_ratings'."""
        # Access via the new explicit related_name
        ratings = self.character.merit_flaw_ratings.all()
        self.assertEqual(ratings.count(), 1)
        self.assertEqual(ratings.first().mf, self.merit_flaw)
        self.assertEqual(ratings.first().rating, 2)

    def test_meritflawrating_mf_related_name(self):
        """Test MeritFlawRating.mf has related_name='character_ratings'."""
        # Access via the new explicit related_name
        ratings = self.merit_flaw.character_ratings.all()
        self.assertEqual(ratings.count(), 1)
        self.assertEqual(ratings.first().character.pk, self.character.pk)
        self.assertEqual(ratings.first().rating, 2)


class MeritFlawRatingIndexTests(TestCase):
    """Tests for MeritFlawRating database indexes."""

    def test_merit_flaw_rating_has_character_mf_composite_index(self):
        """Test that MeritFlawRating has a composite index on (character, mf)."""
        indexes = MeritFlawRating._meta.indexes
        index_field_sets = [tuple(idx.fields) for idx in indexes]
        self.assertIn(("character", "mf"), index_field_sets)

    def test_merit_flaw_rating_character_field_has_db_index(self):
        """Test that MeritFlawRating.character ForeignKey has db_index=True."""
        character_field = MeritFlawRating._meta.get_field("character")
        self.assertTrue(character_field.db_index)

    def test_merit_flaw_rating_mf_field_has_db_index(self):
        """Test that MeritFlawRating.mf ForeignKey has db_index=True."""
        mf_field = MeritFlawRating._meta.get_field("mf")
        self.assertTrue(mf_field.db_index)

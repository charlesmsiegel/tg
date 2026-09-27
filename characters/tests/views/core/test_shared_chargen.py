"""Behavioral contracts across registered adapters, independent of their MRO."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from characters.chargen import get_workflow
from characters.models.core.attribute_block import Attribute
from characters.models.core.merit_flaw_block import MeritFlaw, MeritFlawRating
from characters.views.core import GenericCharacterDetailView


def registered_characters():
    seen = set()
    for kind, router in GenericCharacterDetailView().view_mapping.items():
        if getattr(router, "chargen_router", False) and router not in seen:
            seen.add(router)
            yield kind, router.model_class


class SharedChargenTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(username="shared-step-owner")
        cls.other = get_user_model().objects.create_user(username="shared-step-other")
        cls.language = MeritFlaw.objects.create(name="Language")
        Attribute.objects.create(name="Strength", property_name="strength")

    def setUp(self):
        self.client.force_login(self.owner)

    def character_at(self, kind, model, key, **kwargs):
        workflow = get_workflow(kind)
        position = next(i for i, step in enumerate(workflow.steps, 1) if step.key == key)
        return model.objects.create(
            name=f"{kind} {key}", owner=self.owner, creation_status=position, **kwargs
        )

    def languages(self, kind, model):
        character = self.character_at(kind, model, "languages")
        MeritFlawRating.objects.create(character=character, mf=self.language, rating=2)
        url = reverse("characters:character", args=[character.pk])
        position = character.creation_status
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="language_1"')
        self.assertContains(response, 'name="language_2"')
        character.refresh_from_db()
        self.assertEqual(character.creation_status, position)
        self.assertFalse(character.languages.exists())
        response = self.client.post(url, {"language_1": "French", "language_2": "Japanese"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url)
        character.refresh_from_db()
        self.assertGreater(character.creation_status, position)
        self.assertSetEqual(
            set(character.languages.values_list("name", flat=True)),
            {"English", "French", "Japanese"},
        )

    def test_language_get_and_post_across_existing_adapters(self):
        for kind, model in registered_characters():
            if kind in {"companion", "sorcerer"}:
                continue
            with self.subTest(kind=kind):
                self.languages(kind, model)

    def test_companion_saves_every_language_and_english(self):
        from characters.models.mage.companion import Companion

        self.languages("companion", Companion)

    def test_sorcerer_adds_english_alongside_selected_languages(self):
        from characters.models.mage.sorcerer import Sorcerer

        self.languages("sorcerer", Sorcerer)

    def test_missing_language_does_not_write_or_advance(self):
        for kind, model in registered_characters():
            with self.subTest(kind=kind):
                character = self.character_at(kind, model, "languages")
                MeritFlawRating.objects.create(character=character, mf=self.language, rating=2)
                position = character.creation_status
                response = self.client.post(
                    reverse("characters:character", args=[character.pk]), {"language_1": "French"}
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn("language_2", response.context["form"].errors)
                character.refresh_from_db()
                self.assertEqual(character.creation_status, position)
                self.assertFalse(character.languages.exists())

    def test_specialty_get_and_submission_across_adapters(self):
        for kind, model in registered_characters():
            with self.subTest(kind=kind):
                character = self.character_at(kind, model, "specialties", strength=4)
                position = character.creation_status
                url = reverse("characters:character", args=[character.pk])
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'name="strength"')
                character.refresh_from_db()
                self.assertEqual(character.status, "Un")
                response = self.client.post(url, {"strength": "Power lifting"})
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, character.get_absolute_url())
                character.refresh_from_db()
                self.assertEqual(character.status, "Sub")
                self.assertEqual(character.creation_status, position)
                self.assertTrue(
                    character.specialties.filter(stat="strength", name="Power lifting").exists()
                )

    def test_invalid_specialty_does_not_submit(self):
        for kind, model in registered_characters():
            with self.subTest(kind=kind):
                character = self.character_at(kind, model, "specialties", strength=4)
                response = self.client.post(
                    reverse("characters:character", args=[character.pk]), {}
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn("strength", response.context["form"].errors)
                character.refresh_from_db()
                self.assertEqual(character.status, "Un")
                self.assertFalse(character.specialties.exists())

    def test_ability_get_and_post_across_adapters(self):
        for kind, model in registered_characters():
            with self.subTest(kind=kind):
                character = self.character_at(kind, model, "abilities")
                position = character.creation_status
                url = reverse("characters:character", args=[character.pk])
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                form = response.context["form"]
                payload = dict.fromkeys(form.fields, 0)
                for group, total in zip(
                    ("talents", "skills", "knowledges"),
                    (
                        response.context["primary"],
                        response.context["secondary"],
                        response.context["tertiary"],
                    ),
                ):
                    for name in getattr(character, group):
                        if name in payload:
                            payload[name] = min(total, 3)
                            total -= payload[name]
                    self.assertEqual(total, 0)
                response = self.client.post(url, payload)
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, url)
                character.refresh_from_db()
                self.assertEqual(character.creation_status, position + 1)
                for name, value in payload.items():
                    self.assertEqual(getattr(character, name), value)

    def test_invalid_ability_pool_does_not_persist(self):
        for kind, model in registered_characters():
            with self.subTest(kind=kind):
                character = self.character_at(kind, model, "abilities")
                position = character.creation_status
                url = reverse("characters:character", args=[character.pk])
                form = self.client.get(url).context["form"]
                payload = dict.fromkeys(form.fields, 0)
                response = self.client.post(url, payload)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].non_field_errors())
                character.refresh_from_db()
                self.assertEqual(character.creation_status, position)

    def test_other_user_posts_leave_each_family_unchanged(self):
        self.client.force_login(self.other)
        for kind, model in registered_characters():
            for key in ("abilities", "languages", "specialties"):
                with self.subTest(kind=kind, step=key):
                    character = self.character_at(kind, model, key)
                    position = character.creation_status
                    response = self.client.post(
                        reverse("characters:character", args=[character.pk]),
                        {"language_1": "French", "strength": "Power lifting"},
                    )
                    self.assertIn(response.status_code, (403, 404))
                    character.refresh_from_db()
                    self.assertEqual(character.creation_status, position)
                    self.assertEqual(character.status, "Un")
                    self.assertFalse(character.languages.exists())
                    self.assertFalse(character.specialties.exists())

    def test_sorcerer_path_specialty_renders_and_saves_without_a_statistic_row(self):
        from characters.models.core.ability_block import Ability
        from characters.models.mage.sorcerer import LinearMagicPath, PathRating, Sorcerer

        # Rituals is an M2M relation, not a rated ability. The Sorcerer hook must
        # exclude it and include qualifying paths, which aren't Statistic rows.
        Ability.objects.create(name="Rituals", property_name="rituals")
        character = self.character_at("sorcerer", Sorcerer, "specialties")
        path = LinearMagicPath.objects.create(name="Weather Control")
        PathRating.objects.create(character=character, path=path, rating=4)
        url = reverse("characters:character", args=[character.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="weather_control"')
        response = self.client.post(url, {"weather_control": "Storms"})
        self.assertEqual(response.status_code, 302)
        character.refresh_from_db()
        self.assertEqual(character.status, "Sub")
        self.assertTrue(
            character.specialties.filter(stat="weather_control", name="Storms").exists()
        )

    def test_mage_secondary_abilities_are_not_allocated_or_overwritten(self):
        from characters.models.mage.mtahuman import MtAHuman

        character = self.character_at(MtAHuman.type, MtAHuman, "abilities", animal_kinship=5)
        url = reverse("characters:character", args=[character.pk])
        form = self.client.get(url).context["form"]
        self.assertNotIn("animal_kinship", form.fields)
        payload = dict.fromkeys(form.fields, 0)
        for group, total in zip(("talents", "skills", "knowledges"), (11, 7, 4)):
            for name in getattr(character, group):
                if name in payload:
                    payload[name] = min(total, 3)
                    total -= payload[name]
        response = self.client.post(url, {**payload, "animal_kinship": 0})
        self.assertEqual(response.status_code, 302)
        character.refresh_from_db()
        self.assertEqual(character.animal_kinship, 5)

    def test_natural_linguist_form_count_drives_saved_languages(self):
        from characters.models.mage.companion import Companion

        character = self.character_at("companion", Companion, "languages")
        MeritFlawRating.objects.create(character=character, mf=self.language, rating=1)
        linguist = MeritFlaw.objects.create(name="Natural Linguist")
        MeritFlawRating.objects.create(character=character, mf=linguist, rating=2)
        response = self.client.post(
            reverse("characters:character", args=[character.pk]),
            {"language_1": "French", "language_2": "Japanese", "language_3": "Forged"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertSetEqual(
            set(character.languages.values_list("name", flat=True)),
            {"English", "French", "Japanese"},
        )

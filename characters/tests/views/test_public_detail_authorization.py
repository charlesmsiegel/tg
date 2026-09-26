from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from characters.models.changeling.chimera import Chimera
from characters.models.core import Ability, Attribute
from characters.models.core.human import Human
from characters.models.mage.effect import Effect
from characters.models.mage.mage import Mage
from characters.models.mage.rote import Rote
from characters.models.mage.sorcerer import Sorcerer
from characters.models.werewolf.wtahuman import WtAHuman
from game.models import Chronicle, Gameline, STRelationship


class PublicCharacterDetailTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user("character_owner")
        self.other = user_model.objects.create_user("other_player")
        self.character = Human.objects.create(
            name="Unfinished hero",
            public_info="Approved public text",
            st_notes="PRIVATE ST NOTES",
            owner=self.owner,
            creation_status=1,
        )
        self.url = reverse("characters:character", kwargs={"pk": self.character.pk})

    def test_anonymous_and_other_player_get_only_public_card(self):
        for user in (None, self.other):
            with self.subTest(user=user):
                if user:
                    self.client.force_login(user)
                else:
                    self.client.logout()
                response = self.client.get(self.url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Unfinished hero")
                self.assertContains(response, "Approved public text")
                self.assertNotContains(response, "PRIVATE ST NOTES")
                self.assertNotIn("object", response.context)
                self.assertNotIn("character", response.context)

    def test_anonymous_and_other_player_cannot_post_current_step(self):
        for user in (None, self.other):
            with self.subTest(user=user):
                if user:
                    self.client.force_login(user)
                else:
                    self.client.logout()
                self.assertIn(self.client.post(self.url, {}).status_code, {403, 404})
                self.character.refresh_from_db()
                self.assertEqual(self.character.creation_status, 1)

    def test_owner_get_does_not_advance_freebie_step(self):
        self.character.creation_status = 5
        self.character.freebies = 0
        self.character.save()
        self.client.force_login(self.owner)
        self.client.get(self.url)
        self.character.refresh_from_db()
        self.assertEqual(self.character.creation_status, 5)

    def test_approved_owner_gets_full_sheet_without_edit_permission(self):
        Human.objects.filter(pk=self.character.pk).update(status="App")
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/core/human/detail.html")
        self.assertTrue(response.context["is_approved_user"])

    def test_owner_cannot_mark_character_deceased(self):
        Human.objects.filter(pk=self.character.pk).update(status="App")
        self.client.force_login(self.owner)
        self.assertEqual(self.client.post(self.url, {"decease": "1"}).status_code, 302)
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "App")

    def test_character_index_uses_public_fields_only(self):
        self.character.visibility = "PUB"
        self.character.save(update_fields=["visibility"])
        response = self.client.get(reverse("characters:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/public_object_list.html")
        self.assertContains(response, "Approved public text")
        self.assertNotContains(response, "PRIVATE ST NOTES")
        self.assertNotContains(response, self.owner.username)

        self.client.force_login(self.owner)
        response = self.client.get(reverse("characters:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("character_form", response.context)


class SkipStepReadOnlyTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user("skip_step_owner")
        self.client.force_login(self.owner)

    def test_language_skip_requires_post_to_advance(self):
        character = WtAHuman.objects.create(
            name="Language skip", owner=self.owner, status="Un", creation_status=6
        )
        url = reverse("characters:character", args=[character.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Continue")
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 6)
        self.assertEqual(character.languages.count(), 0)
        self.assertEqual(self.client.post(url, {}).status_code, 302)
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 7)

    def test_sorcerer_skip_requires_post_to_advance(self):
        character = Sorcerer.objects.create(
            name="Psychic skip", owner=self.owner, status="Un",
            creation_status=4, sorcerer_type="hedge_mage",
        )
        url = reverse("characters:character", args=[character.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Continue")
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 4)
        self.assertEqual(self.client.post(url, {}).status_code, 302)
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 5)


class CreatedObjectPublicCardTests(TestCase):
    def test_rote_effect_and_chimera_public_cards_hide_full_details(self):
        owner = get_user_model().objects.create_user("created_object_owner")
        for model in (Rote, Effect, Chimera):
            with self.subTest(model=model.__name__):
                extra = {}
                if model is Rote:
                    extra = {
                        "effect": Effect.objects.create(name="Card effect"),
                        "attribute": Attribute.objects.create(
                            name="Card attribute", property_name="card_attribute"
                        ),
                        "ability": Ability.objects.create(
                            name="Card ability", property_name="card_ability"
                        ),
                    }
                obj = model.objects.create(
                    name=f"Private {model.__name__}", owner=owner,
                    status="App", public_info="Public description",
                    description="OWNER ONLY DETAIL",
                    **extra,
                )
                self.client.logout()
                public = self.client.get(obj.get_absolute_url())
                self.assertEqual(public.status_code, 200)
                self.assertTemplateUsed(public, "core/public_object_detail.html")
                self.assertContains(public, "Public description")
                self.assertNotContains(public, "OWNER ONLY DETAIL")

                self.client.force_login(owner)
                full = self.client.get(obj.get_absolute_url())
                self.assertEqual(full.status_code, 200)
                self.assertNotIn("core/public_object_detail.html", [
                    template.name for template in full.templates
                ])
                self.assertEqual(full.context["object"].pk, obj.pk)


class MageStepAuthorizationTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("mage_step_owner")
        self.other = users.objects.create_user("mage_step_other")
        self.st = users.objects.create_user("mage_step_st")
        self.wrong_line_st = users.objects.create_user("mage_step_wrong_line")
        self.head = users.objects.create_user("mage_step_head")
        self.staff = users.objects.create_user("mage_step_staff", is_staff=True)
        self.chronicle = Chronicle.objects.create(name="Mage step chronicle", head_st=self.head)
        mage = Gameline.objects.create(name="Mage: the Ascension")
        vampire = Gameline.objects.create(name="Vampire: the Masquerade")
        STRelationship.objects.create(user=self.st, chronicle=self.chronicle, gameline=mage)
        STRelationship.objects.create(
            user=self.wrong_line_st, chronicle=self.chronicle, gameline=vampire
        )
        self.mage = Mage.objects.create(
            name="Unfinished mage", owner=self.owner, chronicle=self.chronicle,
            status="Un", creation_status=5, st_notes="PRIVATE MAGE NOTES",
        )
        self.url = reverse("characters:character", args=[self.mage.pk])

    def test_unapproved_mage_focus_step_is_private_and_read_does_not_mutate(self):
        for user in (None, self.other):
            with self.subTest(user=user):
                if user is None:
                    self.client.logout()
                else:
                    self.client.force_login(user)
                response = self.client.get(self.url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Unfinished mage")
                self.assertNotContains(response, "PRIVATE MAGE NOTES")
                self.assertIn(self.client.post(self.url, {}).status_code, {403, 404})
                self.mage.refresh_from_db()
                self.assertEqual(self.mage.creation_status, 5)

    def test_owner_and_scoped_storytellers_can_open_focus_step(self):
        for user in (self.owner, self.st, self.head, self.staff):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                self.assertEqual(self.client.get(self.url).status_code, 200)
                self.mage.refresh_from_db()
                self.assertEqual(self.mage.creation_status, 5)

    def test_other_gameline_storyteller_cannot_submit_focus_step(self):
        self.client.force_login(self.wrong_line_st)
        self.assertIn(self.client.post(self.url, {}).status_code, {403, 404})
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.creation_status, 5)

    def test_owner_cannot_mark_mage_deceased_but_head_st_can(self):
        Mage.objects.filter(pk=self.mage.pk).update(status="App")
        self.client.force_login(self.owner)
        self.assertEqual(self.client.post(self.url, {"decease": "1"}).status_code, 403)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.status, "App")
        self.client.force_login(self.head)
        self.assertEqual(self.client.post(self.url, {"decease": "1"}).status_code, 302)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.status, "Dec")

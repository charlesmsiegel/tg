from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from characters.chargen import get_workflow
from characters.models.core import Character
from characters.models.vampire.vampire import Vampire


class WorkflowRenderingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(username="chargen-owner")
        cls.other = get_user_model().objects.create_user(username="chargen-other")

    def test_every_step_renders_for_its_owner_without_changing_progress(self):
        from characters.views.core import GenericCharacterDetailView

        self.client.force_login(self.owner)
        seen = set()
        for kind, router in GenericCharacterDetailView().view_mapping.items():
            if not getattr(router, "chargen_router", False) or router in seen:
                continue
            seen.add(router)
            character = router.model_class.objects.create(name=kind, owner=self.owner)
            for position, step in enumerate(get_workflow(kind).steps, 1):
                with self.subTest(kind=kind, position=position):
                    Character.objects.filter(pk=character.pk).update(creation_status=position)
                    response = self.client.get(reverse("characters:character", args=[character.pk]))
                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, f"Edit {character.name}")
                    self.assertEqual(response.context["step"].key, step.key)
                    self.assertEqual(
                        len(response.context["chargen_steps"]), len(router.view_mapping)
                    )
                    character.refresh_from_db()
                    self.assertEqual(character.creation_status, position)

    def test_unequal_ability_groups_keep_empty_cells_without_none_text(self):
        from unittest.mock import patch

        from django.template.loader import render_to_string

        vampire = Vampire.objects.create(name="Unequal groups", owner=self.owner, creation_status=2)
        self.client.force_login(self.owner)
        with patch.multiple(
            Vampire, talents=["alertness"], skills=["crafts", "drive"], knowledges=["academics"]
        ):
            response = self.client.get(reverse("characters:character", args=[vampire.pk]))
        rows = response.context["ability_rows"]
        self.assertEqual(len(rows), 2)
        self.assertIsNone(rows[1][0])
        self.assertEqual(rows[1][1].name, "drive")
        self.assertIsNone(rows[1][2])
        html = render_to_string("characters/core/chargen/abilities.html", {"ability_rows": rows})
        self.assertInHTML(
            '<div class="row"><div class="col-sm"></div><div class="col-sm dots"></div>'
            f'<div class="col-sm">Drive</div><div class="col-sm dots">{rows[1][1]}</div>'
            '<div class="col-sm"></div><div class="col-sm dots"></div></div>',
            html,
        )

    def test_vampire_late_forms_match_their_views(self):
        from characters.models.core.background_block import Background, BackgroundRating

        self.client.force_login(self.owner)
        vampire = Vampire.objects.create(name="Late forms", owner=self.owner)
        for position, key in ((10, "mentor"), (11, "contacts"), (12, "retainers")):
            with self.subTest(key=key):
                bg, _ = Background.objects.get_or_create(property_name=key, defaults={"name": key})
                BackgroundRating.objects.create(char=vampire, bg=bg, rating=1)
                Character.objects.filter(pk=vampire.pk).update(creation_status=position)
                response = self.client.get(reverse("characters:character", args=[vampire.pk]))
                self.assertContains(response, 'name="name"')
                self.assertEqual(response.context["step"].key, key)

    def test_background_forms_render_with_an_incomplete_rating(self):
        from functools import partial

        from characters.chargen.predicates import no_background
        from characters.models.core.background_block import Background, BackgroundRating
        from characters.views.core import GenericCharacterDetailView

        self.client.force_login(self.owner)
        seen = set()
        for kind, router in GenericCharacterDetailView().view_mapping.items():
            workflow = get_workflow(kind)
            if workflow is None or router in seen:
                continue
            seen.add(router)
            character = router.model_class.objects.create(name=kind, owner=self.owner)
            for position, step in enumerate(workflow.steps, 1):
                if not isinstance(step.skip_if, partial) or step.skip_if.func is not no_background:
                    continue
                with self.subTest(kind=kind, step=step.key):
                    bg, _ = Background.objects.get_or_create(
                        property_name=step.key, defaults={"name": step.label}
                    )
                    BackgroundRating.objects.create(char=character, bg=bg, rating=1)
                    Character.objects.filter(pk=character.pk).update(creation_status=position)
                    response = self.client.get(reverse("characters:character", args=[character.pk]))
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.context["step"].key, step.key)
                    self.assertNotIn("skip_step", response.context)
                    self.assertTrue(response.context["form"].fields)
                    body = response.content.decode()
                    missing = [
                        field.name
                        for field in response.context["form"]
                        if not (
                            getattr(field.field, "choices", None) is not None
                            and not field.field.choices
                        )
                        and f'name="{field.html_name}"' not in body
                    ]
                    self.assertEqual(
                        missing, [], msg=f"Missing fields: {kind} {step.key}: {missing}"
                    )

    def test_unauthorized_reads_and_posts_do_not_advance(self):
        vampire = Vampire.objects.create(name="Private", owner=self.owner, creation_status=8)
        url = reverse("characters:character", args=[vampire.pk])
        self.client.force_login(self.other)
        self.client.get(url)
        self.client.post(url)
        vampire.refresh_from_db()
        self.assertEqual(vampire.creation_status, 8)
        self.assertFalse(vampire.languages.exists())

    def test_skipping_language_returns_to_the_wizard(self):
        vampire = Vampire.objects.create(name="Skip", owner=self.owner, creation_status=8)
        self.client.force_login(self.owner)
        url = reverse("characters:character", args=[vampire.pk])
        response = self.client.post(url)
        self.assertRedirects(response, url)
        vampire.refresh_from_db()
        self.assertEqual(vampire.creation_status, 13)

    def test_unapproved_zero_freebies_wait_on_get_and_reject_post(self):
        vampire = Vampire.objects.create(
            name="Waiting", owner=self.owner, creation_status=7, freebies=0
        )
        self.client.force_login(self.owner)
        url = reverse("characters:character", args=[vampire.pk])
        self.assertContains(self.client.get(url), "Waiting on ST")
        self.assertEqual(self.client.post(url).status_code, 403)
        vampire.refresh_from_db()
        self.assertEqual(vampire.creation_status, 7)

    def test_terminal_specialties_submit_without_advancing_out_of_bounds(self):
        vampire = Vampire.objects.create(name="Complete", owner=self.owner, creation_status=13)
        self.client.force_login(self.owner)
        response = self.client.post(reverse("characters:character", args=[vampire.pk]))
        self.assertEqual(response.status_code, 302)
        vampire.refresh_from_db()
        self.assertEqual(vampire.status, "Sub")
        self.assertEqual(vampire.creation_status, 13)

    def test_invalid_historical_position_cannot_navigate_back(self):
        vampire = Vampire.objects.create(name="Old data", owner=self.owner, creation_status=99)
        self.assertFalse(vampire.can_navigate_back())
        self.client.force_login(self.owner)
        response = self.client.post(reverse("characters:chargen_back", args=[vampire.pk]))
        self.assertEqual(response.status_code, 302)
        vampire.refresh_from_db()
        self.assertEqual(vampire.creation_status, 99)

    def test_sorcerer_final_freebie_stops_at_required_node(self):
        from characters.models.core.background_block import Background, BackgroundRating
        from characters.models.mage.sorcerer import Sorcerer

        sorcerer = Sorcerer.objects.create(
            name="Final freebie",
            owner=self.owner,
            creation_status=8,
            freebies=1,
            freebies_approved=True,
            willpower=3,
        )
        bg = Background.objects.create(name="Node", property_name="node")
        BackgroundRating.objects.create(char=sorcerer, bg=bg, rating=1)
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("characters:character", args=[sorcerer.pk]), {"category": "Willpower"}
        )
        self.assertEqual(response.status_code, 302)
        sorcerer.refresh_from_db()
        self.assertEqual(sorcerer.freebies, 0)
        self.assertEqual(sorcerer.creation_status, 10)

        # With no outstanding backgrounds it reaches specialties exactly once.
        other = Sorcerer.objects.create(
            name="No backgrounds",
            owner=self.owner,
            creation_status=8,
            freebies=1,
            freebies_approved=True,
            willpower=3,
        )
        response = self.client.post(
            reverse("characters:character", args=[other.pk]), {"category": "Willpower"}
        )
        self.assertEqual(response.status_code, 302)
        other.refresh_from_db()
        self.assertEqual(other.creation_status, 18)

    def test_sorcerer_freebies_render_ritual_fields(self):
        from characters.models.mage.sorcerer import Sorcerer

        sorcerer = Sorcerer.objects.create(
            name="Rituals", owner=self.owner, creation_status=8, freebies=21, freebies_approved=True
        )
        self.client.force_login(self.owner)
        response = self.client.get(reverse("characters:character", args=[sorcerer.pk]))
        for name in ("name", "path", "level", "description"):
            self.assertTrue(f'name="{name}"' in response.content.decode(), name)

    def test_completed_wraith_allocations_are_skipped_on_continue_and_back(self):
        from characters.chargen.transitions import previous_position
        from characters.models.wraith.wraith import Wraith

        wraith = Wraith.objects.create(
            name="Complete allocations", owner=self.owner, creation_status=8
        )
        for i in range(2):
            wraith.add_passion("Love", f"Passion {i}", rating=5)
            wraith.add_fetter("object", f"Fetter {i}", rating=5)
        self.assertEqual(previous_position(wraith), 5)
        Character.objects.filter(pk=wraith.pk).update(creation_status=6)
        self.client.force_login(self.owner)
        url = reverse("characters:character", args=[wraith.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        wraith.refresh_from_db()
        self.assertEqual(wraith.creation_status, 6)
        self.assertEqual(self.client.post(url).status_code, 302)
        wraith.refresh_from_db()
        self.assertEqual(wraith.creation_status, 8)

    def test_multiple_background_ratings_are_completed_before_advancing(self):
        from characters.models.core.background_block import Background, BackgroundRating

        vampire = Vampire.objects.create(name="Allies", owner=self.owner, creation_status=9)
        bg = Background.objects.create(name="Allies", property_name="allies")
        for _ in range(2):
            BackgroundRating.objects.create(char=vampire, bg=bg, rating=1)
        self.client.force_login(self.owner)
        url = reverse("characters:character", args=[vampire.pk])
        for name, expected in (("First ally", 9), ("Second ally", 13)):
            response = self.client.post(url, {"npc_type": "vtmhuman", "name": name, "rank": 1})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, url)
            vampire.refresh_from_db()
            self.assertEqual(vampire.creation_status, expected)
        self.assertEqual(vampire.backgrounds.filter(complete=True).count(), 2)

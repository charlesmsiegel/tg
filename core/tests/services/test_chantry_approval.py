"""Chantry submission and revision through the approval endpoints."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from characters.models.core.background_block import Background
from characters.models.mage.effect import Effect
from game.models import Chronicle, Gameline, STRelationship
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.services import chantry_points as svc


class ChantrySubmissionFlowTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("flow_owner")
        self.st = users.objects.create_user("flow_st")
        self.chronicle = Chronicle.objects.create(name="Flow chronicle")
        mage = Gameline.objects.get_or_create(name="Mage: the Ascension")[0]
        STRelationship.objects.create(user=self.st, chronicle=self.chronicle, gameline=mage)
        self.chantry = Chantry.objects.create(
            name="Flow",
            owner=self.owner,
            chronicle=self.chronicle,
            total_points=2,
            creation_status=2,
        )
        allies = Background.objects.get_or_create(name="Allies", property_name="allies")[0]
        self.allies = ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=allies, rating=1, complete=False
        )
        self.submit = reverse("accounts:object_submission", args=["location", self.chantry.pk])
        self.revise = reverse("accounts:object_revision", args=["location", self.chantry.pk])

    def test_submit_refused_with_reasons(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.submit)
        self.assertContains(
            response,
            "Finish every creation step (the chantry is on step 2 of 6).; "
            "Allies has not been set up yet.",
            status_code=400,
        )
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.status, "Un")

    def test_valid_chantry_submits_and_return_resets_the_wizard(self):
        self.allies.complete = True
        self.allies.save()
        self.chantry.creation_status = 7
        self.chantry.save()

        self.client.force_login(self.owner)
        self.assertEqual(self.client.post(self.submit).status_code, 302)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.status, "Sub")

        self.client.force_login(self.st)
        self.assertEqual(self.client.post(self.revise).status_code, 302)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.status, "Rev")
        self.assertEqual(self.chantry.creation_status, 1)
        self.assertEqual(self.chantry.backgrounds.get().rating, 1)

    def test_return_after_purchases_keeps_them_and_only_resets_the_wizard(self):
        """Review Focus: an ST returns a chantry that has effects bought.

        The player must land on step 1 with the background rating, the
        Integrated Effects score and the chosen effect all still held.
        """
        self.allies.complete = True
        self.allies.save()
        self.chantry.creation_status = 7
        self.chantry.total_points = 6
        self.chantry.save()

        # Buy a background dot and an Integrated Effects dot through the
        # chantry_points service, then integrate an effect the way
        # ChantryEffectsForm.save() does.
        svc.buy_background_dot(self.chantry, self.allies.bg)
        svc.buy_ie_dot(self.chantry)
        effect = Effect.objects.create(name="Bolt", forces=1)
        self.chantry.integrated_effects.add(effect)

        self.client.force_login(self.owner)
        self.assertEqual(self.client.post(self.submit).status_code, 302)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.status, "Sub")

        self.client.force_login(self.st)
        self.assertEqual(self.client.post(self.revise).status_code, 302)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.status, "Rev")
        self.assertEqual(self.chantry.creation_status, 1)
        self.assertEqual(self.chantry.backgrounds.get().rating, 2)
        self.assertEqual(self.chantry.integrated_effects_score, 1)
        self.assertEqual(list(self.chantry.integrated_effects.all()), [effect])

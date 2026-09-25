from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from characters.models.core.human import Human
from game.models import Chronicle, Gameline, STRelationship


class ObjectWorkflowTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("workflow_owner")
        self.st = users.objects.create_user("workflow_st")
        self.other_st = users.objects.create_user("workflow_other_st")
        self.staff = users.objects.create_user("workflow_staff", is_staff=True)
        self.chronicle = Chronicle.objects.create(name="Workflow chronicle")
        other_chronicle = Chronicle.objects.create(name="Other chronicle")
        wod = Gameline.objects.create(name="World of Darkness")
        STRelationship.objects.create(user=self.st, chronicle=self.chronicle, gameline=wod)
        STRelationship.objects.create(
            user=self.other_st, chronicle=other_chronicle, gameline=wod
        )
        self.character = Human.objects.create(
            name="Draft hero", owner=self.owner, chronicle=self.chronicle,
            status="Un", concept="Initial concept",
        )

    def test_owner_cannot_self_approve_through_update_form(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("characters:update:character", kwargs={"pk": self.character.pk}),
            {"name": "Draft hero", "status": "App"},
        )
        self.assertEqual(response.status_code, 403)
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "Un")

    def test_submit_return_resubmit_and_approve(self):
        submit = reverse("accounts:object_submission", args=["character", self.character.pk])
        revise = reverse("accounts:object_revision", args=["character", self.character.pk])
        approve = reverse("accounts:object_approval", args=["character", self.character.pk])
        update = reverse("characters:update:character", kwargs={"pk": self.character.pk})

        self.client.force_login(self.owner)
        self.assertEqual(self.client.post(submit).status_code, 302)
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "Sub")
        self.assertEqual(self.client.get(update).status_code, 403)

        self.client.force_login(self.other_st)
        self.assertEqual(self.client.post(revise).status_code, 403)
        self.client.force_login(self.st)
        response = self.client.post(revise)
        self.assertEqual(response.status_code, 302, response.content)
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "Rev")

        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(update).status_code, 200)
        self.assertEqual(self.client.post(submit).status_code, 302)
        self.client.force_login(self.st)
        self.assertEqual(self.client.post(approve).status_code, 302)
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "App")
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(update).status_code, 403)

    def test_staff_can_edit_submitted_object(self):
        self.character.status = "Sub"
        self.character.save()
        self.client.force_login(self.staff)
        response = self.client.get(
            reverse("characters:update:character", kwargs={"pk": self.character.pk})
        )
        self.assertEqual(response.status_code, 200)

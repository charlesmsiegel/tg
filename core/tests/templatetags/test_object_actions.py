"""The object_actions tag hides Submit while a model reports submission errors."""

from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.test import RequestFactory, TestCase

from characters.models.core.human import Human
from game.models import Chronicle
from locations.models.mage.chantry import Chantry


def render_actions(obj, user):
    request = RequestFactory().get("/")
    request.user = user
    template = Template("{% load object_actions %}{% object_actions %}")
    return template.render(Context({"object": obj, "request": request}))


class ObjectActionsTagTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user("actions_owner")
        self.chronicle = Chronicle.objects.create(name="Actions chronicle")

    def test_unfinished_chantry_lists_reasons_instead_of_submit(self):
        chantry = Chantry.objects.create(
            name="Draft", owner=self.owner, chronicle=self.chronicle, creation_status=3
        )
        html = render_actions(chantry, self.owner)
        self.assertNotIn("Submit for approval", html)
        self.assertIn("Finish creation first", html)
        self.assertIn("Finish every creation step (the chantry is on step 3 of 6).", html)

    def test_finished_chantry_shows_submit(self):
        chantry = Chantry.objects.create(
            name="Done",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=7,
            total_points=0,
        )
        html = render_actions(chantry, self.owner)
        self.assertIn("Submit for approval", html)
        self.assertNotIn("Finish creation first", html)

    def test_model_without_hook_shows_submit(self):
        character = Human.objects.create(
            name="Plain", owner=self.owner, chronicle=self.chronicle, status="Un"
        )
        html = render_actions(character, self.owner)
        self.assertIn("Submit for approval", html)
        self.assertNotIn("Finish creation first", html)

    def test_reasons_hidden_from_viewers_who_cannot_submit(self):
        chantry = Chantry.objects.create(
            name="Draft", owner=self.owner, chronicle=self.chronicle, creation_status=3
        )
        stranger = get_user_model().objects.create_user("actions_stranger")
        self.assertNotIn("Finish creation first", render_actions(chantry, stranger))

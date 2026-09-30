"""The canonical character page (``characters:character``) outside the wizard.

A chargen router renders its ``default_redirect`` once a character has left
creation. That view must carry an access policy, or ``AuthorizationMiddleware``'s
evaluator answers 403 on the character's own page.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from characters.models.demon.demon import Demon
from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.thrall import Thrall
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.vampire import Vampire
from characters.views.core import GenericCharacterDetailView
from core.access_policy import route_name, route_policy
from core.views.generic import DictView


class ChargenRouterFallbackPolicyTests(TestCase):
    def test_every_chargen_router_falls_back_to_a_declared_view(self):
        for type_name, view in GenericCharacterDetailView().view_mapping.items():
            if not (isinstance(view, type) and issubclass(view, DictView)):
                continue
            fallback = view.default_redirect
            if isinstance(fallback, str):
                continue
            with self.subTest(type=type_name, fallback=route_name(fallback)):
                self.assertIsNotNone(route_policy(fallback))


class CanonicalPageOutsideWizardTests(TestCase):
    MODELS = (Vampire, Ghoul, Demon, DtFHuman, Thrall)

    def setUp(self):
        self.owner = get_user_model().objects.create_user("router_owner")
        self.client.force_login(self.owner)

    def test_owner_sees_the_sheet_once_the_character_is_submitted(self):
        for model in self.MODELS:
            for status in ("Sub", "App"):
                with self.subTest(model=model.__name__, status=status):
                    character = model.objects.create(
                        name=f"{model.__name__} {status}", owner=self.owner
                    )
                    model.objects.filter(pk=character.pk).update(status=status)
                    url = reverse("characters:character", kwargs={"pk": character.pk})
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.context["object"].pk, character.pk)

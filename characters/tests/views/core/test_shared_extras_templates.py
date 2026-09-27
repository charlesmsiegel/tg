"""Behavior contracts for biography steps and optional starting templates."""

from importlib import import_module

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from characters.chargen import get_workflow
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.mage.companion import Advantage, Companion
from characters.models.werewolf.charm import SpiritCharm
from characters.views.core import GenericCharacterDetailView
from core.models import CharacterTemplate, TemplateApplication

TEMPLATE_FLOWS = (
    ("changeling.ctdhuman", "CtDHuman", "ctd", "changeling"),
    ("demon.dtfhuman_chargen", "DtFHuman", "dtf", "demon"),
    ("mage.mtahuman", "MtAHuman", "mta", "mage"),
    ("vampire.vtmhuman", "VtMHuman", "vtm", "vampire"),
    ("werewolf.wtahuman", "WtAHuman", "wta", "werewolf"),
    ("wraith.wtohuman", "WtOHuman", "wto", "wraith"),
)


def biography_cases():
    seen = set()
    for kind, router in GenericCharacterDetailView().view_mapping.items():
        workflow = get_workflow(kind)
        if workflow is None or router in seen:
            continue
        seen.add(router)
        for position, step in enumerate(workflow.steps, 1):
            if step.key == "biography":
                yield router.model_class, position, step.view


class ExtrasCharacterizationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(username="extras-owner")
        cls.other = get_user_model().objects.create_user(username="extras-other")
        cls.thaumivore = MeritFlaw.objects.create(name="Thaumivore")
        cls.thaumivore.add_rating(-5)
        cls.bond = Advantage.objects.create(name="Bond-Sharing")
        cls.bond.add_rating(4)
        cls.paradox = Advantage.objects.create(name="Paradox Nullification")
        cls.paradox.add_rating(2)
        cls.charm = SpiritCharm.objects.create(name="Airt Sense")

    def setUp(self):
        self.client.force_login(self.owner)

    def payload(self, character):
        response = self.client.get(reverse("characters:character", args=[character.pk]))
        self.assertEqual(response.status_code, 200)
        data = {}
        for name, field in response.context["form"].fields.items():
            if isinstance(field, forms.DateField):
                data[name] = "1990-01-02"
            elif isinstance(field, forms.IntegerField):
                data[name] = 30
            elif isinstance(field, forms.ChoiceField):
                data[name] = next(value for value, _ in field.choices if value != "")
            else:
                data[name] = "Biography " + name
        return data

    def test_all_registered_biographies_save_every_field_and_advance(self):
        for model, position, _view in biography_cases():
            with self.subTest(model=model.__name__):
                character = model.objects.create(
                    name=model.__name__, owner=self.owner, creation_status=position
                )
                data = self.payload(character)
                character.refresh_from_db()
                self.assertEqual(character.creation_status, position, "GET must be read-only")
                response = self.client.post(
                    reverse("characters:character", args=[character.pk]),
                    {**data, "xp": 999, "status": "App"},
                )
                self.assertEqual(response.status_code, 302, getattr(response, "context", None))
                character.refresh_from_db()
                self.assertEqual(
                    character.creation_status, get_workflow(character.type).freebie_step
                )
                self.assertEqual(character.xp, 0)
                self.assertEqual(character.status, "Un")
                for name, value in data.items():
                    self.assertEqual(str(getattr(character, name)), str(value), name)

    def test_all_biographies_reject_invalid_dates_without_saving(self):
        for model, position, _view in biography_cases():
            with self.subTest(model=model.__name__):
                character = model.objects.create(
                    name="Invalid", owner=self.owner, creation_status=position
                )
                data = self.payload(character)
                data["date_of_birth"] = "not a date"
                response = self.client.post(
                    reverse("characters:character", args=[character.pk]), data
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn("date_of_birth", response.context["form"].errors)
                character.refresh_from_db()
                self.assertEqual(character.creation_status, position)
                self.assertEqual(character.history, "")

    def test_companion_budgets_and_familiar_grants(self):
        position = next(position for model, position, _ in biography_cases() if model is Companion)
        for kind, npc, expected in (
            ("companion", False, 15),
            ("consor", False, 21),
            ("familiar", False, 24),
            ("familiar", True, 14),
        ):
            with self.subTest(kind=kind, npc=npc):
                character = Companion.objects.create(
                    name=kind,
                    owner=self.owner,
                    creation_status=position,
                    companion_type=kind,
                    npc=npc,
                )
                self.client.post(
                    reverse("characters:character", args=[character.pk]), self.payload(character)
                )
                character.refresh_from_db()
                self.assertEqual(character.freebies, expected)
                if kind == "familiar":
                    self.assertEqual(character.advantage_rating(self.bond), 4)
                    self.assertEqual(character.advantage_rating(self.paradox), 2)
                    self.assertTrue(character.charms.filter(pk=self.charm.pk).exists())
                    self.assertTrue(
                        character.merits_and_flaws.filter(pk=self.thaumivore.pk).exists()
                    )
                    self.assertEqual(len(character.spent_freebies), 3)

    def test_direct_biography_posts_reject_nonowners_and_locked_characters(self):
        for model, position, view in biography_cases():
            for user, status in ((self.other, "Un"), (self.owner, "App")):
                with self.subTest(model=model.__name__, status=status, user=user.username):
                    character = model.objects.create(
                        name="Protected", owner=self.owner, creation_status=position, status=status
                    )
                    request = RequestFactory().post("/biography/", {"history": "Forged"})
                    request.user = user
                    with self.assertRaises(Http404):
                        view.as_view()(request, pk=character.pk)
                    character.refresh_from_db()
                    self.assertEqual(character.creation_status, position)
                    self.assertEqual(character.history, "")

    def test_returned_biographies_can_save_and_preserve_returned_status(self):
        for model, position, _view in biography_cases():
            with self.subTest(model=model.__name__):
                character = model.objects.create(
                    name="Returned", owner=self.owner, creation_status=position, status="Rev"
                )
                response = self.client.post(
                    reverse("characters:character", args=[character.pk]), self.payload(character)
                )
                self.assertEqual(response.status_code, 302)
                character.refresh_from_db()
                self.assertEqual(
                    character.creation_status, get_workflow(character.type).freebie_step
                )
                self.assertEqual(character.status, "Rev")

    def test_wraith_requires_both_death_fields(self):
        model, position, _ = next(case for case in biography_cases() if case[0].type == "wraith")
        for missing in ("age_at_death", "death_description"):
            with self.subTest(missing=missing):
                character = model.objects.create(
                    name="Wraith", owner=self.owner, creation_status=position
                )
                data = self.payload(character)
                data[missing] = "0" if missing == "age_at_death" else ""
                response = self.client.post(
                    reverse("characters:character", args=[character.pk]), data
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn(missing, response.context["form"].errors)
                character.refresh_from_db()
                self.assertEqual(character.creation_status, position)

    def test_companion_budget_is_prepared_before_navigation_checks_freebies(self):
        position = next(position for model, position, _ in biography_cases() if model is Companion)
        character = Companion.objects.create(
            name="Consor",
            owner=self.owner,
            companion_type="consor",
            creation_status=position,
            freebies=0,
            freebies_approved=True,
        )
        response = self.client.post(
            reverse("characters:character", args=[character.pk]), self.payload(character)
        )
        self.assertEqual(response.status_code, 302)
        character.refresh_from_db()
        self.assertEqual(character.freebies, 21)
        self.assertEqual(character.creation_status, get_workflow(character.type).freebie_step)


class TemplateSelectionCharacterizationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(username="templates-owner")
        cls.other = get_user_model().objects.create_user(username="templates-other")

    def request(self, method, user=None, data=None):
        request = getattr(RequestFactory(), method)("/template/", data or {})
        request.user = self.owner if user is None else user
        request.session = {}
        request._messages = FallbackStorage(request)
        return request

    def cases(self):
        for module_name, prefix, gameline, kind in TEMPLATE_FLOWS:
            module = import_module("characters.views." + module_name)
            yield module, getattr(module, prefix), getattr(
                module, prefix + "TemplateSelectView"
            ), gameline, kind

    def test_all_template_filters_match_context_and_reject_other_templates(self):
        for module, model, view, gameline, kind in self.cases():
            with self.subTest(gameline=gameline):
                character = model.objects.create(
                    name="Template filters", owner=self.owner, creation_status=0
                )
                good = CharacterTemplate.objects.create(
                    name="Visible", gameline=gameline, character_type=kind, status="App"
                )
                hidden = CharacterTemplate.objects.create(
                    name="Private",
                    gameline=gameline,
                    character_type=kind,
                    status="App",
                    is_public=False,
                )
                CharacterTemplate.objects.create(
                    name="Unapproved", gameline=gameline, character_type=kind
                )
                CharacterTemplate.objects.create(
                    name="Wrong type", gameline=gameline, character_type="other", status="App"
                )
                CharacterTemplate.objects.create(
                    name="Wrong line " + gameline, gameline="wod", character_type=kind, status="App"
                )
                response = view.as_view()(self.request("get"), pk=character.pk)
                self.assertEqual(list(response.context_data["available_templates"]), [good])
                self.assertEqual(
                    list(response.context_data["form"].fields["template"].queryset), [good]
                )
                self.assertFalse(
                    module.CharacterTemplateSelectionForm().fields["template"].queryset.exists()
                )
                response = view.as_view()(
                    self.request("post", data={"template": hidden.pk}), pk=character.pk
                )
                self.assertIn("template", response.context_data["form"].errors)
                character.refresh_from_db()
                self.assertEqual(character.creation_status, 0)

    def test_all_template_apply_skip_and_repeat_flows(self):
        for _module, model, view, gameline, kind in self.cases():
            for apply in (False, True):
                with self.subTest(gameline=gameline, apply=apply):
                    character = model.objects.create(
                        name="Optional", owner=self.owner, creation_status=0
                    )
                    template = CharacterTemplate.objects.create(
                        name="Starting " + str(apply),
                        gameline=gameline,
                        character_type=kind,
                        status="App",
                        attributes={"strength": 3},
                    )
                    data = {"template": template.pk} if apply else {}
                    response = view.as_view()(self.request("post", data=data), pk=character.pk)
                    self.assertEqual(response.status_code, 302)
                    self.assertIn("creation", response.url)
                    character.refresh_from_db()
                    self.assertEqual(character.creation_status, 1)
                    self.assertEqual(character.strength, 3 if apply else 1)
                    self.assertEqual(
                        TemplateApplication.objects.filter(character=character).count(), int(apply)
                    )
                    response = view.as_view()(self.request("post", data=data), pk=character.pk)
                    self.assertEqual(response.status_code, 302)
                    template.refresh_from_db()
                    self.assertEqual(template.times_used, int(apply))

    def test_all_template_views_reject_nonowners(self):
        for _module, model, view, gameline, _kind in self.cases():
            with self.subTest(gameline=gameline):
                character = model.objects.create(
                    name="Private", owner=self.owner, creation_status=0
                )
                with self.assertRaises(Http404):
                    view.as_view()(self.request("post", user=self.other), pk=character.pk)
                character.refresh_from_db()
                self.assertEqual(character.creation_status, 0)

    def test_all_template_views_redirect_anonymous_before_loading_character(self):
        for _module, _model, view, gameline, _kind in self.cases():
            with self.subTest(gameline=gameline):
                response = view.as_view()(self.request("get", user=AnonymousUser()), pk=999999)
                self.assertEqual(response.status_code, 302)
                self.assertIn("login", response.url)

    def test_all_template_views_reject_locked_characters_at_position_zero(self):
        for _module, model, view, gameline, _kind in self.cases():
            for status in ("Sub", "App", "Ret", "Dec"):
                with self.subTest(gameline=gameline, status=status):
                    character = model.objects.create(
                        name="Locked", owner=self.owner, creation_status=0, status=status
                    )
                    with self.assertRaises(PermissionDenied):
                        view.as_view()(self.request("post"), pk=character.pk)
                    character.refresh_from_db()
                    self.assertEqual(character.creation_status, 0)

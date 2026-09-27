"""Character sheet action endpoints (Step 5): approve/reject XP, retire, decease,
specialties. Each is tested against the full audience, GET, and old URLs."""

from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.human import Human
from characters.models.core.specialty import Specialty
from characters.views.core import GenericCharacterDetailView
from core.tests.action_audience import ActionAudienceMixin
from game.models import XPSpendingRequest

# Expected status per audience member for each rule.
SCOPED_ST_ONLY = {
    "owner": 403,
    "player": 404,
    "st": 302,
    "other_line_st": 403,
    "other_chronicle_st": 404,
    "staff": 302,
    "anonymous": 401,
}
OWNER_OR_SCOPED_ST = {**SCOPED_ST_ONLY, "owner": 302}


def _messages(response):
    return [str(m) for m in get_messages(response.wsgi_request)]


class CharacterActionTestBase(ActionAudienceMixin, TestCase):
    def setUp(self):
        super().setUp()
        Attribute.objects.get_or_create(name="Strength", property_name="strength")
        Ability.objects.get_or_create(name="Athletics", property_name="athletics")
        self.character = Human.objects.create(
            name="Sheet Hero",
            owner=self.users["owner"],
            chronicle=self.chronicle,
            status="App",
            xp=30,
            strength=3,
        )

    def new_request(self, **kwargs):
        fields = {
            "character": self.character,
            "trait_name": "Strength",
            "trait_type": "attribute",
            "trait_value": 4,
            "cost": 12,
        }
        fields.update(kwargs)
        return XPSpendingRequest.objects.create(**fields)


class XPDecisionActionTests(CharacterActionTestBase):
    def url(self, name, xp_request):
        return reverse(name, kwargs={"pk": self.character.pk, "request_pk": xp_request.pk})

    def test_approve_matrix(self):
        for who, expected in SCOPED_ST_ONLY.items():
            with self.subTest(who=who):
                xp_request = self.new_request()
                self.login_as(who)
                response = self.client.post(self.url("characters:xp_request_approve", xp_request))
                self.assertEqual(response.status_code, expected)
                xp_request.refresh_from_db()
                self.assertEqual(xp_request.approved, "Approved" if expected == 302 else "Pending")

    def test_reject_matrix(self):
        for who, expected in SCOPED_ST_ONLY.items():
            with self.subTest(who=who):
                xp_request = self.new_request()
                self.login_as(who)
                response = self.client.post(self.url("characters:xp_request_reject", xp_request))
                self.assertEqual(response.status_code, expected)
                xp_request.refresh_from_db()
                self.assertEqual(xp_request.approved, "Denied" if expected == 302 else "Pending")

    def test_approve_applies_once_and_redirects_to_sheet(self):
        xp_request = self.new_request()
        self.login_as("st")
        response = self.client.post(self.url("characters:xp_request_approve", xp_request))
        self.assertRedirects(
            response, self.character.get_absolute_url(), fetch_redirect_response=False
        )
        self.character.refresh_from_db()
        self.assertEqual(self.character.strength, 4)
        xp_request.refresh_from_db()
        self.assertEqual(xp_request.approved_by, self.users["st"])

    def test_double_submit_approve_is_idempotent(self):
        xp_request = self.new_request()
        self.login_as("st")
        url = self.url("characters:xp_request_approve", xp_request)
        self.client.post(url)
        self.character.refresh_from_db()
        after_first = (self.character.strength, self.character.xp)
        xp_request.refresh_from_db()
        first_approved_at = (xp_request.approved, xp_request.approved_by_id)

        second = self.client.post(url)

        self.assertEqual(second.status_code, 302)
        self.assertTrue(any("already approved" in m for m in _messages(second)))
        self.character.refresh_from_db()
        self.assertEqual((self.character.strength, self.character.xp), after_first)
        xp_request.refresh_from_db()
        self.assertEqual((xp_request.approved, xp_request.approved_by_id), first_approved_at)

    def test_reject_after_approve_does_not_undo_the_spend(self):
        xp_request = self.new_request()
        self.login_as("st")
        self.client.post(self.url("characters:xp_request_approve", xp_request))
        response = self.client.post(self.url("characters:xp_request_reject", xp_request))
        self.assertEqual(response.status_code, 302)
        xp_request.refresh_from_db()
        self.assertEqual(xp_request.approved, "Approved")
        self.character.refresh_from_db()
        self.assertEqual(self.character.strength, 4)

    def test_request_of_another_character_is_404(self):
        other = Human.objects.create(
            name="Other", owner=self.users["player"], chronicle=self.chronicle, status="App"
        )
        xp_request = self.new_request(character=other)
        self.login_as("st")
        response = self.client.post(
            reverse(
                "characters:xp_request_approve",
                kwargs={"pk": self.character.pk, "request_pk": xp_request.pk},
            )
        )
        self.assertEqual(response.status_code, 404)
        xp_request.refresh_from_db()
        self.assertEqual(xp_request.approved, "Pending")

    def test_st_cannot_self_approve_player_character_but_can_npc(self):
        self.character.owner = self.users["st"]
        self.character.save()
        xp_request = self.new_request()
        self.login_as("st")
        response = self.client.post(self.url("characters:xp_request_approve", xp_request))
        self.assertEqual(response.status_code, 403)

        self.character.npc = True
        self.character.save()
        response = self.client.post(self.url("characters:xp_request_approve", xp_request))
        self.assertEqual(response.status_code, 302)
        xp_request.refresh_from_db()
        self.assertEqual(xp_request.approved, "Approved")

    def test_get_is_rejected(self):
        xp_request = self.new_request()
        for who in ("anonymous", "st"):
            for name in ("characters:xp_request_approve", "characters:xp_request_reject"):
                with self.subTest(who=who, name=name):
                    self.login_as(who)
                    self.assertEqual(self.client.get(self.url(name, xp_request)).status_code, 405)
        xp_request.refresh_from_db()
        self.assertEqual(xp_request.approved, "Pending")

    def test_old_button_post_to_detail_page_changes_nothing(self):
        xp_request = self.new_request()
        self.login_as("st")
        response = self.client.post(
            reverse("characters:character", kwargs={"pk": self.character.pk}),
            {f"xp_request_{xp_request.pk}_approve": "Approve"},
        )
        self.assertEqual(response.status_code, 405)
        xp_request.refresh_from_db()
        self.assertEqual(xp_request.approved, "Pending")


class StatusActionTests(CharacterActionTestBase):
    def post(self, name):
        return self.client.post(reverse(name, kwargs={"pk": self.character.pk}))

    def reset(self):
        Human.objects.filter(pk=self.character.pk).update(status="App")

    def test_retire_matrix(self):
        for who, expected in OWNER_OR_SCOPED_ST.items():
            with self.subTest(who=who):
                self.reset()
                self.login_as(who)
                self.assertEqual(self.post("characters:retire").status_code, expected)
                self.character.refresh_from_db()
                self.assertEqual(self.character.status, "Ret" if expected == 302 else "App")

    def test_decease_matrix(self):
        for who, expected in SCOPED_ST_ONLY.items():
            with self.subTest(who=who):
                self.reset()
                self.login_as(who)
                self.assertEqual(self.post("characters:decease").status_code, expected)
                self.character.refresh_from_db()
                self.assertEqual(self.character.status, "Dec" if expected == 302 else "App")

    def test_invalid_transition_is_reported_and_changes_nothing(self):
        Human.objects.filter(pk=self.character.pk).update(status="Dec")
        self.login_as("st")
        response = self.post("characters:retire")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(any("cannot be marked retired" in m for m in _messages(response)))
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "Dec")

    def test_get_is_rejected(self):
        for who in ("anonymous", "owner"):
            for name in ("characters:retire", "characters:decease"):
                with self.subTest(who=who, name=name):
                    self.login_as(who)
                    response = self.client.get(reverse(name, kwargs={"pk": self.character.pk}))
                    self.assertEqual(response.status_code, 405)
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "App")

    def test_old_detail_post_changes_nothing(self):
        self.login_as("st")
        response = self.client.post(
            reverse("characters:character", kwargs={"pk": self.character.pk}),
            {"retire": "Mark Retired", "decease": "Mark Deceased"},
        )
        self.assertEqual(response.status_code, 405)
        self.character.refresh_from_db()
        self.assertEqual(self.character.status, "App")

    def test_buttons_point_at_the_endpoints(self):
        self.login_as("st")
        response = self.client.get(self.character.get_absolute_url())
        self.assertContains(
            response, reverse("characters:retire", kwargs={"pk": self.character.pk})
        )
        self.assertContains(
            response, reverse("characters:decease", kwargs={"pk": self.character.pk})
        )


class EveryCharacterTypeStatusTests(ActionAudienceMixin, TestCase):
    """Every mapped character type offers retire/decease, and both work."""

    def test_retire_and_decease_work_for_every_type(self):
        from django.apps import apps

        from characters.models.core import Character

        seen = set()
        for key in GenericCharacterDetailView().view_mapping:
            model = next(
                (
                    m
                    for m in apps.get_app_config("characters").get_models()
                    if issubclass(m, Character) and getattr(m, "type", None) == key
                ),
                None,
            )
            if model is None or model in seen:
                continue
            seen.add(model)
            with self.subTest(type=key):
                for target, who in (("Ret", "owner"), ("Ret", "staff"), ("Dec", "staff")):
                    character = model(
                        name=f"{key} {target} {who}",
                        owner=self.users["owner"],
                        chronicle=None,
                        status="App",
                    )
                    # Some types require chargen choices unrelated to status.
                    character.save(skip_validation=True)
                    self.login_as(who)
                    name = "characters:retire" if target == "Ret" else "characters:decease"
                    response = self.client.post(reverse(name, kwargs={"pk": character.pk}))
                    self.assertEqual(response.status_code, 302)
                    character.refresh_from_db()
                    try:
                        character.full_clean()
                    except ValidationError:
                        # An incomplete fixture cannot be saved at all; the
                        # action reports that instead of failing with a 500.
                        self.assertEqual(character.status, "App")
                        self.assertTrue(_messages(response))
                    else:
                        self.assertEqual(character.status, target)
        self.assertGreater(len(seen), 30)


class SpecialtiesActionTests(CharacterActionTestBase):
    def setUp(self):
        super().setUp()
        Human.objects.filter(pk=self.character.pk).update(status="Un", athletics=1)
        self.character.refresh_from_db()
        self.url = reverse("characters:add_specialties", kwargs={"pk": self.character.pk})

    def test_matrix(self):
        # EDIT_FULL: the owner of a draft, the scoped ST and staff.
        expected = {**SCOPED_ST_ONLY, "owner": 302}
        for who, status in expected.items():
            with self.subTest(who=who):
                self.character.specialties.clear()
                self.login_as(who)
                response = self.client.post(self.url, {"athletics": "Parkour"})
                self.assertEqual(response.status_code, status)
                self.assertEqual(
                    self.character.specialties.filter(name="Parkour").exists(), status == 302
                )

    def test_unrequested_stat_is_ignored(self):
        self.login_as("owner")
        self.client.post(self.url, {"athletics": "Parkour", "brawl": "Boxing"})
        self.assertFalse(Specialty.objects.filter(stat="brawl", name="Boxing").exists())

    def test_get_is_rejected(self):
        self.login_as("owner")
        self.assertEqual(self.client.get(self.url).status_code, 405)


class ActionRedirectTargetTests(ActionAudienceMixin, TestCase):
    """D8: actions land on the type's own sheet, not the generic router, which
    denies an approved Vampire or Demon (a Step 2 router defect)."""

    def test_retire_redirect_renders_for_router_denied_types(self):
        from characters.models.demon.demon import Demon
        from characters.models.vampire.vampire import Vampire

        self.login_as("staff")
        for model in (Vampire, Demon):
            with self.subTest(model=model.__name__):
                character = model.objects.create(
                    name=f"Redirect {model.__name__}", owner=self.users["owner"], status="App"
                )
                generic = reverse("characters:character", kwargs={"pk": character.pk})
                self.assertEqual(self.client.get(generic).status_code, 403)
                response = self.client.post(
                    reverse("characters:retire", kwargs={"pk": character.pk}), follow=True
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.redirect_chain[-1][0], character.get_absolute_url())

"""The Werewolf and Changeling create / edit forms render natively and completely.

Every visible field of the view's form must reach the page (a field the template
leaves out makes the POST fail validation, or blanks the value on save), for the
storyteller's full form and for the owner's limited one, and the page must render
outside the legacy wrapper.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.changeling.autumn_person import AutumnPerson
from characters.models.changeling.cantrip import Cantrip
from characters.models.changeling.changeling import Changeling
from characters.models.changeling.chimera import Chimera
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.changeling.house import House
from characters.models.changeling.house_faction import HouseFaction
from characters.models.changeling.inanimae import Inanimae
from characters.models.changeling.kith import Kith
from characters.models.changeling.legacy import Legacy
from characters.models.changeling.motley import Motley
from characters.models.changeling.nunnehi import Nunnehi
from characters.models.werewolf.battlescar import BattleScar
from characters.models.werewolf.camp import Camp
from characters.models.werewolf.charm import SpiritCharm
from characters.models.werewolf.drone import Drone
from characters.models.werewolf.fera import Fera
from characters.models.werewolf.fomor import Fomor
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.gift import Gift
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.pack import Pack
from characters.models.werewolf.renownincident import RenownIncident
from characters.models.werewolf.rite import Rite
from characters.models.werewolf.septposition import SeptPosition
from characters.models.werewolf.spirit_character import SpiritCharacter
from characters.models.werewolf.totem import Totem
from characters.models.werewolf.tribe import Tribe
from characters.models.werewolf.wtahuman import WtAHuman

LEGACY_MAIN = 'class="tl-content tl-legacy"'


class FormPageMixin:
    def assert_native_and_complete(self, response, skip=()):
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, LEGACY_MAIN)
        self.assertNotContains(response, 'class="row')
        self.assertNotContains(response, "tg-card")
        form = response.context["form"]
        for field in form.visible_fields():
            if field.name in skip:
                continue
            with self.subTest(field=field.name):
                self.assertContains(response, f'name="{field.html_name}"')


class CharacterEditFormTests(FormPageMixin, TestCase):
    """Storyteller (full form) and owner (LimitedHumanEditForm) edit pages."""

    CASES = (
        ("characters:werewolf:update:wta_human_full", WtAHuman, {}),
        ("characters:werewolf:update:werewolf_full", Werewolf, {}),
        ("characters:werewolf:update:kinfolk_full", Kinfolk, {}),
        ("characters:werewolf:update:fomor_full", Fomor, {}),
        ("characters:werewolf:update:drone_full", Drone, {}),
        ("characters:werewolf:update:fera_full", Fera, {}),
        ("characters:changeling:update:ctd_human_full", CtDHuman, {}),
        ("characters:changeling:update:changeling_full", Changeling, {}),
        ("characters:changeling:update:autumn_person", AutumnPerson, {"archetype": "cynic"}),
        (
            "characters:changeling:update:inanimae",
            Inanimae,
            {"kingdom": "kubera", "inanimae_seeming": "naturae", "season": "summer"},
        ),
        (
            "characters:changeling:update:nunnehi",
            Nunnehi,
            {"tribe": "yunwi_tsundi", "nunnehi_seeming": "kohedan", "path": "warrior"},
        ),
    )

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user("owner", password="pw")
        cls.admin = User.objects.create_superuser("admin", "a@example.com", "pw")

    def test_full_and_limited_forms_render_every_field(self):
        for url_name, model, extra in self.CASES:
            character = model.objects.create(
                name=f"{model.__name__} one", owner=self.owner, **extra
            )
            url = reverse(url_name, args=[character.pk])
            for user in (self.admin, self.owner):
                with self.subTest(view=url_name, user=user.username):
                    self.client.force_login(user)
                    response = self.client.get(url)
                    self.assert_native_and_complete(response)
                    self.assertContains(response, 'enctype="multipart/form-data"')

    def test_full_form_shows_trait_sections(self):
        garou = Werewolf.objects.create(name="Wolf", owner=self.owner)
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("characters:werewolf:update:werewolf_full", args=[garou.pk])
        )
        self.assertContains(response, 'id="attributes"')
        self.assertContains(response, 'id="abilities"')
        self.assertContains(response, 'id="renown"')
        self.assertContains(response, 'name="primal_urge"')

        changeling = Changeling.objects.create(name="Fae", owner=self.owner)
        response = self.client.get(
            reverse("characters:changeling:update:changeling_full", args=[changeling.pk])
        )
        self.assertContains(response, 'id="arts-realms"')
        self.assertContains(response, 'name="kenning"')
        self.assertContains(response, 'name="nature_realm"')

    def test_owner_form_keeps_story_fields(self):
        garou = Werewolf.objects.create(name="Wolf", owner=self.owner, notes="Keep me")
        self.client.force_login(self.owner)
        response = self.client.get(
            reverse("characters:werewolf:update:werewolf_full", args=[garou.pk])
        )
        self.assertNotContains(response, 'id="attributes"')
        self.assertContains(response, 'name="public_info"')
        self.assertContains(response, "Keep me")


class ReferenceFormTests(FormPageMixin, TestCase):
    """Create and edit pages of the reference objects and groups."""

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser("admin", "a@example.com", "pw")
        tribe = Tribe.objects.create(name="Uktena")
        cls.objects = {
            "battlescar": BattleScar.objects.create(name="Scar"),
            "camp": Camp.objects.create(name="Camp", tribe=tribe),
            "spirit_charm": SpiritCharm.objects.create(name="Airt Sense"),
            "gift": Gift.objects.create(name="Gift"),
            "rite": Rite.objects.create(name="Rite"),
            "totem": Totem.objects.create(name="Totem"),
            "tribe": tribe,
            "renownincident": RenownIncident.objects.create(name="Deed"),
            "septposition": SeptPosition.objects.create(name="Warder"),
            "pack": Pack.objects.create(name="Pack"),
            "spirit": SpiritCharacter.objects.create(name="Spirit", owner=cls.admin),
            "cantrip": Cantrip.objects.create(name="Cantrip"),
            "chimera": Chimera.objects.create(name="Chimera"),
            "house": House.objects.create(name="House"),
            "house_faction": HouseFaction.objects.create(name="Faction"),
            "kith": Kith.objects.create(name="Kith"),
            "legacy": Legacy.objects.create(name="Legacy"),
            "motley": Motley.objects.create(name="Motley"),
        }

    def setUp(self):
        self.client.force_login(self.admin)

    def test_create_pages(self):
        names = {
            "werewolf": ["battlescar", "camp", "gift", "rite", "totem", "tribe", "pack", "spirit"],
            "changeling": ["cantrip", "chimera", "house", "kith", "legacy", "motley"],
        }
        for line, keys in names.items():
            for key in keys:
                with self.subTest(view=key):
                    response = self.client.get(reverse(f"characters:{line}:create:{key}"))
                    self.assert_native_and_complete(response)

    def test_update_pages(self):
        for key, obj in self.objects.items():
            line = "changeling" if obj._meta.model_name in {
                "cantrip", "chimera", "house", "housefaction", "kith", "legacy", "motley"
            } else "werewolf"  # fmt: skip
            with self.subTest(view=key):
                response = self.client.get(
                    reverse(f"characters:{line}:update:{key}", args=[obj.pk])
                )
                self.assert_native_and_complete(response)

    def test_previously_missing_fields_are_rendered(self):
        """Camp type, the renown incident's rite, a kith's affinity and a legacy's court
        were silently left out of the old templates."""
        checks = (
            ("characters:werewolf:update:camp", "camp", "camp_type"),
            ("characters:werewolf:update:renownincident", "renownincident", "rite"),
            ("characters:changeling:update:kith", "kith", "affinity"),
            ("characters:changeling:update:legacy", "legacy", "court"),
            ("characters:changeling:update:house", "house", "court"),
            ("characters:werewolf:update:pack", "pack", "members"),
        )
        for url_name, key, field in checks:
            with self.subTest(field=field):
                response = self.client.get(reverse(url_name, args=[self.objects[key].pk]))
                self.assertContains(response, f'name="{field}"')

    def test_pack_list_is_native(self):
        response = self.client.get(reverse("characters:werewolf:list:pack"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, LEGACY_MAIN)
        self.assertContains(response, 'class="tl-table"')
        self.assertContains(response, self.objects["pack"].get_absolute_url())


class BasicsFormTests(FormPageMixin, TestCase):
    """The first chargen page (basics) of each Werewolf and Changeling type."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("player", password="pw")

    def test_basics_pages(self):
        pages = (
            "characters:werewolf:create:wta_human",
            "characters:werewolf:create:werewolf",
            "characters:werewolf:create:kinfolk",
            "characters:werewolf:create:fomor",
            "characters:werewolf:create:drone",
            "characters:werewolf:create:fera",
            "characters:changeling:create:ctd_human",
            "characters:changeling:create:changeling",
        )
        self.client.force_login(self.user)
        for url_name in pages:
            with self.subTest(view=url_name):
                response = self.client.get(reverse(url_name))
                storyteller = response.context.get("storyteller")
                skip = () if storyteller else ("npc",)
                if url_name.endswith(":fera"):
                    skip += ("breed",)  # set by the Fera type; FeraCreationForm ignores it
                self.assert_native_and_complete(response, skip=skip)

    def test_drone_basics_renders(self):
        """The drone basics template extended a template that no longer exists."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("characters:werewolf:create:drone"))
        self.assertContains(response, 'name="bane_name"')


class ChargenStepTests(TestCase):
    """The Werewolf and Changeling step templates render every field in Spread markup."""

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user("stepper", password="pw")

    def setUp(self):
        self.client.force_login(self.owner)

    def at(self, model, key, **kwargs):
        from characters.chargen import get_workflow

        workflow = get_workflow(model.type)
        status = next(i for i, step in enumerate(workflow.steps, 1) if step.key == key)
        return model.objects.create(
            name=f"{model.__name__} {key}", owner=self.owner, creation_status=status, **kwargs
        )

    def step(self, character):
        response = self.client.get(reverse("characters:character", args=[character.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'class="row')
        self.assertNotContains(response, "tg-card")
        self.assertNotContains(response, '<form method="post">')  # no nested step form
        for field in response.context["form"].visible_fields():
            with self.subTest(field=field.name):
                self.assertContains(response, f'name="{field.html_name}"')
        return response

    def test_ability_steps_use_the_shared_columns(self):
        from characters.models.werewolf.ratkin import Ratkin

        for model in (WtAHuman, Werewolf, Kinfolk, Fomor, Drone, Ratkin, CtDHuman, Changeling):
            with self.subTest(model=model.__name__):
                response = self.step(self.at(model, "abilities"))
                self.assertContains(response, "data-ability-group", count=3)
                self.assertContains(response, 'id="abilities-validation-status"')

    def test_arts_realms_step(self):
        response = self.step(self.at(Changeling, "arts_realms"))
        self.assertContains(response, 'class="tl-alloc tl-alloc--2"')
        self.assertContains(response, "Dragon's Ire")

    def test_fomor_powers_step(self):
        response = self.step(self.at(Fomor, "powers"))
        self.assertContains(response, "Fomori powers")

    def test_fera_steps(self):
        from characters.models.werewolf.gift import GiftPermission
        from characters.models.werewolf.ratkin import Ratkin

        self.step(self.at(Ratkin, "breed_faction"))
        self.step(self.at(Ratkin, "history"))
        permission = GiftPermission.objects.create(shifter="ratkin", condition="homid")
        Gift.objects.create(name="Scent of Sight", rank=1).allowed.add(permission)
        response = self.step(self.at(Ratkin, "gifts", breed="homid"))
        self.assertContains(response, "Breed Gifts")
        self.assertContains(response, "Scent of Sight")

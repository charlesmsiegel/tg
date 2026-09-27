"""Characterization of chargen game rules at their view boundary.

Written against the pre-Step-4 views and kept green while each rule moved to a
form, service or model method. Tests named ``*_regression`` pin the defects
the Step 4 spec lists as fixed (they failed before the move).
"""

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from characters.chargen import get_workflow
from characters.models.core.ability_block import Ability
from characters.models.core.background_block import Background, BackgroundRating


def position(kind, key):
    workflow = get_workflow(kind)
    return next(i for i, step in enumerate(workflow.steps, 1) if step.key == key)


def formset_data(prefix, rows, initial=0):
    data = {
        f"{prefix}-TOTAL_FORMS": str(len(rows)),
        f"{prefix}-INITIAL_FORMS": str(initial),
        f"{prefix}-MIN_NUM_FORMS": "0",
        f"{prefix}-MAX_NUM_FORMS": "1000",
    }
    for i, row in enumerate(rows):
        for key, value in row.items():
            data[f"{prefix}-{i}-{key}"] = value
    return data


class RuleStepTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(username="rule-step-owner")

    def setUp(self):
        self.client.force_login(self.owner)

    def at(self, kind, model, key, **kwargs):
        return model.objects.create(
            name=f"{kind} {key}", owner=self.owner, creation_status=position(kind, key), **kwargs
        )

    def post(self, character, data):
        return self.client.post(reverse("characters:character", args=[character.pk]), data)

    def flashes(self, response):
        return [str(m) for m in get_messages(response.wsgi_request)]

    def form_errors(self, response):
        form = response.context["form"]
        errors = list(form.non_field_errors()) if hasattr(form, "non_field_errors") else []
        if hasattr(form, "forms"):
            for sub in form.forms:
                errors.extend(sub.non_field_errors())
                for field_errors in sub.errors.values():
                    errors.extend(field_errors)
        else:
            for name, field_errors in form.errors.items():
                if name != "__all__":
                    errors.extend(field_errors)
        return errors

    def assert_stays(self, character, response):
        self.assertEqual(response.status_code, 200)
        before = character.creation_status
        character.refresh_from_db()
        self.assertEqual(character.creation_status, before)


class BackgroundStepTests(RuleStepTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.resources = Background.objects.create(name="Resources", property_name="resources")
        cls.allies = Background.objects.create(name="Allies", property_name="allies")
        cls.pure_breed = Background.objects.create(name="Pure Breed", property_name="pure_breed")
        cls.mentor = Background.objects.create(name="Mentor", property_name="mentor")

    def rows(self, *ratings):
        return formset_data(
            "backgrounds",
            [
                {"bg": bg.pk, "rating": rating, "note": "", "display_alt_name": "", "pooled": ""}
                for bg, rating in ratings
            ],
        )

    def test_human_background_total(self):
        from characters.models.core.human import Human

        human = self.at("human", Human, "backgrounds")
        response = self.post(human, self.rows((self.resources, 3)))
        self.assert_stays(human, response)
        self.assertIn("Backgrounds must total 5 points", self.form_errors(response))
        self.assertFalse(BackgroundRating.objects.filter(char=human).exists())

        response = self.post(human, self.rows((self.resources, 3), (self.allies, 2)))
        self.assertEqual(response.status_code, 302)
        human.refresh_from_db()
        self.assertEqual(human.creation_status, position("human", "backgrounds") + 1)
        self.assertEqual(BackgroundRating.objects.get(char=human, bg=self.resources).rating, 3)

    def kinfolk(self, tribe_name):
        from characters.models.werewolf.kinfolk import Kinfolk
        from characters.models.werewolf.tribe import Tribe

        tribe = Tribe.objects.create(name=tribe_name)
        return self.at("kinfolk", Kinfolk, "backgrounds", tribe=tribe)

    def test_kinfolk_tribe_restrictions(self):
        cases = [
            (
                "Bone Gnawers",
                ((self.pure_breed, 1), (self.allies, 4)),
                "Bone Gnawers may not purchase Pure Breed",
            ),
            (
                "Bone Gnawers",
                ((self.resources, 4), (self.allies, 1)),
                "Bone Gnawers may not purchase more than 3 dots of Resources",
            ),
            (
                "Glass Walkers",
                ((self.mentor, 1), (self.allies, 4)),
                "Glass Walkers may not purchase Mentor",
            ),
            ("Red Talons", ((self.allies, 5),), "Red Talons may not purchase Allies"),
            ("Shadow Lords", ((self.mentor, 5),), "Shadow Lords may not purchase Mentor"),
            (
                "Silent Striders",
                ((self.resources, 5),),
                "Silent Striders may not purchase more than 3 dots of Resources",
            ),
            (
                "Stargazers",
                ((self.resources, 4), (self.allies, 1)),
                "Stargazers may not purchase more than 3 dots of Resources",
            ),
            (
                "Wendigo",
                ((self.resources, 5),),
                "Wendigo may not purchase more than 3 dots of Resources",
            ),
            (
                "Silver Fangs",
                ((self.allies, 5),),
                "Silver Fangs must purchase at least 1 dot of Pure Breed",
            ),
        ]
        for tribe_name, ratings, message in cases:
            with self.subTest(tribe=tribe_name, message=message):
                kinfolk = self.kinfolk(tribe_name)
                response = self.post(kinfolk, self.rows(*ratings))
                self.assert_stays(kinfolk, response)
                self.assertIn(message, self.form_errors(response))
                self.assertFalse(BackgroundRating.objects.filter(char=kinfolk).exists())

    def test_kinfolk_restrictions_precede_total(self):
        kinfolk = self.kinfolk("Red Talons")
        response = self.post(kinfolk, self.rows((self.allies, 1)))
        errors = self.form_errors(response)
        self.assertIn("Red Talons may not purchase Allies", errors)
        self.assertNotIn("Backgrounds must total 5 points", errors)

    def test_kinfolk_allowed_purchase_advances(self):
        kinfolk = self.kinfolk("Silver Fangs")
        response = self.post(kinfolk, self.rows((self.pure_breed, 2), (self.allies, 3)))
        self.assertEqual(response.status_code, 302)
        kinfolk.refresh_from_db()
        self.assertEqual(kinfolk.creation_status, position("kinfolk", "backgrounds") + 1)

    def test_kinfolk_add_background_uses_same_limits(self):
        kinfolk = self.kinfolk("Bone Gnawers")
        self.assertFalse(kinfolk.add_background("pure_breed"))
        kinfolk.resources = 3
        self.assertFalse(kinfolk.add_background("resources"))
        kinfolk.resources = 2
        self.assertTrue(kinfolk.add_background("resources"))


class AttributeAbilityStepTests(RuleStepTestCase):
    ATTRS = {
        "strength": 3,
        "dexterity": 3,
        "stamina": 4,
        "charisma": 2,
        "manipulation": 3,
        "appearance": 3,
        "perception": 2,
        "intelligence": 2,
        "wits": 2,
    }

    def test_attribute_messages(self):
        from characters.models.core.human import Human

        human = self.at("human", Human, "attributes")
        response = self.post(human, {**self.ATTRS, "strength": 4})
        self.assert_stays(human, response)
        self.assertEqual(
            list(response.context["form"].non_field_errors()),
            ["Attributes must be distributed 7/5/3"],
        )
        response = self.post(human, self.ATTRS)
        self.assertEqual(response.status_code, 302)
        human.refresh_from_db()
        self.assertEqual(human.stamina, 4)
        self.assertEqual(human.creation_status, position("human", "attributes") + 1)


class VirtueStepTests(RuleStepTestCase):
    def test_vampire_virtues(self):
        from characters.models.vampire.vampire import Vampire

        vampire = self.at("vampire", Vampire, "virtues")
        data = {"conscience": 3, "self_control": 2, "courage": 3, "conviction": 0, "instinct": 0}
        response = self.post(vampire, {**data, "courage": 1})
        self.assert_stays(vampire, response)
        self.assertEqual(
            list(response.context["form"].non_field_errors()),
            ["Virtues must total 7 dots. Currently: 6"],
        )
        self.assertIn(
            "Virtue allocation error: You must spend exactly 7 dots. You have 6.",
            self.flashes(response),
        )
        response = self.post(vampire, {**data, "conscience": 2, "self_control": 2})
        self.assertEqual(response.status_code, 302)
        vampire.refresh_from_db()
        self.assertEqual((vampire.willpower, vampire.humanity, vampire.path_rating), (3, 4, 0))

    def test_demon_and_thrall_virtue_total(self):
        from characters.models.demon.demon import Demon
        from characters.models.demon.thrall import Thrall

        for kind, model in (("demon", Demon), ("thrall", Thrall)):
            with self.subTest(kind=kind):
                character = self.at(kind, model, "virtues")
                response = self.post(character, {"conviction": 3, "courage": 3, "conscience": 3})
                self.assert_stays(character, response)
                self.assertEqual(
                    list(response.context["form"].non_field_errors()),
                    ["Virtues must total 6 dots. Currently: 9"],
                )
                response = self.post(character, {"conviction": 2, "courage": 3, "conscience": 1})
                self.assertEqual(response.status_code, 302)
                character.refresh_from_db()
                self.assertEqual(character.willpower, 3)

    def test_low_courage_caps_temporary_willpower_regression(self):
        """D1: Demon/Thrall Willpower = Courage keeps temporary <= permanent."""
        from characters.models.demon.demon import Demon
        from characters.models.demon.thrall import Thrall

        for kind, model in (("demon", Demon), ("thrall", Thrall)):
            with self.subTest(kind=kind):
                character = self.at(kind, model, "virtues", willpower=3, temporary_willpower=3)
                response = self.post(character, {"conviction": 3, "courage": 1, "conscience": 2})
                self.assertEqual(response.status_code, 302)
                character.refresh_from_db()
                self.assertEqual((character.willpower, character.temporary_willpower), (1, 1))

    def test_demon_lores(self):
        from characters.models.demon.demon import Demon

        demon = self.at("demon", Demon, "lores")
        from characters.rules.limits import DEMON_LORES

        lores = dict.fromkeys(DEMON_LORES.fields, 0)
        response = self.post(demon, {**lores, "lore_of_flame": 2})
        self.assert_stays(demon, response)
        self.assertEqual(
            list(response.context["form"].non_field_errors()),
            ["You must spend exactly 3 dots on Lores. Currently: 2"],
        )


class MageStepTests(RuleStepTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        from characters.models.mage.focus import Practice, Tenet
        from characters.models.mage.sphere import Sphere

        cls.met = Tenet.objects.create(name="Met", tenet_type="met")
        cls.per = Tenet.objects.create(name="Per", tenet_type="per")
        cls.asc = Tenet.objects.create(name="Asc", tenet_type="asc")
        cls.occult = Ability.objects.create(name="Occult", property_name="occult")
        cls.practice = Practice.objects.create(name="High Ritual Magick")
        cls.practice.abilities.add(cls.occult)
        cls.forces = Sphere.objects.create(name="Forces", property_name="forces")

    def mage(self, key, **kwargs):
        from characters.models.mage.mage import Mage

        return self.at("mage", Mage, key, **kwargs)

    def focus_data(self, rating, **tenets):
        data = {
            "metaphysical_tenet": self.met.pk,
            "personal_tenet": self.per.pk,
            "ascension_tenet": self.asc.pk,
        }
        data.update(tenets)
        data.update(
            formset_data("practicerating_set", [{"practice": self.practice.pk, "rating": rating}])
        )
        return data

    def test_focus_requires_tenets(self):
        mage = self.mage("focus", arete=1, occult=2)
        response = self.post(mage, self.focus_data(1, metaphysical_tenet=""))
        self.assert_stays(mage, response)
        self.assertIn("Must include Metaphysical Tenet", self.form_errors(response))

    def test_focus_practices_sum_to_arete_without_saving_regression(self):
        """D8: a rejected Focus step writes neither tenets nor practices."""
        mage = self.mage("focus", arete=2, occult=4)
        response = self.post(mage, self.focus_data(1))
        self.assert_stays(mage, response)
        self.assertIn("Starting Practices must add up to Arete rating", self.form_errors(response))
        mage.refresh_from_db()
        self.assertIsNone(mage.metaphysical_tenet_id)
        self.assertFalse(mage.practicerating_set.exists())

    def test_focus_practice_needs_two_ability_dots_per_dot(self):
        mage = self.mage("focus", arete=2, occult=3)
        response = self.post(mage, self.focus_data(2))
        self.assert_stays(mage, response)
        self.assertIn(
            "You must have at least 2 dots in associated abilities for each dot of a Practice",
            self.form_errors(response),
        )
        self.assertFalse(mage.practicerating_set.exists())

    def test_focus_success(self):
        mage = self.mage("focus", arete=2, occult=4)
        response = self.post(mage, self.focus_data(2))
        self.assertEqual(response.status_code, 302)
        mage.refresh_from_db()
        self.assertEqual(mage.metaphysical_tenet, self.met)
        self.assertEqual(
            list(mage.practicerating_set.values_list("practice", "rating")),
            [(self.practice.pk, 2)],
        )
        self.assertEqual(mage.creation_status, position("mage", "focus") + 1)

    def spheres_data(self, arete, **extra):
        data = {
            "arete": arete,
            "correspondence": 0,
            "time": 0,
            "spirit": 0,
            "forces": 2,
            "matter": 2,
            "life": 1,
            "entropy": 0,
            "mind": 1,
            "prime": 0,
            "affinity_sphere": self.forces.pk,
            "corr_name": "correspondence",
            "prime_name": "prime",
            "spirit_name": "spirit",
            "resonance": "Dynamic",
        }
        data.update(extra)
        return data

    def test_spheres_buy_arete_with_freebies(self):
        mage = self.mage("spheres", freebies=15)
        response = self.post(mage, self.spheres_data(3))
        self.assertEqual(response.status_code, 302)
        mage.refresh_from_db()
        self.assertEqual(mage.arete, 3)
        self.assertEqual(mage.freebies, 7)
        self.assertEqual(
            [(r["trait"], r["value"], r["cost"]) for r in mage.spent_freebies],
            [("Arete", 2, 4), ("Arete", 3, 4)],
        )
        from characters.models.mage.mage import ResRating

        self.assertEqual(ResRating.objects.get(mage=mage, resonance__name="Dynamic").rating, 1)
        self.assertEqual(mage.creation_status, position("mage", "spheres") + 1)

    def test_spheres_blank_resonance_rejected_regression(self):
        """D14: blank Resonance no longer bypasses validation."""
        mage = self.mage("spheres", freebies=15)
        response = self.post(mage, self.spheres_data(2, resonance=""))
        self.assert_stays(mage, response)
        self.assertIn("resonance", response.context["form"].errors)

    def test_spheres_invalid_total_does_not_advance(self):
        mage = self.mage("spheres", freebies=15)
        response = self.post(mage, self.spheres_data(1))
        self.assert_stays(mage, response)
        mage.refresh_from_db()
        self.assertEqual(mage.freebies, 15)

    def test_rote_step_requires_a_choice(self):
        from characters.models.mage.mage import PracticeRating

        mage = self.mage("rote", arete=1, forces=1)
        PracticeRating.objects.create(mage=mage, practice=self.practice, rating=1)
        response = self.post(mage, {})
        self.assert_stays(mage, response)
        self.assertIn("Must create or select a rote", self.form_errors(response))

    def test_detail_specialties_reject_unrequested_stats_regression(self):
        """D12: detail-page specialties only accept stats that need one."""
        from characters.models.core.attribute_block import Attribute
        from characters.models.core.specialty import Specialty
        from characters.models.mage.mage import Mage

        Attribute.objects.create(name="Strength", property_name="strength")
        admin = get_user_model().objects.create_superuser("rule-admin")
        mage = Mage.objects.create(name="Detail Mage", owner=self.owner, status="App", strength=4)
        self.client.force_login(admin)
        response = self.post(mage, {"specialties": "1", "strength": "Brawny", "wits": "Sneaky"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(mage.specialties.filter(stat="strength", name="Brawny").exists())
        self.assertFalse(Specialty.objects.filter(stat="wits").exists())


class SorcererStepTests(RuleStepTestCase):
    """D10: every numina submission used to raise a 500 (chained-choice strings
    assigned to PathRating foreign keys), so these pin the repaired step."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        from characters.models.mage.sorcerer import LinearMagicPath

        cls.telepathy = LinearMagicPath.objects.create(name="Telepathy", numina_type="psychic")
        cls.alchemy = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")

    def sorcerer(self, key):
        from characters.models.mage.sorcerer import Sorcerer

        return self.at("sorcerer", Sorcerer, key, sorcerer_type="psychic")

    def rows(self, *ratings, path=None):
        return formset_data(
            "numina_form",
            [{"path": (path or self.telepathy).pk, "rating": rating} for rating in ratings],
        )

    def test_psychic_numina_total_regression(self):
        sorcerer = self.sorcerer("psychic")
        response = self.post(sorcerer, self.rows(3))
        self.assert_stays(sorcerer, response)
        self.assertIn("Must choose exactly five levels of Numina", self.form_errors(response))
        self.assertFalse(sorcerer.pathrating_set.exists())

    def test_psychic_numina_success_regression(self):
        sorcerer = self.sorcerer("psychic")
        response = self.post(sorcerer, self.rows(5))
        self.assertEqual(response.status_code, 302)
        sorcerer.refresh_from_db()
        self.assertEqual((sorcerer.willpower, sorcerer.freebies), (5, 21))
        self.assertEqual(sorcerer.path_rating(self.telepathy), 5)
        self.assertGreater(sorcerer.creation_status, position("sorcerer", "psychic"))

    def test_psychic_numina_rejects_bad_input_regression(self):
        """D10: a non-numeric rating or a hedge path is a form error, not a 500."""
        sorcerer = self.sorcerer("psychic")
        response = self.post(sorcerer, self.rows("five"))
        self.assert_stays(sorcerer, response)
        response = self.post(sorcerer, self.rows(5, path=self.alchemy))
        self.assert_stays(sorcerer, response)
        self.assertFalse(sorcerer.pathrating_set.exists())


class FeraStepTests(RuleStepTestCase):
    def test_gifts_need_exactly_three(self):
        from characters.models.werewolf.corax import Corax
        from characters.models.werewolf.gift import Gift, GiftPermission

        corax = self.at("corax", Corax, "gifts")
        permission = GiftPermission.objects.create(shifter="corax", condition="corax")
        corax.gift_permissions.add(permission)
        gifts = [Gift.objects.create(name=f"Gift {i}", rank=1) for i in range(4)]
        for gift in gifts:
            gift.allowed.add(permission)
        response = self.post(corax, {"gifts": [g.pk for g in gifts[:2]]})
        self.assert_stays(corax, response)
        self.assertIn("You must select exactly 3 starting Gifts.", self.form_errors(response))
        response = self.post(corax, {"gifts": [g.pk for g in gifts[:3]]})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(corax.gifts.count(), 3)


class ApocalypticFormStepTests(RuleStepTestCase):
    def test_invalid_selection_keeps_saved_traits_regression(self):
        """D9: a rejected Apocalyptic Form submission changes nothing."""
        from characters.models.demon.apocalyptic_form import (
            ApocalypticForm,
            ApocalypticFormTrait,
        )
        from characters.models.demon.demon import Demon

        demon = self.at("demon", Demon, "apocalyptic_form")
        traits = [ApocalypticFormTrait.objects.create(name=f"T{i}", cost=2) for i in range(8)]
        existing = ApocalypticForm.objects.create(name=f"{demon.name}'s Apocalyptic Form")
        existing.low_torment_traits.add(*traits[:4])
        existing.high_torment_traits.add(*traits[4:])
        data = {f"low_trait_{t.pk}": "on" for t in traits[:3]}
        data.update({f"high_trait_{t.pk}": "on" for t in traits[4:]})
        response = self.post(demon, data)
        self.assert_stays(demon, response)
        self.assertIn(
            "You must select exactly 4 low torment traits. Currently: 3",
            self.form_errors(response),
        )
        self.assertEqual(existing.low_torment_traits.count(), 4)
        self.assertEqual(existing.high_torment_traits.count(), 4)

    def test_valid_selection(self):
        from characters.models.demon.apocalyptic_form import ApocalypticFormTrait
        from characters.models.demon.demon import Demon

        demon = self.at("demon", Demon, "apocalyptic_form")
        traits = [ApocalypticFormTrait.objects.create(name=f"T{i}", cost=2) for i in range(8)]
        data = {f"low_trait_{t.pk}": "on" for t in traits[:4]}
        data.update({f"high_trait_{t.pk}": "on" for t in traits[4:]})
        response = self.post(demon, data)
        self.assertEqual(response.status_code, 302)
        demon.refresh_from_db()
        self.assertEqual(demon.apocalyptic_form.low_torment_traits.count(), 4)
        self.assertEqual(demon.creation_status, position("demon", "apocalyptic_form") + 1)

    def test_budget_and_overlap(self):
        from characters.models.demon.apocalyptic_form import ApocalypticFormTrait
        from characters.models.demon.demon import Demon

        demon = self.at("demon", Demon, "apocalyptic_form")
        traits = [ApocalypticFormTrait.objects.create(name=f"T{i}", cost=3) for i in range(8)]
        data = {f"low_trait_{t.pk}": "on" for t in traits[:4]}
        data.update({f"high_trait_{t.pk}": "on" for t in traits[4:]})
        response = self.post(demon, data)
        self.assertIn(
            "Point budget exceeded. Maximum is 16 points. Currently: 24",
            self.form_errors(response),
        )
        cheap = [ApocalypticFormTrait.objects.create(name=f"C{i}", cost=1) for i in range(4)]
        data = {f"low_trait_{t.pk}": "on" for t in cheap}
        data.update({f"high_trait_{t.pk}": "on" for t in cheap})
        response = self.post(demon, data)
        self.assertIn(
            "A trait cannot be selected as both low and high torment.",
            self.form_errors(response),
        )


class SorcererBasicsTests(RuleStepTestCase):
    def test_casting_attribute_must_be_favoured_by_the_fellowship_regression(self):
        """D11: basics no longer accept an attribute or path outside the fellowship."""
        from characters.models.core.archetype import Archetype
        from characters.models.core.attribute_block import Attribute
        from characters.models.mage.fellowship import SorcererFellowship
        from characters.models.mage.sorcerer import LinearMagicPath, Sorcerer

        archetype = Archetype.objects.create(name="Survivor")
        wits = Attribute.objects.create(name="Wits", property_name="wits")
        strength = Attribute.objects.create(name="Strength", property_name="strength")
        path = LinearMagicPath.objects.create(name="Alchemy")
        fellowship = SorcererFellowship.objects.create(name="Circle")
        fellowship.favored_attributes.add(wits)
        fellowship.favored_paths.add(path)
        data = {
            "name": "Hedge",
            "nature": archetype.pk,
            "demeanor": archetype.pk,
            "concept": "Witch",
            "fellowship": fellowship.pk,
            "affinity_path": path.pk,
            "casting_attribute": strength.pk,
            "sorcerer_type": "hedge_mage",
        }
        url = reverse("characters:mage:create:sorcerer")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("casting_attribute", response.context["form"].errors)
        self.assertFalse(Sorcerer.objects.filter(name="Hedge").exists())

        response = self.client.post(url, {**data, "casting_attribute": wits.pk})
        self.assertEqual(response.status_code, 302)
        sorcerer = Sorcerer.objects.get(name="Hedge")
        self.assertEqual((sorcerer.casting_attribute, sorcerer.affinity_path), (wits, path))
        self.assertEqual(sorcerer.owner, self.owner)


class CompanionBudgetTests(RuleStepTestCase):
    def test_budget_by_type_preserves_d2(self):
        """Budgets keep the original keys; plain companions get none (defect D2)."""
        from characters.models.mage.companion import Companion

        cases = (("consor", 7, 21), ("companion", 7, 7))
        for companion_type, before, after in cases:
            with self.subTest(companion_type=companion_type):
                companion = Companion.objects.create(
                    name=companion_type,
                    owner=self.owner,
                    companion_type=companion_type,
                    freebies=before,
                )
                companion.prepare_starting_freebies()
                self.assertEqual(companion.freebies, after)
                self.assertEqual(companion.spent_freebies, [])


FERA_BREED_STEP = {
    # kind: (fields, {field: help text} beyond breed, gift context keys given all choices)
    "ratkin": (
        ["breed", "aspect"],
        {"aspect": "Choose your aspect (similar to auspice for Garou)."},
        {"breed_gifts", "aspect_gifts"},
    ),
    "mokole": (
        ["breed", "stream", "auspice"],
        {
            "stream": "Choose your stream (cultural/regional grouping).",
            "auspice": "Choose your auspice (based on sun position at birth).",
        },
        {"breed_gifts", "stream_gifts", "auspice_gifts"},
    ),
    "bastet": (
        ["breed", "tribe", "pryio"],
        {
            "tribe": "Choose your tribe (cat species).",
            "pryio": "Choose your Pryio (moon-based role).",
        },
        {"breed_gifts", "tribe_gifts", "pryio_gifts"},
    ),
    "corax": (["breed"], {}, {"breed_gifts", "corax_gifts"}),
    "nuwisha": (
        ["breed", "role"],
        {"role": "Choose your role (optional, loose affiliation)."},
        {"breed_gifts", "nuwisha_gifts", "role_gifts"},
    ),
    "gurahl": (
        ["breed", "auspice"],
        {"auspice": "Choose your auspice (seasonal role)."},
        {"breed_gifts", "auspice_gifts"},
    ),
    "ananasi": (
        ["breed", "aspect"],
        {"aspect": "Choose your aspect (role among the Ananasi)."},
        {"breed_gifts", "aspect_gifts"},
    ),
    "rokea": (
        ["breed", "auspice"],
        {"auspice": "Choose your auspice (time of birth)."},
        {"breed_gifts", "auspice_gifts"},
    ),
    "kitsune": (
        ["breed", "path"],
        {"path": "Choose your path (role in society)."},
        {"breed_gifts", "path_gifts"},
    ),
    "nagah": (
        ["breed", "auspice"],
        {"auspice": "Choose your auspice (role as assassin)."},
        {"breed_gifts", "auspice_gifts"},
    ),
    "ajaba": (
        ["breed", "auspice"],
        {"auspice": "Choose your auspice (lunar cycle)."},
        {"breed_gifts", "auspice_gifts"},
    ),
    "grondr": (
        ["breed", "auspice"],
        {"auspice": "Choose your auspice (seasonal role)."},
        {"breed_gifts", "auspice_gifts"},
    ),
}


class FeraDispatchTests(RuleStepTestCase):
    """Each Changing Breed renders the fields, help text and gift lists it always did."""

    def fera_model(self, kind):
        from django.apps import apps

        return apps.get_model("characters", kind)

    def test_breed_faction_step_per_type(self):
        for kind, (fields, help_text, _) in FERA_BREED_STEP.items():
            with self.subTest(kind=kind):
                fera = self.at(kind, self.fera_model(kind), "breed_faction")
                response = self.client.get(reverse("characters:character", args=[fera.pk]))
                self.assertEqual(response.status_code, 200)
                form = response.context["form"]
                self.assertEqual(list(form.fields), fields)
                self.assertEqual(form.fields["breed"].help_text, "Choose your breed (birth form).")
                for field, text in help_text.items():
                    self.assertEqual(form.fields[field].help_text, text)
                self.assertEqual(response.context["fera_type"], type(fera).__name__)
                if kind == "nuwisha":
                    self.assertFalse(form.fields["role"].required)

    def test_breed_choice_runs_the_setters(self):
        from characters.models.werewolf.gift import GiftPermission

        fera = self.at("ratkin", self.fera_model("ratkin"), "breed_faction")
        response = self.post(fera, {"breed": "homid", "aspect": "warrior"})
        self.assertEqual(response.status_code, 302)
        fera.refresh_from_db()
        self.assertEqual(
            (fera.breed, fera.aspect, fera.gnosis, fera.rage), ("homid", "warrior", 1, 4)
        )
        self.assertTrue(
            fera.gift_permissions.filter(
                pk=GiftPermission.objects.get(shifter="ratkin", condition="warrior").pk
            ).exists()
        )

    def test_gift_groups_per_type(self):
        from characters.models.werewolf.gift import Gift, GiftPermission

        for kind, (fields, _, keys) in FERA_BREED_STEP.items():
            with self.subTest(kind=kind):
                model = self.fera_model(kind)
                values = {
                    field: (model._meta.get_field(field).choices or [(f"{kind}-{field}",)])[0][0]
                    for field in fields
                }
                fera = self.at(kind, model, "gifts", **values)
                conditions = list(values.values()) + [kind]
                for condition in conditions:
                    permission = GiftPermission.objects.create(shifter=kind, condition=condition)
                    Gift.objects.create(name=f"{kind} {condition}", rank=1).allowed.add(permission)
                response = self.client.get(reverse("characters:character", args=[fera.pk]))
                self.assertEqual(response.status_code, 200)
                present = {key for key in response.context.keys() if key.endswith("_gifts")}
                self.assertEqual(present, keys)

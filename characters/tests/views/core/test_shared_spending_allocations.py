"""Characterization and regressions for shared spending/allocation lifecycles."""

from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.cache import cache
from django.http import Http404
from django.test import RequestFactory, TestCase

from characters.chargen import get_workflow
from characters.forms.mage.freebies import CompanionFreebiesForm, SorcererFreebiesForm
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.mage.companion import Advantage, Companion
from characters.models.mage.focus import Practice
from characters.models.mage.sorcerer import LinearMagicPath, LinearMagicRitual, Sorcerer
from characters.models.wraith.fetter import Fetter
from characters.models.wraith.passion import Passion
from characters.models.wraith.wraith import Wraith
from characters.views.mage.companion import CompanionFreebiesView
from characters.views.mage.sorcerer import SorcererFreebiesView
from characters.views.wraith.wraith_chargen import WraithFettersView, WraithPassionsView
from game.models import FreebieSpendingRecord


class SpendingAllocationCase(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.owner = User.objects.create_user(username="allocator")
        self.factory = RequestFactory()

    def character(self, model, step, **kwargs):
        workflow = get_workflow(model.type)
        position = next(i for i, item in enumerate(workflow.steps, 1) if item.key == step)
        return model.objects.create(
            name="Allocation subject",
            owner=self.owner,
            creation_status=position,
            freebies_approved=True,
            **kwargs,
        )

    def request(self, view, character, data=None, user=None):
        request = self.factory.get("/") if data is None else self.factory.post("/", data)
        request.user = user or self.owner
        request.session = {}
        request._messages = FallbackStorage(request)
        return view.as_view()(request, pk=character.pk), request


class SpendingCharacterizationTests(SpendingAllocationCase):
    def test_actual_chained_categories_and_background_prefixes(self):
        bg = Background.objects.create(name="Resources", property_name="resources")
        for model, form_type in (
            (Companion, CompanionFreebiesForm),
            (Sorcerer, SorcererFreebiesForm),
        ):
            with self.subTest(model=model.type):
                char = self.character(model, "freebies", freebies=20)
                form = form_type(instance=char)
                categories = dict(form.fields["category"].choices)
                self.assertIn("Background", categories)
                self.assertNotIn("New Background", categories)
                self.assertIn(
                    (f"bg_{bg.pk}", str(bg)), form.fields["example"].choices_map["Background"]
                )
                if model is Sorcerer:
                    self.assertIn("New Path", categories)
                    self.assertIn("Existing Path", categories)
                    self.assertNotIn("Path", categories)

    def test_companion_willpower_price_and_familiar_essence(self):
        char = self.character(
            Companion, "freebies", freebies=10, willpower=3, companion_type="familiar"
        )
        response, _ = self.request(CompanionFreebiesView, char, {"category": "Willpower"})
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual((char.freebies, char.willpower, char.essence), (8, 4, 20))


class WraithAllocationCharacterizationTests(SpendingAllocationCase):
    cases = (
        (
            "passions",
            WraithPassionsView,
            Passion,
            "passion",
            {"emotion": "Love", "is_dark_passion": "on"},
        ),
        ("fetters", WraithFettersView, Fetter, "fetter", {"fetter_type": "object"}),
    )

    def test_get_context_is_read_only_and_partial_then_complete_post(self):
        for step, view, record, noun, extra in self.cases:
            with self.subTest(step=step):
                char = self.character(Wraith, step)
                initial = char.creation_status
                response, _ = self.request(view, char)
                self.assertEqual(response.context_data[f"{noun}_points_remaining"], 10)
                char.refresh_from_db()
                self.assertEqual(char.creation_status, initial)
                response, request = self.request(
                    view, char, dict(extra, rating=2, description="Anchor")
                )
                self.assertEqual(response.status_code, 302)
                char.refresh_from_db()
                self.assertEqual(char.creation_status, initial)
                self.assertEqual(
                    str(list(request._messages)[0]),
                    f"{noun.title()} added successfully! 8 points remaining.",
                )
                saved = record.objects.get(wraith=char)
                if noun == "passion":
                    self.assertTrue(saved.is_dark_passion)
                response, request = self.request(
                    view, char, dict(extra, rating=8, description="Second anchor")
                )
                char.refresh_from_db()
                self.assertEqual(char.creation_status, initial + 1)
                self.assertEqual(
                    str(list(request._messages)[0]), f"All {step.title()} allocated successfully!"
                )

    def test_over_budget_and_invalid_rating_leave_records_and_position_unchanged(self):
        for step, view, record, noun, extra in self.cases:
            for rating in (0, 4, 11):
                with self.subTest(step=step, rating=rating):
                    char = self.character(Wraith, step)
                    getattr(char, f"add_{noun}")(
                        **dict(
                            {k: v for k, v in extra.items() if k != "is_dark_passion"},
                            rating=8,
                            description="Existing",
                        )
                    )
                    initial = char.creation_status
                    response, _ = self.request(
                        view, char, dict(extra, rating=rating, description="Anchor")
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertIn("rating", response.context_data["form"].errors)
                    self.assertEqual(record.objects.filter(wraith=char).count(), 1)
                    char.refresh_from_db()
                    self.assertEqual(char.creation_status, initial)

    def test_unauthorized_post_cannot_skip_complete_allocation(self):
        stranger = User.objects.create_user(username="stranger")
        for step, view, record, noun, extra in self.cases:
            char = self.character(Wraith, step)
            getattr(char, f"add_{noun}")(
                **dict(
                    {k: v for k, v in extra.items() if k != "is_dark_passion"},
                    rating=10,
                    description="Existing",
                )
            )
            initial = char.creation_status
            with self.assertRaises(Http404):
                self.request(view, char, dict(extra, rating=1, description="Anchor"), user=stranger)
            char.refresh_from_db()
            self.assertEqual(char.creation_status, initial)
            self.assertEqual(record.objects.filter(wraith=char).count(), 1)


class SharedSpendingRegressionTests(SpendingAllocationCase):
    def test_advantage_purchase_cannot_refund_or_repeat_an_existing_rating(self):
        advantage = Advantage.objects.create(name="Ferocity")
        advantage.add_ratings([1, 4])
        for value in (1, 4):
            with self.subTest(value=value):
                char = self.character(Companion, "freebies", freebies=20, rage=2)
                char.add_advantage(advantage, 4)
                position = char.creation_status
                response, _ = self.request(
                    CompanionFreebiesView,
                    char,
                    {"category": "Advantage", "example": advantage.pk, "value": value},
                )
                self.assertEqual(response.status_code, 200)
                char.refresh_from_db()
                self.assertEqual(
                    (char.freebies, char.rage, char.creation_status), (20, 2, position)
                )
                self.assertEqual(char.advantage_rating(advantage), 4)
                self.assertFalse(FreebieSpendingRecord.objects.filter(character=char).exists())

    def test_unsupported_advantage_rating_never_charges_or_records_spending(self):
        advantage = Advantage.objects.create(name="Ferocity")
        advantage.add_rating(4)
        char = self.character(Companion, "freebies", freebies=20)
        response, _ = self.request(
            CompanionFreebiesView,
            char,
            {"category": "Advantage", "example": advantage.pk, "value": 3},
        )
        self.assertEqual(response.status_code, 200)
        char.refresh_from_db()
        self.assertEqual((char.freebies, char.rage, char.advantage_rating(advantage)), (20, 0, 0))
        self.assertFalse(FreebieSpendingRecord.objects.filter(character=char).exists())

    def test_every_registered_freebie_adapter_spends_a_common_attribute(self):
        from characters.chargen.definitions import WORKFLOWS

        attribute = Attribute.objects.create(name="Strength", property_name="strength")
        for character_type, workflow in WORKFLOWS.items():
            with self.subTest(character_type=character_type):
                view = workflow.step(workflow.freebie_step).view
                char = self.character(view.model, "freebies", freebies=10)
                response, _ = self.request(
                    view, char, {"category": "Attribute", "example": attribute.pk}
                )
                self.assertEqual(response.status_code, 302)
                char.refresh_from_db()
                self.assertEqual((char.freebies, char.strength), (5, 2))
                self.assertEqual(FreebieSpendingRecord.objects.filter(character=char).count(), 1)

    def test_changeling_chained_art_and_realm_choices(self):
        from characters.models.changeling.changeling import Changeling
        from characters.models.core.statistic import Statistic
        from characters.views.changeling.changeling import ChangelingFreebiesView

        char = self.character(Changeling, "freebies", freebies=20)
        for category, property_name, price in (("Art", "chicanery", 5), ("Realm", "actor", 2)):
            trait = Statistic.objects.create(
                name=property_name.title(), property_name=property_name
            )
            before = char.freebies
            response, _ = self.request(
                ChangelingFreebiesView, char, {"category": category, "example": trait.pk}
            )
            self.assertEqual(response.status_code, 302)
            char.refresh_from_db()
            self.assertEqual(getattr(char, property_name), 1)
            self.assertEqual(char.freebies, before - price)

    def test_mage_chained_sphere_choice(self):
        from characters.models.mage.mage import Mage
        from characters.models.mage.sphere import Sphere
        from characters.views.mage.mage import MageFreebiesView

        char = self.character(Mage, "freebies", freebies=20, arete=2)
        sphere = Sphere.objects.create(name="Matter", property_name="matter")
        response, _ = self.request(
            MageFreebiesView, char, {"category": "Sphere", "example": sphere.pk}
        )
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual((char.matter, char.freebies), (1, 13))

    def test_mage_arete_level_choice_is_not_treated_as_a_practice(self):
        from characters.models.mage.mage import Mage
        from characters.views.mage.mage import MageFreebiesView

        char = self.character(Mage, "freebies", freebies=10, arete=1)
        response, _ = self.request(MageFreebiesView, char, {"category": "Arete", "example": "2"})
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual((char.arete, char.freebies), (2, 6))
        record = FreebieSpendingRecord.objects.get(character=char)
        self.assertEqual((record.trait_name, record.trait_type, record.cost), ("Arete", "arete", 4))

    def test_mage_rotes_and_resonance_form_values_reach_service(self):
        from characters.models.mage.mage import Mage
        from characters.models.mage.resonance import Resonance
        from characters.views.mage.mage import MageFreebiesView

        char = self.character(Mage, "freebies", freebies=20, arete=2, rote_points=0)
        response, _ = self.request(MageFreebiesView, char, {"category": "Rotes"})
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual((char.rote_points, char.freebies), (4, 19))
        response, _ = self.request(
            MageFreebiesView, char, {"category": "Resonance", "resonance": "Calm"}
        )
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual(char.freebies, 16)
        self.assertEqual(char.resonance_rating(Resonance.objects.get(name="Calm")), 1)

    def test_missing_companion_advantage_value_renders_validation_error(self):
        advantage = Advantage.objects.create(name="Ferocity")
        advantage.add_rating(1)
        char = self.character(Companion, "freebies", freebies=20)
        response, _ = self.request(
            CompanionFreebiesView, char, {"category": "Advantage", "example": advantage.pk}
        )
        self.assertEqual(response.status_code, 200)
        char.refresh_from_db()
        self.assertEqual(char.freebies, 20)

    def test_vampire_chained_discipline_and_string_virtue(self):
        from characters.models.vampire.clan import VampireClan
        from characters.models.vampire.discipline import Discipline
        from characters.models.vampire.vampire import Vampire
        from characters.views.vampire.vampire_chargen import VampireFreebiesView

        discipline = Discipline.objects.create(name="Potence", property_name="potence")
        clan = VampireClan.objects.create(name="Brujah")
        clan.disciplines.add(discipline)
        char = self.character(Vampire, "freebies", freebies=20, clan=clan)
        response, _ = self.request(
            VampireFreebiesView, char, {"category": "Discipline", "example": discipline.pk}
        )
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual((char.potence, char.freebies), (1, 13))
        before = char.courage
        response, _ = self.request(
            VampireFreebiesView, char, {"category": "Virtue", "example": "courage"}
        )
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual((char.courage, char.freebies), (before + 1, 11))

    def test_invalid_chained_choice_does_not_spend_or_raise(self):
        for model, view in ((Companion, CompanionFreebiesView), (Sorcerer, SorcererFreebiesView)):
            with self.subTest(model=model.type):
                char = self.character(model, "freebies", freebies=15)
                response, _ = self.request(
                    view, char, {"category": "Attribute", "example": "missing"}
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn("example", response.context_data["form"].errors)
                char.refresh_from_db()
                self.assertEqual(char.freebies, 15)
                self.assertFalse(FreebieSpendingRecord.objects.filter(character=char).exists())

    def test_chained_attribute_resolves_to_model_and_final_spend_advances_once(self):
        attribute = Attribute.objects.create(name="Strength", property_name="strength")
        for model, view in ((Companion, CompanionFreebiesView), (Sorcerer, SorcererFreebiesView)):
            with self.subTest(model=model.type):
                char = self.character(model, "freebies", freebies=5)
                from characters.chargen.transitions import advance

                with patch(f"{view.form_valid.__module__}.advance", wraps=advance) as advance_spy:
                    response, _ = self.request(
                        view, char, {"category": "Attribute", "example": attribute.pk}
                    )
                self.assertEqual(response.status_code, 302)
                self.assertEqual(advance_spy.call_count, 1)
                char.refresh_from_db()
                self.assertEqual((char.freebies, char.strength), (0, 2))

    def test_background_prefix_and_multiplier_are_preserved(self):
        bg = Background.objects.create(name="Resources", property_name="resources", multiplier=3)
        for model, view in ((Companion, CompanionFreebiesView), (Sorcerer, SorcererFreebiesView)):
            with self.subTest(model=model.type):
                char = self.character(model, "freebies", freebies=10)
                response, _ = self.request(
                    view,
                    char,
                    {"category": "Background", "example": f"bg_{bg.pk}", "note": "Trust"},
                )
                self.assertEqual(response.status_code, 302)
                char.refresh_from_db()
                self.assertEqual(char.freebies, 7)
                self.assertEqual(BackgroundRating.objects.get(char=char, bg=bg).note, "Trust")

    def test_ferocity_derived_rage_is_preserved(self):
        advantage = Advantage.objects.create(name="Ferocity")
        advantage.add_rating(4)
        char = self.character(
            Companion, "freebies", freebies=20, companion_type="familiar", willpower=3
        )
        response, _ = self.request(
            CompanionFreebiesView,
            char,
            {"category": "Advantage", "example": advantage.pk, "value": "4"},
        )
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual((char.rage, char.essence, char.advantage_rating(advantage)), (2, 15, 4))

    def test_final_point_stops_at_incomplete_linked_background(self):
        bg = Background.objects.create(name="Library", property_name="library")
        for model, view, price in (
            (Companion, CompanionFreebiesView, 2),
            (Sorcerer, SorcererFreebiesView, 1),
        ):
            with self.subTest(model=model.type):
                char = self.character(model, "freebies", freebies=price, willpower=3)
                BackgroundRating.objects.create(char=char, bg=bg, rating=1, complete=False)
                response, _ = self.request(view, char, {"category": "Willpower"})
                self.assertEqual(response.status_code, 302)
                char.refresh_from_db()
                self.assertEqual(get_workflow(char.type).step(char.creation_status).key, "library")
                self.assertTrue(char.languages.filter(name="English").exists())

    def test_sorcerer_new_and_existing_path_use_validated_practice_and_ability(self):
        ability = Ability.objects.create(name="Occult", property_name="occult")
        practice = Practice.objects.create(name="Alchemy")
        practice.abilities.add(ability)
        path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        char = self.character(Sorcerer, "freebies", freebies=20, sorcerer_type="hedge_mage")
        response, _ = self.request(
            SorcererFreebiesView,
            char,
            {
                "category": "New Path",
                "example": path.pk,
                "practice": practice.pk,
                "ability": ability.pk,
            },
        )
        self.assertEqual(response.status_code, 302)
        rating = char.pathrating_set.get(path=path)
        self.assertEqual((rating.rating, rating.practice, rating.ability), (1, practice, ability))
        response, _ = self.request(
            SorcererFreebiesView, char, {"category": "Existing Path", "example": path.pk}
        )
        self.assertEqual(response.status_code, 302)
        rating.refresh_from_db()
        char.refresh_from_db()
        self.assertEqual((rating.rating, char.freebies), (2, 6))

    def test_sorcerer_select_ritual_resolves_choice(self):
        path = LinearMagicPath.objects.create(name="Alchemy")
        char = self.character(Sorcerer, "freebies", freebies=10, sorcerer_type="hedge_mage")
        char.add_path(path, None, None)
        ritual = LinearMagicRitual.objects.create(name="Elixir", path=path, level=1)
        response, _ = self.request(
            SorcererFreebiesView, char, {"category": "Select Ritual", "example": ritual.pk}
        )
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual(char.freebies, 7)
        self.assertTrue(char.rituals.filter(pk=ritual.pk).exists())

    def test_service_rejection_does_not_change_companion_derived_stats(self):
        char = self.character(
            Companion, "freebies", freebies=1, willpower=3, companion_type="familiar", essence=15
        )
        response, _ = self.request(CompanionFreebiesView, char, {"category": "Willpower"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Not enough freebies", str(response.context_data["form"].errors))
        char.refresh_from_db()
        self.assertEqual((char.freebies, char.willpower, char.essence), (1, 3, 15))

    def test_existing_background_price_and_other_characters_choice_rejected(self):
        from characters.models.mage.mtahuman import MtAHuman
        from characters.views.mage.mtahuman import MtAHumanFreebiesView

        bg = Background.objects.create(name="Resources", property_name="resources", multiplier=3)
        char = self.character(MtAHuman, "freebies", freebies=10)
        rating = BackgroundRating.objects.create(char=char, bg=bg, rating=1)
        response, _ = self.request(
            MtAHumanFreebiesView, char, {"category": "Background", "example": f"br_{rating.pk}"}
        )
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        rating.refresh_from_db()
        self.assertEqual((char.freebies, rating.rating), (7, 2))
        other = self.character(MtAHuman, "freebies", freebies=10)
        response, _ = self.request(
            MtAHumanFreebiesView, other, {"category": "Background", "example": f"br_{rating.pk}"}
        )
        self.assertEqual(response.status_code, 200)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 2)

    def test_ritual_creation_validates_extra_form_before_spending(self):
        path = LinearMagicPath.objects.create(name="Alchemy")
        char = self.character(Sorcerer, "freebies", freebies=10, sorcerer_type="hedge_mage")
        char.add_path(path, None, None)
        data = {
            "category": "Create Ritual",
            "name": "Elixir",
            "path": path.pk,
            "level": "invalid",
            "description": "A potion",
        }
        response, _ = self.request(SorcererFreebiesView, char, data)
        self.assertEqual(response.status_code, 200)
        char.refresh_from_db()
        self.assertEqual(char.freebies, 10)
        self.assertFalse(LinearMagicRitual.objects.exists())
        data["level"] = 1
        response, _ = self.request(SorcererFreebiesView, char, data)
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual(char.freebies, 7)
        self.assertEqual(char.rituals.get().name, "Elixir")

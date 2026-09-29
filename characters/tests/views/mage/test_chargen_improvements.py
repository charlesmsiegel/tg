"""Player-facing Mage creation rules and controls."""

import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.forms.mage.chained_freebies import ChainedMageFreebiesForm
from characters.forms.mage.mage import MageSpheresForm
from characters.forms.mage.practiceform import PracticeRatingFormSet
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Practice
from characters.models.mage.mage import Mage
from characters.models.mage.sphere import Sphere


class MageCreationControlsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("mage_creator")
        self.client.force_login(self.user)

    def wizard(self, mage):
        return self.client.get(reverse("characters:character", kwargs={"pk": mage.pk}))

    def test_attribute_and_ability_priority_is_inferred_from_dots(self):
        for step in (1, 2):
            with self.subTest(step=step):
                mage = Mage.objects.create(name=f"Mage {step}", owner=self.user, creation_status=step)
                response = self.wizard(mage)
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, 'data-priority-picker')
                self.assertContains(response, 'data-priority-group')

    def test_sphere_step_uses_dots_and_shows_budget(self):
        mage = Mage.objects.create(name="Sphere Mage", owner=self.user, creation_status=4)
        response = self.wizard(mage)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-sphere-budget')
        self.assertContains(response, 'data-dot-rating')
        self.assertContains(response, 'name="resonance"')

    def test_sphere_names_replace_the_labels_beside_their_dots(self):
        mage = Mage.objects.create(name="Named Sphere Mage", owner=self.user, creation_status=4)
        response = self.wizard(mage)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        for field in ("corr_name", "prime_name", "spirit_name"):
            with self.subTest(field=field):
                self.assertRegex(
                    html,
                    rf'<div class="tl-alloc__row[^>]*>\s*<label class="tl-sr"[^>]*>[^<]+</label>\s*<select[^>]*name="{field}"',
                )

    def test_returning_to_spheres_keeps_saved_arete(self):
        mage = Mage.objects.create(name="Returning Mage", owner=self.user, creation_status=4, arete=3)
        response = self.wizard(mage)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"]["arete"].value(), 3)

    def test_rote_balance_is_visible_before_either_creation_mode(self):
        mage = Mage.objects.create(
            name="Rote Mage", owner=self.user, creation_status=9, rote_points=5, arete=2, forces=2
        )
        effect = Effect.objects.create(name="Spark", owner=self.user, forces=2)
        response = self.wizard(mage)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn('data-rote-budget', html)
        self.assertLess(html.index('data-rote-budget'), html.index('data-create-or-select-container'))
        self.assertContains(response, 'Rote points remaining')
        self.assertContains(response, 'data-available="5"')
        self.assertEqual(json.loads(response.context["effect_costs_json"])[str(effect.pk)], 2)

    def test_allies_shows_character_type_specific_fields(self):
        mage = Mage.objects.create(name="Allied Mage", owner=self.user, creation_status=16)
        allies = Background.objects.create(name="Allies", property_name="allies")
        BackgroundRating.objects.create(char=mage, bg=allies, rating=2)
        response = self.wizard(mage)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["step"].key, "allies")
        self.assertContains(response, 'data-linked-npc-form')
        self.assertContains(response, 'data-npc-types="vampire"')
        self.assertContains(response, 'name="clan"')
        self.assertContains(response, 'name="sect"')
        self.assertContains(response, 'tl-linked-npc__section')
        self.assertContains(response, 'Who are they?')
        self.assertContains(response, 'Their connection to you')
        self.assertRegex(response.content.decode(), r'<select name="clan"[^>]*>')
        self.assertRegex(response.content.decode(), r'<select name="sect"[^>]*>')
        self.assertNotContains(response, 'For Vampires only')
        self.assertNotContains(response, 'if Vampire')
        self.assertContains(response, 'linked-npc-fields.js')

    def test_freebie_category_populates_attribute_and_only_relevant_fields_show(self):
        Attribute.objects.create(name="Strength", property_name="strength")
        mage = Mage.objects.create(
            name="Freebie Mage", owner=self.user, creation_status=7, freebies_approved=True
        )
        form = ChainedMageFreebiesForm(instance=mage)
        tree = form.fields["category"].widget.choices_tree
        self.assertIn("category:Attribute", tree)
        self.assertTrue(tree["category:Attribute"])
        response = self.wizard(mage)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="example_wrap"')
        self.assertContains(response, 'id="resonance_wrap"')
        self.assertContains(response, "widgets/chained.js")
        self.assertContains(response, "widgets/conditional.js")

    def test_biography_ages_are_bounded_whole_number_controls(self):
        mage = Mage.objects.create(name="Biographical Mage", owner=self.user, creation_status=6)
        response = self.wizard(mage)
        self.assertEqual(response.status_code, 200)
        for name in ("age", "apparent_age", "age_of_awakening"):
            with self.subTest(name=name):
                field = response.context["form"].fields[name]
                self.assertEqual(field.min_value, 0)
                self.assertEqual(field.max_value, 65535)
                self.assertIn(f'name="{name}"', response.content.decode())

        Mage.objects.filter(pk=mage.pk).update(
            age=50000, apparent_age=50000, age_of_awakening=50000
        )
        mage.refresh_from_db()
        self.assertEqual((mage.age, mage.apparent_age, mage.age_of_awakening), (50000,) * 3)


class MageSphereRulesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("mage_creator")
        self.faction = MageFaction.objects.create(name="Example Faction")
        self.preferred = Sphere.objects.create(name="Forces", property_name="forces")
        self.other = Sphere.objects.create(name="Mind", property_name="mind")
        self.faction.affinities.add(self.preferred)
        self.mage = Mage.objects.create(name="Mage", owner=self.user, faction=self.faction)

    def data(self, *, arete=3, affinity=None, resonance="Dynamic"):
        return {
            "arete": arete,
            "forces": 3,
            "mind": 3,
            "correspondence": 0,
            "time": 0,
            "spirit": 0,
            "matter": 0,
            "life": 0,
            "entropy": 0,
            "prime": 0,
            "affinity_sphere": affinity or self.other.pk,
            "resonance": resonance,
            "corr_name": "correspondence",
            "prime_name": "prime",
            "spirit_name": "spirit",
        }

    def test_non_preferred_sphere_is_valid_affinity(self):
        form = MageSpheresForm(data=self.data(), instance=self.mage)
        self.assertTrue(form.is_valid(), form.errors)

    def test_sphere_step_offers_all_affinities_and_marks_preferred_one(self):
        self.mage.creation_status = 4
        self.mage.save(update_fields=["creation_status"])
        self.client.force_login(self.user)
        response = self.client.get(reverse("characters:character", kwargs={"pk": self.mage.pk}))
        choices = list(response.context["form"].fields["affinity_sphere"].choices)
        self.assertIn((self.other.pk, "Mind"), choices)
        self.assertIn((self.preferred.pk, "Forces (preferred)"), choices)
        sphere_map = json.loads(
            response.context["form"].fields["affinity_sphere"].widget.attrs["data-sphere-map"]
        )
        self.assertEqual(sphere_map[str(self.other.pk)], "mind")
        self.assertEqual(sphere_map[str(self.preferred.pk)], "forces")

    def test_resonance_is_required_and_non_npc_arete_is_capped(self):
        self.assertIn("resonance", MageSpheresForm(data=self.data(resonance=""), instance=self.mage).errors)
        self.assertIn("arete", MageSpheresForm(data=self.data(arete=4), instance=self.mage).errors)
        self.mage.npc = True
        self.assertTrue(MageSpheresForm(data=self.data(arete=4), instance=self.mage).is_valid())


class MagePracticeControlsTests(TestCase):
    def test_only_eligible_practices_are_offered_with_ability_limited_dots(self):
        user = User.objects.create_user("practice_mage")
        mage = Mage.objects.create(name="Practice Mage", owner=user, arete=3, athletics=2)
        athletics = Ability.objects.create(name="Athletics", property_name="athletics")
        eligible = Practice.objects.create(name="Movement")
        eligible.abilities.add(athletics)
        ineligible = Practice.objects.create(name="Stillness")
        formset = PracticeRatingFormSet(instance=mage, mage=mage)
        options = list(formset.forms[0].fields["practice"].queryset)
        self.assertIn(eligible, options)
        self.assertNotIn(ineligible, options)
        self.assertEqual(formset.forms[0].fields["rating"].widget.maximum, 3)
        self.assertEqual(formset.practice_limits[str(eligible.pk)], 1)

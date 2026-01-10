from characters.costs import get_freebie_cost
from characters.forms.core.freebies import CATEGORY_CHOICES, HumanFreebiesForm
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.mage.companion import Advantage
from characters.models.mage.focus import Practice, Tenet
from characters.models.mage.resonance import Resonance
from characters.models.mage.sorcerer import LinearMagicPath, LinearMagicRitual
from characters.models.mage.sphere import Sphere
from core.widgets import AutocompleteTextInput
from django import forms
from django.db.models import Q
from game.models import ObjectType
from widgets import ChainedChoiceField, ChainedSelectMixin

CATEGORY_CHOICES = CATEGORY_CHOICES + [
    ("Sphere", "Sphere"),
    ("Rotes", "Rotes"),
    ("Resonance", "Resonance"),
    ("Tenet", "Tenet"),
    ("Practice", "Practice"),
    ("Arete", "Arete"),
    ("Quintessence", "Quintessence"),
]


class CompanionFreebiesForm(ChainedSelectMixin, HumanFreebiesForm):
    category = ChainedChoiceField(choices=[])
    example = ChainedChoiceField(parent_field="category", choices_map={}, required=False)
    value = ChainedChoiceField(parent_field="example", choices_map={}, required=False)

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if suggestions is None:
            suggestions = [x.name.title() for x in Resonance.objects.order_by("name")]

        # Build category choices
        base_cats = list(CATEGORY_CHOICES)
        additional_cats = [("Advantage", "Advantage")]
        if self.instance.companion_type == "familiar":
            additional_cats.append(("Charms", "Charms"))
        all_cats = base_cats + additional_cats
        all_cats = [x for x in all_cats if self.validator(x[0])]
        self.fields["category"].choices = all_cats

        # Build example choices_map based on category
        example_choices_map = {}
        m = self.instance
        companion, _ = ObjectType.objects.get_or_create(
            name="companion", defaults={"type": "char", "gameline": "mta"}
        )

        for cat_value, cat_label in all_cats:
            if cat_value == "Attribute":
                examples = Attribute.objects.all()
                examples = [x for x in examples if getattr(m, x.property_name, 0) < 5]
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "Ability":
                examples = Ability.objects.order_by("name")
                examples = [x for x in examples if hasattr(m, x.property_name)]
                examples = [x for x in examples if isinstance(getattr(m, x.property_name), int)]
                examples = [x for x in examples if getattr(m, x.property_name, 0) < 4]
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "New Background":
                examples = Background.objects.filter(
                    property_name__in=m.allowed_backgrounds
                ).order_by("name")
                example_choices_map[cat_value] = [(f"bg_{x.pk}", str(x)) for x in examples]
            elif cat_value == "Background":
                examples = Background.objects.filter(
                    property_name__in=m.allowed_backgrounds
                ).order_by("name")
                example_choices_map[cat_value] = [(f"bg_{x.pk}", str(x)) for x in examples]
            elif cat_value == "Existing Background":
                examples = BackgroundRating.objects.filter(char=m, rating__lt=4)
                example_choices_map[cat_value] = [(f"bgr_{x.pk}", str(x)) for x in examples]
            elif cat_value == "MeritFlaw":
                examples = MeritFlaw.objects.filter(allowed_types=companion)
                if m.total_flaws() <= 0:
                    examples = examples.exclude(max_rating__lt=min(0, -7 - m.total_flaws()))
                examples = examples.exclude(min_rating__gt=m.freebies)
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "Advantage":
                examples = Advantage.objects.all().order_by("name")
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            else:
                example_choices_map[cat_value] = []

        self.fields["example"].choices_map = example_choices_map

        # Build value choices_map for MeritFlaw (example → value)
        value_choices_map = {}
        if "MeritFlaw" in example_choices_map:
            for mf_pk, mf_label in example_choices_map["MeritFlaw"]:
                mf = MeritFlaw.objects.get(pk=mf_pk)
                ratings = list(range(mf.min_rating, mf.max_rating + 1))
                # Filter out ratings based on character's current state
                ratings = [r for r in ratings if r <= m.freebies or r < 0]
                if m.total_flaws() <= 0:
                    ratings = [r for r in ratings if r >= -7 - m.total_flaws()]
                value_choices_map[mf_pk] = [(str(r), str(r)) for r in ratings]
        if "Advantage" in example_choices_map:
            for adv_pk, adv_label in example_choices_map["Advantage"]:
                adv = Advantage.objects.get(pk=adv_pk)
                # Advantage values are typically 1-5
                ratings = list(range(1, 6))
                ratings = [r for r in ratings if r * 3 <= m.freebies]  # 3 freebies per dot
                value_choices_map[adv_pk] = [(str(r), str(r)) for r in ratings]

        self.fields["value"].choices_map = value_choices_map

        # Re-run chain setup after choices configured
        self._setup_chains()

    def save(self, *args, **kwargs):
        return self.instance


class SorcererFreebiesForm(ChainedSelectMixin, HumanFreebiesForm):
    category = ChainedChoiceField(choices=[])
    example = ChainedChoiceField(parent_field="category", choices_map={}, required=False)
    practice = ChainedChoiceField(choices=[], required=False)
    ability = ChainedChoiceField(parent_field="practice", choices_map={}, required=False)

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if suggestions is None:
            suggestions = [x.name.title() for x in Resonance.objects.order_by("name")]

        m = self.instance

        # Build category choices
        base_cats = list(CATEGORY_CHOICES)
        additional_cats = [("Existing Path", "Existing Path"), ("New Path", "New Path")]
        if m.sorcerer_type == "hedge_mage":
            additional_cats.append(("Create Ritual", "Create Ritual"))
            additional_cats.append(("Select Ritual", "Select Ritual"))
        all_cats = base_cats + additional_cats
        all_cats = [x for x in all_cats if self.validator(x[0])]
        self.fields["category"].choices = all_cats

        # Build example choices_map based on category
        example_choices_map = {}
        companion, _ = ObjectType.objects.get_or_create(
            name="companion", defaults={"type": "char", "gameline": "mta"}
        )

        for cat_value, cat_label in all_cats:
            if cat_value == "Attribute":
                examples = Attribute.objects.all()
                examples = [x for x in examples if getattr(m, x.property_name, 0) < 5]
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "Ability":
                examples = Ability.objects.order_by("name")
                examples = [x for x in examples if hasattr(m, x.property_name)]
                examples = [x for x in examples if isinstance(getattr(m, x.property_name), int)]
                examples = [x for x in examples if getattr(m, x.property_name, 0) < 4]
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "New Background":
                examples = Background.objects.filter(
                    property_name__in=m.allowed_backgrounds
                ).order_by("name")
                example_choices_map[cat_value] = [(f"bg_{x.pk}", str(x)) for x in examples]
            elif cat_value == "Background":
                examples = Background.objects.filter(
                    property_name__in=m.allowed_backgrounds
                ).order_by("name")
                example_choices_map[cat_value] = [(f"bg_{x.pk}", str(x)) for x in examples]
            elif cat_value == "Existing Background":
                examples = BackgroundRating.objects.filter(char=m, rating__lt=4)
                example_choices_map[cat_value] = [(f"bgr_{x.pk}", str(x)) for x in examples]
            elif cat_value == "MeritFlaw":
                examples = MeritFlaw.objects.filter(allowed_types=companion)
                if m.total_flaws() <= 0:
                    examples = examples.exclude(max_rating__lt=min(0, -7 - m.total_flaws()))
                examples = examples.exclude(min_rating__gt=m.freebies)
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "New Path":
                if m.sorcerer_type == "hedge_mage":
                    examples = LinearMagicPath.objects.filter(numina_type="hedge_magic")
                else:
                    examples = LinearMagicPath.objects.filter(numina_type="psychic")
                examples = examples.exclude(id__in=[x.id for x in m.paths.all()])
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "Existing Path":
                if m.sorcerer_type == "hedge_mage":
                    examples = LinearMagicPath.objects.filter(numina_type="hedge_magic")
                else:
                    examples = LinearMagicPath.objects.filter(numina_type="psychic")
                examples = examples.filter(
                    id__in=[x.id for x in examples if 5 > m.path_rating(x) > 0]
                )
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "Select Ritual":
                rituals = Q()
                for path in m.pathrating_set.all():
                    ritual_levels = list(
                        m.rituals.filter(path=path.path).values_list("level", flat=True)
                    )
                    if ritual_levels:
                        maximum_level_ritual = max(ritual_levels)
                    else:
                        maximum_level_ritual = 0
                    rituals |= Q(
                        **{
                            "path": path.path,
                            "level__lte": min([path.rating, maximum_level_ritual + 1]),
                        }
                    )
                examples = LinearMagicRitual.objects.filter(rituals).exclude(
                    id__in=[x.id for x in m.rituals.all()]
                )
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            else:
                example_choices_map[cat_value] = []

        self.fields["example"].choices_map = example_choices_map

        # Build practice → ability chain (for New Path with hedge_mage)
        practices = (
            Practice.objects.exclude(polymorphic_ctype__model="specializedpractice")
            .exclude(polymorphic_ctype__model="corruptedpractice")
            .order_by("name")
        )
        self.fields["practice"].choices = [("", "---------")] + [
            (str(p.pk), str(p)) for p in practices
        ]

        ability_choices_map = {}
        for practice in practices:
            abilities = practice.abilities.all().order_by("name")
            ability_choices_map[str(practice.pk)] = [(str(a.pk), str(a)) for a in abilities]
        self.fields["ability"].choices_map = ability_choices_map

        # Re-run chain setup after choices configured
        self._setup_chains()

    def validator(self, trait_type):
        trait_type = trait_type.lower().split(" ")[-1]
        cost = get_freebie_cost(trait_type)
        if not isinstance(cost, int):
            return True
        if cost == 10000:
            return True
        if cost <= self.instance.freebies:
            return True
        return False

    def save(self, *args, **kwargs):
        return self.instance


class MageFreebiesForm(HumanFreebiesForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    resonance = forms.CharField(required=False, widget=AutocompleteTextInput(suggestions=[]))

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if suggestions is None:
            suggestions = [x.name.title() for x in Resonance.objects.order_by("name")]
        self.fields["resonance"].widget.suggestions = suggestions
        ADDITIONAL_CATS = [
            ("Sphere", "Sphere"),
            ("Rotes", "Rotes"),
            ("Resonance", "Resonance"),
            ("Tenet", "Tenet"),
            ("Practice", "Practice"),
            ("Arete", "Arete"),
            ("Quintessence", "Quintessence"),
        ]
        if (
            self.instance.freebies < 4
            or (self.instance.total_freebies() == 45 and self.instance.arete >= 4)
            or (self.instance.total_freebies() != 45 and self.instance.arete >= 3)
            or (self.instance.other_tenets.count() + 3 == self.instance.arete)
        ):
            ADDITIONAL_CATS = [x for x in ADDITIONAL_CATS if x[0] != "Arete"]
        if self.instance.freebies < 7:
            ADDITIONAL_CATS = [x for x in ADDITIONAL_CATS if x[0] != "Sphere"]
        if self.instance.freebies < 3:
            ADDITIONAL_CATS = [x for x in ADDITIONAL_CATS if x[0] != "Resonance"]
        self.fields["category"].choices += ADDITIONAL_CATS
        self.fields["category"].choices = [
            x for x in self.fields["category"].choices if self.validator(x[0])
        ]

        if self.is_bound:
            if self.data["category"] == "Sphere":
                self.fields["example"].queryset = Sphere.objects.all()
            if self.data["category"] == "Tenet":
                self.fields["example"].queryset = Tenet.objects.all()
            if self.data["category"] == "Practice" or self.data["category"] == "Arete":
                self.fields["example"].queryset = Practice.objects.all()

    def save(self, *args, **kwargs):
        return self.instance

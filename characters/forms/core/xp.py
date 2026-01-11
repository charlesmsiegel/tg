from django import forms

from characters.costs import get_meritflaw_xp_cost, get_xp_cost
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw
from widgets import ChainedChoiceField, ChainedSelectMixin


def _calculate_xp_cost(trait_type, current_value):
    """Calculate XP cost for raising a trait, handling new trait costs."""
    if current_value == 0:
        # Check for new trait cost
        new_key = f"new_{trait_type}"
        new_cost = get_xp_cost(new_key)
        if new_cost != 10000:  # Found a new trait cost
            return new_cost
    return get_xp_cost(trait_type) * current_value


CATEGORY_CHOICES = [
    ("-----", "-----"),
    ("Image", "Image"),
    ("Attribute", "Attribute"),
    ("Ability", "Ability"),
    ("Background", "Background"),
    ("Willpower", "Willpower"),
    ("MeritFlaw", "MeritFlaw"),
]


class XPForm(ChainedSelectMixin, forms.Form):
    category = ChainedChoiceField(choices=[])
    example = ChainedChoiceField(parent_field="category", choices_map={}, required=False)
    value = ChainedChoiceField(parent_field="example", choices_map={}, required=False)
    note = forms.CharField(max_length=300, required=False)
    pooled = forms.BooleanField(required=False)
    image_field = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character", None)
        super().__init__(*args, **kwargs)

        # Build category choices based on what's valid for the character
        category_choices = list(CATEGORY_CHOICES)
        if not self.image_valid():
            category_choices = [x for x in category_choices if x[0] != "Image"]
        if not self.attribute_valid():
            category_choices = [x for x in category_choices if x[0] != "Attribute"]
        if not self.ability_valid():
            category_choices = [x for x in category_choices if x[0] != "Ability"]
        if not self.background_valid():
            category_choices = [x for x in category_choices if x[0] != "Background"]
        if not self.willpower_valid():
            category_choices = [x for x in category_choices if x[0] != "Willpower"]
        if not self.mf_valid():
            category_choices = [x for x in category_choices if x[0] != "MeritFlaw"]
        self.fields["category"].choices = category_choices

        # Build example choices_map based on category
        example_choices_map = self._build_example_choices_map(category_choices)
        self.fields["example"].choices_map = example_choices_map

        # Build value choices_map for MeritFlaw (example → value)
        value_choices_map = self._build_value_choices_map(example_choices_map)
        self.fields["value"].choices_map = value_choices_map

        # Re-run chain setup after choices configured
        self._setup_chains()

    def _build_example_choices_map(self, category_choices):
        """Build the choices_map for example field based on categories."""
        example_choices_map = {}
        char = self.character

        for cat_value, cat_label in category_choices:
            if cat_value == "Attribute":
                examples = [
                    attr
                    for attr in Attribute.objects.all()
                    if getattr(char, attr.property_name) < 5
                    and _calculate_xp_cost("attribute", getattr(char, attr.property_name))
                    <= char.xp
                ]
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "Ability":
                examples = [
                    ability
                    for ability in Ability.objects.filter(
                        property_name__in=char.talents + char.skills + char.knowledges
                    )
                    if getattr(char, ability.property_name) < 5
                    and _calculate_xp_cost("ability", getattr(char, ability.property_name))
                    <= char.xp
                ]
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "Background":
                # New backgrounds
                new_bgs = Background.objects.filter(
                    property_name__in=char.allowed_backgrounds
                ).order_by("name")
                new_bg_choices = [(f"bg_{x.pk}", f"New: {x}") for x in new_bgs if char.xp >= 5]
                # Existing backgrounds that can be increased
                existing_bgs = char.backgrounds.filter(rating__lt=5)
                existing_bg_choices = [
                    (f"br_{x.pk}", f"{x}")
                    for x in existing_bgs
                    if _calculate_xp_cost("background", x.rating) <= char.xp
                ]
                example_choices_map[cat_value] = new_bg_choices + existing_bg_choices
            elif cat_value == "MeritFlaw":
                from game.models import ObjectType

                char_type = char.type
                if "human" in char_type:
                    char_type = "human"
                chartype, _ = ObjectType.objects.get_or_create(
                    name=char_type, defaults={"type": "char", "gameline": "wod"}
                )
                filtered_mfs = MeritFlaw.objects.filter(allowed_types=chartype)
                affordable_mfs = []
                for mf in filtered_mfs:
                    current_rating = char.mf_rating(mf)
                    ratings = mf.get_ratings()
                    for rating in ratings:
                        cost = get_meritflaw_xp_cost(current_rating, rating)
                        if cost <= char.xp and rating != current_rating:
                            affordable_mfs.append(mf.id)
                            break
                filtered_mfs = filtered_mfs.filter(id__in=affordable_mfs)
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in filtered_mfs]
            else:
                example_choices_map[cat_value] = []

        return example_choices_map

    def _build_value_choices_map(self, example_choices_map):
        """Build the choices_map for value field (MeritFlaw ratings)."""
        value_choices_map = {}
        char = self.character

        if "MeritFlaw" in example_choices_map:
            for mf_pk, mf_label in example_choices_map["MeritFlaw"]:
                mf = MeritFlaw.objects.get(pk=mf_pk)
                current_rating = char.mf_rating(mf)
                ratings = mf.get_ratings()
                affordable_ratings = []
                for rating in ratings:
                    cost = get_meritflaw_xp_cost(current_rating, rating)
                    if cost <= char.xp and rating != current_rating:
                        affordable_ratings.append(rating)
                value_choices_map[mf_pk] = [(str(r), str(r)) for r in affordable_ratings]

        return value_choices_map

    def image_valid(self):
        if self.character.image and self.character.image.storage.exists(self.character.image.name):
            return False
        else:
            return True

    def attribute_valid(self):
        filtered_attributes = [
            attribute
            for attribute in Attribute.objects.all()
            if getattr(self.character, attribute.property_name) < 5
        ]
        filtered_for_xp_cost = [
            x
            for x in filtered_attributes
            if _calculate_xp_cost("attribute", getattr(self.character, x.property_name))
            <= self.character.xp
        ]
        return len(filtered_for_xp_cost) > 0

    def ability_valid(self):
        filtered_abilities = [
            ability
            for ability in Ability.objects.filter(
                property_name__in=self.character.talents
                + self.character.skills
                + self.character.knowledges
            )
            if getattr(self.character, ability.property_name) < 5
        ]
        filtered_for_xp_cost = [
            x
            for x in filtered_abilities
            if _calculate_xp_cost("ability", getattr(self.character, x.property_name))
            <= self.character.xp
        ]
        return len(filtered_for_xp_cost) > 0

    def background_valid(self):
        """Check if any background (new or existing) is affordable."""
        # Check if new background is affordable (minimum 5 XP)
        if self.character.xp >= get_xp_cost("new_background"):
            return True
        # Check if any existing background can be increased
        bgs = self.character.backgrounds.filter(rating__lt=5)
        filtered_for_xp_cost = [
            x for x in bgs if _calculate_xp_cost("background", x.rating) <= self.character.xp
        ]
        return len(filtered_for_xp_cost) > 0

    def willpower_valid(self):
        return _calculate_xp_cost("willpower", self.character.willpower) <= self.character.xp

    def mf_valid(self):
        # Check if character has any affordable merit/flaws
        from game.models import ObjectType

        char_type = self.character.type
        if "human" in char_type:
            char_type = "human"

        chartype, _ = ObjectType.objects.get_or_create(
            name=char_type, defaults={"type": "char", "gameline": "wod"}
        )
        filtered_mfs = MeritFlaw.objects.filter(allowed_types=chartype)

        # Check if any merit/flaw has an affordable rating
        for mf in filtered_mfs:
            current_rating = self.character.mf_rating(mf)
            ratings = mf.get_ratings()

            for rating in ratings:
                cost = get_meritflaw_xp_cost(current_rating, rating)
                if cost <= self.character.xp and rating != current_rating:
                    return True

        return False

    def clean_category(self):
        category = self.cleaned_data.get("category")

        if category == "-----":
            raise forms.ValidationError("Invalid category selected")

        return category

    def clean_example(self):

        category = self.cleaned_data.get("category")
        example = self.cleaned_data.get("example")

        if category == "Attribute":
            example = Attribute.objects.get(pk=example)
        elif category == "Ability":
            example = Ability.objects.get(pk=example)
        elif category == "Background":
            # Parse prefixed value: "bg_123" for Background, "br_456" for BackgroundRating
            if example.startswith("bg_"):
                bg_pk = example[3:]
                example = Background.objects.get(pk=bg_pk)
            elif example.startswith("br_"):
                br_pk = example[3:]
                example = BackgroundRating.objects.get(pk=br_pk)
            else:
                raise forms.ValidationError("Invalid background selection")
        elif category == "MeritFlaw":
            example = MeritFlaw.objects.get(pk=example)

        return example

    def clean_value(self):
        value = self.cleaned_data.get("value")
        if value is not None and value != "":
            # Value comes in as a string (the ID), convert to int
            return int(value)
        return None

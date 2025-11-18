from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background
from characters.models.core.merit_flaw_block import MeritFlaw
from core.models import Number
from django import forms

CATEGORY_CHOICES = [
    ("-----", "-----"),
    ("Image", "Image"),
    ("Attribute", "Attribute"),
    ("Ability", "Ability"),
    ("New Background", "New Background"),
    ("Existing Background", "Existing Background"),
    ("Willpower", "Willpower"),
    ("MeritFlaw", "MeritFlaw"),
]


class XPForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    example = forms.ChoiceField(choices=[], required=False)
    value = forms.ModelChoiceField(queryset=Number.objects.all(), required=False)
    note = forms.CharField(max_length=300, required=False)
    pooled = forms.BooleanField(required=False)
    image_field = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character", None)
        super().__init__(*args, **kwargs)

        if not self.image_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "Image"
            ]
        if not self.attribute_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "Attribute"
            ]
        if not self.ability_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "Ability"
            ]
        if not self.new_bg_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "New Background"
            ]
        if not self.existing_bg_valid():
            self.fields["category"].choices = [
                x
                for x in self.fields["category"].choices
                if x[0] != "Existing Background"
            ]
        if not self.willpower_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "Willpower"
            ]
        if not self.mf_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "MeritFlaw"
            ]

        category = self.data.get("category")
        if category == "Attribute":
            self.fields["example"].choices = [
                (attr.id, attr.name) for attr in Attribute.objects.all()
            ]
        elif category == "Ability":
            self.fields["example"].choices = [
                (ability.id, ability.name) for ability in Ability.objects.all()
            ]
        elif category == "New Background":
            self.fields["example"].choices = [
                (bg.id, bg.name) for bg in Background.objects.all()
            ]
        elif category == "Existing Background":
            self.fields["example"].choices = [
                (bg.id, bg.bg.name + f" ({bg.note})")
                for bg in self.character.backgrounds.all()
            ]
        elif category == "MeritFlaw":
            # Filter merit/flaws by character type and affordability
            from game.models import ObjectType

            char_type = self.character.type
            if "human" in char_type:
                char_type = "human"

            try:
                chartype = ObjectType.objects.get(name=char_type)
                filtered_mfs = MeritFlaw.objects.filter(allowed_types=chartype)
            except ObjectType.DoesNotExist:
                filtered_mfs = MeritFlaw.objects.none()

            # Only show merit/flaws with at least one affordable rating
            affordable_mfs = []
            for mf in filtered_mfs:
                current_rating = self.character.mf_rating(mf)
                ratings = mf.get_ratings()

                for rating in ratings:
                    # Calculate cost: 3 × |new_rating - current_rating|
                    cost = 3 * abs(rating - current_rating)
                    if cost <= self.character.xp and rating != current_rating:
                        affordable_mfs.append(mf.id)
                        break

            filtered_mfs = filtered_mfs.filter(id__in=affordable_mfs)

            self.fields["example"].choices = [
                (mf.id, mf.name) for mf in filtered_mfs
            ]

    def image_valid(self):
        if self.character.image and self.character.image.storage.exists(
            self.character.image.name
        ):
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
            if self.character.xp_cost(
                "attribute",
                getattr(self.character, x.property_name),
            )
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
            if self.character.xp_cost(
                "ability",
                getattr(self.character, x.property_name),
            )
            <= self.character.xp
        ]
        return len(filtered_for_xp_cost) > 0

    def new_bg_valid(self):
        return self.character.xp >= 5

    def existing_bg_valid(self):
        bgs = self.character.backgrounds.filter(rating__lt=5)
        filtered_for_xp_cost = [
            x
            for x in bgs
            if self.character.xp_cost(
                "background",
                x.rating,
            )
            <= self.character.xp
        ]
        return len(filtered_for_xp_cost) > 0

    def willpower_valid(self):
        return (
            self.character.xp_cost("willpower", self.character.willpower)
            <= self.character.xp
        )

    def mf_valid(self):
        # Check if character has any affordable merit/flaws
        from game.models import ObjectType

        char_type = self.character.type
        if "human" in char_type:
            char_type = "human"

        try:
            chartype = ObjectType.objects.get(name=char_type)
            filtered_mfs = MeritFlaw.objects.filter(allowed_types=chartype)
        except ObjectType.DoesNotExist:
            return False

        # Check if any merit/flaw has an affordable rating
        for mf in filtered_mfs:
            current_rating = self.character.mf_rating(mf)
            ratings = mf.get_ratings()

            for rating in ratings:
                # Calculate cost: 3 × |new_rating - current_rating|
                cost = 3 * abs(rating - current_rating)
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
        elif category == "New Background":
            example = Background.objects.get(pk=example)
        elif category == "Existing Background":
            example = self.character.backgrounds.get(pk=example)
        elif category == "MeritFlaw":
            example = MeritFlaw.objects.get(pk=example)

        return example

    def clean_value(self):
        value = self.cleaned_data.get("value")
        if value is not None:
            return value.id
        return value

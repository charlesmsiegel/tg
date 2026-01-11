"""
Chained Select Freebie Forms

These forms use ChainedSelectMixin to provide cascading dropdowns
without manual AJAX. Choices are computed at form initialization
and embedded in the page JavaScript.
"""

from django import forms

from characters.costs import get_freebie_cost
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw
from game.models import ObjectType
from widgets import ChainedChoiceField, ChainedSelectMixin, ConditionalFieldsMixin

CATEGORY_CHOICES = [
    ("-----", "-----"),
    ("Attribute", "Attribute"),
    ("Ability", "Ability"),
    ("Background", "Background"),
    ("Willpower", "Willpower"),
    ("MeritFlaw", "MeritFlaw"),
]

# Base conditional visibility rules for freebies forms
# Subclasses can extend via _get_conditional_fields()
BASE_CONDITIONAL_FIELDS = {
    "example": {
        "hidden_when": {
            "category": {"value_in": ["-----", "Willpower", "Quintessence", "Rotes", "Resonance"]}
        },
        "initially_hidden": True,
    },
    "value": {
        "visible_when": {"category": {"value_is": "MeritFlaw"}},
        "initially_hidden": True,
    },
    "note": {
        "visible_when": {"category": {"value_is": "Background"}},
        "initially_hidden": True,
    },
    "pooled": {
        "visible_when": {
            "category": {"value_is": "Background"},
            "example": {"metadata_truthy": "poolable"},
            "_context": {"is_group_member": True},
        },
        "initially_hidden": True,
    },
}


class ChainedHumanFreebiesForm(ConditionalFieldsMixin, ChainedSelectMixin, forms.Form):
    """
    Freebie spending form using ChainedSelectMixin and ConditionalFieldsMixin.

    All cascading dropdown options are computed at form initialization
    based on the character instance, then embedded in the page.

    Field visibility is handled declaratively via conditional_fields rules,
    eliminating the need for custom JavaScript in templates.
    """

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    example = ChainedChoiceField(
        parent_field="category",
        required=False,
        empty_label="---------",
    )
    value = ChainedChoiceField(
        parent_field="example",
        required=False,
        empty_label="---------",
    )
    note = forms.CharField(max_length=300, required=False)
    pooled = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)

        if self.instance:
            self._setup_category_choices()
            self._setup_example_choices()
            self._setup_value_choices()

    def get_conditional_context(self):
        """Provide context variables for conditional field visibility."""
        context = super().get_conditional_context()
        if self.instance:
            context["is_group_member"] = getattr(self.instance, "is_group_member", False)
        return context

    def get_conditional_rules(self):
        """Return visibility rules, allowing subclasses to extend."""
        rules = dict(BASE_CONDITIONAL_FIELDS)
        rules.update(self._get_additional_conditional_fields())
        return rules

    def _get_additional_conditional_fields(self):
        """Override in subclasses to add gameline-specific visibility rules."""
        return {}

    def _get_base_categories(self):
        """Return base category choices. Override to customize."""
        return list(CATEGORY_CHOICES)

    def _get_additional_categories(self):
        """Override in subclasses to add gameline-specific categories."""
        return []

    def _setup_category_choices(self):
        """Filter category choices based on affordability."""
        choices = self._get_base_categories() + self._get_additional_categories()

        if self.instance.freebies < 5:
            choices = [x for x in choices if x[0] != "Attribute"]
        if self.instance.freebies < 2:
            choices = [x for x in choices if x[0] != "Ability"]

        # Filter based on freebie cost
        choices = [x for x in choices if self._can_afford_category(x[0])]
        self.fields["category"].choices = choices

    def _can_afford_category(self, category):
        """Check if character can afford this category type."""
        trait_type = category.lower().split(" ")[-1]
        cost = get_freebie_cost(trait_type)

        if not isinstance(cost, int):
            return True
        if cost == 10000:
            return False
        return cost <= self.instance.freebies

    def _setup_example_choices(self):
        """Build the category->example choices map."""
        example_map = {}

        # Attributes - filter to those below 5
        attrs = [
            x for x in Attribute.objects.all() if getattr(self.instance, x.property_name, 0) < 5
        ]
        example_map["Attribute"] = [(str(a.pk), str(a)) for a in attrs]

        # Abilities - filter to those below 5 and that character has
        abilities = [
            x
            for x in Ability.objects.order_by("name")
            if getattr(self.instance, x.property_name, 0) < 5
            and hasattr(self.instance, x.property_name)
        ]
        example_map["Ability"] = [(str(a.pk), str(a)) for a in abilities]

        # Backgrounds - combined new and existing with prefixes
        example_map["Background"] = self._get_background_choices()

        # Merit/Flaws - filter by character type and affordability
        example_map["MeritFlaw"] = self._get_meritflaw_choices()

        # Categories with no example selection
        example_map["Willpower"] = []
        example_map["-----"] = []

        # Add gameline-specific categories
        example_map.update(self._get_additional_example_choices())

        self.fields["example"].choices_map = example_map

    def _get_background_choices(self):
        """Get combined new and existing background choices with metadata."""
        options = []

        # New backgrounds - prefixed with "bg_"
        new_backgrounds = Background.objects.filter(
            property_name__in=self.instance.allowed_backgrounds
        ).order_by("name")
        for bg in new_backgrounds:
            poolable = bg.poolable if hasattr(bg, "poolable") else False
            # Use 3-tuple format: (value, label, metadata_dict)
            options.append((f"bg_{bg.pk}", f"{bg.name} (new)", {"poolable": str(poolable).lower()}))

        # Existing backgrounds - prefixed with "br_"
        existing_backgrounds = BackgroundRating.objects.filter(char=self.instance, rating__lt=5)
        for br in existing_backgrounds:
            options.append((f"br_{br.pk}", str(br), {"poolable": "false"}))

        return options

    def _get_meritflaw_choices(self):
        """Get affordable merit/flaw choices for this character type."""
        char_type = self.instance.type
        if "human" in char_type:
            char_type = "human"

        chartype, _ = ObjectType.objects.get_or_create(
            name=char_type, defaults={"type": "char", "gameline": "wod"}
        )
        all_mfs = MeritFlaw.objects.filter(allowed_types=chartype)

        # Filter to only show merit/flaws with at least one affordable rating
        affordable_mfs = []
        current_flaws = self.instance.total_flaws()
        available_freebies = self.instance.freebies

        for mf in all_mfs:
            ratings = mf.get_ratings()
            has_affordable = False

            for rating in ratings:
                if rating < 0:
                    # Flaws are affordable if they don't exceed -7 limit
                    if current_flaws + rating >= -7:
                        has_affordable = True
                        break
                else:
                    # Merits are affordable if we have enough freebies
                    if rating <= available_freebies:
                        has_affordable = True
                        break

            if has_affordable:
                affordable_mfs.append((str(mf.pk), str(mf)))

        return affordable_mfs

    def _get_additional_example_choices(self):
        """Override in subclasses to add gameline-specific example choices."""
        return {}

    def _setup_value_choices(self):
        """Build the example->value choices map for merit/flaws."""
        value_map = {}

        # Get all merit/flaws that might be selected
        char_type = self.instance.type
        if "human" in char_type:
            char_type = "human"

        chartype, _ = ObjectType.objects.get_or_create(
            name=char_type, defaults={"type": "char", "gameline": "wod"}
        )
        all_mfs = MeritFlaw.objects.filter(allowed_types=chartype)

        current_flaws = self.instance.total_flaws()
        available_freebies = self.instance.freebies
        current_rating = lambda mf: self.instance.mf_rating(mf)

        for mf in all_mfs:
            ratings = mf.get_ratings()
            affordable_ratings = []

            for rating in sorted(ratings):
                if rating < 0:
                    # Flaw - check -7 limit
                    if current_flaws + rating >= -7:
                        affordable_ratings.append((str(rating), str(rating)))
                else:
                    # Merit - check freebies
                    if rating <= available_freebies:
                        affordable_ratings.append((str(rating), str(rating)))

            if affordable_ratings:
                value_map[str(mf.pk)] = affordable_ratings

        self.fields["value"].choices_map = value_map

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")

        if category == "-----":
            raise forms.ValidationError("Must Choose Freebie Expenditure Type")
        elif category == "MeritFlaw" and (
            not cleaned_data.get("example") or not cleaned_data.get("value")
        ):
            raise forms.ValidationError("Must Choose Merit/Flaw and rating")
        elif category in [
            "Attribute",
            "Ability",
            "Background",
            "Sphere",
            "Tenet",
            "Practice",
        ] and not cleaned_data.get("example"):
            raise forms.ValidationError("Must Choose Trait")
        elif category == "Resonance" and not cleaned_data.get("resonance"):
            raise forms.ValidationError("Must Choose Resonance")

        return cleaned_data

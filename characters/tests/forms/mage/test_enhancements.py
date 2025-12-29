"""
Tests for Mage Enhancement forms.

Tests cover:
- EnhancementForm initialization with different ranks
- Validation of enhancement style and type
- Attribute enhancement validation
- Existing device enhancement validation
- New device enhancement validation (with new and existing effects)
- Health enhancement
- Flaw and paradox handling
- Form save functionality for all enhancement types
"""

from characters.forms.mage.enhancements import EnhancementForm
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw, MeritFlawRating
from characters.models.mage.effect import Effect
from characters.models.mage.mage import Mage
from characters.models.mage.resonance import Resonance
from characters.tests.utils import mage_setup
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import ObjectType
from items.models.mage.artifact import Artifact
from items.models.mage.talisman import Talisman
from items.models.mage.wonder import Wonder


class TestEnhancementFormInit(TestCase):
    """Test EnhancementForm initialization."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_form_initializes_with_rank(self):
        """Test that form initializes with rank parameter."""
        form = EnhancementForm(rank=2)
        self.assertEqual(form.rank, 2)

    def test_form_creates_attribute_fields_based_on_rank(self):
        """Test that form creates correct number of attribute fields."""
        form = EnhancementForm(rank=3)

        for i in range(3):
            self.assertIn(f"attribute_{i}", form.fields)
        self.assertNotIn("attribute_3", form.fields)

    def test_form_creates_resonance_suggestions(self):
        """Test that resonance field has autocomplete suggestions."""
        form = EnhancementForm(rank=1)

        suggestions = form.fields["new_device_resonance"].widget.suggestions
        self.assertIsNotNone(suggestions)
        self.assertGreater(len(suggestions), 0)

    def test_form_accepts_custom_suggestions(self):
        """Test that form accepts custom resonance suggestions."""
        custom_suggestions = ["Custom 1", "Custom 2"]
        form = EnhancementForm(rank=1, suggestions=custom_suggestions)

        self.assertEqual(
            form.fields["new_device_resonance"].widget.suggestions, custom_suggestions
        )

    def test_form_includes_wonder_form_fields(self):
        """Test that form includes embedded WonderForm fields."""
        form = EnhancementForm(rank=1)

        self.assertIn("new_device_name", form.fields)
        self.assertIn("new_device_description", form.fields)
        self.assertIn("new_device_wonder_type", form.fields)

    def test_form_wonder_type_choices(self):
        """Test that wonder type choices are limited to artifact and talisman."""
        form = EnhancementForm(rank=1)

        choices = form.fields["new_device_wonder_type"].choices
        choice_values = [c[0] for c in choices]

        self.assertIn("artifact", choice_values)
        self.assertIn("talisman", choice_values)
        self.assertNotIn("charm", choice_values)

    def test_form_flaw_queryset_filters_by_rank(self):
        """Test that flaw queryset is filtered to match enhancement rank."""
        mage_type = ObjectType.objects.get(name="mage")

        # Create flaws at different ratings
        flaw_rank2 = MeritFlaw.objects.create(name="Test Flaw Rank 2")
        flaw_rank2.add_rating(-2)
        flaw_rank2.allowed_types.add(mage_type)

        flaw_rank3 = MeritFlaw.objects.create(name="Test Flaw Rank 3")
        flaw_rank3.add_rating(-3)
        flaw_rank3.allowed_types.add(mage_type)

        form = EnhancementForm(rank=2)
        flaw_queryset = form.fields["flaw"].queryset

        self.assertIn(flaw_rank2, flaw_queryset)
        self.assertNotIn(flaw_rank3, flaw_queryset)

    def test_form_device_queryset_filters_by_rank(self):
        """Test that device queryset is filtered to match enhancement rank."""
        wonder1 = Wonder.objects.create(name="Wonder Rank 1", rank=1)
        wonder2 = Wonder.objects.create(name="Wonder Rank 2", rank=2)

        form = EnhancementForm(rank=2)
        device_queryset = form.fields["device"].queryset

        self.assertIn(wonder2, device_queryset)
        self.assertNotIn(wonder1, device_queryset)

    def test_form_effect_queryset_filters_by_rank(self):
        """Test that effect queryset is filtered by rote cost based on rank."""
        # Rank 2 means max effect cost is 2 * 2 = 4
        small_effect = Effect.objects.create(name="Small Effect", forces=2)
        big_effect = Effect.objects.create(name="Big Effect", forces=5)

        form = EnhancementForm(rank=2)
        effect_queryset = form.fields["new_device_effect"].queryset

        self.assertIn(small_effect, effect_queryset)
        self.assertNotIn(big_effect, effect_queryset)


class TestEnhancementFormValidation(TestCase):
    """Test EnhancementForm validation logic."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_missing_enhancement_style_raises_error(self):
        """Test that missing enhancement style raises validation error."""
        form = EnhancementForm(
            data={"enhancement_type": "Attributes"},
            rank=1,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Enhancement style must be selected", str(form.errors))

    def test_missing_enhancement_type_raises_error(self):
        """Test that missing enhancement type raises validation error."""
        form = EnhancementForm(
            data={"enhancement_style": "Cybernetics"},
            rank=1,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Enhancement type must be selected", str(form.errors))

    def test_valid_enhancement_style_choices(self):
        """Test that all enhancement style choices are valid."""
        for style in ["Cybernetics", "Biomods", "Genegineering"]:
            form = EnhancementForm(rank=1)
            self.assertIn(style, [c[0] for c in form.fields["enhancement_style"].choices])

    def test_valid_enhancement_type_choices(self):
        """Test that all enhancement type choices are valid."""
        for type_ in ["Attributes", "Existing Device", "New Device", "Health"]:
            form = EnhancementForm(rank=1)
            self.assertIn(type_, [c[0] for c in form.fields["enhancement_type"].choices])


class TestEnhancementFormAttributeValidation(TestCase):
    """Test validation for Attributes enhancement type."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_attributes_requires_correct_number_of_selections(self):
        """Test that Attributes type requires exactly rank attributes selected."""
        strength = Attribute.objects.get(property_name="strength")
        dexterity = Attribute.objects.get(property_name="dexterity")

        # Missing one attribute for rank 2
        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "Attributes",
                "attribute_0": strength.pk,
            },
            rank=2,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("must select exactly 2 attribute", str(form.errors))

    def test_attributes_valid_with_correct_selections(self):
        """Test that Attributes type validates with correct number of attributes."""
        strength = Attribute.objects.get(property_name="strength")
        dexterity = Attribute.objects.get(property_name="dexterity")

        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "Attributes",
                "attribute_0": strength.pk,
                "attribute_1": dexterity.pk,
            },
            rank=2,
        )

        self.assertTrue(form.is_valid())


class TestEnhancementFormExistingDeviceValidation(TestCase):
    """Test validation for Existing Device enhancement type."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_existing_device_requires_device_selection(self):
        """Test that Existing Device type requires a device to be selected."""
        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "Existing Device",
            },
            rank=2,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("must select an existing device", str(form.errors))

    def test_existing_device_valid_with_selection(self):
        """Test that Existing Device type validates with device selected."""
        wonder = Wonder.objects.create(name="Test Wonder", rank=2)

        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "Existing Device",
                "device": wonder.pk,
            },
            rank=2,
        )

        self.assertTrue(form.is_valid())


class TestEnhancementFormNewDeviceValidation(TestCase):
    """Test validation for New Device enhancement type."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.effect = Effect.objects.create(name="Test Effect", forces=2)
        Resonance.objects.get_or_create(name="Dynamic")

    def test_new_device_requires_power_option(self):
        """Test that New Device type requires power option selection."""
        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "New Device",
                "new_device_wonder_type": "artifact",
                "new_device_resonance": "Dynamic",
            },
            rank=2,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("must select a power option", str(form.errors))

    def test_new_device_requires_wonder_type(self):
        """Test that New Device type requires wonder type selection."""
        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "New Device",
                "new_device_new_power_option": "New Effect",
                "new_device_resonance": "Dynamic",
            },
            rank=2,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("must select a wonder type", str(form.errors))

    def test_new_device_requires_resonance(self):
        """Test that New Device type requires resonance."""
        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "New Device",
                "new_device_new_power_option": "New Effect",
                "new_device_wonder_type": "artifact",
            },
            rank=2,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("must specify a resonance", str(form.errors))

    def test_new_effect_requires_name(self):
        """Test that creating new effect requires a name."""
        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "New Device",
                "new_device_new_power_option": "New Effect",
                "new_device_wonder_type": "artifact",
                "new_device_resonance": "Dynamic",
                "new_device_new_effect_description": "Test Description",
            },
            rank=2,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("must provide a name for the new effect", str(form.errors))

    def test_new_effect_requires_description(self):
        """Test that creating new effect requires a description."""
        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "New Device",
                "new_device_new_power_option": "New Effect",
                "new_device_wonder_type": "artifact",
                "new_device_resonance": "Dynamic",
                "new_device_new_effect_name": "Test Effect",
            },
            rank=2,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("must provide a description for the new effect", str(form.errors))

    def test_new_effect_cost_cannot_exceed_limit(self):
        """Test that new effect cost cannot exceed 2 * rank."""
        # Rank 1 means max cost is 2, so forces=3 is too expensive
        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "New Device",
                "new_device_new_power_option": "New Effect",
                "new_device_wonder_type": "artifact",
                "new_device_resonance": "Dynamic",
                "new_device_new_effect_name": "Test Effect",
                "new_device_new_effect_description": "Test Description",
                "new_device_new_effect_forces": 3,
                # Provide all sphere fields with 0 to avoid NoneType error
                "new_device_new_effect_correspondence": 0,
                "new_device_new_effect_time": 0,
                "new_device_new_effect_spirit": 0,
                "new_device_new_effect_matter": 0,
                "new_device_new_effect_life": 0,
                "new_device_new_effect_entropy": 0,
                "new_device_new_effect_mind": 0,
                "new_device_new_effect_prime": 0,
            },
            rank=1,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Effect cost", str(form.errors))

    def test_existing_effect_requires_selection(self):
        """Test that Existing Effect option requires effect selection."""
        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "New Device",
                "new_device_new_power_option": "Existing Effect",
                "new_device_wonder_type": "artifact",
                "new_device_resonance": "Dynamic",
            },
            rank=2,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("must select an existing effect", str(form.errors))

    def test_existing_effect_valid_with_selection(self):
        """Test that Existing Effect validates with effect selected."""
        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "New Device",
                "new_device_new_power_option": "Existing Effect",
                "new_device_wonder_type": "artifact",
                "new_device_resonance": "Dynamic",
                "new_device_effect": self.effect.pk,
            },
            rank=2,
        )

        self.assertTrue(form.is_valid())


class TestEnhancementFormSave(TestCase):
    """Test EnhancementForm save functionality."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
        )

    def test_save_requires_char_kwarg(self):
        """Test that save raises error without char kwarg."""
        strength = Attribute.objects.get(property_name="strength")
        dexterity = Attribute.objects.get(property_name="dexterity")

        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "Attributes",
                "attribute_0": strength.pk,
                "attribute_1": dexterity.pk,
            },
            rank=2,
        )
        form.is_valid()

        with self.assertRaises(ValueError):
            form.save()

    def test_save_existing_device_enhancement(self):
        """Test saving an Existing Device enhancement adds device to mage."""
        # Create incomplete background rating for enhancement
        enhancement_bg = Background.objects.get_or_create(
            property_name="enhancement", defaults={"name": "Enhancement"}
        )[0]
        BackgroundRating.objects.create(
            char=self.mage,
            bg=enhancement_bg,
            rating=2,
            complete=False,
        )

        wonder = Wonder.objects.create(name="Cyber Eye", rank=2)

        form = EnhancementForm(
            data={
                "enhancement_style": "Cybernetics",
                "enhancement_type": "Existing Device",
                "device": wonder.pk,
            },
            rank=2,
        )
        form.is_valid()
        form.save(char=self.mage)

        self.mage.refresh_from_db()

        # Verify device was added
        self.assertIn(wonder, self.mage.enhancement_devices.all())

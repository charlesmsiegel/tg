"""
Tests for URLMethodsMixin.

Tests verify:
- URL generation with url_namespace and url_name set
- Default url_name behavior (lowercase class name)
- NotImplementedError when url_namespace is missing
- Both instance methods and class methods work correctly
"""

from django.test import TestCase

from characters.models.core import Archetype, Derangement
from characters.models.mage import Resonance
from core.models import URLMethodsMixin


class TestURLMethodsMixinErrorHandling(TestCase):
    """Test URLMethodsMixin error handling when url_namespace is not set."""

    def test_get_absolute_url_raises_without_namespace(self):
        """Test that get_absolute_url raises NotImplementedError when url_namespace is None."""

        class TestModel(URLMethodsMixin):
            pk = 1

        obj = TestModel()
        with self.assertRaises(NotImplementedError) as context:
            obj.get_absolute_url()

        self.assertIn("TestModel", str(context.exception))
        self.assertIn("url_namespace", str(context.exception))

    def test_get_update_url_raises_without_namespace(self):
        """Test that get_update_url raises NotImplementedError when url_namespace is None."""

        class TestModel(URLMethodsMixin):
            pk = 1

        obj = TestModel()
        with self.assertRaises(NotImplementedError) as context:
            obj.get_update_url()

        self.assertIn("TestModel", str(context.exception))
        self.assertIn("url_namespace", str(context.exception))

    def test_get_creation_url_raises_without_namespace(self):
        """Test that get_creation_url raises NotImplementedError when url_namespace is None."""

        class TestModel(URLMethodsMixin):
            pass

        with self.assertRaises(NotImplementedError) as context:
            TestModel.get_creation_url()

        self.assertIn("TestModel", str(context.exception))
        self.assertIn("url_namespace", str(context.exception))


class TestURLMethodsMixinDefaultUrlName(TestCase):
    """Test URLMethodsMixin default url_name behavior."""

    def test_default_url_name_uses_lowercase_class_name(self):
        """Test that _get_url_name returns lowercase class name when url_name is not set."""

        class MyCustomModel(URLMethodsMixin):
            url_namespace = "test"

        obj = MyCustomModel()
        self.assertEqual(obj._get_url_name(), "mycustommodel")

    def test_default_url_name_cls_uses_lowercase_class_name(self):
        """Test that _get_url_name_cls returns lowercase class name when url_name is not set."""

        class MyCustomModel(URLMethodsMixin):
            url_namespace = "test"

        self.assertEqual(MyCustomModel._get_url_name_cls(), "mycustommodel")

    def test_explicit_url_name_overrides_default(self):
        """Test that explicit url_name overrides the default lowercase class name."""

        class MyCustomModel(URLMethodsMixin):
            url_namespace = "test"
            url_name = "custom_name"

        obj = MyCustomModel()
        self.assertEqual(obj._get_url_name(), "custom_name")

    def test_explicit_url_name_cls_overrides_default(self):
        """Test that explicit url_name overrides default for class method."""

        class MyCustomModel(URLMethodsMixin):
            url_namespace = "test"
            url_name = "custom_name"

        self.assertEqual(MyCustomModel._get_url_name_cls(), "custom_name")


class TestURLMethodsMixinURLGeneration(TestCase):
    """Test URLMethodsMixin URL generation with real models."""

    @classmethod
    def setUpTestData(cls):
        cls.archetype = Archetype.objects.create(name="Test Archetype")
        cls.derangement = Derangement.objects.create(name="Test Derangement")
        cls.resonance = Resonance.objects.create(name="Test Resonance")

    def test_archetype_get_absolute_url(self):
        """Test Archetype generates correct absolute URL."""
        url = self.archetype.get_absolute_url()
        self.assertEqual(url, f"/characters/archetypes/{self.archetype.pk}/")

    def test_archetype_get_update_url(self):
        """Test Archetype generates correct update URL."""
        url = self.archetype.get_update_url()
        self.assertEqual(url, f"/characters/update/archetypes/{self.archetype.pk}/")

    def test_archetype_get_creation_url(self):
        """Test Archetype generates correct creation URL."""
        url = Archetype.get_creation_url()
        self.assertEqual(url, "/characters/create/archetypes/")

    def test_derangement_get_absolute_url(self):
        """Test Derangement generates correct absolute URL."""
        url = self.derangement.get_absolute_url()
        self.assertEqual(url, f"/characters/derangement/{self.derangement.pk}/")

    def test_derangement_get_update_url(self):
        """Test Derangement generates correct update URL."""
        url = self.derangement.get_update_url()
        self.assertEqual(url, f"/characters/update/derangement/{self.derangement.pk}/")

    def test_derangement_get_creation_url(self):
        """Test Derangement generates correct creation URL."""
        url = Derangement.get_creation_url()
        self.assertEqual(url, "/characters/create/derangement/")

    def test_resonance_get_absolute_url(self):
        """Test Resonance (nested namespace) generates correct absolute URL."""
        url = self.resonance.get_absolute_url()
        self.assertEqual(url, f"/characters/mage/resonances/{self.resonance.pk}/")

    def test_resonance_get_update_url(self):
        """Test Resonance (nested namespace) generates correct update URL."""
        url = self.resonance.get_update_url()
        self.assertEqual(url, f"/characters/mage/update/resonances/{self.resonance.pk}/")

    def test_resonance_get_creation_url(self):
        """Test Resonance (nested namespace) generates correct creation URL."""
        url = Resonance.get_creation_url()
        self.assertEqual(url, "/characters/mage/create/resonance/")


class TestURLMethodsMixinMRO(TestCase):
    """Test that URLMethodsMixin is correctly placed in MRO."""

    def test_archetype_has_mixin_in_mro(self):
        """Test that Archetype has URLMethodsMixin in its MRO."""
        self.assertTrue(issubclass(Archetype, URLMethodsMixin))

    def test_derangement_has_mixin_in_mro(self):
        """Test that Derangement has URLMethodsMixin in its MRO."""
        self.assertTrue(issubclass(Derangement, URLMethodsMixin))

    def test_resonance_has_mixin_in_mro(self):
        """Test that Resonance has URLMethodsMixin in its MRO."""
        self.assertTrue(issubclass(Resonance, URLMethodsMixin))

    def test_mixin_comes_before_model_in_archetype(self):
        """Test that URLMethodsMixin comes before Model in Archetype MRO."""
        from core.models import Model

        mro = Archetype.__mro__
        mixin_index = mro.index(URLMethodsMixin)
        model_index = mro.index(Model)

        self.assertLess(mixin_index, model_index)


class TestURLMethodsMixinClassAttributes(TestCase):
    """Test URLMethodsMixin class attribute configuration."""

    def test_archetype_url_namespace(self):
        """Test Archetype has correct url_namespace."""
        self.assertEqual(Archetype.url_namespace, "characters")

    def test_archetype_url_name(self):
        """Test Archetype has correct url_name."""
        self.assertEqual(Archetype.url_name, "archetype")

    def test_derangement_url_namespace(self):
        """Test Derangement has correct url_namespace."""
        self.assertEqual(Derangement.url_namespace, "characters")

    def test_derangement_url_name(self):
        """Test Derangement has correct url_name."""
        self.assertEqual(Derangement.url_name, "derangement")

    def test_resonance_url_namespace(self):
        """Test Resonance has correct nested url_namespace."""
        self.assertEqual(Resonance.url_namespace, "characters:mage")

    def test_resonance_url_name(self):
        """Test Resonance has correct url_name."""
        self.assertEqual(Resonance.url_name, "resonance")

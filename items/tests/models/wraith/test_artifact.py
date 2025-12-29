"""Tests for WraithArtifact model."""
from django.test import TestCase
from items.models.wraith.artifact import WraithArtifact


class TestWraithArtifact(TestCase):
    """Test WraithArtifact model methods."""

    def setUp(self):
        self.artifact = WraithArtifact.objects.create(
            name="Test Wraith Artifact",
            level=3,
            artifact_type="soulforged",
            material="soulsteel",
        )

    def test_save_sets_background_cost_to_level(self):
        """Test save() sets background_cost equal to level."""
        artifact = WraithArtifact.objects.create(name="Level Test", level=4)
        self.assertEqual(artifact.background_cost, 4)

    def test_set_level(self):
        """Test set_level sets level and background_cost."""
        result = self.artifact.set_level(5)
        self.assertTrue(result)
        self.assertEqual(self.artifact.level, 5)
        self.assertEqual(self.artifact.background_cost, 5)

    def test_has_level_true(self):
        """Test has_level returns True when level > 0."""
        self.assertTrue(self.artifact.has_level())

    def test_has_level_false(self):
        """Test has_level returns False when level is 0."""
        artifact = WraithArtifact.objects.create(name="No Level", level=0)
        self.assertFalse(artifact.has_level())


class TestWraithArtifactDefaults(TestCase):
    """Test WraithArtifact default values."""

    def test_level_default(self):
        """Test level defaults to 1."""
        artifact = WraithArtifact.objects.create(name="Default Level")
        self.assertEqual(artifact.level, 1)

    def test_artifact_type_default(self):
        """Test artifact_type defaults to soulforged."""
        artifact = WraithArtifact.objects.create(name="Default Type")
        self.assertEqual(artifact.artifact_type, "soulforged")

    def test_material_default(self):
        """Test material defaults to soulsteel."""
        artifact = WraithArtifact.objects.create(name="Default Material")
        self.assertEqual(artifact.material, "soulsteel")

    def test_corpus_default(self):
        """Test corpus defaults to 0."""
        artifact = WraithArtifact.objects.create(name="Default Corpus")
        self.assertEqual(artifact.corpus, 0)

    def test_pathos_cost_default(self):
        """Test pathos_cost defaults to 0."""
        artifact = WraithArtifact.objects.create(name="Default Pathos")
        self.assertEqual(artifact.pathos_cost, 0)


class TestWraithArtifactType(TestCase):
    """Test artifact type choices."""

    def test_artifact_type_choices(self):
        """Test artifact_type can be set to valid choices."""
        valid_types = ["soulforged", "skin", "spectre", "other"]
        for atype in valid_types:
            artifact = WraithArtifact.objects.create(name=f"{atype} artifact", artifact_type=atype)
            self.assertEqual(artifact.artifact_type, atype)


class TestWraithArtifactMaterial(TestCase):
    """Test material choices."""

    def test_material_choices(self):
        """Test material can be set to valid choices."""
        valid_materials = ["soulsteel", "stygian_steel", "necropolis_steel", "ash_iron", "labyrinthine_adamas"]
        for material in valid_materials:
            artifact = WraithArtifact.objects.create(name=f"{material} artifact", material=material)
            self.assertEqual(artifact.material, material)


class TestWraithArtifactUrls(TestCase):
    """Test URL methods for WraithArtifact."""

    def setUp(self):
        self.artifact = WraithArtifact.objects.create(name="URL Test Artifact")

    def test_get_update_url(self):
        """Test get_update_url generates correct URL."""
        url = self.artifact.get_update_url()
        self.assertIn(str(self.artifact.id), url)
        self.assertIn("artifact", url)

    def test_get_creation_url(self):
        """Test get_creation_url generates correct URL."""
        url = WraithArtifact.get_creation_url()
        self.assertIn("artifact", url)
        self.assertIn("create", url)

    def test_get_heading(self):
        """Test get_heading returns correct heading class."""
        self.assertEqual(self.artifact.get_heading(), "wto_heading")


class TestWraithArtifactDetailView(TestCase):
    """Test WraithArtifact detail view."""

    def setUp(self):
        self.artifact = WraithArtifact.objects.create(name="Test Artifact")
        self.url = self.artifact.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/wraith/artifact/detail.html")


class TestWraithArtifactCreateView(TestCase):
    """Test WraithArtifact create view."""

    def setUp(self):
        self.url = WraithArtifact.get_creation_url()

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/wraith/artifact/form.html")


class TestWraithArtifactUpdateView(TestCase):
    """Test WraithArtifact update view."""

    def setUp(self):
        self.artifact = WraithArtifact.objects.create(name="Test Artifact", description="Test")
        self.url = self.artifact.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/wraith/artifact/form.html")


class TestWraithArtifactProperties(TestCase):
    """Test WraithArtifact specific properties."""

    def test_type_is_artifact(self):
        """Test type is 'artifact'."""
        artifact = WraithArtifact.objects.create(name="Type Test")
        self.assertEqual(artifact.type, "artifact")

    def test_gameline_is_wto(self):
        """Test gameline is 'wto'."""
        artifact = WraithArtifact.objects.create(name="Gameline Test")
        self.assertEqual(artifact.gameline, "wto")

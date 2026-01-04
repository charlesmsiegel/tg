"""Tests to verify templates use tg-card classes instead of Bootstrap card classes."""

import re
from pathlib import Path

from django.test import SimpleTestCase


class TestSceneDetailTemplateTgCardClasses(SimpleTestCase):
    """Test that game/scene/detail.html uses tg-card instead of Bootstrap card classes."""

    def test_scene_detail_template_uses_tg_card_classes(self):
        """Verify scene detail template uses tg-card instead of Bootstrap card classes."""
        template_path = Path(__file__).parent.parent.parent / "templates/game/scene/detail.html"
        content = template_path.read_text()

        # Verify tg-card classes are used
        self.assertIn("tg-card", content)

        # Remove script tags from content before checking
        content_without_scripts = re.sub(
            r"<script[\s\S]*?</script>", "", content, flags=re.IGNORECASE
        )

        # Find Bootstrap card classes that are NOT tg-card
        # Look for 'card' as a standalone class (not tg-card, header-card, card-*, etc.)
        # Pattern: word boundary + card + word boundary, but not preceded by -
        bootstrap_card_matches = []
        for line in content_without_scripts.split("\n"):
            if 'class="' in line:
                # Extract class values
                class_match = re.search(r'class="([^"]*)"', line)
                if class_match:
                    classes = class_match.group(1).split()
                    for cls in classes:
                        # Check for Bootstrap card classes (card, card-body, card-header, etc.)
                        if cls == "card" or cls.startswith("card-"):
                            bootstrap_card_matches.append(f"Line: {line.strip()}")

        self.assertEqual(
            len(bootstrap_card_matches),
            0,
            f"Found Bootstrap card classes instead of tg-card in scene/detail.html:\n"
            + "\n".join(bootstrap_card_matches),
        )


class TestWonderFormTemplateTgCardClasses(SimpleTestCase):
    """Test that items/mage/wonder/form_include.html uses tg-card wrapper if needed."""

    def test_wonder_form_template_structure(self):
        """Verify wonder form template has a consistent wrapper structure.

        Note: The wonder form include is embedded in a parent template
        that provides the tg-card wrapper. The form include itself uses
        Bootstrap grid classes (row, col-sm) which are acceptable for
        form layout within a tg-card container.
        """
        template_path = (
            Path(__file__).parent.parent.parent.parent
            / "items/templates/items/mage/wonder/form_include.html"
        )
        content = template_path.read_text()

        # This template uses row/col-sm for layout, which is acceptable
        # within a tg-card container. The test verifies the template exists
        # and doesn't contain standalone Bootstrap card classes.

        # Remove script tags from content before checking
        content_without_scripts = re.sub(
            r"<script[\s\S]*?</script>", "", content, flags=re.IGNORECASE
        )

        # Find Bootstrap card classes
        bootstrap_card_matches = []
        for line in content_without_scripts.split("\n"):
            if 'class="' in line:
                # Extract class values
                class_match = re.search(r'class="([^"]*)"', line)
                if class_match:
                    classes = class_match.group(1).split()
                    for cls in classes:
                        # Check for Bootstrap card classes (card, card-body, card-header, etc.)
                        if cls == "card" or cls.startswith("card-"):
                            bootstrap_card_matches.append(f"Line: {line.strip()}")

        self.assertEqual(
            len(bootstrap_card_matches),
            0,
            f"Found Bootstrap card classes instead of tg-card in wonder/form_include.html:\n"
            + "\n".join(bootstrap_card_matches),
        )

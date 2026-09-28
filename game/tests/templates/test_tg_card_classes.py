"""Tests to verify templates use tg-card classes instead of Bootstrap card classes."""

import re
from pathlib import Path

from django.test import SimpleTestCase


class TestSceneDetailTemplateSpread(SimpleTestCase):
    """game/scene/detail.html is on the Spread shell: no Bootstrap or tg-card markup."""

    def test_scene_detail_template_uses_the_spread_shell(self):
        template_path = Path(__file__).parent.parent.parent / "templates/game/scene/detail.html"
        content = template_path.read_text()
        self.assertIn('{% extends "core/tl_base.html" %}', content)

        content_without_scripts = re.sub(
            r"<script[\s\S]*?</script>", "", content, flags=re.IGNORECASE
        )
        legacy = []
        for class_value in re.findall(r'class="([^"]*)"', content_without_scripts):
            for cls in class_value.split():
                if cls in {"card", "tg-card", "btn", "row"} or cls.startswith(("card-", "btn-", "col-")):
                    legacy.append(cls)
        self.assertEqual(legacy, [], "Legacy Bootstrap/tg-card classes in scene/detail.html")


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
            "Found Bootstrap card classes instead of tg-card in wonder/form_include.html:\n"
            + "\n".join(bootstrap_card_matches),
        )

"""Every fixture page renders: detail and edit pages of one object per concrete model,
every argument-free list page, the character index and the scene page.

``test_routed_templates`` proves each routed template exists and compiles; this test
renders them with real objects, so a template that fails only at render time (a bad
filter argument, a missing context variable used in a tag, a broken include chosen at
runtime) fails here. Pages listed in ``EXPECTED_ERRORS`` return 500 today because
their template was never written; each points at its ``KNOWN_MISSING`` entry.
"""

from django.test import TestCase

from core.tests.template_fixtures import fixture_pages, seed
from core.tests.test_routed_templates import KNOWN_MISSING

EXPECTED_ERRORS = {}


class TemplateRenderSmokeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fixtures = seed()
        cls.pages = fixture_pages(cls.fixtures)

    def test_expected_errors_are_known_missing_templates(self):
        for slug, template in EXPECTED_ERRORS.items():
            with self.subTest(slug=slug):
                self.assertIn(slug, self.pages)
                self.assertIn(template, KNOWN_MISSING)

    def test_fixture_set_covers_the_models(self):
        self.assertLessEqual(
            set(self.fixtures.skipped),
            {"characters.CharacterModel", "characters.Rote", "game.Journal"},
            "The fixture seeder can no longer build these models",
        )
        self.assertGreater(len(self.pages), 400)

    def test_every_fixture_page_renders(self):
        self.client.raise_request_exception = False
        self.client.force_login(self.fixtures.st)
        failures = {}
        for slug, url in sorted(self.pages.items()):
            response = self.client.get(url, follow=True)
            expected = 500 if slug in EXPECTED_ERRORS else 200
            if response.status_code != expected:
                failures[slug] = (url, response.status_code)
        self.assertEqual(failures, {})

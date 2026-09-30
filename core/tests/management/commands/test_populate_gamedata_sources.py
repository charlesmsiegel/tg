"""Guard: every source title in populate_db names a Book that 00_books.py loads.

``Model.add_source(title, page)`` looks the book up with ``Book.objects.get_or_create(
name=title)``, so a title that differs from the Book row by as little as a capital letter
creates a second, bare Book (no gameline, edition or URL) and cites that instead.
"""

import ast
from collections import Counter
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

POPULATE_DB = Path(settings.BASE_DIR) / "populate_db"

# Titles that do not say which edition they cite, so no Book can be chosen for them
# without the book in hand. Do not add to this list: fix the title instead.
AMBIGUOUS_TITLES = {
    "Tradition Book: Celestial Chorus",
    "Tradition Book: Euthanatos",
    "Tradition Book: Verbena",
}


def scan():
    """Return (Book names, Counter of cited titles) found in populate_db."""
    books, cited = set(), Counter()
    for path in sorted(POPULATE_DB.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text())):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            is_book_create = (
                isinstance(func, ast.Attribute)
                and func.attr == "get_or_create"
                and isinstance(func.value, ast.Attribute)
                and isinstance(func.value.value, ast.Name)
                and func.value.value.id == "Book"
            )
            for keyword in node.keywords:
                if not isinstance(keyword.value, ast.Constant):
                    continue
                if is_book_create and keyword.arg == "name":
                    books.add(keyword.value.value)
                elif keyword.arg == "source_book":
                    cited[keyword.value.value] += 1
            if (
                isinstance(func, ast.Attribute)
                and func.attr == "add_source"
                and node.args
                and isinstance(node.args[0], ast.Constant)
            ):
                cited[node.args[0].value] += 1
    return books, cited


class SourceTitlesMatchBooksTests(SimpleTestCase):
    def test_every_cited_title_is_a_book(self):
        books, cited = scan()
        self.assertGreater(len(books), 500)
        unknown = {
            title: count
            for title, count in cited.items()
            if title not in books and title not in AMBIGUOUS_TITLES
        }
        self.assertEqual(unknown, {}, "add_source titles with no matching Book name")

    def test_ambiguous_titles_are_still_cited(self):
        # Drop a title from AMBIGUOUS_TITLES once its citations are fixed.
        _books, cited = scan()
        self.assertEqual({title for title in AMBIGUOUS_TITLES if cited[title]}, AMBIGUOUS_TITLES)

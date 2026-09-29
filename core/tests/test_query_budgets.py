"""Query budgets for the pages whose templates used to run hidden queries.

Two kinds of check:

* **Ceilings** for every seeded character detail page (one per concrete character
  model, so every gameline and splat), the scene page and the character index,
  measured on the shared fixture set. Before Step 8 a human sheet cost 73 queries,
  Changeling and Kinfolk sheets 114-115 and the scene page 82. A page that needs more
  should get a reviewed ceiling change here, not a silent regression. (Fera and Drone
  sheets rose by 4-7 when they moved onto Spread: they used to render only the cover
  and now show the full human sheet plus Gifts, Rites and Fetishes. Every character cover
  also lists its book sources, one query; the Wraith sheet's Thorns section is one more.)
* **Scaling**: a sheet costs the same with more specialties, the scene page the same
  with more posts, and the character index and chronicle page the same with more
  grouped characters. These are the N+1 patterns the old templates had
  (``get_specialty`` per stat, ``post.character.owner.profile.is_st`` per post,
  ``group_set.first`` per character).

Polymorphic hydration costs one query per concrete type in a list, so scaling tests
add rows of types that are already present. Most of the scene page's remaining
queries are that hydration for its two character drop-downs (one per character type).
"""

from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from characters.models.core import CharacterModel
from characters.models.core.specialty import Specialty
from characters.models.vampire.vtmhuman import VtMHuman
from core.tests.template_fixtures import seed
from game.models import Post

# Queries per character detail page for the fixture storyteller, by model label.
SHEET_CEILINGS = {
    "characters.Ajaba": 57,
    "characters.Ananasi": 40,
    "characters.AutumnPerson": 31,
    "characters.Bastet": 36,
    "characters.Changeling": 33,
    "characters.Character": 66,
    "characters.Companion": 36,
    "characters.Corax": 36,
    "characters.CtDHuman": 33,
    "characters.Demon": 33,
    "characters.Drone": 31,
    "characters.DtFHuman": 31,
    "characters.Earthbound": 32,
    "characters.Fera": 36,
    "characters.Fomor": 34,
    "characters.Ghoul": 31,
    "characters.Grondr": 36,
    "characters.Gurahl": 36,
    "characters.HtRHuman": 31,
    "characters.Human": 33,
    "characters.Hunter": 31,
    "characters.Inanimae": 31,
    "characters.Kinfolk": 36,
    "characters.Kitsune": 36,
    "characters.Mage": 85,
    "characters.Mokole": 36,
    "characters.MtAHuman": 33,
    "characters.MtRHuman": 31,
    "characters.Mummy": 31,
    "characters.Nagah": 36,
    "characters.Nunnehi": 31,
    "characters.Nuwisha": 36,
    "characters.Ratkin": 36,
    "characters.Revenant": 31,
    "characters.Rokea": 36,
    "characters.Sorcerer": 36,
    "characters.SpiritCharacter": 29,
    "characters.Thrall": 32,
    "characters.Vampire": 31,
    "characters.VtMHuman": 33,
    "characters.Werewolf": 39,
    "characters.Wraith": 35,
    "characters.WtAHuman": 33,
    "characters.WtOHuman": 33,
}
SCENE_CEILING = 75
INDEX_CEILING = 56


class QueryBudgetTest(TestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        cls.fixtures = seed()

    def setUp(self):
        self.client.force_login(self.fixtures.st)

    def count(self, url):
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, url)
        return len(ctx.captured_queries)

    def characters(self):
        return {
            label: obj
            for label, obj in self.fixtures.objects.items()
            if isinstance(obj, CharacterModel)
        }

    def test_every_character_model_has_a_ceiling(self):
        self.assertEqual(set(self.characters()), set(SHEET_CEILINGS))

    def test_character_sheets_stay_within_their_ceilings(self):
        over = {}
        for label, character in sorted(self.characters().items()):
            queries = self.count(character.get_absolute_url())
            if queries > SHEET_CEILINGS[label]:
                over[label] = (queries, SHEET_CEILINGS[label])
        self.assertEqual(over, {}, "(queries, ceiling) per sheet over budget")

    def test_sheet_cost_does_not_grow_with_specialties(self):
        character = self.fixtures.objects["characters.VtMHuman"]
        before = self.count(character.get_absolute_url())
        for stat in ("brawl", "firearms", "occult", "wits", "athletics"):
            character.specialties.add(Specialty.objects.create(name=f"Extra {stat}", stat=stat))
        self.assertEqual(self.count(character.get_absolute_url()), before)

    def test_scene_page_within_ceiling(self):
        self.assertLessEqual(self.count(self.fixtures.scene.get_absolute_url()), SCENE_CEILING)

    def test_scene_cost_does_not_grow_with_posts(self):
        scene = self.fixtures.scene
        url = scene.get_absolute_url()
        authors = [post.character for post in scene.post_set.all()[:2]]

        def add_posts(number):
            for index in range(number):
                Post.objects.create(
                    scene=scene,
                    character=authors[index % 2],
                    display_name="More",
                    message=f"More {index}",
                )

        # The first visit pays one-off costs (the navigation counts it caches, the
        # reader's scene status row). Each measured visit follows new posts, so both
        # move the reader's marker once.
        self.count(url)
        add_posts(1)
        before = self.count(url)
        add_posts(10)
        self.assertEqual(self.count(url), before)

    def test_index_within_ceiling(self):
        self.assertLessEqual(self.count("/characters/index/"), INDEX_CEILING)

    def _add_grouped_vtm_humans(self, number):
        group = self.fixtures.objects["characters.Coterie"]
        for index in range(number):
            character = VtMHuman.objects.create(
                name=f"Grouped {index}",
                owner=self.fixtures.player,
                chronicle=self.fixtures.chronicle,
                status="App",
            )
            group.members.add(character)

    def test_index_cost_does_not_grow_with_grouped_characters(self):
        self._add_grouped_vtm_humans(1)
        before = self.count("/characters/index/")
        self._add_grouped_vtm_humans(5)
        self.assertEqual(self.count("/characters/index/"), before)

    def test_chronicle_cost_does_not_grow_with_grouped_characters(self):
        url = self.fixtures.chronicle.get_absolute_url()
        self._add_grouped_vtm_humans(1)
        before = self.count(url)
        self._add_grouped_vtm_humans(5)
        self.assertEqual(self.count(url), before)

"""Location create / edit pages render as Spread forms that submit every field they own."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core import MeritFlaw
from characters.models.mage.focus import Practice
from characters.models.mage.resonance import Resonance
from core.models import Number
from game.models import Chronicle, ObjectType
from locations.models.mage import Node, NodeMeritFlawRating, NodeResonanceRating
from locations.models.mage.library import Library
from locations.models.mage.reality_zone import RealityZone, ZoneRating
from locations.models.mage.sector import Sector
from locations.registry import registry
from locations.tests.views.mage.chantry_fixtures import submitted_values

LEGACY_MARKERS = ('class="tl-content tl-legacy"', "tg-card", 'class="row', 'class="col-')


class CreatePagesAreSpreadFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("form_staff", is_staff=True)
        Chronicle.objects.create(name="Form chronicle")
        self.client.force_login(self.user)

    def test_every_create_page_renders_outside_the_legacy_wrapper(self):
        for spec in registry:
            if "create" not in spec.actions:
                continue
            url = registry.url(spec.model, "create")
            with self.subTest(model=spec.model_label):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'class="tl-locform"')
                for marker in LEGACY_MARKERS:
                    self.assertNotContains(response, marker)


class EditRoundTripTest(TestCase):
    """Saving an unchanged edit page keeps what the page shows."""

    def setUp(self):
        self.user = User.objects.create_user("form_owner")
        self.client.force_login(self.user)

    def test_sector_edit_renders_and_keeps_every_field(self):
        sector = Sector.objects.create(
            name="Spy's Demise",
            owner=self.user,
            status="Un",
            access_level="restricted",
            approved_users="Virtual Adepts",
            power_rating=6,
            genre_theme="Film noir",
        )
        url = sector.get_update_url()
        data = submitted_values(self.client.get(url))
        for name in ("access_level", "power_rating", "genre_theme", "aro_density", "hazards"):
            self.assertIn(name, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        sector.refresh_from_db()
        self.assertEqual(sector.access_level, "restricted")
        self.assertEqual(sector.power_rating, 6)
        self.assertEqual(sector.genre_theme, "Film noir")

    def test_library_edit_keeps_its_books(self):
        library = Library.objects.create(name="Stacks", owner=self.user, status="Un", rank=1)
        self.assertIn("books", submitted_values(self.client.get(library.get_update_url())))

    def test_node_edit_updates_its_ratings_instead_of_copying_them(self):
        node = Node.objects.create(name="Grove", owner=self.user, status="Un", rank=1)
        node.reality_zone = RealityZone.objects.create(name="Grove")
        node.save()
        ZoneRating.objects.create(
            zone=node.reality_zone, practice=Practice.objects.create(name="Craftwork"), rating=1
        )
        ZoneRating.objects.create(
            zone=node.reality_zone, practice=Practice.objects.create(name="Hypertech"), rating=-1
        )
        NodeResonanceRating.objects.create(
            node=node, resonance=Resonance.objects.create(name="Verdant"), rating=1
        )
        node_type, _ = ObjectType.objects.get_or_create(
            name="node", defaults={"type": "loc", "gameline": "mta"}
        )
        merit = MeritFlaw.objects.create(name="Sacred Ground")
        merit.allowed_types.add(node_type)
        merit.ratings.add(Number.objects.create(value=1), Number.objects.create(value=2))
        NodeMeritFlawRating.objects.create(node=node, mf=merit, rating=1)
        url = node.get_update_url()
        page = self.client.get(url)
        for name in ("resonance-0-id", "merit_flaw-0-id", "reality_zone-0-id"):
            self.assertContains(page, f'name="{name}"')
        data = submitted_values(page)
        self.assertEqual(data["resonance-0-resonance"], ["Verdant"])
        self.assertEqual(data["merit_flaw-0-mf"], [str(merit.pk)])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            list(NodeResonanceRating.objects.filter(node=node).values_list("resonance__name")),
            [("Verdant",)],
        )
        self.assertEqual(
            list(NodeMeritFlawRating.objects.filter(node=node).values_list("mf", "rating")),
            [(merit.pk, 1)],
        )
        self.assertEqual(ZoneRating.objects.filter(zone=node.reality_zone).count(), 2)

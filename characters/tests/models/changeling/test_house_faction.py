from characters.models.changeling.house import House
from characters.models.changeling.house_faction import HouseFaction
from django.test import TestCase


class TestHouseFactionDetailView(TestCase):
    def setUp(self) -> None:
        self.faction = HouseFaction.objects.create(name="Test Faction")
        self.url = self.faction.get_absolute_url()

    def test_house_faction_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_house_faction_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/house_faction/detail.html")


class TestHouseFactionCreateView(TestCase):
    def setUp(self):
        self.house1 = House.objects.create(name="House 1")
        self.house2 = House.objects.create(name="House 2")
        self.valid_data = {
            "name": "Faction",
            "description": "Test",
            "houses": [self.house1.id, self.house2.id],
        }
        self.url = HouseFaction.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/house_faction/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(HouseFaction.objects.count(), 1)
        faction = HouseFaction.objects.first()
        self.assertEqual(faction.name, "Faction")
        # Check that the houses are associated with the faction
        self.house1.refresh_from_db()
        self.house2.refresh_from_db()
        self.assertIn(faction, self.house1.factions.all())
        self.assertIn(faction, self.house2.factions.all())


class TestHouseFactionUpdateView(TestCase):
    def setUp(self):
        self.faction = HouseFaction.objects.create(
            name="Test Faction",
            description="Test description",
        )
        self.house1 = House.objects.create(name="House 1")
        self.house2 = House.objects.create(name="House 2")
        self.house3 = House.objects.create(name="House 3")
        # Initially associate house1 with the faction
        self.house1.factions.add(self.faction)

        self.valid_data = {
            "name": "Faction Updated",
            "description": "Test",
            "houses": [self.house2.id, self.house3.id],
        }
        self.url = self.faction.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/house_faction/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.faction.refresh_from_db()
        self.assertEqual(self.faction.name, "Faction Updated")
        self.assertEqual(self.faction.description, "Test")
        # Check that the houses are updated correctly
        self.house1.refresh_from_db()
        self.house2.refresh_from_db()
        self.house3.refresh_from_db()
        # house1 should no longer have this faction
        self.assertNotIn(self.faction, self.house1.factions.all())
        # house2 and house3 should have this faction
        self.assertIn(self.faction, self.house2.factions.all())
        self.assertIn(self.faction, self.house3.factions.all())

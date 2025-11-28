from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.pack import Pack
from characters.models.werewolf.totem import Totem
from characters.tests.utils import werewolf_setup
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestPack(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        werewolf_setup()

    def test_pack_creation(self):
        pack = Pack.objects.create(name="Pack 1")
        pack.members.set(Werewolf.objects.all())
        pack.leader = Werewolf.objects.first()
        pack.save()
        self.assertEqual(pack.members.count(), 5)
        self.assertIsNotNone(pack.leader)

    def test_totem_total(self):
        p = Pack.objects.create(name="Pack")
        self.assertEqual(p.total_totem(), 0)
        for i in range(4):
            w = Werewolf.objects.create(name=f"Werewolf {i}", owner=self.player)
            w.totem = i + 1
            w.save()
            p.members.add(w)
            p.save()
        self.assertEqual(p.total_totem(), 10)

    def test_set_totem(self):
        pack = Pack.objects.create(name="Pack 1")
        t = Totem.objects.first()
        self.assertFalse(pack.has_totem())
        self.assertTrue(pack.set_totem(t))
        self.assertTrue(pack.has_totem())

    def test_has_totem(self):
        pack = Pack.objects.create(name="Pack 1")
        t = Totem.objects.first()
        self.assertFalse(pack.has_totem())
        pack.set_totem(t)
        self.assertTrue(pack.has_totem())

    def test_str(self):
        pack = Pack.objects.create(name="Pack 1")
        self.assertEqual(str(pack), "Pack 1")


class TestPackDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.pack = Pack.objects.create(name="Test Pack")

    def test_pack_detail_view_status_code(self):
        response = self.client.get(f"/characters/groups/{self.pack.id}/")
        self.assertEqual(response.status_code, 200)

    def test_pack_detail_view_templates(self):
        response = self.client.get(f"/characters/groups/{self.pack.id}/")
        self.assertTemplateUsed(response, "characters/werewolf/pack/detail.html")


class TestPackCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Pack",
            "description": "Test",
        }
        self.url = Pack.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/pack/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Pack.objects.count(), 1)
        self.assertEqual(Pack.objects.first().name, "Pack")


class TestPackUpdateView(TestCase):
    def setUp(self):
        self.pack = Pack.objects.create(
            name="Test Pack",
            description="Test description",
        )
        self.valid_data = {
            "name": "Pack Updated",
            "description": "Test",
        }
        self.url = self.pack.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/pack/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.pack.refresh_from_db()
        self.assertEqual(self.pack.name, "Pack Updated")
        self.assertEqual(self.pack.description, "Test")


class TestPackListView(TestCase):
    def setUp(self):
        self.pack1 = Pack.objects.create(name="Pack Alpha")
        self.pack2 = Pack.objects.create(name="Pack Beta")
        self.url = reverse("characters:werewolf:list:pack")

    def test_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/pack/list.html")

    def test_list_view_contains_packs(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Pack Alpha")
        self.assertContains(response, "Pack Beta")

    def test_list_view_ordering(self):
        response = self.client.get(self.url)
        packs = response.context["object_list"]
        self.assertEqual(list(packs), [self.pack1, self.pack2])

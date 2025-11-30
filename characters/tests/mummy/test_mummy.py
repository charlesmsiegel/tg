from characters.models.mummy.dynasty import Dynasty
from characters.models.mummy.mtr_human import MtRHuman
from characters.models.mummy.mummy import Mummy
from characters.models.mummy.mummy_title import MummyTitle
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestMummy(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.dynasty = Dynasty.objects.create(
            name="Test Dynasty", era="Old Kingdom", favored_hekau="Necromancy"
        )
        self.mummy = Mummy.objects.create(
            name="Test Mummy",
            owner=self.player,
            dynasty=self.dynasty,
            web="isis",
            sekhem=3,
        )

    def test_mummy_creation(self):
        self.assertEqual(self.mummy.name, "Test Mummy")
        self.assertEqual(self.mummy.gameline, "mtr")
        self.assertEqual(self.mummy.type, "mummy")
        self.assertEqual(self.mummy.dynasty, self.dynasty)
        self.assertEqual(self.mummy.web, "isis")

    def test_ka_auto_calculation(self):
        """Ka should auto-calculate as Sekhem * 10"""
        self.assertEqual(self.mummy.ka_rating, 30)  # 3 * 10
        self.mummy.sekhem = 5
        self.mummy.save()
        self.assertEqual(self.mummy.ka_rating, 50)  # 5 * 10

    def test_get_hekau(self):
        """Test getting non-zero Hekau paths"""
        self.mummy.alchemy = 2
        self.mummy.necromancy = 3
        self.mummy.ushabti = 1
        self.mummy.save()

        hekau = self.mummy.get_hekau()
        self.assertEqual(len(hekau), 3)
        self.assertEqual(hekau["Alchemy"], 2)
        self.assertEqual(hekau["Necromancy"], 3)
        self.assertEqual(hekau["Ushabti"], 1)

    def test_total_hekau(self):
        """Test total Hekau calculation"""
        self.mummy.alchemy = 2
        self.mummy.celestial = 1
        self.mummy.ushabti = 3
        self.mummy.save()

        self.assertEqual(self.mummy.total_hekau(), 6)

    def test_is_web_hekau(self):
        """Test checking if Hekau is favored for Web"""
        # Isis Web favors Ushabti
        self.assertTrue(self.mummy.is_web_hekau("ushabti"))
        self.assertFalse(self.mummy.is_web_hekau("necromancy"))
        self.assertFalse(self.mummy.is_web_hekau("judge"))

    def test_ba_spending(self):
        """Test Ba spending"""
        self.mummy.ba = 20
        self.mummy.save()

        result = self.mummy.spend_ba(5)
        self.assertTrue(result)
        self.assertEqual(self.mummy.ba, 15)

        result = self.mummy.spend_ba(100)  # More than available
        self.assertFalse(result)
        self.assertEqual(self.mummy.ba, 15)  # Unchanged

    def test_ba_regaining(self):
        """Test Ba regaining"""
        self.mummy.ba = 10
        self.mummy.ka_rating = 30
        self.mummy.save()

        self.mummy.regain_ba(5)
        self.assertEqual(self.mummy.ba, 15)

        self.mummy.regain_ba(100)  # More than max
        self.assertEqual(self.mummy.ba, 30)  # Capped at Ka

    def test_get_absolute_url(self):
        url = self.mummy.get_absolute_url()
        self.assertEqual(url, reverse("characters:mummy:mummy", args=[self.mummy.id]))


class TestMtRHuman(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.human = MtRHuman.objects.create(name="Test Human", owner=self.player)

    def test_mtrhuman_creation(self):
        self.assertEqual(self.human.name, "Test Human")
        self.assertEqual(self.human.gameline, "mtr")
        self.assertEqual(self.human.type, "mtr_human")

    def test_mtrhuman_abilities(self):
        """Test MtRHuman has correct ability lists"""
        self.assertIn("awareness", self.human.talents)
        self.assertIn("leadership", self.human.talents)
        self.assertIn("meditation", self.human.skills)
        self.assertIn("theology", self.human.knowledges)

    def test_mtrhuman_backgrounds(self):
        """Test MtRHuman has mummy-specific backgrounds"""
        self.assertIn("tomb", self.human.allowed_backgrounds)
        self.assertIn("remembrance", self.human.allowed_backgrounds)
        self.assertIn("amenti_companion", self.human.allowed_backgrounds)


class TestDynasty(TestCase):
    def setUp(self):
        self.dynasty = Dynasty.objects.create(
            name="Test Dynasty",
            era="Middle Kingdom",
            favored_hekau="Alchemy",
            description="A test dynasty",
        )

    def test_dynasty_creation(self):
        self.assertEqual(self.dynasty.name, "Test Dynasty")
        self.assertEqual(self.dynasty.era, "Middle Kingdom")
        self.assertEqual(self.dynasty.favored_hekau, "Alchemy")

    def test_dynasty_str(self):
        self.assertEqual(str(self.dynasty), "Test Dynasty")

    def test_dynasty_get_absolute_url(self):
        url = self.dynasty.get_absolute_url()
        self.assertEqual(url, reverse("characters:mummy:dynasty", args=[self.dynasty.id]))


class TestMummyTitle(TestCase):
    def setUp(self):
        self.title = MummyTitle.objects.create(
            name="Test Title", rank_level=3, description="A test title"
        )

    def test_title_creation(self):
        self.assertEqual(self.title.name, "Test Title")
        self.assertEqual(self.title.rank_level, 3)

    def test_title_str(self):
        self.assertEqual(str(self.title), "Test Title")

    def test_title_get_absolute_url(self):
        url = self.title.get_absolute_url()
        self.assertEqual(url, reverse("characters:mummy:title", args=[self.title.id]))


class TestMummyDetailView(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Player", password="password")
        self.mummy = Mummy.objects.create(name="Test Mummy", owner=self.player)
        self.url = self.mummy.get_absolute_url()

    def test_detail_view_status_code(self):
        # Owner can view their own character
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/mummy/detail.html")


class TestMtRHumanDetailView(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Player", password="password")
        self.human = MtRHuman.objects.create(name="Test MtRHuman", owner=self.player)
        self.url = self.human.get_absolute_url()

    def test_detail_view_status_code(self):
        # Owner can view their own character
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/mtrhuman/detail.html")


class TestDynastyDetailView(TestCase):
    def setUp(self):
        self.dynasty = Dynasty.objects.create(name="Test Dynasty")
        self.url = self.dynasty.get_absolute_url()

    def test_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/dynasty/detail.html")


class TestMummyTitleDetailView(TestCase):
    def setUp(self):
        self.title = MummyTitle.objects.create(name="Test Title")
        self.url = self.title.get_absolute_url()

    def test_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mummy/title/detail.html")

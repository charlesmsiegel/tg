from characters.costs import get_freebie_cost, get_xp_cost
from characters.models.mummy.dynasty import Dynasty
from characters.models.mummy.mtr_human import MtRHuman
from characters.models.mummy.mummy import Mummy
from characters.models.mummy.mummy_title import MummyTitle
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from game.models import Chronicle


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


class TestMummyUpdateView(TestCase):
    """Test the Mummy update view with permission checks."""

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.other_user = User.objects.create_user(username="other", password="password")
        self.st = User.objects.create_user(username="st", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.mummy = Mummy.objects.create(
            name="Test Mummy", owner=self.owner, chronicle=self.chronicle
        )
        self.url = reverse("characters:mummy:update:mummy", args=[self.mummy.id])

    def test_st_can_access_update_view(self):
        """ST should be able to access update view with full form."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Full form has 'name' field
        self.assertIn("name", response.context["form"].fields)

    def test_other_user_cannot_access(self):
        """Non-owner/non-ST should not be able to access update view."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class TestMtRHumanUpdateView(TestCase):
    """Test the MtRHuman update view with permission checks."""

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.st = User.objects.create_user(username="st", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.human = MtRHuman.objects.create(
            name="Test Human", owner=self.owner, chronicle=self.chronicle
        )
        self.url = reverse("characters:mummy:update:mtrhuman", args=[self.human.id])

    def test_st_can_access_update_view(self):
        """ST should be able to access update view with full form."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].fields)


class TestMummyListView(TestCase):
    """Test the Mummy list view URL routing."""

    def test_list_url_resolves(self):
        """List view URL should resolve correctly."""
        url = reverse("characters:mummy:list:mummy")
        self.assertEqual(url, "/characters/mummy/list/mummy/")


class TestMtRHumanListView(TestCase):
    """Test the MtRHuman list view URL routing."""

    def test_list_url_resolves(self):
        """List view URL should resolve correctly."""
        url = reverse("characters:mummy:list:mtrhuman")
        self.assertEqual(url, "/characters/mummy/list/mtrhuman/")


class TestMummyHekauMethods(TestCase):
    """Test Mummy Hekau magic system methods."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.mummy = Mummy.objects.create(
            name="Hekau Test Mummy",
            owner=self.player,
            web="isis",
            sekhem=3,
        )

    def test_get_hekau_empty(self):
        """get_hekau returns empty dict when no Hekau is learned."""
        hekau = self.mummy.get_hekau()
        self.assertEqual(hekau, {})

    def test_get_hekau_all_paths(self):
        """get_hekau returns all non-zero paths."""
        self.mummy.alchemy = 1
        self.mummy.celestial = 2
        self.mummy.effigy = 3
        self.mummy.necromancy = 4
        self.mummy.nomenclature = 5
        self.mummy.ushabti = 1
        self.mummy.judge = 2
        self.mummy.phoenix = 3
        self.mummy.vision = 4
        self.mummy.divination = 5
        self.mummy.save()

        hekau = self.mummy.get_hekau()
        self.assertEqual(len(hekau), 10)
        self.assertEqual(hekau["Alchemy"], 1)
        self.assertEqual(hekau["Celestial"], 2)
        self.assertEqual(hekau["Effigy"], 3)
        self.assertEqual(hekau["Necromancy"], 4)
        self.assertEqual(hekau["Nomenclature"], 5)
        self.assertEqual(hekau["Ushabti"], 1)
        self.assertEqual(hekau["Judge"], 2)
        self.assertEqual(hekau["Phoenix"], 3)
        self.assertEqual(hekau["Vision"], 4)
        self.assertEqual(hekau["Divination"], 5)

    def test_is_web_hekau_all_webs(self):
        """Test is_web_hekau for all web types."""
        # Test Isis - favors Ushabti
        self.mummy.web = "isis"
        self.assertTrue(self.mummy.is_web_hekau("ushabti"))
        self.assertFalse(self.mummy.is_web_hekau("judge"))

        # Test Osiris - favors Judge
        self.mummy.web = "osiris"
        self.assertTrue(self.mummy.is_web_hekau("judge"))
        self.assertFalse(self.mummy.is_web_hekau("ushabti"))

        # Test Horus - favors Phoenix
        self.mummy.web = "horus"
        self.assertTrue(self.mummy.is_web_hekau("phoenix"))
        self.assertFalse(self.mummy.is_web_hekau("judge"))

        # Test Ma'at - favors Vision
        self.mummy.web = "maat"
        self.assertTrue(self.mummy.is_web_hekau("vision"))
        self.assertFalse(self.mummy.is_web_hekau("phoenix"))

        # Test Thoth - favors Divination
        self.mummy.web = "thoth"
        self.assertTrue(self.mummy.is_web_hekau("divination"))
        self.assertFalse(self.mummy.is_web_hekau("vision"))

    def test_is_web_hekau_case_insensitive(self):
        """is_web_hekau should be case-insensitive."""
        self.mummy.web = "isis"
        self.assertTrue(self.mummy.is_web_hekau("USHABTI"))
        self.assertTrue(self.mummy.is_web_hekau("Ushabti"))
        self.assertTrue(self.mummy.is_web_hekau("ushabti"))

    def test_is_web_hekau_empty_web(self):
        """is_web_hekau with empty web returns False."""
        self.mummy.web = ""
        self.assertFalse(self.mummy.is_web_hekau("ushabti"))

    def test_is_web_hekau_invalid_web(self):
        """is_web_hekau with invalid web returns False."""
        self.mummy.web = "invalid_web"
        self.assertFalse(self.mummy.is_web_hekau("ushabti"))

    def test_total_hekau_empty(self):
        """total_hekau returns 0 when no Hekau is learned."""
        self.assertEqual(self.mummy.total_hekau(), 0)

    def test_total_hekau_all_paths(self):
        """total_hekau sums all paths correctly."""
        self.mummy.alchemy = 1
        self.mummy.celestial = 1
        self.mummy.effigy = 1
        self.mummy.necromancy = 1
        self.mummy.nomenclature = 1
        self.mummy.ushabti = 1
        self.mummy.judge = 1
        self.mummy.phoenix = 1
        self.mummy.vision = 1
        self.mummy.divination = 1

        self.assertEqual(self.mummy.total_hekau(), 10)

    def test_has_hekau_false(self):
        """has_hekau returns False when no Hekau is learned."""
        self.assertFalse(self.mummy.has_hekau())

    def test_has_hekau_true(self):
        """has_hekau returns True when any Hekau is learned."""
        self.mummy.alchemy = 1
        self.assertTrue(self.mummy.has_hekau())


class TestMummyXPAndFreebieCosts(TestCase):
    """Test Mummy XP and freebie cost calculations."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.mummy = Mummy.objects.create(
            name="Cost Test Mummy",
            owner=self.player,
            web="isis",
            sekhem=3,
        )

    def test_xp_cost_favored_hekau(self):
        """Favored Hekau costs 4 XP per level."""
        cost = get_xp_cost("favored_hekau") * 1
        self.assertEqual(cost, 4)

        cost = get_xp_cost("favored_hekau") * 3
        self.assertEqual(cost, 12)

    def test_xp_cost_hekau(self):
        """Hekau (alias for favored) costs 5 XP per level."""
        cost = get_xp_cost("hekau") * 1
        self.assertEqual(cost, 5)

    def test_xp_cost_other_hekau(self):
        """Other Web's Hekau costs 6 XP per level."""
        cost = get_xp_cost("other_hekau") * 1
        self.assertEqual(cost, 6)

    def test_xp_cost_new_hekau(self):
        """New Hekau path costs 7 XP flat."""
        cost = get_xp_cost("new_hekau")
        self.assertEqual(cost, 7)

    def test_xp_cost_sekhem(self):
        """Sekhem costs 10 XP per level."""
        cost = get_xp_cost("sekhem") * 1
        self.assertEqual(cost, 10)

    def test_xp_cost_balance(self):
        """Balance costs 7 XP per level."""
        cost = get_xp_cost("balance") * 1
        self.assertEqual(cost, 7)

    def test_xp_cost_virtue(self):
        """Virtue costs 2 XP per level."""
        cost = get_xp_cost("virtue") * 1
        self.assertEqual(cost, 2)

    def test_freebie_cost_hekau(self):
        """Hekau costs 5 freebies."""
        cost = get_freebie_cost("hekau")
        self.assertEqual(cost, 5)

    def test_freebie_cost_sekhem(self):
        """Sekhem costs 1 freebie."""
        cost = get_freebie_cost("sekhem")
        self.assertEqual(cost, 1)

    def test_freebie_cost_balance(self):
        """Balance costs 4 freebies."""
        cost = get_freebie_cost("balance")
        self.assertEqual(cost, 4)

    def test_freebie_cost_virtue(self):
        """Virtue costs 2 freebies."""
        cost = get_freebie_cost("virtue")
        self.assertEqual(cost, 2)

    def test_freebie_cost_ba(self):
        """Ba costs 1 freebie per point."""
        cost = get_freebie_cost("ba")
        self.assertEqual(cost, 1)


class TestMummyBaMethods(TestCase):
    """Test Mummy Ba spending and regaining methods."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.mummy = Mummy.objects.create(
            name="Ba Test Mummy",
            owner=self.player,
            web="isis",
            sekhem=3,
            ba=20,
        )

    def test_spend_ba_exact_amount(self):
        """Can spend exactly the amount of Ba available."""
        self.mummy.ba = 10
        self.mummy.save()

        result = self.mummy.spend_ba(10)
        self.assertTrue(result)
        self.assertEqual(self.mummy.ba, 0)

    def test_spend_ba_zero(self):
        """Spending 0 Ba is allowed."""
        result = self.mummy.spend_ba(0)
        self.assertTrue(result)
        self.assertEqual(self.mummy.ba, 20)

    def test_regain_ba_zero(self):
        """Regaining 0 Ba leaves Ba unchanged."""
        initial_ba = self.mummy.ba
        self.mummy.regain_ba(0)
        self.assertEqual(self.mummy.ba, initial_ba)

    def test_regain_ba_at_max(self):
        """Regaining Ba when already at max does nothing."""
        self.mummy.ba = self.mummy.ka_rating
        self.mummy.save()

        self.mummy.regain_ba(10)
        self.assertEqual(self.mummy.ba, self.mummy.ka_rating)


class TestMummyURLMethods(TestCase):
    """Test Mummy URL generation methods."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.mummy = Mummy.objects.create(
            name="URL Test Mummy",
            owner=self.player,
        )

    def test_get_update_url(self):
        """get_update_url returns correct URL."""
        url = self.mummy.get_update_url()
        expected = reverse("characters:mummy:update:mummy", kwargs={"pk": self.mummy.pk})
        self.assertEqual(url, expected)

    def test_get_creation_url(self):
        """get_creation_url returns correct URL."""
        url = Mummy.get_creation_url()
        expected = reverse("characters:mummy:create:mummy")
        self.assertEqual(url, expected)

    def test_get_heading(self):
        """get_heading returns mtr_heading."""
        heading = self.mummy.get_heading()
        self.assertEqual(heading, "mtr_heading")


class TestMummyDefaults(TestCase):
    """Test Mummy default values."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.mummy = Mummy.objects.create(
            name="Default Test Mummy",
            owner=self.player,
        )

    def test_default_balance(self):
        """Default balance is 5."""
        self.assertEqual(self.mummy.balance, 5)

    def test_default_sekhem(self):
        """Default sekhem is 1."""
        self.assertEqual(self.mummy.sekhem, 1)

    def test_default_ba(self):
        """Default ba is 10."""
        self.assertEqual(self.mummy.ba, 10)

    def test_default_conviction(self):
        """Default conviction is 1."""
        self.assertEqual(self.mummy.conviction, 1)

    def test_default_restraint(self):
        """Default restraint is 1."""
        self.assertEqual(self.mummy.restraint, 1)

    def test_default_incarnation(self):
        """Default incarnation is 1."""
        self.assertEqual(self.mummy.incarnation, 1)

    def test_default_years_since_rebirth(self):
        """Default years since rebirth is 0."""
        self.assertEqual(self.mummy.years_since_rebirth, 0)

    def test_default_mummified_appearance(self):
        """Default mummified appearance is 'preserved'."""
        self.assertEqual(self.mummy.mummified_appearance, "preserved")

    def test_default_can_pass_as_mortal(self):
        """Default can_pass_as_mortal is True."""
        self.assertTrue(self.mummy.can_pass_as_mortal)

    def test_default_hekau_values(self):
        """All Hekau paths default to 0."""
        self.assertEqual(self.mummy.alchemy, 0)
        self.assertEqual(self.mummy.celestial, 0)
        self.assertEqual(self.mummy.effigy, 0)
        self.assertEqual(self.mummy.necromancy, 0)
        self.assertEqual(self.mummy.nomenclature, 0)
        self.assertEqual(self.mummy.ushabti, 0)
        self.assertEqual(self.mummy.judge, 0)
        self.assertEqual(self.mummy.phoenix, 0)
        self.assertEqual(self.mummy.vision, 0)
        self.assertEqual(self.mummy.divination, 0)


class TestMummyRelationships(TestCase):
    """Test Mummy relationship fields."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.dynasty = Dynasty.objects.create(
            name="Test Dynasty",
            era="Old Kingdom",
        )
        self.mentor = Mummy.objects.create(
            name="Mentor Mummy",
            owner=self.player,
        )
        self.title = MummyTitle.objects.create(
            name="High Priest",
            rank_level=5,
        )

    def test_dynasty_relationship(self):
        """Mummy can have a dynasty."""
        mummy = Mummy.objects.create(
            name="Dynasty Mummy",
            owner=self.player,
            dynasty=self.dynasty,
        )
        self.assertEqual(mummy.dynasty, self.dynasty)

    def test_mentor_relationship(self):
        """Mummy can have a mentor mummy."""
        student = Mummy.objects.create(
            name="Student Mummy",
            owner=self.player,
            mentor_mummy=self.mentor,
        )
        self.assertEqual(student.mentor_mummy, self.mentor)
        self.assertIn(student, self.mentor.students.all())

    def test_titles_relationship(self):
        """Mummy can have multiple titles."""
        mummy = Mummy.objects.create(
            name="Titled Mummy",
            owner=self.player,
        )
        mummy.titles.add(self.title)
        self.assertIn(self.title, mummy.titles.all())

    def test_dynasty_null_on_delete(self):
        """Deleting dynasty sets mummy's dynasty to null."""
        mummy = Mummy.objects.create(
            name="Dynasty Mummy",
            owner=self.player,
            dynasty=self.dynasty,
        )
        dynasty_id = self.dynasty.id
        self.dynasty.delete()
        mummy.refresh_from_db()
        self.assertIsNone(mummy.dynasty)

    def test_mentor_null_on_delete(self):
        """Deleting mentor mummy sets student's mentor to null."""
        student = Mummy.objects.create(
            name="Student Mummy",
            owner=self.player,
            mentor_mummy=self.mentor,
        )
        self.mentor.delete()
        student.refresh_from_db()
        self.assertIsNone(student.mentor_mummy)


class TestDynastyURLMethods(TestCase):
    """Test Dynasty URL generation methods."""

    def setUp(self):
        self.dynasty = Dynasty.objects.create(
            name="URL Test Dynasty",
            era="Old Kingdom",
        )

    def test_get_update_url(self):
        """get_update_url returns correct URL."""
        url = self.dynasty.get_update_url()
        expected = reverse("characters:mummy:update:dynasty", kwargs={"pk": self.dynasty.pk})
        self.assertEqual(url, expected)

    def test_get_creation_url(self):
        """get_creation_url returns correct URL."""
        url = Dynasty.get_creation_url()
        expected = reverse("characters:mummy:create:dynasty")
        self.assertEqual(url, expected)


class TestMummyTitleURLMethods(TestCase):
    """Test MummyTitle URL generation methods."""

    def setUp(self):
        self.title = MummyTitle.objects.create(
            name="URL Test Title",
            rank_level=1,
        )

    def test_get_update_url(self):
        """get_update_url returns correct URL."""
        url = self.title.get_update_url()
        expected = reverse("characters:mummy:update:title", kwargs={"pk": self.title.pk})
        self.assertEqual(url, expected)

    def test_get_creation_url(self):
        """get_creation_url returns correct URL."""
        url = MummyTitle.get_creation_url()
        expected = reverse("characters:mummy:create:title")
        self.assertEqual(url, expected)


class TestMtRHumanURLMethods(TestCase):
    """Test MtRHuman URL generation methods."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.human = MtRHuman.objects.create(
            name="URL Test Human",
            owner=self.player,
        )

    def test_get_update_url(self):
        """get_update_url returns correct URL."""
        url = self.human.get_update_url()
        expected = reverse("characters:mummy:update:mtrhuman", kwargs={"pk": self.human.pk})
        self.assertEqual(url, expected)

    def test_get_creation_url(self):
        """get_creation_url returns correct URL."""
        url = MtRHuman.get_creation_url()
        expected = reverse("characters:mummy:create:mtrhuman")
        self.assertEqual(url, expected)

    def test_get_heading(self):
        """get_heading returns mtr_heading."""
        heading = self.human.get_heading()
        self.assertEqual(heading, "mtr_heading")


class TestMtRHumanAbilityLists(TestCase):
    """Test MtRHuman ability list configuration."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.human = MtRHuman.objects.create(
            name="Ability Test Human",
            owner=self.player,
        )

    def test_talents_list(self):
        """Verify talents list is complete."""
        expected_talents = [
            "alertness",
            "athletics",
            "brawl",
            "empathy",
            "expression",
            "intimidation",
            "streetwise",
            "subterfuge",
            "awareness",
            "leadership",
        ]
        for talent in expected_talents:
            self.assertIn(talent, self.human.talents)
        self.assertEqual(len(self.human.talents), 10)

    def test_skills_list(self):
        """Verify skills list is complete."""
        expected_skills = [
            "crafts",
            "drive",
            "etiquette",
            "firearms",
            "melee",
            "stealth",
            "animal_ken",
            "larceny",
            "meditation",
            "performance",
            "survival",
        ]
        for skill in expected_skills:
            self.assertIn(skill, self.human.skills)
        self.assertEqual(len(self.human.skills), 11)

    def test_knowledges_list(self):
        """Verify knowledges list is complete."""
        expected_knowledges = [
            "academics",
            "computer",
            "investigation",
            "medicine",
            "science",
            "enigmas",
            "law",
            "occult",
            "politics",
            "technology",
            "theology",
        ]
        for knowledge in expected_knowledges:
            self.assertIn(knowledge, self.human.knowledges)
        self.assertEqual(len(self.human.knowledges), 11)

    def test_allowed_backgrounds_list(self):
        """Verify allowed backgrounds list is complete."""
        expected_backgrounds = [
            "contacts",
            "mentor",
            "allies",
            "resources",
            "retainers",
            "cult",
            "tomb",
            "rank",
            "remembrance",
            "vessel",
            "artifact",
            "ka",
            "amenti_companion",
        ]
        for background in expected_backgrounds:
            self.assertIn(background, self.human.allowed_backgrounds)
        self.assertEqual(len(self.human.allowed_backgrounds), 13)


class TestMtRHumanDefaults(TestCase):
    """Test MtRHuman default values."""

    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.human = MtRHuman.objects.create(
            name="Default Test Human",
            owner=self.player,
        )

    def test_default_additional_talents(self):
        """Additional talents default to 0."""
        self.assertEqual(self.human.awareness, 0)
        self.assertEqual(self.human.leadership, 0)

    def test_default_additional_skills(self):
        """Additional skills default to 0."""
        self.assertEqual(self.human.animal_ken, 0)
        self.assertEqual(self.human.larceny, 0)
        self.assertEqual(self.human.meditation, 0)
        self.assertEqual(self.human.performance, 0)
        self.assertEqual(self.human.survival, 0)

    def test_default_additional_knowledges(self):
        """Additional knowledges default to 0."""
        self.assertEqual(self.human.enigmas, 0)
        self.assertEqual(self.human.law, 0)
        self.assertEqual(self.human.occult, 0)
        self.assertEqual(self.human.politics, 0)
        self.assertEqual(self.human.technology, 0)
        self.assertEqual(self.human.theology, 0)

    def test_default_mummy_backgrounds(self):
        """Mummy-specific backgrounds default to 0."""
        self.assertEqual(self.human.allies, 0)
        self.assertEqual(self.human.resources, 0)
        self.assertEqual(self.human.retainers, 0)
        self.assertEqual(self.human.tomb, 0)
        self.assertEqual(self.human.rank, 0)
        self.assertEqual(self.human.remembrance, 0)
        self.assertEqual(self.human.vessel, 0)
        self.assertEqual(self.human.artifact, 0)
        self.assertEqual(self.human.ka, 0)
        self.assertEqual(self.human.amenti_companion, 0)

    def test_freebie_step(self):
        """MtRHuman freebie_step is 5."""
        self.assertEqual(self.human.freebie_step, 5)

    def test_mummy_freebie_step(self):
        """Mummy freebie_step is 7."""
        mummy = Mummy.objects.create(
            name="Freebie Test Mummy",
            owner=self.player,
        )
        self.assertEqual(mummy.freebie_step, 7)

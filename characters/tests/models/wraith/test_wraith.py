"""Tests for Wraith model."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.costs import get_freebie_cost, get_xp_cost
from characters.models.wraith.faction import WraithFaction
from characters.models.wraith.fetter import Fetter
from characters.models.wraith.guild import Guild
from characters.models.wraith.passion import Passion
from characters.models.wraith.shadow_archetype import ShadowArchetype
from characters.models.wraith.thorn import Thorn
from characters.models.wraith.wraith import ThornRating, Wraith


class WraithTestCase(TestCase):
    """Base test case with common setup for Wraith tests."""

    def setUp(self):
        """Create test user and wraith."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.wraith = Wraith.objects.create(name="Test Wraith", owner=self.user)


class TestWraithCreation(WraithTestCase):
    """Tests for basic Wraith creation and default values."""

    def test_wraith_creation(self):
        """Wraith can be created with a name and owner."""
        self.assertEqual(self.wraith.name, "Test Wraith")
        self.assertEqual(self.wraith.owner, self.user)

    def test_wraith_default_corpus(self):
        """Wraith has default corpus of 10."""
        self.assertEqual(self.wraith.corpus, 10)

    def test_wraith_default_pathos(self):
        """Wraith has default pathos of 5."""
        self.assertEqual(self.wraith.pathos, 5)
        self.assertEqual(self.wraith.temporary_pathos, 5)

    def test_wraith_default_angst(self):
        """Wraith has default angst of 1 (all wraiths have a Shadow)."""
        self.assertEqual(self.wraith.angst, 1)
        self.assertEqual(self.wraith.temporary_angst, 1)

    def test_wraith_default_character_type(self):
        """Wraith has default character type of wraith."""
        self.assertEqual(self.wraith.character_type, "wraith")

    def test_wraith_default_catharsis_state(self):
        """Wraith has default catharsis state."""
        self.assertFalse(self.wraith.in_catharsis)
        self.assertEqual(self.wraith.catharsis_count, 0)

    def test_wraith_default_harrowing_state(self):
        """Wraith has default harrowing state."""
        self.assertEqual(self.wraith.harrowing_count, 0)
        self.assertEqual(self.wraith.last_harrowing_result, "none")

    def test_wraith_type_attribute(self):
        """Wraith has correct type attribute."""
        self.assertEqual(self.wraith.type, "wraith")

    def test_wraith_freebie_step(self):
        """Wraith has correct freebie step."""
        self.assertEqual(self.wraith.freebie_step, 7)

    def test_wraith_background_points(self):
        """Wraith has correct background points."""
        self.assertEqual(self.wraith.background_points, 7)

    def test_wraith_passion_points(self):
        """Wraith has correct passion points."""
        self.assertEqual(self.wraith.passion_points, 10)

    def test_wraith_fetter_points(self):
        """Wraith has correct fetter points."""
        self.assertEqual(self.wraith.fetter_points, 10)


class TestWraithUrls(WraithTestCase):
    """Tests for Wraith URL methods."""

    def test_get_absolute_url(self):
        """Wraith returns correct absolute URL."""
        url = self.wraith.get_absolute_url()
        self.assertIn(str(self.wraith.pk), url)
        self.assertIn("wraith", url)

    def test_get_heading(self):
        """Wraith returns correct heading class."""
        self.assertEqual(self.wraith.get_heading(), "wto_heading")


class TestWraithGuild(WraithTestCase):
    """Tests for Wraith guild methods."""

    def setUp(self):
        super().setUp()
        self.guild = Guild.objects.create(
            name="Masquers",
            guild_type="greater",
            willpower=6,
        )

    def test_has_guild_returns_false_when_none(self):
        """has_guild returns False when no guild set."""
        self.assertFalse(self.wraith.has_guild())

    def test_has_guild_returns_true_when_set(self):
        """has_guild returns True when guild is set."""
        self.wraith.guild = self.guild
        self.wraith.save()
        self.assertTrue(self.wraith.has_guild())

    def test_set_guild_assigns_guild(self):
        """set_guild assigns guild to wraith."""
        result = self.wraith.set_guild(self.guild)
        self.assertTrue(result)
        self.assertEqual(self.wraith.guild, self.guild)

    def test_set_guild_sets_willpower(self):
        """set_guild sets willpower from guild."""
        self.wraith.set_guild(self.guild)
        self.assertEqual(self.wraith.willpower, 6)

    def test_set_guild_with_none(self):
        """set_guild can clear guild by passing None."""
        self.wraith.set_guild(self.guild)
        result = self.wraith.set_guild(None)
        self.assertTrue(result)
        self.assertIsNone(self.wraith.guild)


class TestWraithLegion(WraithTestCase):
    """Tests for Wraith legion methods."""

    def setUp(self):
        super().setUp()
        self.legion = WraithFaction.objects.create(
            name="Iron Legion",
            faction_type="legion",
        )

    def test_has_legion_returns_false_when_none(self):
        """has_legion returns False when no legion set."""
        self.assertFalse(self.wraith.has_legion())

    def test_has_legion_returns_true_when_set(self):
        """has_legion returns True when legion is set."""
        self.wraith.legion = self.legion
        self.wraith.save()
        self.assertTrue(self.wraith.has_legion())

    def test_set_legion_assigns_legion(self):
        """set_legion assigns legion to wraith."""
        result = self.wraith.set_legion(self.legion)
        self.assertTrue(result)
        self.assertEqual(self.wraith.legion, self.legion)


class TestWraithFaction(WraithTestCase):
    """Tests for Wraith faction methods."""

    def setUp(self):
        super().setUp()
        self.faction = WraithFaction.objects.create(
            name="Renegades",
            faction_type="other",
        )

    def test_has_faction_returns_false_when_none(self):
        """has_faction returns False when no faction set."""
        self.assertFalse(self.wraith.has_faction())

    def test_has_faction_returns_true_when_set(self):
        """has_faction returns True when faction is set."""
        self.wraith.faction = self.faction
        self.wraith.save()
        self.assertTrue(self.wraith.has_faction())

    def test_set_faction_assigns_faction(self):
        """set_faction assigns faction to wraith."""
        result = self.wraith.set_faction(self.faction)
        self.assertTrue(result)
        self.assertEqual(self.wraith.faction, self.faction)


class TestWraithArcanoi(WraithTestCase):
    """Tests for Wraith arcanoi methods."""

    def test_get_arcanoi_returns_dict(self):
        """get_arcanoi returns dictionary of arcanoi."""
        arcanoi = self.wraith.get_arcanoi()
        self.assertIsInstance(arcanoi, dict)
        self.assertIn("argos", arcanoi)
        self.assertIn("castigate", arcanoi)
        self.assertIn("embody", arcanoi)
        self.assertIn("fatalism", arcanoi)
        self.assertIn("flux", arcanoi)
        self.assertIn("inhabit", arcanoi)
        self.assertIn("keening", arcanoi)
        self.assertIn("lifeweb", arcanoi)
        self.assertIn("moliate", arcanoi)
        self.assertIn("mnemosynis", arcanoi)
        self.assertIn("outrage", arcanoi)
        self.assertIn("pandemonium", arcanoi)
        self.assertIn("phantasm", arcanoi)
        self.assertIn("usury", arcanoi)
        self.assertIn("intimation", arcanoi)

    def test_get_arcanoi_values(self):
        """get_arcanoi returns correct values."""
        self.wraith.argos = 3
        self.wraith.castigate = 2
        self.wraith.save()

        arcanoi = self.wraith.get_arcanoi()
        self.assertEqual(arcanoi["argos"], 3)
        self.assertEqual(arcanoi["castigate"], 2)
        self.assertEqual(arcanoi["embody"], 0)

    def test_get_dark_arcanoi(self):
        """get_dark_arcanoi returns dark arcanoi dictionary."""
        dark_arcanoi = self.wraith.get_dark_arcanoi()
        self.assertIsInstance(dark_arcanoi, dict)
        self.assertIn("blighted_insight", dark_arcanoi)
        self.assertIn("collogue", dark_arcanoi)
        self.assertIn("corruptor", dark_arcanoi)
        self.assertIn("false_life", dark_arcanoi)
        self.assertIn("tempestos", dark_arcanoi)
        self.assertIn("osseum", dark_arcanoi)
        self.assertIn("connaissance", dark_arcanoi)

    def test_total_arcanoi(self):
        """total_arcanoi returns sum of all arcanoi."""
        self.assertEqual(self.wraith.total_arcanoi(), 0)
        self.wraith.argos = 2
        self.wraith.castigate = 3
        self.assertEqual(self.wraith.total_arcanoi(), 5)

    def test_total_dark_arcanoi(self):
        """total_dark_arcanoi returns sum of dark arcanoi."""
        self.assertEqual(self.wraith.total_dark_arcanoi(), 0)
        self.wraith.blighted_insight = 2
        self.wraith.tempestos = 1
        self.assertEqual(self.wraith.total_dark_arcanoi(), 3)

    def test_add_arcanos_increases_value(self):
        """add_arcanos increases arcanos value by 1."""
        self.assertEqual(self.wraith.argos, 0)
        result = self.wraith.add_arcanos("argos")
        self.assertTrue(result)
        self.assertEqual(self.wraith.argos, 1)

    def test_add_arcanos_up_to_max(self):
        """add_arcanos works up to maximum of 5."""
        for i in range(5):
            result = self.wraith.add_arcanos("argos")
            self.assertTrue(result)
        self.assertEqual(self.wraith.argos, 5)
        # Cannot exceed 5
        result = self.wraith.add_arcanos("argos")
        self.assertFalse(result)
        self.assertEqual(self.wraith.argos, 5)

    def test_filter_arcanoi_all(self):
        """filter_arcanoi returns all arcanoi when no constraints."""
        filtered = self.wraith.filter_arcanoi()
        self.assertEqual(len(filtered), 15)

    def test_filter_arcanoi_by_maximum(self):
        """filter_arcanoi filters by maximum."""
        self.wraith.argos = 3
        self.wraith.castigate = 5
        self.wraith.save()

        filtered = self.wraith.filter_arcanoi(maximum=3)
        self.assertEqual(len(filtered), 14)  # All except castigate
        self.assertNotIn("castigate", filtered)

    def test_filter_arcanoi_by_minimum(self):
        """filter_arcanoi filters by minimum."""
        self.wraith.argos = 3
        self.wraith.castigate = 2
        self.wraith.save()

        filtered = self.wraith.filter_arcanoi(minimum=2)
        self.assertEqual(len(filtered), 2)
        self.assertIn("argos", filtered)
        self.assertIn("castigate", filtered)

    def test_filter_arcanoi_by_range(self):
        """filter_arcanoi filters by range."""
        self.wraith.argos = 3
        self.wraith.castigate = 2
        self.wraith.embody = 1
        self.wraith.save()

        filtered = self.wraith.filter_arcanoi(minimum=2, maximum=3)
        self.assertEqual(len(filtered), 2)
        self.assertIn("argos", filtered)
        self.assertIn("castigate", filtered)

    def test_has_arcanoi_false_when_insufficient(self):
        """has_arcanoi returns False when total < 5."""
        self.assertFalse(self.wraith.has_arcanoi())
        self.wraith.argos = 2
        self.wraith.castigate = 2
        self.assertFalse(self.wraith.has_arcanoi())

    def test_has_arcanoi_true_when_sufficient(self):
        """has_arcanoi returns True when total == 5."""
        self.wraith.argos = 3
        self.wraith.castigate = 2
        self.assertTrue(self.wraith.has_arcanoi())


class TestWraithPassions(WraithTestCase):
    """Tests for Wraith passion methods."""

    def test_add_passion(self):
        """add_passion creates a passion for the wraith."""
        result = self.wraith.add_passion("Love", "Protect my sister", rating=3)
        self.assertTrue(result)
        self.assertEqual(Passion.objects.filter(wraith=self.wraith).count(), 1)

    def test_add_passion_with_rating(self):
        """add_passion creates passion with specified rating."""
        self.wraith.add_passion("Rage", "Avenge my murder", rating=4)
        passion = Passion.objects.get(wraith=self.wraith)
        self.assertEqual(passion.rating, 4)
        self.assertEqual(passion.emotion, "Rage")

    def test_add_dark_passion(self):
        """add_passion can create dark passions."""
        self.wraith.add_passion("Hatred", "Destroy all living", rating=2, is_dark=True)
        passion = Passion.objects.get(wraith=self.wraith)
        self.assertTrue(passion.is_dark_passion)

    def test_total_passion_rating(self):
        """total_passion_rating returns sum of all passion ratings."""
        self.assertEqual(self.wraith.total_passion_rating(), 0)
        self.wraith.add_passion("Love", "Family", rating=3)
        self.wraith.add_passion("Rage", "Murder", rating=4)
        self.assertEqual(self.wraith.total_passion_rating(), 7)

    def test_has_passions_false_when_insufficient(self):
        """has_passions returns False when total < 10."""
        self.assertFalse(self.wraith.has_passions())
        self.wraith.add_passion("Love", "Family", rating=5)
        self.assertFalse(self.wraith.has_passions())

    def test_has_passions_true_when_sufficient(self):
        """has_passions returns True when total == 10."""
        self.wraith.add_passion("Love", "Family", rating=5)
        self.wraith.add_passion("Rage", "Murder", rating=5)
        self.assertTrue(self.wraith.has_passions())


class TestWraithFetters(WraithTestCase):
    """Tests for Wraith fetter methods."""

    def test_add_fetter(self):
        """add_fetter creates a fetter for the wraith."""
        result = self.wraith.add_fetter("object", "My wedding ring", rating=3)
        self.assertTrue(result)
        self.assertEqual(Fetter.objects.filter(wraith=self.wraith).count(), 1)

    def test_add_fetter_with_type(self):
        """add_fetter creates fetter with specified type."""
        self.wraith.add_fetter("location", "The house where I died", rating=4)
        fetter = Fetter.objects.get(wraith=self.wraith)
        self.assertEqual(fetter.fetter_type, "location")
        self.assertEqual(fetter.rating, 4)

    def test_total_fetter_rating(self):
        """total_fetter_rating returns sum of all fetter ratings."""
        self.assertEqual(self.wraith.total_fetter_rating(), 0)
        self.wraith.add_fetter("object", "Ring", rating=3)
        self.wraith.add_fetter("person", "My daughter", rating=4)
        self.assertEqual(self.wraith.total_fetter_rating(), 7)

    def test_has_fetters_false_when_insufficient(self):
        """has_fetters returns False when total < 10."""
        self.assertFalse(self.wraith.has_fetters())
        self.wraith.add_fetter("object", "Ring", rating=5)
        self.assertFalse(self.wraith.has_fetters())

    def test_has_fetters_true_when_sufficient(self):
        """has_fetters returns True when total == 10."""
        self.wraith.add_fetter("object", "Ring", rating=5)
        self.wraith.add_fetter("person", "Daughter", rating=5)
        self.assertTrue(self.wraith.has_fetters())


class TestWraithShadow(WraithTestCase):
    """Tests for Wraith shadow archetype and thorn methods."""

    def setUp(self):
        super().setUp()
        self.shadow = ShadowArchetype.objects.create(
            name="The Director",
            point_cost=2,
            core_function="Controls through manipulation",
            modus_operandi="Uses guilt and obligation",
            dominance_behavior="Commands attention and obedience",
            effect_on_psyche="Creates feelings of inadequacy",
            strengths="Effective in social situations",
            weaknesses="Struggles with direct confrontation",
        )
        self.thorn = Thorn.objects.create(
            name="Shadow Call",
            point_cost=2,
            activation_cost="1 Angst",
            activation_trigger="When the Wraith experiences strong emotion",
            mechanical_description="The Shadow can speak through the Wraith",
            resistance_system="Willpower roll",
            duration="One scene",
            frequency_limitation="Once per session",
            limitations="Cannot be used in Harrowing",
        )

    def test_has_shadow_false_when_none(self):
        """has_shadow returns False when no archetype set."""
        self.assertFalse(self.wraith.has_shadow())

    def test_has_shadow_true_when_set(self):
        """has_shadow returns True when archetype is set."""
        self.wraith.shadow_archetype = self.shadow
        self.assertTrue(self.wraith.has_shadow())

    def test_set_shadow_archetype(self):
        """set_shadow_archetype assigns archetype to wraith."""
        result = self.wraith.set_shadow_archetype(self.shadow)
        self.assertTrue(result)
        self.assertEqual(self.wraith.shadow_archetype, self.shadow)

    def test_add_thorn_creates_rating(self):
        """add_thorn creates ThornRating for wraith."""
        result = self.wraith.add_thorn(self.thorn)
        self.assertTrue(result)
        self.assertTrue(ThornRating.objects.filter(wraith=self.wraith, thorn=self.thorn).exists())

    def test_add_thorn_sets_rating_to_one(self):
        """add_thorn sets rating to 1."""
        self.wraith.add_thorn(self.thorn)
        rating = ThornRating.objects.get(wraith=self.wraith, thorn=self.thorn)
        self.assertEqual(rating.rating, 1)

    def test_add_thorn_returns_false_if_already_added(self):
        """add_thorn returns False if thorn already at rating 1+."""
        self.wraith.add_thorn(self.thorn)
        result = self.wraith.add_thorn(self.thorn)
        self.assertFalse(result)


class TestWraithCorpusPathos(WraithTestCase):
    """Tests for Wraith corpus and pathos methods."""

    def test_add_corpus(self):
        """add_corpus increases corpus by 1."""
        self.assertEqual(self.wraith.corpus, 10)
        # Corpus is already at 10, so adding won't work
        result = self.wraith.add_corpus()
        self.assertFalse(result)

    def test_add_corpus_from_lower_value(self):
        """add_corpus can increase corpus when below 10."""
        self.wraith.corpus = 8
        self.wraith.save()
        result = self.wraith.add_corpus()
        self.assertTrue(result)
        self.assertEqual(self.wraith.corpus, 9)

    def test_add_pathos(self):
        """add_pathos increases pathos by 1."""
        self.assertEqual(self.wraith.pathos, 5)
        result = self.wraith.add_pathos()
        self.assertTrue(result)
        self.assertEqual(self.wraith.pathos, 6)

    def test_add_pathos_up_to_max(self):
        """add_pathos works up to maximum of 10."""
        self.wraith.pathos = 9
        self.wraith.save()
        result = self.wraith.add_pathos()
        self.assertTrue(result)
        self.assertEqual(self.wraith.pathos, 10)
        # Cannot exceed 10
        result = self.wraith.add_pathos()
        self.assertFalse(result)

    def test_add_angst(self):
        """add_angst increases angst by 1."""
        self.assertEqual(self.wraith.angst, 1)  # Default is now 1
        result = self.wraith.add_angst()
        self.assertTrue(result)
        self.assertEqual(self.wraith.angst, 2)

    def test_add_angst_up_to_max(self):
        """add_angst works up to maximum of 10."""
        self.wraith.angst = 9
        self.wraith.save()
        result = self.wraith.add_angst()
        self.assertTrue(result)
        self.assertEqual(self.wraith.angst, 10)
        # Cannot exceed 10
        result = self.wraith.add_angst()
        self.assertFalse(result)


class TestWraithHistory(WraithTestCase):
    """Tests for Wraith history methods."""

    def test_has_wraith_history_false_when_incomplete(self):
        """has_wraith_history returns False when history incomplete."""
        self.assertFalse(self.wraith.has_wraith_history())
        self.wraith.death_description = "Murdered by rival"
        self.assertFalse(self.wraith.has_wraith_history())
        self.wraith.death_description = ""
        self.wraith.age_at_death = 35
        self.assertFalse(self.wraith.has_wraith_history())

    def test_has_wraith_history_true_when_complete(self):
        """has_wraith_history returns True when history complete."""
        self.wraith.death_description = "Murdered by rival"
        self.wraith.age_at_death = 35
        self.assertTrue(self.wraith.has_wraith_history())


class TestWraithCatharsis(WraithTestCase):
    """Tests for Wraith catharsis mechanics."""

    def test_check_catharsis_trigger_false_when_angst_low(self):
        """check_catharsis_trigger returns False when temporary_angst <= willpower."""
        self.wraith.temporary_angst = 3
        self.wraith.willpower = 5
        self.assertFalse(self.wraith.check_catharsis_trigger())

    def test_check_catharsis_trigger_true_when_angst_high(self):
        """check_catharsis_trigger returns True when temporary_angst > willpower."""
        self.wraith.temporary_angst = 6
        self.wraith.willpower = 5
        self.assertTrue(self.wraith.check_catharsis_trigger())

    def test_trigger_catharsis_fails_when_conditions_not_met(self):
        """trigger_catharsis returns False when conditions not met."""
        self.wraith.temporary_angst = 3
        self.wraith.willpower = 5
        result = self.wraith.trigger_catharsis()
        self.assertFalse(result)
        self.assertFalse(self.wraith.in_catharsis)

    def test_trigger_catharsis_succeeds_when_conditions_met(self):
        """trigger_catharsis succeeds when temporary_angst > willpower."""
        self.wraith.temporary_angst = 6
        self.wraith.willpower = 5
        result = self.wraith.trigger_catharsis()
        self.assertTrue(result)
        self.assertTrue(self.wraith.in_catharsis)
        self.assertTrue(self.wraith.is_shadow_dominant)
        self.assertEqual(self.wraith.catharsis_count, 1)

    def test_resolve_catharsis_psyche_wins(self):
        """resolve_catharsis with shadow_won=False restores psyche."""
        self.wraith.temporary_angst = 6
        self.wraith.willpower = 5
        self.wraith.trigger_catharsis()

        result = self.wraith.resolve_catharsis(shadow_won=False)
        self.assertTrue(result)
        self.assertFalse(self.wraith.in_catharsis)
        self.assertFalse(self.wraith.is_shadow_dominant)

    def test_resolve_catharsis_shadow_wins(self):
        """resolve_catharsis with shadow_won=True keeps shadow dominant."""
        self.wraith.temporary_angst = 6
        self.wraith.willpower = 5
        self.wraith.trigger_catharsis()

        result = self.wraith.resolve_catharsis(shadow_won=True)
        self.assertTrue(result)
        self.assertFalse(self.wraith.in_catharsis)
        self.assertTrue(self.wraith.is_shadow_dominant)

    def test_get_catharsis_info(self):
        """get_catharsis_info returns correct state information."""
        self.wraith.temporary_angst = 6
        self.wraith.willpower = 5
        self.wraith.trigger_catharsis()

        info = self.wraith.get_catharsis_info()
        self.assertTrue(info["in_catharsis"])
        self.assertEqual(info["catharsis_count"], 1)
        self.assertTrue(info["shadow_dominant"])
        self.assertEqual(info["temporary_angst"], 6)
        self.assertEqual(info["willpower"], 5)


class TestWraithHarrowing(WraithTestCase):
    """Tests for Wraith harrowing mechanics."""

    def test_check_harrowing_trigger_empty_when_no_triggers(self):
        """check_harrowing_trigger returns empty list when no triggers."""
        # Add fetter to avoid "no_fetters" trigger
        self.wraith.add_fetter("object", "Ring", rating=3)
        triggers = self.wraith.check_harrowing_trigger()
        self.assertEqual(triggers, [])

    def test_check_harrowing_trigger_zero_willpower(self):
        """check_harrowing_trigger detects zero willpower."""
        self.wraith.willpower = 0
        triggers = self.wraith.check_harrowing_trigger()
        self.assertIn("zero_willpower", triggers)

    def test_check_harrowing_trigger_zero_corpus(self):
        """check_harrowing_trigger detects zero corpus."""
        self.wraith.corpus = 0
        triggers = self.wraith.check_harrowing_trigger()
        self.assertIn("zero_corpus", triggers)

    def test_check_harrowing_trigger_no_fetters(self):
        """check_harrowing_trigger detects no fetters."""
        triggers = self.wraith.check_harrowing_trigger()
        self.assertIn("no_fetters", triggers)

    def test_check_harrowing_trigger_max_angst(self):
        """check_harrowing_trigger detects max angst."""
        self.wraith.angst = 10
        triggers = self.wraith.check_harrowing_trigger()
        self.assertIn("max_angst", triggers)

    def test_check_harrowing_trigger_no_fetters_excluded_when_has_fetters(self):
        """check_harrowing_trigger excludes no_fetters when fetters exist."""
        self.wraith.add_fetter("object", "Ring", rating=3)
        triggers = self.wraith.check_harrowing_trigger()
        self.assertNotIn("no_fetters", triggers)

    def test_trigger_harrowing(self):
        """trigger_harrowing increments count and returns info."""
        result = self.wraith.trigger_harrowing(trigger_type="zero_willpower")
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["trigger"], "zero_willpower")
        self.assertIn("Harrowing #1", result["message"])

    def test_trigger_harrowing_increments_count(self):
        """trigger_harrowing increments harrowing count."""
        self.wraith.trigger_harrowing()
        self.wraith.trigger_harrowing()
        self.assertEqual(self.wraith.harrowing_count, 2)

    def test_resolve_harrowing_success(self):
        """resolve_harrowing with success result."""
        result = self.wraith.resolve_harrowing(result="success")
        self.assertTrue(result)
        self.assertEqual(self.wraith.last_harrowing_result, "success")

    def test_resolve_harrowing_catharsis(self):
        """resolve_harrowing with catharsis reduces angst."""
        self.wraith.angst = 5
        self.wraith.temporary_angst = 5
        result = self.wraith.resolve_harrowing(result="catharsis")
        self.assertTrue(result)
        self.assertEqual(self.wraith.last_harrowing_result, "catharsis")
        self.assertEqual(self.wraith.angst, 4)
        self.assertEqual(self.wraith.temporary_angst, 2)

    def test_resolve_harrowing_failure_becomes_spectre(self):
        """resolve_harrowing with failure transforms to spectre."""
        self.wraith.add_fetter("object", "Ring", rating=3)
        result = self.wraith.resolve_harrowing(result="failure")
        # become_spectre returns True when successful
        self.assertTrue(result)
        self.assertEqual(self.wraith.character_type, "spectre")

    def test_get_harrowing_info(self):
        """get_harrowing_info returns correct information."""
        self.wraith.trigger_harrowing()
        self.wraith.resolve_harrowing(result="success")

        info = self.wraith.get_harrowing_info()
        self.assertEqual(info["harrowing_count"], 1)
        self.assertEqual(info["last_result"], "success")


class TestWraithBecomeSpectre(WraithTestCase):
    """Tests for Wraith becoming a Spectre."""

    def test_become_spectre_changes_type(self):
        """become_spectre changes character type to spectre."""
        self.wraith.add_fetter("object", "Ring", rating=5)
        result = self.wraith.become_spectre()
        self.assertTrue(result)
        self.assertEqual(self.wraith.character_type, "spectre")

    def test_become_spectre_sets_shadow_dominant(self):
        """become_spectre sets is_shadow_dominant to True."""
        self.wraith.add_fetter("object", "Ring", rating=5)
        self.wraith.become_spectre()
        self.assertTrue(self.wraith.is_shadow_dominant)

    def test_become_spectre_sets_spectrehood_date(self):
        """become_spectre sets spectrehood_date."""
        self.wraith.add_fetter("object", "Ring", rating=5)
        self.wraith.become_spectre()
        self.assertIsNotNone(self.wraith.spectrehood_date)

    def test_become_spectre_converts_passions_to_dark(self):
        """become_spectre converts passions to dark passions."""
        self.wraith.add_passion("Love", "Family", rating=3)
        passion = Passion.objects.get(wraith=self.wraith)
        self.assertFalse(passion.is_dark_passion)

        self.wraith.become_spectre()
        passion.refresh_from_db()
        self.assertTrue(passion.is_dark_passion)

    def test_become_spectre_halves_fetter_ratings(self):
        """become_spectre halves fetter ratings."""
        self.wraith.add_fetter("object", "Ring", rating=4)
        fetter = Fetter.objects.get(wraith=self.wraith)
        self.assertEqual(fetter.rating, 4)

        self.wraith.become_spectre()
        fetter.refresh_from_db()
        self.assertEqual(fetter.rating, 2)

    def test_become_spectre_converts_eidolon_to_angst(self):
        """become_spectre converts eidolon to angst."""
        self.wraith.eidolon = 3
        self.wraith.angst = 2
        self.wraith.add_fetter("object", "Ring", rating=4)

        self.wraith.become_spectre()
        self.assertEqual(self.wraith.eidolon, 0)
        self.assertEqual(self.wraith.angst, 5)

    def test_become_spectre_returns_false_if_already_spectre(self):
        """become_spectre returns False if already a spectre."""
        self.wraith.character_type = "spectre"
        result = self.wraith.become_spectre()
        self.assertFalse(result)


class TestWraithRedemption(WraithTestCase):
    """Tests for Spectre redemption mechanics."""

    def setUp(self):
        super().setUp()
        self.wraith.add_fetter("object", "Ring", rating=5)
        self.wraith.become_spectre()

    def test_attempt_redemption_fails_if_not_spectre(self):
        """attempt_redemption fails if character is not a spectre."""
        wraith = Wraith.objects.create(name="Normal Wraith", owner=self.user)
        result = wraith.attempt_redemption()
        self.assertFalse(result["success"])
        self.assertIn("not a Spectre", result["message"])

    def test_attempt_redemption_fails_if_no_fetters(self):
        """attempt_redemption fails if no fetters remain."""
        Fetter.objects.filter(wraith=self.wraith).delete()
        result = self.wraith.attempt_redemption()
        self.assertFalse(result["success"])

    def test_attempt_redemption_fails_if_angst_too_high(self):
        """attempt_redemption fails if angst >= 10."""
        self.wraith.angst = 10
        result = self.wraith.attempt_redemption()
        self.assertFalse(result["success"])

    def test_attempt_redemption_succeeds_if_conditions_met(self):
        """attempt_redemption succeeds if conditions met."""
        self.wraith.angst = 5
        result = self.wraith.attempt_redemption()
        self.assertTrue(result["success"])
        self.assertTrue(result["can_attempt"])

    def test_attempt_redemption_increments_attempts(self):
        """attempt_redemption increments redemption_attempts."""
        self.wraith.angst = 5
        self.wraith.attempt_redemption()
        self.assertEqual(self.wraith.redemption_attempts, 1)

    def test_complete_redemption_success(self):
        """complete_redemption succeeds when psyche wins."""
        self.wraith.angst = 5
        self.wraith.add_passion("Hatred", "Destroy", rating=3, is_dark=True)

        result = self.wraith.complete_redemption(psyche_successes=5, shadow_successes=2)
        self.assertTrue(result["success"])
        self.assertEqual(self.wraith.character_type, "wraith")
        self.assertFalse(self.wraith.is_shadow_dominant)

    def test_complete_redemption_reduces_angst(self):
        """complete_redemption reduces angst on success."""
        self.wraith.angst = 5
        self.wraith.temporary_angst = 8

        result = self.wraith.complete_redemption(psyche_successes=5, shadow_successes=2)
        self.assertTrue(result["success"])
        self.assertEqual(self.wraith.angst, 2)  # Reduced by 3 (5-2)
        self.assertEqual(self.wraith.temporary_angst, 2)  # Reduced by 6 (3*2)

    def test_complete_redemption_failure(self):
        """complete_redemption fails when shadow wins."""
        result = self.wraith.complete_redemption(psyche_successes=2, shadow_successes=5)
        self.assertFalse(result["success"])
        self.assertEqual(self.wraith.character_type, "spectre")


class TestWraithXPCosts(WraithTestCase):
    """Tests for Wraith XP cost calculations."""

    def test_xp_cost_arcanos(self):
        """xp_cost returns correct cost for arcanoi."""
        cost = get_xp_cost("arcanos") * 3
        self.assertEqual(cost, 9)  # 3 * 3

    def test_xp_cost_pathos(self):
        """xp_cost returns correct cost for pathos."""
        cost = get_xp_cost("pathos") * 2
        self.assertEqual(cost, 4)  # 2 * 2

    def test_xp_cost_corpus(self):
        """xp_cost returns correct cost for corpus."""
        cost = get_xp_cost("corpus") * 3
        self.assertEqual(cost, 3)  # 1 * 3

    def test_xp_cost_angst(self):
        """xp_cost returns correct cost for angst."""
        cost = get_xp_cost("angst") * 4
        self.assertEqual(cost, 4)  # 1 * 4

    def test_xp_frequencies(self):
        """xp_frequencies returns correct distribution."""
        freq = self.wraith.xp_frequencies()
        self.assertEqual(freq["arcanos"], 37)
        self.assertEqual(freq["pathos"], 2)


class TestWraithFreebieCosts(WraithTestCase):
    """Tests for Wraith freebie cost calculations."""

    def test_freebie_cost_arcanos(self):
        """freebie_cost returns correct cost for arcanoi."""
        cost = get_freebie_cost("arcanos")
        self.assertEqual(cost, 5)

    def test_freebie_cost_pathos(self):
        """freebie_cost returns correct cost for pathos."""
        cost = get_freebie_cost("pathos")
        self.assertEqual(cost, 0.5)

    def test_freebie_cost_passion(self):
        """freebie_cost returns correct cost for passion."""
        cost = get_freebie_cost("passion")
        self.assertEqual(cost, 2)

    def test_freebie_cost_fetter(self):
        """freebie_cost returns correct cost for fetter."""
        cost = get_freebie_cost("fetter")
        self.assertEqual(cost, 1)

    def test_freebie_cost_wraith_willpower(self):
        """freebie_cost returns correct cost for wraith willpower."""
        cost = get_freebie_cost("wraith_willpower")
        self.assertEqual(cost, 2)

    def test_freebie_costs(self):
        """Test centralized freebie costs for wraith traits."""
        self.assertEqual(get_freebie_cost("arcanos"), 5)
        self.assertEqual(get_freebie_cost("pathos"), 0.5)
        self.assertEqual(get_freebie_cost("passion"), 2)
        self.assertEqual(get_freebie_cost("fetter"), 1)

    def test_freebie_frequencies(self):
        """freebie_frequencies returns correct distribution."""
        freq = self.wraith.freebie_frequencies()
        self.assertEqual(freq["arcanos"], 25)
        self.assertEqual(freq["pathos"], 5)
        self.assertEqual(freq["passion"], 5)
        self.assertEqual(freq["fetter"], 5)
        self.assertEqual(freq["corpus"], 5)


class TestWraithSpendXP(WraithTestCase):
    """Tests for Wraith XP spending."""

    def test_spend_xp_on_arcanos_insufficient_xp(self):
        """spend_xp fails when insufficient XP."""
        self.wraith.xp = 5
        self.wraith.argos = 1
        self.wraith.save()

        result = self.wraith.spend_xp("argos")
        self.assertFalse(result)
        self.assertEqual(self.wraith.argos, 1)


class TestWraithSpendFreebies(WraithTestCase):
    """Tests for Wraith freebie spending."""

    def test_spend_freebies_on_arcanos_insufficient(self):
        """spend_freebies fails when insufficient freebies."""
        self.wraith.freebies = 4  # Arcanos costs 5, so 4 is insufficient
        result = self.wraith.spend_freebies("argos")
        self.assertFalse(result)
        self.assertEqual(self.wraith.argos, 0)

    def test_spend_freebies_returns_trait_for_special_categories(self):
        """spend_freebies returns trait name for passion/fetter."""
        self.wraith.freebies = 10
        result = self.wraith.spend_freebies("passion")
        self.assertEqual(result, "passion")

        result = self.wraith.spend_freebies("fetter")
        self.assertEqual(result, "fetter")


class ThornRatingDeleteBehaviorTests(TestCase):
    """Tests for ThornRating SET_NULL behavior when parent objects are deleted."""

    def setUp(self):
        """Create test user, wraith, thorn, and rating."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.wraith = Wraith.objects.create(name="Test Wraith", owner=self.user)
        self.thorn = Thorn.objects.create(
            name="Shadow Call",
            point_cost=2,
            activation_cost="1 Angst",
            activation_trigger="When the Wraith experiences strong emotion",
            mechanical_description="The Shadow can speak through the Wraith",
            resistance_system="Willpower roll",
            duration="One scene",
            frequency_limitation="Once per session",
            limitations="Cannot be used in Harrowing",
        )
        self.rating = ThornRating.objects.create(wraith=self.wraith, thorn=self.thorn, rating=3)

    def test_deleting_wraith_sets_null_preserves_rating(self):
        """Deleting a Wraith should set wraith FK to NULL, not delete ThornRating."""
        rating_id = self.rating.id
        self.wraith.delete()

        # ThornRating should still exist
        self.assertTrue(ThornRating.objects.filter(id=rating_id).exists())

        # wraith FK should be NULL
        rating = ThornRating.objects.get(id=rating_id)
        self.assertIsNone(rating.wraith)
        self.assertEqual(rating.thorn, self.thorn)
        self.assertEqual(rating.rating, 3)

    def test_deleting_thorn_sets_null_preserves_rating(self):
        """Deleting a Thorn should set thorn FK to NULL, not delete ThornRating."""
        rating_id = self.rating.id
        self.thorn.delete()

        # ThornRating should still exist
        self.assertTrue(ThornRating.objects.filter(id=rating_id).exists())

        # thorn FK should be NULL
        rating = ThornRating.objects.get(id=rating_id)
        self.assertIsNone(rating.thorn)
        self.assertEqual(rating.wraith, self.wraith)
        self.assertEqual(rating.rating, 3)

    def test_related_name_thorn_ratings_on_wraith(self):
        """Wraith should have thorn_ratings related manager."""
        self.assertIn(self.rating, self.wraith.thorn_ratings.all())

    def test_related_name_wraith_ratings_on_thorn(self):
        """Thorn should have wraith_ratings related manager."""
        self.assertIn(self.rating, self.thorn.wraith_ratings.all())


class TestWraithAngstValidation(WraithTestCase):
    """Tests for Wraith angst minimum validation (issue #1366)."""

    def test_angst_minimum_validation_in_clean(self):
        """clean() raises ValidationError when angst is below 1."""
        from django.core.exceptions import ValidationError

        self.wraith.angst = 0
        with self.assertRaises(ValidationError) as context:
            self.wraith.clean()
        self.assertIn("angst", context.exception.message_dict)

    def test_angst_at_one_is_valid(self):
        """clean() passes when angst is exactly 1."""
        self.wraith.angst = 1
        # Should not raise
        self.wraith.clean()

    def test_resolve_harrowing_catharsis_respects_minimum(self):
        """resolve_harrowing with catharsis never reduces angst below 1."""
        self.wraith.angst = 1
        self.wraith.temporary_angst = 5
        result = self.wraith.resolve_harrowing(result="catharsis")
        self.assertTrue(result)
        # Angst should remain at 1, not drop to 0
        self.assertEqual(self.wraith.angst, 1)

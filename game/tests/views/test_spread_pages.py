"""View logic behind the Spread game pages: chronicle tabs, week navigation, covers."""

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from characters.models.core.human import Human
from core.models import HouseRule
from game.models import (
    Chronicle,
    Gameline,
    Journal,
    Story,
    STRelationship,
    Week,
    XPSpendingRequest,
)
from game.views import current_week


class ChronicleTabsTest(TestCase):
    def setUp(self):
        self.player = User.objects.create_user("tab_player", password="pw")
        self.other = User.objects.create_user("tab_other", password="pw")
        self.st = User.objects.create_user("tab_st", password="pw")
        self.chronicle = Chronicle.objects.create(name="Tabbed", head_st=self.st)
        STRelationship.objects.create(
            user=self.st, chronicle=self.chronicle, gameline=Gameline.objects.create(name="WoD")
        )
        Human.objects.create(name="Mine", owner=self.player, chronicle=self.chronicle)
        Human.objects.create(name="Gone", owner=self.player, chronicle=self.chronicle, status="Ret")
        Human.objects.create(name="Theirs", owner=self.other, chronicle=self.chronicle)
        self.url = self.chronicle.get_absolute_url()

    def get(self, user, query=""):
        self.client.force_login(user)
        return self.client.get(self.url + query)

    def test_overview_is_the_default_and_unknown_tabs_fall_back_to_it(self):
        for query in ("", "?tab=nonsense"):
            with self.subTest(query=query):
                response = self.get(self.player, query)
                self.assertEqual(response.context["tab"], "overview")
                self.assertContains(response, 'href="?tab=overview" aria-current="page"')

    def test_character_status_sub_tab_picks_the_list(self):
        response = self.get(self.player, "?tab=characters&status=retired")
        self.assertEqual(response.context["character_status"], "retired")
        self.assertContains(response, "Gone")
        self.assertNotContains(response, ">Mine<")

    def test_character_tab_keeps_permission_filtering(self):
        # Chronicle members who are not staff see only their own rows (chronicle_overview).
        for status in ("active", "retired", "deceased", "npc"):
            with self.subTest(status=status):
                response = self.get(self.player, f"?tab=characters&status={status}")
                self.assertNotContains(response, "Theirs")

    def test_unknown_line_falls_back_to_the_first_group(self):
        response = self.get(self.st, "?tab=characters&line=zzz")
        self.assertEqual(response.context["character_line"], "wod")

    def test_new_scene_needs_scene_rights(self):
        self.assertFalse(self.get(self.player).context["can_create_scene"])
        self.assertNotContains(self.get(self.player, "?tab=scenes"), 'id="new-scene"')
        response = self.get(self.st, "?tab=scenes&new=scene")
        self.assertTrue(response.context["can_create_scene"])
        self.assertContains(response, 'id="new-scene" open')

    def test_failed_story_create_reopens_the_stories_tab(self):
        self.client.force_login(self.st)
        response = self.client.post(
            reverse("game:chronicle_create_story", kwargs={"pk": self.chronicle.pk}), {"name": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tab"], "stories")
        self.assertContains(response, 'id="new-story" open')

    def test_cover_facts(self):
        Story.objects.create(name="Open story", chronicle=self.chronicle)
        HouseRule.objects.create(name="Rule", chronicle=self.chronicle)
        week = Week.objects.create(end_date=timezone.localdate() + timedelta(days=2))
        response = self.get(self.player)
        self.assertEqual(response.context["house_rule_count"], 1)
        self.assertEqual(response.context["current_week"], week)
        self.assertContains(response, "1 apply")
        self.assertContains(response, "Open story")


class CurrentWeekTest(TestCase):
    def test_week_whose_days_include_today(self):
        today = date(2026, 3, 10)
        Week.objects.create(end_date=today - timedelta(days=1))
        this_week = Week.objects.create(end_date=today + timedelta(days=7))
        Week.objects.create(end_date=today + timedelta(days=8))
        self.assertEqual(current_week(today), this_week)

    def test_none_when_no_week_covers_today(self):
        Week.objects.create(end_date=date(2020, 1, 1))
        self.assertIsNone(current_week(date(2026, 3, 10)))


class WeekNavigationTest(TestCase):
    def test_previous_and_next_weeks(self):
        user = User.objects.create_user("week_viewer", password="pw")
        first = Week.objects.create(end_date=date(2026, 1, 7))
        middle = Week.objects.create(end_date=date(2026, 1, 14))
        last = Week.objects.create(end_date=date(2026, 1, 21))
        self.client.force_login(user)
        response = self.client.get(middle.get_absolute_url())
        self.assertEqual(response.context["previous_week"], first)
        self.assertEqual(response.context["next_week"], last)
        self.assertContains(response, first.get_absolute_url())
        edge = self.client.get(last.get_absolute_url())
        self.assertIsNone(edge.context["next_week"])


class CharacterContextTest(TestCase):
    """Record pages get their character as its concrete class, for the line cover."""

    def setUp(self):
        self.owner = User.objects.create_user("record_owner", password="pw")
        self.character = Human.objects.create(name="Recorded", owner=self.owner)
        self.client.force_login(self.owner)

    def test_journal_and_spend_pages(self):
        journal = Journal.objects.get(character=self.character)
        spend = XPSpendingRequest.objects.create(
            character=self.character,
            trait_name="Wits",
            trait_type="attribute",
            trait_value=3,
            cost=8,
        )
        for url in (
            journal.get_absolute_url(),
            reverse("game:xp_spending_request:detail", args=[spend.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertIsInstance(response.context["character"], Human)
                self.assertEqual(response.context["character"].pk, self.character.pk)

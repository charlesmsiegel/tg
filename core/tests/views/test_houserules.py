"""Tests for the house rules pages (Spread M6)."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import HouseRule
from core.views.houserules import group_rules_by_gameline


class GroupRulesByGamelineTests(TestCase):
    def test_all_lines_first_then_gameline_order_empty_lines_dropped(self):
        werewolf = HouseRule(name="Renown", gameline="wta")
        mage = HouseRule(name="Paradox", gameline="mta")
        general = HouseRule(name="Weekly XP", gameline="wod")
        groups = group_rules_by_gameline([werewolf, mage, general])
        self.assertEqual([g["code"] for g in groups], ["wod", "wta", "mta"])
        self.assertEqual([g["label"] for g in groups], ["All lines", "Werewolf", "Mage"])
        self.assertEqual(groups[0]["rules"], [general])

    def test_rules_keep_their_order_inside_a_group(self):
        first = HouseRule(name="A", gameline="mta")
        second = HouseRule(name="B", gameline="mta")
        self.assertEqual(group_rules_by_gameline([first, second])[0]["rules"], [first, second])

    def test_no_rules_no_groups(self):
        self.assertEqual(group_rules_by_gameline([]), [])


class HouseRulesIndexViewTests(TestCase):
    def test_index_groups_rules_and_links_details(self):
        rule = HouseRule.objects.create(
            name="Rote points", gameline="mta", description="Chargen only."
        )
        HouseRule.objects.create(name="Weekly XP", gameline="wod")
        response = self.client.get(reverse("core:houserules"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [g["label"] for g in response.context["rule_groups"]], ["All lines", "Mage"]
        )
        self.assertContains(response, reverse("core:houserule", args=[rule.pk]))
        self.assertContains(response, "Chargen only.")
        # The create action is staff-only (STAFF_WRITE policy).
        self.assertNotContains(response, reverse("core:create_houserule"))

    def test_empty_index_shows_empty_state(self):
        response = self.client.get(reverse("core:houserules"))
        self.assertContains(response, 'class="tl-empty"')


class HouseRuleFormErrorsTests(TestCase):
    def test_invalid_post_shows_error_summary_and_invalid_field(self):
        staff = get_user_model().objects.create_user("rules-staff", is_staff=True)
        self.client.force_login(staff)
        response = self.client.post(
            reverse("core:create_houserule"), {"name": "", "gameline": "wod"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="tl-errsum"')
        self.assertContains(response, '<a href="#id_name">')
        self.assertContains(response, "tl-field is-invalid")

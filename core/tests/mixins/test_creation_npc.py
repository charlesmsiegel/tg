"""Only staff and the chosen scope's storytellers may create an NPC through a creation form.

ScopedCreationFormMixin drops the ``npc`` field for everyone else (the chargen basics
views), and prepare_created_object clears it (MessageMixin create views).
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.core.archetype import Archetype
from characters.models.core.human import Human
from characters.models.demon.thrall import Thrall
from characters.models.mummy.mummy import Mummy
from game.models import Chronicle


class CreationNPCFieldTests(TestCase):
    def setUp(self):
        self.player = User.objects.create_user("npc_player")
        self.head_st = User.objects.create_user("npc_head_st")
        self.staff = User.objects.create_user("npc_staff", is_staff=True)
        self.chronicle = Chronicle.objects.create(name="NPC chronicle", head_st=self.head_st)
        Human.objects.create(name="Existing PC", owner=self.player, chronicle=self.chronicle)
        self.nature = Archetype.objects.create(name="Survivor")
        self.demeanor = Archetype.objects.create(name="Loner")

    def payload(self, name):
        return {
            "name": name,
            "nature": self.nature.pk,
            "demeanor": self.demeanor.pk,
            "concept": "Test concept",
            "chronicle": self.chronicle.pk,
            "npc": "on",
        }

    def post_thrall(self, user, name):
        self.client.force_login(user)
        response = self.client.post(reverse("characters:demon:create:thrall"), self.payload(name))
        self.assertEqual(response.status_code, 302)
        return Thrall.objects.get(name=name)

    def post_mummy(self, user, name):
        self.client.force_login(user)
        response = self.client.post(reverse("characters:mummy:create:mummy"), self.payload(name))
        self.assertEqual(response.status_code, 302)
        return Mummy.objects.get(name=name)

    def test_player_posting_npc_on_to_basics_view_creates_a_non_npc(self):
        thrall = self.post_thrall(self.player, "Player thrall")
        self.assertFalse(thrall.npc)
        self.assertEqual(thrall.owner, self.player)

    def test_storyteller_and_staff_may_create_an_npc_in_basics_view(self):
        for user in (self.head_st, self.staff):
            with self.subTest(user=user.username):
                self.assertTrue(self.post_thrall(user, f"{user.username} thrall").npc)

    def test_basics_form_omits_npc_for_a_player(self):
        self.client.force_login(self.player)
        url = reverse("characters:demon:create:thrall")
        response = self.client.get(url, {"chronicle": self.chronicle.pk})
        self.assertNotIn("npc", response.context["form"].fields)
        self.client.force_login(self.head_st)
        response = self.client.get(url, {"chronicle": self.chronicle.pk})
        self.assertIn("npc", response.context["form"].fields)

    def test_player_posting_npc_on_to_create_view_creates_a_non_npc(self):
        self.assertFalse(self.post_mummy(self.player, "Player mummy").npc)

    def test_storyteller_may_create_an_npc_in_create_view(self):
        self.assertTrue(self.post_mummy(self.head_st, "ST mummy").npc)

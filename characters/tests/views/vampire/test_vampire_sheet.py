"""The Vampire, Ghoul and Revenant sheets render on the Spread shell (C16)."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.vampire.clan import VampireClan
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.path import Path
from characters.models.vampire.revenant import Revenant, RevenantFamily
from characters.models.vampire.sect import VampireSect
from characters.models.vampire.vampire import Vampire


class VampireSheetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="player", password="pw")
        cls.clan = VampireClan.objects.create(name="Toreador")
        cls.sect = VampireSect.objects.create(name="Camarilla")
        cls.vampire = Vampire.objects.create(
            name="Celestine",
            owner=cls.user,
            status="App",
            clan=cls.clan,
            sect=cls.sect,
            generation_rating=10,
            auspex=2,
            presence=3,
            conscience=3,
            self_control=2,
            courage=4,
            humanity=7,
            blood_pool=9,
        )

    def get(self, obj, tab=""):
        self.client.force_login(self.user)
        return self.client.get(obj.get_absolute_url() + (f"?tab={tab}" if tab else ""))

    def test_cover_facts(self):
        response = self.get(self.vampire)
        self.assertContains(response, '<span class="tl-facts__k">Clan</span>', html=False)
        self.assertContains(response, '<span class="tl-facts__k">Sect</span>', html=False)
        self.assertContains(response, '<span class="tl-facts__v">10th</span>', html=False)
        self.assertNotContains(response, '<span class="tl-facts__k">Path</span>', html=False)

    def test_disciplines_are_the_power_section(self):
        response = self.get(self.vampire)
        self.assertContains(
            response, 'class="tl-section tl-section--power tl-span-7" id="disciplines"'
        )
        self.assertContains(response, "Auspex")
        self.assertContains(response, 'class="tl-dots tl-dots--acc" role="img" aria-label="3 of 5"')

    def test_advantage_tracks(self):
        response = self.get(self.vampire)
        self.assertContains(response, '<span class="tl-track__label">Humanity</span>', html=False)
        self.assertContains(response, '<span class="tl-track__label">Blood pool</span>', html=False)
        # Blood pool squares run to max_blood_pool (13 at the 10th generation).
        self.assertContains(response, 'class="tl-boxes" role="img" aria-label="9 of 13"')
        self.assertNotContains(response, "Path rating")

    def test_path_replaces_humanity(self):
        path = Path.objects.create(name="Path of Caine")
        Vampire.objects.filter(pk=self.vampire.pk).update(path=path, path_rating=5)
        response = self.get(self.vampire)
        self.assertContains(
            response, '<span class="tl-track__label">Path rating</span>', html=False
        )
        self.assertContains(response, '<span class="tl-facts__k">Path</span>', html=False)
        self.assertNotContains(
            response, '<span class="tl-track__label">Humanity</span>', html=False
        )

    def test_virtues_block(self):
        response = self.get(self.vampire)
        self.assertContains(response, 'id="virtues"')
        for name in ("Conscience", "Self-Control", "Courage"):
            self.assertContains(response, name)

    def test_no_bootstrap_cards(self):
        response = self.get(self.vampire)
        self.assertNotContains(response, "tg-card")

    def test_freebies_on_experience_tab(self):
        Vampire.objects.filter(pk=self.vampire.pk).update(status="Sub", freebies=5)
        response = self.get(self.vampire, "experience")
        self.assertContains(response, 'id="freebies"')
        self.assertContains(response, "Discipline (out of clan)")
        self.assertNotContains(self.get(self.vampire), 'id="freebies"')


class GhoulAndRevenantSheetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="player", password="pw")
        cls.domitor = Vampire.objects.create(name="Domitor", owner=cls.user, status="App")
        cls.ghoul = Ghoul.objects.create(
            name="Odette",
            owner=cls.user,
            status="App",
            domitor=cls.domitor,
            years_as_ghoul=12,
            potence=1,
            blood_pool=1,
        )
        cls.family = RevenantFamily.objects.create(name="Zantosa")
        cls.revenant = Revenant.objects.create(
            name="Istvan",
            owner=cls.user,
            status="App",
            family=cls.family,
            actual_age=212,
            presence=2,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_ghoul_sheet(self):
        response = self.client.get(self.ghoul.get_absolute_url())
        self.assertContains(response, '<span class="tl-facts__k">Domitor</span>', html=False)
        self.assertContains(response, '<span class="tl-facts__k">Years as ghoul</span>', html=False)
        self.assertContains(response, 'id="disciplines"')
        self.assertContains(response, "Potence")
        self.assertContains(response, 'aria-label="1 of 2"')  # blood pool to max_blood_pool
        self.assertContains(response, 'id="virtues"')

    def test_revenant_sheet(self):
        response = self.client.get(self.revenant.get_absolute_url())
        self.assertContains(response, '<span class="tl-facts__k">Family</span>', html=False)
        self.assertContains(
            response, '<span class="tl-facts__k">Pseudo-generation</span>', html=False
        )
        self.assertContains(response, 'id="disciplines"')
        self.assertContains(response, "Presence")
        self.assertContains(response, "Actual age")
        self.assertNotContains(response, 'id="virtues"')

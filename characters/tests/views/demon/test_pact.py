"""Pact pages are private to those who may fully view the pact's demon or thrall."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.core.human import Human
from characters.models.demon import Demon
from characters.models.demon.pact import Pact
from characters.models.demon.thrall import Thrall
from game.models import Chronicle


class PactVisibilityTests(TestCase):
    def setUp(self):
        self.demon_owner = User.objects.create_user("demon_owner")
        self.thrall_owner = User.objects.create_user("thrall_owner")
        self.head_st = User.objects.create_user("head_st")
        self.fellow_player = User.objects.create_user("fellow_player")
        self.outsider = User.objects.create_user("outsider")
        self.staff = User.objects.create_user("staff", is_staff=True)
        self.chronicle = Chronicle.objects.create(name="Burning Year", head_st=self.head_st)
        Human.objects.create(name="Bystander", owner=self.fellow_player, chronicle=self.chronicle)
        self.demon = Demon.objects.create(
            name="Ahrimel", owner=self.demon_owner, chronicle=self.chronicle, status="App"
        )
        self.thrall = Thrall.objects.create(
            name="Marcus", owner=self.thrall_owner, chronicle=self.chronicle, status="App"
        )
        self.pact = Pact.objects.create(
            demon=self.demon, thrall=self.thrall, terms="Secret bargain", faith_payment=2
        )
        other_demon = Demon.objects.create(name="Elsewhere", owner=self.outsider)
        self.other_pact = Pact.objects.create(demon=other_demon, terms="Unrelated bargain")
        self.detail_url = self.pact.get_absolute_url()
        self.list_url = reverse("characters:demon:list:pact")

    def test_parties_storyteller_and_staff_see_the_pact(self):
        for user in (self.demon_owner, self.thrall_owner, self.head_st, self.staff):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                response = self.client.get(self.detail_url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Secret bargain")

    def test_other_users_get_the_same_404_as_a_missing_pact(self):
        missing_url = reverse("characters:demon:pact", kwargs={"pk": self.other_pact.pk + 1000})
        for user in (self.fellow_player, self.outsider):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                hidden = self.client.get(self.detail_url)
                missing = self.client.get(missing_url)
                self.assertEqual(hidden.status_code, 404)
                self.assertEqual(missing.status_code, 404)
                self.assertNotContains(hidden, "Secret bargain", status_code=404)

    def test_anonymous_users_are_refused(self):
        for url in (self.detail_url, self.list_url):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 401)
                self.assertNotContains(response, "Secret bargain", status_code=401)

    def test_list_shows_only_pacts_the_user_may_view(self):
        expected = {
            self.demon_owner: [self.pact],
            self.thrall_owner: [self.pact],
            self.head_st: [self.pact],
            self.fellow_player: [],
            self.outsider: [self.other_pact],
        }
        for user, pacts in expected.items():
            with self.subTest(user=user.username):
                self.client.force_login(user)
                response = self.client.get(self.list_url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(list(response.context["object_list"]), pacts)

    def test_staff_list_shows_every_pact(self):
        self.client.force_login(self.staff)
        response = self.client.get(self.list_url)
        self.assertEqual(set(response.context["object_list"]), {self.pact, self.other_pact})

    def test_staff_see_a_pact_without_parties(self):
        orphan = Pact.objects.create(terms="Orphaned bargain")
        self.client.force_login(self.staff)
        self.assertContains(self.client.get(orphan.get_absolute_url()), "Orphaned bargain")
        self.client.force_login(self.head_st)
        self.assertEqual(self.client.get(orphan.get_absolute_url()).status_code, 404)

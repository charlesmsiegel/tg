from characters.models.core import Human
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle, Gameline, STRelationship


class TestSignUpView(TestCase):
    """Class that Tests SignUpView"""

    def test_correct_template(self):
        self.client.get("/accounts/")
        self.assertTemplateUsed("registration/login.html")


class TestProfileView(TestCase):
    """Class that Tests the ProfileView"""

    def setUp(self) -> None:
        self.user1 = User.objects.create_user("Test User 1", "test@user1.com", "testpass")
        self.user2 = User.objects.create_user("Test User 2", "test@user2.com", "testpass")
        self.storyteller = User.objects.create_user("Test Storyteller", "test@st.com", "testpass")

        mta = Gameline.objects.create(name="Mage: the Ascension")

        chronicle = Chronicle.objects.create(name="Test Chronicle")

        STRelationship.objects.create(user=self.storyteller, gameline=mta, chronicle=chronicle)

        self.char1 = Human.objects.create(name="Test Character 1", owner=self.user1)
        self.char2 = Human.objects.create(
            name="Test Character 2", owner=self.user2, chronicle=chronicle
        )
        self.char3 = Human.objects.create(name="Test Character 3", owner=self.user1)
        self.char4 = Human.objects.create(name="Test Character 4", owner=self.user2)
        self.char5 = Human.objects.create(name="Test Character 5", owner=self.user1)
        self.char6 = Human.objects.create(name="Test Character 6", owner=self.user2)

    def test_template_logged_in(self):
        self.client.login(username="Test User 1", password="testpass")
        response = self.client.get(self.user1.profile.get_absolute_url())
        self.assertTemplateUsed(response, "accounts/detail.html")

    def test_template_logged_out(self):
        response = self.client.get("/accounts/", follow=True)
        self.assertTemplateUsed(response, "core/index.html")

    def test_character_list(self):
        self.client.login(username="Test User 1", password="testpass")
        response = self.client.get(self.user1.profile.get_absolute_url())
        self.assertTemplateUsed(response, "accounts/detail.html")

        self.assertContains(response, "Test Character 1")
        self.assertNotContains(response, "Test Character 2")
        self.assertContains(response, f"/characters/{self.char1.id}/")

        self.assertContains(response, "Test Character 3")
        self.assertNotContains(response, "Test Character 4")
        self.assertContains(response, f"/characters/{self.char3.id}/")

        self.assertContains(response, "Test Character 5")
        self.assertNotContains(response, "Test Character 6")
        self.assertContains(response, f"/characters/{self.char5.id}/")

    def test_approval_list(self):
        self.client.login(username="Test Storyteller", password="testpass")
        response = self.client.get(self.storyteller.profile.get_absolute_url())
        self.assertContains(response, "Test Character 2")
        self.assertContains(response, "To Approve")

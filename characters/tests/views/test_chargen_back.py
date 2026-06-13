"""Tests for chargen back navigation."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.core.human import Human
from characters.models.vampire.vtmhuman import VtMHuman


class TestChargenBackView(TestCase):
    """Test the chargen back navigation view."""

    def setUp(self):
        self.user = User.objects.create_user("player", "p@test.com", "password")
        self.char = Human.objects.create(
            name="Test Char", owner=self.user, status="Un", creation_status=3
        )

    def test_can_go_back(self):
        self.client.login(username="player", password="password")
        url = reverse("characters:chargen_back", kwargs={"pk": self.char.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.char.refresh_from_db()
        self.assertEqual(self.char.creation_status, 2)
        # The redirect goes through the generic character router (not
        # get_absolute_url, which gameline subclasses override to a detail
        # route), so unfinished characters land on their creation step view.
        self.assertEqual(
            response.url, reverse("characters:character", kwargs={"pk": self.char.pk})
        )
        follow = self.client.get(response.url)
        self.assertEqual(follow.status_code, 200)

    def test_back_redirects_through_router_for_subclassed_url(self):
        """VtMHuman.get_absolute_url points at a detail route; Back must still
        route through the dispatcher so the user stays in chargen."""
        char = VtMHuman.objects.create(
            name="Vamp Human", owner=self.user, status="Un", creation_status=3
        )
        self.client.login(username="player", password="password")
        url = reverse("characters:chargen_back", kwargs={"pk": char.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse("characters:character", kwargs={"pk": char.pk})
        )

    def test_cannot_go_back_past_step_1(self):
        self.char.creation_status = 1
        self.char.save()
        self.client.login(username="player", password="password")
        url = reverse("characters:chargen_back", kwargs={"pk": self.char.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.char.refresh_from_db()
        self.assertEqual(self.char.creation_status, 1)

    def test_cannot_go_back_on_submitted_character(self):
        self.char.status = "Sub"
        self.char.save()
        self.client.login(username="player", password="password")
        url = reverse("characters:chargen_back", kwargs={"pk": self.char.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.char.refresh_from_db()
        self.assertEqual(self.char.creation_status, 3)  # Unchanged

    def test_cannot_go_back_on_approved_character(self):
        # Status transitions are validated: Un -> Sub -> App
        self.char.status = "Sub"
        self.char.save()
        self.char.status = "App"
        self.char.save()
        self.client.login(username="player", password="password")
        url = reverse("characters:chargen_back", kwargs={"pk": self.char.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.char.refresh_from_db()
        self.assertEqual(self.char.creation_status, 3)  # Unchanged

    def test_get_method_not_allowed(self):
        self.client.login(username="player", password="password")
        url = reverse("characters:chargen_back", kwargs={"pk": self.char.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_nonexistent_character_404(self):
        self.client.login(username="player", password="password")
        url = reverse("characters:chargen_back", kwargs={"pk": 99999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_other_user_cannot_go_back(self):
        other = User.objects.create_user("other", "o@test.com", "password")
        self.client.login(username="other", password="password")
        url = reverse("characters:chargen_back", kwargs={"pk": self.char.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_st_cannot_go_back_on_another_players_character(self):
        """ST status grants no back-navigation on someone else's character."""
        st = User.objects.create_user("st", "st@test.com", "password")
        st.is_staff = True
        st.save()
        self.client.login(username="st", password="password")
        url = reverse("characters:chargen_back", kwargs={"pk": self.char.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.char.refresh_from_db()
        self.assertEqual(self.char.creation_status, 3)

    def test_not_logged_in_redirects(self):
        url = reverse("characters:chargen_back", kwargs={"pk": self.char.pk})
        response = self.client.post(url)
        # AuthErrorHandlerMiddleware returns 401; plain Django would redirect
        self.assertIn(response.status_code, [302, 401])
        if response.status_code == 302:
            self.assertIn("login", response.url)

    def test_cannot_go_back_past_freebie_step_if_approved(self):
        """Cannot back past the freebie step once freebies have been approved."""
        # VtMHuman freebie_step is 5. Set creation_status to 6 (past freebies).
        char = VtMHuman.objects.create(
            name="Freebie Char",
            owner=self.user,
            status="Un",
            creation_status=6,
            freebies_approved=True,
        )
        self.client.login(username="player", password="password")
        url = reverse("characters:chargen_back", kwargs={"pk": char.pk})
        # Going back from 6 to 5 is the freebie step — blocked because
        # freebies have already been approved.
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual(char.creation_status, 6)  # Unchanged

    def test_cannot_go_back_from_freebie_step_if_approved(self):
        """Backing out of the freebie step itself is blocked once approved."""
        char = VtMHuman.objects.create(
            name="On Freebie Step",
            owner=self.user,
            status="Un",
            creation_status=5,
            freebies_approved=True,
        )
        self.client.login(username="player", password="password")
        url = reverse("characters:chargen_back", kwargs={"pk": char.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual(char.creation_status, 5)  # Unchanged

    def test_can_go_back_past_freebie_step_if_not_approved(self):
        """Can go back into the freebie step when freebies are not yet approved."""
        char = VtMHuman.objects.create(
            name="No Freebie Char",
            owner=self.user,
            status="Un",
            creation_status=6,
            freebies_approved=False,
        )
        self.client.login(username="player", password="password")
        url = reverse("characters:chargen_back", kwargs={"pk": char.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        char.refresh_from_db()
        self.assertEqual(char.creation_status, 5)


class TestChargenBackUrlProperty(TestCase):
    """The chargen_back_url property gates the shared Back button."""

    def setUp(self):
        self.user = User.objects.create_user("player", "p@test.com", "password")

    def test_present_mid_chargen(self):
        char = Human.objects.create(
            name="C", owner=self.user, status="Un", creation_status=3
        )
        self.assertEqual(
            char.chargen_back_url,
            reverse("characters:chargen_back", kwargs={"pk": char.pk}),
        )

    def test_empty_on_step_1(self):
        char = Human.objects.create(
            name="C", owner=self.user, status="Un", creation_status=1
        )
        self.assertEqual(char.chargen_back_url, "")

    def test_empty_when_submitted(self):
        char = Human.objects.create(
            name="C", owner=self.user, status="Un", creation_status=3
        )
        char.status = "Sub"
        char.save()
        self.assertEqual(char.chargen_back_url, "")

    def test_empty_when_freebies_approved(self):
        """The view blocks back-nav once freebies are approved, so the button
        must hide rather than render a guaranteed no-op."""
        char = Human.objects.create(
            name="C",
            owner=self.user,
            status="Un",
            creation_status=6,
            freebies_approved=True,
        )
        self.assertEqual(char.chargen_back_url, "")

    def test_locations_have_no_chargen_back_url(self):
        """LocationModel also has creation_status but must not expose the
        Back button — the property lives on Character only."""
        from locations.models.core.location import LocationModel

        loc = LocationModel.objects.create(name="Chantry", status="Un")
        self.assertFalse(hasattr(loc, "chargen_back_url"))


class TestChargenBackButtonRendering(TestCase):
    """The Back button must appear only for the owner mid-chargen."""

    def setUp(self):
        self.user = User.objects.create_user("player", "p@test.com", "password")
        self.client.login(username="player", password="password")

    def _get(self, char):
        return self.client.get(
            reverse("characters:character", kwargs={"pk": char.pk})
        )

    def test_button_present_mid_chargen(self):
        char = Human.objects.create(
            name="C", owner=self.user, status="Un", creation_status=2
        )
        response = self._get(char)
        self.assertContains(response, "chargen/back/")

    def test_button_absent_on_step_1(self):
        char = Human.objects.create(
            name="C", owner=self.user, status="Un", creation_status=1
        )
        response = self._get(char)
        self.assertNotContains(response, "chargen/back/")

    def test_button_absent_when_freebies_approved(self):
        # VtMHuman step 2 (abilities) renders reliably; with freebies approved
        # the property returns "" so the button must not appear.
        char = VtMHuman.objects.create(
            name="C",
            owner=self.user,
            status="Un",
            creation_status=2,
            freebies_approved=True,
        )
        response = self._get(char)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "chargen/back/")

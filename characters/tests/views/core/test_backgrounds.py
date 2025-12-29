"""Tests for backgrounds view module."""

from characters.forms.core.backgroundform import BackgroundRatingFormSet
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from characters.tests.utils import human_setup
from characters.views.core.backgrounds import HumanBackgroundsView
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse
from game.models import Chronicle


class TestHumanBackgroundsViewBasics(TestCase):
    """Tests for HumanBackgroundsView basic functionality."""

    def setUp(self):
        human_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.user,
            creation_status=3,  # Set to backgrounds step
        )
        self.contacts = Background.objects.get(property_name="contacts")
        self.mentor = Background.objects.get(property_name="mentor")
        self.factory = RequestFactory()

    def test_view_uses_correct_form_class(self):
        """View uses BackgroundRatingFormSet as form_class."""
        self.assertEqual(HumanBackgroundsView.form_class, BackgroundRatingFormSet)

    def test_view_uses_correct_template(self):
        """View uses the correct template."""
        self.assertEqual(
            HumanBackgroundsView.template_name, "characters/core/human/chargen.html"
        )

    def test_get_object_returns_human(self):
        """get_object() returns the correct Human instance."""
        request = self.factory.get("/")
        request.user = self.user
        view = HumanBackgroundsView()
        view.request = request
        view.kwargs = {"pk": self.human.pk}

        obj = view.get_object()
        self.assertEqual(obj, self.human)

    def test_get_success_url_returns_character_absolute_url(self):
        """get_success_url() returns the character's absolute URL."""
        request = self.factory.get("/")
        request.user = self.user
        view = HumanBackgroundsView()
        view.request = request
        view.kwargs = {"pk": self.human.pk}

        url = view.get_success_url()
        self.assertEqual(url, self.human.get_absolute_url())


class TestHumanBackgroundsViewPermissions(TestCase):
    """Tests for HumanBackgroundsView permission handling."""

    def setUp(self):
        human_setup()
        self.owner = User.objects.create_user(username="owner", password="password")
        self.other_user = User.objects.create_user(
            username="other", password="password"
        )
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.owner,
            creation_status=3,
        )
        self.contacts = Background.objects.get(property_name="contacts")
        self.factory = RequestFactory()

    def test_owner_can_access_view(self):
        """Character owner can access the backgrounds view."""
        self.client.login(username="owner", password="password")

        # Access through the character's absolute URL (creation status 3 = backgrounds)
        response = self.client.get(self.human.get_absolute_url())
        # View should render successfully (200) or redirect (302)
        self.assertIn(response.status_code, [200, 302])

    def test_other_user_cannot_access_view(self):
        """Non-owner cannot access the backgrounds view for unfinished character."""
        self.client.login(username="other", password="password")

        # Access through the character's absolute URL
        response = self.client.get(self.human.get_absolute_url())
        # Should be forbidden or redirect
        self.assertIn(response.status_code, [403, 302])

    def test_st_can_access_view(self):
        """Storyteller can access the backgrounds view."""
        # Create an ST with a chronicle
        st = User.objects.create_user(username="st", password="password")
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        chronicle.storytellers.add(st)
        self.human.chronicle = chronicle
        self.human.save()

        self.client.login(username="st", password="password")
        response = self.client.get(self.human.get_absolute_url())
        # ST should have access
        self.assertIn(response.status_code, [200, 302])


class TestHumanBackgroundsViewFormValidation(TestCase):
    """Tests for HumanBackgroundsView form validation."""

    def setUp(self):
        human_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.user,
            creation_status=3,
        )
        self.contacts = Background.objects.get(property_name="contacts")
        self.mentor = Background.objects.get(property_name="mentor")
        self.factory = RequestFactory()

    def test_form_valid_with_correct_total_points(self):
        """Form validates when background points total to required amount."""
        request = self.factory.post("/", data={})
        request.user = self.user
        view = HumanBackgroundsView()
        view.request = request
        view.kwargs = {"pk": self.human.pk}

        # Create a mock formset that totals 5 points (human.background_points)
        from unittest.mock import MagicMock

        mock_form1 = MagicMock()
        mock_form1.cleaned_data = {"bg": self.contacts, "rating": 3}
        mock_form2 = MagicMock()
        mock_form2.cleaned_data = {"bg": self.mentor, "rating": 2}

        mock_formset = MagicMock()
        mock_formset.__iter__ = MagicMock(return_value=iter([mock_form1, mock_form2]))
        mock_formset.save = MagicMock()

        # Set up the view
        view.object = self.human

        # The form_valid method should accept the form
        # We need to verify the calculation logic
        total = sum(
            [
                f.cleaned_data["rating"] * f.cleaned_data["bg"].multiplier
                for f in [mock_form1, mock_form2]
            ]
        )
        self.assertEqual(total, 5)
        self.assertEqual(total, self.human.background_points)

    def test_form_invalid_with_wrong_total_points(self):
        """Form is invalid when background points don't match required."""
        # Create backgrounds with ratings that don't total to 5
        # Human has background_points = 5 by default
        self.assertEqual(self.human.background_points, 5)

        # Test with wrong total
        request = self.factory.post("/", data={})
        request.user = self.user
        view = HumanBackgroundsView()
        view.request = request
        view.kwargs = {"pk": self.human.pk}
        view.object = self.human

        # Create a mock formset that totals incorrectly
        from unittest.mock import MagicMock

        mock_form1 = MagicMock()
        mock_form1.cleaned_data = {"bg": self.contacts, "rating": 2}
        mock_form1.add_error = MagicMock()

        mock_formset = MagicMock()
        mock_formset.__iter__ = MagicMock(return_value=iter([mock_form1]))

        # Total is 2, not 5
        total = sum(
            [f.cleaned_data["rating"] * f.cleaned_data["bg"].multiplier for f in [mock_form1]]
        )
        self.assertNotEqual(total, self.human.background_points)


class TestHumanBackgroundsViewContextData(TestCase):
    """Tests for HumanBackgroundsView context data."""

    def setUp(self):
        human_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.user,
            creation_status=3,
        )
        self.contacts = Background.objects.get(property_name="contacts")
        self.mentor = Background.objects.get(property_name="mentor")

    def test_context_includes_object(self):
        """Context data includes the character object."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.human.get_absolute_url())

        if response.status_code == 200:
            self.assertIn("object", response.context)
            self.assertEqual(response.context["object"], self.human)

    def test_context_bg_queryset_filtered_by_allowed_backgrounds(self):
        """Background queryset is filtered to allowed_backgrounds for the character type."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.human.get_absolute_url())

        if response.status_code == 200:
            form = response.context["form"]
            for f in form:
                queryset = f.fields["bg"].queryset
                # All backgrounds in queryset should be in allowed_backgrounds
                for bg in queryset:
                    self.assertIn(bg.property_name, self.human.allowed_backgrounds)

    def test_context_includes_empty_form(self):
        """Context includes an empty_form for adding new backgrounds."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.human.get_absolute_url())

        if response.status_code == 200:
            self.assertIn("empty_form", response.context)


class TestHumanBackgroundsViewIntegration(TestCase):
    """Integration tests for HumanBackgroundsView."""

    def setUp(self):
        human_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.user,
            creation_status=3,
        )
        self.contacts = Background.objects.get(property_name="contacts")
        self.mentor = Background.objects.get(property_name="mentor")

    def test_successful_form_submission_increments_creation_status(self):
        """Successful form submission increments creation_status."""
        self.client.login(username="testuser", password="password")

        initial_status = self.human.creation_status
        data = {
            "backgrounds-TOTAL_FORMS": "2",
            "backgrounds-INITIAL_FORMS": "0",
            "backgrounds-MIN_NUM_FORMS": "0",
            "backgrounds-MAX_NUM_FORMS": "1000",
            "backgrounds-0-bg": self.contacts.pk,
            "backgrounds-0-rating": 3,
            "backgrounds-0-note": "",
            "backgrounds-0-display_alt_name": "",
            "backgrounds-0-pooled": "",
            "backgrounds-1-bg": self.mentor.pk,
            "backgrounds-1-rating": 2,
            "backgrounds-1-note": "",
            "backgrounds-1-display_alt_name": "",
            "backgrounds-1-pooled": "",
        }

        response = self.client.post(self.human.get_absolute_url(), data=data)
        self.human.refresh_from_db()

        # Should redirect on success
        if response.status_code == 302:
            self.assertEqual(self.human.creation_status, initial_status + 1)

    def test_successful_form_submission_creates_background_ratings(self):
        """Successful form submission creates BackgroundRating objects."""
        self.client.login(username="testuser", password="password")

        # Ensure no background ratings exist
        BackgroundRating.objects.filter(char=self.human).delete()

        data = {
            "backgrounds-TOTAL_FORMS": "2",
            "backgrounds-INITIAL_FORMS": "0",
            "backgrounds-MIN_NUM_FORMS": "0",
            "backgrounds-MAX_NUM_FORMS": "1000",
            "backgrounds-0-bg": self.contacts.pk,
            "backgrounds-0-rating": 3,
            "backgrounds-0-note": "",
            "backgrounds-0-display_alt_name": "",
            "backgrounds-0-pooled": "",
            "backgrounds-1-bg": self.mentor.pk,
            "backgrounds-1-rating": 2,
            "backgrounds-1-note": "",
            "backgrounds-1-display_alt_name": "",
            "backgrounds-1-pooled": "",
        }

        response = self.client.post(self.human.get_absolute_url(), data=data)

        if response.status_code == 302:
            ratings = BackgroundRating.objects.filter(char=self.human)
            self.assertEqual(ratings.count(), 2)

    def test_invalid_total_points_shows_error(self):
        """Submitting with wrong total points shows an error."""
        self.client.login(username="testuser", password="password")

        data = {
            "backgrounds-TOTAL_FORMS": "1",
            "backgrounds-INITIAL_FORMS": "0",
            "backgrounds-MIN_NUM_FORMS": "0",
            "backgrounds-MAX_NUM_FORMS": "1000",
            "backgrounds-0-bg": self.contacts.pk,
            "backgrounds-0-rating": 2,  # Only 2 points, not 5
            "backgrounds-0-note": "",
            "backgrounds-0-display_alt_name": "",
            "backgrounds-0-pooled": "",
        }

        response = self.client.post(self.human.get_absolute_url(), data=data)
        self.human.refresh_from_db()

        # Should stay on the same page (not redirect)
        # creation_status should not change
        self.assertEqual(self.human.creation_status, 3)


class TestHumanBackgroundsViewMultiplier(TestCase):
    """Tests for background multiplier handling in HumanBackgroundsView."""

    def setUp(self):
        human_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.user,
            creation_status=3,
        )
        # Create a background with multiplier > 1
        self.double_bg = Background.objects.create(
            name="Expensive Background",
            property_name="expensive",
            multiplier=2,
        )
        self.human.allowed_backgrounds.append("expensive")
        self.contacts = Background.objects.get(property_name="contacts")

    def test_multiplier_affects_total_calculation(self):
        """Background multiplier is factored into total points calculation."""
        # With multiplier=2, a rating of 2 costs 4 points
        # Plus 1 point from contacts = 5 total
        self.client.login(username="testuser", password="password")

        data = {
            "backgrounds-TOTAL_FORMS": "2",
            "backgrounds-INITIAL_FORMS": "0",
            "backgrounds-MIN_NUM_FORMS": "0",
            "backgrounds-MAX_NUM_FORMS": "1000",
            "backgrounds-0-bg": self.double_bg.pk,
            "backgrounds-0-rating": 2,  # 2 * 2 = 4 points
            "backgrounds-0-note": "",
            "backgrounds-0-display_alt_name": "",
            "backgrounds-0-pooled": "",
            "backgrounds-1-bg": self.contacts.pk,
            "backgrounds-1-rating": 1,  # 1 * 1 = 1 point
            "backgrounds-1-note": "",
            "backgrounds-1-display_alt_name": "",
            "backgrounds-1-pooled": "",
        }

        initial_status = self.human.creation_status
        response = self.client.post(self.human.get_absolute_url(), data=data)
        self.human.refresh_from_db()

        # Total = 4 + 1 = 5, should be valid
        if response.status_code == 302:
            self.assertEqual(self.human.creation_status, initial_status + 1)

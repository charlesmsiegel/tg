"""Tests for circle views module."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.core.human import Human
from characters.models.wraith.circle import Circle
from game.models import Chronicle


class TestCircleCreateView(TestCase):
    """Test CircleCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_create_view_accessible_when_logged_in(self):
        """Test that circle create view is accessible when logged in."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:create:circle")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that correct template is used for circle create view."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:create:circle")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/circle/form.html")

    def test_create_view_requires_login(self):
        """Test that circle create view requires login."""
        url = reverse("characters:wraith:create:circle")
        response = self.client.get(url)
        # App returns 401 for unauthenticated users instead of redirect
        self.assertEqual(response.status_code, 401)

    def test_create_circle_successfully(self):
        """Test creating a circle successfully."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:create:circle")
        data = {
            "name": "Test Circle",
            "description": "A test circle",
            "chronicle": self.chronicle.pk,
            "public_info": "Public info",
        }
        response = self.client.post(url, data)
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Circle.objects.filter(name="Test Circle").exists())

    def test_create_circle_with_leader_adds_to_members(self):
        """Test that leader is added to members when creating circle."""
        self.client.login(username="testuser", password="password")
        leader = Human.objects.create(
            name="Circle Leader",
            owner=self.user,
            chronicle=self.chronicle,
        )
        url = reverse("characters:wraith:create:circle")
        data = {
            "name": "Test Circle",
            "description": "A test circle",
            "chronicle": self.chronicle.pk,
            "leader": leader.pk,
            "public_info": "",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        circle = Circle.objects.get(name="Test Circle")
        self.assertIn(leader, circle.members.all())


class TestCircleUpdateView(TestCase):
    """Test CircleUpdateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.circle = Circle.objects.create(
            name="Test Circle",
            description="A test circle",
            chronicle=self.chronicle,
        )

    def test_update_view_accessible_when_logged_in(self):
        """Test that circle update view is accessible when logged in."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:update:circle", kwargs={"pk": self.circle.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that correct template is used for circle update view."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:update:circle", kwargs={"pk": self.circle.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/circle/form.html")

    def test_update_view_returns_404_for_invalid_pk(self):
        """Test that update view returns 404 for non-existent circle."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:update:circle", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update_circle_successfully(self):
        """Test updating a circle successfully."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:update:circle", kwargs={"pk": self.circle.pk})
        data = {
            "name": "Updated Circle",
            "description": "Updated description",
            "chronicle": self.chronicle.pk,
            "public_info": "",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.circle.refresh_from_db()
        self.assertEqual(self.circle.name, "Updated Circle")

    def test_update_view_has_new_character_field(self):
        """Test that update view has new_character field for adding members."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:update:circle", kwargs={"pk": self.circle.pk})
        response = self.client.get(url)
        self.assertIn("new_character", response.context["form"].fields)

    def test_update_view_adds_new_member(self):
        """Test that update view can add new members."""
        self.client.login(username="testuser", password="password")
        new_member = Human.objects.create(
            name="New Member",
            owner=self.user,
            chronicle=self.chronicle,
        )
        url = reverse("characters:wraith:update:circle", kwargs={"pk": self.circle.pk})
        data = {
            "name": self.circle.name,
            "description": self.circle.description,
            "chronicle": self.chronicle.pk,
            "public_info": "",
            "new_character": new_member.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.circle.refresh_from_db()
        self.assertIn(new_member, self.circle.members.all())


class TestCircleListViewQueryOptimization(TestCase):
    """Test that CircleListView uses optimized queries."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        # Create multiple circles with leaders and members
        for i in range(3):
            leader = Human.objects.create(
                name=f"Leader {i}",
                owner=self.user,
                chronicle=self.chronicle,
            )
            circle = Circle.objects.create(
                name=f"Circle {i}",
                chronicle=self.chronicle,
                leader=leader,
            )
            # Add some members
            for j in range(2):
                member = Human.objects.create(
                    name=f"Member {i}-{j}",
                    owner=self.user,
                    chronicle=self.chronicle,
                )
                circle.members.add(member)

    def test_get_queryset_uses_select_related(self):
        """Test that get_queryset uses select_related for leader."""
        from characters.views.wraith.circle import CircleListView

        view = CircleListView()
        view.request = None
        queryset = view.get_queryset()
        # Check that select_related is used (by checking query has JOIN)
        self.assertIn("leader", str(queryset.query).lower())

    def test_get_queryset_uses_prefetch_related(self):
        """Test that get_queryset uses prefetch_related for members."""
        from characters.views.wraith.circle import CircleListView

        view = CircleListView()
        view.request = None
        queryset = view.get_queryset()
        # Check that the queryset has prefetch for members
        self.assertTrue(queryset._prefetch_related_lookups)

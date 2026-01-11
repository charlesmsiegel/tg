"""Tests for motley module."""

from django.contrib.auth.models import User
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from characters.models.changeling.motley import Motley
from characters.models.core.human import Human
from game.models import Chronicle


class TestMotleyListViewQueryOptimization(TestCase):
    """Test that MotleyListView uses optimized queries."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        for i in range(3):
            leader = Human.objects.create(
                name=f"Motley Leader {i}",
                owner=self.user,
                chronicle=self.chronicle,
            )
            motley = Motley.objects.create(
                name=f"Motley {i}",
                chronicle=self.chronicle,
                leader=leader,
            )
            for j in range(2):
                member = Human.objects.create(
                    name=f"Motley Member {i}-{j}",
                    owner=self.user,
                    chronicle=self.chronicle,
                )
                motley.members.add(member)

    def test_list_view_query_count_is_bounded(self):
        """Test that list view query count doesn't scale with number of motleys."""
        self.client.login(username="testuser", password="password")

        with CaptureQueriesContext(connection) as context:
            response = self.client.get("/characters/changeling/list/motley/")

        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        # Base overhead includes session, user/profile, polymorphic lookups, etc.
        # The optimization ensures queries don't scale with number of motleys
        self.assertLessEqual(
            query_count,
            20,
            f"Too many queries ({query_count}). List view may have N+1 issue.",
        )


class TestMotleyDetailView(TestCase):
    """Test Motley detail view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.leader = Human.objects.create(
            name="Motley Leader",
            owner=self.user,
            chronicle=self.chronicle,
        )
        self.motley = Motley.objects.create(
            name="Test Motley",
            chronicle=self.chronicle,
            leader=self.leader,
        )

    def test_detail_view_returns_200(self):
        """Test that detail view returns 200 for authenticated user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:motley", kwargs={"pk": self.motley.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that detail view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:motley", kwargs={"pk": self.motley.pk})
        )
        self.assertTemplateUsed(response, "characters/changeling/motley/detail.html")


class TestMotleyCreateView(TestCase):
    """Test Motley create view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_create_view_returns_200(self):
        """Test that create view returns 200 for authenticated user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:changeling:create:motley"))
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that create view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:changeling:create:motley"))
        self.assertTemplateUsed(response, "characters/changeling/motley/form.html")


class TestMotleyUpdateView(TestCase):
    """Test Motley update view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.leader = Human.objects.create(
            name="Motley Leader",
            owner=self.user,
            chronicle=self.chronicle,
        )
        self.motley = Motley.objects.create(
            name="Test Motley",
            chronicle=self.chronicle,
            leader=self.leader,
        )

    def test_update_view_returns_200(self):
        """Test that update view returns 200 for authenticated user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:update:motley", kwargs={"pk": self.motley.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that update view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:update:motley", kwargs={"pk": self.motley.pk})
        )
        self.assertTemplateUsed(response, "characters/changeling/motley/form.html")

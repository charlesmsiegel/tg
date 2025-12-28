"""Tests for generic module."""

from characters.models.mage.mage import Mage
from core.views.generic import DictView
from django.contrib.auth import get_user_model
from django.http import Http404
from django.test import RequestFactory, TestCase

User = get_user_model()


class DictViewTest(TestCase):
    """Test DictView 404 handling."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_get_object_nonexistent_pk_raises_404(self):
        """Test that get_object raises Http404 for nonexistent primary keys."""

        class TestDictView(DictView):
            model_class = Mage
            view_mapping = {}
            key_property = "creation_status"
            default_redirect = "characters:index"

        view = TestDictView()
        with self.assertRaises(Http404):
            view.get_object(pk=99999)

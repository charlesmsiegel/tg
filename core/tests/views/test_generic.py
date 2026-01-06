"""Tests for generic module."""

from characters.models.core.character import Character
from characters.models.mage.mage import Mage
from core.views.generic import DictView, MultipleFormsetsMixin
from django import forms
from django.contrib.auth import get_user_model
from django.forms import formset_factory, inlineformset_factory
from django.http import Http404, HttpResponse
from django.test import RequestFactory, TestCase
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView
from game.models import Chronicle

User = get_user_model()


class DictViewTest(TestCase):
    """Test DictView functionality."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
        )

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

    def test_get_object_returns_object(self):
        """Test that get_object returns the correct object."""

        class TestDictView(DictView):
            model_class = Character
            view_mapping = {}
            key_property = "status"
            default_redirect = "characters:index"

        view = TestDictView()
        obj = view.get_object(pk=self.character.pk)
        self.assertEqual(obj, self.character)

    def test_is_valid_key_returns_true_for_mapped_key(self):
        """Test is_valid_key returns True when key exists in view_mapping."""

        class MockView(TemplateView):
            template_name = "test.html"

        class TestDictView(DictView):
            model_class = Character
            view_mapping = {"App": MockView}
            key_property = "status"
            default_redirect = "characters:index"

        view = TestDictView()
        self.assertTrue(view.is_valid_key(self.character, "App"))

    def test_is_valid_key_returns_false_for_unmapped_key(self):
        """Test is_valid_key returns False when key is not in view_mapping."""

        class TestDictView(DictView):
            model_class = Character
            view_mapping = {}
            key_property = "status"
            default_redirect = "characters:index"

        view = TestDictView()
        self.assertFalse(view.is_valid_key(self.character, "App"))

    def test_get_default_redirect_with_string_url(self):
        """Test get_default_redirect returns redirect for string URL."""

        class TestDictView(DictView):
            model_class = Character
            view_mapping = {}
            key_property = "status"
            default_redirect = "core:home"

        view = TestDictView()
        request = self.factory.get("/")
        request.user = self.user

        response = view.get_default_redirect(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 302)

    def test_get_default_redirect_with_callable_view(self):
        """Test get_default_redirect works with a view class."""

        class FallbackView(TemplateView):
            template_name = "core/home.html"

        class TestDictView(DictView):
            model_class = Character
            view_mapping = {}
            key_property = "status"
            default_redirect = FallbackView

        view = TestDictView()
        request = self.factory.get("/")
        request.user = self.user

        response = view.get_default_redirect(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)

    def test_get_default_redirect_raises_value_error_for_invalid_type(self):
        """Test get_default_redirect raises ValueError for invalid redirect type."""

        class TestDictView(DictView):
            model_class = Character
            view_mapping = {}
            key_property = "status"
            default_redirect = 123  # Invalid type

        view = TestDictView()
        request = self.factory.get("/")
        request.user = self.user

        with self.assertRaises(ValueError) as cm:
            view.get_default_redirect(request, pk=self.character.pk)
        self.assertIn("default_redirect must be a URL name or a view callable", str(cm.exception))

    def test_handle_request_dispatches_to_mapped_view(self):
        """Test handle_request dispatches to the correct view for valid keys."""

        class MappedView(TemplateView):
            template_name = "core/home.html"

            def get(self, request, *args, **kwargs):
                return HttpResponse("Mapped View Response")

        class TestDictView(DictView):
            model_class = Character
            view_mapping = {"App": MappedView}
            key_property = "status"
            default_redirect = "core:home"

        view = TestDictView()
        request = self.factory.get("/")
        request.user = self.user

        response = view.handle_request(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Mapped View Response")

    def test_handle_request_uses_default_redirect_for_unmapped_key(self):
        """Test handle_request uses default redirect for unmapped keys."""

        class TestDictView(DictView):
            model_class = Character
            view_mapping = {}  # No mappings
            key_property = "status"
            default_redirect = "core:home"

        view = TestDictView()
        request = self.factory.get("/")
        request.user = self.user

        response = view.handle_request(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 302)

    def test_get_method_calls_handle_request(self):
        """Test that GET requests are handled via handle_request."""

        class MappedView(TemplateView):
            template_name = "core/home.html"

            def get(self, request, *args, **kwargs):
                return HttpResponse("GET Response")

        class TestDictView(DictView):
            model_class = Character
            view_mapping = {"App": MappedView}
            key_property = "status"
            default_redirect = "core:home"

        request = self.factory.get("/")
        request.user = self.user

        view = TestDictView.as_view()
        response = view(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"GET Response")

    def test_post_method_calls_handle_request(self):
        """Test that POST requests are handled via handle_request."""

        class MappedView(TemplateView):
            template_name = "core/home.html"

            def post(self, request, *args, **kwargs):
                return HttpResponse("POST Response")

        class TestDictView(DictView):
            model_class = Character
            view_mapping = {"App": MappedView}
            key_property = "status"
            default_redirect = "core:home"

        request = self.factory.post("/")
        request.user = self.user

        view = TestDictView.as_view()
        response = view(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"POST Response")


class SimpleForm(forms.Form):
    """Simple form for testing formsets."""

    name = forms.CharField(max_length=100)
    value = forms.IntegerField(required=False)


SimpleFormSet = formset_factory(SimpleForm, extra=1)


class MultipleFormsetsMixinTest(TestCase):
    """Test MultipleFormsetsMixin functionality."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_get_formset_kwargs_without_object(self):
        """Test get_formset_kwargs returns prefix only when no object exists."""

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {"items": SimpleFormSet}

        view = TestView()
        kwargs = view.get_formset_kwargs("items")
        self.assertEqual(kwargs, {"prefix": "items"})

    def test_get_formset_kwargs_with_object(self):
        """Test get_formset_kwargs includes instance when object exists."""

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {"items": SimpleFormSet}

        view = TestView()
        view.object = "mock_object"
        kwargs = view.get_formset_kwargs("items")
        self.assertEqual(kwargs["prefix"], "items")
        self.assertEqual(kwargs["instance"], "mock_object")

    def test_get_formset_context_generates_context_and_js(self):
        """Test get_formset_context generates proper context and JavaScript."""

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {"items": SimpleFormSet}

        view = TestView()
        context, js_code = view.get_formset_context(SimpleFormSet, "items")

        self.assertIn("formset", context)
        self.assertEqual(context["formset_prefix"], "items")
        self.assertEqual(context["add_button_id"], "add_items_form")
        self.assertEqual(context["remove_button_class"], "remove_items_form")
        self.assertIn("empty_form", context)
        self.assertIn("<script>", js_code)
        self.assertIn("add_items_form", js_code)

    def test_get_formset_context_with_bound_formset(self):
        """Test get_formset_context uses bound formset when provided."""

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {"items": SimpleFormSet}

        view = TestView()
        bound_formset = SimpleFormSet(
            data={
                "items-TOTAL_FORMS": "1",
                "items-INITIAL_FORMS": "0",
                "items-0-name": "Test",
            },
            prefix="items",
        )
        context, js_code = view.get_formset_context(SimpleFormSet, "items", bound_formset)

        self.assertEqual(context["formset"], bound_formset)

    def test_get_formset_context_ensures_at_least_one_form(self):
        """Test get_formset_context creates formset with at least one form."""
        EmptyFormSet = formset_factory(SimpleForm, extra=0)

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {"items": EmptyFormSet}

        view = TestView()
        context, js_code = view.get_formset_context(EmptyFormSet, "items")

        # Should have at least one form due to initial=[{}]
        self.assertGreaterEqual(len(context["formset"].forms), 1)

    def test_get_bound_formsets_creates_formsets_from_post_data(self):
        """Test get_bound_formsets creates formsets bound to POST data."""

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {"items": SimpleFormSet}

        view = TestView()
        view.request = self.factory.post(
            "/",
            data={
                "items-TOTAL_FORMS": "1",
                "items-INITIAL_FORMS": "0",
                "items-0-name": "Test Item",
                "items-0-value": "42",
            },
        )

        bound_formsets = view.get_bound_formsets()
        self.assertIn("items", bound_formsets)
        self.assertTrue(bound_formsets["items"].is_bound)

    def test_get_bound_formsets_caches_result(self):
        """Test get_bound_formsets caches and returns same result."""

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {"items": SimpleFormSet}

        view = TestView()
        view.request = self.factory.post(
            "/",
            data={
                "items-TOTAL_FORMS": "1",
                "items-INITIAL_FORMS": "0",
                "items-0-name": "Test",
            },
        )

        first_call = view.get_bound_formsets()
        second_call = view.get_bound_formsets()
        self.assertIs(first_call, second_call)

    def test_get_formsets_returns_context_and_js_for_all_formsets(self):
        """Test get_formsets returns context and JS for all defined formsets."""

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {
                "items": SimpleFormSet,
                "extras": SimpleFormSet,
            }

        view = TestView()
        formsets_context, formsets_js = view.get_formsets()

        self.assertIn("items_context", formsets_context)
        self.assertIn("extras_context", formsets_context)
        self.assertIn("items_js", formsets_js)
        self.assertIn("extras_js", formsets_js)

    def test_get_context_data_includes_formsets(self):
        """Test get_context_data includes formset context and JS."""

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {"items": SimpleFormSet}

        view = TestView()
        view.request = self.factory.get("/")

        context = view.get_context_data()
        self.assertIn("items_context", context)
        self.assertIn("items_js", context)

    def test_get_form_data_returns_empty_for_invalid_prefix(self):
        """Test get_form_data returns empty list for nonexistent prefix."""

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {"items": SimpleFormSet}

        view = TestView()
        view.request = self.factory.post("/", data={})

        result = view.get_form_data("nonexistent")
        self.assertEqual(result, [])

    def test_get_form_data_extracts_form_data(self):
        """Test get_form_data extracts data from formset forms."""

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {"items": SimpleFormSet}

        view = TestView()
        view.request = self.factory.post(
            "/",
            data={
                "items-TOTAL_FORMS": "2",
                "items-INITIAL_FORMS": "0",
                "items-0-name": "First",
                "items-0-value": "1",
                "items-1-name": "Second",
                "items-1-value": "2",
            },
        )

        result = view.get_form_data("items")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "First")
        self.assertEqual(result[1]["name"], "Second")

    def test_get_form_data_filters_blank_entries(self):
        """Test get_form_data filters out entries with blank required fields."""

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {"items": SimpleFormSet}

        view = TestView()
        view.request = self.factory.post(
            "/",
            data={
                "items-TOTAL_FORMS": "2",
                "items-INITIAL_FORMS": "0",
                "items-0-name": "Valid",
                "items-0-value": "1",
                "items-1-name": "",  # Blank - should be filtered
                "items-1-value": "2",
            },
        )

        result = view.get_form_data("items")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Valid")

    def test_get_form_data_respects_blankable_fields(self):
        """Test get_form_data allows blank values in blankable fields."""

        class TestView(MultipleFormsetsMixin, TemplateView):
            template_name = "test.html"
            formsets = {"items": SimpleFormSet}

        view = TestView()
        view.request = self.factory.post(
            "/",
            data={
                "items-TOTAL_FORMS": "1",
                "items-INITIAL_FORMS": "0",
                "items-0-name": "Test",
                "items-0-value": "",  # Blank but in blankable list
            },
        )

        result = view.get_form_data("items", blankable=["value"])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Test")


class MultipleFormsetsMixinFormValidTest(TestCase):
    """Test form_valid and form_invalid methods of MultipleFormsetsMixin."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_form_valid_saves_valid_formsets(self):
        """Test form_valid saves formsets when they are valid."""
        saved_formsets = []

        class MockFormSet:
            def __init__(self, *args, **kwargs):
                self.forms = []
                self._is_valid = True

            def is_valid(self):
                return self._is_valid

            def save(self):
                saved_formsets.append(self)

        class TestForm(forms.Form):
            name = forms.CharField()

        class TestView(MultipleFormsetsMixin, CreateView):
            template_name = "test.html"
            form_class = TestForm
            success_url = "/"
            formsets = {"items": MockFormSet}

        view = TestView()
        view.request = self.factory.post("/", data={"name": "Test"})
        view.object = None

        form = TestForm(data={"name": "Test"})
        # Simulate super().form_valid() redirect
        try:
            view.form_valid(form)
        except Exception:
            pass  # May fail on redirect but formsets should be processed

        self.assertEqual(len(saved_formsets), 1)

    def test_form_valid_returns_form_invalid_for_invalid_formsets(self):
        """Test form_valid returns form_invalid when formsets are invalid."""

        class MockFormSet:
            def __init__(self, *args, **kwargs):
                self.forms = []
                self._is_valid = False

            def is_valid(self):
                return self._is_valid

        class TestForm(forms.Form):
            name = forms.CharField()

        class TestView(MultipleFormsetsMixin, CreateView):
            template_name = "test.html"
            form_class = TestForm
            success_url = "/"
            formsets = {"items": MockFormSet}

            def form_invalid(self, form):
                return HttpResponse("Invalid", status=400)

        view = TestView()
        view.request = self.factory.post("/", data={"name": "Test"})
        view.object = None
        view._bound_formsets = None

        form = TestForm(data={"name": "Test"})
        response = view.form_valid(form)
        self.assertEqual(response.status_code, 400)

    def test_form_invalid_preserves_bound_formsets(self):
        """Test form_invalid ensures bound formsets are available."""

        class TestView(MultipleFormsetsMixin, CreateView):
            template_name = "test.html"
            form_class = SimpleForm
            success_url = "/"
            formsets = {"items": SimpleFormSet}

            def render_to_response(self, context, **kwargs):
                return HttpResponse("Rendered")

        view = TestView()
        view.request = self.factory.post(
            "/",
            data={
                "name": "",  # Invalid
                "items-TOTAL_FORMS": "1",
                "items-INITIAL_FORMS": "0",
                "items-0-name": "Test",
            },
        )
        view.object = None
        view._bound_formsets = None

        form = SimpleForm(data={"name": ""})
        view.form_invalid(form)

        # Bound formsets should now be populated
        self.assertIsNotNone(view._bound_formsets)

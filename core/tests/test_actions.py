"""ObjectActionView: the order of checks, the transaction and the htmx hook."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.test import RequestFactory, TestCase

from characters.models.core.human import Human
from core.actions import ActionFailed, ObjectActionView
from core.permissions import Permission


class RenameForm(forms.Form):
    name = forms.CharField(max_length=20)


class RenameThenFail(ObjectActionView):
    """Writes, then fails when asked to, so the rollback is observable."""

    model = Human
    permission = Permission.EDIT_FULL
    form_class = RenameForm
    success_message = "Renamed {object.name}"
    calls = 0

    def perform(self, form):
        type(self).calls += 1
        self.object.name = form.cleaned_data["name"]
        self.object.save()
        if form.cleaned_data["name"] == "fail":
            raise ActionFailed("Refused")
        return None


class FragmentAction(RenameThenFail):
    def fragment_response(self, result=None, form=None, error=None):
        return HttpResponse(f"fragment:{error or ('invalid' if form is not None else 'ok')}")


class ObjectActionViewTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("base_owner")
        self.stranger = users.objects.create_user("base_stranger")
        self.character = Human.objects.create(name="Before", owner=self.owner, status="Un")
        RenameThenFail.calls = 0

    def call(self, view_class, user, data):
        request = RequestFactory().post("/", data)
        SessionMiddleware(lambda r: None).process_request(request)
        request._messages = FallbackStorage(request)
        request.user = user
        return view_class.as_view()(request, pk=self.character.pk), request

    def test_success_flashes_and_redirects(self):
        response, request = self.call(RenameThenFail, self.owner, {"name": "After"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], self.character.get_absolute_url())
        self.assertEqual([str(m) for m in get_messages(request)], ["Renamed After"])

    def test_failure_rolls_back_the_write(self):
        response, request = self.call(RenameThenFail, self.owner, {"name": "fail"})
        self.assertEqual(response.status_code, 302)
        self.character.refresh_from_db()
        self.assertEqual(self.character.name, "Before")
        self.assertEqual([str(m) for m in get_messages(request)], ["Refused"])

    def test_invalid_form_writes_nothing(self):
        response, request = self.call(RenameThenFail, self.owner, {"name": "x" * 30})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RenameThenFail.calls, 0)
        self.assertTrue(list(get_messages(request)))

    def test_hidden_subject_is_404_before_form_validation(self):
        with self.assertRaises(Http404):
            self.call(RenameThenFail, self.stranger, {"name": "x" * 30})
        self.assertEqual(RenameThenFail.calls, 0)

    def test_missing_subject_is_404(self):
        request = RequestFactory().post("/", {"name": "After"})
        request.user = self.owner
        with self.assertRaises(Http404):
            RenameThenFail.as_view()(request, pk=self.character.pk + 1000)

    def test_visible_but_not_permitted_is_403(self):
        Human.objects.filter(pk=self.character.pk).update(status="App")
        with self.assertRaises(PermissionDenied):
            self.call(RenameThenFail, self.owner, {"name": "After"})
        self.assertEqual(RenameThenFail.calls, 0)

    def test_fragment_hook_short_circuits_every_path(self):
        for data, body in (
            ({"name": "After"}, "fragment:ok"),
            ({"name": "fail"}, "fragment:Refused"),
            ({"name": "x" * 30}, "fragment:invalid"),
        ):
            with self.subTest(body=body):
                response, _ = self.call(FragmentAction, self.owner, data)
                self.assertEqual(response.content.decode(), body)

    def test_get_is_not_allowed_on_the_view_itself(self):
        request = RequestFactory().get("/")
        request.user = self.owner
        response = RenameThenFail.as_view()(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 405)

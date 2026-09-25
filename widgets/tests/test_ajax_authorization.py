"""Security contract for the chained-select endpoint."""

from django.contrib.auth import get_user_model
from django.test import TestCase

from characters.models.mage.faction import MageFaction


class ChainedSelectAuthorizationTests(TestCase):
    url = "/__chained_select__/"
    form = "characters.forms.mage.mage.MageCreationForm"

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="mage_player", password="password"
        )

    def test_anonymous_cannot_request_choices(self):
        response = self.client.get(self.url, {"form": self.form, "field": "faction"})
        self.assertEqual(response.status_code, 401)

    def test_unregistered_import_path_is_rejected(self):
        self.client.force_login(self.user)
        for form in ("os.abort", "os.getcwd", "os.path"):
            with self.subTest(form=form):
                response = self.client.get(
                    self.url, {"form": form, "field": "faction", "parent_value": "1"}
                )
                self.assertEqual(response.status_code, 400)

    def test_registered_form_returns_only_valid_child_choices(self):
        parent = MageFaction.objects.create(name="Traditions")
        child = MageFaction.objects.create(name="Order of Hermes", parent=parent)
        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {"form": self.form, "field": "faction", "parent_value": str(parent.pk)},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["choices"],
            [{"value": str(child.pk), "label": child.name}],
        )

    def test_invalid_field_and_parent_are_rejected(self):
        self.client.force_login(self.user)
        for data in (
            {"form": self.form, "field": "name", "parent_value": "1"},
            {"form": self.form, "field": "faction", "parent_value": "not-an-id"},
            {"form": self.form, "field": "faction", "parent_value": "999999"},
        ):
            with self.subTest(data=data):
                self.assertEqual(self.client.get(self.url, data).status_code, 400)

    def test_post_is_not_accepted(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"form": self.form, "field": "faction"})
        self.assertEqual(response.status_code, 405)

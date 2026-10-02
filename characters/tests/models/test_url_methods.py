"""Every URL method a characters model defines reverses to a real route."""

from django.apps import apps
from django.test import SimpleTestCase
from django.urls import NoReverseMatch, resolve

from characters.models.demon.earthbound import Earthbound
from characters.models.hunter.htrhuman import HtRHuman
from characters.models.hunter.hunter import Hunter
from characters.models.mage.companion import Companion
from characters.models.mage.sorcerer import Sorcerer
from characters.models.werewolf.nagah import Nagah


class ModelURLMethodTests(SimpleTestCase):
    INSTANCE_METHODS = ("get_absolute_url", "get_update_url")
    CLASS_METHODS = ("get_creation_url",)

    def models(self):
        return [
            model
            for model in apps.get_app_config("characters").get_models()
            if not model._meta.abstract and hasattr(model, "type")
        ]

    def assert_routes(self, model, name, call):
        with self.subTest(model=model.__name__, method=name):
            try:
                url = call()
            except NoReverseMatch as error:
                self.fail(f"{model.__name__}.{name}(): {error}")
            resolve(url)

    def test_every_url_method_reverses(self):
        for model in self.models():
            instance = model(pk=1)
            for name in self.INSTANCE_METHODS:
                if hasattr(model, name):
                    self.assert_routes(model, name, getattr(instance, name))
            for name in self.CLASS_METHODS:
                if hasattr(model, name):
                    self.assert_routes(model, name, getattr(model, name))

    def test_types_with_their_own_routes_use_them(self):
        expected = {
            Earthbound: "characters:demon:update:earthbound",
            HtRHuman: "characters:hunter:update:htrhuman",
            Hunter: "characters:hunter:update:hunter",
            Companion: "characters:mage:update:companion_full",
            Sorcerer: "characters:mage:update:sorcerer_full",
            Nagah: "characters:werewolf:update:fera",
        }
        for model, route in expected.items():
            with self.subTest(model=model.__name__):
                self.assertEqual(resolve(model(pk=1).get_update_url()).view_name, route)

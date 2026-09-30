"""Every ``core.models.Model`` subclass has a ``type`` of its own within its app."""

from collections import defaultdict

from django.apps import apps
from django.test import SimpleTestCase

from core.models import Model


class ModelTypeUniquenessTest(SimpleTestCase):
    def test_type_is_unique_within_each_app(self):
        by_type = defaultdict(list)
        for model in apps.get_models():
            if issubclass(model, Model):
                by_type[(model._meta.app_label, model.type)].append(model.__name__)
        duplicates = {key: names for key, names in by_type.items() if len(names) > 1}
        self.assertEqual(duplicates, {}, "Give each model its own snake_case `type`.")

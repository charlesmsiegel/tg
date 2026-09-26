"""The golden fixture records routing before the registry migration."""

import json
from pathlib import Path

from django.template.loader import get_template
from django.test import SimpleTestCase

from characters.chargen import get_workflow


class RegistryTests(SimpleTestCase):
    def test_all_persisted_positions_are_preserved(self):
        golden = json.loads((Path(__file__).parent / "fixtures/chargen_order.json").read_text())
        for kind, paths in golden.items():
            with self.subTest(kind=kind):
                workflow = get_workflow(kind)
                self.assertEqual([step.view_path for step in workflow.steps], paths)
                self.assertEqual(len({step.key for step in workflow.steps}), len(paths))
                freebies = [i for i, step in enumerate(workflow.steps, 1) if step.key == "freebies"]
                self.assertEqual(freebies, [workflow.freebie_step])
                self.assertIn("Freebies", workflow.step(workflow.freebie_step).view.__name__)
                for step in workflow.steps:
                    get_template(step.template)

    def test_router_coverage(self):
        from characters.views.core import GenericCharacterDetailView

        for kind, router in GenericCharacterDetailView().view_mapping.items():
            with self.subTest(kind=kind):
                workflow = get_workflow(kind)
                if getattr(router, "chargen_router", False):
                    self.assertIsNotNone(workflow)
                    self.assertEqual(router.view_mapping, workflow.view_mapping)
                else:
                    self.assertIsNone(workflow)

    def test_aliases_share_the_fera_workflow(self):
        self.assertIs(get_workflow("bastet"), get_workflow("fera"))
        self.assertIsNone(get_workflow("earthbound"))
        self.assertIsNone(get_workflow("not_a_character"))

    def test_detail_only_types_preserve_freebie_metadata_without_a_wizard(self):
        from characters.models.demon.earthbound import Earthbound
        from characters.models.hunter.hunter import Hunter
        from characters.models.mummy.mummy import Mummy
        from characters.models.vampire.revenant import Revenant

        for model, position in ((Earthbound, 7), (Hunter, 7), (Mummy, 7), (Revenant, 6)):
            with self.subTest(model=model.__name__):
                self.assertIsNone(get_workflow(model.type))
                self.assertEqual(model.freebie_step, position)

    def test_positions_are_bounded(self):
        workflow = get_workflow("vampire")
        for position in (0, -1, 14):
            with self.assertRaises(ValueError):
                workflow.step(position)

    def test_no_orphan_step_views(self):
        import importlib
        import inspect

        from characters.chargen.definitions import WORKFLOWS
        from characters.views.core.chargen_mixins import ChargenStepMixin

        views = {step.view for workflow in WORKFLOWS.values() for step in workflow.steps}
        for module in {view.__module__ for view in views}:
            for name, cls in inspect.getmembers(importlib.import_module(module), inspect.isclass):
                if cls.__module__ == module and issubclass(cls, ChargenStepMixin):
                    with self.subTest(view=name):
                        self.assertTrue(any(issubclass(view, cls) for view in views))

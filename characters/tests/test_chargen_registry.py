"""The golden fixture records routing before the registry migration."""

import importlib
import inspect
import json
from functools import partial
from pathlib import Path

from django.template.loader import get_template
from django.test import SimpleTestCase

from characters.chargen import get_workflow
from characters.chargen.definitions import DETAIL_ONLY_FREEBIE_POSITIONS, WORKFLOWS
from characters.chargen.predicates import no_background
from characters.chargen.registry import progress_rows
from characters.models.changeling.autumn_person import AutumnPerson
from characters.models.changeling.inanimae import Inanimae
from characters.models.changeling.nunnehi import Nunnehi
from characters.models.demon.earthbound import Earthbound
from characters.models.hunter.htrhuman import HtRHuman
from characters.models.hunter.hunter import Hunter
from characters.models.mummy.mtr_human import MtRHuman
from characters.models.mummy.mummy import Mummy
from characters.models.vampire.revenant import Revenant
from characters.views.core import GenericCharacterDetailView
from characters.views.core.chargen_mixins import ChargenStepMixin


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
        expected = (
            (AutumnPerson, 5),
            (Inanimae, 5),
            (Nunnehi, 5),
            (Earthbound, 7),
            (HtRHuman, 5),
            (Hunter, 7),
            (MtRHuman, 5),
            (Mummy, 7),
            (Revenant, 6),
        )
        self.assertEqual(set(DETAIL_ONLY_FREEBIE_POSITIONS), {model.type for model, _ in expected})
        for model, position in expected:
            with self.subTest(model=model.__name__):
                self.assertIsNone(get_workflow(model.type))
                self.assertEqual(model.freebie_step, position)
                self.assertEqual(model().freebie_step, position)

    def test_positions_are_bounded(self):
        workflow = get_workflow("vampire")
        for position in (0, -1, 14):
            with self.assertRaises(ValueError):
                workflow.step(position)

    def test_no_orphan_step_views(self):
        views = {step.view for workflow in WORKFLOWS.values() for step in workflow.steps}
        for module in {view.__module__ for view in views}:
            for name, cls in inspect.getmembers(importlib.import_module(module), inspect.isclass):
                if cls.__module__ == module and issubclass(cls, ChargenStepMixin):
                    with self.subTest(view=name):
                        self.assertTrue(any(issubclass(view, cls) for view in views))


class ProgressTests(SimpleTestCase):
    """Workflow.progress() and progress_rows() feed the chargen step list."""

    def test_progress_marks_conditional_and_grouped_steps(self):
        steps = {step["key"]: step for step in get_workflow("mage").progress(1)}
        self.assertEqual(
            (steps["attributes"]["conditional"], steps["attributes"]["group"]), (False, None)
        )
        self.assertEqual(
            (steps["languages"]["conditional"], steps["languages"]["group"]), (True, None)
        )
        self.assertEqual((steps["rote"]["conditional"], steps["rote"]["group"]), (True, None))
        self.assertEqual(
            (steps["node"]["conditional"], steps["node"]["group"]), (True, "background")
        )
        self.assertEqual(steps["attributes"]["status"], "current")

    def test_every_background_gated_step_is_in_the_background_group(self):
        for workflow in WORKFLOWS.values():
            for step in workflow.steps:
                gated = isinstance(step.skip_if, partial) and step.skip_if.func is no_background
                with self.subTest(step=step.key):
                    self.assertEqual(step.group == "background", gated)

    def test_mage_background_details_collapse_into_one_row(self):
        rows = progress_rows(get_workflow("mage").progress(1))
        self.assertEqual(len(rows), 11)
        self.assertEqual([row["number"] for row in rows], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 21])
        details = rows[9]
        self.assertEqual(details["group"], "background")
        self.assertEqual(
            [step["label"] for step in details["steps"]],
            [
                "Node",
                "Library",
                "Familiar",
                "Wonder",
                "Enhancement",
                "Sanctum",
                "Allies",
                "Mentor",
                "Contacts",
                "Retainers",
                "Chantry",
            ],
        )
        self.assertEqual((rows[10]["label"], rows[10]["group"]), ("Specialties", None))
        self.assertEqual([row["status"] for row in rows[:2]], ["current", "pending"])
        self.assertTrue(rows[7]["conditional"])  # Languages

    def test_group_row_status_follows_its_steps(self):
        workflow = get_workflow("mage")
        library = [step.key for step in workflow.steps].index("library") + 1
        self.assertEqual(progress_rows(workflow.progress(library))[9]["status"], "current")
        last = progress_rows(workflow.progress(len(workflow.steps)))
        self.assertEqual([last[9]["status"], last[10]["status"]], ["completed", "current"])

    def test_rows_accept_progress_without_groups(self):
        rows = progress_rows(
            [{"label": "Stats", "status": "completed"}, {"label": "Powers", "status": "current"}]
        )
        self.assertEqual(
            [(row["number"], row["label"], row["group"], row["conditional"]) for row in rows],
            [(1, "Stats", None, False), (2, "Powers", None, False)],
        )

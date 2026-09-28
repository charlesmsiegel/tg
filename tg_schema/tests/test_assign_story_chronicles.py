"""tg_schema 0007 assigns unassigned stories to the one chronicle their characters play in."""

import importlib
from types import SimpleNamespace

from django.db import connection
from django.test import TestCase

from characters.models.core.human import Human
from game.models import Chronicle, Story, StoryXPRequest

migration = importlib.import_module("tg_schema.migrations.0007_assign_story_chronicles")


class AssignStoryChroniclesTests(TestCase):
    def setUp(self):
        self.ashes = Chronicle.objects.create(name="Ashes")
        self.embers = Chronicle.objects.create(name="Embers")
        self.ash_one = Human.objects.create(name="Ash One", chronicle=self.ashes)
        self.ash_two = Human.objects.create(name="Ash Two", chronicle=self.ashes)
        self.ember = Human.objects.create(name="Ember", chronicle=self.embers)
        self.drifter = Human.objects.create(name="Drifter")

    def story(self, name, *characters, chronicle=None):
        story = Story.objects.create(name=name, chronicle=chronicle)
        for character in characters:
            StoryXPRequest.objects.create(story=story, character=character)
        return story

    def run_migration(self):
        # A data-only migration: it reads the editor's connection and nothing else.
        migration.assign_story_chronicles(None, SimpleNamespace(connection=connection))

    def chronicle_of(self, story):
        story.refresh_from_db()
        return story.chronicle

    def test_a_story_joins_the_chronicle_its_characters_share(self):
        story = self.story("The Moving Streets", self.ash_one, self.ash_two)
        self.run_migration()
        self.assertEqual(self.chronicle_of(story), self.ashes)

    def test_characters_without_a_chronicle_do_not_count(self):
        story = self.story("Crossroads", self.ash_one, self.drifter)
        self.run_migration()
        self.assertEqual(self.chronicle_of(story), self.ashes)

    def test_characters_in_several_chronicles_leave_it_unassigned(self):
        story = self.story("Crossover", self.ash_one, self.ember)
        self.run_migration()
        self.assertIsNone(self.chronicle_of(story))

    def test_a_story_without_placed_characters_stays_unassigned(self):
        empty = self.story("Never Played")
        drifting = self.story("Drifting", self.drifter)
        self.run_migration()
        self.assertIsNone(self.chronicle_of(empty))
        self.assertIsNone(self.chronicle_of(drifting))

    def test_assigned_stories_are_left_alone_and_a_rerun_changes_nothing(self):
        placed = self.story("Placed", self.ash_one, chronicle=self.embers)
        story = self.story("The Moving Streets", self.ash_one)
        self.run_migration()
        self.run_migration()
        self.assertEqual(self.chronicle_of(placed), self.embers)
        self.assertEqual(self.chronicle_of(story), self.ashes)

    def test_one_query_for_the_spans_and_one_update_per_story(self):
        self.story("One", self.ash_one)
        self.story("Two", self.ember)
        self.story("Mixed", self.ash_one, self.ember)
        with self.assertNumQueries(3):
            self.run_migration()

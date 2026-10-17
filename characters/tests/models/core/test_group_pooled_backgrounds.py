"""Characterize pooled updates and guard against per-contribution background reads."""

from django.db import connection
from django.db.models.signals import post_save
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from characters.models.core.background_block import (
    Background,
    BackgroundRating,
    PooledBackgroundRating,
)
from characters.models.core.group import Group
from characters.models.core.human import Human


class GroupPooledBackgroundTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Pool")
        self.member = Human.objects.create(name="Member")
        self.other = Human.objects.create(name="Other")
        self.group.members.add(self.member)
        self.background = Background.objects.create(name="Contacts", property_name="contacts")

    def contribute(self, **kwargs):
        return BackgroundRating.objects.create(
            char=kwargs.pop("char", self.member),
            bg=kwargs.pop("bg", self.background),
            pooled=kwargs.pop("pooled", True),
            rating=kwargs.pop("rating", 1),
            **kwargs,
        )

    def test_totals_are_keyed_by_background_and_note_and_limited_to_pooled_members(self):
        second = Background.objects.create(name="Allies", property_name="allies", poolable=False)
        self.contribute(rating=2)
        self.contribute(rating=3)
        self.contribute(note="Work", rating=4)
        self.contribute(bg=second, rating=2)
        self.contribute(char=self.other, rating=9)
        self.contribute(pooled=False, rating=8)
        self.group.update_pooled_backgrounds()
        self.assertCountEqual(
            self.group.pooled_backgrounds.values_list("bg_id", "note", "rating"),
            [(self.background.pk, "", 5), (self.background.pk, "Work", 4), (second.pk, "", 2)],
        )

    def test_existing_row_metadata_and_stale_rows_are_preserved(self):
        current = PooledBackgroundRating.objects.create(
            group=self.group, bg=self.background, rating=9, complete=True, url="reference"
        )
        stale = PooledBackgroundRating.objects.create(
            group=self.group, bg=self.background, note="Stale", rating=7
        )
        self.contribute(rating=2)
        self.group.update_pooled_backgrounds()
        current.refresh_from_db()
        stale.refresh_from_db()
        self.assertEqual((current.rating, current.complete, current.url), (2, True, "reference"))
        self.assertEqual(stale.rating, 7)
        self.group.members.clear()
        with self.assertNumQueries(1):
            self.group.update_pooled_backgrounds()
        current.refresh_from_db()
        self.assertEqual(current.rating, 2)

    def test_null_background_and_zero_contributions_are_retained(self):
        self.contribute(bg=None, rating=0)
        self.group.update_pooled_backgrounds()
        self.assertEqual(self.group.pooled_backgrounds.get(bg=None).rating, 0)

    def test_existing_pool_still_emits_save_signal(self):
        pool = PooledBackgroundRating.objects.create(group=self.group, bg=self.background)
        self.contribute(rating=2)
        saved = []

        def record_save(sender, instance, created, **kwargs):
            saved.append((instance.pk, instance.rating, created))

        post_save.connect(record_save, sender=PooledBackgroundRating)
        try:
            self.group.update_pooled_backgrounds()
        finally:
            post_save.disconnect(record_save, sender=PooledBackgroundRating)
        self.assertEqual(saved, [(pool.pk, 2, False)])

    def test_saves_follow_background_name_order_and_repeat_updates_existing_rows(self):
        allies = Background.objects.create(name="Allies", property_name="allies")
        self.contribute(note="Work", rating=2)
        self.contribute(bg=allies, rating=3)
        saved = []

        def record_save(sender, instance, **kwargs):
            saved.append((instance.bg_id, instance.note, instance.rating))

        post_save.connect(record_save, sender=PooledBackgroundRating)
        try:
            self.group.update_pooled_backgrounds()
            saved.clear()
            self.group.update_pooled_backgrounds()
        finally:
            post_save.disconnect(record_save, sender=PooledBackgroundRating)
        self.assertEqual(saved, [(allies.pk, "", 3), (self.background.pk, "Work", 2)])
        self.assertEqual(self.group.pooled_backgrounds.count(), 2)

    def test_query_count_is_constant_as_contributions_grow_for_existing_pool(self):
        PooledBackgroundRating.objects.create(group=self.group, bg=self.background)
        self.contribute()
        with CaptureQueriesContext(connection) as small:
            self.group.update_pooled_backgrounds()
        for _ in range(8):
            self.contribute()
        with CaptureQueriesContext(connection) as large:
            self.group.update_pooled_backgrounds()
        self.assertEqual(len(small), 3)
        self.assertEqual(len(large), len(small))
        self.assertEqual(self.group.pooled_backgrounds.get().rating, 9)

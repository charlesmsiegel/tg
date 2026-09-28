"""Assign each unassigned story to the chronicle its characters play in.

A story's only link to play is its story XP requests: a story whose requests'
characters all belong to one chronicle joins that chronicle. Characters without a
chronicle are ignored; a story with no such characters, or with characters in
several chronicles, stays unassigned for staff to place by hand. Assigned stories
are never touched, so the migration is safe to re-run.
"""

from django.db import migrations
from django.db.models import Max, Min

from game.models import Story, StoryXPRequest


def assign_story_chronicles(apps, schema_editor):
    # ``game`` has no migration state on legacy installations (see 0005), so the
    # live models are used; only their primary keys and chronicle links are read.
    using = schema_editor.connection.alias
    spans = (
        StoryXPRequest.objects.using(using)
        .filter(story__chronicle__isnull=True, character__chronicle__isnull=False)
        .values("story_id")
        .annotate(low=Min("character__chronicle"), high=Max("character__chronicle"))
    )
    for span in spans:
        if span["low"] == span["high"]:
            Story.objects.using(using).filter(
                pk=span["story_id"], chronicle__isnull=True
            ).update(chronicle_id=span["low"])


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0006_sheet_cover_facts")]
    operations = [migrations.RunPython(assign_story_chronicles, migrations.RunPython.noop)]

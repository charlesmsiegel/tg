from collections import defaultdict
from functools import cached_property

from django.db import models
from django.urls import reverse

from characters.models.core.background_block import (
    BackgroundRating,
    PooledBackgroundRating,
)
from characters.models.core.character import Character
from core.models import Model
from core.utils import CharacterOrganizationRegistry


class Group(Model):
    type = "group"

    members = models.ManyToManyField(Character, blank=True)
    leader = models.ForeignKey(
        Character,
        blank=True,
        related_name="leads_group",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def get_absolute_url(self):
        return reverse("characters:group", kwargs={"pk": self.pk})

    def get_display_type(self):
        return self.type.title()

    def get_update_url(self):
        return reverse("characters:update:group", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:create:group")

    @cached_property
    def roster(self):
        """The leader first, then the other members by name, owners loaded.

        Cached per instance: the group page reads it for the cover count and the table.

        The leader is listed even when it is not among ``members``; members come
        back as their concrete character types, so gameline fields are available.
        """
        members = list(self.members.select_related("owner").order_by("name"))
        if self.leader_id is None:
            return members
        leader = next((m for m in members if m.pk == self.leader_id), None)
        if leader is None:
            leader = self.leader.get_real_instance()
        return [leader] + [m for m in members if m.pk != self.leader_id]

    def update_pooled_backgrounds(self):
        bgs = BackgroundRating.objects.filter(char__in=self.members.all(), pooled=True)
        d = defaultdict(lambda: defaultdict(int))
        for bgr in bgs:
            d[bgr.bg][bgr.note] += bgr.rating
        for bg in d.keys():
            for note in d[bg].keys():
                p = PooledBackgroundRating.objects.get_or_create(bg=bg, note=note, group=self)[0]
                p.rating = d[bg][note]
                p.save()

    @staticmethod
    def cleanup_character_organizations(character):
        """Remove character from all Group organizational structures."""
        # Remove from Group memberships
        for group in Group.objects.filter(members=character):
            group.members.remove(character)

        # Remove from Group leadership positions
        for group in Group.objects.filter(leader=character):
            group.leader = None
            group.save()


# Register the cleanup handler with the registry
CharacterOrganizationRegistry.register(Group.cleanup_character_organizations)

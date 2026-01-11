import random

from django.db import models
from django.urls import reverse

from locations.models.core.location import LocationModel


class Library(LocationModel):
    type = "library"
    gameline = "mta"

    rank = models.IntegerField(default=1)
    faction = models.ForeignKey(
        "characters.MageFaction", null=True, blank=True, on_delete=models.SET_NULL
    )
    books = models.ManyToManyField("items.Grimoire", blank=True)

    class Meta:
        verbose_name = "Library"
        verbose_name_plural = "Libraries"

    def get_update_url(self):
        return reverse("locations:mage:update:library", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mage:create:library")

    def add_book(self, grimoire):
        self.books.add(grimoire)
        self.save()
        return True

    def set_faction(self, faction):
        self.faction = faction
        return True

    def has_faction(self):
        return self.faction is not None

    def num_books(self):
        return self.books.count()

    def set_rank(self, rank):
        self.rank = rank
        self.save()
        return True

    def increase_rank(self, book=None):
        if book is None or book in self.books.all():
            self.rank += 1
            self.random_book()
        else:
            self.rank += 1
            self.add_book(book)

    def random_book(self):
        from characters.models.mage.faction import MageFaction
        from items.models.mage.grimoire import Grimoire

        book = Grimoire.objects.create(name="", owner=self.owner, chronicle=self.chronicle)
        if self.owned_by:
            book.owned_by.add(self.owned_by)
        rank = random.randint(1, self.rank)
        if random.random() < 0.5 and MageFaction.objects.filter(parent=self.faction).exists():
            f = MageFaction.objects.filter(parent=self.faction).order_by("?").first()
        else:
            f = self.faction
        book.random(rank=rank, faction=f)
        return self.add_book(book)

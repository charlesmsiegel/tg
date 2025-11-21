from core.utils import filepath
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from game.models import Chronicle
from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager


class Book(models.Model):
    name = models.TextField(default="")
    url = models.CharField(max_length=200, null=True, blank=True)
    edition = models.CharField(
        max_length=4,
        choices=[
            ("1e", "1st Edition"),
            ("2e", "2nd Edition"),
            ("Rev", "Revised Edition"),
            ("20th", "20th Anniversary Edition"),
        ],
        default="1e",
    )
    gameline = models.CharField(
        max_length=3,
        choices=[
            ("wod", "World of Darkness"),
            ("vtm", "Vampire: the Masquerade"),
            ("wta", "Werewolf: the Apocalypse"),
            ("mta", "Mage: the Ascension"),
            ("wto", "Wraith: the Oblivion"),
            ("ctd", "Changeling: the Dreaming"),
        ],
        default="wod",
    )
    storytellers_vault = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def get_absolute_url(self):
        return reverse("book", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class BookReference(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    page = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Book Reference"
        verbose_name_plural = "Book References"

    def __str__(self):
        return f"<i>{self.book}</i> p. {self.page}"


class ModelManager(PolymorphicManager):
    """Custom manager for Model with common query patterns."""

    def submitted(self):
        """Objects with status='Sub' (Submitted for approval)"""
        return self.filter(status="Sub")

    def pending_approval(self):
        """Objects with status in ['Un', 'Sub'] (awaiting approval)"""
        return self.filter(status__in=["Un", "Sub"])

    def approved(self):
        """Objects with status='App' (Approved)"""
        return self.filter(status="App")

    def retired(self):
        """Objects with status='Ret' (Retired)"""
        return self.filter(status="Ret")

    def deceased(self):
        """Objects with status='Dec' (Deceased)"""
        return self.filter(status="Dec")

    def active(self):
        """Objects not retired or deceased"""
        return self.exclude(status__in=["Dec", "Ret"])

    def visible(self):
        """Objects with display=True"""
        return self.filter(display=True)

    def for_chronicle(self, chronicle):
        """Objects in a specific chronicle"""
        return self.filter(chronicle=chronicle).select_related("chronicle")

    def for_user_chronicles(self, user):
        """Objects in any of the user's chronicles"""
        return self.filter(chronicle__in=user.chronicle_set.all()).select_related(
            "chronicle"
        )

    def owned_by(self, user):
        """Objects owned by a specific user"""
        return self.filter(owner=user).select_related("owner")

    def with_pending_images(self):
        """Objects with images awaiting approval"""
        return self.filter(image_status="sub").exclude(image="")

    def top_level(self):
        """Objects with no parent (top-level in hierarchy)"""
        return self.filter(parent=None)

    def pending_approval_for_user(self, user):
        """Objects awaiting approval in user's chronicles (optimized)"""
        return (
            self.filter(status="Sub", chronicle__in=user.chronicle_set.all())
            .select_related("chronicle", "owner")
            .order_by("name")
        )


class Model(PolymorphicModel):
    type = "model"

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    chronicle = models.ForeignKey(
        Chronicle, blank=True, null=True, on_delete=models.SET_NULL
    )

    objects = ModelManager()

    status_keys = ["Un", "Sub", "App", "Ret", "Dec"]
    statuses = [
        "Unfinished",
        "Submitted",
        "Approved",
        "Retired",
        "Deceased",
    ]
    status = models.CharField(
        max_length=3, choices=zip(status_keys, statuses), default="Un"
    )
    display = models.BooleanField(default=True)
    sources = models.ManyToManyField(BookReference, blank=True)
    description = models.TextField(default="")
    public_info = models.TextField(default="")
    image = models.ImageField(upload_to=filepath, blank=True, null=True)
    image_status = models.CharField(
        max_length=3,
        choices=zip(["sub", "app"], ["Submitted", "Approved"]),
        default="sub",
    )
    freebies_approved = models.BooleanField(default=False)

    st_notes = models.TextField(default="")

    class Meta:
        abstract = True
        verbose_name = "Model"
        verbose_name_plural = "Models"

    def __str__(self):
        return self.name

    def has_name(self):
        return self.name != ""

    def set_name(self, name):
        self.name = name
        return True

    def has_description(self):
        return self.description != ""

    def set_description(self, description):
        self.description = description
        return True

    def has_owner(self):
        return self.owner is not None

    def set_owner(self, owner):
        self.owner = owner
        return True

    def owned_by_list(self):
        return []

    def update_status(self, status):
        self.status = status
        return True

    def toggle_display(self):
        self.display = not self.display
        return True

    def has_source(self):
        return self.sources.count() > 0

    def add_source(self, book_title, page_number):
        book = Book.objects.get_or_create(name=book_title)[0]
        bookref = BookReference.objects.get_or_create(book=book, page=page_number)[0]
        self.sources.add(bookref)
        return self

    def get_gameline(self):
        s = str(self.__class__).split(" ")[-1].split(".")[2]
        if s == "core":
            return "World of Darkness"
        return str(self.__class__).split(" ")[-1].split(".")[2].title()

    def get_full_gameline(self):
        short = self.get_gameline()
        if short == "World of Darkness":
            return short
        elif short == "Vampire":
            return "Vampire: the Masquerade"
        elif short == "Werewolf":
            return "Werewolf: the Apocalypse"
        elif short == "Mage":
            return "Mage: the Ascension"
        elif short == "Changeling":
            return "Changeling: the Dreaming"
        elif short == "Wraith":
            return "Wraith: the Oblivion"


class NewsItem(models.Model):
    title = models.CharField(default="", max_length=100)
    content = models.TextField(default="")
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "News Item"
        verbose_name_plural = "News Items"

    def get_absolute_url(self):
        return reverse("newsitem", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("update_newsitem", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("create_newsitem")


class Language(models.Model):
    """Class managing Language data"""

    name = models.CharField(max_length=100)
    frequency = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def get_absolute_url(self):
        return reverse("language", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("update_language", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("create_language")

    def __str__(self):
        return f"{self.name}"


class Number(models.Model):
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.value)


class Noun(models.Model):
    name = models.TextField(default="")

    class Meta:
        verbose_name = "Noun"
        verbose_name_plural = "Nouns"

    def __str__(self):
        return self.name


class HouseRule(models.Model):
    name = models.CharField(default="", max_length=100)
    sources = models.ManyToManyField(BookReference, blank=True)
    description = models.TextField(default="")
    chronicle = models.ForeignKey(
        Chronicle, blank=True, null=True, on_delete=models.SET_NULL
    )
    gameline = models.CharField(
        max_length=3,
        choices=[
            ("wod", "World of Darkness"),
            ("vtm", "Vampire: the Masquerade"),
            ("wta", "Werewolf: the Apocalypse"),
            ("mta", "Mage: the Ascension"),
            ("wto", "Wraith: the Oblivion"),
            ("ctd", "Changeling: the Dreaming"),
        ],
        default="wod",
    )

    def __str__(self):
        return self.name

    def display_sources(self):
        return ", ".join([str(x) for x in self.sources.all()])

    def add_source(self, book_title, page_number):
        book = Book.objects.get_or_create(name=book_title)[0]
        bookref = BookReference.objects.get_or_create(book=book, page=page_number)[0]
        self.sources.add(bookref)
        return self

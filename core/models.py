from core.utils import filepath
from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from game.models import Chronicle
from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager
from polymorphic.query import PolymorphicQuerySet


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


class ModelQuerySet(PolymorphicQuerySet):
    """Custom queryset for Model with chainable query patterns."""

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
        """Objects with no parent (top-level in hierarchy)

        Raises:
            AttributeError: If the model doesn't have a 'parent' field
        """
        # Check if the model has a parent field
        if not hasattr(self.model, '_meta'):
            raise AttributeError(f"{self.model.__name__} manager cannot use top_level()")

        try:
            self.model._meta.get_field('parent')
        except Exception:
            raise AttributeError(
                f"{self.model.__name__} does not have a 'parent' field. "
                f"top_level() can only be used on models with hierarchical parent relationships."
            )

        return self.filter(parent=None)

    def pending_approval_for_user(self, user):
        """Objects awaiting approval in user's chronicles (optimized)"""
        return (
            self.filter(status="Sub", chronicle__in=user.chronicle_set.all())
            .select_related("chronicle", "owner")
            .order_by("name")
        )


class ModelManager(PolymorphicManager):
    """Custom manager for Model with common query patterns."""

    def get_queryset(self):
        """Return custom queryset with chainable methods."""
        return ModelQuerySet(self.model, using=self._db)


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


class CharacterTemplate(models.Model):
    """Pre-configured character builds from World of Darkness sourcebooks"""

    GAMELINE_CHOICES = [
        ("wod", "World of Darkness"),
        ("vtm", "Vampire: the Masquerade"),
        ("wta", "Werewolf: the Apocalypse"),
        ("mta", "Mage: the Ascension"),
        ("wto", "Wraith: the Oblivion"),
        ("ctd", "Changeling: the Dreaming"),
        ("dtf", "Demon: the Fallen"),
    ]

    # Core Identification
    name = models.CharField(max_length=100)
    gameline = models.CharField(max_length=10, choices=GAMELINE_CHOICES)
    character_type = models.CharField(
        max_length=100
    )  # "vampire", "mage", "werewolf", etc.

    # Metadata
    description = models.TextField(blank=True)
    source_book = models.CharField(
        max_length=200, blank=True
    )  # "Mage: The Ascension Revised p. 87"
    concept = models.CharField(max_length=100, blank=True)

    # Character Data (JSONFields for flexibility)
    basic_info = models.JSONField(
        default=dict, blank=True
    )  # nature, demeanor, essence, etc.
    attributes = models.JSONField(
        default=dict, blank=True
    )  # {"strength": 2, "perception": 4, ...}
    abilities = models.JSONField(
        default=dict, blank=True
    )  # {"alertness": 2, "investigation": 3, ...}
    backgrounds = models.JSONField(
        default=list, blank=True
    )  # [{"name": "Contacts", "rating": 3}]
    powers = models.JSONField(
        default=dict, blank=True
    )  # spheres, disciplines, gifts, etc.
    merits_flaws = models.JSONField(
        default=list, blank=True
    )  # [{"name": "Eidetic Memory", "rating": 2}]
    specialties = models.JSONField(
        default=list, blank=True
    )  # ["Investigation (Crime Scenes)"]

    # Freebie Allocation Guidance
    suggested_freebie_spending = models.JSONField(default=dict, blank=True)

    # Additional Resources
    languages = models.JSONField(default=list, blank=True)  # ["English", "Spanish"]
    equipment = models.TextField(blank=True)  # Starting gear description

    # Access Control
    is_official = models.BooleanField(
        default=False
    )  # From published books vs user-created
    is_public = models.BooleanField(default=True)  # Available to all users
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_templates"
    )

    # Tracking
    times_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["gameline", "name"]
        indexes = [
            models.Index(fields=["gameline", "character_type"]),
        ]
        verbose_name = "Character Template"
        verbose_name_plural = "Character Templates"

    def __str__(self):
        return f"{self.name} ({self.get_gameline_display()})"

    def get_top_attributes(self, limit=3):
        """Return top N attributes by rating"""
        if not self.attributes:
            return []
        sorted_attrs = sorted(self.attributes.items(), key=lambda x: x[1], reverse=True)
        return [attr[0].replace("_", " ").title() for attr in sorted_attrs[:limit]]

    def get_summary_stats(self):
        """Return summary for quick preview"""
        return {
            "total_attributes": sum(self.attributes.values()) if self.attributes else 0,
            "total_abilities": sum(self.abilities.values()) if self.abilities else 0,
            "background_count": len(self.backgrounds) if self.backgrounds else 0,
            "power_count": len(self.powers) if self.powers else 0,
        }

    def apply_to_character(self, character):
        """
        Apply template data to character instance.
        Returns dict of applied changes for audit trail.
        """
        applied_changes = {}

        # 1. Basic Info (concept, etc.)
        if self.basic_info:
            for field, value in self.basic_info.items():
                if hasattr(character, field):
                    if isinstance(value, str) and value.startswith("FK:"):
                        # Handle foreign keys: "FK:Archetype:Judge"
                        parts = value.split(":")
                        if len(parts) == 3:
                            model_name, object_name = parts[1], parts[2]
                            try:
                                model = apps.get_model("characters", model_name)
                                obj = model.objects.get(name=object_name)
                                setattr(character, field, obj)
                                applied_changes[field] = object_name
                            except Exception:
                                pass
                    else:
                        setattr(character, field, value)
                        applied_changes[field] = value

        # 2. Attributes
        if self.attributes:
            for attr, rating in self.attributes.items():
                if hasattr(character, attr):
                    setattr(character, attr, rating)
            applied_changes["attributes"] = self.attributes

        # 3. Abilities
        if self.abilities:
            for ability, rating in self.abilities.items():
                if hasattr(character, ability):
                    setattr(character, ability, rating)
            applied_changes["abilities"] = self.abilities

        # 4. Backgrounds
        if self.backgrounds:
            from characters.models.core.background_block import Background, BackgroundRating

            for bg_data in self.backgrounds:
                try:
                    background = Background.objects.get(name=bg_data["name"])
                    BackgroundRating.objects.get_or_create(
                        character=character,
                        bg=background,
                        defaults={"rating": bg_data["rating"]},
                    )
                except Background.DoesNotExist:
                    pass
            applied_changes["backgrounds"] = self.backgrounds

        # 5. Powers (gameline-specific: spheres, disciplines, gifts, etc.)
        if self.powers:
            for power_name, rating in self.powers.items():
                if hasattr(character, power_name):
                    setattr(character, power_name, rating)
            applied_changes["powers"] = self.powers

        # 6. Merits/Flaws
        if self.merits_flaws:
            from characters.models.core.meritflaw import MeritFlaw, MeritFlawRating

            for mf_data in self.merits_flaws:
                try:
                    mf_obj = MeritFlaw.objects.get(name=mf_data["name"])
                    MeritFlawRating.objects.get_or_create(
                        character=character,
                        mf=mf_obj,
                        defaults={"rating": mf_data["rating"]},
                    )
                except MeritFlaw.DoesNotExist:
                    pass
            applied_changes["merits_flaws"] = self.merits_flaws

        # 7. Languages
        if self.languages:
            for lang_name in self.languages:
                try:
                    lang = Language.objects.get(name=lang_name)
                    character.languages.add(lang)
                except Language.DoesNotExist:
                    pass
            applied_changes["languages"] = self.languages

        # 8. Specialties
        if self.specialties:
            from characters.models.core.specialty import Specialty

            for specialty_name in self.specialties:
                try:
                    # Specialties are stored as strings like "Investigation (Crime Scenes)"
                    Specialty.objects.get_or_create(
                        character=character, name=specialty_name
                    )
                except Exception:
                    pass
            applied_changes["specialties"] = self.specialties

        character.save()

        # 9. Create application record
        TemplateApplication.objects.create(
            character=character, template=self, customized_fields=[]
        )

        # 10. Increment usage counter
        self.times_used += 1
        self.save(update_fields=["times_used"])

        return applied_changes


class TemplateApplication(models.Model):
    """Track when templates are applied to characters"""

    character = models.OneToOneField(
        "characters.Character",
        on_delete=models.CASCADE,
        related_name="template_application",
    )
    template = models.ForeignKey(
        CharacterTemplate,
        on_delete=models.SET_NULL,
        null=True,
        related_name="applications",
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    customized_fields = models.JSONField(
        default=list, blank=True
    )  # Track what user changed

    class Meta:
        verbose_name = "Template Application"
        verbose_name_plural = "Template Applications"

    def __str__(self):
        template_name = self.template.name if self.template else "Unknown"
        return f"{self.character.name} - {template_name}"

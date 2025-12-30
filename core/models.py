from core.constants import CharacterStatus, GameLine, ImageStatus
from core.utils import filepath
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from django.utils import timezone
from game.models import Chronicle
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel
from polymorphic.query import PolymorphicQuerySet


class ModelQuerySet(PolymorphicQuerySet):
    """
    Base queryset for all polymorphic models with default ContentType optimization.

    Automatically applies select_related('polymorphic_ctype') to prevent
    N+1 queries when resolving polymorphic types (e.g., determining if a
    Character is VtMHuman, Mage, Garou, etc.).
    """

    def pending_approval_for_user(self, user):
        """
        Objects awaiting approval in user's chronicles (optimized).
        Default implementation uses status in ['Un', 'Sub'].
        Override in subclasses if different status logic is needed.
        """
        return (
            self.filter(status__in=["Un", "Sub"], chronicle__in=user.chronicle_set.all())
            .select_related("chronicle", "owner")
            .order_by("name")
        )

    def visible(self):
        """Objects with display=True (visible to users)"""
        return self.filter(display=True)

    def for_chronicle(self, chronicle):
        """Objects in a specific chronicle"""
        return self.filter(chronicle=chronicle)

    def owned_by(self, user):
        """Objects owned by a specific user"""
        return self.filter(owner=user)

    def with_pending_images(self):
        """Objects with images awaiting approval"""
        return self.filter(image_status="sub").exclude(image="")

    def for_user_chronicles(self, user):
        """Objects in any of the user's chronicles"""
        return self.filter(chronicle__in=user.chronicle_set.all())


# Create custom manager with polymorphic_ctype optimization
class ModelManager(PolymorphicManager.from_queryset(ModelQuerySet)):
    """
    Manager for polymorphic models with automatic ContentType optimization.

    Applies select_related('polymorphic_ctype') by default to prevent N+1 queries
    when resolving polymorphic types. Uses Django's standard get_queryset() pattern
    instead of fragile internal query manipulation.
    """

    def get_queryset(self):
        """Return queryset with polymorphic_ctype optimization applied."""
        return super().get_queryset().select_related("polymorphic_ctype")


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
            ("DA", "Dark Ages"),
            ("VA", "Victorian Age"),
            ("WW", "Wild West"),
            ("SC", "Sorcerer's Crusade"),
            ("KotE", "Kindred of the East"),
        ],
        default="1e",
    )
    gameline = models.CharField(
        max_length=3,
        choices=settings.GAMELINE_CHOICES,
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

    def clean(self):
        """Validate book data before saving."""
        super().clean()
        errors = {}

        # Validate name is not empty
        if not self.name or not self.name.strip():
            errors["name"] = "Book name is required"

        # Validate gameline is in valid choices
        valid_gamelines = [choice[0] for choice in settings.GAMELINE_CHOICES]
        if self.gameline not in valid_gamelines:
            errors["gameline"] = (
                f"Invalid gameline '{self.gameline}'. Must be one of: {', '.join(valid_gamelines)}"
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure validation runs on save."""
        self.full_clean()
        super().save(*args, **kwargs)


class BookReference(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    page = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Book Reference"
        verbose_name_plural = "Book References"

    def __str__(self):
        return f"<i>{self.book}</i> p. {self.page}"

    def clean(self):
        """Validate book reference data before saving."""
        super().clean()
        errors = {}

        # Validate page number is non-negative
        if self.page < 0:
            errors["page"] = "Page number cannot be negative"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure validation runs on save."""
        self.full_clean()
        super().save(*args, **kwargs)


class Observer(models.Model):
    """
    Grants specific users observer access to any object.
    Uses generic foreign key to support Characters, Items, Locations, etc.
    """

    # Generic FK to any object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    # Who can observe
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="observing")

    # Metadata
    granted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="granted_observer_access",
    )
    granted_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = [["content_type", "object_id", "user"]]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["user"]),
        ]
        verbose_name = "Observer"
        verbose_name_plural = "Observers"

    def __str__(self):
        return f"{self.user.username} observing {self.content_object}"

    def clean(self):
        """Validate observer data before saving."""
        super().clean()
        errors = {}

        # Validate user is provided
        if not self.user_id:
            errors["user"] = "Observer must have a user"

        # Validate content_type and object_id are provided
        if not self.content_type_id:
            errors["content_type"] = "Content type is required"

        if not self.object_id:
            errors["object_id"] = "Object ID is required"

        # Validate the content object actually exists
        if self.content_type_id and self.object_id:
            try:
                model_class = self.content_type.model_class()
                if not model_class.objects.filter(pk=self.object_id).exists():
                    errors["object_id"] = (
                        f"No {model_class.__name__} with ID {self.object_id} exists"
                    )
            except Exception:
                pass  # If content_type isn't loaded yet, skip this check

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure validation runs on save."""
        self.full_clean()
        super().save(*args, **kwargs)


class PermissionMixin(models.Model):
    """
    Mixin for permission-controlled objects.
    Add to Character, ItemModel, LocationModel, etc.
    """

    visibility = models.CharField(
        max_length=3,
        choices=[
            ("PUB", "Public"),
            ("PRI", "Private"),
            ("CHR", "Chronicle Only"),
            ("CUS", "Custom"),
        ],
        default="PRI",
        help_text="Controls baseline visibility",
    )

    # Generic relation to observers
    observers = GenericRelation("core.Observer", related_query_name="%(class)s")

    class Meta:
        abstract = True

    def get_user_roles(self, user):
        """Get all roles user has for this object."""
        from core.permissions import PermissionManager

        return PermissionManager.get_user_roles(user, self)

    def user_can_view(self, user):
        """Check if user can view this object."""
        from core.permissions import PermissionManager

        return PermissionManager.user_can_view(user, self)

    def user_can_edit(self, user):
        """Check if user can edit this object (EDIT_FULL)."""
        from core.permissions import PermissionManager

        return PermissionManager.user_can_edit(user, self)

    def user_can_spend_xp(self, user):
        """Check if user can spend XP on this object."""
        from core.permissions import PermissionManager

        return PermissionManager.user_can_spend_xp(user, self)

    def user_can_spend_freebies(self, user):
        """Check if user can spend freebie points on this object."""
        from core.permissions import PermissionManager

        return PermissionManager.user_can_spend_freebies(user, self)

    def get_visibility_tier(self, user):
        """Get visibility tier for user."""
        from core.permissions import PermissionManager

        return PermissionManager.get_visibility_tier(user, self)

    def add_observer(self, user, granted_by):
        """Grant observer access to a user."""
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(self)
        Observer.objects.get_or_create(
            content_type=content_type,
            object_id=self.pk,
            user=user,
            defaults={"granted_by": granted_by},
        )

    def remove_observer(self, user):
        """Remove observer access."""
        self.observers.filter(user=user).delete()


class Model(PermissionMixin, PolymorphicModel):
    type = "model"
    gameline = "wod"  # Default gameline; override in subclasses

    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    chronicle = models.ForeignKey(Chronicle, blank=True, null=True, on_delete=models.SET_NULL)

    objects = ModelManager()

    status = models.CharField(
        max_length=3,
        choices=CharacterStatus.CHOICES,
        default=CharacterStatus.UNAPPROVED,
        db_index=True,
    )
    display = models.BooleanField(default=True)
    sources = models.ManyToManyField(BookReference, blank=True)
    description = models.TextField(default="", blank=True)
    public_info = models.TextField(default="", blank=True)
    image = models.ImageField(upload_to=filepath, blank=True, null=True)
    image_status = models.CharField(
        max_length=3,
        choices=ImageStatus.CHOICES,
        default=ImageStatus.SUBMITTED,
    )
    freebies_approved = models.BooleanField(default=False)

    st_notes = models.TextField(default="", blank=True)

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
        """
        Get the gameline code for this model.

        Returns the gameline class attribute, with 'wod' as a fallback
        for any model that doesn't explicitly define a gameline.

        Returns:
            str: Gameline code (e.g., 'vtm', 'wta', 'wod')
        """
        return getattr(self.__class__, "gameline", "wod")

    def get_full_gameline(self):
        """
        Get the full gameline name for this model.

        Returns:
            str: Full gameline name from settings (e.g., 'Vampire: the Masquerade')
        """
        from core.utils import get_gameline_name

        return get_gameline_name(self.get_gameline())

    def get_type(self):
        """
        Get a human-readable display version of the type.
        Replaces underscores with spaces and title-cases each word.

        Returns:
            str: Formatted type (e.g., 'autumn_person' -> 'Autumn Person')
        """
        return self.type.replace("_", " ").title()

    # Secondary/mortal types that get lighter badges
    # Everything else is considered "primary" and gets full-color badges
    SECONDARY_TYPES = {
        "vtm_human",
        "wta_human",
        "mta_human",
        "ctd_human",
        "wto_human",
        "dtf_human",
        "mtr_human",
        "htr_human",
        "spirit_character",
    }

    def is_primary_type(self):
        """
        Check if this object's type is a primary supernatural type.
        Primary types get full-color badges, secondary/mortal types get lighter badges.

        Returns:
            bool: True if primary type, False otherwise
        """
        return self.type not in self.SECONDARY_TYPES

    def get_badge_class(self):
        """
        Get the CSS badge class for this object based on gameline and type.
        Returns classes like 'badge-mta', 'badge-vtm-light', 'badge-secondary'.

        Returns:
            str: CSS class name for the badge
        """
        gameline = self.get_gameline()
        if gameline == "wod":
            return "badge-secondary"

        if self.is_primary_type():
            return f"badge-{gameline}"
        else:
            return f"badge-{gameline}-light"

    @property
    def status_keys(self):
        """Return valid status keys from CharacterStatus."""
        return [key for key, _ in CharacterStatus.CHOICES]

    @property
    def image_status_keys(self):
        """Return valid image status keys from ImageStatus."""
        return [key for key, _ in ImageStatus.CHOICES]

    def clean(self):
        """Validate model data before saving."""
        super().clean()
        errors = {}

        # Validate name is not empty
        if not self.name or not self.name.strip():
            errors["name"] = "Name is required"

        # Validate status is in valid choices
        if self.status not in self.status_keys:
            errors["status"] = (
                f"Invalid status '{self.status}'. Must be one of: {', '.join(self.status_keys)}"
            )

        # Validate image_status is in valid choices
        if self.image_status not in self.image_status_keys:
            errors["image_status"] = (
                f"Invalid image status '{self.image_status}'. Must be one of: {', '.join(self.image_status_keys)}"
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure validation runs on save unless skip_validation=True."""
        if not kwargs.pop("skip_validation", False):
            self.full_clean()
        super().save(*args, **kwargs)


class NewsItem(models.Model):
    title = models.CharField(default="", max_length=100)
    content = models.TextField(default="")
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "News Item"
        verbose_name_plural = "News Items"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("newsitem", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("update_newsitem", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("create_newsitem")

    def clean(self):
        """Validate news item data before saving."""
        super().clean()
        errors = {}

        # Validate title is not empty
        if not self.title or not self.title.strip():
            errors["title"] = "Title is required"

        # Validate content is not empty
        if not self.content or not self.content.strip():
            errors["content"] = "Content is required"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure validation runs on save."""
        self.full_clean()
        super().save(*args, **kwargs)


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

    def clean(self):
        """Validate language data before saving."""
        super().clean()
        errors = {}

        # Validate name is not empty
        if not self.name or not self.name.strip():
            errors["name"] = "Language name is required"

        # Validate frequency is non-negative
        if self.frequency < 0:
            errors["frequency"] = "Frequency cannot be negative"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure validation runs on save."""
        self.full_clean()
        super().save(*args, **kwargs)


class Number(models.Model):
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.value)


class BaseMeritFlawRating(models.Model):
    """
    Abstract base class for MeritFlaw rating through-models.

    Provides the common `mf` foreign key and `rating` field with validators.
    Concrete subclasses must define:
    - A parent FK (e.g., `character`, `node`, `haven`, `tomb`)
    - Their own Meta class with constraints and unique_together as needed
    """

    mf = models.ForeignKey(
        "characters.MeritFlaw",
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(-10), MaxValueValidator(10)],
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.mf}: {self.rating}"


class BaseBackgroundRating(models.Model):
    """
    Abstract base class for Background rating through-models.

    Provides common fields for all Background ratings:
    - bg: Foreign key to Background
    - rating: Integer 0-10
    - note: Optional note about this rating
    - url: Optional URL for more info
    - complete: Whether the background is complete

    Concrete subclasses must define:
    - A parent FK (e.g., `char`, `group`, `chantry`)
    - Any additional fields (e.g., `pooled`, `display_alt_name`)
    - Their own Meta class with constraints and ordering as needed
    """

    bg = models.ForeignKey(
        "characters.Background",
        on_delete=models.SET_NULL,
        null=True,
    )
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    note = models.CharField(max_length=100, default="", blank=True)
    url = models.CharField(max_length=500, default="", blank=True)
    complete = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.bg} ({self.note})"


class Noun(models.Model):
    name = models.TextField(default="")

    class Meta:
        verbose_name = "Noun"
        verbose_name_plural = "Nouns"

    def __str__(self):
        return self.name

    def clean(self):
        """Validate noun data before saving."""
        super().clean()
        errors = {}

        # Validate name is not empty
        if not self.name or not self.name.strip():
            errors["name"] = "Noun name is required"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure validation runs on save."""
        self.full_clean()
        super().save(*args, **kwargs)


class HouseRule(models.Model):
    name = models.CharField(default="", max_length=100)
    sources = models.ManyToManyField(BookReference, blank=True)
    description = models.TextField(default="", blank=True)
    chronicle = models.ForeignKey(Chronicle, blank=True, null=True, on_delete=models.SET_NULL)
    gameline = models.CharField(
        max_length=3,
        choices=settings.GAMELINE_CHOICES,
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

    def clean(self):
        """Validate house rule data before saving."""
        super().clean()
        errors = {}

        # Validate name is not empty
        if not self.name or not self.name.strip():
            errors["name"] = "House rule name is required"

        # Validate gameline is in valid choices
        valid_gamelines = [choice[0] for choice in settings.GAMELINE_CHOICES]
        if self.gameline not in valid_gamelines:
            errors["gameline"] = (
                f"Invalid gameline '{self.gameline}'. Must be one of: {', '.join(valid_gamelines)}"
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure validation runs on save."""
        self.full_clean()
        super().save(*args, **kwargs)


class CharacterTemplate(Model):
    """
    Pre-configured character templates for quick character creation.
    Stores character data as JSON and can apply it to new characters.

    Inherits from Model to get: name, description, sources (via add_source()),
    owner, chronicle, status, and permission system.
    """

    type = "character_template"

    # Template-specific fields
    gameline = models.CharField(
        max_length=3,
        choices=GameLine.CHOICES,
        default=GameLine.WOD,
    )
    character_type = models.CharField(
        max_length=50,
        help_text="e.g., 'mage', 'vampire', 'werewolf', 'changeling', 'wraith', 'demon'",
    )
    concept = models.CharField(max_length=200, blank=True)
    faction = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional faction/clan/tribe/tradition name (e.g., 'Brujah', 'Glass Walkers', 'Virtual Adepts')",
    )

    # Character Data (stored as JSON)
    # Note: default=list and default=dict are safe in Django's JSONField.
    # Django treats them as callable factories, calling them each time to get a fresh instance.
    basic_info = models.JSONField(
        default=dict, blank=True, help_text="Nature, demeanor, concept, etc."
    )
    attributes = models.JSONField(default=dict, blank=True, help_text="Strength, dexterity, etc.")
    abilities = models.JSONField(
        default=dict, blank=True, help_text="Alertness, investigation, etc."
    )
    backgrounds = models.JSONField(
        default=list, blank=True, help_text="List of {name, rating} dicts"
    )
    powers = models.JSONField(
        default=dict, blank=True, help_text="Disciplines, spheres, gifts, etc."
    )
    merits_flaws = models.JSONField(
        default=list, blank=True, help_text="List of {name, rating} dicts"
    )
    specialties = models.JSONField(
        default=list, blank=True, help_text="List of 'Ability (Specialty)' strings"
    )
    languages = models.JSONField(default=list, blank=True, help_text="List of language names")
    equipment = models.TextField(blank=True, help_text="Starting gear description")
    suggested_freebie_spending = models.JSONField(
        default=dict, blank=True, help_text="Suggested allocation"
    )

    # Metadata
    is_official = models.BooleanField(
        default=True, help_text="Official WW template vs user-created"
    )
    is_public = models.BooleanField(default=True, help_text="Available to all users")
    times_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Character Template"
        verbose_name_plural = "Character Templates"
        unique_together = [["gameline", "character_type", "name"]]
        indexes = [
            models.Index(fields=["gameline", "character_type"]),
            models.Index(fields=["is_public"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_gameline_display()})"

    def apply_to_character(self, character):
        """
        Apply this template to a character instance.
        Handles FK resolution, attribute setting, and related object creation.
        """
        # Import here to avoid circular imports
        from characters.models.core.archetype import Archetype
        from characters.models.core.background_block import Background, BackgroundRating
        from characters.models.core.merit_flaw_block import MeritFlaw, MeritFlawRating

        # 1. Apply basic info (nature, demeanor, etc.)
        for field, value in self.basic_info.items():
            if value and isinstance(value, str) and value.startswith("FK:"):
                # Resolve foreign key: "FK:Model:Name"
                _, model_name, obj_name = value.split(":")
                if model_name == "Archetype":
                    try:
                        obj = Archetype.objects.get(name=obj_name)
                        setattr(character, field, obj)
                    except Archetype.DoesNotExist:
                        pass
            elif hasattr(character, field):
                setattr(character, field, value)

        # 2. Apply attributes
        for attr_name, rating in self.attributes.items():
            if hasattr(character, attr_name):
                setattr(character, attr_name, rating)

        # 3. Apply abilities
        for ability_name, rating in self.abilities.items():
            if hasattr(character, ability_name):
                setattr(character, ability_name, rating)

        # 4. Apply backgrounds
        for bg_data in self.backgrounds:
            try:
                background = Background.objects.get(name=bg_data["name"])
                BackgroundRating.objects.get_or_create(
                    character=character,
                    bg=background,
                    defaults={"rating": bg_data.get("rating", 0)},
                )
            except Background.DoesNotExist:
                pass

        # 5. Apply powers (disciplines, spheres, gifts, etc.)
        for power_name, rating in self.powers.items():
            if hasattr(character, power_name):
                setattr(character, power_name, rating)

        # 6. Apply merits/flaws
        for mf_data in self.merits_flaws:
            try:
                merit_flaw = MeritFlaw.objects.get(name=mf_data["name"])
                MeritFlawRating.objects.get_or_create(
                    character=character,
                    mf=merit_flaw,
                    defaults={"rating": mf_data.get("rating", 0)},
                )
            except MeritFlaw.DoesNotExist:
                pass

        # 7. Apply languages
        for lang_name in self.languages:
            try:
                language = Language.objects.get(name=lang_name)
                character.languages.add(language)
            except Language.DoesNotExist:
                pass

        # 8. Apply specialties
        from characters.models.core.ability_block import Ability
        from characters.models.core.specialty import Specialty

        for specialty_str in self.specialties:
            # Format: "Ability (Specialty)"
            if "(" in specialty_str and ")" in specialty_str:
                ability_name = specialty_str.split("(")[0].strip()
                specialty_name = specialty_str.split("(")[1].split(")")[0].strip()
                try:
                    ability = Ability.objects.get(name=ability_name)
                    Specialty.objects.get_or_create(
                        character=character,
                        skill=ability,
                        defaults={"name": specialty_name},
                    )
                except Ability.DoesNotExist:
                    pass

        # Save character
        character.save()

        # 9. Create application record
        TemplateApplication.objects.create(character=character, template=self)

        # 10. Increment usage counter
        self.times_used += 1
        self.save(update_fields=["times_used"])

    def clean(self):
        """Validate character template data before saving."""
        super().clean()
        errors = {}

        # Validate character_type is not empty
        if not self.character_type or not self.character_type.strip():
            errors["character_type"] = "Character type is required"

        # Validate gameline is in valid choices (already done in Model, but verify)
        valid_gamelines = ["wod", "vtm", "wta", "mta", "wto", "ctd", "dtf"]
        if self.gameline not in valid_gamelines:
            errors["gameline"] = (
                f"Invalid gameline '{self.gameline}'. Must be one of: {', '.join(valid_gamelines)}"
            )

        if errors:
            raise ValidationError(errors)

    # Note: save() method inherited from Model base class already calls full_clean()


class TemplateApplication(models.Model):
    """
    Tracks when a template is applied to a character.
    Used for statistics and auditing.
    """

    character = models.ForeignKey(
        "characters.Character",
        on_delete=models.CASCADE,
        related_name="template_applications",
    )
    template = models.ForeignKey(
        CharacterTemplate,
        on_delete=models.SET_NULL,
        null=True,
        related_name="applications",
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Template Application"
        verbose_name_plural = "Template Applications"

    def __str__(self):
        return f"{self.template.name} → {self.character.name} ({self.applied_at.date()})"

    def clean(self):
        """Validate template application data before saving."""
        super().clean()
        errors = {}

        # Validate character is provided
        if not self.character_id:
            errors["character"] = "Character is required"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure validation runs on save."""
        self.full_clean()
        super().save(*args, **kwargs)

from core.models import (
    Book,
    BookReference,
    CharacterTemplate,
    HouseRule,
    Language,
    NewsItem,
    TemplateApplication,
)
from django.contrib import admin

admin.site.register(NewsItem)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


admin.site.register(BookReference)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"


admin.site.register(HouseRule)


@admin.register(CharacterTemplate)
class CharacterTemplateAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "gameline",
        "character_type",
        "concept",
        "is_official",
        "is_public",
        "times_used",
        "status",
        "created_at",
    ]
    list_filter = [
        "gameline",
        "character_type",
        "is_official",
        "is_public",
        "status",
        "created_at",
    ]
    search_fields = ["name", "description", "concept"]
    readonly_fields = ["times_used", "created_at", "updated_at"]

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "gameline",
                    "character_type",
                    "concept",
                    "description",
                )
            },
        ),
        (
            "Sources",
            {
                "fields": ("sources",),
                "description": "Use the add_source() method or manage sources here",
            },
        ),
        (
            "Character Data",
            {
                "fields": (
                    "basic_info",
                    "attributes",
                    "abilities",
                    "backgrounds",
                    "powers",
                    "merits_flaws",
                    "specialties",
                    "languages",
                    "equipment",
                    "suggested_freebie_spending",
                ),
                "classes": ["collapse"],
            },
        ),
        (
            "Metadata & Permissions",
            {
                "fields": (
                    "is_official",
                    "is_public",
                    "owner",
                    "chronicle",
                    "status",
                    "visibility",
                    "display",
                    "times_used",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(TemplateApplication)
class TemplateApplicationAdmin(admin.ModelAdmin):
    list_display = ["character", "template", "applied_at"]
    list_filter = ["applied_at", "template__gameline"]
    search_fields = ["character__name", "template__name"]
    readonly_fields = ["applied_at"]
    raw_id_fields = ["character"]

    class Meta:
        verbose_name = "Template Application"
        verbose_name_plural = "Template Applications"

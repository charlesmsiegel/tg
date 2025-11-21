from core.models import (
    Book,
    BookReference,
    # CharacterTemplate,  # TODO: Model not yet implemented
    HouseRule,
    Language,
    NewsItem,
    # TemplateApplication,  # TODO: Model not yet implemented
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


# TODO: Uncomment when CharacterTemplate model is implemented in core/models.py
# @admin.register(CharacterTemplate)
# class CharacterTemplateAdmin(admin.ModelAdmin):
#     list_display = [
#         "name",
#         "gameline",
#         "character_type",
#         "concept",
#         "is_official",
#         "is_public",
#         "times_used",
#         "created_at",
#     ]
#     list_filter = ["gameline", "character_type", "is_official", "is_public", "created_at"]
#     search_fields = ["name", "description", "source_book", "concept"]
#     readonly_fields = ["times_used", "created_at", "updated_at"]
#
#     fieldsets = (
#         (
#             "Basic Info",
#             {
#                 "fields": (
#                     "name",
#                     "gameline",
#                     "character_type",
#                     "concept",
#                     "description",
#                     "source_book",
#                 )
#             },
#         ),
#         (
#             "Character Data",
#             {
#                 "fields": (
#                     "basic_info",
#                     "attributes",
#                     "abilities",
#                     "backgrounds",
#                     "powers",
#                     "merits_flaws",
#                     "specialties",
#                     "languages",
#                     "equipment",
#                     "suggested_freebie_spending",
#                 ),
#                 "classes": ["collapse"],
#             },
#         ),
#         (
#             "Metadata",
#             {
#                 "fields": (
#                     "is_official",
#                     "is_public",
#                     "created_by",
#                     "times_used",
#                     "created_at",
#                     "updated_at",
#                 )
#             },
#         ),
#     )
#
#     class Meta:
#         verbose_name = "Character Template"
#         verbose_name_plural = "Character Templates"


# TODO: Uncomment when TemplateApplication model is implemented in core/models.py
# @admin.register(TemplateApplication)
# class TemplateApplicationAdmin(admin.ModelAdmin):
#     list_display = ["character", "template", "applied_at"]
#     list_filter = ["applied_at", "template__gameline"]
#     search_fields = ["character__name", "template__name"]
#     readonly_fields = ["applied_at"]
#     raw_id_fields = ["character"]
#
#     class Meta:
#         verbose_name = "Template Application"
#         verbose_name_plural = "Template Applications"

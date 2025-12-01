from django.contrib import admin
from game.models import (
    Chronicle,
    FreebieSpendingRecord,
    Gameline,
    Journal,
    JournalEntry,
    ObjectType,
    Post,
    Scene,
    SettingElement,
    Story,
    StoryXPRequest,
    STRelationship,
    UserSceneReadStatus,
    Week,
    WeeklyXPRequest,
    XPSpendingRequest,
)


@admin.register(Chronicle)
class ChronicleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "head_st",
        "storyteller_list",
        "headings",
        "year",
        "total_scenes",
    )
    list_filter = ("headings", "year")
    search_fields = ("name", "theme", "mood")
    filter_horizontal = ("common_knowledge_elements", "allowed_objects", "game_storytellers")

    fieldsets = (
        ("Basic Information", {"fields": ("name", "headings", "year")}),
        ("Narrative", {"fields": ("theme", "mood", "common_knowledge_elements")}),
        ("Storytellers", {"fields": ("head_st", "game_storytellers")}),
        ("Game Configuration", {"fields": ("allowed_objects",)}),
    )


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "chronicle",
        "location",
        "finished",
        "xp_given",
        "waiting_for_st",
        "num_pcs",
        "total_posts",
    )
    list_filter = ("chronicle", "finished", "xp_given", "waiting_for_st")

    def num_pcs(self, obj):
        return obj.characters.player_characters().count()

    def total_posts(self, obj):
        return obj.total_posts()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("character", "display_name", "scene", "message")
    list_filter = ("scene", "character", "display_name")


@admin.register(SettingElement)
class SettingElementAdmin(admin.ModelAdmin):
    list_display = ("name", "gameline", "description")
    list_filter = ("gameline",)
    search_fields = ("name", "description")


@admin.register(ObjectType)
class ObjectTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "gameline")
    list_filter = ("type", "gameline")
    search_fields = ("name",)


@admin.register(Gameline)
class GamelineAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(STRelationship)
class STRelationshipAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "chronicle",
        "gameline",
    )


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ("start_date", "end_date", "num_characters", "num_scenes")
    list_filter = ("end_date",)
    filter_horizontal = ("characters",)

    def num_characters(self, obj):
        return obj.characters.count()

    num_characters.short_description = "Characters"

    def num_scenes(self, obj):
        return obj.finished_scenes().count()

    num_scenes.short_description = "Finished Scenes"


@admin.register(WeeklyXPRequest)
class WeeklyXPRequestAdmin(admin.ModelAdmin):
    list_display = (
        "character",
        "week",
        "total_xp",
        "finishing",
        "learning",
        "rp",
        "focus",
        "standingout",
        "approved",
    )
    list_filter = ("approved", "week")
    search_fields = ("character__name",)
    readonly_fields = ("total_xp",)

    fieldsets = (
        ("Basic Information", {"fields": ("character", "week", "approved")}),
        (
            "XP Categories",
            {
                "fields": (
                    "finishing",
                    ("learning", "learning_scene"),
                    ("rp", "rp_scene"),
                    ("focus", "focus_scene"),
                    ("standingout", "standingout_scene"),
                )
            },
        ),
        ("Summary", {"fields": ("total_xp",)}),
    )


@admin.register(StoryXPRequest)
class StoryXPRequestAdmin(admin.ModelAdmin):
    list_display = (
        "character",
        "story",
        "success",
        "danger",
        "growth",
        "drama",
        "duration",
        "total_xp",
    )
    list_filter = ("story", "success", "danger", "growth", "drama")
    search_fields = ("character__name", "story__name")

    def total_xp(self, obj):
        return sum([obj.success, obj.danger, obj.growth, obj.drama]) + obj.duration

    total_xp.short_description = "Total XP"


@admin.register(UserSceneReadStatus)
class UserSceneReadStatusAdmin(admin.ModelAdmin):
    list_display = ("user", "scene", "read")
    list_filter = ("read", "scene")
    search_fields = ("user__username", "scene__name")


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("character", "num_entries")
    search_fields = ("character__name",)

    def num_entries(self, obj):
        return obj.all_entries().count()

    num_entries.short_description = "Entries"


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("journal", "date", "datetime_created", "has_message", "has_st_message")
    list_filter = ("journal", "date")
    search_fields = ("journal__character__name", "message", "st_message")
    readonly_fields = ("datetime_created",)

    def has_message(self, obj):
        return bool(obj.message)

    has_message.boolean = True
    has_message.short_description = "Has Message"

    def has_st_message(self, obj):
        return bool(obj.st_message)

    has_st_message.boolean = True
    has_st_message.short_description = "Has ST Message"


@admin.register(XPSpendingRequest)
class XPSpendingRequestAdmin(admin.ModelAdmin):
    list_display = (
        "character",
        "trait_name",
        "trait_type",
        "trait_value",
        "cost",
        "approved",
        "created_at",
        "approved_by",
    )
    list_filter = ("approved", "trait_type", "created_at")
    search_fields = ("character__name", "trait_name")
    readonly_fields = ("created_at", "approved_at")

    fieldsets = (
        (
            "Request Information",
            {"fields": ("character", "trait_name", "trait_type", "trait_value", "cost")},
        ),
        ("Approval", {"fields": ("approved", "approved_by", "approved_at")}),
        ("Timestamps", {"fields": ("created_at",)}),
    )


@admin.register(FreebieSpendingRecord)
class FreebieSpendingRecordAdmin(admin.ModelAdmin):
    list_display = (
        "character",
        "trait_name",
        "trait_type",
        "trait_value",
        "cost",
        "created_at",
    )
    list_filter = ("trait_type", "created_at")
    search_fields = ("character__name", "trait_name")
    readonly_fields = ("created_at",)

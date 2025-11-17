from django.contrib import admin
from game.models import (
    Chronicle,
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
)

admin.site.register(Chronicle)


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
        return obj.characters.filter(npc=False).count()

    def total_posts(self, obj):
        return obj.total_posts()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("character", "display_name", "scene", "message")
    list_filter = ("scene", "character", "display_name")


admin.site.register(SettingElement)
admin.site.register(ObjectType)

admin.site.register(Gameline)


@admin.register(STRelationship)
class STRelationshipAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "chronicle",
        "gameline",
    )


admin.site.register(Story)
admin.site.register(Week)
admin.site.register(WeeklyXPRequest)
admin.site.register(StoryXPRequest)
admin.site.register(UserSceneReadStatus)


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("character",)


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("journal", "date", "datetime_created")
    list_filter = ("journal", "date")

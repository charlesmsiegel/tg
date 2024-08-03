from django.contrib import admin
from game.models import Chronicle, Post, Scene, Story

# Register your models here.
admin.site.register(Chronicle)


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "story",
        "location",
        "finished",
    )


admin.site.register(Post)

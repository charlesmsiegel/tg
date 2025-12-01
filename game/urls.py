from characters import views as char_views
from django.urls import include, path
from game import views

app_name = "game"

story_urls = [
    path("list/", views.StoryListView.as_view(), name="list"),
    path("<pk>/", views.StoryDetailView.as_view(), name="detail"),
    path("create/", views.StoryCreateView.as_view(), name="create"),
    path("<pk>/update/", views.StoryUpdateView.as_view(), name="update"),
]

week_urls = [
    path("list/", views.WeekListView.as_view(), name="list"),
    path("<pk>/", views.WeekDetailView.as_view(), name="detail"),
    path("create/", views.WeekCreateView.as_view(), name="create"),
    path("<pk>/update/", views.WeekUpdateView.as_view(), name="update"),
]

weekly_xp_request_urls = [
    path("list/", views.WeeklyXPRequestListView.as_view(), name="list"),
    path("<pk>/", views.WeeklyXPRequestDetailView.as_view(), name="detail"),
    path(
        "create/<week_pk>/<character_pk>/",
        views.WeeklyXPRequestCreateView.as_view(),
        name="create",
    ),
    path("<pk>/approve/", views.WeeklyXPRequestApproveView.as_view(), name="approve"),
    path(
        "batch-approve/",
        views.WeeklyXPRequestBatchApproveView.as_view(),
        name="batch_approve",
    ),
]

story_xp_request_urls = [
    path("list/", views.StoryXPRequestListView.as_view(), name="list"),
    path("<pk>/", views.StoryXPRequestDetailView.as_view(), name="detail"),
]

setting_element_urls = [
    path("list/", views.SettingElementListView.as_view(), name="list"),
    path("<pk>/", views.SettingElementDetailView.as_view(), name="detail"),
    path("create/", views.SettingElementCreateView.as_view(), name="create"),
    path("<pk>/update/", views.SettingElementUpdateView.as_view(), name="update"),
]

urlpatterns = [
    path("chronicles/", views.ChronicleListView.as_view(), name="chronicles"),
    path("chronicle/<pk>", views.ChronicleDetailView.as_view(), name="chronicle"),
    path(
        "chronicle/<pk>/scenes/",
        views.ChronicleScenesDetailView.as_view(),
        name="chronicle_scenes",
    ),
    path(
        "chronicle/<pk>/retired/",
        char_views.core.RetiredCharacterIndex.as_view(),
        name="retired",
    ),
    path(
        "chronicle/<pk>/deceased/",
        char_views.core.DeceasedCharacterIndex.as_view(),
        name="deceased",
    ),
    path("chronicle/<pk>/npc/", char_views.core.NPCCharacterIndex.as_view(), name="npc"),
    path("scenes/", views.SceneListView.as_view(), name="scenes"),
    path("scene/<pk>", views.SceneDetailView.as_view(), name="scene"),
    path("commands/", views.CommandsView.as_view(), name="commands"),
    path("journals/", views.JournalListView.as_view(), name="journals"),
    path("journal/<pk>", views.JournalDetailView.as_view(), name="journal"),
    path("story/", include((story_urls, "story"))),
    path("week/", include((week_urls, "week"))),
    path("weekly-xp-request/", include((weekly_xp_request_urls, "weekly_xp_request"))),
    path("story-xp-request/", include((story_xp_request_urls, "story_xp_request"))),
    path("setting-element/", include((setting_element_urls, "setting_element"))),
]

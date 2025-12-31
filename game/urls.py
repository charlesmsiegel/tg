from characters import views as char_views
from django.urls import include, path
from game import views

app_name = "game"

story_urls = [
    path("list/", views.StoryListView.as_view(), name="list"),
    path("create/", views.StoryCreateView.as_view(), name="create"),
    path("<int:pk>/", views.StoryDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.StoryUpdateView.as_view(), name="update"),
]

week_urls = [
    path("list/", views.WeekListView.as_view(), name="list"),
    path("create/", views.WeekCreateView.as_view(), name="create"),
    path("<int:pk>/", views.WeekDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.WeekUpdateView.as_view(), name="update"),
]

weekly_xp_request_urls = [
    path("list/", views.WeeklyXPRequestListView.as_view(), name="list"),
    path(
        "create/<int:week_pk>/<int:character_pk>/",
        views.WeeklyXPRequestCreateView.as_view(),
        name="create",
    ),
    path(
        "batch-approve/",
        views.WeeklyXPRequestBatchApproveView.as_view(),
        name="batch_approve",
    ),
    path("<int:pk>/", views.WeeklyXPRequestDetailView.as_view(), name="detail"),
    path("<int:pk>/approve/", views.WeeklyXPRequestApproveView.as_view(), name="approve"),
]

story_xp_request_urls = [
    path("list/", views.StoryXPRequestListView.as_view(), name="list"),
    path(
        "create/<int:character_pk>/",
        views.StoryXPRequestCreateView.as_view(),
        name="create",
    ),
    path("<int:pk>/", views.StoryXPRequestDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.StoryXPRequestUpdateView.as_view(), name="update"),
]

setting_element_urls = [
    path("list/", views.SettingElementListView.as_view(), name="list"),
    path("create/", views.SettingElementCreateView.as_view(), name="create"),
    path("<int:pk>/", views.SettingElementDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.SettingElementUpdateView.as_view(), name="update"),
]

xp_spending_request_urls = [
    path("list/", views.XPSpendingRequestListView.as_view(), name="list"),
    path(
        "create/<int:character_pk>/",
        views.XPSpendingRequestCreateView.as_view(),
        name="create",
    ),
    path("<int:pk>/", views.XPSpendingRequestDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.XPSpendingRequestUpdateView.as_view(), name="update"),
    path("<int:pk>/approve/", views.XPSpendingRequestApproveView.as_view(), name="approve"),
]

freebie_spending_record_urls = [
    path("list/", views.FreebieSpendingRecordListView.as_view(), name="list"),
    path(
        "create/<int:character_pk>/",
        views.FreebieSpendingRecordCreateView.as_view(),
        name="create",
    ),
    path("<int:pk>/", views.FreebieSpendingRecordDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.FreebieSpendingRecordUpdateView.as_view(), name="update"),
]

chronicle_urls = [
    path("create/", views.ChronicleCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.ChronicleUpdateView.as_view(), name="update"),
]

scene_urls = [
    path("create/", views.SceneCreateView.as_view(), name="create"),
    path(
        "create/<int:chronicle_pk>/",
        views.SceneCreateView.as_view(),
        name="create_for_chronicle",
    ),
    path("<int:pk>/update/", views.SceneUpdateView.as_view(), name="update"),
]

urlpatterns = [
    path("chronicles/", views.ChronicleListView.as_view(), name="chronicles"),
    path("chronicle/<int:pk>", views.ChronicleDetailView.as_view(), name="chronicle"),
    path(
        "chronicle/<int:pk>/retired/",
        char_views.core.RetiredCharacterIndex.as_view(),
        name="retired",
    ),
    path(
        "chronicle/<int:pk>/deceased/",
        char_views.core.DeceasedCharacterIndex.as_view(),
        name="deceased",
    ),
    path("chronicle/<int:pk>/npc/", char_views.core.NPCCharacterIndex.as_view(), name="npc"),
    path("scenes/", views.SceneListView.as_view(), name="scenes"),
    path("scene/<int:pk>", views.SceneDetailView.as_view(), name="scene"),
    path("commands/", views.CommandsView.as_view(), name="commands"),
    path("journals/", views.JournalListView.as_view(), name="journals"),
    path("journal/<int:pk>", views.JournalDetailView.as_view(), name="journal"),
    path("story/", include((story_urls, "story"))),
    path("week/", include((week_urls, "week"))),
    path("weekly-xp-request/", include((weekly_xp_request_urls, "weekly_xp_request"))),
    path("story-xp-request/", include((story_xp_request_urls, "story_xp_request"))),
    path("setting-element/", include((setting_element_urls, "setting_element"))),
    path("xp-spending-request/", include((xp_spending_request_urls, "xp_spending_request"))),
    path(
        "freebie-spending-record/",
        include((freebie_spending_record_urls, "freebie_spending_record")),
    ),
    path("chronicle-manage/", include((chronicle_urls, "chronicle_manage"))),
    path("scene-manage/", include((scene_urls, "scene_manage"))),
]

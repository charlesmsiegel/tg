from django.urls import path

from accounts import views
from core import views as core_views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("profile/update/<pk>/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/<pk>/", views.ProfileView.as_view(), name="profile"),
    path(
        "scene/<int:scene_pk>/award-xp/",
        views.SceneXPAwardView.as_view(),
        name="scene_xp_award",
    ),
    path(
        "scene/<int:scene_pk>/mark-read/",
        views.MarkSceneReadView.as_view(),
        name="mark_scene_read",
    ),
    path(
        "approve/<str:object_type>/<int:pk>/",
        views.ObjectApprovalView.as_view(),
        name="object_approval",
    ),
    path(
        "approve-image/<str:object_type>/<int:pk>/",
        views.ImageApprovalView.as_view(),
        name="image_approval",
    ),
    path(
        "character/<int:character_pk>/award-freebies/",
        views.FreebieAwardView.as_view(),
        name="freebie_award",
    ),
    path(
        "weekly-xp/<int:week_pk>/<int:character_pk>/request/",
        views.WeeklyXPRequestView.as_view(),
        name="weekly_xp_request",
    ),
    path(
        "weekly-xp/<int:week_pk>/<int:character_pk>/approve/",
        views.WeeklyXPApprovalView.as_view(),
        name="weekly_xp_approval",
    ),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("", core_views.HomeListView.as_view(), name="user"),
]

from django.urls import path

from items import views

app_name = "items:detail"
urls = [
    path("material/<pk>/", views.core.MaterialDetailView.as_view(), name="material"),
    path("medium/<pk>/", views.core.MediumDetailView.as_view(), name="medium"),
    path("weapon/<pk>/", views.core.WeaponDetailView.as_view(), name="weapon"),
    path(
        "melee_weapon/<pk>/",
        views.core.MeleeWeaponDetailView.as_view(),
        name="melee_weapon",
    ),
    path(
        "ranged_weapon/<pk>/",
        views.core.RangedWeaponDetailView.as_view(),
        name="ranged_weapon",
    ),
    path(
        "thrown_weapon/<pk>/",
        views.core.ThrownWeaponDetailView.as_view(),
        name="thrown_weapon",
    ),
    path("<pk>/", views.core.GenericItemDetailView.as_view(), name="item"),
]

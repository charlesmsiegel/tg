from django.urls import path
from items import views

urls = [
    path("material/", views.core.MaterialListView.as_view(), name="material"),
    path("medium/", views.core.MediumListView.as_view(), name="medium"),
    path("weapon/", views.core.WeaponListView.as_view(), name="weapon"),
    path("melee_weapon/", views.core.MeleeWeaponListView.as_view(), name="melee_weapon"),
    path(
        "ranged_weapon/",
        views.core.RangedWeaponListView.as_view(),
        name="ranged_weapon",
    ),
    path(
        "thrown_weapon/",
        views.core.ThrownWeaponListView.as_view(),
        name="thrown_weapon",
    ),
]

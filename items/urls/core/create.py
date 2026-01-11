from django.urls import path

from items import views

app_name = "items:create"
urls = [
    path("item/", views.core.ItemCreateView.as_view(), name="item"),
    path(
        "weapon/",
        views.core.WeaponCreateView.as_view(),
        name="weapon",
    ),
    path(
        "meleeweapon/",
        views.core.MeleeWeaponCreateView.as_view(),
        name="melee_weapon",
    ),
    path(
        "rangedweapon/",
        views.core.RangedWeaponCreateView.as_view(),
        name="ranged_weapon",
    ),
    path(
        "thrownweapon/",
        views.core.ThrownWeaponCreateView.as_view(),
        name="thrown_weapon",
    ),
    path(
        "material/",
        views.core.MaterialCreateView.as_view(),
        name="material",
    ),
    path(
        "medium/",
        views.core.MediumCreateView.as_view(),
        name="medium",
    ),
]

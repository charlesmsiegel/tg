from django.urls import path

from items import views

app_name = "items:update"
urls = [
    path(
        "item/<pk>/",
        views.core.ItemUpdateView.as_view(),
        name="item",
    ),
    path(
        "weapon/<pk>/",
        views.core.WeaponUpdateView.as_view(),
        name="weapon",
    ),
    path(
        "meleeweapon/<pk>/",
        views.core.MeleeWeaponUpdateView.as_view(),
        name="melee_weapon",
    ),
    path(
        "rangedweapon/<pk>/",
        views.core.RangedWeaponUpdateView.as_view(),
        name="ranged_weapon",
    ),
    path(
        "thrownweapon/<pk>/",
        views.core.ThrownWeaponUpdateView.as_view(),
        name="thrown_weapon",
    ),
    path(
        "material/<pk>/",
        views.core.MaterialUpdateView.as_view(),
        name="material",
    ),
    path(
        "medium/<pk>/",
        views.core.MediumUpdateView.as_view(),
        name="medium",
    ),
]

from django.urls import path
from items import views

urls = [
    path(
        "wonder/<pk>/",
        views.mage.WonderUpdateView.as_view(),
        name="wonder",
    ),
    path(
        "charm/<pk>/",
        views.mage.CharmUpdateView.as_view(),
        name="charm",
    ),
    path(
        "artifact/<pk>/",
        views.mage.ArtifactUpdateView.as_view(),
        name="artifact",
    ),
    path(
        "talisman/<pk>/",
        views.mage.TalismanUpdateView.as_view(),
        name="talisman",
    ),
    path(
        "grimoire/<pk>/",
        views.mage.GrimoireUpdateView.as_view(),
        name="grimoire",
    ),
    path(
        "sorcerer_artifact/<pk>/",
        views.mage.SorcererArtifactUpdateView.as_view(),
        name="sorcerer_artifact",
    ),
]

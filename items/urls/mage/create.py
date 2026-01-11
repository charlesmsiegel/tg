from django.urls import path

from items import views

urls = [
    path(
        "wonder/",
        views.mage.WonderCreateView.as_view(),
        name="wonder",
    ),
    path(
        "charm/",
        views.mage.CharmCreateView.as_view(),
        name="charm",
    ),
    path(
        "artifact/",
        views.mage.ArtifactCreateView.as_view(),
        name="artifact",
    ),
    path(
        "talisman/",
        views.mage.TalismanCreateView.as_view(),
        name="talisman",
    ),
    path(
        "periapt/",
        views.mage.PeriaptCreateView.as_view(),
        name="periapt",
    ),
    path(
        "grimoire/",
        views.mage.GrimoireCreateView.as_view(),
        name="grimoire",
    ),
    path(
        "sorcerer_artifact/",
        views.mage.SorcererArtifactCreateView.as_view(),
        name="sorcerer_artifact",
    ),
]

from django.urls import path
from items import views

urls = [
    path("wonder/", views.mage.WonderListView.as_view(), name="wonder"),
    path("charm/", views.mage.CharmListView.as_view(), name="charm"),
    path("artifact/", views.mage.ArtifactListView.as_view(), name="artifact"),
    path("talisman/", views.mage.TalismanListView.as_view(), name="talisman"),
    path("periapt/", views.mage.PeriaptListView.as_view(), name="periapt"),
    path("grimoire/", views.mage.GrimoireListView.as_view(), name="grimoire"),
    path(
        "sorcerer_artifact/",
        views.mage.SorcererArtifactListView.as_view(),
        name="sorcerer_artifact",
    ),
]

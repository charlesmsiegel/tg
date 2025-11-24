from django.urls import path
from items import views

app_name = "items:mage:detail"
urls = [
    path("wonder/<pk>/", views.mage.WonderDetailView.as_view(), name="wonder"),
    path("charm/<pk>/", views.mage.CharmDetailView.as_view(), name="charm"),
    path("artifact/<pk>/", views.mage.ArtifactDetailView.as_view(), name="artifact"),
    path("talisman/<pk>/", views.mage.TalismanDetailView.as_view(), name="talisman"),
    path("periapt/<pk>/", views.mage.PeriaptDetailView.as_view(), name="periapt"),
    path("grimoire/<pk>/", views.mage.GrimoireDetailView.as_view(), name="grimoire"),
    path(
        "sorcerer_artifact/<pk>/",
        views.mage.SorcererArtifactDetailView.as_view(),
        name="sorcerer_artifact",
    ),
]

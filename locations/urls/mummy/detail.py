from django.urls import path

from locations import views

app_name = "mummy:detail"
urls = [
    path("tomb/<int:pk>/", views.mummy.TombDetailView.as_view(), name="tomb"),
    path(
        "cult_temple/<int:pk>/",
        views.mummy.CultTempleDetailView.as_view(),
        name="cult_temple",
    ),
    path(
        "sanctuary/<int:pk>/",
        views.mummy.UndergroundSanctuaryDetailView.as_view(),
        name="sanctuary",
    ),
]

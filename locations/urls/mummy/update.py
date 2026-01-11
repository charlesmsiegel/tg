from django.urls import path

from locations import views

app_name = "mummy:update"
urls = [
    path("tomb/<int:pk>/", views.mummy.TombUpdateView.as_view(), name="tomb"),
    path(
        "cult_temple/<int:pk>/",
        views.mummy.CultTempleUpdateView.as_view(),
        name="cult_temple",
    ),
    path(
        "sanctuary/<int:pk>/",
        views.mummy.UndergroundSanctuaryUpdateView.as_view(),
        name="sanctuary",
    ),
]

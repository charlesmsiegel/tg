from django.urls import path
from locations import views

urls = [
    path("tomb/", views.mummy.TombListView.as_view(), name="tomb"),
    path("cult_temple/", views.mummy.CultTempleListView.as_view(), name="cult_temple"),
    path("sanctuary/", views.mummy.UndergroundSanctuaryListView.as_view(), name="sanctuary"),
]

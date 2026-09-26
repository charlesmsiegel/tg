from django.urls import path

from locations import views

urls = [
    path("tomb/", views.mummy.TombCreateView.as_view(), name="tomb"),
    path("cult_temple/", views.mummy.CultTempleCreateView.as_view(), name="cult_temple"),
    path("sanctuary/", views.mummy.UndergroundSanctuaryCreateView.as_view(), name="sanctuary"),
]

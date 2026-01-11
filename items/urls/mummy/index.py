from django.urls import path

from items import views

urls = [
    path("relic/", views.mummy.MummyRelicListView.as_view(), name="relic"),
    path("vessel/", views.mummy.VesselListView.as_view(), name="vessel"),
    path("ushabti/", views.mummy.UshabtiListView.as_view(), name="ushabti"),
]

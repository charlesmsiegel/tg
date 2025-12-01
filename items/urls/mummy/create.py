from django.urls import path
from items import views

app_name = "mummy:create"
urls = [
    path("relic/", views.mummy.MummyRelicCreateView.as_view(), name="relic"),
    path("vessel/", views.mummy.VesselCreateView.as_view(), name="vessel"),
    path("ushabti/", views.mummy.UshabtiCreateView.as_view(), name="ushabti"),
]

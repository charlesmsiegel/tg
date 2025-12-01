from django.urls import path
from items import views

app_name = "mummy:update"
urls = [
    path("relic/<int:pk>/", views.mummy.MummyRelicUpdateView.as_view(), name="relic"),
    path("vessel/<int:pk>/", views.mummy.VesselUpdateView.as_view(), name="vessel"),
    path("ushabti/<int:pk>/", views.mummy.UshabtiUpdateView.as_view(), name="ushabti"),
]

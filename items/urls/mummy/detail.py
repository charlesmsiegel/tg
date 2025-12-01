from django.urls import path
from items import views

app_name = "mummy:detail"
urls = [
    path("relic/<int:pk>/", views.mummy.MummyRelicDetailView.as_view(), name="relic"),
    path("vessel/<int:pk>/", views.mummy.VesselDetailView.as_view(), name="vessel"),
    path("ushabti/<int:pk>/", views.mummy.UshabtiDetailView.as_view(), name="ushabti"),
]

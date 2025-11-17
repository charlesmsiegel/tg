from django.urls import path
from items import views

app_name = "items:werewolf:detail"
urls = [
    path("fetish/<pk>/", views.werewolf.FetishDetailView.as_view(), name="fetish"),
    path("talen/<pk>/", views.werewolf.TalenDetailView.as_view(), name="talen"),
]

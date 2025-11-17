from django.urls import path
from locations import views

app_name = "locations:detail"
urls = [
    path("caern/", views.werewolf.CaernListView.as_view(), name="caern"),
]

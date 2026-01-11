from django.urls import path

from locations import views

app_name = "locations:detail"
urls = [
    path("caern/<pk>/", views.werewolf.CaernDetailView.as_view(), name="caern"),
]

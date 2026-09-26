from django.urls import path

from locations import views

urls = [
    path("caern/<pk>/", views.werewolf.CaernDetailView.as_view(), name="caern"),
]

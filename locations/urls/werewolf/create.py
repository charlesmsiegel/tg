from django.urls import path

from locations import views

app_name = "mage:create"
urls = [
    path(
        "caern/",
        views.werewolf.CaernCreateView.as_view(),
        name="caern",
    ),
]

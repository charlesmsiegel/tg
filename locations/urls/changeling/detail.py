from django.urls import path

from locations import views

app_name = "changeling"
urls = [
    path(
        "freehold/<int:pk>/",
        views.changeling.FreeholdDetailView.as_view(),
        name="freehold",
    ),
    path(
        "dream_realm/<int:pk>/",
        views.changeling.DreamRealmDetailView.as_view(),
        name="dream_realm",
    ),
    path(
        "holding/<int:pk>/",
        views.changeling.HoldingDetailView.as_view(),
        name="holding",
    ),
    path(
        "trod/<int:pk>/",
        views.changeling.TrodDetailView.as_view(),
        name="trod",
    ),
]

from django.urls import path
from locations import views

app_name = "changeling:update"
urls = [
    # Multi-step creation router - routes to appropriate step based on creation_status
    path(
        "freehold/<int:pk>/",
        views.changeling.FreeholdCreationView.as_view(),
        name="freehold",
    ),
    # Direct update (all-at-once) - for approved/completed freeholds
    path(
        "freehold/<int:pk>/direct/",
        views.changeling.FreeholdUpdateView.as_view(),
        name="freehold_direct",
    ),
]

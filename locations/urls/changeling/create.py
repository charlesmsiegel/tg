from django.urls import path
from locations import views

app_name = "changeling:create"
urls = [
    # Multi-step creation starts with basics
    path(
        "freehold/",
        views.changeling.FreeholdBasicsView.as_view(),
        name="freehold",
    ),
    # Direct creation (all-at-once) - kept for backwards compatibility
    path(
        "freehold/direct/",
        views.changeling.FreeholdCreateView.as_view(),
        name="freehold_direct",
    ),
]

from core import views
from django.urls import path

# Create your URLs here
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]

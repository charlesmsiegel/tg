from accounts import views
from core import views as core_views
from django.urls import path

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("profile/update/<pk>/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/<pk>/", views.ProfileView.as_view(), name="profile"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("", core_views.HomeListView.as_view(), name="user"),
]

from django.contrib.auth.mixins import LoginRequiredMixin
from locations import views
from django.urls import path

app_name = "mage:create"

# For example, updating ChantryBasicsView to enforce login
class ChantryBasicsView(LoginRequiredMixin, views.mage.ChantryBasicsView):
    login_url = "/accounts/login/"
    redirect_field_name = "next"

urlpatterns = [
    path(
        "node/",
        LoginRequiredMixin.as_view(view_class=views.mage.NodeCreateView, login_url="/accounts/login/"),
        name="node",
    ),
    path(
        "sector/",
        LoginRequiredMixin.as_view(view_class=views.mage.SectorCreateView, login_url="/accounts/login/"),
        name="sector",
    ),
    path(
        "realm/",
        LoginRequiredMixin.as_view(view_class=views.mage.RealmCreateView, login_url="/accounts/login/"),
        name="horizon_realm",
    ),
    path(
        "paradox_realm/",
        LoginRequiredMixin.as_view(view_class=views.mage.ParadoxRealmCreateView, login_url="/accounts/login/"),
        name="paradox_realm",
    ),
    path(
        "sanctum/",
        LoginRequiredMixin.as_view(view_class=views.mage.SanctumCreateView, login_url="/accounts/login/"),
        name="sanctum",
    ),
    path(
        "demesne/",
        LoginRequiredMixin.as_view(view_class=views.mage.DemesneCreateView, login_url="/accounts/login/"),
        name="demesne",
    ),
    path(
        "library/",
        LoginRequiredMixin.as_view(view_class=views.mage.LibraryCreateView, login_url="/accounts/login/"),
        name="library",
    ),
    path(
        "chantry/",
        ChantryBasicsView.as_view(),
        name="chantry",
    ),
    path(
        "reality_zone/",
        LoginRequiredMixin.as_view(view_class=views.mage.RealityZoneCreateView, login_url="/accounts/login/"),
        name="reality_zone",
    ),
]

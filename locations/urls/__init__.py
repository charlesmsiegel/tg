from django.urls import include, path
from locations import views

from . import mage, vampire, werewolf, wraith
from .core import create, detail, index, update

urlpatterns = [
    path("vampire/", include((vampire.urls, "vampire"), namespace="vampire")),
    path("werewolf/", include((werewolf.urls, "werewolf"), namespace="werewolf")),
    path("mage/", include((mage.urls, "mage"), namespace="mage")),
    path("wraith/", include((wraith.urls, "wraith"), namespace="wraith")),
    path("create/", include((create.urls, "locations_create"), namespace="create")),
    path("update/", include((update.urls, "locations_update"), namespace="update")),
    path("list/", include((index.urls, "locations_list"), namespace="list")),
    path("index/", views.core.LocationIndexView.as_view(), name="index"),
    path("", include(detail.urls)),
]

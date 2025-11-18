from django.urls import include, path
from items import views

from . import mage, vampire, werewolf
from .core import create, detail, index, update

urlpatterns = [
    path("vampire/", include((vampire.urls, "vampire"), namespace="vampire")),
    path("werewolf/", include((werewolf.urls, "werewolf"), namespace="werewolf")),
    path("mage/", include((mage.urls, "mage"), namespace="mage")),
    path("create/", include((create.urls, "items_create"), namespace="create")),
    path("update/", include((update.urls, "items_update"), namespace="update")),
    path("list/", include((index.urls, "items_list"), namespace="list")),
    path("index/", views.core.ItemIndexView.as_view(), name="index"),
    path("", include(detail.urls)),
]

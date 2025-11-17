from characters import views
from django.urls import include, path

from . import changeling, demon, mage, vampire, werewolf, wraith
from .core import ajax, create, detail, index, update

urlpatterns = [
    path("vampire/", include((vampire.urls, "vampire"), namespace="vampire")),
    path("werewolf/", include((werewolf.urls, "werewolf"), namespace="werewolf")),
    path("mage/", include((mage.urls, "mage"), namespace="mage")),
    path("wraith/", include((wraith.urls, "wraith"), namespace="wraith")),
    path(
        "changeling/", include((changeling.urls, "changeling"), namespace="changeling")
    ),
    path("demon/", include((demon.urls, "demon"), namespace="demon")),
    path("ajax/", include((ajax.urls, "characters_ajax"), namespace="ajax")),
    path("create/", include((create.urls, "characters_create"), namespace="create")),
    path("update/", include((update.urls, "characters_update"), namespace="update")),
    path("list/", include((index.urls, "characters_list"), namespace="list")),
    path("index/", views.core.CharacterIndexView.as_view(), name="index"),
    path("retired/", views.core.RetiredCharacterIndex.as_view(), name="retired"),
    path("deceased/", views.core.DeceasedCharacterIndex.as_view(), name="deceased"),
    path("npc/", views.core.NPCCharacterIndex.as_view(), name="npc"),
    path("", include(detail.urls)),
]

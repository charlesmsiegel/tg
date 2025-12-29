from characters.views.changeling.autumn_person import AutumnPersonCreateView
from characters.views.changeling.changeling import ChangelingBasicsView
from characters.views.changeling.ctdhuman import CtDHumanBasicsView
from characters.views.changeling.house import HouseCreateView
from characters.views.changeling.house_faction import HouseFactionCreateView
from characters.views.changeling.inanimae import InanimaeCreateView
from characters.views.changeling.kith import KithCreateView
from characters.views.changeling.legacy import LegacyCreateView
from characters.views.changeling.motley import MotleyCreateView
from characters.views.changeling.nunnehi import NunnehiCreateView
from django.urls import path

urls = [
    path(
        "changeling/",
        ChangelingBasicsView.as_view(),
        name="changeling",
    ),
    path(
        "motley/",
        MotleyCreateView.as_view(),
        name="motley",
    ),
    path(
        "kith/",
        KithCreateView.as_view(),
        name="kith",
    ),
    path(
        "house/",
        HouseCreateView.as_view(),
        name="house",
    ),
    path(
        "house_faction/",
        HouseFactionCreateView.as_view(),
        name="house_faction",
    ),
    path(
        "legacy/",
        LegacyCreateView.as_view(),
        name="legacy",
    ),
    path(
        "ctdhuman/",
        CtDHumanBasicsView.as_view(),
        name="ctd_human",
    ),
    path(
        "inanimae/",
        InanimaeCreateView.as_view(),
        name="inanimae",
    ),
    path(
        "nunnehi/",
        NunnehiCreateView.as_view(),
        name="nunnehi",
    ),
    path(
        "autumn_person/",
        AutumnPersonCreateView.as_view(),
        name="autumn_person",
    ),
]

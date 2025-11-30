from .dynasty import (
    DynastyCreateView,
    DynastyDetailView,
    DynastyListView,
    DynastyUpdateView,
)
from .mtr_human import MtRHumanCreateView, MtRHumanDetailView, MtRHumanUpdateView
from .mummy import MummyCreateView, MummyDetailView, MummyListView, MummyUpdateView
from .mummy_title import (
    MummyTitleCreateView,
    MummyTitleDetailView,
    MummyTitleListView,
    MummyTitleUpdateView,
)

__all__ = [
    "MtRHumanDetailView",
    "MtRHumanCreateView",
    "MtRHumanUpdateView",
    "MummyDetailView",
    "MummyCreateView",
    "MummyUpdateView",
    "MummyListView",
    "DynastyDetailView",
    "DynastyCreateView",
    "DynastyUpdateView",
    "DynastyListView",
    "MummyTitleDetailView",
    "MummyTitleCreateView",
    "MummyTitleUpdateView",
    "MummyTitleListView",
]

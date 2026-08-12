from .dynasty import (
    DynastyCreateView,
    DynastyDetailView,
    DynastyListView,
    DynastyUpdateView,
)
from .mtr_human import (
    MtRHumanCreateView,
    MtRHumanDetailView,
    MtRHumanListView,
    MtRHumanUpdateView,
)
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
    "MtRHumanListView",
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

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
    "DynastyCreateView",
    "DynastyDetailView",
    "DynastyListView",
    "DynastyUpdateView",
    "MtRHumanCreateView",
    "MtRHumanDetailView",
    "MtRHumanListView",
    "MtRHumanUpdateView",
    "MummyCreateView",
    "MummyDetailView",
    "MummyListView",
    "MummyUpdateView",
    "MummyTitleCreateView",
    "MummyTitleDetailView",
    "MummyTitleListView",
    "MummyTitleUpdateView",
]

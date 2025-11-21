from .changeling import (
    ChangelingCharacterCreationView,
    ChangelingDetailView as ChangelingCharacterDetailView,
    ChangelingCreateView as ChangelingCharacterListView,
    ChangelingUpdateView as ChangelingCharacterUpdateView,
)
from .ctdhuman import (
    CtDHumanCharacterCreationView,
    CtDHumanDetailView as CtDHumanCharacterDetailView,
    CtDHumanCreateView as CtDHumanCharacterListView,
    CtDHumanUpdateView as CtDHumanCharacterUpdateView,
)
from .house_faction import (
    HouseFactionCreateView as ChangelingFactionCreateView,
    HouseFactionDetailView as ChangelingFactionDetailView,
    HouseFactionListView as ChangelingFactionListView,
    HouseFactionUpdateView as ChangelingFactionUpdateView,
)
from .house import (
    HouseCreateView as ChangelingHouseCreateView,
    HouseDetailView as ChangelingHouseDetailView,
    HouseListView as ChangelingHouseListView,
    HouseUpdateView as ChangelingHouseUpdateView,
)
from .kith import (
    KithCreateView,
    KithDetailView,
    KithListView,
    KithUpdateView,
)
from .legacy import (
    LegacyCreateView,
    LegacyDetailView,
    LegacyListView,
    LegacyUpdateView,
)
from .motley import (
    MotleyCreateView,
    MotleyDetailView,
    MotleyUpdateView,
)

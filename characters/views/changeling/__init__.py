from .autumn_person import (
    AutumnPersonCreateView,
    AutumnPersonDetailView,
    AutumnPersonUpdateView,
)
from .changeling import ChangelingCharacterCreationView
from .changeling import ChangelingCreateView as ChangelingCharacterListView
from .changeling import ChangelingDetailView as ChangelingCharacterDetailView
from .changeling import ChangelingUpdateView as ChangelingCharacterUpdateView
from .ctdhuman import CtDHumanBasicsView, CtDHumanCharacterCreationView
from .ctdhuman import CtDHumanCreateView as CtDHumanCharacterListView
from .ctdhuman import CtDHumanDetailView as CtDHumanCharacterDetailView
from .ctdhuman import CtDHumanTemplateSelectView
from .ctdhuman import CtDHumanUpdateView as CtDHumanCharacterUpdateView
from .house import HouseCreateView as ChangelingHouseCreateView
from .house import HouseDetailView as ChangelingHouseDetailView
from .house import HouseListView as ChangelingHouseListView
from .house import HouseUpdateView as ChangelingHouseUpdateView
from .house_faction import HouseFactionCreateView as ChangelingFactionCreateView
from .house_faction import HouseFactionDetailView as ChangelingFactionDetailView
from .house_faction import HouseFactionListView as ChangelingFactionListView
from .house_faction import HouseFactionUpdateView as ChangelingFactionUpdateView
from .inanimae import InanimaeCreateView, InanimaeDetailView, InanimaeUpdateView
from .kith import KithCreateView, KithDetailView, KithListView, KithUpdateView
from .legacy import LegacyCreateView, LegacyDetailView, LegacyListView, LegacyUpdateView
from .motley import MotleyCreateView, MotleyDetailView, MotleyListView, MotleyUpdateView
from .nunnehi import NunnehiCreateView, NunnehiDetailView, NunnehiUpdateView

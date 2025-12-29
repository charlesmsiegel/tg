from .advantage import AdvantageDetailView
from .cabal import CabalCreateView, CabalDetailView, CabalListView, CabalUpdateView
from .companion import (
    CompanionBasicsView,
    CompanionCreateView,
    CompanionUpdateView,
    CopanionCharacterCreationView,
)
from .effect import EffectCreateView, EffectDetailView, EffectListView, EffectUpdateView
from .faction import (
    MageFactionCreateView,
    MageFactionDetailView,
    MageFactionListView,
    MageFactionUpdateView,
)
from .fellowship import (
    SorcererFellowshipCreateView,
    SorcererFellowshipDetailView,
    SorcererFellowshipListView,
    SorcererFellowshipUpdateView,
)
from .focus import (
    CorruptedPracticeCreateView,
    CorruptedPracticeDetailView,
    CorruptedPracticeUpdateView,
    GenericPracticeDetailView,
    InstrumentCreateView,
    InstrumentDetailView,
    InstrumentListView,
    InstrumentUpdateView,
    ParadigmCreateView,
    ParadigmDetailView,
    ParadigmListView,
    ParadigmUpdateView,
    PracticeCreateView,
    PracticeDetailView,
    PracticeListView,
    PracticeUpdateView,
    SpecializedPracticeCreateView,
    SpecializedPracticeDetailView,
    SpecializedPracticeUpdateView,
    TenetCreateView,
    TenetDetailView,
    TenetListView,
    TenetUpdateView,
)
from .hedge_magic import PathDetailView, RitualDetailView
from .mage import (
    GetAbilitiesView,
    LoadFactionsView,
    LoadMFRatingsView,
    LoadSubfactionsView,
    MageBasicsView,
    MageCharacterCreationView,
    MageCreateView,
    MageDetailView,
    MageUpdateView,
)
from .mtahuman import (
    MtAHumanAbilityView,
    MtAHumanBasicsView,
    MtAHumanCharacterCreationView,
    MtAHumanCreateView,
    MtAHumanDetailView,
    MtAHumanTemplateSelectView,
    MtAHumanUpdateView,
)
from .resonance import (
    ResonanceCreateView,
    ResonanceDetailView,
    ResonanceListView,
    ResonanceUpdateView,
)
from .rote import RoteCreateView, RoteDetailView, RoteListView, RoteUpdateView
from .sorcerer import (
    GetPracticeAbilitiesView,
    LoadAffinitiesView,
    LoadAttributesView,
    SorcererBasicsView,
    SorcererCharacterCreationView,
    SorcererDetailView,
    SorcererUpdateView,
)
from .companion import LoadCompanionValuesView

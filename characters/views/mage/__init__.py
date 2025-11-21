from .advantage import AdvantageDetailView
from .cabal import CabalCreateView, CabalDetailView, CabalUpdateView
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
    MageBasicsView,
    MageCharacterCreationView,
    MageCreateView,
    MageDetailView,
    MageUpdateView,
    load_factions,
    load_mf_ratings,
    load_subfactions,
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
    SorcererBasicsView,
    SorcererCharacterCreationView,
    SorcererDetailView,
    SorcererUpdateView,
)

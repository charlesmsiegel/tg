from core.mixins import SpecialUserMixin

from . import generic
from .book import BookCreateView, BookDetailView, BookListView, BookUpdateView
from .character_template import (
    CharacterTemplateCreateView,
    CharacterTemplateDeleteView,
    CharacterTemplateDetailView,
    CharacterTemplateExportView,
    CharacterTemplateImportView,
    CharacterTemplateListView,
    CharacterTemplateQuickNPCView,
    CharacterTemplateUpdateView,
)
from .generic import CachedDetailView, CachedListView, DictView, MultipleFormsetsMixin
from .home import HomeListView
from .houserules import (
    HouseRuleCreateView,
    HouseRuleDetailView,
    HouseRulesIndexView,
    HouseRuleUpdateView,
)
from .language import (
    LanguageCreateView,
    LanguageDetailView,
    LanguageListView,
    LanguageUpdateView,
)
from .newsitem import (
    NewsItemCreateView,
    NewsItemDetailView,
    NewsItemListView,
    NewsItemUpdateView,
)

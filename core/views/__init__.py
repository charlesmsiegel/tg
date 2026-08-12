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
from .reference import ReferenceViewSet, create_reference_views

__all__ = [
    "SpecialUserMixin",
    "generic",
    "BookCreateView",
    "BookDetailView",
    "BookListView",
    "BookUpdateView",
    "CharacterTemplateCreateView",
    "CharacterTemplateDeleteView",
    "CharacterTemplateDetailView",
    "CharacterTemplateExportView",
    "CharacterTemplateImportView",
    "CharacterTemplateListView",
    "CharacterTemplateQuickNPCView",
    "CharacterTemplateUpdateView",
    "CachedDetailView",
    "CachedListView",
    "DictView",
    "MultipleFormsetsMixin",
    "HomeListView",
    "HouseRuleCreateView",
    "HouseRuleDetailView",
    "HouseRulesIndexView",
    "HouseRuleUpdateView",
    "LanguageCreateView",
    "LanguageDetailView",
    "LanguageListView",
    "LanguageUpdateView",
    "NewsItemCreateView",
    "NewsItemDetailView",
    "NewsItemListView",
    "NewsItemUpdateView",
    "ReferenceViewSet",
    "create_reference_views",
]

from typing import Any

from characters.models.mage.focus import (
    CorruptedPractice,
    Instrument,
    Paradigm,
    Practice,
    SpecializedPractice,
    Tenet,
)
from core.utils import display_queryset
from core.views.generic import DictView
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class InstrumentDetailView(DetailView):
    model = Instrument
    template_name = "characters/mage/instrument/detail.html"


class InstrumentCreateView(MessageMixin, CreateView):
    model = Instrument
    fields = ["name", "description"]
    template_name = "characters/mage/instrument/form.html"
    success_message = "Instrument created successfully."
    error_message = "There was an error creating the Instrument."


class InstrumentUpdateView(MessageMixin, UpdateView):
    model = Instrument
    fields = ["name", "description"]
    template_name = "characters/mage/instrument/form.html"
    success_message = "Instrument updated successfully."
    error_message = "There was an error updating the Instrument."


class InstrumentListView(ListView):
    model = Instrument
    ordering = ["name"]
    template_name = "characters/mage/instrument/list.html"


class ParadigmDetailView(DetailView):
    model = Paradigm
    template_name = "characters/mage/paradigm/detail.html"


class ParadigmCreateView(MessageMixin, CreateView):
    model = Paradigm
    fields = ["name", "tenets", "description"]
    template_name = "characters/mage/paradigm/form.html"
    success_message = "Paradigm created successfully."
    error_message = "There was an error creating the Paradigm."


class ParadigmUpdateView(MessageMixin, UpdateView):
    model = Paradigm
    fields = ["name", "tenets", "description"]
    template_name = "characters/mage/paradigm/form.html"
    success_message = "Paradigm updated successfully."
    error_message = "There was an error updating the Paradigm."


class ParadigmListView(ListView):
    model = Paradigm
    ordering = ["name"]
    template_name = "characters/mage/paradigm/list.html"


class PracticeDetailView(DetailView):
    model = Practice
    template_name = "characters/mage/practice/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["specializations"] = SpecializedPractice.objects.filter(
            parent_practice=self.object
        )
        context["corruptions"] = CorruptedPractice.objects.filter(
            parent_practice=self.object
        )
        return context


class PracticeCreateView(MessageMixin, CreateView):
    model = Practice
    fields = [
        "name",
        "abilities",
        "instruments",
        "common_resonance_traits",
        "benefit",
        "penalty",
        "description",
    ]
    template_name = "characters/mage/practice/form.html"
    success_message = "Practice created successfully."
    error_message = "There was an error creating the Practice."


class PracticeUpdateView(MessageMixin, UpdateView):
    model = Practice
    fields = [
        "name",
        "abilities",
        "instruments",
        "common_resonance_traits",
        "benefit",
        "penalty",
        "description",
    ]
    template_name = "characters/mage/practice/form.html"
    success_message = "Practice updated successfully."
    error_message = "There was an error updating the Practice."


class PracticeListView(ListView):
    model = Practice
    ordering = ["name"]
    template_name = "characters/mage/practice/list.html"


class CorruptedPracticeDetailView(PracticeDetailView):
    model = CorruptedPractice
    template_name = "characters/mage/corrupted_practice/detail.html"


class CorruptedPracticeCreateView(MessageMixin, CreateView):
    model = CorruptedPractice
    fields = [
        "name",
        "abilities",
        "instruments",
        "common_resonance_traits",
        "benefit",
        "penalty",
        "extra_benefit",
        "price",
        "description",
    ]
    template_name = "characters/mage/corrupted_practice/form.html"
    success_message = "Corrupted Practice created successfully."
    error_message = "There was an error creating the Corrupted Practice."


class CorruptedPracticeUpdateView(MessageMixin, UpdateView):
    model = CorruptedPractice
    fields = [
        "name",
        "abilities",
        "instruments",
        "common_resonance_traits",
        "benefit",
        "penalty",
        "extra_benefit",
        "price",
        "description",
    ]
    template_name = "characters/mage/corrupted_practice/form.html"
    success_message = "Corrupted Practice updated successfully."
    error_message = "There was an error updating the Corrupted Practice."


class SpecializedPracticeDetailView(PracticeDetailView):
    model = SpecializedPractice
    template_name = "characters/mage/specialized_practice/detail.html"


class SpecializedPracticeCreateView(MessageMixin, CreateView):
    model = SpecializedPractice
    fields = [
        "name",
        "abilities",
        "instruments",
        "common_resonance_traits",
        "benefit",
        "penalty",
        "extra_benefit",
        "description",
    ]
    template_name = "characters/mage/specialized_practice/form.html"
    success_message = "Specialized Practice created successfully."
    error_message = "There was an error creating the Specialized Practice."


class SpecializedPracticeUpdateView(MessageMixin, UpdateView):
    model = SpecializedPractice
    fields = [
        "name",
        "abilities",
        "instruments",
        "common_resonance_traits",
        "benefit",
        "penalty",
        "extra_benefit",
        "description",
    ]
    template_name = "characters/mage/specialized_practice/form.html"
    success_message = "Specialized Practice updated successfully."
    error_message = "There was an error updating the Specialized Practice."


class TenetDetailView(DetailView):
    model = Tenet
    template_name = "characters/mage/tenet/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["associated_practices"] = display_queryset(
            self.object.associated_practices.all()
        )
        context["limited_practices"] = display_queryset(
            self.object.limited_practices.all()
        )
        return context


class TenetCreateView(MessageMixin, CreateView):
    model = Tenet
    fields = [
        "name",
        "tenet_type",
        "associated_practices",
        "limited_practices",
        "description",
    ]
    template_name = "characters/mage/tenet/form.html"
    success_message = "Tenet created successfully."
    error_message = "There was an error creating the Tenet."


class TenetUpdateView(MessageMixin, UpdateView):
    model = Tenet
    fields = [
        "name",
        "tenet_type",
        "associated_practices",
        "limited_practices",
        "description",
    ]
    template_name = "characters/mage/tenet/form.html"
    success_message = "Tenet updated successfully."
    error_message = "There was an error updating the Tenet."


class TenetListView(ListView):
    model = Tenet
    ordering = ["name"]
    template_name = "characters/mage/tenet/list.html"


class GenericPracticeDetailView(DictView):
    view_mapping = {
        "practice": PracticeDetailView,
        "specialized_practice": SpecializedPracticeDetailView,
        "corrupted_practice": CorruptedPracticeDetailView,
    }
    model_class = Practice
    key_property = "type"
    default_redirect = "characters:index mage"

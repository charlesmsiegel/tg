from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models import PhysicalPlace


class PhysicalPlaceDetailView(LoginRequiredMixin, DetailView):
    """Detail view showing a physical place and all its supernatural locations."""

    model = PhysicalPlace
    template_name = "locations/core/physical_place/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get supernatural locations grouped by gameline
        by_gameline = self.object.get_supernatural_locations_by_gameline()

        # Add gameline display names
        gameline_locations = []
        for gameline_code, locations in by_gameline.items():
            gameline_name = settings.GAMELINES.get(gameline_code, {}).get(
                "name", gameline_code.upper()
            )
            gameline_locations.append({
                "code": gameline_code,
                "name": gameline_name,
                "locations": locations,
            })

        # Sort by gameline name
        gameline_locations.sort(key=lambda x: x["name"])

        context["gameline_locations"] = gameline_locations
        context["total_locations"] = self.object.get_supernatural_locations().count()
        return context


class PhysicalPlaceListView(LoginRequiredMixin, ListView):
    """List view for all physical places."""

    model = PhysicalPlace
    template_name = "locations/core/physical_place/list.html"
    context_object_name = "physical_places"
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by chronicle if user has one selected
        # and filter by visibility
        return queryset.filter(display=True).prefetch_related("locations")


class PhysicalPlaceCreateView(LoginRequiredMixin, CreateView):
    """Create view for physical places."""

    model = PhysicalPlace
    template_name = "locations/core/physical_place/form.html"
    fields = [
        "name",
        "description",
        "address",
        "city",
        "state",
        "country",
        "postal_code",
        "latitude",
        "longitude",
        "place_type",
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description", "rows": 4}
        )
        form.fields["address"].widget.attrs.update({"placeholder": "Street address"})
        form.fields["city"].widget.attrs.update({"placeholder": "City"})
        form.fields["state"].widget.attrs.update({"placeholder": "State/Province"})
        form.fields["country"].widget.attrs.update({"placeholder": "Country"})
        form.fields["postal_code"].widget.attrs.update({"placeholder": "Postal code"})
        form.fields["latitude"].widget.attrs.update({"placeholder": "e.g., 47.6097"})
        form.fields["longitude"].widget.attrs.update({"placeholder": "e.g., -122.3331"})
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PhysicalPlaceUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for physical places."""

    model = PhysicalPlace
    template_name = "locations/core/physical_place/form.html"
    fields = [
        "name",
        "description",
        "address",
        "city",
        "state",
        "country",
        "postal_code",
        "latitude",
        "longitude",
        "place_type",
        "display",
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description", "rows": 4}
        )
        form.fields["address"].widget.attrs.update({"placeholder": "Street address"})
        form.fields["city"].widget.attrs.update({"placeholder": "City"})
        form.fields["state"].widget.attrs.update({"placeholder": "State/Province"})
        form.fields["country"].widget.attrs.update({"placeholder": "Country"})
        form.fields["postal_code"].widget.attrs.update({"placeholder": "Postal code"})
        form.fields["latitude"].widget.attrs.update({"placeholder": "e.g., 47.6097"})
        form.fields["longitude"].widget.attrs.update({"placeholder": "e.g., -122.3331"})
        return form

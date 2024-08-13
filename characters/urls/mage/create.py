from characters import views
from django.urls import path

# Create your URLs here
app_name = "mage:create"
urls = [
    path(
        "effect/",
        views.mage.EffectCreateView.as_view(),
        name="effect",
    ),
    path(
        "resonances/create/",
        views.mage.ResonanceCreateView.as_view(),
        name="resonance",
    ),
]
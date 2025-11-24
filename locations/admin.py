from django.contrib import admin
from locations.models.changeling import Freehold
from locations.models.core import City, LocationModel
from locations.models.demon import Bastion, Reliquary
from locations.models.mage import Node, NodeMeritFlawRating, NodeResonanceRating
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.models.mage.library import Library
from locations.models.mage.reality_zone import RealityZone, ZoneRating
from locations.models.mage.realm import HorizonRealm
from locations.models.mage.sanctum import Sanctum
from locations.models.mage.sector import Sector
from locations.models.vampire import (
    Barrens,
    Domain,
    Elysium,
    Haven,
    HavenMeritFlawRating,
    Rack,
    TremereChantry,
)
from locations.models.werewolf.caern import Caern
from locations.models.wraith.haunt import Haunt
from locations.models.wraith.necropolis import Necropolis

admin.site.register(LocationModel)
admin.site.register(Sanctum)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ("name", "rank", "parent")


admin.site.register(NodeMeritFlawRating)
admin.site.register(NodeResonanceRating)


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("name", "rank", "faction", "parent")


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("name", "sector_class")


admin.site.register(HorizonRealm)
admin.site.register(RealityZone)
admin.site.register(ZoneRating)


@admin.register(Caern)
class CaernAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Chantry)
class ChantryAdmin(admin.ModelAdmin):
    list_display = ("name", "rank", "parent", "faction")


@admin.register(ChantryBackgroundRating)
class ChantryBackgroundRatingAdmin(admin.ModelAdmin):
    list_display = ("chantry", "bg", "note", "rating", "url", "complete")


@admin.register(Haunt)
class HauntAdmin(admin.ModelAdmin):
    list_display = ("name", "rank", "haunt_type", "shroud_rating", "parent")
    list_filter = ("haunt_type", "rank")


@admin.register(Necropolis)
class NecropolisAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "population", "deathlord")
    list_filter = ("region",)


# Vampire locations
@admin.register(Haven)
class HavenAdmin(admin.ModelAdmin):
    list_display = ("name", "size", "security", "location", "total_rating")


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", "size", "population", "control", "total_rating")


@admin.register(Elysium)
class ElysiumAdmin(admin.ModelAdmin):
    list_display = ("name", "prestige", "elysium_type", "keeper_name")


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ("name", "quality", "population_density", "risk_level")


@admin.register(TremereChantry)
class TremereChantryAdmin(admin.ModelAdmin):
    list_display = ("name", "size", "security_level", "library_rating", "pyramid_level", "regent_name")


@admin.register(Barrens)
class BarrensAdmin(admin.ModelAdmin):
    list_display = ("name", "size", "danger_level", "barrens_type")


admin.site.register(HavenMeritFlawRating)


# Changeling locations
@admin.register(Freehold)
class FreeholdAdmin(admin.ModelAdmin):
    list_display = ("name", "archetype", "balefire", "size", "sanctuary", "resources")
    list_filter = ("archetype",)


# Demon locations
from locations.models.demon.bastion import Bastion
from locations.models.demon.reliquary import Reliquary


@admin.register(Bastion)
class BastionAdmin(admin.ModelAdmin):
    list_display = ("name", "ritual_strength", "warding_level", "consecration_date")
    list_filter = ("ritual_strength", "warding_level")


@admin.register(Reliquary)
class ReliquaryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "reliquary_type",
        "max_health_levels",
        "current_health_levels",
        "soak_rating",
    )
    list_filter = ("reliquary_type",)

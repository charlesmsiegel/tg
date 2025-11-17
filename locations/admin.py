from django.contrib import admin
from locations.models.core import City, LocationModel
from locations.models.mage import Node, NodeMeritFlawRating, NodeResonanceRating
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.models.mage.library import Library
from locations.models.mage.reality_zone import RealityZone, ZoneRating
from locations.models.mage.realm import HorizonRealm
from locations.models.mage.sanctum import Sanctum
from locations.models.mage.sector import Sector
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

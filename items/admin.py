from django.contrib import admin
from items.models.core import (
    ItemModel,
    Material,
    Medium,
    MeleeWeapon,
    RangedWeapon,
    ThrownWeapon,
    Weapon,
)
from items.models.mage import Charm, Wonder, WonderResonanceRating
from items.models.mage.artifact import Artifact
from items.models.mage.grimoire import Grimoire
from items.models.mage.sorcerer_artifact import SorcererArtifact
from items.models.mage.talisman import Talisman
from items.models.werewolf.fetish import Fetish


@admin.register(ItemModel)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Weapon)
admin.site.register(MeleeWeapon)
admin.site.register(ThrownWeapon)
admin.site.register(RangedWeapon)


@admin.register(Medium)
class MediumAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Medium"
        verbose_name_plural = "Mediums"


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"


@admin.register(Wonder)
class WonderAdmin(admin.ModelAdmin):
    list_display = ("name", "rank", "background_cost", "quintessence_max")


admin.site.register(WonderResonanceRating)
admin.site.register(Charm)
admin.site.register(Talisman)
admin.site.register(Artifact)


@admin.register(Grimoire)
class GrimoireAdmin(admin.ModelAdmin):
    list_display = ("name", "rank", "is_primer", "medium", "faction")


@admin.register(Fetish)
class FetishAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(SorcererArtifact)

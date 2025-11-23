from django.contrib import admin
from items.models.changeling import Treasure
from items.models.core import (
    ItemModel,
    Material,
    Medium,
    MeleeWeapon,
    RangedWeapon,
    ThrownWeapon,
    Weapon,
)
from items.models.demon import Relic
from items.models.mage import Charm, Wonder, WonderResonanceRating
from items.models.mage.artifact import Artifact
from items.models.mage.grimoire import Grimoire
from items.models.mage.sorcerer_artifact import SorcererArtifact
from items.models.mage.talisman import Talisman
from items.models.vampire import Bloodstone, VampireArtifact
from items.models.werewolf.fetish import Fetish
from items.models.wraith import WraithArtifact, WraithRelic


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


# Vampire items
@admin.register(VampireArtifact)
class VampireArtifactAdmin(admin.ModelAdmin):
    list_display = ("name", "power_level", "background_cost", "is_cursed", "is_unique")


@admin.register(Bloodstone)
class BloodstoneAdmin(admin.ModelAdmin):
    list_display = ("name", "blood_stored", "max_blood", "is_active")


# Demon items
from items.models.demon.relic import Relic


@admin.register(Relic)
class RelicAdmin(admin.ModelAdmin):
    list_display = ("name", "relic_type", "complexity", "house", "difficulty")
    list_filter = ("relic_type", "house")


# Wraith items
@admin.register(WraithRelic)
class WraithRelicAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "rarity", "background_cost", "pathos_cost")


@admin.register(WraithArtifact)
class WraithArtifactAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "artifact_type", "material", "corpus")


# Changeling items
@admin.register(Treasure)
class TreasureAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "treasure_type", "permanence", "glamour_storage")

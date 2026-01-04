from characters.models.changeling import (
    Changeling,
    CtDHuman,
    House,
    Kith,
    Legacy,
    Motley,
)
from characters.models.changeling.house_faction import HouseFaction
from characters.models.core import (
    Archetype,
    Character,
    CharacterModel,
    Derangement,
    Group,
    Human,
    MeritFlaw,
    MeritFlawRating,
    Specialty,
)
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import (
    Background,
    BackgroundRating,
    PooledBackgroundRating,
)
from characters.models.core.statistic import Statistic
from characters.models.demon import (
    Demon,
    DemonFaction,
    DemonHouse,
    DtFHuman,
    Earthbound,
    Lore,
    LoreRating,
    Pact,
    Thrall,
    Visage,
)
from characters.models.demon.apocalyptic_form import ApocalypticFormTrait
from characters.models.mage import (
    Cabal,
    CorruptedPractice,
    Effect,
    Instrument,
    Mage,
    MageFaction,
    MtAHuman,
    Paradigm,
    Practice,
    PracticeRating,
    Resonance,
    ResRating,
    Rote,
    SpecializedPractice,
    Tenet,
)
from characters.models.mage.companion import Advantage, AdvantageRating, Companion
from characters.models.mage.fellowship import SorcererFellowship
from characters.models.mage.sorcerer import (
    LinearMagicPath,
    LinearMagicRitual,
    PathRating,
    Sorcerer,
)
from characters.models.mage.sphere import Sphere
from characters.models.vampire import (
    Discipline,
    Ghoul,
    Path,
    Revenant,
    RevenantFamily,
    Vampire,
    VampireClan,
    VampireSect,
    VampireTitle,
    VtMHuman,
)
from characters.models.werewolf import (
    Ajaba,
    Ananasi,
    BattleScar,
    Camp,
    Drone,
    Fomor,
    FomoriPower,
    Gift,
    GiftPermission,
    Grondr,
    Kinfolk,
    Kitsune,
    Nagah,
    Pack,
    RenownIncident,
    Rite,
    Rokea,
    SeptPosition,
    SpiritCharacter,
    SpiritCharm,
    Totem,
    Tribe,
    Werewolf,
    WtAHuman,
)
from characters.models.wraith import WtOHuman
from characters.models.wraith.arcanos import Arcanos
from characters.models.wraith.faction import WraithFaction
from characters.models.wraith.fetter import Fetter
from characters.models.wraith.guild import Guild
from characters.models.wraith.passion import Passion
from characters.models.wraith.shadow_archetype import ShadowArchetype
from characters.models.wraith.thorn import Thorn
from characters.models.wraith.wraith import ThornRating, Wraith
from django.contrib import admin

admin.site.register(CharacterModel)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "chronicle")


@admin.register(Human)
class HumanCharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "chronicle")


@admin.register(Archetype)
class ArchetypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(MeritFlaw)
class MeritFlawAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(MeritFlawRating)


@admin.register(Derangement)
class DerangementAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "leader", "chronicle")


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("name", "stat")


@admin.register(Resonance)
class ResonanceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "correspondence",
        "entropy",
        "forces",
        "life",
        "matter",
        "mind",
        "prime",
        "spirit",
        "time",
    )


@admin.register(Effect)
class EffectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "correspondence",
        "entropy",
        "forces",
        "life",
        "matter",
        "mind",
        "prime",
        "spirit",
        "time",
    )


@admin.register(Paradigm)
class ParadigmAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(SpecializedPractice)
class SpecializedPracticeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(CorruptedPractice)
class CorruptedPracticeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Tenet)
class TenetAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(MageFaction)
class MageFactionAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")


@admin.register(Rote)
class RoteAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "practice",
        "attribute",
        "ability",
        "correspondence",
        "entropy",
        "forces",
        "matter",
        "mind",
        "life",
        "prime",
        "spirit",
        "time",
    )

    def correspondence(self, obj):
        """Get the Correspondence sphere rating from the rote's effect."""
        return obj.effect.correspondence

    def time(self, obj):
        """Get the Time sphere rating from the rote's effect."""
        return obj.effect.time

    def spirit(self, obj):
        """Get the Spirit sphere rating from the rote's effect."""
        return obj.effect.spirit

    def matter(self, obj):
        """Get the Matter sphere rating from the rote's effect."""
        return obj.effect.matter

    def life(self, obj):
        """Get the Life sphere rating from the rote's effect."""
        return obj.effect.life

    def forces(self, obj):
        """Get the Forces sphere rating from the rote's effect."""
        return obj.effect.forces

    def entropy(self, obj):
        """Get the Entropy sphere rating from the rote's effect."""
        return obj.effect.entropy

    def mind(self, obj):
        """Get the Mind sphere rating from the rote's effect."""
        return obj.effect.mind

    def prime(self, obj):
        """Get the Prime sphere rating from the rote's effect."""
        return obj.effect.prime


@admin.register(Totem)
class TotemAdmin(admin.ModelAdmin):
    list_display = ("name", "cost")


@admin.register(SpiritCharm)
class SpiritCharmAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(SpiritCharacter)
class SpiritCharacterAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(MtAHuman)


@admin.register(Mage)
class MageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "arete",
        "affiliation",
        "faction",
        "subfaction",
        "essence",
        "affinity_sphere",
        "chronicle",
        "status",
    )
    list_filter = ("owner", "arete", "essence", "affinity_sphere", "chronicle")


@admin.register(ResRating)
class ResRatingAdmin(admin.ModelAdmin):
    list_display = ("mage", "resonance", "rating")


@admin.register(Cabal)
class CabalAdmin(admin.ModelAdmin):
    list_display = ("name", "leader")


admin.site.register(HouseFaction)

admin.site.register(VtMHuman)
admin.site.register(Vampire)
admin.site.register(Ghoul)
admin.site.register(Revenant)
admin.site.register(RevenantFamily)
admin.site.register(VampireClan)
admin.site.register(VampireSect)
admin.site.register(VampireTitle)
admin.site.register(Path)
admin.site.register(Discipline)
admin.site.register(WtOHuman)
admin.site.register(PracticeRating)

admin.site.register(Statistic)
admin.site.register(Ability)
admin.site.register(Attribute)

admin.site.register(Background)


@admin.register(BackgroundRating)
class BackgroundRatingAdmin(admin.ModelAdmin):
    list_display = ("char", "bg", "rating", "note")


admin.site.register(PooledBackgroundRating)

admin.site.register(WtAHuman)


@admin.register(Rite)
class RiteAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "type")


@admin.register(Tribe)
class TribeAdmin(admin.ModelAdmin):
    list_display = ("name", "willpower")


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ("name", "rank")


@admin.register(RenownIncident)
class RenownIncidentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "glory",
        "honor",
        "wisdom",
        "posthumous",
        "only_once",
        "breed",
        "rite",
    )


@admin.register(BattleScar)
class BattleScarAdmin(admin.ModelAdmin):
    list_display = ("name", "glory")


@admin.register(Camp)
class CampAdmin(admin.ModelAdmin):
    list_display = ("name", "tribe")


@admin.register(Werewolf)
class WerewolfAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "rank",
        "auspice",
        "breed",
        "tribe",
        "rage",
        "gnosis",
        "glory",
        "wisdom",
        "honor",
    )


@admin.register(Kinfolk)
class KinfolkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "breed",
        "tribe",
    )


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ("name", "leader", "totem")


@admin.register(Fomor)
class FomorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(FomoriPower)
class FomoriPowerAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Ananasi)
class AnanasiAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "aspect", "cunning", "obedience", "wisdom")


@admin.register(Rokea)
class RokeaAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "auspice", "valor", "harmony", "innovation")


@admin.register(Kitsune)
class KitsuneAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "path", "chie", "toku", "kagayaki")


@admin.register(Nagah)
class NagahAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "auspice", "obligation", "wisdom", "subtlety")


@admin.register(Ajaba)
class AjabaAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "auspice", "ferocity", "obligation", "wisdom")


@admin.register(Grondr)
class GrondrAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "auspice", "glory", "honor", "wisdom")


@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    list_display = ("name", "bane_name", "bane_type", "rage", "gnosis")


@admin.register(SeptPosition)
class SeptPositionAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Changeling)
class ChangelingAdmin(admin.ModelAdmin):
    list_display = ("name", "kith")


admin.site.register(Legacy)
admin.site.register(CtDHuman)
admin.site.register(House)
admin.site.register(Kith)
admin.site.register(Motley)


@admin.register(Companion)
class CompanionAdmin(admin.ModelAdmin):
    list_display = ("name", "companion_type")


@admin.register(Sorcerer)
class SorcererAdmin(admin.ModelAdmin):
    list_display = ("name", "sorcerer_type")


admin.site.register(LinearMagicPath)


@admin.register(LinearMagicRitual)
class LinearMagicRitualAdmin(admin.ModelAdmin):
    list_display = ("name", "path", "level")


admin.site.register(PathRating)
admin.site.register(Sphere)
admin.site.register(SorcererFellowship)
admin.site.register(Advantage)
admin.site.register(AdvantageRating)
admin.site.register(GiftPermission)

# Demon Models


@admin.register(Demon)
class DemonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "celestial_name",
        "owner",
        "house",
        "faction",
        "faith",
        "torment",
        "chronicle",
        "status",
    )
    list_filter = ("owner", "house", "faction", "chronicle", "status")
    search_fields = ("name", "celestial_name")
    ordering = ("name",)


admin.site.register(DtFHuman)


@admin.register(DemonFaction)
class DemonFactionAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(DemonHouse)
class DemonHouseAdmin(admin.ModelAdmin):
    list_display = ("name", "celestial_name", "starting_torment")


@admin.register(Visage)
class VisageAdmin(admin.ModelAdmin):
    list_display = ("name", "house")
    list_filter = ("house",)


@admin.register(Lore)
class LoreAdmin(admin.ModelAdmin):
    list_display = ("name", "property_name")


admin.site.register(LoreRating)
admin.site.register(Pact)


@admin.register(Thrall)
class ThrallAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "master", "faith_potential")
    list_filter = ("owner", "master")


@admin.register(Earthbound)
class EarthboundAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "house",
        "faith",
        "torment",
        "reliquary_type",
        "chronicle",
        "status",
    )
    list_filter = ("owner", "house", "reliquary_type", "chronicle", "status")


@admin.register(ApocalypticFormTrait)
class ApocalypticFormTraitAdmin(admin.ModelAdmin):
    list_display = ("name", "cost", "high_torment_only")
    list_filter = ("cost", "high_torment_only")


from characters.models.demon.ritual import Ritual


@admin.register(Ritual)
class RitualAdmin(admin.ModelAdmin):
    list_display = ("name", "house", "primary_lore", "primary_lore_rating", "base_cost")
    list_filter = ("house", "primary_lore")
    search_fields = ("name", "description")


# Wraith Models


@admin.register(Wraith)
class WraithAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "guild",
        "legion",
        "faction",
        "corpus",
        "pathos",
        "angst",
        "chronicle",
        "status",
    )
    list_filter = ("owner", "guild", "legion", "faction", "chronicle", "status")


@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    list_display = ("name", "willpower")


@admin.register(WraithFaction)
class WraithFactionAdmin(admin.ModelAdmin):
    list_display = ("name", "faction_type")
    list_filter = ("faction_type",)


@admin.register(Arcanos)
class ArcanosAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(ShadowArchetype)
class ShadowArchetypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Thorn)
class ThornAdmin(admin.ModelAdmin):
    list_display = ("name", "thorn_type", "point_cost")
    list_filter = ("thorn_type", "point_cost")


admin.site.register(ThornRating)
admin.site.register(Fetter)
admin.site.register(Passion)

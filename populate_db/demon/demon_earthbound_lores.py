"""
Populate database with Earthbound Lores from Demon: Earthbound Chapter 3.

These secret bodies of lore are blasphemous powers available to Earthbound demons.
They are crude, destructive forces that cannot be used in positive or subtle ways.
"""

from characters.models.demon.lore import Lore

# Lore of Chaos
lore_of_chaos = Lore.objects.get_or_create(
    name="Lore of Chaos",
    property_name="chaos",
    description="Control over the chaotic energies of realms beyond Creation; reality distortion, probability manipulation, summoning outsiders from chaos realms",
)[0]
lore_of_chaos.add_source("Demon: Earthbound", 87)

# Lore of Contamination
lore_of_contamination = Lore.objects.get_or_create(
    name="Lore of Contamination",
    property_name="contamination",
    description="Infuse Earthbound essence into objects, mortals, and places; create proxies, corrupt relics, taint locations with demonic power",
)[0]
lore_of_contamination.add_source("Demon: Earthbound", 89)

# Lore of Violation
lore_of_violation = Lore.objects.get_or_create(
    name="Lore of Violation",
    property_name="violation",
    description="Brutal control and damage to mortal minds; nightmare sending, mind rape, visions of terror, enslavement, soul devouring",
)[0]
lore_of_violation.add_source("Demon: Earthbound", 91)

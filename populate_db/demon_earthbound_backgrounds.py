"""
Populate database with Earthbound Backgrounds from Demon: Earthbound Chapter 3.

These Backgrounds are available for all Earthbound characters.
Normal Demon characters cannot take these Backgrounds unless they become
Earthbound over the course of a chronicle.
"""

from characters.models.core.background_block import Background

# Codex
codex = Background.objects.get_or_create(name="Codex", property_name="codex")[0]

# Cult
cult_bg = Background.objects.get_or_create(name="Cult", property_name="cult")[0]

# Hoard
hoard = Background.objects.get_or_create(name="Hoard", property_name="hoard")[0]

# Mastery
mastery = Background.objects.get_or_create(name="Mastery", property_name="mastery")[0]

# Thralls
thralls = Background.objects.get_or_create(name="Thralls", property_name="thralls")[0]

# Worship
worship = Background.objects.get_or_create(name="Worship", property_name="worship")[0]

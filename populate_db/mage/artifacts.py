from items.models.mage.sorcerer_artifact import SorcererArtifact

SorcererArtifact.objects.get_or_create(name="Eternal Light", rank=1, display=False)[
    0
].add_source("M20 Sorcerer", 108)
SorcererArtifact.objects.get_or_create(
    name="Reindeer Antler Rune Stones", rank=1, display=False
)[0].add_source("M20 Sorcerer", 108)
SorcererArtifact.objects.get_or_create(
    name="Reflection of the Inner Self", rank=2, display=False
)[0].add_source("M20 Sorcerer", 108)
SorcererArtifact.objects.get_or_create(
    name="The Secret-Keeper's Journal", rank=2, display=False
)[0].add_source("M20 Sorcerer", 108)
SorcererArtifact.objects.get_or_create(name="Witch's Bottle", rank=2, display=False)[
    0
].add_source("M20 Sorcerer", 109)
SorcererArtifact.objects.get_or_create(
    name="Osiris's Resting Place", rank=3, display=False
)[0].add_source("M20 Sorcerer", 109)
SorcererArtifact.objects.get_or_create(name="Silent Feet", rank=3, display=False)[
    0
].add_source("M20 Sorcerer", 110)
SorcererArtifact.objects.get_or_create(
    name="Sympathetic Bindings", rank=3, display=False
)[0].add_source("M20 Sorcerer", 110)
SorcererArtifact.objects.get_or_create(name="Witch's Steed", rank=3, display=False)[
    0
].add_source("M20 Sorcerer", 110)
SorcererArtifact.objects.get_or_create(name="Love Poppet", rank=4, display=False)[
    0
].add_source("M20 Sorcerer", 110)
SorcererArtifact.objects.get_or_create(name="Vision Skull", rank=4, display=False)[
    0
].add_source("M20 Sorcerer", 110)
SorcererArtifact.objects.get_or_create(
    name="Deshayes' Fatal Cup", rank=5, display=False
)[0].add_source("M20 Sorcerer", 110)

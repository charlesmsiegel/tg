from characters.models.mage.focus import CorruptedPractice
from populate_db.mage.practices_INC import (
    animalism,
    crazywisdom,
    faith,
    highritualmagick,
    hypertech,
    shamanism,
    yoga,
)

abyssalism = (
    CorruptedPractice.objects.get_or_create(name="Abyssalism", parent_practice=crazywisdom)[0]
    .add_source("Book of the Fallen", 139)
    .add_source("Prism of Focus", 59)
)
feralism = (
    CorruptedPractice.objects.get_or_create(name="Feralism", parent_practice=animalism)[0]
    .add_source("Prism of Focus", 39)
    .add_source("Book of the Fallen", 142)
)
theblackmass = (
    CorruptedPractice.objects.get_or_create(name="The Black Mass", parent_practice=faith)[0]
    .add_source("Prism of Focus", 71)
    .add_source("Book of the Fallen", 140)
)
goetia = (
    CorruptedPractice.objects.get_or_create(name="Goetia", parent_practice=highritualmagick)[0]
    .add_source("Prism of Focus", 80)
    .add_source("Book of the Fallen", 143)
)
infernalsciences = (
    CorruptedPractice.objects.get_or_create(name="Infernal Sciences", parent_practice=hypertech)[0]
    .add_source("Prism of Focus", 84)
    .add_source("Book of the Fallen", 144)
)
demonism = (
    CorruptedPractice.objects.get_or_create(name="Demonism", parent_practice=shamanism)[0]
    .add_source("Prism of Focus", 112)
    .add_source("Book of the Fallen", 141)
)
vamamarga = (
    CorruptedPractice.objects.get_or_create(name="Vamamarga", parent_practice=yoga)[0]
    .add_source("Prism of Focus", 124)
    .add_source("Book of the Fallen", 145)
)

for cp in CorruptedPractice.objects.all():
    cp.add_abilities([x for x in cp.parent_practice.abilities.all()])
    cp.instruments.add(*cp.parent_practice.instruments.all())
    cp.common_resonance_traits.add(*cp.parent_practice.common_resonance_traits.all())
    cp.save()

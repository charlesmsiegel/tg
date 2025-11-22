from characters.models.mage.focus import SpecializedPractice
from populate_db.magefactions import (
    ab,
    ahl_i_batin,
    bataa,
    cc,
    cok,
    cox,
    ds,
    eu,
    hollow_ones,
    itx,
    kopa_loei,
    ngoma,
    nwo,
    ooh,
    prog,
    soe,
    soh,
    syn,
    taftani,
    templars,
    va,
    ve,
    verb,
    wulung,
)
from populate_db.mage.practices_INC import (
    alchemy,
    artofdesire,
    craftwork,
    crazywisdom,
    cybernetics,
    dominion,
    elementalism,
    faith,
    guttermagick,
    highritualmagick,
    hypertech,
    invigoration,
    martialarts,
    medicinework,
    realityhacking,
    shamanism,
    voudoun,
    weirdscience,
    witchcraft,
    yoga,
)

theroyalart = SpecializedPractice.objects.get_or_create(
    name="The Royal Art", parent_practice=alchemy, faction=cok
)[0].add_source("Prism of Focus", 36)
hypereconomics = (
    SpecializedPractice.objects.get_or_create(
        name="Hypereconomics", parent_practice=artofdesire, faction=syn
    )[0]
    .add_source("Mage: the Ascension 20th Anniversary Edition", 573)
    .add_source("Prism of Focus", 45)
)
weaving = SpecializedPractice.objects.get_or_create(
    name="Weaving", parent_practice=craftwork, faction=taftani
)[0].add_source("Prism of Focus", 56)
occultation = SpecializedPractice.objects.get_or_create(
    name="Occultation", parent_practice=crazywisdom, faction=ahl_i_batin
)[0].add_source("Prism of Focus", 59)
integrativetechnology = SpecializedPractice.objects.get_or_create(
    name="Integrative Technology", parent_practice=cybernetics, faction=itx
)[0].add_source("Prism of Focus", 62)
authority = SpecializedPractice.objects.get_or_create(
    name="Authority", parent_practice=dominion, faction=nwo
)[0].add_source("Prism of Focus", 65)
wayfinding = SpecializedPractice.objects.get_or_create(
    name="Wayfinding", parent_practice=elementalism, faction=kopa_loei
)[0].add_source("Prism of Focus", 68)
harmony = SpecializedPractice.objects.get_or_create(
    name="Harmony", parent_practice=faith, faction=cc
)[0].add_source("Prism of Focus", 71)
gladiusdomioni = SpecializedPractice.objects.get_or_create(
    name="Galdius Domini", parent_practice=faith, faction=templars
)[0].add_source("Prism of Focus", 71)
thescene = SpecializedPractice.objects.get_or_create(
    name="The Scene", parent_practice=guttermagick, faction=hollow_ones
)[0].add_source("Prism of Focus", 77)
nyeredzi = SpecializedPractice.objects.get_or_create(
    name="Nyeredzi", parent_practice=highritualmagick, faction=ngoma
)[0].add_source("Prism of Focus", 80)
ceremonialmagick = SpecializedPractice.objects.get_or_create(
    name="Ceremonial Magick", parent_practice=highritualmagick, faction=ooh
)[0].add_source("Prism of Focus", 81)
bureaucracy = SpecializedPractice.objects.get_or_create(
    name="Bureaucracy", parent_practice=highritualmagick, faction=wulung
)[0].add_source("Prism of Focus", 81)
tecknology = SpecializedPractice.objects.get_or_create(
    name="Tecknology", parent_practice=hypertech, faction=ve
)[0].add_source("Prism of Focus", 85)
lakashim = SpecializedPractice.objects.get_or_create(
    name="Lakashim", parent_practice=invigoration, faction=cox
)[0].add_source("Prism of Focus", 90)
do = (
    SpecializedPractice.objects.get_or_create(
        name="Do", parent_practice=martialarts, faction=ab
    )[0]
    .add_source("Mage: the Ascension 20th Anniversary Edition", 292)
    .add_source("Prism of Focus", 96)
)
biotech = SpecializedPractice.objects.get_or_create(
    name="Biotech", parent_practice=medicinework, faction=prog
)[0].add_source("Prism of Focus", 101)
artemissgift = SpecializedPractice.objects.get_or_create(
    name="Artemis's Gift", parent_practice=medicinework, faction=soh
)[0].add_source("Prism of Focus", 101)
realitycoding = SpecializedPractice.objects.get_or_create(
    name="Reality Coding", parent_practice=realityhacking, faction=va
)[0].add_source("Prism of Focus", 109)
spiritties = SpecializedPractice.objects.get_or_create(
    name="Spirit Ties", parent_practice=shamanism, faction=ds
)[0].add_source("Prism of Focus", 113)
asagwe = SpecializedPractice.objects.get_or_create(
    name="Asagwe", parent_practice=voudoun, faction=bataa
)[0].add_source("Prism of Focus", 115)
ethertech = SpecializedPractice.objects.get_or_create(
    name="Ethertech", parent_practice=weirdscience, faction=soe
)[0].add_source("Prism of Focus", 118)
theoldways = SpecializedPractice.objects.get_or_create(
    name="The Old Ways", parent_practice=witchcraft, faction=verb
)[0].add_source("Prism of Focus", 122)
wheeltending = SpecializedPractice.objects.get_or_create(
    name="Wheel-Tending", parent_practice=yoga, faction=eu
)[0].add_source("Prism of Focus", 124)

for sp in SpecializedPractice.objects.all():
    sp.add_abilities([x for x in sp.parent_practice.abilities.all()])
    sp.instruments.add(*sp.parent_practice.instruments.all())
    sp.common_resonance_traits.add(*sp.parent_practice.common_resonance_traits.all())
    sp.benefit = sp.parent_practice.benefit
    sp.penalty = sp.parent_practice.penalty
    sp.save()

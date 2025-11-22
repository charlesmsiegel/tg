from characters.models.mage.focus import Tenet
from populate_db.mage.practices_INC import (
    alchemy,
    animalism,
    appropriation,
    artofdesire,
    bardism,
    chaosmagick,
    charity,
    craftwork,
    crazywisdom,
    cybernetics,
    dominion,
    elementalism,
    faith,
    godbonding,
    guttermagick,
    highritualmagick,
    hypertech,
    invigoration,
    maleficia,
    martialarts,
    mediacontrol,
    medicinework,
    mediumship,
    psionics,
    realityhacking,
    shamanism,
    voudoun,
    weirdscience,
    witchcraft,
    yoga,
)

a_rational_universe = Tenet.objects.get_or_create(
    name="A Rational Universe", tenet_type="met"
)[0].add_source("Prism of Focus", 16)
a_rational_universe.associated_practices.add(
    alchemy, craftwork, cybernetics, hypertech, realityhacking
)
a_rational_universe.limited_practices.add(
    chaosmagick, crazywisdom, guttermagick, voudoun, witchcraft
)
as_above_so_below = Tenet.objects.get_or_create(
    name="As Above, So Below", tenet_type="met"
)[0].add_source("Prism of Focus", 16)
as_above_so_below.associated_practices.add(
    alchemy, dominion, faith, highritualmagick, witchcraft
)
as_above_so_below.limited_practices.add(
    artofdesire, chaosmagick, hypertech, realityhacking, weirdscience
)
fall_from_grace = Tenet.objects.get_or_create(name="Fall From Grace", tenet_type="met")[
    0
].add_source("Prism of Focus", 16)
fall_from_grace.associated_practices.add(animalism, faith, godbonding, highritualmagick)
fall_from_grace.limited_practices.add(
    hypertech, invigoration, medicinework, realityhacking, yoga
)
reality_is_a_lie = Tenet.objects.get_or_create(
    name="Reality is a Lie", tenet_type="met"
)[0].add_source("Prism of Focus", 16)
reality_is_a_lie.associated_practices.add(
    bardism, chaosmagick, crazywisdom, martialarts, yoga
)
reality_is_a_lie.limited_practices.add(
    craftwork, cybernetics, elementalism, highritualmagick, weirdscience
)
the_divine_is_real = Tenet.objects.get_or_create(
    name="The Divine is Real", tenet_type="met"
)[0].add_source("Prism of Focus", 16)
the_divine_is_real.associated_practices.add(
    faith, godbonding, invigoration, witchcraft, yoga
)
the_divine_is_real.limited_practices.add(bardism, realityhacking, weirdscience)
unfathomable_forces_at_work = Tenet.objects.get_or_create(
    name="Unfathomable Forces at Work", tenet_type="met"
)[0].add_source("Prism of Focus", 16)
unfathomable_forces_at_work.associated_practices.add(
    elementalism, invigoration, maleficia, psionics, voudoun
)
unfathomable_forces_at_work.limited_practices.add(
    artofdesire, cybernetics, dominion, realityhacking, weirdscience
)
i_am_chosen = Tenet.objects.get_or_create(name="I Am Chosen", tenet_type="per")[
    0
].add_source("Prism of Focus", 16)
i_am_chosen.associated_practices.add(
    cybernetics, godbonding, martialarts, mediumship, shamanism, witchcraft
)
i_am_chosen.limited_practices.add(
    alchemy, artofdesire, elementalism, highritualmagick, hypertech, invigoration
)
i_am_not_limited = Tenet.objects.get_or_create(
    name="I Am Not Limited", tenet_type="per"
)[0].add_source("Prism of Focus", 17)
i_am_not_limited.associated_practices.add(
    crazywisdom, highritualmagick, invigoration, psionics, weirdscience
)
i_am_not_limited.limited_practices.add(craftwork, martialarts, witchcraft)
i_am_special = Tenet.objects.get_or_create(name="I Am Special", tenet_type="per")[
    0
].add_source("Prism of Focus", 17)
i_am_special.associated_practices.add(
    bardism, dominion, elementalism, psionics, shamanism
)
i_am_special.limited_practices.add(chaosmagick, guttermagick, mediumship)
i_have_greater_understanding = Tenet.objects.get_or_create(
    name="I Have Greater Understanding", tenet_type="per"
)[0].add_source("Prism of Focus", 17)
i_have_greater_understanding.associated_practices.add(
    alchemy, crazywisdom, hypertech, medicinework, realityhacking
)
i_have_greater_understanding.limited_practices.add(
    bardism, godbonding, guttermagick, psionics
)
achieve_full_knowledge = Tenet.objects.get_or_create(
    name="Achieve Full Knowledge", tenet_type="asc"
)[0].add_source("Prism of Focus", 17)
achieve_full_knowledge.associated_practices.add(
    alchemy, hypertech, medicinework, realityhacking, weirdscience
)
achieve_full_knowledge.limited_practices.add(
    animalism, bardism, faith, godbonding, mediumship, yoga
)
annihilation_is_freedom = Tenet.objects.get_or_create(
    name="Annihilation is Freedom", tenet_type="asc"
)[0].add_source("Prism of Focus", 18)
annihilation_is_freedom.associated_practices.add(
    chaosmagick, guttermagick, maleficia, martialarts
)
annihilation_is_freedom.limited_practices.add(
    animalism, artofdesire, craftwork, elementalism, medicinework
)
build_a_utopia = Tenet.objects.get_or_create(name="Build a Utopia", tenet_type="asc")[
    0
].add_source("Prism of Focus", 18)
build_a_utopia.associated_practices.add(
    artofdesire, craftwork, cybernetics, dominion, faith, weirdscience
)
build_a_utopia.limited_practices.add(animalism, maleficia, voudoun)
existence_is_meaningless = Tenet.objects.get_or_create(
    name="Existence is Meaningless", tenet_type="asc"
)[0].add_source("Prism of Focus", 18)
existence_is_meaningless.associated_practices.add(animalism, bardism, guttermagick)
existence_is_meaningless.limited_practices.add(alchemy, faith, godbonding, medicinework)
merge_with_the_divine = Tenet.objects.get_or_create(
    name="Merge With the Divine", tenet_type="asc"
)[0].add_source("Prism of Focus", 18)
merge_with_the_divine.associated_practices.add(
    elementalism, faith, godbonding, mediumship, voudoun, yoga
)
merge_with_the_divine.limited_practices.add(
    chaosmagick, cybernetics, hypertech, weirdscience
)
power_is_its_own_reward = Tenet.objects.get_or_create(
    name="Power is its Own Reward", tenet_type="asc"
)[0].add_source("Prism of Focus", 18)
power_is_its_own_reward.associated_practices.add(
    artofdesire, dominion, highritualmagick, maleficia
)
power_is_its_own_reward.limited_practices.add(
    crazywisdom, faith, shamanism, voudoun, yoga
)
i_illuminate = Tenet.objects.get_or_create(name="I Illuminate", tenet_type="oth")[
    0
].add_source("Prism of Focus", 18)
i_illuminate.associated_practices.add(
    alchemy, charity, faith, highritualmagick, hypertech
)
i_illuminate.limited_practices.add(
    animalism, appropriation, maleficia, mediacontrol, psionics
)
i_rule = Tenet.objects.get_or_create(name="I Rule", tenet_type="oth")[0].add_source(
    "Prism of Focus", 18
)
i_rule.associated_practices.add(
    alchemy, artofdesire, dominion, highritualmagick, mediacontrol
)
i_rule.limited_practices.add(charity, faith, mediumship, shamanism, witchcraft)
i_serve = Tenet.objects.get_or_create(name="I Serve", tenet_type="oth")[0].add_source(
    "Prism of Focus", 19
)
i_serve.associated_practices.add(charity, faith, mediumship, shamanism, witchcraft)
i_serve.limited_practices.add(
    alchemy, artofdesire, dominion, highritualmagick, mediacontrol
)
mystical_insights = Tenet.objects.get_or_create(
    name="Mystical Insights", tenet_type="oth"
)[0].add_source("Prism of Focus", 19)
mystical_insights.associated_practices.add(
    alchemy, chaosmagick, crazywisdom, highritualmagick, witchcraft
)
mystical_insights.limited_practices.add(cybernetics, faith, hypertech, mediacontrol)
scientific_experimentation = Tenet.objects.get_or_create(
    name="Scientific Experimentation", tenet_type="oth"
)[0].add_source("Prism of Focus", 19)
scientific_experimentation.associated_practices.add(
    alchemy, craftwork, cybernetics, highritualmagick, hypertech, weirdscience
)
scientific_experimentation.limited_practices.add(
    chaosmagick, crazywisdom, faith, maleficia, shamanism, witchcraft
)
divine_revelations = Tenet.objects.get_or_create(
    name="Divine Revelations", tenet_type="oth"
)[0].add_source("Prism of Focus", 19)
divine_revelations.associated_practices.add(
    crazywisdom, faith, godbonding, maleficia, shamanism
)
divine_revelations.limited_practices.add(
    alchemy, highritualmagick, hypertech, martialarts, weirdscience
)
closed_paradigm = Tenet.objects.get_or_create(name="Closed Paradigm", tenet_type="oth")[
    0
].add_source("Prism of Focus", 19)
closed_paradigm.associated_practices.add(cybernetics, dominion, hypertech)
closed_paradigm.limited_practices.add(
    artofdesire, chaosmagick, crazywisdom, guttermagick, weirdscience
)
hierarchical_paradigm = Tenet.objects.get_or_create(
    name="Hierarchical Paradigm", tenet_type="oth"
)[0].add_source("Prism of Focus", 19)
hierarchical_paradigm.associated_practices.add(
    dominion, godbonding, martialarts, weirdscience
)
hierarchical_paradigm.limited_practices.add(
    chaosmagick, cybernetics, faith, highritualmagick, hypertech
)
open_paradigm = Tenet.objects.get_or_create(name="Open Paradigm", tenet_type="oth")[
    0
].add_source("Prism of Focus", 19)
open_paradigm.associated_practices.add(
    artofdesire, chaosmagick, crazywisdom, guttermagick, weirdscience
)
open_paradigm.limited_practices.add(cybernetics, dominion, hypertech)
reincarnation = Tenet.objects.get_or_create(name="Reincarnation", tenet_type="oth")[
    0
].add_source("Prism of Focus", 19)
reincarnation.associated_practices.add(
    chaosmagick, crazywisdom, martialarts, shamanism, witchcraft, yoga
)
reincarnation.limited_practices.add(alchemy, faith, hypertech, weirdscience)
yolo = Tenet.objects.get_or_create(name="YOLO", tenet_type="oth")[0].add_source(
    "Prism of Focus", 19
)
yolo.associated_practices.add(alchemy, faith, hypertech, weirdscience)
yolo.limited_practices.add(
    chaosmagick, crazywisdom, martialarts, shamanism, witchcraft, yoga
)

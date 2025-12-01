from characters.models.mage.focus import Paradigm
from populate_db.mage.tenets import (
    a_rational_universe,
    achieve_full_knowledge,
    annihilation_is_freedom,
    build_a_utopia,
    existence_is_meaningless,
    fall_from_grace,
    i_am_chosen,
    i_am_not_limited,
    i_am_special,
    i_have_greater_understanding,
    merge_with_the_divine,
    power_is_its_own_reward,
    reality_is_a_lie,
    the_divine_is_real,
    unfathomable_forces_at_work,
)

draladharma = Paradigm.objects.get_or_create(
    name="Draladharma",
)[
    0
].add_source("Lore of the Traditions", 32)
draladharma.set_tenets(a_rational_universe, i_have_greater_understanding, achieve_full_knowledge)

a_mechanistic_cosmos = Paradigm.objects.get_or_create(
    name="A Mechanistic Cosmos",
)[
    0
].add_source("Prism of Focus", 20)
a_mechanistic_cosmos.set_tenets(
    a_rational_universe, i_have_greater_understanding, achieve_full_knowledge
)
gods_and_monsters = Paradigm.objects.get_or_create(
    name="A World of Gods and Monsters",
)[
    0
].add_source("Prism of Focus", 20)
gods_and_monsters.set_tenets(unfathomable_forces_at_work, i_am_chosen, power_is_its_own_reward)
aliens_make_us = Paradigm.objects.get_or_create(name="Aliens Make Us What We Are")[0].add_source(
    "Prism of Focus", 21
)
aliens_make_us.set_tenets(unfathomable_forces_at_work, i_am_special, build_a_utopia)
all_power_from_god = Paradigm.objects.get_or_create(name="All Power Comes From God(s)")[
    0
].add_source("Prism of Focus", 21)
all_power_from_god.set_tenets(the_divine_is_real, i_am_chosen, power_is_its_own_reward)
all_power_from_sin = (
    Paradigm.objects.get_or_create(name="All Power Comes From Sin")[0]
    .add_source("Prism of Focus", 21)
    .add_source("Book of the Fallen", 131)
)
all_power_from_sin.set_tenets(the_divine_is_real, i_am_not_limited, annihilation_is_freedom)
all_the_worlds_a_stage = Paradigm.objects.get_or_create(name="All the World's a Stage")[
    0
].add_source("Prism of Focus", 21)
all_the_worlds_a_stage.set_tenets(reality_is_a_lie, i_am_special, existence_is_meaningless)
ancestor_veneration = Paradigm.objects.get_or_create(name="Ancestor Veneration")[0].add_source(
    "Prism of Focus", 21
)
ancestor_veneration.set_tenets(
    the_divine_is_real, i_have_greater_understanding, merge_with_the_divine
)
ancient_wisdom = Paradigm.objects.get_or_create(name="Ancient Wisdom is the Key")[0].add_source(
    "Prism of Focus", 22
)
ancient_wisdom.set_tenets(fall_from_grace, i_have_greater_understanding, build_a_utopia)
barbarism_is_true = (
    Paradigm.objects.get_or_create(name="Barbarism is the Truest State of Man")[0]
    .add_source("Book of the Fallen", 132)
    .add_source("Prism of Focus", 22)
)
barbarism_is_true.set_tenets(fall_from_grace, i_am_not_limited, build_a_utopia)
bring_back_the_golden_age = Paradigm.objects.get_or_create(name="Bring Back the Golden Age!")[
    0
].add_source("Prism of Focus", 22)
bring_back_the_golden_age.set_tenets(fall_from_grace, i_am_special, build_a_utopia)
consciousness_is_reality = Paradigm.objects.get_or_create(
    name="Consciousness is the Only True Reality"
)[0].add_source("Prism of Focus", 22)
consciousness_is_reality.set_tenets(reality_is_a_lie, i_am_special, power_is_its_own_reward)
cosmic_horror = (
    Paradigm.objects.get_or_create(name="Cosmic Horror is the Only Truth")[0]
    .add_source("Book of the Fallen", 132)
    .add_source("Prism of Focus", 22)
)
cosmic_horror.set_tenets(reality_is_a_lie, i_have_greater_understanding, merge_with_the_divine)
divine_and_alive = Paradigm.objects.get_or_create(
    name="Creation's Divine and Alive",
)[
    0
].add_source("Prism of Focus", 23)
divine_and_alive.set_tenets(the_divine_is_real, i_am_special, achieve_full_knowledge)
divine_order_earthly_chaos = Paradigm.objects.get_or_create(
    name="Divine Order and Earthly Chaos",
)[
    0
].add_source("Prism of Focus", 23)
divine_order_earthly_chaos.set_tenets(
    the_divine_is_real, i_have_greater_understanding, achieve_full_knowledge
)
embrace_the_threshold = Paradigm.objects.get_or_create(name="Embrace the Threshold")[0].add_source(
    "Prism of Focus", 24
)
embrace_the_threshold.set_tenets(reality_is_a_lie, i_am_not_limited, achieve_full_knowledge)
everyones_against_me = (
    Paradigm.objects.get_or_create(name="Everyone's Against Me, so Whatever I do is Justified")[0]
    .add_source("Book of the Fallen", 133)
    .add_source("Prism of Focus", 24)
)
everyones_against_me.set_tenets(unfathomable_forces_at_work, i_am_special, existence_is_meaningless)
everything_is_chaos = Paradigm.objects.get_or_create(
    name="Everything is Chaos",
)[
    0
].add_source("Prism of Focus", 24)
everything_is_chaos.set_tenets(unfathomable_forces_at_work, i_am_special, existence_is_meaningless)
everything_is_data = Paradigm.objects.get_or_create(
    name="Everything is Data",
)[
    0
].add_source("Prism of Focus", 25)
everything_is_data.set_tenets(a_rational_universe, i_am_not_limited, achieve_full_knowledge)
everything_is_an_illusion = Paradigm.objects.get_or_create(
    name="Everything's an Illusion, Prison, or Mistake"
)[0].add_source("Prism of Focus", 24)
everything_is_an_illusion.set_tenets(
    reality_is_a_lie, i_have_greater_understanding, annihilation_is_freedom
)
everything_has_value = Paradigm.objects.get_or_create(name="Everything Has Value")[0].add_source(
    "Prism of Focus", 24
)
everything_has_value.set_tenets(
    unfathomable_forces_at_work, i_have_greater_understanding, power_is_its_own_reward
)
evil_is_necessary = (
    Paradigm.objects.get_or_create(name="Evil is Necessary, and so I am Evil")[0]
    .add_source("Book of the Fallen", 134)
    .add_source("Prism of Focus", 25)
)
evil_is_necessary.set_tenets(the_divine_is_real, i_am_not_limited, build_a_utopia)
existence_is_unknowable = (
    Paradigm.objects.get_or_create(name="Existence is Unknowable, Irrational, and Sublime")[0]
    .add_source("Book of the Fallen", 134)
    .add_source("Prism of Focus", 25)
)
existence_is_unknowable.set_tenets(
    reality_is_a_lie, i_have_greater_understanding, existence_is_meaningless
)
forbidden_wisdom = (
    Paradigm.objects.get_or_create(name="Forbidden Wisdom is the Truest Source of Power")[0]
    .add_source("Book of the Fallen", 135)
    .add_source("Prism of Focus", 25)
)
forbidden_wisdom.set_tenets(fall_from_grace, i_am_chosen, achieve_full_knowledge)
holographic_reality = Paradigm.objects.get_or_create(name="Holographic Reality")[0].add_source(
    "Prism of Focus", 20
)
holographic_reality.set_tenets(
    reality_is_a_lie, i_have_greater_understanding, achieve_full_knowledge
)
i_am_all = (
    Paradigm.objects.get_or_create(name="I am All")[0]
    .add_source("Book of the Fallen", 135)
    .add_source("Prism of Focus", 25)
)
i_am_all.set_tenets(reality_is_a_lie, i_am_special, annihilation_is_freedom)
im_a_predator = (
    Paradigm.objects.get_or_create(name="I'm a Predator, and the World is My Prey")[0]
    .add_source("Book of the Fallen", 135)
    .add_source("Prism of Focus", 26)
)
im_a_predator.set_tenets(unfathomable_forces_at_work, i_am_special, power_is_its_own_reward)
indulgence = (
    Paradigm.objects.get_or_create(name="Indulgence is Nature's Only Law")[0]
    .add_source("Book of the Fallen", 136)
    .add_source("Prism of Focus", 26)
)
indulgence.set_tenets(
    unfathomable_forces_at_work, i_have_greater_understanding, power_is_its_own_reward
)
have_faith = Paradigm.objects.get_or_create(
    name="It's All Good - Have Faith!",
)[
    0
].add_source("Prism of Focus", 26)
have_faith.set_tenets(the_divine_is_real, i_am_chosen, merge_with_the_divine)
might_is_right = Paradigm.objects.get_or_create(
    name="Might Is Right",
)[
    0
].add_source("Prism of Focus", 26)
might_is_right.set_tenets(unfathomable_forces_at_work, i_am_not_limited, power_is_its_own_reward)
more_is_more = Paradigm.objects.get_or_create(
    name="More is More",
)[
    0
].add_source("Prism of Focus", 26)
more_is_more.set_tenets(a_rational_universe, i_am_not_limited, power_is_its_own_reward)
one_way_trip_to_oblivion = Paradigm.objects.get_or_create(name="One Way Trip to Oblivion")[
    0
].add_source("Prism of Focus", 26)
one_way_trip_to_oblivion.set_tenets(
    fall_from_grace, i_have_greater_understanding, annihilation_is_freedom
)
only_the_strongest = (
    Paradigm.objects.get_or_create(name="Only the Strongest Deserve to Survive")[0]
    .add_source("Book of the Fallen", 137)
    .add_source("Prism of Focus", 27)
)
only_the_strongest.set_tenets(unfathomable_forces_at_work, i_am_special, power_is_its_own_reward)
people_are_shit = (
    Paradigm.objects.get_or_create(name="People are Shit")[0]
    .add_source("Book of the Fallen", 137)
    .add_source("Prism of Focus", 27)
)
people_are_shit.set_tenets(fall_from_grace, i_am_special, existence_is_meaningless)
philanthropy_in_all_things = Paradigm.objects.get_or_create(name="Philanthrop in All Things")[
    0
].add_source("Prism of Focus", 27)
philanthropy_in_all_things.set_tenets(the_divine_is_real, i_am_special, build_a_utopia)
power_trickles_down = Paradigm.objects.get_or_create(name="Power Trickles Down")[0].add_source(
    "Prism of Focus", 27
)
power_trickles_down.set_tenets(the_divine_is_real, i_am_special, merge_with_the_divine)
rebellion = (
    Paradigm.objects.get_or_create(name="Rebellion is the Road to Transcendence")[0]
    .add_source("Book of the Fallen", 137)
    .add_source("Prism of Focus", 27)
)
rebellion.set_tenets(the_divine_is_real, i_am_chosen, annihilation_is_freedom)
stormtroopers_of_the_abyss = (
    Paradigm.objects.get_or_create(name="We are Stormtroopers of the Abyss")[0]
    .add_source("Book of the Fallen", 138)
    .add_source("Prism of Focus", 29)
)
stormtroopers_of_the_abyss.set_tenets(
    unfathomable_forces_at_work, i_am_chosen, annihilation_is_freedom
)
tech_holds_all_answers = Paradigm.objects.get_or_create(
    name="Tech Holds All Answers",
)[
    0
].add_source("Prism of Focus", 28)
tech_holds_all_answers.set_tenets(a_rational_universe, i_have_greater_understanding, build_a_utopia)
transcend_limits = Paradigm.objects.get_or_create(name="Transcend Your Limits")[0].add_source(
    "Prism of Focus", 28
)
transcend_limits.set_tenets(reality_is_a_lie, i_am_not_limited, merge_with_the_divine)
turning_the_keys = Paradigm.objects.get_or_create(name="Turning the Keys to Reality")[0].add_source(
    "Prism of Focus", 28
)
turning_the_keys.set_tenets(a_rational_universe, i_am_special, achieve_full_knowledge)
we_are_meant_to_be_wild = Paradigm.objects.get_or_create(name="We Are Meant to be Wild")[
    0
].add_source("Prism of Focus", 29)
we_are_meant_to_be_wild.set_tenets(fall_from_grace, i_am_not_limited, existence_is_meaningless)
we_are_not_men = Paradigm.objects.get_or_create(name="We Are Not Men!")[0].add_source(
    "Prism of Focus", 29
)
we_are_not_men.set_tenets(unfathomable_forces_at_work, i_am_special, achieve_full_knowledge)
we_are_god = Paradigm.objects.get_or_create(name="We're All God(s) in Disguise")[0].add_source(
    "Prism of Focus", 29
)
we_are_god.set_tenets(the_divine_is_real, i_am_special, merge_with_the_divine)

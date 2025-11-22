from characters.models.werewolf.camp import Camp
from populate_db.werewolf.tribes import (
    black_furies,
    bone_gnawers,
    children_of_gaia,
    fianna,
    get_of_fenris,
    glass_walker,
    red_talons,
    shadow_lords,
    silent_striders,
    silver_fangs,
    stargazers,
    uktena,
    wendigo,
)

Camp.objects.get_or_create(name="Amazons of Diana", tribe=black_furies)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 491
)
Camp.objects.get_or_create(name="Bacchantes/Maenads", tribe=black_furies)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 491
)
Camp.objects.get_or_create(name="Freebooters", tribe=black_furies)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 491
)
Camp.objects.get_or_create(name="Moon-Daughters", tribe=black_furies)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 492
)
Camp.objects.get_or_create(name="Order of Our Merciful Mother", tribe=black_furies)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 492)
Camp.objects.get_or_create(name="The Sisterhood", tribe=black_furies)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 492
)
Camp.objects.get_or_create(name="The Temple of Artemis", tribe=black_furies)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 492)
Camp.objects.get_or_create(name="Deserters", tribe=bone_gnawers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 492
)
Camp.objects.get_or_create(name="Frankenweilers", tribe=bone_gnawers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 492
)
Camp.objects.get_or_create(name="Maneaters", tribe=bone_gnawers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 492
)
Camp.objects.get_or_create(name="Hillfolk", tribe=bone_gnawers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 493
)
Camp.objects.get_or_create(name="The Hood", tribe=bone_gnawers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 493
)
Camp.objects.get_or_create(name="Rat Finks", tribe=bone_gnawers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 493
)
Camp.objects.get_or_create(name="Road Warders", tribe=bone_gnawers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 493
)
Camp.objects.get_or_create(name="The Swarm", tribe=bone_gnawers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 493
)
Camp.objects.get_or_create(name="Aethera Inamorata", tribe=children_of_gaia)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 493)
Camp.objects.get_or_create(name="Angels in the Garden", tribe=children_of_gaia)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 493)
Camp.objects.get_or_create(name="The Anounted Ones", tribe=children_of_gaia)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 493)
Camp.objects.get_or_create(name="Bringers of Eternal Peace", tribe=children_of_gaia)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 494)
Camp.objects.get_or_create(name="Demeter's Daughters", tribe=children_of_gaia)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 494)
Camp.objects.get_or_create(name="Imminent Strike", tribe=children_of_gaia)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 494)
Camp.objects.get_or_create(name="The One Tree", tribe=children_of_gaia)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 494
)
Camp.objects.get_or_create(name="The Patient Deed", tribe=children_of_gaia)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 494)
Camp.objects.get_or_create(name="Seekers of the Lost Tribes", tribe=children_of_gaia)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 494)
Camp.objects.get_or_create(name="Servants of Unicorn", tribe=children_of_gaia)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 494)
Camp.objects.get_or_create(name="Brotherhood of Herne", tribe=fianna)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 494
)
Camp.objects.get_or_create(name="Children of Dire", tribe=fianna)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 495
)
Camp.objects.get_or_create(name="Grandchildren of Fionn", tribe=fianna)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 495
)
Camp.objects.get_or_create(name="Mother's Fundamentalists", tribe=fianna)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 495
)
Camp.objects.get_or_create(name="Songkeepers", tribe=fianna)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 495
)
Camp.objects.get_or_create(name="Tuatha de Fionn", tribe=fianna)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 495
)
Camp.objects.get_or_create(name="Whispering Rovers", tribe=fianna)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 495
)
Camp.objects.get_or_create(name="The Fangs of Garm", tribe=get_of_fenris)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 495
)
Camp.objects.get_or_create(name="The Glorious Fist of Wotan", tribe=get_of_fenris)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 496)
Camp.objects.get_or_create(name="The Hand of Tyr", tribe=get_of_fenris)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 496
)
Camp.objects.get_or_create(name="Loki's Smile", tribe=get_of_fenris)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 496
)
Camp.objects.get_or_create(name="Mjolnir's Thunder", tribe=get_of_fenris)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 496
)
Camp.objects.get_or_create(name="The Swords of Heimdall", tribe=get_of_fenris)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 496)
Camp.objects.get_or_create(name="The Valkyria of Freya", tribe=get_of_fenris)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 497)
Camp.objects.get_or_create(name="Ymir's Sweat", tribe=get_of_fenris)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 497
)
Camp.objects.get_or_create(name="City Farmers", tribe=glass_walker)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 497
)
Camp.objects.get_or_create(name="Corporate Wolves", tribe=glass_walker)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 497
)
Camp.objects.get_or_create(name="Cyber Dogs", tribe=glass_walker)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 497
)
Camp.objects.get_or_create(name="Dies Ultimae", tribe=glass_walker)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 497
)
Camp.objects.get_or_create(name="Mechanical Awakening", tribe=glass_walker)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 497)
Camp.objects.get_or_create(name="Random Interrupts", tribe=glass_walker)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 498
)
Camp.objects.get_or_create(name="Umbral Pilots", tribe=glass_walker)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 498
)
Camp.objects.get_or_create(name="Urban Primitives", tribe=glass_walker)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 498
)
Camp.objects.get_or_create(name="Wise Guys", tribe=glass_walker)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 498
)
Camp.objects.get_or_create(name="The Dying Cubs", tribe=red_talons)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 498
)
Camp.objects.get_or_create(name="The Lodge of the Predator Kings", tribe=red_talons)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 498)
Camp.objects.get_or_create(name="Warders of the Land", tribe=red_talons)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 498
)
Camp.objects.get_or_create(name="Whelp's Compromise", tribe=red_talons)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 498
)
Camp.objects.get_or_create(name="The Masks", tribe=shadow_lords)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 499
)
Camp.objects.get_or_create(name="Bringers of Light", tribe=shadow_lords)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 499
)
Camp.objects.get_or_create(name="Children of Crow", tribe=shadow_lords)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 499
)
Camp.objects.get_or_create(name="Judges of Doom", tribe=shadow_lords)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 499
)
Camp.objects.get_or_create(name="Lords of the Summit", tribe=shadow_lords)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 499)
Camp.objects.get_or_create(name="Revolutionary Guard", tribe=shadow_lords)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 499)
Camp.objects.get_or_create(name="Society of Nidhogg", tribe=shadow_lords)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 499
)
Camp.objects.get_or_create(name="The Bitter Hex", tribe=silent_striders)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 500
)
Camp.objects.get_or_create(name="The Dispossessed", tribe=silent_striders)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 500)
Camp.objects.get_or_create(name="Harbingers", tribe=silent_striders)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 500
)
Camp.objects.get_or_create(name="Eaters of the Dead", tribe=silent_striders)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 500)
Camp.objects.get_or_create(name="Seekers", tribe=silent_striders)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 500
)
Camp.objects.get_or_create(name="Swords of Night", tribe=silent_striders)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 500
)
Camp.objects.get_or_create(name="Wayfarers", tribe=silent_striders)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 500
)
Camp.objects.get_or_create(name="Grey Raptors", tribe=silver_fangs)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 502
)
Camp.objects.get_or_create(name="Ivory Priesthood", tribe=silver_fangs)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 502
)
Camp.objects.get_or_create(name="Masters of the Seal", tribe=silver_fangs)[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 502)
Camp.objects.get_or_create(name="Renewal", tribe=silver_fangs)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 502
)
Camp.objects.get_or_create(name="Ana-gamin", tribe=stargazers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 502
)
Camp.objects.get_or_create(
    name="The Heavenly Successors of the Demon-Eater", tribe=stargazers
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 502)
Camp.objects.get_or_create(name="The Inner Path", tribe=stargazers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 503
)
Camp.objects.get_or_create(name="Klaital Puk", tribe=stargazers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 503
)
Camp.objects.get_or_create(name="Ouroboroans", tribe=stargazers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 503
)
Camp.objects.get_or_create(name="The Sacred Thread", tribe=stargazers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 503
)
Camp.objects.get_or_create(name="Trance Runners", tribe=stargazers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 503
)
Camp.objects.get_or_create(name="The World Tree", tribe=stargazers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 503
)
Camp.objects.get_or_create(name="The Zephyr", tribe=stargazers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 503
)
Camp.objects.get_or_create(name="The Metastic Birth", tribe=stargazers)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 503
)
Camp.objects.get_or_create(name="Bane Tenders", tribe=uktena)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 503
)
Camp.objects.get_or_create(name="Earth Guides", tribe=uktena)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 504
)
Camp.objects.get_or_create(name="Path Dancers", tribe=uktena)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 504
)
Camp.objects.get_or_create(name="Scouts", tribe=uktena)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 504
)
Camp.objects.get_or_create(name="Skywalkers", tribe=uktena)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 504
)
Camp.objects.get_or_create(name="Society of Bitter Frost", tribe=uktena)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 504
)
Camp.objects.get_or_create(name="Web Walkers", tribe=uktena)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 504
)
Camp.objects.get_or_create(name="Wyld Children", tribe=uktena)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 504
)
Camp.objects.get_or_create(name="Gluskap's Lodge", tribe=wendigo)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 504
)
Camp.objects.get_or_create(name="Myeengun's Lodge", tribe=wendigo)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 504
)
Camp.objects.get_or_create(name="The Sacred Hoop", tribe=wendigo)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 504
)
Camp.objects.get_or_create(name="The Secret Hoop", tribe=wendigo)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 504
)
Camp.objects.get_or_create(name="The Warpath", tribe=wendigo)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 505
)
Camp.objects.get_or_create(name="Fang Breakers", tribe=None)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 505
)
Camp.objects.get_or_create(name="Ghost Dancers", tribe=None)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 505
)
Camp.objects.get_or_create(name="Lazarite Movement", tribe=None)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 505
)
Camp.objects.get_or_create(name="Hakken", tribe=shadow_lords)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 506
)
Camp.objects.get_or_create(name="Boli Zousizhe", tribe=glass_walker)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 505
)
Camp.objects.get_or_create(name="Kucha Ekundu", tribe=red_talons)[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 507
)

Camp.objects.get_or_create(
    name="Lodge of the Moon", tribe=silver_fangs, camp_type="lodge"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 501)
Camp.objects.get_or_create(
    name="Lodge of the Sun", tribe=silver_fangs, camp_type="lodge"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 501)
Camp.objects.get_or_create(
    name="House Austere Howl", tribe=silver_fangs, camp_type="house"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 501)
Camp.objects.get_or_create(
    name="The Blood-Red Crest", tribe=silver_fangs, camp_type="house"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 501)
Camp.objects.get_or_create(
    name="Clan Crescent Moon", tribe=silver_fangs, camp_type="house"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 501)
Camp.objects.get_or_create(
    name="House Gleaming Eye", tribe=silver_fangs, camp_type="house"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 501)
Camp.objects.get_or_create(
    name="House Unbreakable Hearth", tribe=silver_fangs, camp_type="house"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 501)
Camp.objects.get_or_create(
    name="House Wise Heart", tribe=silver_fangs, camp_type="house"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 502)
Camp.objects.get_or_create(name="House Wyrmfoe", tribe=silver_fangs, camp_type="house")[
    0
].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 502)
Camp.objects.get_or_create(
    name="Renewalists", tribe=silver_fangs, camp_type="philosophy"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 502)
Camp.objects.get_or_create(
    name="Royalists", tribe=silver_fangs, camp_type="philosophy"
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 502)

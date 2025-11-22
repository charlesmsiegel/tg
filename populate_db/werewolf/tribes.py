from characters.models.werewolf.tribe import Tribe

black_furies = Tribe.objects.get_or_create(name="Black Furies", willpower=3)[0]
bone_gnawers = Tribe.objects.get_or_create(name="Bone Gnawers", willpower=4)[0]
children_of_gaia = Tribe.objects.get_or_create(name="Children of Gaia", willpower=4)[0]
fianna = Tribe.objects.get_or_create(name="Fianna", willpower=3)[0]
get_of_fenris = Tribe.objects.get_or_create(name="Get of Fenris", willpower=3)[0]
glass_walker = Tribe.objects.get_or_create(name="Glass Walkers", willpower=3)[0]
red_talons = Tribe.objects.get_or_create(name="Red Talons", willpower=3)[0]
shadow_lords = Tribe.objects.get_or_create(name="Shadow Lords", willpower=3)[0]
silent_striders = Tribe.objects.get_or_create(name="Silent Striders", willpower=3)[0]
silver_fangs = Tribe.objects.get_or_create(name="Silver Fangs", willpower=3)[0]
stargazers = Tribe.objects.get_or_create(name="Stargazers", willpower=4)[0]
uktena = Tribe.objects.get_or_create(name="Uktena", willpower=3)[0]
wendigo = Tribe.objects.get_or_create(name="Wendigo", willpower=4)[0]

Tribe.objects.get_or_create(name="Black Spiral Dancers", willpower=3)[0]

Tribe.objects.get_or_create(name="Bunyip", willpower=4)[0]
Tribe.objects.get_or_create(name="Croatan", willpower=4)[0]
Tribe.objects.get_or_create(name="White Howlers", willpower=3)[0]

from items.models.core.material import Material

bone = Material.objects.get_or_create(name="Bone")[0]
cloth = Material.objects.get_or_create(name="Cloth", is_hard=False)[0]
iron = Material.objects.get_or_create(name="Iron")[0]
leather = Material.objects.get_or_create(name="Leather", is_hard=False)[0]
paper = Material.objects.get_or_create(name="Paper", is_hard=False)[0]
parchment = Material.objects.get_or_create(name="Parchment", is_hard=False)[0]
steel = Material.objects.get_or_create(name="Steel")[0]
vellum = Material.objects.get_or_create(name="Vellum", is_hard=False)[0]
wood = Material.objects.get_or_create(name="Wood")[0]
glass = Material.objects.get_or_create(name="Glass")[0]
crystal = Material.objects.get_or_create(name="Crystal")[0]
silver = Material.objects.get_or_create(name="Silver")[0]
brass = Material.objects.get_or_create(name="Brass")[0]
lead = Material.objects.get_or_create(name="Lead")[0]
gems = Material.objects.get_or_create(name="Gems")[0]
copper = Material.objects.get_or_create(name="Copper")[0]
stone = Material.objects.get_or_create(name="Stone")[0]
gold = Material.objects.get_or_create(name="Gold")[0]
petrified_wood = Material.objects.get_or_create(name="Petrified Wood")[0]
ceramics = Material.objects.get_or_create(name="Ceramics")[0]

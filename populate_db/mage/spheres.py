from characters.models.mage.sphere import Sphere

correspondence = Sphere.objects.get_or_create(
    name="Correspondence", property_name="correspondence"
)[0]
spirit = Sphere.objects.get_or_create(name="Spirit", property_name="spirit")[0]
time = Sphere.objects.get_or_create(name="Time", property_name="time")[0]
forces = Sphere.objects.get_or_create(name="Forces", property_name="forces")[0]
matter = Sphere.objects.get_or_create(name="Matter", property_name="matter")[0]
life = Sphere.objects.get_or_create(name="Life", property_name="life")[0]
entropy = Sphere.objects.get_or_create(name="Entropy", property_name="entropy")[0]
prime = Sphere.objects.get_or_create(name="Prime", property_name="prime")[0]
mind = Sphere.objects.get_or_create(name="Mind", property_name="mind")[0]

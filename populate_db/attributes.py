from characters.models.core.attribute_block import Attribute

strength = Attribute.objects.get_or_create(name="Strength", property_name="strength")[0]
dexterity = Attribute.objects.get_or_create(name="Dexterity", property_name="dexterity")[0]
stamina = Attribute.objects.get_or_create(name="Stamina", property_name="stamina")[0]
perception = Attribute.objects.get_or_create(name="Perception", property_name="perception")[0]
intelligence = Attribute.objects.get_or_create(name="Intelligence", property_name="intelligence")[0]
wits = Attribute.objects.get_or_create(name="Wits", property_name="wits")[0]
charisma = Attribute.objects.get_or_create(name="Charisma", property_name="charisma")[0]
manipulation = Attribute.objects.get_or_create(name="Manipulation", property_name="manipulation")[0]
appearance = Attribute.objects.get_or_create(name="Appearance", property_name="appearance")[0]

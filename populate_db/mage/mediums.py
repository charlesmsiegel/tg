from items.models.core.medium import Medium

book = Medium.objects.get_or_create(name="Book")[0]
journal = Medium.objects.get_or_create(
    name="Journal", length_modifier_type="/", length_modifier=40
)[0]
ebook = Medium.objects.get_or_create(name="eBook", length_modifier_type="/", length_modifier=20)[0]
flash_drive = Medium.objects.get_or_create(
    name="Flash Drive", length_modifier_type="/", length_modifier=10
)[0]
scrolls = Medium.objects.get_or_create(
    name="Scrolls", length_modifier_type="/", length_modifier=20
)[0]
software = Medium.objects.get_or_create(
    name="Software", length_modifier_type="/", length_modifier=1
)[0]
tablets = Medium.objects.get_or_create(
    name="Tablets", length_modifier_type="/", length_modifier=40
)[0]
audio = Medium.objects.get_or_create(name="Audio Recording")[0]
video = Medium.objects.get_or_create(
    name="Video Recording", length_modifier_type="/", length_modifier=20
)[0]

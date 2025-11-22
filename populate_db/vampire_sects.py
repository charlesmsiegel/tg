from characters.models.vampire.sect import VampireSect

# Create the four main Vampire sects

camarilla = VampireSect.objects.get_or_create(
    name="Camarilla",
    philosophy="Maintain the Masquerade at all costs; rule mortal world from shadows. "
    "Feudal structure with Princes ruling cities. The Camarilla follows the Six Traditions "
    "that govern vampire society and seeks to preserve vampire existence through secrecy.",
)[0]

sabbat = VampireSect.objects.get_or_create(
    name="Sabbat",
    philosophy="Reject Masquerade; prepare for Gehenna; freedom through chaos. "
    "Organized into packs led by Ductus; domains ruled by Archbishops. "
    "Practices rituals like the Vaulderie for pack bonding. Believes in actively preparing "
    "for the end times when the Antediluvians will rise.",
)[0]

anarch_movement = VampireSect.objects.get_or_create(
    name="Anarch Movement",
    philosophy="Freedom from elders; self-determination. Loose structure that varies by region. "
    "Rejects the authority of both Camarilla and Sabbat. Some view them as a Camarilla "
    "subdivision while others see them as truly independent. Led by Barons when leadership exists.",
)[0]

independent = VampireSect.objects.get_or_create(
    name="Independent",
    philosophy="Clan-specific philosophies and goals. These vampires do not formally align "
    "with Camarilla or Sabbat, maintaining their own traditions and hierarchies. "
    "Includes clans like Assamites, Followers of Set, Giovanni, and Ravnos.",
)[0]

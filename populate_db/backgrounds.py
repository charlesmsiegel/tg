from characters.models.core.background_block import Background

Background.objects.get_or_create(name="Contacts", property_name="contacts")[0]
Background.objects.get_or_create(name="Mentor", property_name="mentor")[0]
Background.objects.get_or_create(name="Allies", property_name="allies")[0]
Background.objects.get_or_create(name="Alternate Identity", property_name="alternate_identity")[0]
arcane = Background.objects.get_or_create(name="Arcane", property_name="arcane")[0]
arcane.alternate_name = "Cloaking"
arcane.save()
Background.objects.get_or_create(name="Artifact", property_name="artifact")[0]
avatar = Background.objects.get_or_create(name="Avatar", property_name="avatar")[0]
avatar.alternate_name = "Genius"
avatar.save()
Background.objects.get_or_create(name="Backup", property_name="backup")[0]
Background.objects.get_or_create(name="Blessing", property_name="blessing")[0]
Background.objects.get_or_create(name="Certification", property_name="certification")[0]
chantry = Background.objects.get_or_create(name="Chantry", property_name="chantry")[0]
chantry.alternate_name = "Construct"
chantry.save()
Background.objects.get_or_create(name="Cult", property_name="cult")[0]
Background.objects.get_or_create(name="Demesne", property_name="demesne")[0]
Background.objects.get_or_create(name="Destiny", property_name="destiny")[0]
dream = Background.objects.get_or_create(name="Dream", property_name="dream")[0]
dream.alternate_name = "Hypercram"
dream.save()
Background.objects.get_or_create(name="Enhancement", property_name="enhancement", multiplier=2)[0]
Background.objects.get_or_create(name="Fame", property_name="fame")[0]
familiar = Background.objects.get_or_create(name="Familiar", property_name="familiar")[0]
familiar.alternate_name = "Companion"
familiar.save()
Background.objects.get_or_create(name="Influence", property_name="influence")[0]
Background.objects.get_or_create(name="Legend", property_name="legend")[0]
Background.objects.get_or_create(name="Library", property_name="library")[0]
Background.objects.get_or_create(name="Node", property_name="node")[0]
Background.objects.get_or_create(name="Past Lives", property_name="past_lives")[0]
Background.objects.get_or_create(name="Patron", property_name="patron")[0]
Background.objects.get_or_create(name="Rank", property_name="rank")[0]
Background.objects.get_or_create(name="Requisitions", property_name="requisitions")[0]
Background.objects.get_or_create(name="Resources", property_name="resources")[0]
Background.objects.get_or_create(name="Retainers", property_name="retainers")[0]
sanctum = Background.objects.get_or_create(name="Sanctum", property_name="sanctum", multiplier=2)[0]
sanctum.alternate_name = "Laboratory"
sanctum.save()
Background.objects.get_or_create(name="Secret weapons", property_name="secret_weapons")[0]
Background.objects.get_or_create(name="Spies", property_name="spies")[0]
Background.objects.get_or_create(name="Status", property_name="status_background")[0]
Background.objects.get_or_create(name="Totem", property_name="totem", multiplier=2)[0]
Background.objects.get_or_create(name="Wonder", property_name="wonder")[0]

Background.objects.get_or_create(name="Chimera", property_name="chimera")[0]
Background.objects.get_or_create(name="Dreamers", property_name="dreamers")[0]
Background.objects.get_or_create(name="Holdings", property_name="holdings")[0]
Background.objects.get_or_create(name="Remembrance", property_name="remembrance")[0]
Background.objects.get_or_create(name="Retinue", property_name="retinue")[0]
Background.objects.get_or_create(name="Title", property_name="title")[0]
Background.objects.get_or_create(name="Treasure", property_name="treasure")[0]

Background.objects.get_or_create(name="Rituals", property_name="rituals")[0]
Background.objects.get_or_create(name="Herd", property_name="herd")[0]
Background.objects.get_or_create(name="Generation", property_name="generation")[0]
Background.objects.get_or_create(name="Domain", property_name="domain")[0]
Background.objects.get_or_create(
    name="Black Hand Membership", property_name="black_hand_membership"
)[0]

Background.objects.get_or_create(name="Ancestors", property_name="ancestors")[0]
Background.objects.get_or_create(name="Fate", property_name="fate")[0]
Background.objects.get_or_create(name="Fetish", property_name="fetish")[0]
Background.objects.get_or_create(name="Kinfolk", property_name="kinfolk_rating")[0]
Background.objects.get_or_create(name="Pure Breed", property_name="pure_breed")[0]
Background.objects.get_or_create(name="Rites", property_name="rites")[0]
Background.objects.get_or_create(name="Spirit Heritage", property_name="spirit_heritage")[0]


Background.objects.get_or_create(name="Eidolon", property_name="eidolon")[0]
Background.objects.get_or_create(name="Haunt", property_name="haunt")[0]
Background.objects.get_or_create(name="Legacy", property_name="legacy")[0]
Background.objects.get_or_create(name="Memoriam", property_name="memoriam")[0]
Background.objects.get_or_create(name="Notoriety", property_name="notoriety")[0]
Background.objects.get_or_create(name="Relic", property_name="relic")[0]

Background.objects.get_or_create(name="Elders", property_name="elders")[0]

Background.objects.get_or_create(name="Eminence", property_name="eminence")[0]
Background.objects.get_or_create(name="Followers", property_name="followers")[0]
Background.objects.get_or_create(name="Legacy", property_name="legacy")[0]
Background.objects.get_or_create(name="Pacts", property_name="pacts")[0]
Background.objects.get_or_create(name="Paragon", property_name="paragon")[0]
Background.objects.get_or_create(name="Ritual Knowledge", property_name="ritual_knowledge")[0]

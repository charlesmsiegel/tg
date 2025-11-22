from characters.models.demon.faction import DemonFaction

# The Five Major Demon Factions

# 1. Luciferans - Seekers of Their Lost Leader
luciferans = DemonFaction.objects.get_or_create(
    name="Luciferans",
    philosophy="Belief that first war was not truly lost; Lucifer will return to lead victory",
    goal="Locate Lucifer and resume war against Heaven",
    leadership="Scourge Nazriel (primary leader); Devil Grifiel (cunning commander)",
    tactics="Send outriders in packs globally to find demonic activity; Control media for intelligence gathering and propaganda; Maintain communications network among fallen",
)[0]

# 2. Faustians - Enslavers and Human Empire-Builders
faustians = DemonFaction.objects.get_or_create(
    name="Faustians",
    philosophy="Mortals are the key to power; control them utterly; use them for spiritual rebellion against God",
    goal="Enslave humanity and build demonic empire on Earth using mortal slaves as weapons against Heaven",
    leadership="Devil Belphigor (primary leader); Defiler Senivel (more humanistic faction)",
    tactics="Grant mortals cursed gifts and poisoned blessings; Establish elaborate pacts with thralls; Control world population increase; Maintain infrastructure of human vassalage",
)[0]

# 3. Reconcilers - Penitent Path to Redemption
reconcilers = DemonFaction.objects.get_or_create(
    name="Reconcilers",
    philosophy="The rebellion was lost; seek redemption through good works and restoration; some believe God's mercy extends to penitent fallen",
    goal="Restore Earth to paradise it was before Age of Wrath; seek God's forgiveness",
    leadership="Devil Nuriel (warrior seeking peace; chief planner); Scourge Ouestucati (the real soul; Archangel of Ocean Wind; leads by example)",
    tactics="Explore human condition and world state; Investigate supernatural aspects remaining; Determine if any loyal angels abandoned world; Travel extensively for balanced worldview; Work toward balance and peace",
)[0]

# 4. Cryptics - Seekers of Hidden Truths
cryptics = DemonFaction.objects.get_or_create(
    name="Cryptics",
    philosophy="Questions must be asked; mysteries must be solved; truth will set them free",
    goal="Unearth truth behind Lucifer's disappearance and unanswered questions about the Fall",
    leadership="Gipontel (Fundamental and onetime Archangel; coalition-builder; more accessible faction)",
    tactics="Gather information from all sources; Build networks of knowledge: Scelestinomicon (Book of Rebels) and Crucianomicon (Book of Tormented); Make truces with other factions to observe/learn; Ally with others to foster inquisitive attitudes",
)[0]

# 5. Raveners - Destroyers and Nihilists
raveners = DemonFaction.objects.get_or_create(
    name="Raveners",
    philosophy="Rebellion was lost decisively; redemption is impossible; destruction is the only honest choice",
    goal="Destruction of the universe and everything in it",
    leadership="Sauriel the Releaser (Slayer; one of Lucifer's Archdukes; leads through threat/intimidation)",
    tactics="Live hard and die harder; No hope for victory means no planning beyond immediate; Break hearts and minds; undermine values; Kill and corrupt indiscriminately; Sic faithful humans on Faustian operatives",
)[0]

from characters.models.changeling.kith import Kith

Kith.objects.get_or_create(
    name="Boggan",
    affinity="actor",
    birthrights=["Craftwork", "Social Dynamics"],
    frailty="Call of the Needy",
    description="Boggans are the craftspeople and caretakers of Kithain society. Homely and often overlooked, they possess an unparalleled talent for creating beautiful works and maintaining order. Boggans are natural homemakers who take pride in their work, whether it's baking the perfect loaf of bread, crafting an exquisite piece of furniture, or organizing a chaotic household. They can be found in all walks of life but are often drawn to service industries, skilled trades, and domestic work. Despite their humble demeanor, Boggans are master manipulators of social situations. They know everyone's business (often because people forget they're even in the room) and can leverage this information with subtle precision. Their birthrights allow them to craft items of superior quality with supernatural speed (Craftwork) and make themselves all but invisible in social gatherings, blending into the background until needed (Social Dynamics). However, Boggans suffer from the Call of the Needy - they are compelled to help those who genuinely need assistance, often placing others' needs before their own. This can be exploited by those who know the Boggan's nature, though betraying such trust is considered despicable among the Kithain.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 88)
Kith.objects.get_or_create(
    name="Clurichaun",
    affinity="actor",
    birthrights=["Twinkling of an Eye", "Fighting Words"],
    frailty="Hoard",
    description="The Clurichaun are the wild cousins of the Boggans, preferring revelry and mischief to honest labor. These diminutive fae are found wherever there's drink, laughter, and the potential for mayhem. Clurichaun love three things above all: fine spirits, clever pranks, and a good brawl. They're natural troublemakers who can turn any gathering into a memorable (if chaotic) event. Don't let their small stature and jovial nature fool you - Clurichaun are fierce when roused. Their birthrights include Twinkling of an Eye (allowing them to appear and disappear with startling speed) and Fighting Words (their insults and taunts carry supernatural sting). They're equally comfortable in seedy taverns or elegant wine cellars, though they tend to leave both establishments somewhat worse for wear. The Clurichaun's frailty is their Hoard - each Clurichaun obsessively collects and guards something, whether it's rare whiskeys, gold coins, or something more esoteric. They become extremely agitated if separated from their hoard and may resort to extreme measures to protect or recover it.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 90)
Kith.objects.get_or_create(
    name="Eshu",
    affinity="scene",
    birthrights=["Serendipity", "Talecraft"],
    frailty="Recklessness",
    description="The Eshu are wanderers, storytellers, and seekers of fortune. Originating from Africa, these traveling fae can be found on every continent, following roads both physical and metaphorical. Eshu are driven by an insatiable wanderlust and an irresistible urge to see what lies beyond the next horizon. They serve as messengers, traders, and lorekeepers for the Kithain, carrying news and tales from one freehold to another. Eshu possess an uncanny ability to be in the right place at the right time. Their birthright of Serendipity ensures that fortunate coincidences follow them wherever they go - they find exactly what they need just when they need it, encounter the right person at the right moment, or stumble upon hidden opportunities. Combined with their Talecraft ability (which makes their stories captivating and memorable), Eshu are natural adventurers and diplomats. However, the Eshu's blessing is also their curse. Recklessness drives them to take unnecessary risks, leap before they look, and rush into danger. They struggle to stay in one place for long, and their impulsive nature can land them (and their companions) in serious trouble.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 92)
Kith.objects.get_or_create(
    name="Nocker",
    affinity="prop",
    birthrights=["Make it Work", "Fix-It"],
    frailty="Perfect is the Enemy of Done",
    description="Nockers are the surly, brilliant craftspeople and inventors of the Kithain. These cantankerous fae have a natural affinity for understanding how things work - and how to make them work better. Nockers are found in workshops, laboratories, and anywhere complex mechanisms need to be created or repaired. They're equally at home with traditional blacksmithing and cutting-edge technology, seeing no contradiction between forge and computer. A Nocker's birthrights reflect their mechanical genius. Make it Work allows them to temporarily repair or jury-rig anything, making broken items function just long enough to get the job done. Fix-It grants them supernatural insight into the workings of devices, letting them diagnose problems instantly and craft superior tools and machines. Nocker-made items are renowned for their quality, though often come with grumpy instructions and passive-aggressive design choices. The curse of the Nocker is that Perfect is the Enemy of Done - no matter how well they craft something, they can always see its flaws. Nockers are never truly satisfied with their work, leading to chronic grouchiness and a tendency to verbally tear apart both their own creations and those of others. This makes them brilliant craftspeople but difficult companions.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 94)
Kith.objects.get_or_create(
    name="Piskey",
    affinity="actor",
    birthrights=["Nimble", "Blending In"],
    frailty="Light-Fingers",
    description="Piskeys are the small, mischievous fae of Cornwall and surrounding regions. Tiny even by changeling standards, Piskeys stand no taller than a foot high in their fae seeming. What they lack in size, they make up for in cunning, agility, and sticky fingers. Piskeys are natural thieves, pranksters, and scouts, able to slip into places larger beings cannot reach. Their birthrights make them exceptional infiltrators and rogues. Nimble grants them supernatural agility and dexterity, allowing acrobatic feats that would be impossible for their size. Blending In lets them become nearly invisible in crowds or cluttered environments, as people's eyes simply slide past them. Combined with their small size, Piskeys make excellent spies and burglars. However, Piskeys suffer from Light-Fingers - they are compelled to steal things that catch their eye, even when doing so is dangerous or counterproductive. This kleptomaniacal urge has gotten many Piskeys (and their motleys) into serious trouble. Items stolen this way often have little practical value but possess some quality that appeals to the Piskey's strange aesthetic sense.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 96)
Kith.objects.get_or_create(
    name="Pooka",
    affinity="nature",
    birthrights=["Shapechanging", "Confidante"],
    frailty="Untruths",
    description="Pookas are shapechangers and inveterate liars who embody the playful trickster spirit of the Dreaming. Each Pooka has an affinity with a particular animal, which influences their personality and appearance even in their mortal seeming. A Pooka might be cat-like, crow-ish, rabbit-natured, or bear-hearted, and this nature shines through in subtle ways. Their most notable birthright is Shapechanging - the ability to assume the form of their affinity animal at will. In this form, they retain their intelligence but gain the animal's natural abilities. A cat Pooka can climb walls and see in the dark, while a horse Pooka can run with supernatural speed. Their Confidante birthright makes them excellent listeners and trustworthy companions; beings instinctively want to confide in Pookas. The dark side of the Pooka nature is their connection to Untruths - they literally cannot speak only the complete truth. Every statement they make must contain some element of falsehood, exaggeration, or misdirection. This can range from minor embellishments to outright lies, and skilled Pookas learn to tell truth through their lies, but they can never simply speak plainly. This makes them both charming and frustrating companions.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 98)
Kith.objects.get_or_create(
    name="Redcap",
    affinity="nature",
    birthrights=["Dark Appetite", "Bully Browbeat"],
    frailty="Bad Attitude",
    description="Redcaps are the monsters of Kithain society - violent, crude, and terrifying. With their jagged teeth, powerful jaws, and caps stained red with the blood of their victims, Redcaps embody the nightmare aspect of faerie tales. They can eat literally anything - glass, metal, wood, stone, or flesh - and take perverse pleasure in consuming things that would kill normal beings. Their birthrights reflect their monstrous nature. Dark Appetite allows them to eat and digest absolutely anything, gaining sustenance and even healing from their bizarre meals. Bully Browbeat makes them naturally intimidating, capable of cowing others through sheer presence and aggressive posturing. Redcaps make excellent shock troops, enforcers, and anyone who needs something (or someone) disposed of. Redcaps struggle with their Bad Attitude frailty - they have extremely short tempers and difficulty controlling their violent impulses. While not mindlessly destructive, Redcaps tend toward aggression as a first resort rather than a last one. Combined with their frightening appearance, this makes them outcasts even among other changelings. However, loyal Redcaps make fiercely protective companions who will literally consume any threat to their friends.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 100)
Kith.objects.get_or_create(
    name="Satyr",
    affinity="fae",
    birthrights=["Gift of Pan", "Physical Prowess"],
    frailty="Passion's Curse",
    description="Satyrs are the revelers and sensualists of the Kithain, embodying passion in all its forms. These goat-legged fae pursue pleasure, art, and experience with single-minded intensity. Satyrs are found wherever there's music, dancing, fine wine, beautiful companions, or wild celebrations. They are natural artists, musicians, and lovers who believe that life is meant to be lived to its fullest. The Gift of Pan allows satyrs to invoke wild revelry and panic in those around them - they can inspire others to dance, celebrate, or flee in terror with their music and presence. Physical Prowess grants them enhanced strength, stamina, and athleticism, particularly in pursuits related to celebration, performance, or romance. Satyrs are simultaneously sophisticated artists and wild nature spirits. Their curse is Passion's Curse - satyrs find it nearly impossible to resist indulging their desires. They must pursue beauty, pleasure, and artistic expression even when doing so is dangerous or inappropriate. A satyr who encounters their particular passion (which varies by individual - it might be music, wine, attractive people, or forbidden knowledge) finds it nearly impossible to resist, leading them into excess and trouble.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 102)
Kith.objects.get_or_create(
    name="Selkie",
    affinity="nature",
    birthrights=["Seal Form", "Ocean's Grace"],
    frailty="Seal Coat",
    description="Selkies are the seal-folk of Celtic legend, equally at home on land or in the sea. These melancholy fae carry the ocean in their hearts, always hearing the call of waves even when far inland. In their fae form, Selkies possess sealskin cloaks that allow them to transform into seals, but these cloaks are also the source of their greatest vulnerability. Their birthrights make them masters of the aquatic realm. Seal Form allows them to transform into a seal by donning their magical sealskin, granting them all the grace and ability of these marine mammals. Ocean's Grace ensures they are never awkward in or around water - they swim with supernatural skill, can hold their breath for extended periods, and have an intuitive understanding of tides, currents, and marine life. The tragic frailty of the Selkie is their Seal Coat - if separated from their sealskin, they become mortal, losing all their fae powers and eventually succumbing to Banality. Stories tell of Selkies whose seal coats were stolen, forcing them into unwanted marriages or servitude. Many Selkies live in constant fear of losing their coat and guard it obsessively. Even touching a Selkie's coat without permission is considered a grave offense.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 104)
Kith.objects.get_or_create(
    name="Arcadian Sidhe",
    affinity="time",
    birthrights=["Unearthly Beauty", "Noble Bearing"],
    frailty="Curse of Banality",
    description="The Arcadian Sidhe are the High Lords and Ladies of the Kithain, the nobility who returned from Arcadia during the Resurgence in 1969. Tall, beautiful, and impossibly graceful, the Arcadian Sidhe are fairy-tale princes and princesses made flesh. They possess an aura of majesty that commands respect and admiration, and many believe they are the true rulers of the fae by right of blood and bearing. Their birthrights reflect their noble heritage. Unearthly Beauty makes them supernaturally attractive, with an otherworldly grace that mortals find compelling and other Kithain acknowledge as the mark of nobility. Noble Bearing grants them natural authority and leadership ability - people instinctively defer to them and follow their commands. Arcadian Sidhe expect to be obeyed and are rarely disappointed. However, the Arcadian Sidhe's long sojourn in timeless Arcadia has left them vulnerable to the Curse of Banality. They are more susceptible to Banality than other Kithain, finding the mundane world particularly draining and painful. Prolonged exposure to the banal can sicken an Arcadian Sidhe or even force them into premature Undoing. This makes them seem haughty and removed, as they must often retreat to freeholds and places of Glamour to survive.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 106)
Kith.objects.get_or_create(
    name="Autumn Sidhe",
    affinity="fae",
    birthrights=["Unearthly Beauty", "Noble Bearing"],
    frailty="Adoration",
    description="The Autumn Sidhe are the original nobility of the Kithain, who remained on Earth when their Arcadian cousins fled to the fae homeland centuries ago. Also known as Danaan sidhe, they weathered the long winter of Banality and adapted to survival in the mundane world. When the Arcadian Sidhe returned during the Resurgence, they found their Autumn cousins already established and unwilling to simply step aside. Autumn Sidhe possess the same birthrights as their Arcadian cousins - Unearthly Beauty and Noble Bearing grant them supernatural attractiveness and natural authority. However, having lived through centuries on Earth, they tend to be more pragmatic and willing to compromise than their idealistic Arcadian relatives. They understand the common changelings better and are more likely to lead through earned respect rather than assumed divine right. The Autumn Sidhe's frailty is Adoration - they require the love and admiration of others to thrive. Without subjects, followers, or admirers, an Autumn Sidhe begins to fade, losing Glamour and eventually risking Undoing. This drives them to seek positions of leadership and influence, not merely from pride but from spiritual necessity. An Autumn Sidhe without a following is like a plant without sunlight.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 108)
Kith.objects.get_or_create(
    name="Sluagh",
    affinity="prop",
    birthrights=["Squirm", "Sharpened Senses"],
    frailty="Curse of Silence",
    description="The Sluagh are the keepers of secrets, the whisperers in darkness, and the watchers from the shadows. These pale, gaunt fae are uncomfortable in bright light and rarely speak above a whisper. Sluagh collect secrets like others collect coins, trading in information and hidden knowledge. They are found in libraries, archives, beneath old houses, and anywhere secrets might hide. Their birthrights make them ideal information brokers and infiltrators. Squirm allows them to contort their bodies in impossible ways, slipping through gaps far too small for their apparent size. Combined with Sharpened Senses (which grants them exceptional perception, particularly in darkness and for hearing whispers and secrets), Sluagh can go anywhere and learn anything. The Curse of Silence is the Sluagh's defining frailty - they can never speak above a whisper. Some interpret this curse broadly, believing Sluagh cannot reveal secrets they've been told to keep, while others take it literally as an inability to raise their voices. Either way, Sluagh must lean in close to be heard, which paradoxically makes them excellent confidants - people lower their own voices in response, turning every conversation into an exchange of secrets.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 110)
Kith.objects.get_or_create(
    name="Troll",
    affinity="fae",
    birthrights=["Titan's Power", "Strong of Will and Body"],
    frailty="Bond of Duty",
    description="Trolls are the stalwart guardians and oath-keepers of the Kithain. Large, strong, and seemingly primitive, Trolls are actually among the most honorable and trustworthy of all changelings. They serve as bodyguards, knights, and champions, taking their oaths and duties with absolute seriousness. A Troll's word is their bond, and they will fulfill their promises regardless of personal cost. Their birthrights reflect their role as protectors and warriors. Titan's Power grants them exceptional strength and resilience, allowing them to stand against threats that would overwhelm smaller kith. Strong of Will and Body provides enhanced physical and mental resistance, making Trolls difficult to harm, manipulate, or break. They are living fortresses who stand between danger and those they've sworn to protect. The Bond of Duty is both the Troll's greatest strength and their defining frailty. Trolls are compelled to honor their oaths and fulfill their duties, even when doing so costs them dearly. They cannot break a promise without suffering severe spiritual consequences, and clever enemies can bind Trolls with carefully worded oaths. However, this same quality makes Trolls the most trusted companions in all the Dreaming - a Troll's promise is absolutely reliable.",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 112)

# Thallain - Dark/evil counterparts to the noble kiths
Kith.objects.get_or_create(
    name="Boggart",
    affinity="actor",
    birthrights=["Slippery Customer", "Knavery"],
    frailty="Oathbreaker",
    description="Boggarts are the twisted, evil cousins of Boggans. Where Boggans are helpful and industrious, Boggarts are spiteful saboteurs who take pleasure in ruining the work of others. They appear as twisted, malformed creatures with cruel features. Their birthrights make them masters of mischief and destruction. Slippery Customer allows them to escape bonds, grasps, and confinement with supernatural ease. Knavery grants them the ability to intuitively understand how to break, sabotage, or corrupt anything they encounter. Boggarts are compulsive destroyers who cannot resist undoing good work. Their frailty, Oathbreaker, means they are physically incapable of keeping their word - any promise they make will eventually be broken, often in the most harmful way possible.",
)[0]
Kith.objects.get_or_create(
    name="Ogre",
    affinity="nature",
    birthrights=["Brute Strength", "Terrible Appetite"],
    frailty="Hideous",
    description="Ogres are monstrous, brutish Thallain who embody raw violence and cruelty. Far larger and more savage than Trolls, Ogres revel in causing pain and fear. Their birthrights reflect their nature as predators. Brute Strength grants them superhuman power, allowing them to tear apart obstacles and victims alike. Terrible Appetite means they can consume anything, including human flesh, and are driven to feast on the weak and helpless. Unlike Redcaps who eat out of curiosity, Ogres eat out of hunger and malice. Their frailty is Hideous - Ogres are so repulsive that they cannot hide their monstrous nature, causing revulsion and fear in all who see them.",
)[0]
Kith.objects.get_or_create(
    name="Beastie",
    affinity="nature",
    birthrights=["Shapeshifting", "Beast Nature"],
    frailty="Uncontrollable Rage",
    description="Beasties are the dark mirror of Pookas, savage shapeshifters who take the form of predatory animals. Where Pookas are playful tricksters, Beasties are vicious hunters who revel in the kill. Their birthrights allow them to assume animal forms (typically wolves, bears, or other predators) with full predatory instincts, and they gain enhanced senses for tracking prey. Their frailty is Uncontrollable Rage - when wounded or threatened, Beasties fly into a berserk fury and attack anything nearby, unable to distinguish friend from foe.",
)[0]
Kith.objects.get_or_create(
    name="Boogie",
    affinity="prop",
    birthrights=["Hide and Seek", "Terror"],
    frailty="Banished by Bravery",
    description="Boogies are living nightmares, the things that hide under beds and in closets. They are masters of fear, feeding on terror and taking pleasure in tormenting the helpless. Their birthrights make them perfect stalkers. Hide and Seek allows them to become invisible in shadows and tight spaces, emerging only to strike. Terror grants them the ability to instill supernatural fear in their victims, paralyzing them with dread. Boogies are cowards at heart - their frailty, Banished by Bravery, means they must flee from anyone who stands up to them with true courage.",
)[0]
Kith.objects.get_or_create(
    name="Aithu",
    affinity="time",
    birthrights=["Unearthly Beauty", "Cruel Charm"],
    frailty="Addiction to Suffering",
    description="Aithus are the dark nobility, corrupted Sidhe-like beings who embody the cruel and capricious nature of dark faerie tales. They possess terrible beauty that draws victims to them, only to destroy them. Their birthrights include Unearthly Beauty (like Sidhe) and Cruel Charm, which allows them to manipulate and control others through a combination of attraction and fear. Unlike Sidhe who may be noble, Aithus delight in causing suffering. Their frailty is Addiction to Suffering - Aithus must regularly inflict pain, humiliation, or despair on others or they begin to weaken and fade.",
)[0]

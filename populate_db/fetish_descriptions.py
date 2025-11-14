# Fetish Descriptions for Werewolf: The Apocalypse
# This file adds descriptions to fetishes defined in fetishes.py
# Information extracted from Werewolf: The Apocalypse 20th Anniversary Edition

from items.models.werewolf.fetish import Fetish

# Rank 1 Fetishes

apeskin = Fetish.objects.get(name="Apeskin")
apeskin.description = """A leather jacket, vest, or other garment crafted from human-tanned leather and bound with a Homid Ancestor-Spirit. When worn, the Apeskin allows the Garou to appear completely human even when in Crinos form. The fetish doesn't change the werewolf's actual form, but creates a powerful illusion that makes witnesses perceive the wearer as an ordinary human. This is invaluable for Glass Walkers and other werewolves who need to move through human society even during dire emergencies. The spirit within the Apeskin resonates with humanity's essence, cloaking the beast in the guise of man."""
apeskin.save()

harmony_flute = Fetish.objects.get(name="Harmony Flute")
harmony_flute.description = """A delicate wooden flute bound with a spirit of peace, calm, water, or a bird spirit. When played, the Harmony Flute's haunting melody soothes angry souls and calms violent tempers. The music can pacify enraged individuals, including Garou in frenzy, and can even affect supernatural creatures. The flute is particularly favored by Philodox and Children of Gaia, who use it to prevent unnecessary bloodshed and promote peaceful resolution of conflicts. The spirit's calming influence flows through the music, touching the hearts of all who hear it."""
harmony_flute.save()

magpie_swag = Fetish.objects.get(name="Magpie's Swag")
magpie_swag.description = """A leather pouch or small bag bound with a Magpie or Marsupial Spirit. The Magpie's Swag is dimensionally larger on the inside than the outside, able to hold far more than its size would suggest. Items placed within are preserved in stasis and can be retrieved instantly. The fetish is named for the magpie's hoarding instincts and is popular among Ragabash and Glass Walkers who need to carry an assortment of tools, weapons, and supplies. Some versions are decorated with shiny objects and feathers as tribute to the spirit bound within."""
magpie_swag.save()

mirrorshades = Fetish.objects.get(name="Mirrorshades")
mirrorshades.description = """Mirrored sunglasses containing a Glass Elemental spirit. When worn, Mirrorshades protect the wearer's eyes from bright lights and flashes, preventing blindness effects and negating vision-based attacks. They also allow the wearer to gaze into the reflective surfaces of the glasses to scry distant locations or peer into the Umbra. Glass Walkers prize these items as both practical gear and mystical tools, blending their tribal aesthetic with spiritual utility."""
mirrorshades.save()

nyx_bangle = Fetish.objects.get(name="Nyx's Bangle")
nyx_bangle.description = """A bracelet or bangle of dark metal bound with a Night or Darkness spirit. When activated, Nyx's Bangle shrouds the wearer in supernatural shadows, making them difficult to see even in broad daylight. The darkness follows the wearer like a living cloak, providing concealment and adding to Stealth attempts. The fetish is named for Nyx, the Greek primordial goddess of night, and is particularly favored by Silent Striders and Shadow Lords who move through darkness like predators."""
nyx_bangle.save()

truth_earring = Fetish.objects.get(name="Truth Earring")
truth_earring.description = """An earring bound with a Servant of Falcon, the totem of honor and truth. When worn, this fetish allows the wearer to detect lies spoken in their presence. The earring grows warm when falsehoods are uttered, with the intensity of heat corresponding to the magnitude of the deception. Philodox particularly value Truth Earrings during moots and trials, as they help ensure justice is served. However, the spirit of Falcon demands that the wearer themselves speak only truth while wearing the earring, or face the Falcon spirit's displeasure."""
truth_earring.save()

# Rank 2 Fetishes

cup_of_alicorn = Fetish.objects.get(name="Cup of the Alicorn")
cup_of_alicorn.description = """A chalice or cup bound with a healing spirit, snake spirit, or bear spirit. Legends say these cups were once made from actual unicorn horns (alicorns), though modern versions use silver, horn, or carved wood. When water or any liquid is poured into the Cup and blessed with Gnosis, it becomes a powerful healing draught capable of curing diseases, neutralizing poisons, and accelerating wound healing. The Cup is particularly sacred to Children of Gaia and theurges who dedicate themselves to healing. Each cup can only produce one dose of healing liquid per day."""
cup_of_alicorn.save()

chameleon_skin = Fetish.objects.get(name="Chameleon Skin")
chameleon_skin.description = """A cloak, jacket, or body suit bound with a Chameleon Spirit. When activated, the Chameleon Skin changes color and pattern to match the wearer's surroundings, providing exceptional camouflage. The material shifts continuously, adapting to new environments as the wearer moves. Unlike mundane camouflage, the Chameleon Skin works in any environment - urban, forest, desert, or even the bizarre landscapes of the Umbra. The wearer seems to fade into the background, becoming nearly invisible to casual observation."""
chameleon_skin.save()

dagger_of_retribution = Fetish.objects.get(name="Dagger of Retribution")
dagger_of_retribution.description = """A ritual dagger bound with a Vengeance Spirit. This weapon is forged with a specific purpose: to strike down those who have committed grave wrongs. When the wielder declares a specific crime or injustice that their target has committed, the Dagger of Retribution gains supernatural potency against that individual. The blade thirsts for righteous vengeance, dealing enhanced damage to the guilty party. However, if wielded for unjust purposes or personal spite rather than true retribution, the spirit within may turn on its bearer. Philodox and Ahroun often carry these daggers as instruments of justice."""
dagger_of_retribution.save()

dream_stealer = Fetish.objects.get(name="Dream Stealer")
dream_stealer.description = """A small talisman or dreamcatcher bound with a Dream Spirit or one of Cuckoo's Brood. This insidious fetish allows the user to steal into a sleeping victim's dreams, observing their subconscious thoughts and fears. The Dream Stealer can extract information, plant suggestions, or even cause nightmares. While useful for gathering intelligence, its use is considered ethically questionable by many Garou. Ragabash and Shadow Lords are most likely to employ Dream Stealers, though wise packs keep such items secured to prevent abuse. The dream-walking leaves no physical trace, making it nearly impossible to prove."""
dream_stealer.save()

spirit_tracer = Fetish.objects.get(name="Spirit Tracer")
spirit_tracer.description = """A compass, tracking device, or marked stone bound with a Predator Spirit or a spirit possessing the Tracking Charm. The Spirit Tracer allows its user to track a specific target across both the physical world and the Umbra. Once the fetish has been attuned to a target (through contact with something belonging to them, their blood, or their scent), it points unerringly toward that individual regardless of distance or dimensional barriers. The device is invaluable for hunting fugitives, tracking kidnapped packmates, or pursuing enemies through the spirit world."""
spirit_tracer.save()

# Rank 3 Fetishes

baneskin = Fetish.objects.get(name="Baneskin")
baneskin.description = """A grotesque garment crafted from the remains of a slain Bane and bound with a Parrot or Mockingbird Spirit. When worn, the Baneskin disguises the wearer as a Bane or other Wyrm-creature, allowing infiltration of Wyrm-tainted areas without immediate detection. The skin mimics the spiritual corruption of the Wyrm, masking the wearer's true nature. However, wearing a Baneskin is spiritually dangerous - prolonged use can actually taint the wearer with genuine Wyrm corruption. Most Garou will only don a Baneskin for desperate missions into Wyrm strongholds, and cleansing rites are performed immediately upon removal."""
baneskin.save()

beast_mask = Fetish.objects.get(name="Beast Mask")
beast_mask.description = """A carved mask depicting an animal's face, bound with the appropriate animal spirit. When worn and activated, the Beast Mask grants the wearer some of the attributes and abilities of that animal. An eagle mask might grant keen vision and the ability to glide short distances, while a bear mask could provide enhanced strength and resilience. The mask creates a spiritual connection with the animal's essence, temporarily blessing the wearer with the beast's gifts. Glass Walkers favor rat or cockroach masks for urban survival, while Red Talons might use wolf or raven masks to enhance their already formidable predatory abilities."""
beast_mask.save()

dsiah = Fetish.objects.get(name="D'siah")
dsiah.description = """An African throwing blade bound with a War Spirit, usually one of Cobra's Brood. The D'siah (pronounced "dee-SEE-ah") is a traditional weapon of the Silent Striders, resembling a sickle-shaped blade designed to be thrown in a spinning arc. When activated, the D'siah returns to the wielder's hand after being thrown, similar to a boomerang. The war spirit within guides the blade's flight, allowing it to strike with supernatural accuracy and return even if it misses or hits its target. Warriors can throw the D'siah repeatedly without fear of losing their weapon, making it deadly in sustained combat."""
dsiah.save()

fang_dagger = Fetish.objects.get(name="Fang Dagger")
fang_dagger.description = """A dagger crafted from a werewolf's fang or claw, bound with a Snake Spirit or spirit of War, Pain, or Death. The Fang Dagger is one of the few weapons that can harm creatures normally immune to conventional attacks. It deals aggravated damage like the natural weapons of Garou, and its wounds are particularly difficult to heal. The blade carries spiritual venom from the snake spirit, causing excruciating pain to those it cuts. These daggers are often created as memorial weapons from the fangs of fallen pack members, carrying a piece of the deceased warrior's rage into battle."""
fang_dagger.save()

partridge_wing = Fetish.objects.get(name="Partridge Wing")
partridge_wing.description = """A feathered fan or wing-shaped talisman bound with a Spirit of Water or Forgetfulness. When waved, the Partridge Wing creates a supernatural mist or fog that obscures vision and confuses pursuers. More insidiously, those caught in the mist find their recent memories becoming hazy and uncertain - they forget the faces of those they pursued, lose track of their purpose, or become disoriented. The fetish is named after the partridge's tendency to fake injury to lead predators away from its nest. Silent Striders and Ragabash use Partridge Wings to escape pursuit or cover their pack's retreat."""
partridge_wing.save()

phoebe_veil = Fetish.objects.get(name="Phoebe's Veil")
phoebe_veil.description = """A shimmering veil or cloak bound with a Lune (moon spirit), Chameleon Spirit, or spirit of Illusion or Shadow. Named after Phoebe, the Greek titan of the moon, this fetish creates powerful illusions around the wearer. Unlike mere camouflage, Phoebe's Veil can make the wearer appear as someone else entirely - a different person, an animal, or even seem to disappear completely. The illusion affects all senses, making the disguise nearly perfect. However, it requires concentration to maintain, and spiritual perception or keen supernatural senses may pierce the veil."""
phoebe_veil.save()

sanctuary_chimes = Fetish.objects.get(name="Sanctuary Chimes")
sanctuary_chimes.description = """A set of wind chimes bound with a Spirit of Protection or Turtle Spirit. When hung at the entrance to a caern, sept, or dwelling, the Sanctuary Chimes create a protective ward. The chimes ring when danger approaches, alerting those within to threats. More powerfully, the chimes generate a spiritual barrier that hampers hostile spirits and makes it more difficult for enemies to find or approach the protected area. The gentle tinkling sound is soothing to allies but discordant and unsettling to those who mean harm. Many septs hang Sanctuary Chimes at the borders of their territories."""
sanctuary_chimes.save()

sun_whip = Fetish.objects.get(name="Sun Whip")
sun_whip.description = """A braided whip bound with a Spirit of Flame or Sunlight. When cracked, the Sun Whip ignites with solar fire, becoming a lash of pure sunlight. The flaming whip deals both physical and fire damage, and its solar nature makes it particularly effective against vampires and other creatures vulnerable to sunlight. Even beings normally immune to fire find themselves burned by the whip's holy flames. The weapon sheds bright light in a wide radius, banishing shadows and revealing hidden enemies. Red Talons and Fianna warriors sometimes wield Sun Whips, seeing them as Gaia's wrath made manifest."""
sun_whip.save()

wind_whistle = Fetish.objects.get(name="Wind Whistle")
wind_whistle.description = """A whistle carved from bone or wood, bound with a Wind Elemental. When blown, the Wind Whistle summons powerful winds at the user's command. The winds can range from a gentle breeze to a howling gale, depending on how hard the whistle is blown. Users can direct the winds to scatter gas or fog, push aside light objects, fill sails, or knock opponents off balance. Some Garou use Wind Whistles to clear away the Wyrm's toxic miasmas or to carry messages on the wind to distant allies."""
wind_whistle.save()

# Rank 4 Fetishes

feathered_cloak = Fetish.objects.get(name="Feathered Cloak")
feathered_cloak.description = """A magnificent cloak woven from hundreds of feathers and bound with a powerful Bird Spirit. When worn and activated, the Feathered Cloak grants the wearer the gift of flight. The user can soar through the air with the grace of a bird, whether in the physical world or the Umbra. The cloak doesn't change the wearer's form but allows them to defy gravity and ride the winds. Flight speed depends on the wearer's physical prowess, but most can match the speed of large birds. The cloak is particularly prized by Silver Fangs and other Garou who value dramatic displays of power."""
feathered_cloak.save()

ironhammer = Fetish.objects.get(name="Ironhammer")
ironhammer.description = """A massive war hammer bound with a War Spirit. Despite its name, the Ironhammer is often forged from silver to make it lethal against werewolves and other supernatural creatures. The hammer strikes with devastating force, channeling the war spirit's fury into each blow. When wielded in battle, the Ironhammer can shatter bones, crush armor, and shatter barriers. Some versions can also be hurled like a thrown weapon, returning to the wielder's hand like the mythical hammer of Thor. Get of Fenris particularly prize these weapons, seeing them as worthy tools for honorable warriors."""
ironhammer.save()

klaive = Fetish.objects.get(name="Klaive")
klaive.description = """The most iconic weapon of the Garou Nation, a Klaive is a silver blade bound with a War Spirit. These weapons are crafted by master theurges in sacred rituals, binding powerful spirits into weapons of exquisite craftsmanship. Klaives deal aggravated damage and never break or dull. Each Klaive is unique, often decorated with tribal symbols and imbued with the personality of its bound spirit. Some Klaives can burst into flame, discharge lightning, or possess other powers depending on the spirit within. Owning a Klaive is a mark of status and honor - they are awarded for great deeds, inherited from mentors, or won in combat. The most famous Klaives have names and histories spanning centuries."""
klaive.save()

labrys = Fetish.objects.get(name="Labrys of Isthmene")
labrys.description = """A double-headed axe in the ancient Greek style, bound with a War Spirit. The Labrys of Isthmene is named after an legendary Amazon warrior and is particularly sacred to the Black Furies. The weapon is both a tool of war and a symbol of Gaia's fierce protection. When wielded, the Labrys cleaves through armor and flesh with equal ease, dealing terrible wounds to those who would harm Gaia or her children. The double-bladed design allows for spinning attacks and can strike multiple opponents. Some Labrys glow with silver moonlight when raised in righteous fury."""
labrys.save()

monkey_puzzle = Fetish.objects.get(name="Monkey Puzzle")
monkey_puzzle.description = """A complex mechanical puzzle box or intricate device bound with a Ghost, Spirit of Illusion, or Trickster Spirit. The Monkey Puzzle is the ultimate tool of confusion and misdirection. When activated, it creates a zone of bewilderment around the user, causing enemies to become confused, disoriented, and suggestible. Foes may attack allies by mistake, flee in random directions, or simply stand befuddled. The puzzle constantly shifts and changes, its solution forever elusive, much like the confusion it inflicts. Ragabash treasure these items, using them to turn enemy forces against each other or escape impossible situations through sheer chaos."""
monkey_puzzle.save()

spirit_whistle = Fetish.objects.get(name="Spirit Whistle")
spirit_whistle.description = """A bone whistle bound with a Screech-Owl Spirit or spirit of Madness or Discord. When blown, the Spirit Whistle produces an ultrasonic shriek audible in both the physical world and Umbra. The sound is agonizing to spirits, forcing them to flee or become disoriented. More terrifyingly, the whistle can drive spirits into frenzy or temporarily sever their connection to the physical world. This makes it an invaluable tool for combating possessed creatures or banishing hostile spirits. However, the whistle affects ALL spirits in range, including helpful totems and spirit allies, so it must be used with great care."""
spirit_whistle.save()

puda = Fetish.objects.get(name="Personal Umbral Digital Application")
puda.description = """A high-tech smartphone or tablet bound with a Bee Spirit, representing the Weaver's connection to communication and information. The PUDA (pronounced "POO-dah") allows its user to access information from across the Umbra, communicate with packmates across vast distances, and even hack into Weaver-dominated digital systems from the spirit world. The device can translate between spirit speech and human languages, record observations in the Umbra, and maintain connection to both the Digital Web and the physical internet. Glass Walkers created these devices to bridge the gap between their tribal affinity for technology and the spiritual nature of Garou existence."""
puda.save()

unbroken_cord = Fetish.objects.get(name="Unbroken Cord")
unbroken_cord.description = """A braided cord or rope bound with a Unity Spirit. The Unbroken Cord creates an unbreakable spiritual link between pack members. When each member of a pack ties the cord around their wrist or holds a piece of it, they can sense each other's locations, emotional states, and even share thoughts. The cord allows perfect coordination in battle and ensures that pack members can always find each other, even across the Gauntlet. More importantly, the Unity Spirit within strengthens pack bonds, making the pack more resistant to mental attacks that would turn them against each other. Some packs perform binding rituals with the Unbroken Cord, making it a symbol of their eternal loyalty to each other."""
unbroken_cord.save()

# Rank 5 Fetishes

grand_klaive = Fetish.objects.get(name="Grand Klaive")
grand_klaive.description = """A masterwork silver blade bound with an exceptionally powerful War Spirit. Grand Klaives are among the most potent weapons in the Garou Nation, typically wielded only by tribal leaders, legendary heroes, and the most honored warriors. These blades are larger and more ornate than standard Klaives, often appearing as great swords, nodachi, or other impressive weapons. Grand Klaives deal devastating aggravated damage and often possess unique powers granted by their mighty spirits - they might emit waves of fear, cut through mystical barriers, or channel elemental fury. Each Grand Klaive is a legendary artifact with a storied history, and their creation requires months of ritual and sacrifice. To carry a Grand Klaive is to carry the weight of the Garou Nation's martial tradition."""
grand_klaive.save()

jarlhammer = Fetish.objects.get(name="Jarlhammer")
jarlhammer.description = """A massive silver war hammer bound with both a War Spirit and a Silver Spirit. The Jarlhammer is a weapon of kingship and command, traditionally wielded by jarls (leaders) of the Get of Fenris. The hammer is both a devastating weapon and a symbol of authority. In battle, it crushes enemies with overwhelming force, dealing aggravated damage even to creatures resistant to silver. When struck against the ground, the Jarlhammer can create shockwaves that knock down all nearby enemies, or produce a resonating tone that rallies allies and strikes fear into foes. The weapon is so heavy that only the strongest warriors can wield it effectively, but in the hands of a true leader, the Jarlhammer becomes an instrument of victory."""
jarlhammer.save()

runestones = Fetish.objects.get(name="Runestones")
runestones.description = """A set of carved stones or bones inscribed with ancient runes, bound with a Spirit of Time, Dream, Enigmas, or Wisdom. Runestones are tools of divination and prophecy, allowing the user to glimpse potential futures and divine hidden truths. When cast in a sacred manner, the stones reveal patterns and meanings that guide the user toward wise decisions. The runes can answer specific questions about future events, reveal hidden enemies or allies, or provide cryptic warnings about dangers to come. However, the future is never certain, and the stones show only possibilities, not certainties. Galliards and theurges often consult Runestones before major decisions, and some packs carry them as spiritual compasses. The most ancient sets are said to have been carved by the first Garou and contain wisdom from the time of the Impergium."""
runestones.save()

# Rank 0 (Consumable/Minor) Fetishes

bane_arrows = Fetish.objects.get(name="Bane Arrows")
bane_arrows.description = """Silver-tipped arrows bound with spirits of War, Air, or Pain. Bane Arrows are single-use fetishes designed to slay supernatural creatures from a distance. Each arrow deals aggravated damage and flies with supernatural accuracy, guided by the spirit bound within. The arrows are particularly effective against vampires, hostile spirits, and other creatures vulnerable to silver. Once fired and having struck their target, the arrow's spirit is released and the fetish is expended. Bane Arrows are typically crafted in batches and distributed to pack members before dangerous missions. Some versions explode on impact or trail fire through the air."""
bane_arrows.save()

chiropteran_spies = Fetish.objects.get(name="Chiropteran Spies")
chiropteran_spies.description = """Small mechanical bats bound with Bat Spirits. When released, these Chiropteran Spies (mechanical bat drones) fly to designated locations and observe, recording everything they see and hear. The bat spirits grant the devices supernatural stealth and the ability to navigate in complete darkness using echolocation. After completing their reconnaissance, the spies return to their owner and replay the recorded information. Glass Walkers developed these devices as a marriage of technology and spiritual insight. Each spy can operate for several hours before its spirit must rest, and the devices are small enough to infiltrate through air vents or windows."""
chiropteran_spies.save()

death_dust = Fetish.objects.get(name="Death Dust")
death_dust.description = """A pouch of ash or powder bound with a Spirit of Death, Communication, or Divination. When sprinkled over a corpse or a place where someone died, Death Dust allows the user to witness the final moments of the deceased. The ash swirls and forms ghostly images that replay the circumstances of death, revealing how the person died and potentially identifying their killer. The dust can also reveal the presence of ghosts or wraiths, making invisible spirits briefly visible. Silent Striders, with their affinity for death and the underworld, most commonly use Death Dust in their investigations of mysterious deaths."""
death_dust.save()

gaia_breath = Fetish.objects.get(name="Gaia's Breath")
gaia_breath.description = """A small vial or sachet of sacred herbs bound with a Healing Spirit. When inhaled or consumed, Gaia's Breath provides immediate relief from poisons, diseases, and toxins. The healing essence flows through the user's body, purging impurities and restoring health. The fetish is particularly effective against Wyrm-spawned toxins and spiritual corruption. Each vial contains only a single dose, making Gaia's Breath a precious emergency remedy. Theurges often create batches of Gaia's Breath before the pack ventures into Wyrm-tainted areas where poisonous gases and infectious diseases are common."""
gaia_breath.save()

moon_glow = Fetish.objects.get(name="Moon Glow")
moon_glow.description = """A crystal or glass orb bound with a powerful Lune (moon spirit). When activated, Moon Glow creates brilliant light equal to the full moon's radiance. This supernatural moonlight provides all the benefits of Luna's glow - allowing Garou to regenerate normally, revealing beings hidden by darkness, and banishing shadows. The light is holy to werewolves, filling them with Luna's blessing while causing discomfort to creatures of the Wyrm. Moon Glow is invaluable when fighting in windowless buildings, underground tunnels, or the depths of the Umbra where Luna's light cannot normally reach. Each activation lasts for one scene before the Lune must rest."""
moon_glow.save()

moon_sign = Fetish.objects.get(name="Moon Sign")
moon_sign.description = """A temporary mark or sigil bound with a Lune, Wyld Spirit, or Wolf Spirit. Moon Signs are mystical gang signs or territorial markers that only other Garou can see. When drawn or placed, the sign is invisible to normal sight but glows with spiritual significance to werewolves and spirit-sensitive beings. Moon Signs can convey messages ('Safe place,' 'Danger here,' 'Enemies passed this way'), mark territory boundaries, or serve as waypoints for packs. The signs fade after a few days or can be deliberately erased. Some Bone Gnawers and Glass Walkers use Moon Signs to create invisible networks of information throughout urban territories."""
moon_sign.save()

nightshade = Fetish.objects.get(name="Nightshade")
nightshade.description = """A small container of poisonous plant matter bound with a Spirit of Night or Darkness. Despite the name, this is not merely the toxic plant but a mystical poison that affects both physical and spiritual beings. When administered (usually coating a weapon or added to food/drink), Nightshade causes wracking pain, hallucinations, and eventual death if not treated. Unlike normal poisons, Nightshade can harm spirits and supernatural creatures that would normally be immune to toxins. The darkness spirit within makes the poison particularly insidious, as it also blinds its victims, wrapping them in supernatural shadow as they die. Most Garou consider using Nightshade dishonorable except against the most heinous enemies."""
nightshade.save()

wind_snorkel = Fetish.objects.get(name="Wind Snorkel")
wind_snorkel.description = """A breathing apparatus bound with an Air Elemental. The Wind Snorkel allows the wearer to breathe normally even in environments with no air - underwater, in toxic gas, in smoke-filled buildings, or even in the vacuum of space or certain hostile Umbral realms. The air elemental continuously provides fresh, clean air to the wearer, filtering out contaminants and creating breathable atmosphere. This simple but invaluable fetish has saved countless Garou lives during battles in chemical plants, underwater combat, and journeys through inhospitable spirit realms."""
wind_snorkel.save()

wyrm_scale = Fetish.objects.get(name="Wym Scale")
wyrm_scale.description = """A scale, tooth, or fragment taken from a Wyrm creature and bound with a captured Wyrm Spirit. Wyrm Scales are dangerous and controversial fetishes that allow the bearer to resist Wyrm corruption and even disguise themselves as tainted creatures. The scale provides protection against the Wyrm's spiritual influence, making it harder for Banes to possess the bearer or for Wyrm-taint to spread. Paradoxically, it can also make the bearer appear tainted to spiritual senses, allowing infiltration of Wyrm strongholds. However, carrying a Wyrm Scale is spiritually perilous - the bound Wyrm spirit constantly whispers corrupting thoughts and seeks to twist the bearer toward the Wyrm's service. Most Garou will only touch a Wyrm Scale when absolutely necessary for critical missions."""
wyrm_scale.save()

# Additional Fetishes from page 384

horn_of_distress = Fetish.objects.get(name="Horn of Distress")
horn_of_distress.description = """A curved horn bound with a Peacock or Air Spirit. When blown, the Horn of Distress releases a piercing, supernatural cry that can be heard for miles in all directions, including across the Gauntlet into the Near Umbra. The sound conveys urgent need and summons nearby allies to the aid of the horn's blower. The spirit ensures that the horn's call can penetrate through walls, over the din of battle, and past magical silence. Packs often carry Horns of Distress as emergency beacons, knowing that their sept-mates will come running when they hear the call. However, false alarms are considered serious breaches of trust and honor."""
horn_of_distress.save()

amulet_of_kinship = Fetish.objects.get(name="Amulet of Kinship")
amulet_of_kinship.description = """A carved amulet bound with an Ancestor Spirit. The Amulet of Kinship helps the wearer connect with their tribal heritage and ancestral wisdom. When activated, the amulet allows the wearer to draw upon the knowledge and skills of their ancestors, gaining temporary insight into forgotten lore or ancient techniques. The amulet also makes it easier to commune with ancestor spirits and can reveal one's spiritual lineage. Some versions allow the wearer to briefly channel an ancestor's personality, speaking with their voice and accessing their memories. The amulet is sacred to those who honor their ancestors, particularly among the Silver Fangs and Wendigo."""
amulet_of_kinship.save()

klaive_hammer = Fetish.objects.get(name="Klaive Hammer")
klaive_hammer.description = """A smith's hammer bound with spirits of Balance, Light, or Fire. The Klaive Hammer is not a weapon but a tool for crafting other fetishes, particularly Klaives. When used by a skilled theurge in the creation of a fetish, the Klaive Hammer makes the process easier and more likely to succeed. The hammer can shape silver without heat, bind spirits more firmly into their physical vessels, and ensure perfect balance in the finished weapon. The fire spirit within can also heat metal without the need for a forge, while the light spirit reveals flaws in materials or binding rituals. Master crafters guard their Klaive Hammers jealously, as these tools represent generations of accumulated knowledge."""
klaive_hammer.save()

test_vial = Fetish.objects.get(name="Test Vial")
test_vial.description = """A small glass vial bound with an Ancestor, Divination, or Crow Spirit. The Test Vial is a diagnostic tool that can identify supernatural creatures by their blood or other bodily fluids. A drop of blood placed in the vial causes it to glow different colors depending on what kind of creature the sample came from: red for vampires, green for fae, blue for mages, silver for Garou, black for Wyrm-tainted beings, and so on. The vial can also detect diseases, poisons, and other contaminants. Glass Walkers and Children of Gaia use Test Vials to screen humans who wish to approach Kinfolk, ensuring they aren't possessed or tainted. Each vial can perform one test before needing to rest."""
test_vial.save()

hero_mead = Fetish.objects.get(name="Hero's Mead")
hero_mead.description = """A flask of honey mead bound with a Thunder Spirit. This potent beverage fills the drinker with the fury of a storm and the courage of legends. When consumed before battle, Hero's Mead grants enhanced strength, fearlessness, and fighting prowess. The drinker feels thunder in their veins and lightning in their blood, becoming nearly unstoppable in combat. However, the effects are temporary and leave the warrior exhausted when they fade. The Get of Fenris particularly prize Hero's Mead, consuming it before the most desperate battles. Each flask contains a single dose, and creating more requires capturing a thunder spirit during a raging storm."""
hero_mead.save()

long_whispers = Fetish.objects.get(name="Long Whispers")
long_whispers.description = """A pair of carved stones or shells bound with a Dove or Pigeon Spirit. Long Whispers allow two individuals to communicate across vast distances. Each person holds one stone and can whisper messages that the other hears instantly, regardless of the physical distance between them. The communication is two-way and can cross the Gauntlet, allowing conversation between someone in the physical world and another in the Umbra. The dove/pigeon spirit carries the messages faithfully and swiftly. Packs often split pairs of Long Whispers when members must separate for reconnaissance or separate missions, ensuring they can coordinate and call for help if needed."""
long_whispers.save()

dire_call = Fetish.objects.get(name="Dire Call")
dire_call.description = """A powerful horn or drum bound with a mighty Lune. The Dire Call is an emergency beacon of last resort, used only in the most desperate situations. When activated, it sends a supernatural summons to all Garou within a vast radius (potentially hundreds of miles), compelling them to come to the aid of the caller. The call conveys the urgency and nature of the threat, and Garou who hear it feel Luna's command to respond. However, using a Dire Call frivolously or for unworthy causes risks Luna's wrath and the scorn of all tribes. The Dire Call requires enormous spiritual energy to activate and can only be used once per lunar cycle."""
dire_call.save()

print("All fetish descriptions have been added successfully!")

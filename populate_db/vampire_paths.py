from characters.models.vampire.path import Path

# Major Paths of Enlightenment (alternatives to Humanity)

# SABBAT PATHS

path_of_caine = Path.objects.get_or_create(
    name="Path of Caine",
    requires_conviction=True,
    requires_instinct=True,
    ethics="Follow Caine's example as the first vampire. Reject mortal morality entirely. "
    "Embrace vampiric nature fully. The Sabbat are Caine's chosen. Prepare for Gehenna. "
    "Mortal life has no value except as sustenance. Build strength to fight the Antediluvians. "
    "Study the Book of Nod as scripture.",
    description="The iconic Sabbat Path. Followers seek to emulate Caine and prepare for the Final Nights. "
    "Highly theological, based on interpretation of the Book of Nod. Rejects all human morality.",
)[0]

path_of_death_and_the_soul = Path.objects.get_or_create(
    name="Path of Death and the Soul",
    requires_conviction=True,
    requires_instinct=False,
    ethics="All existence is suffering. Undeath is the highest state. The soul is immortal energy. "
    "Preserve vampires, destroy mortals to free their souls. Study death in all forms. "
    "The Embrace is salvation from mortal suffering. Hasten mortals to death to release them. "
    "Torpor and Final Death are mysteries to study.",
    description="Nihilistic Path viewing undeath as superior to life. Practitioners study death and "
    "destroy mortals to 'free' their souls. Often appear cold and calculating. Also called the Path of Bones.",
)[0]

path_of_honorable_accord = Path.objects.get_or_create(
    name="Path of Honorable Accord",
    requires_conviction=True,
    requires_instinct=False,
    ethics="Keep your word absolutely. Loyalty to pack and sect above all. Personal honor defines you. "
    "Debts must be repaid. Oathbreaking is the ultimate sin. Courage in battle is sacred. "
    "Respect strength and despise weakness. Die before breaking sworn oath.",
    description="Code of honor and loyalty. Popular among Sabbat warriors. Based on keeping oaths and "
    "personal honor. Followers will die before breaking their word. Emphasizes strength and courage.",
)[0]

path_of_power_and_the_inner_voice = Path.objects.get_or_create(
    name="Path of Power and the Inner Voice",
    requires_conviction=True,
    requires_instinct=True,
    ethics="Power is the only truth. The Beast is strength, not weakness. Listen to instinct over reason. "
    "Dominate or be dominated. Build personal power constantly. Weakness deserves destruction. "
    "The strong rule by right. Trust your Beast's wisdom.",
    description="Social Darwinist philosophy embracing the Beast. Power and strength are the only virtues. "
    "Practitioners ride the edge of frenzy, seeing the Beast as ally rather than curse. Popular among Lasombra.",
)[0]

path_of_cathari = Path.objects.get_or_create(
    name="Path of Cathari",
    requires_conviction=True,
    requires_instinct=True,
    ethics="Pleasure and sensation are paths to transcendence. Explore all experiences. "
    "Break taboos to free yourself. Indulgence leads to enlightenment. Test your limits constantly. "
    "Mortal restrictions are chains. Freedom through excess. Shame is weakness.",
    description="Hedonistic Path seeking transcendence through extreme sensation and experience. "
    "Break all taboos. Followers pursue pleasure and pain equally. Previously called Path of Pleasure. "
    "Associated with Toreador antitribu.",
)[0]

path_of_night = Path.objects.get_or_create(
    name="Path of Night",
    requires_conviction=True,
    requires_instinct=True,
    ethics="Vampires are predators. Mortals are prey. Hunt skillfully and without mercy. "
    "The strong survive. Study your prey. Perfect the hunt. Feel no guilt for feeding. "
    "Stealth and cunning define success. Leave no witnesses.",
    description="Predator's code. Vampires are apex hunters; mortals exist as prey. Emphasizes skill "
    "in hunting and feeding. Practitioners take pride in the hunt. No guilt over killing. "
    "Popular among independently minded Sabbat.",
)[0]

path_of_metamorphosis = Path.objects.get_or_create(
    name="Path of Metamorphosis",
    requires_conviction=True,
    requires_instinct=True,
    ethics="The body is clay to be shaped. Transcend flesh through transformation. "
    "Change is the only constant. Stagnation is death. Experiment with fleshcrafting. "
    "Evolution through modification. The perfect form doesn't exist. Keep changing forever.",
    description="Tzimisce Path focused on endless transformation through Vicissitude. "
    "Practitioners constantly modify themselves and others. Change is sacred; stasis is failure. "
    "The body is art to be sculpted.",
)[0]

path_of_lilith = Path.objects.get_or_create(
    name="Path of Lilith",
    requires_conviction=True,
    requires_instinct=True,
    ethics="Lilith, not Caine, is the true progenitor. Feminine divine power. Reject Caine's authority. "
    "Sexuality as power and weapon. Independence from male authority. Protect women. "
    "Bahari traditions are truth. Temptation is strength.",
    description="Feminist theology claiming Lilith as the true first vampire. Practiced by Bahari cult. "
    "Emphasizes feminine power and independence. Uses sexuality as spiritual power. "
    "Rejects traditional Cainite hierarchy.",
)[0]

# INDEPENDENT AND CAMARILLA PATHS

path_of_blood = Path.objects.get_or_create(
    name="Path of Blood",
    requires_conviction=True,
    requires_instinct=False,
    ethics="Blood is sacred. The Amaranth brings enlightenment. Diablerie is sacrament. "
    "Lower your Generation through Amaranth. Study vitae in all forms. Blood magic reveals truth. "
    "Generation determines worth. Pursue the blood of elders.",
    description="Assamite Path focused on blood and diablerie. Practitioners seek to lower their Generation "
    "through Amaranth. Blood is studied as sacred substance. Diablerie is religious act. "
    "Also called Tariqa el-Samma (Path of Heaven's Blood).",
)[0]

path_of_typhon = Path.objects.get_or_create(
    name="Path of Typhon",
    requires_conviction=True,
    requires_instinct=False,
    ethics="Set is the one true god. Corruption brings enlightenment. Spread Set's influence. "
    "Break others' chains through vice. Test others with temptation. Knowledge is in forbidden things. "
    "Destroy the weak gods. Set will rise again.",
    description="Followers of Set Path worshipping Set as deity. Spread corruption to free others from "
    "false morality. Temptation is holy work. Practitioners trade in vice and forbidden knowledge. "
    "Believe Set will return to rule.",
)[0]

path_of_paradox = Path.objects.get_or_create(
    name="Path of Paradox",
    requires_conviction=True,
    requires_instinct=False,
    ethics="Logic and reason are tools of enlightenment. Paradox reveals truth. Study contradictions. "
    "Emotion clouds judgment. The universe follows knowable laws. Time can be understood. "
    "Master causality. Existence is mathematical.",
    description="Rare Path of True Brujah emphasizing logic and reason. Study time and causality. "
    "Paradox is key to enlightenment. Emotion is weakness. The universe follows rational principles "
    "that can be understood and manipulated.",
)[0]

path_of_orion = Path.objects.get_or_create(
    name="Path of Orion",
    requires_conviction=True,
    requires_instinct=False,
    ethics="Hunt infernalists and demons. Protect mortals from supernatural evil. "
    "Undeath is curse and gift both. Use curse to fight greater evil. Evil must be destroyed. "
    "Sacrifice yourself for the innocent. Faith powers the righteous.",
    description="Salubri warrior Path focused on hunting infernalists and protecting innocents. "
    "Practitioners see themselves as cursed but use curse for good. Self-sacrifice is noble. "
    "Hunt demons and evil supernaturals.",
)[0]

path_of_haqim = Path.objects.get_or_create(
    name="Path of Haqim",
    requires_conviction=True,
    requires_instinct=False,
    ethics="Haqim judges all. Maintain balance. Accept contracts with honor. Blood is sacred but not all. "
    "Judge vampires by their actions. Lower Generation through righteous Amaranth. "
    "Follow the Qadi's wisdom. Unity with mortal kin.",
    description="Modern Assamite Path after breaking Tremere curse. More moderate than Path of Blood. "
    "Emphasizes judgment and balance. Contracts are sacred. Amaranth allowed but only against the wicked. "
    "Maintains connections to mortal Islamic traditions.",
)[0]

path_of_the_feral_heart = Path.objects.get_or_create(
    name="Path of the Feral Heart",
    requires_conviction=True,
    requires_instinct=True,
    ethics="The Beast is natural. Embrace animal nature. Civilization is prison. "
    "Hunt and kill freely. The wild is truth. Cities are cages. Instinct over thought. "
    "Pack loyalty is sacred. Territory must be defended.",
    description="Feral Path rejecting civilization. Practitioners embrace Beast and animal nature. "
    "Live as predators in wilderness. Cities are rejected as unnatural. Popular among some Gangrel. "
    "Also called Path of the Beast.",
)[0]

path_of_the_scorched_heart = Path.objects.get_or_create(
    name="Path of the Scorched Heart",
    requires_conviction=True,
    requires_instinct=False,
    ethics="Emotion is weakness. Burn away all feeling. Achieve perfect detachment. "
    "Love and hate equally cloud judgment. Passion destroys. Cold reason is strength. "
    "The heart must be scorched clean. No attachments.",
    description="Ascetic Path seeking to eliminate all emotion. Practitioners burn away feelings to "
    "achieve cold perfection. Attachments are weaknesses. Perfect detachment is goal. "
    "Extremely difficult to maintain; requires constant discipline.",
)[0]

path_of_entelechy = Path.objects.get_or_create(
    name="Path of Entelechy",
    requires_conviction=True,
    requires_instinct=False,
    ethics="Achieve perfection in chosen area. Master your art completely. "
    "Undeath allows unlimited time for perfection. Distractions must be eliminated. "
    "The work is everything. Obsessive focus brings enlightenment. Never settle.",
    description="Path of perfection and mastery. Practitioners obsessively pursue perfection in chosen "
    "field or art. Undeath's immortality allows unlimited time to master craft. Everything else is "
    "distraction. Popular among Toreador seeking artistic transcendence.",
)[0]

path_of_harmony = Path.objects.get_or_create(
    name="Path of Harmony",
    requires_conviction=False,
    requires_instinct=False,
    ethics="Seek balance in all things. Undeath and life must coexist. Extremes are harmful. "
    "Preserve mortals and Kindred both. Middle way is wisdom. Feed without killing. "
    "Meditation brings clarity. Karma affects all.",
    description="Eastern-influenced Path seeking balance between mortal and vampire nature. "
    "Practitioners try to harmonize Beast and human soul. Influenced by Buddhism and Taoism. "
    "Feed without killing when possible. Rare among Western vampires.",
)[0]

path_of_the_hive = Path.objects.get_or_create(
    name="Path of the Hive",
    requires_conviction=True,
    requires_instinct=True,
    ethics="The circle is everything. Individual doesn't matter. Serve the collective. "
    "Circle-mates are one being. Share all with brothers. Perfect unity is goal. "
    "Separation is death. The hive mind is sacred.",
    description="Blood Brothers exclusive Path. The circle of brothers created together is everything. "
    "Individual identity merges into collective. Separation from circle is agony. "
    "Perfect synchronization with circle-mates is goal.",
)[0]

path_of_evil_revelations = Path.objects.get_or_create(
    name="Path of Evil Revelations",
    requires_conviction=True,
    requires_instinct=True,
    ethics="Evil is liberating. Moral codes are chains. Inflict suffering to free others. "
    "Destruction is creation. Taboos must be broken. Corruption enlightens. "
    "The Abyss reveals truth. Infernalism is tool.",
    description="Dark Path practiced by Baali and other infernalists. Evil acts bring enlightenment. "
    "Suffering frees the soul. Morality is prison. Practitioners commit atrocities as spiritual acts. "
    "Connected to demonic powers and the Abyss.",
)[0]

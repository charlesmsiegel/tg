from characters.models.mage.focus import Instrument

armor = Instrument.objects.get_or_create(name="Armor")[0]
artwork = Instrument.objects.get_or_create(name="Artwork")[0]
atrocity = Instrument.objects.get_or_create(name="Atrocity")[0].add_source(
    "Book of the Fallen", 147
)
blessings = Instrument.objects.get_or_create(name="Blessings and curses")[0]
blood = Instrument.objects.get_or_create(name="Blood and fluids")[0]
body_modification = Instrument.objects.get_or_create(name="Body Modification")[0]
bodywork = Instrument.objects.get_or_create(name="Bodywork")[0]
bones = Instrument.objects.get_or_create(name="Bones and remains")[0]
books = Instrument.objects.get_or_create(name="Books and periodicals")[0]
brain_computer_interface = Instrument.objects.get_or_create(name="Brain/Computer interface")[0]
brews = Instrument.objects.get_or_create(name="Brews and concoctions")[0]
cannibalism = Instrument.objects.get_or_create(name="Cannibalism")[0]
cards = Instrument.objects.get_or_create(name="Cards and instruments of chance")[0]
celestial_alignments = Instrument.objects.get_or_create(name="Celestial alignments")[0]
circles = Instrument.objects.get_or_create(name="Circles and designs")[0]
computer_gear = Instrument.objects.get_or_create(name="Computer gear")[0]
cosmetics = Instrument.objects.get_or_create(name="Cosmetics")[0]
crossroads = Instrument.objects.get_or_create(name="Crossroads and crossing-days")[0]
cups = Instrument.objects.get_or_create(name="Cups and vessels")[0]
cybernetic_implants = Instrument.objects.get_or_create(name="Cybernetic Implants")[0]
dances = Instrument.objects.get_or_create(name="Dances and movement")[0]
devices = Instrument.objects.get_or_create(name="Devices and machines")[0]
drugs = Instrument.objects.get_or_create(name="Drugs and poisons")[0]
elements = Instrument.objects.get_or_create(name="Elements")[0]
energy = Instrument.objects.get_or_create(name="Energy")[0]
eye_contact = Instrument.objects.get_or_create(name="Eye contact")[0]
fashion = Instrument.objects.get_or_create(name="Fashion")[0]
food = Instrument.objects.get_or_create(name="Food and drink")[0]
formulae = Instrument.objects.get_or_create(name="Formulae and math")[0]
gadgets = Instrument.objects.get_or_create(name="Gadgets and inventions")[0]
gems = Instrument.objects.get_or_create(name="Gems and stones")[0]
genetic_manipulation = Instrument.objects.get_or_create(name="Genetic Manipulation")[0]
group_rites = Instrument.objects.get_or_create(name="Group rites")[0]
herbs = Instrument.objects.get_or_create(name="Herbs and plants")[0]
household_tools = Instrument.objects.get_or_create(name="Household tools")[0]
hypersigils = Instrument.objects.get_or_create(name="Hypersigils")[0].add_source(
    "Book of the Fallen", 148
)
internet_activity = Instrument.objects.get_or_create(name="Internet Activity")[0]
knots = Instrument.objects.get_or_create(name="Knots and ropes")[0]
labs = Instrument.objects.get_or_create(name="Labs and gear")[0]
languages = Instrument.objects.get_or_create(name="Languages")[0]
management = Instrument.objects.get_or_create(name="Management and HR")[0]
mass_media = Instrument.objects.get_or_create(name="Mass media")[0]
medical_procedures = Instrument.objects.get_or_create(name="Medical Procedures")[0]
meditation_instrument = Instrument.objects.get_or_create(name="Meditation")[0]
money = Instrument.objects.get_or_create(name="Money and wealth")[0]
music = Instrument.objects.get_or_create(name="Music")[0]
mutilation = Instrument.objects.get_or_create(name="Mutilation")[0].add_source(
    "Book of the Fallen", 148
)
nanotech = Instrument.objects.get_or_create(name="Nanotech")[0]
numbers = Instrument.objects.get_or_create(name="Numbers and numerology")[0]
offerings = Instrument.objects.get_or_create(name="Offerings and sacrifices")[0]
ordeals = Instrument.objects.get_or_create(name="Ordeals and exertions")[0]
perversion = Instrument.objects.get_or_create(name="Perversion")[0].add_source(
    "Book of the Fallen", 148
)
prayers = Instrument.objects.get_or_create(name="Prayers and invocations")[0]
sacred_iconography = Instrument.objects.get_or_create(name="Sacred iconography")[0]
sex = Instrument.objects.get_or_create(name="Sex and sensuality")[0]
social_dominion = Instrument.objects.get_or_create(name="Social domination")[0]
symbols = Instrument.objects.get_or_create(name="Symbols")[0]
thought_forms = Instrument.objects.get_or_create(name="Thought-forms")[0]
torment = Instrument.objects.get_or_create(name="Torment")[0].add_source("Book of the Fallen", 149)
toys = Instrument.objects.get_or_create(name="Toys")[0]
transgression = Instrument.objects.get_or_create(name="Transgression")[0]
tricks = Instrument.objects.get_or_create(name="Tricks and illusions")[0]
trolling = Instrument.objects.get_or_create(name="Trolling and Cyberbullying")[0].add_source(
    "Book of the Fallen", 150
)
true_names = Instrument.objects.get_or_create(name="True Names")[0]
vehicles = Instrument.objects.get_or_create(name="Vehicles")[0]
violation = Instrument.objects.get_or_create(name="Violation")[0].add_source(
    "Book of the Fallen", 150
)
voice = Instrument.objects.get_or_create(name="Voice and vocalizations")[0]
wands = Instrument.objects.get_or_create(name="Wands and staves")[0]
weapons = Instrument.objects.get_or_create(name="Weapons")[0]
writings = Instrument.objects.get_or_create(name="Writings, inscriptions and runes")[0]

artifacts = Instrument.objects.get_or_create(name="Artifacts and Antiques")[0]
contracts = Instrument.objects.get_or_create(name="Contracts")[0]
cryptocurrency = Instrument.objects.get_or_create(name="Cryptocurrency")[0]
employees = Instrument.objects.get_or_create(name="Employees")[0]
governments = Instrument.objects.get_or_create(name="Governments")[0]
markets = Instrument.objects.get_or_create(name="Markets")[0]
physical_media = Instrument.objects.get_or_create(name="Physical Media")[0]
precious_metals = Instrument.objects.get_or_create(name="Precious Metals")[0]
sacred_ground = Instrument.objects.get_or_create(name="Sacred Ground")[0]
social_media = Instrument.objects.get_or_create(name="Social Media")[0]


qi_tools = Instrument.objects.get_or_create(name="Qi Tools")[0].add_source(
    "Lore of the Traditions", 34
)
mantras = Instrument.objects.get_or_create(name="Mantras")[0].add_source(
    "Lore of the Traditions", 34
)
memories = Instrument.objects.get_or_create(name="Memories")[0].add_source(
    "Lore of the Traditions", 34
)

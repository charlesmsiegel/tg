from characters.models.vampire.title import VampireTitle
from characters.models.vampire.sect import VampireSect

# Get sects
camarilla = VampireSect.objects.get(name="Camarilla")
sabbat = VampireSect.objects.get(name="Sabbat")
anarch = VampireSect.objects.get(name="Anarch Movement")
independent = VampireSect.objects.get(name="Independent")

# CAMARILLA TITLES

prince = VampireTitle.objects.get_or_create(
    name="Prince",
    sect=camarilla,
    value=5,
    is_negative=False,
    description="Ruler of a Camarilla domain. Word is law within domain. Can declare Blood Hunts. "
    "Enforces the Six Traditions. Ultimate authority in city. Can grant and revoke hunting rights, "
    "acknowledge new vampires, and pass judgment.",
    powers="Enforce Traditions, declare Blood Hunts, grant domain, acknowledge vampires, "
    "call Conclaves, create and remove other titles (except Justicar)"
)[0]

justicar = VampireTitle.objects.get_or_create(
    name="Justicar",
    sect=camarilla,
    value=5,
    is_negative=False,
    description="Seven Justicars serve as traveling judges and troubleshooters for the Camarilla. "
    "One per clan (only major Camarilla clans). May overturn Princely decrees. Answerable only to "
    "Inner Circle. Cannot set policy directly but have immense investigative and judicial powers.",
    powers="Overturn Prince's decrees, summon Conclaves, call Blood Hunts, appoint Archons, "
    "investigate breaches of Tradition, cannot be held accountable by Princes"
)[0]

inner_circle = VampireTitle.objects.get_or_create(
    name="Inner Circle",
    sect=camarilla,
    value=7,
    is_negative=False,
    description="Governing body of the Camarilla. Ancient elders who set policy for entire sect. "
    "Can grant or revoke any powers. Nominate and censure Justicars. Can depose Princes. "
    "Meet in secret; identities often unknown. Absolute authority within Camarilla.",
    powers="Set Camarilla policy, nominate/censure Justicars, depose Princes, grant any title, "
    "ultimate authority over sect decisions"
)[0]

archon = VampireTitle.objects.get_or_create(
    name="Archon",
    sect=camarilla,
    value=4,
    is_negative=False,
    description="Agents and enforcers of Justicars. Considered above the law when acting on "
    "Justicar's behalf. May not be held accountable for Tradition transgressions while serving. "
    "Temporary position; serve at Justicar's pleasure.",
    powers="Act with Justicar's authority, violate Traditions on Justicar's business, "
    "investigate and enforce across domains, cannot be punished by Princes while serving"
)[0]

seneschal = VampireTitle.objects.get_or_create(
    name="Seneschal",
    sect=camarilla,
    value=4,
    is_negative=False,
    description="Prince's right hand and second-in-command. Acts as Prince when Prince is "
    "unavailable. Can claim Princely privileges if Prince unable to declare them. "
    "Often handles day-to-day governance while Prince handles big picture.",
    powers="Act as Prince in Prince's absence, claim Princely privileges when Prince unavailable, "
    "handle administrative duties, speak with Prince's voice (when authorized)"
)[0]

primogen = VampireTitle.objects.get_or_create(
    name="Primogen",
    sect=camarilla,
    value=3,
    is_negative=False,
    description="Clan representative on Primogen Council. Speaks for clan interests in domain. "
    "Can force Prince to recognize vote on major issues. Vote not binding but shows popular opinion. "
    "Collectively can make Prince's rule difficult if opposed.",
    powers="Voice clan concerns, vote on domain issues, force Prince to acknowledge votes, "
    "nominate positions (Sheriff, Scourge, etc.), collectively advise Prince"
)[0]

sheriff = VampireTitle.objects.get_or_create(
    name="Sheriff",
    sect=camarilla,
    value=2,
    is_negative=False,
    description="Enforcer of Prince's will and domain security. May violate Traditions by Prince's "
    "authority when enforcing law. Tracks down criminals, enforces Blood Hunts, maintains order. "
    "Often has deputies or hounds to assist.",
    powers="Enforce Prince's edicts, violate Traditions on Prince's authority, arrest vampires, "
    "execute Blood Hunts, maintain domain security, appoint deputies"
)[0]

harpy = VampireTitle.objects.get_or_create(
    name="Harpy",
    sect=camarilla,
    value=2,
    is_negative=False,
    description="Arbiter of boons and social standing. Determines validity of boons and debts. "
    "Controls social currency of domain. Can make or break reputations. Often work as group. "
    "Power comes from social influence rather than formal authority.",
    powers="Validate or invalidate boons, determine social standing, spread or suppress rumors, "
    "control information flow, arbitrate social disputes"
)[0]

keeper_of_elysium = VampireTitle.objects.get_or_create(
    name="Keeper of Elysium",
    sect=camarilla,
    value=1,
    is_negative=False,
    description="Maintains Elysium (neutral ground where violence forbidden). Authority within "
    "Elysium only. Acts as host and enforces Elysium rules. Ensures artistic and cultural events. "
    "Can ban individuals from Elysium (with Prince approval).",
    powers="Enforce Elysium rules, ban from Elysium (with approval), organize cultural events, "
    "maintain neutral ground, authority within Elysium only"
)[0]

scourge = VampireTitle.objects.get_or_create(
    name="Scourge",
    sect=camarilla,
    value=1,
    is_negative=False,
    description="Eliminates threats to domain: thin-blooded, Caitiff, unauthorized vampires. "
    "Secret police and cleaner. Status +1 when dealing with elders. Often works in shadows. "
    "May kill unacknowledged vampires without consequence.",
    powers="Destroy thin-blooded and Caitiff, eliminate unauthorized vampires, enforce domain purity, "
    "+1 Status with elders, hunt threats to Masquerade"
)[0]

whip = VampireTitle.objects.get_or_create(
    name="Whip",
    sect=camarilla,
    value=1,
    is_negative=False,
    description="Assistant to Primogen. Gathers clan members for votes and meetings. Enforces "
    "Primogen's will among clan. Acts as Primogen when Primogen unavailable. Often enforcer "
    "or messenger for Primogen.",
    powers="Represent Primogen, gather clan for votes, enforce Primogen decisions, "
    "act as Primogen in their absence, coordinate clan activities"
)[0]

# SABBAT TITLES

regent = VampireTitle.objects.get_or_create(
    name="Regent",
    sect=sabbat,
    value=7,
    is_negative=False,
    description="Autocratic ruler of entire Sabbat sect. Declares policy for sect. "
    "Commands Cardinals and Archbishops. Leads sect in preparation for Gehenna. "
    "Absolute authority within Sabbat structure.",
    powers="Set Sabbat policy, command all Sabbat vampires, declare Crusades and Wars, "
    "create and remove Cardinals, ultimate sect authority, judge disputes between Cardinals"
)[0]

cardinal = VampireTitle.objects.get_or_create(
    name="Cardinal",
    sect=sabbat,
    value=5,
    is_negative=False,
    description="Oversees vast geographical territory. Commands multiple Archbishops. "
    "Political game-players who report to Regent. Guide sect strategy in regions. "
    "May lead Crusades. Scheming and ambitious.",
    powers="Command region, direct Archbishops, lead Crusades, advise Regent, "
    "create and remove Archbishops in territory, strategic planning"
)[0]

archbishop = VampireTitle.objects.get_or_create(
    name="Archbishop",
    sect=sabbat,
    value=5,
    is_negative=False,
    description="Makes rules in Sabbat domain. Ultimate authority in territory. "
    "Equivalent to Camarilla Prince but with different philosophy. Commands packs and Bishops. "
    "Enforces Sabbat codes and prepares for Gehenna.",
    powers="Rule domain, command packs, appoint Bishops and Ductus, declare Crusades locally, "
    "enforce Sabbat law, judge pack disputes"
)[0]

priscus = VampireTitle.objects.get_or_create(
    name="Priscus",
    sect=sabbat,
    value=3,
    is_negative=False,
    description="Clan representative in Sabbat. No set standards for rising to position. "
    "Advises on clan-specific issues. Collectively form Prisci Council. "
    "Influence varies by clan strength and individual capability.",
    powers="Represent clan interests, advise Archbishop/Cardinal/Regent, vote on Prisci Council, "
    "coordinate clan activities, speak for clan to leadership"
)[0]

bishop = VampireTitle.objects.get_or_create(
    name="Bishop",
    sect=sabbat,
    value=3,
    is_negative=False,
    description="Authority over one facet of Cainite influence in domain. Types include: "
    "Bishop of Industry (business), Bishop of Mortal Chattel (food supply), Bishop of Occult "
    "(supernatural threats). Reports to Archbishop.",
    powers="Command specific aspect of domain, direct packs in area of authority, "
    "report to Archbishop, advise on specialty, coordinate domain resources"
)[0]

inquisitor = VampireTitle.objects.get_or_create(
    name="Inquisitor",
    sect=sabbat,
    value=3,
    is_negative=False,
    description="Deals with infernalism and corruption. Greatly feared and respected. "
    "Can investigate anyone, including Archbishops. Answers to Regent. "
    "Empowered to root out demonic influence and traitors.",
    powers="Investigate anyone for infernalism, trial by ordeal, execute infernalists, "
    "cannot be refused or blocked, authority to torture and destroy, report to Regent"
)[0]

templar = VampireTitle.objects.get_or_create(
    name="Templar",
    sect=sabbat,
    value=2,
    is_negative=False,
    description="Bodyguard to Cardinal or Regent. Elite warriors sworn to protect leader. "
    "Hand-picked for loyalty and combat skill. May act with leader's authority. "
    "Prestigious position showing trust.",
    powers="Protect assigned leader, act with leader's authority (when specified), "
    "elite combat training, command resources for protection, investigate threats to leader"
)[0]

paladin = VampireTitle.objects.get_or_create(
    name="Paladin",
    sect=sabbat,
    value=2,
    is_negative=False,
    description="Champion of Sabbat, enforcer and investigator. Mobile troubleshooter "
    "similar to Camarilla Archon. Serves Cardinals or Regent. Hunts enemies and "
    "enforces Sabbat law across territories.",
    powers="Investigate across domains, enforce Sabbat law, hunt enemies, "
    "act with Cardinal/Regent authority, cannot be blocked by local leaders"
)[0]

ductus = VampireTitle.objects.get_or_create(
    name="Ductus",
    sect=sabbat,
    value=1,
    is_negative=False,
    description="Pack leader. Most frequently granted and vacated position. Leads pack in "
    "battle and daily activities. Chosen by pack (formally) or by strength (actually). "
    "Works with Pack Priest to guide pack.",
    powers="Lead pack, direct pack activities, represent pack to Archbishop, "
    "make tactical decisions, coordinate with other Ductus"
)[0]

pack_priest = VampireTitle.objects.get_or_create(
    name="Pack Priest",
    sect=sabbat,
    value=1,
    is_negative=False,
    description="Spiritual complement to Ductus. Guides pack on Path of Enlightenment. "
    "Leads Auctoritas Ritae (Sabbat rituals). Ensures pack stays true to Sabbat ideals. "
    "Performs Vaulderie and other ceremonies.",
    powers="Lead rituals, guide on Paths, perform Vaulderie, advise Ductus spiritually, "
    "conduct Creation Rites and other ceremonies"
)[0]

true_sabbat = VampireTitle.objects.get_or_create(
    name="True Sabbat",
    sect=sabbat,
    value=0,
    is_negative=False,
    description="Proven worthy of continued existence. Minimum rank before earning Status. "
    "Survived Creation Rites and proven loyalty. No special powers but recognized as "
    "legitimate Sabbat member rather than shovelhead or recruit.",
    powers="None formal; simply recognized as worthy Sabbat member, can earn Status, "
    "participate fully in sect activities"
)[0]

# ANARCH MOVEMENT TITLES

baron = VampireTitle.objects.get_or_create(
    name="Baron",
    sect=anarch,
    value=4,
    is_negative=False,
    description="Anarch domain leader. Similar to Prince but with limited powers. "
    "Interprets Masquerade and Domain Traditions for area. Maintains order through "
    "respect and strength rather than formal authority. Power varies by domain.",
    powers="Limited domain authority, interpret Masquerade, maintain order, "
    "speak for domain, coordinate defenses, power based on respect not decree"
)[0]

warlord = VampireTitle.objects.get_or_create(
    name="Warlord",
    sect=anarch,
    value=3,
    is_negative=False,
    description="Charismatic or violent insurgency leader. Motivates fighting factions. "
    "Leads Anarchs in revolt or warfare. May challenge Baron or Prince. "
    "Temporary position often; lasts as long as conflict.",
    powers="Lead rebellion, command in battle, motivate fighters, coordinate attacks, "
    "declare targets, organize resistance"
)[0]

sweeper = VampireTitle.objects.get_or_create(
    name="Sweeper",
    sect=anarch,
    value=2,
    is_negative=False,
    description="Tracks who's in domain. Prevents surprises about population. "
    "Monitors for Camarilla or Sabbat infiltrators. Keeps Baron informed. "
    "Intelligence and security role.",
    powers="Track domain population, identify newcomers, report to Baron, "
    "investigate strangers, maintain intelligence network, counter infiltration"
)[0]

reeve = VampireTitle.objects.get_or_create(
    name="Reeve",
    sect=anarch,
    value=1,
    is_negative=False,
    description="Similar to Sheriff but with less accountability. Enforces Baron's will. "
    "Maintains domain security. Often more brutal than Camarilla Sheriff due to "
    "fewer formal restrictions. Varies by domain.",
    powers="Enforce Baron's will, maintain security, punish transgressors, "
    "defend domain, less formal restriction than Camarilla counterpart"
)[0]

coyote = VampireTitle.objects.get_or_create(
    name="Coyote",
    sect=anarch,
    value=1,
    is_negative=False,
    description="Specializes in smuggling Kindred in and out of domains. "
    "Knows secret routes and contacts. Helps Anarchs move undetected. "
    "May smuggle goods as well. Connected to underworld.",
    powers="Smuggle vampires, know secret routes, bypass domain security, "
    "underground contacts, transport goods and people covertly"
)[0]

# INDEPENDENT TITLES (Universal/Non-Sect)

autarkis = VampireTitle.objects.get_or_create(
    name="Autarkis",
    sect=None,
    value=0,
    is_negative=False,
    description="Vampire who rejects all sect allegiance. Independent loner. "
    "No formal authority but earns respect through independence. May be viewed "
    "with suspicion or admiration. Lives by own code.",
    powers="None formal; owes no sect allegiance, makes own decisions, "
    "outside sect politics and protection"
)[0]

# NEGATIVE TITLES

betrayer = VampireTitle.objects.get_or_create(
    name="Betrayer",
    sect=None,
    value=1,
    is_negative=True,
    description="Known for breaking trust or betraying others. Subtract 1 from social dice pools. "
    "Reputation for treachery precedes them. Cannot be bought off with experience. "
    "Must be earned through roleplaying redemption.",
    powers="None; subtracts from social interactions, marks bearer as untrustworthy"
)[0]

coward = VampireTitle.objects.get_or_create(
    name="Coward",
    sect=None,
    value=1,
    is_negative=True,
    description="Known for fleeing from danger or abandoning allies. Subtract 1 from social dice pools. "
    "Reputation for cowardice. Difficult to remove stigma.",
    powers="None; subtracts from social interactions, marks bearer as unreliable in conflict"
)[0]

oathbreaker = VampireTitle.objects.get_or_create(
    name="Oathbreaker",
    sect=None,
    value=1,
    is_negative=True,
    description="Broke sworn oath or blood vow. Subtract 1 from social dice pools. "
    "Particularly damning in Sabbat where honor is prized. Very difficult to overcome. "
    "Trust is permanently damaged.",
    powers="None; subtracts from social interactions, marks bearer as oath-breaker"
)[0]

masquerade_breacher = VampireTitle.objects.get_or_create(
    name="Masquerade Breacher",
    sect=camarilla,
    value=1,
    is_negative=True,
    description="Known for breaking or threatening Masquerade. Subtract 1 from social dice pools "
    "in Camarilla domains. May face Blood Hunt if breach was severe. Watched carefully by Sheriffs.",
    powers="None; subtracts from social interactions in Camarilla, marked for monitoring"
)[0]

# ADDITIONAL IMPORTANT TITLES

ambassador = VampireTitle.objects.get_or_create(
    name="Ambassador",
    sect=None,
    value=2,
    is_negative=False,
    description="Represents domain or sect to another power. Diplomatic immunity (usually). "
    "Negotiates treaties and agreements. Speaks with authority of sender. "
    "Must be accorded respect per Traditions.",
    powers="Diplomatic immunity, speak for sender, negotiate treaties, "
    "must be received properly per Hospitality Tradition"
)[0]

emissary = VampireTitle.objects.get_or_create(
    name="Emissary",
    sect=None,
    value=1,
    is_negative=False,
    description="Temporary messenger between powers. Lesser than Ambassador. "
    "Delivers messages and minor negotiations. Some diplomatic courtesy expected.",
    powers="Deliver messages, minor negotiations, some diplomatic courtesy, "
    "temporary diplomatic protection"
)[0]

master_of_the_hunt = VampireTitle.objects.get_or_create(
    name="Master of the Hunt",
    sect=camarilla,
    value=2,
    is_negative=False,
    description="Organizes and leads Blood Hunts. Temporary position during hunt. "
    "Commands all participants. Ensures target is destroyed. Coordinates pursuit.",
    powers="Command Blood Hunt participants, coordinate pursuit, track quarry, "
    "ensure destruction, authority during hunt only"
)[0]

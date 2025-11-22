from characters.models.core.archetype import Archetype

activist = Archetype.objects.get_or_create(
    name="Activist",
    description="You see injustice and cannot stand idle. Whether fighting for environmental causes, social justice, or political change, the Activist dedicates their life to making the world better. You organize, protest, educate, and inspire others to action. For you, apathy is the true enemy - as long as people care and act, change is possible. You regain Willpower when your actions directly contribute to positive social or political change, or when you successfully recruit others to your cause.",
)[0].add_source("Mage: the Ascension 20th Anniversary Edition", 268)
alpha = Archetype.objects.get_or_create(
    name="Alpha",
    description="You are the natural leader of the pack, commanding through strength, charisma, and force of will. The Alpha establishes dominance and expects others to follow. You protect your pack fiercely but demand absolute loyalty in return. You regain Willpower when your leadership is challenged and you successfully maintain your position, or when your pack achieves victory through following your commands.",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 486)
architect = (
    Archetype.objects.get_or_create(
        name="Architect",
        description="You build things meant to last - whether physical structures, organizations, institutions, or legacies. The Architect doesn't just create; they create with vision and purpose, laying foundations for the future. You think in terms of decades and generations, not days and weeks. Your greatest satisfaction comes from seeing your creations stand the test of time and serve their intended purpose. You regain Willpower when you complete a significant stage of a long-term project or see your creations benefit others as intended.",
    )[0]
    .add_source("Book of Secrets", 14)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 486)
)
artist = Archetype.objects.get_or_create(
    name="Artist",
    description="You see beauty and meaning in the world that others miss, and you must express it through your chosen medium. Whether painter, musician, writer, or performer, the Artist channels emotion and truth into their work. Art isn't just what you do - it's who you are and how you understand existence. You regain Willpower when your art moves others emotionally or when you achieve an important artistic breakthrough.",
)[0].add_source("Book of Secrets", 14)
barterer = Archetype.objects.get_or_create(name="Barterer")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 486
)
benefactor = Archetype.objects.get_or_create(
    name="Benefactor",
    description="You find purpose in helping others succeed. The Benefactor uses their resources, connections, or expertise to support those with potential but lacking means. You're the patron, mentor, and silent supporter who enables great works without seeking personal glory. Your satisfaction comes from seeing your proteges flourish. You regain Willpower when someone you've assisted achieves significant success through your aid.",
)[0].add_source("Mage: the Ascension 20th Anniversary Edition", 268)
big_bad_wolf = Archetype.objects.get_or_create(name="Big Bad Wolf")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 486
)
bon_vivant = (
    Archetype.objects.get_or_create(
        name="Bon Vivant",
        description="Life is to be enjoyed, savored, and experienced to the fullest. The Bon Vivant pursues pleasure, beauty, and sensation with infectious enthusiasm. You believe that joy and aesthetic appreciation are not frivolous but essential to a life well-lived. While others might see you as hedonistic, you understand that celebrating life's pleasures is its own form of wisdom. You regain Willpower when you fully indulge in your passions or introduce others to new experiences they genuinely enjoy.",
    )[0]
    .add_source("Book of Secrets", 14)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 487)
)
bravo = Archetype.objects.get_or_create(name="Bravo")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 487
)
caregiver = (
    Archetype.objects.get_or_create(
        name="Caregiver",
        description="You nurture and protect those who cannot care for themselves. Whether tending the sick, teaching children, or supporting the vulnerable, the Caregiver finds meaning in service to others. You see potential in everyone and believe that with proper support, people can flourish. Your greatest fear is failing someone who depends on you. You regain Willpower when you successfully protect or nurture someone at risk, particularly when doing so requires personal sacrifice.",
    )[0]
    .add_source("Book of Secrets", 15)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 487)
)
celebrant = Archetype.objects.get_or_create(name="Celebrant")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 487
)
competitor = Archetype.objects.get_or_create(
    name="Competitor",
    description="For you, life is a contest where success is measured by victory. The Competitor thrives on challenges, always seeking to test themselves against worthy opposition. You don't necessarily seek to harm your rivals - you simply need to prove you're the best. Whether in sports, business, academics, or supernatural conflicts, you measure your worth by your victories. You regain Willpower when you succeed in direct competition, particularly against challenging opponents.",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 487)
conformist = (
    Archetype.objects.get_or_create(
        name="Conformist",
        description="You find security and identity in being part of something larger than yourself. The Conformist follows rules, respects hierarchy, and trusts in established institutions. You're not weak or mindless - you genuinely believe that order and tradition provide necessary stability. Your greatest fear is chaos and isolation. You regain Willpower when adhering to group rules leads to success or when the group/authority validates your membership and loyalty.",
    )[0]
    .add_source("Book of Secrets", 15)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 487)
)
conniver = Archetype.objects.get_or_create(name="Conniver")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 487
)
contrary = (
    Archetype.objects.get_or_create(
        name="Contrary",
        description="You question everything and trust nothing at face value. The Contrary plays devil's advocate, challenges assumptions, and refuses to follow the crowd. You're not necessarily opposed to everything - you just demand that beliefs and actions be justified by reason rather than tradition or authority. Others may find you difficult, but you serve the vital function of preventing groupthink. You regain Willpower when your questioning reveals important truth or prevents the group from making a mistake based on unexamined assumptions.",
    )[0]
    .add_source("Mage: the Ascension 20th Anniversary Edition", 268)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 487)
)
crusader = Archetype.objects.get_or_create(
    name="Crusader",
    description="You have found your calling - a cause greater than yourself that demands total commitment. The Crusader fights for their beliefs with unwavering dedication, whether battling cosmic evil, championing social justice, or defending the helpless. Your cause gives your life meaning and direction. You regain Willpower when you make a significant sacrifice for your cause or achieve a major victory in its service.",
)[0].add_source("Mage: the Ascension 20th Anniversary Edition", 268)
cub = Archetype.objects.get_or_create(name="Cub")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 488
)
director = (
    Archetype.objects.get_or_create(
        name="Director",
        description="You lead, organize, and take charge. The Director sees what needs doing and ensures it gets done, coordinating others and making necessary decisions. You have a talent for leadership and the will to shoulder responsibility. While some might see you as controlling, you know that without direction, most efforts end in chaos. You regain Willpower when your leadership directly leads to group success, particularly in challenging situations.",
    )[0]
    .add_source("Book of Secrets", 15)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 488)
)
entertainer = Archetype.objects.get_or_create(
    name="Entertainer",
    description="You live to bring joy, laughter, and wonder to others. The Entertainer performs not for glory or wealth (though those are nice) but for the reaction of the audience. Whether actor, comedian, musician, or storyteller, you understand that entertainment serves a vital social function. You regain Willpower when your performance significantly impacts your audience emotionally or when you receive genuine acclaim for your artistry.",
)[0].add_source("Book of Secrets", 15)
fanatic = Archetype.objects.get_or_create(name="Fanatic")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 488
)
fatalist = Archetype.objects.get_or_create(name="Fatalist")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 488
)
gallant = Archetype.objects.get_or_create(name="Gallant")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 488
)
guardian = Archetype.objects.get_or_create(
    name="Guardian",
    description="You protect what is precious. The Guardian stands watch over people, places, things, or ideals, defending them against all threats. You define yourself by what you protect and take your duty with deadly seriousness. Betraying your charge is unthinkable - you would rather die than abandon your responsibility. You regain Willpower when you successfully protect your charge from significant danger, particularly when doing so requires personal sacrifice.",
)[0].add_source("Book of Secrets", 16)
guru = Archetype.objects.get_or_create(name="Guru")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 488
)
hacker = Archetype.objects.get_or_create(
    name="Hacker",
    description="You break into systems - computer networks, organizations, secrets, or mysteries - because they exist to be challenged. The Hacker sees security as a puzzle and takes joy in bypassing it. You're driven by curiosity and the thrill of the challenge rather than malice. Your greatest satisfaction comes from accessing what should be inaccessible. You regain Willpower when you successfully infiltrate a well-defended system or reveal important hidden information.",
)[0].add_source("Mage: the Ascension 20th Anniversary Edition", 269)
heretic = Archetype.objects.get_or_create(
    name="Heretic",
    description="You reject orthodox doctrine and pursue truth wherever it leads, even into blasphemy. The Heretic sees hidden wisdom in forbidden knowledge and challenges established religious or philosophical traditions. You're not an atheist or nihilist - you have deep spiritual beliefs, they just don't align with mainstream teachings. You regain Willpower when your heterodox beliefs prove insightful or when you discover esoteric truth.",
)[0].add_source("Book of Secrets", 16)
idealist = (
    Archetype.objects.get_or_create(
        name="Idealist",
        description="You believe in a better world and work to manifest it. The Idealist holds fast to principles and dreams even when reality seems to disprove them. You maintain that cynicism and despair are self-fulfilling prophecies, while hope and integrity can genuinely transform the world. Others may call you naive, but you know that ideals are what separate mere survival from meaningful existence. You regain Willpower when you maintain your principles despite pressure to compromise, or when your idealism inspires positive change.",
    )[0]
    .add_source("Mage: the Ascension 20th Anniversary Edition", 269)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 488)
)
innovator = Archetype.objects.get_or_create(
    name="Innovator",
    description="You create new things - technologies, ideas, methods, or approaches. The Innovator refuses to accept that the current way is the only way, constantly seeking to improve, invent, and revolutionize. You thrive on the cutting edge where others fear to tread. Your innovations may be controversial, but you know progress requires risk. You regain Willpower when you successfully implement a novel solution or when one of your innovations proves its worth.",
)[0].add_source("Mage: the Ascension 20th Anniversary Edition", 270)
judge = Archetype.objects.get_or_create(name="Judge")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 488
)
kid = Archetype.objects.get_or_create(
    name="Kid",
    description="Despite your actual age, you see the world with wonder and approach life with youthful enthusiasm. The Kid maintains innocence, curiosity, and optimism that others have lost. You ask questions, try new things, and believe in possibilities that cynical adults dismiss. Your wonder is genuine, not affected, and it can remind others of what they've forgotten. You regain Willpower when your youthful perspective solves a problem or when you experience genuine wonder at discovery.",
)[0].add_source("Mage: the Ascension 20th Anniversary Edition", 270)
loner = (
    Archetype.objects.get_or_create(
        name="Loner",
        description="You walk your own path, neither leading nor following. The Loner finds that groups demand conformity and relationships create dependency. You're self-reliant, independent, and comfortable in your own company. You're not necessarily antisocial - you may have allies - but you don't define yourself through group membership or relationships. You regain Willpower when you accomplish something significant through your own efforts, without help or interference from others.",
    )[0]
    .add_source("Mage: the Ascension 20th Anniversary Edition", 270)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 489)
)
machine = Archetype.objects.get_or_create(
    name="Machine",
    description="You suppress emotion and individual desire in favor of efficiency and function. The Machine subordinates personal feelings to duty, rational analysis, or the needs of the collective. You may be a dedicated soldier, a logical scientist, or a devoted bureaucrat. Emotions cloud judgment and personal wants distract from essential tasks. You regain Willpower when emotional detachment allows you to make necessary hard choices or when efficiency and logic achieve what passion could not.",
)[0].add_source("Mage: the Ascension 20th Anniversary Edition", 270)
mad_scientist = Archetype.objects.get_or_create(
    name="Mad Scientist",
    description="You pursue knowledge and innovation without regard for conventional ethics or safety. The Mad Scientist sees scientific truth as beyond mundane morality - if something CAN be done, it MUST be done, to see what happens. Your experiments may be dangerous or ethically questionable, but you know that progress requires pushing boundaries. You regain Willpower when your unorthodox research yields significant discoveries or when you pursue science despite opposition from the timid.",
)[0].add_source("Mage: the Ascension 20th Anniversary Edition", 270)
martyr = (
    Archetype.objects.get_or_create(
        name="Martyr",
        description="You find meaning in suffering for a cause or ideal. The Martyr believes that sacrifice has spiritual power and that enduring hardship validates their beliefs. You don't seek pain for its own sake, but you're willing - even eager - to suffer if it serves a higher purpose. Your dedication can inspire others or make them uncomfortable with their own compromises. You regain Willpower when you endure significant hardship for your beliefs or when your sacrifice meaningfully advances your cause.",
    )[0]
    .add_source("Mage: the Ascension 20th Anniversary Edition", 271)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 489)
)
mentor = Archetype.objects.get_or_create(
    name="Mentor",
    description="You guide others on their journey, sharing your knowledge and experience. The Mentor finds fulfillment in teaching, advising, and helping others develop their potential. You've walked the path before and understand its dangers and opportunities. Your legacy lives through those you've taught. You regain Willpower when a student you've trained achieves significant success or overcomes a challenge through lessons you provided.",
)[0].add_source("Book of Secrets", 17)
monster = Archetype.objects.get_or_create(
    name="Monster",
    description="You embrace the darkness within and accept that you are the thing others fear. The Monster doesn't pretend to be normal or fight their nature - they acknowledge what they've become and act accordingly. You may be a predator, an outcast, or something genuinely inhuman. Self-deception is not an option. You regain Willpower when you frighten others with your true nature or when you accomplish something only possible by embracing what you are.",
)[0].add_source("Mage: the Ascension 20th Anniversary Edition", 271)
pedagogue = Archetype.objects.get_or_create(name="Pedagogue")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 489
)
penitent = Archetype.objects.get_or_create(name="Penitent")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 489
)
perfectionist = Archetype.objects.get_or_create(name="Perfectionist")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 490
)
prophet = Archetype.objects.get_or_create(
    name="Prophet",
    description="You receive visions of truth - whether divine revelation, mystical insight, or uncanny intuition - and feel compelled to share them. The Prophet serves as a conduit for forces beyond normal understanding, speaking truths that others need to hear but may not want to accept. Your pronouncements are often cryptic or unsettling, but events tend to prove you right. You regain Willpower when your prophecies or insights prove accurate or when your warnings prevent disaster.",
)[0].add_source("Mage: the Ascension 20th Anniversary Edition", 272)
rebel = Archetype.objects.get_or_create(
    name="Rebel",
    description="You fight against authority and established order because freedom requires it. The Rebel sees rules as chains and tradition as stagnation. You question those in power, violate unjust laws, and inspire others to think for themselves. You're not chaotic - you often have strong principles - but you refuse to let authority figures think for you. You regain Willpower when you successfully defy unjust authority or inspire others to question and resist oppression.",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 490)
rogue = (
    Archetype.objects.get_or_create(
        name="Rogue",
        description="You survive by your wits, living by your own code in the margins of society. The Rogue is a trickster, a con artist, a charming scoundrel who bends rules without quite breaking them. You're self-interested but not necessarily evil - you just look out for number one in a world that won't do it for you. You regain Willpower when you profit from a clever scam or when your roguish skills solve a problem that honest methods couldn't.",
    )[0]
    .add_source("Mage: the Ascension 20th Anniversary Edition", 272)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 490)
)
romantic = Archetype.objects.get_or_create(
    name="Romantic",
    description="You believe in love, passion, and deep emotional connection. The Romantic sees relationships and aesthetic beauty as life's highest values. You pursue ideal love and perfect moments of connection, whether romantic, platonic, or artistic. You regain Willpower when you experience or facilitate a profound moment of genuine connection or beauty.",
)[0].add_source("Book of Secrets", 17)
scientist = Archetype.objects.get_or_create(
    name="Scientist",
    description="You seek to understand the universe through systematic observation and rational analysis. The Scientist values evidence over superstition, methodology over intuition. You believe that mystery is simply ignorance waiting to be dispelled through rigorous investigation. Your approach may seem cold, but you know that understanding is the foundation of genuine progress. You regain Willpower when your systematic analysis reveals important truth or when the scientific method solves a problem.",
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 490)
sensualist = Archetype.objects.get_or_create(
    name="Sensualist",
    description="You experience life through the senses, seeking intense sensory and aesthetic experiences. The Sensualist understands that existence is physical and that consciousness itself arises from sensation. You're drawn to beautiful sights, exquisite flavors, sublime music, and all manner of sensory pleasure. You're not merely hedonistic - you're exploring the full spectrum of embodied experience. You regain Willpower when you experience or create something of exceptional beauty or intensity.",
)[0].add_source("Mage: the Ascension 20th Anniversary Edition", 272)
soldier = Archetype.objects.get_or_create(name="Soldier")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 490
)
survivor = (
    Archetype.objects.get_or_create(
        name="Survivor",
        description="You endure. When others would break or surrender, the Survivor finds a way to persist. You've faced hardship that would destroy weaker people, and you've learned that survival requires pragmatism, resilience, and the will to do whatever is necessary. You don't glorify suffering - you simply refuse to quit. You regain Willpower when you survive a genuinely threatening situation through your own resourcefulness and determination.",
    )[0]
    .add_source("Mage: the Ascension 20th Anniversary Edition", 272)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 490)
)
thrill_seeker = Archetype.objects.get_or_create(name="Thrill-Seeker")[0].add_source(
    "Werewolf: the Apocalypse 20th Anniversary Edition", 490
)
traditionalist = (
    Archetype.objects.get_or_create(
        name="Traditionalist",
        description="You honor the old ways and maintain continuity with the past. The Traditionalist sees wisdom in established customs and believes that rapid change destroys more than it creates. You're the keeper of rituals, the maintainer of standards, and the living link to heritage. Progress is fine, but it must build on proven foundations. You regain Willpower when adherence to tradition proves wise or when you successfully preserve important customs against forces of change.",
    )[0]
    .add_source("Mage: the Ascension 20th Anniversary Edition", 272)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 491)
)
trickster = (
    Archetype.objects.get_or_create(
        name="Trickster",
        description="You see the absurdity in everything and can't resist puncturing pretension. The Trickster uses humor, pranks, and clever manipulation to reveal truths that straightforward honesty never could. You're not cruel - you're teaching important lessons about not taking oneself too seriously. Chaos and uncertainty are necessary counterbalances to rigid order. You regain Willpower when your tricks teach someone an important lesson or when your chaos reveals a truth that order concealed.",
    )[0]
    .add_source("Mage: the Ascension 20th Anniversary Edition", 272)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 491)
)
tycoon = Archetype.objects.get_or_create(
    name="Tycoon",
    description="You build empires through business acumen and strategic thinking. The Tycoon measures success in wealth, power, and market dominance. You understand that money is both tool and scorecard in the game of life. You regain Willpower when your business ventures succeed significantly or when you outmaneuver competitors.",
)[0].add_source("Book of Secrets", 17)
vigilante = Archetype.objects.get_or_create(
    name="Vigilante",
    description="Justice delayed is justice denied, and you won't wait for broken systems to protect the innocent. The Vigilante takes justice into their own hands, punishing those who evade legal consequences. You operate outside the law to defend a higher law. You regain Willpower when you successfully punish evildoers who have escaped official justice.",
)[0].add_source("Book of Secrets", 17)
visionary = (
    Archetype.objects.get_or_create(
        name="Visionary",
        description="You see possibilities that others cannot imagine. The Visionary perceives the world not as it is, but as it could be. Your insights may seem mad or impossible, but you understand patterns and potential that escape conventional thinking. You inspire others with your grand vision, even if realizing it seems far-fetched. You regain Willpower when you convince others to believe in your vision or when events prove that your seemingly impossible ideas were actually prophetic.",
    )[0]
    .add_source("Mage: the Ascension 20th Anniversary Edition", 273)
    .add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 491)
)
zealot = Archetype.objects.get_or_create(
    name="Zealot",
    description="Your cause is everything, and you pursue it with fanatical devotion. The Zealot has found absolute truth and cannot comprehend why others don't see it. You will use any means necessary to advance your beliefs, viewing moderation and compromise as betrayal. You regain Willpower when you make converts to your cause or when you sacrifice significantly in service to your beliefs.",
)[0].add_source("Book of Secrets", 17)
addict = Archetype.objects.get_or_create(name="Addict")[0].add_source(
    "Demon: the Fallen", 132
)
architect = Archetype.objects.get_or_create(name="Architect")[0].add_source(
    "Demon: the Fallen", 133
)
autocrat = Archetype.objects.get_or_create(name="Autocrat")[0].add_source(
    "Demon: the Fallen", 133
)
bon_vivant = Archetype.objects.get_or_create(name="Bon Vivant")[0].add_source(
    "Demon: the Fallen", 133
)
bravo = Archetype.objects.get_or_create(name="Bravo")[0].add_source(
    "Demon: the Fallen", 133
)
caregiver = Archetype.objects.get_or_create(name="Caregiver")[0].add_source(
    "Demon: the Fallen", 133
)
child = Archetype.objects.get_or_create(name="Child")[0].add_source(
    "Demon: the Fallen", 133
)
competitor = Archetype.objects.get_or_create(name="Competitor")[0].add_source(
    "Demon: the Fallen", 133
)
conformist = Archetype.objects.get_or_create(name="Conformist")[0].add_source(
    "Demon: the Fallen", 133
)
conniver = Archetype.objects.get_or_create(name="Conniver")[0].add_source(
    "Demon: the Fallen", 133
)
curmudgeon = Archetype.objects.get_or_create(name="Curmudgeon")[0].add_source(
    "Demon: the Fallen", 134
)
deviant = Archetype.objects.get_or_create(name="Deviant")[0].add_source(
    "Demon: the Fallen", 134
)
director = Archetype.objects.get_or_create(name="Director")[0].add_source(
    "Demon: the Fallen", 134
)
fanatic = Archetype.objects.get_or_create(name="Fanatic")[0].add_source(
    "Demon: the Fallen", 134
)
gallant = Archetype.objects.get_or_create(name="Gallant")[0].add_source(
    "Demon: the Fallen", 134
)
gambler = Archetype.objects.get_or_create(name="Gambler")[0].add_source(
    "Demon: the Fallen", 134
)
judge = Archetype.objects.get_or_create(name="Judge")[0].add_source(
    "Demon: the Fallen", 134
)
loner = Archetype.objects.get_or_create(name="Loner")[0].add_source(
    "Demon: the Fallen", 134
)
martyr = Archetype.objects.get_or_create(name="Martyr")[0].add_source(
    "Demon: the Fallen", 134
)
masochist = Archetype.objects.get_or_create(name="Masochist")[0].add_source(
    "Demon: the Fallen", 135
)
monster = Archetype.objects.get_or_create(name="Monster")[0].add_source(
    "Demon: the Fallen", 135
)
pedagogue = Archetype.objects.get_or_create(name="Pedagogue")[0].add_source(
    "Demon: the Fallen", 135
)
penitent = Archetype.objects.get_or_create(name="Penitent")[0].add_source(
    "Demon: the Fallen", 135
)
perfectionist = Archetype.objects.get_or_create(name="Perfectionist")[0].add_source(
    "Demon: the Fallen", 135
)
rebel = Archetype.objects.get_or_create(name="Rebel")[0].add_source(
    "Demon: the Fallen", 135
)
rogue = Archetype.objects.get_or_create(name="Rogue")[0].add_source(
    "Demon: the Fallen", 135
)
survivor = Archetype.objects.get_or_create(name="Survivor")[0].add_source(
    "Demon: the Fallen", 135
)
thrill_seeker = Archetype.objects.get_or_create(name="Thrill-Seeker")[0].add_source(
    "Demon: the Fallen", 135
)
traditionalist = Archetype.objects.get_or_create(name="Traditionalist")[0].add_source(
    "Demon: the Fallen", 135
)
trickster = Archetype.objects.get_or_create(name="Trickster")[0].add_source(
    "Demon: the Fallen", 136
)
visionary = Archetype.objects.get_or_create(name="Visionary")[0].add_source(
    "Demon: the Fallen", 136
)
zealot = Archetype.objects.get_or_create(name="Zealot")[0].add_source(
    "Demon: the Fallen", 136
)
damned_soul = Archetype.objects.get_or_create(name="Damned Soul")[0].add_source(
    "Dammned and Deceived", 60
)
narcissist = Archetype.objects.get_or_create(name="Narcissist")[0].add_source(
    "Dammned and Deceived", 60
)
proselytizer = Archetype.objects.get_or_create(name="Proselytizer")[0].add_source(
    "Dammned and Deceived", 61
)

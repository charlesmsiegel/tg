from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.mage.sphere import Sphere
from populate_db.objects import (
    changeling,
    companion,
    human,
    kinfolk,
    mage,
    node,
    sorcerer,
    werewolf,
)

# W20
mf = MeritFlaw.objects.get_or_create(name="Acute Sense (Werewolf)")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Alcohol Tolerance")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Ambidextrous")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Double-Jointed")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Mixed-morph")[0]
mf.add_ratings([1, 5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Perfect Balance (Werewolf)")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Wolf Sight")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Bad Taste")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Fair Glabro")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Lack of Scent")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Physically Impressive")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Daredevil")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Long-Distance Runner")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Natural Weapons")[0]
mf.add_ratings([3, 4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Huge Size")[0]
mf.add_ratings([4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Metamorph")[0]
mf.add_ratings([7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Animal Musk")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Anosmia")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Hard of Hearing")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Monochrome Vision")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="No Partial Transformation")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Short (Werewolf)")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Strict Carnivore")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="One Eye")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Bad Sight (Werewolf)")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Deformity")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Double Jeopardy")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Lame")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Monstrous")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="One Arm")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Deaf")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Mute")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Blind")[0]
mf.add_ratings([-6])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Common Sense")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Computer Aptitude")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Concentration")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Expert Driver")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Language")[0]
mf.add_ratings([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Lightning Calculator")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Mechanical Aptitude")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Time Sense")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Berserker (Werewolf)")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Code of Honor")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Eidetic Memory")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Inner Strength")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Natural Linguist")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Seldom Sleeps")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Calm Heart")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Iron Will")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Jack-of-all-Trades (Mage and Werewolf)")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Self-Confident")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Untamable")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Compulsion")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Impatient")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Intolerance (Werewolf)")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Nightmares (Werewolf and Changeling)")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Overconfident")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Shy")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Soft-Hearted (Werewolf and Mage)")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Speech Impediment")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Amnesia")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Curiosity")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Pack Mentality")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Phobia (Werewolf and Mage)")[0]
mf.add_ratings([-2, -3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Short Fuse")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Territorial")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Vengeful")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Absent-Minded")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Deranged (Werewolf)")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Driving Goal")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Hatred")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Weak-Willed")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Ability Deficit")[0]
mf.add_ratings([-5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Flashbacks (Werewolf)")[0]
mf.add_ratings([-6])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Family Support (Werewolf)")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Favor")[0]
mf.add_ratings([1, 2, 3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Pitiable")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Camp Goodwill")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Animal Magnetism")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Natural Leader (Werewolf)")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Notable Heritage")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Reputation")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Supporter")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Noted Messenger")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Supernatural Companion")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Conniver")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Dark Secret")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Enemy")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Naive")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Twisted Upbringing")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Camp Enmity")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Gullible")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Persistent Parents")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Notoriety")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Ward")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Hunted (Werewolf)")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Metis Child")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Ancestor Ally")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Moon-Bound")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Spirit Magnet (Werewolf)")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Danger Sense (Werewolf and Mage)")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Lucky")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Natural Channel")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="True Love (Werewolf and Mage)")[0]
mf.add_ratings([4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Immune to Wyrm Emanations")[0]
mf.add_ratings([6])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Silver Tolerance")[0]
mf.add_ratings([7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Banned Transformation")[0]
mf.add_ratings([-1, -2, -3, -4, -5, -6])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Cursed")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Foe from the Past")[0]
mf.add_ratings([-1, -2, -3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Forced Transformation")[0]
mf.add_ratings([-1, -2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Insane Ancestor")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Slip Sideways")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Docile")[0]
mf.add_ratings([-1, -2, -3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Mark of the Predator")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Sign of the Wolf")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Pierced Veil")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Harano Prone")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(werewolf)
mf = MeritFlaw.objects.get_or_create(name="Dark Fate")[0]
mf.add_ratings([-5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Taint of Corruption")[0]
mf.add_ratings([-7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(werewolf)
mf.allowed_types.add(kinfolk)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Feral Appearance")[0]
mf.add_ratings([1])
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Barren/Sterile")[0]
mf.add_ratings([-4])
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Wolf-Sense")[0]
mf.add_ratings([1])
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Gall")[0]
mf.add_ratings([2])
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Recognize werewolf")[0]
mf.add_ratings([3])
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Inferiority Complex")[0]
mf.add_ratings([-1])
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Ulterior Motive")[0]
mf.add_ratings([-2])
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Good Old Boy (or Girl)")[0]
mf.add_ratings([2])
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Outsider")[0]
mf.add_ratings([-2])
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Fetish")[0]
mf.add_ratings([5, 6, 7])
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Gnosis")[0]
mf.add_ratings([5, 6, 7])
mf.allowed_types.add(kinfolk)
mf = MeritFlaw.objects.get_or_create(name="Veiled")[0]
mf.add_ratings([-5])
mf.allowed_types.add(kinfolk)

# M20
mf = MeritFlaw.objects.get_or_create(name="Acute Sense (Mage)")[0]
mf.add_ratings([1, 3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Berserker (Mage)")[0]
mf.add_ratings([4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Dark Triad")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Language", ratings=[1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Stormwarden/Quantum Voyager")[0]
mf.add_ratings([3, 5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Ties")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Too Tough To Die")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="True Faith")[0]
mf.add_ratings([7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Umbral Affinity")[0]
mf.add_ratings([4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Addiction (Mage)")[0]
mf.add_ratings([-1, -3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Construct")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Cursed", ratings=[-1, -2, -3, -4, -5], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Deranged (Mage)")[0]
mf.add_ratings([-3, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Echoes (Mage)")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Enemy", ratings=[-1, -2, -3, -4, -5], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="PTSD")[0]
mf.add_ratings([-2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Stress Atavism")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)

# Book of Secrets
mf = MeritFlaw.objects.get_or_create(name="Alchohol/Drug Tolerance")[0]
mf.add_ratings([1, 2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Ambidextrous", ratings=[1], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Animal Magnetism", ratings=[2], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Artistically Gifted")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Avatar Companion")[0]
mf.add_ratings([7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Bardic Gift")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Burning Aura")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Cast-Iron Stomach")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Catlike Balance")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Celestial Affinity")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Circumspect Avatar")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Clear Sighted")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Cloak of the Seasons")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Code of Honor", ratings=[2], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Common Sense", ratings=[1], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Computer Aptitude", ratings=[1], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Concentration", ratings=[1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Confidence")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Cyclic Magick")[0]
mf.add_ratings([3, -3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Danger Sense", ratings=[3], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Daredevil", ratings=[3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Deathwalker")[0]
mf.add_ratings([4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Dual Affiliation")[0]
mf.add_ratings([7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Eidetic Memory", ratings=[2], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Enchanting Feature")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Expert Driver", ratings=[1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Fae Blood")[0]
mf.add_ratings([4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Faerie Affinity")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Family Support (Mage)")[0]
mf.add_ratings([1, 2, 3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Favor", ratings=[1, 2, 3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Ghoul")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Green Thumb")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Guardian Angel")[0]
mf.add_ratings([6])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Hands of Daedalus")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Hideaway/Safehouse")[0]
mf.add_ratings([2, 4, 6])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Huge Size", ratings=[4], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Hyperflexible")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Hyperfocus")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Hypersensitivity")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Immortal")[0]
mf.add_ratings([5, 7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Inner Knight")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Inner Strength", ratings=[2], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Insensate to Pain")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Iron Will", ratings=[3], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Jack-of-All-Trades", ratings=[3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Judge's Wisdom")[0]
mf.add_ratings([4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Legendary Attributes - Strength")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Legendary Attributes - Dexterity")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Legendary Attributes - Stamina")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Legendary Attributes - Charisma")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Legendary Attributes - Manipulation")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Legendary Attributes - Appearance")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Legendary Attributes - Perception")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Legendary Attributes - Intelligence")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Legendary Attributes - Wits")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Light Sleeper")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Lightning Calculator", ratings=[1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Local Hero")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Loyalty")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Lucky", ratings=[3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Manifest Avatar")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Mark of Favor")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Master of Red Tape")[0]
mf.add_ratings([4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Mechanical Aptitude", ratings=[1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Medium")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Natural Channel", ratings=[3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Natural Leader (Mage)")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Natural Linguist", ratings=[2], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Natural Shapeshifter")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Nephilim/Laham")[0]
mf.add_ratings([7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Nightsight (Mage)")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Nine Lives")[0]
mf.add_ratings([6])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Noble Blood")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Noted Messenger", ratings=[3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Officially Dead")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Oracular Ability")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Parlor Trick")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Perfect Liar")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Physically Impressive", ratings=[2], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Pitiable", ratings=[1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Poison Resistance (Mage)")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Poker Face")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Powerful Ally")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Prestige")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Property")[0]
mf.add_ratings([2, 3, 4, 5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Regal Bearing")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Research Grant")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Rising Star")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Sanctity")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Scientific Mystic/Techgnosi")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Secret Code Language")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Self-Confident", ratings=[5], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Shapechanger Kin")[0]
mf.add_ratings([4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Shattered Avatar")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Socially Networked")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Spark of Life")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Natural - Correspondence")[0]
mf.add_ratings([6])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Natural - Time")[0]
mf.add_ratings([6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Natural - Spirit")[0]
mf.add_ratings([6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Natural - Life")[0]
mf.add_ratings([6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Natural - Matter")[0]
mf.add_ratings([6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Natural - Forces")[0]
mf.add_ratings([6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Natural - Entropy")[0]
mf.add_ratings([6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Natural - Prime")[0]
mf.add_ratings([6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Natural - Mind")[0]
mf.add_ratings([6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Spirit Magnet (Mage)")[0]
mf.add_ratings([3, 4, 5, 6, 7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Spirit Mentor")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sterile")[0]
mf.add_ratings([1, -1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Subculture Insider")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Supernatural Companion", ratings=[3], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Time Sense", ratings=[1], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="True Love", ratings=[4], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Twin Souls")[0]
mf.add_ratings([4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Unaging")[0]
mf.add_ratings([2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Unbondable")[0]
mf.add_ratings([4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Unobtrusive")[0]
mf.add_ratings([1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Ability-Deficit", ratings=[-5], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Absent-Minded", ratings=[-3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Aging")[0]
mf.add_ratings([-2, -4, -6, -8, -10])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Amnesia", ratings=[-2], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Anachronism")[0]
mf.add_ratings([-1, -2, -3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Apprentice")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Bard's Tongue")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Beast Within")[0]
mf.add_ratings([-5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Bedeviled")[0]
mf.add_ratings([-6])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Bigot")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Bizarre Hunger")[0]
mf.add_ratings([-2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Blacklisted")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Blood Magick")[0]
mf.add_ratings([-5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Blood-Hungry Soul")[0]
mf.add_ratings([-2, -3, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Bound")[0]
mf.add_ratings([-5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Branded")[0]
mf.add_ratings([-3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Cast No Shadow Or Reflection")[0]
mf.add_ratings([-1, -2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Catspaw")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Child")[0]
mf.add_ratings([-1, -2, -3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Chronic Depression")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Compulsion", ratings=[-1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Compulsive Speech")[0]
mf.add_ratings([-1, -2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Conflicting Loyalties")[0]
mf.add_ratings([-1, -2, -3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Conniver", ratings=[-1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Crucial Component")[0]
mf.add_ratings([-2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Cultural Other")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Curiosity", ratings=[-2], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Dark Fate", ratings=[-5], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Dark Secret", ratings=[-1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Debts")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Degeneration")[0]
mf.add_ratings([-3, -6, -9])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Demented Eidolon")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Devil's Mark")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Diabolical Mentor")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Discredited")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Dogmatic")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Double Agent")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Driving Goal", ratings=[-3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Easily Intoxicated")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Echo Chamber")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Esoteric Discourse/Technobabbler")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Expendable")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Extreme Kink")[0]
mf.add_ratings([-3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Failure")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Faithless")[0]
mf.add_ratings([-5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Family Issues")[0]
mf.add_ratings([-1, -2, -3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Faulty Enhancements")[0]
mf.add_ratings([-2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Feral Mind")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Fifth Degree")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Flashbacks (Mage and Changeling)")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Gremlin")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Gullible", ratings=[-2], human=True, mage=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Hatred", ratings=[-3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Haunted")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Hero Worship")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Hit List")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Horrific")[0]
mf.add_ratings([-5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Icy")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Immortal Enemy")[0]
mf.add_ratings([-5, -6, -7, -8])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Impatient", ratings=[-1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Impediment")[0]
mf.add_ratings([-1, -2, -3, -4, -5, -6])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Inappropriate")[0]
mf.add_ratings([-1, -2, -3, -4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Infamy")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Insane/Infamous Mentor")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Intemperate")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Jinx/Infernal Contraption")[0]
mf.add_ratings([-2, -3, -4, -5, -6, -7, -8, -9, -10])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Lifesaver")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Locked Vidare")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Mayfly Curse")[0]
mf.add_ratings([-5, -10])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Mental Lock")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Mistaken Identity")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Monstrous", ratings=[-3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Mr. Red Tape")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Naive", ratings=[-1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Narc")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="New Kid")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Nightmares (Mage)")[0]
mf.add_ratings([-1, -3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Notoriety", ratings=[-3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Oathbreaker")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Obsession")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="OCPD")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Offline")[0]
mf.add_ratings([-1, -3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Old Flame")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Overconfident", ratings=[-1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Overextended")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Paranormal Prohibition or Imperative")[0]
mf.add_ratings([-2, -3, -4, -5, -6, -7, -8])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Permanent Paradox Flaw")[0]
mf.add_ratings([-2, -4, -6])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Permanent Wound")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Phobia", ratings=[-2, -3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Phylactery")[0]
mf.add_ratings([-7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Primal Marks")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Probationary Member")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Profiled Appearance")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Prone to Quiet")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Psychic Vampire")[0]
mf.add_ratings([-5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Repulsive Feature")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Rival House")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Rivalry")[0]
mf.add_ratings([-3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Rogue")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Rose-Colored Glasses")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Rotten Liar")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sect Enmity")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Short Fuse", ratings=[-2], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Short (Mage)")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Shy", ratings=[-1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Sleeping with the Enemy")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(changeling)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Soft-Hearted", ratings=[-1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Special Responsibility")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Speech Impediment", ratings=[-1], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Sphere Inept - Correspondence")[0]
mf.add_ratings([-6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Inept - Spirit")[0]
mf.add_ratings([-6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Inept - Time")[0]
mf.add_ratings([-6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Inept - Life")[0]
mf.add_ratings([-6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Inept - Forces")[0]
mf.add_ratings([-6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Inept - Matter")[0]
mf.add_ratings([-6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Inept - Mind")[0]
mf.add_ratings([-6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Inept - Entropy")[0]
mf.add_ratings([-6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Sphere Inept - Prime")[0]
mf.add_ratings([-6])
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Strangeness")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Sympathizer")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
# mf = MeritFlaw.objects.get_or_create(name="Taint of Corruption", ratings=[-7], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Throwback")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Troublemaker")[0]
mf.add_ratings([-2])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Twisted Apprenticeship")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Uncanny")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Vanilla")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Vengeful", ratings=[-2], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Vulnerability")[0]
mf.add_ratings([-1, -2, -3, -4, -5, -6, -7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
# mf = MeritFlaw.objects.get_or_create(name="Ward", ratings=[-3], human=True, mage=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Whimsy")[0]
mf.add_ratings([-1])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Witch-Hunted")[0]
mf.add_ratings([-4])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf.allowed_types.add(companion)

# Book of the Fallen
mf = MeritFlaw.objects.get_or_create(name="Shadow Appeal")[0]
mf.add_ratings([3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Innocuous Aura")[0]
mf.add_ratings([5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Abyssal Mastery")[0]
mf.add_ratings([7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Saint of the Pit")[0]
mf.add_ratings([7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Qlippothic Radiance")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Spectral Presence")[0]
mf.add_ratings([-3])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Abyssal Lunatic")[0]
mf.add_ratings([-5])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)
mf = MeritFlaw.objects.get_or_create(name="Widderslainte")[0]
mf.add_ratings([-7])
mf.allowed_types.add(human)
mf.allowed_types.add(sorcerer)
mf.allowed_types.add(mage)

# C20
mf = MeritFlaw.objects.get_or_create(name="Friendly Face")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Poison Resistance (Changeling)")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Wheelman")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Crack Shot")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Dextrous Toes")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Granite Skin")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Murderous Mien")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Nightsight (Changeling)")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Surreal Beauty")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Increased Pain Threshold")[0]
mf.add_ratings([3])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Perfect Balance (Changeling)")[0]
mf.add_ratings([3])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Prehensile Tongue/Tail")[0]
mf.add_ratings([2, 4])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Sex Appeal")[0]
mf.add_ratings([3])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Huge Size", ratings=[4], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Eidetic Taste")[0]
mf.add_ratings([4])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Blessing of Atlas")[0]
mf.add_ratings([5])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Addiction (Changeling)")[0]
mf.add_ratings([-1, -2, -3])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Allergic")[0]
mf.add_ratings([-1, -2, -3, -4])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Asthma")[0]
mf.add_ratings([-1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Bad Sight (Changeling)")[0]
mf.add_ratings([-1, -3, -6])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Impaired Hearing")[0]
mf.add_ratings([-1, -2, -4])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Short", ratings=[-1], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Twitch")[0]
mf.add_ratings([-1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Deformed")[0]
mf.add_ratings([-2, -3])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Too Human")[0]
mf.add_ratings([-2, -5])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Lame", ratings=[-3], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Parfum de Goat")[0]
mf.add_ratings([-5])
mf.allowed_types.add(changeling)

# mf = MeritFlaw.objects.get_or_create(name="Common Sense", ratings=[1], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Concentration", ratings=[1], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Higher Purpose")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Introspection")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Language", ratings=[1], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Lightning Calculator", ratings=[1], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Mechanical Aptitude", ratings=[1], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Specific Interests")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Eidetic Memory", ratings=[2], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Loyal Heart")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Natural Linguist", ratings=[2], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Iron Will", ratings=[3], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Master Crafsman")[0]
mf.add_ratings([3])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Gut Instincts")[0]
mf.add_ratings([4])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Jack-of-all-Trades (Changeling)")[0]
mf.add_ratings([5])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Beacuse I Think I Can")[0]
mf.add_ratings([6])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Impatient", ratings=[-1], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Nightmares", ratings=[-1], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Amnesia", ratings=[-2], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Curiosity", ratings=[-2], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Phobia (Changeling)")[0]
mf.add_ratings([-2, -4])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Short Fuse", ratings=[-2], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Soft-Hearted (Changeling)")[0]
mf.add_ratings([-2])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Vengeful", ratings=[-2], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Wyld Mind")[0]
mf.add_ratings([-2])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Absent-Minded", ratings=[-3], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Flashbacks", ratings=[-3], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Lifesaver", ratings=[-3], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Weak-Willed", ratings=[-3], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Guilt-Wracked")[0]
mf.add_ratings([-4])
mf.allowed_types.add(changeling)

mf = MeritFlaw.objects.get_or_create(name="Benevolent Patron")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Boon")[0]
mf.add_ratings([1, 2, 3, 4, 5, 6])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Calming Presence")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Good Listener")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="I Know You")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Natural Leader (Changeling)")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Protege")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Your Best Advocate")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Nature's Child")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Reputation", ratings=[2], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Scholar of Others")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Voice of A Songbird")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Sage")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Heir to the Throne")[0]
mf.add_ratings([3])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Fake It")[0]
mf.add_ratings([3])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Rising Star", ratings=[3], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Soul of the Muse")[0]
mf.add_ratings([4])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Trusty Companion")[0]
mf.add_ratings([4])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Dangerous Mentor")[0]
mf.add_ratings([-1])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Dark Secret", ratings=[-1], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Enemy", ratings=[-1, -2, -3, -4, -5], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Insubordinate")[0]
mf.add_ratings([-1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Intolerance (Changeling)")[0]
mf.add_ratings([-2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Foul Mouth")[0]
mf.add_ratings([-2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Possessive")[0]
mf.add_ratings([-2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Shrinking Violet")[0]
mf.add_ratings([-2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Fallen Noble")[0]
mf.add_ratings([-3])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Recruitment Target")[0]
mf.add_ratings([-3])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Sleeping With the Enemy", ratings=[-3], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Ward", ratings=[-3], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Indecisive")[0]
mf.add_ratings([-3])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Hunted (Changeling)")[0]
mf.add_ratings([-4, -5])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="On Probation")[0]
mf.add_ratings([-4])
mf.allowed_types.add(changeling)

mf = MeritFlaw.objects.get_or_create(name="Faerie Eternity")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="True Love (Changeling)")[0]
mf.add_ratings([1])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Danger Sense (Changeling)")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Medium", ratings=[2], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Poetic Heart")[0]
mf.add_ratings([2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Animalistic Favor")[0]
mf.add_ratings([3, 4, 5])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Lucky", ratings=[3], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Blood of the Wolf")[0]
mf.add_ratings([4])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Iron Resistance")[0]
mf.add_ratings([4])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Art Affinity")[0]
mf.add_ratings([5])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Living Legend")[0]
mf.add_ratings([5])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Regeneration")[0]
mf.add_ratings([7])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Bard's Tongue", ratings=[-1], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Changeling's Eyes")[0]
mf.add_ratings([-1])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Cursed", ratings=[-1, -2, -3, -4, -5], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Geas")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Oathbound")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Slipped Seeming")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Bizarre Quality")[0]
mf.add_ratings([-2])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Echoes (Changeling)")[0]
mf.add_ratings([-2, -3, -4, -5])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Winged")[0]
mf.add_ratings([-2, 4])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Cleared Mists")[0]
mf.add_ratings([-3])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Haunted", ratings=[-3], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Iron Allergy")[0]
mf.add_ratings([-3, -4, -5])
mf.allowed_types.add(changeling)
mf = MeritFlaw.objects.get_or_create(name="Chimerical Magnet")[0]
mf.add_ratings([-5])
mf.allowed_types.add(changeling)
# mf = MeritFlaw.objects.get_or_create(name="Dark Fate", ratings=[-5], changeling=True)[0]
# mf = MeritFlaw.objects.get_or_create(name="Psychic Vampire", ratings=[-5], changeling=True)[0]
mf = MeritFlaw.objects.get_or_create(name="Sidhe's Curse")[0]
mf.add_ratings([-5])
mf.allowed_types.add(changeling)


mf = MeritFlaw.objects.get_or_create(name="Cyclic Node")[0]
mf.add_ratings([1, 2])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Famous Node")[0]
mf.add_ratings([1, 2, 3, 4, 5])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Focus Locked")[0]
mf.add_ratings([1, 2, 3])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Functioning Caern")[0]
mf.add_ratings([2])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Functioning Freehold")[0]
mf.add_ratings([2])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Functioning Haunt")[0]
mf.add_ratings([2])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Genius Locus")[0]
mf.add_ratings([3, 5])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Manifestation")[0]
mf.add_ratings([1, 2, 3, 4, 5])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Shallowing")[0]
mf.add_ratings([2, -2])
mf.allowed_types.add(node)
for s in Sphere.objects.all():
    mf = MeritFlaw.objects.get_or_create(name=f"Sphere Attuned ({s.name})")[0]
    mf.add_ratings([2])
    mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Spirit Guardian")[0]
mf.add_ratings([1, 2, 3, 4, 5])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Corrupted")[0]
mf.add_ratings([-4])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Dangerous Energies")[0]
mf.add_ratings([-3])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Enemy")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Former Caern")[0]
mf.add_ratings([-2])
mf.allowed_types.add(node)
mf.add_ratings([-2])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Former Freehold")[0]
mf.add_ratings([-2])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Former Haunt")[0]
mf.add_ratings([-2])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Infamous Node")[0]
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(node)
mf = MeritFlaw.objects.get_or_create(name="Isolated Node")[0]
mf.add_ratings([-2])
mf.allowed_types.add(node)


mf = MeritFlaw.objects.get_or_create(name="Alpha")[0].add_source(
    "Gods and Monsters", 195
)
mf.add_ratings([2])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="My Master is My Slave")[0].add_source(
    "Gods and Monsters", 195
)
mf.add_ratings([2])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Alien Impression")[0].add_source(
    "Gods and Monsters", 195
)
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Animal")[0].add_source(
    "Gods and Monsters", 197
)
mf.add_ratings([-2])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Aura")[0].add_source(
    "Gods and Monsters", 202
)
mf.add_ratings([-3])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Beta")[0].add_source(
    "Gods and Monsters", 197
)
mf.add_ratings([-1])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Broken")[0].add_source(
    "Gods and Monsters", 197
)
mf.add_ratings([-5])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Limbless")[0].add_source(
    "Gods and Monsters", 197
)
mf.add_ratings([-5])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Power Source")[0].add_source(
    "Gods and Monsters", 198
)
mf.add_ratings([-1, -2, -3, -4, -5])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="No Dextrous Limbs")[0].add_source(
    "Gods and Monsters", 197
)
mf.add_ratings([-4])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Omega")[0].add_source(
    "Gods and Monsters", 197
)
mf.add_ratings([-4])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Ungainly Fingers")[0].add_source(
    "Gods and Monsters", 200
)
mf.add_ratings([-2])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Weak Spot")[0].add_source(
    "Gods and Monsters", 200
)
mf.add_ratings([-3])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Thaumivore")[0].add_source(
    "Gods and Monsters", 199
)
mf.add_ratings([-5])
mf.allowed_types.add(companion)
mf = MeritFlaw.objects.get_or_create(name="Unbelief")[0].add_source(
    "Gods and Monsters", 199
)
mf.add_ratings([-3, -5, -8])
mf.allowed_types.add(companion)

# M20 Sorcerer
mf = MeritFlaw.objects.get_or_create(name="Isolated Upbringing")[0].add_source(
    "M20 Sorcerer", 106
)
mf.add_ratings([-2])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Innocent")[0].add_source("M20 Sorcerer", 106)
mf.add_ratings([1])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Psychic Awareness")[0].add_source(
    "M20 Sorcerer", 106
)
mf.add_ratings([3])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Flow of Ki")[0].add_source(
    "M20 Sorcerer", 106
)
mf.add_ratings([3])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Force of Spirit")[0].add_source(
    "M20 Sorcerer", 107
)
mf.add_ratings([2])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Strength of Psyche")[0].add_source(
    "M20 Sorcerer", 107
)
mf.add_ratings([2])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Detached")[0].add_source("M20 Sorcerer", 107)
mf.add_ratings([4])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Black and White")[0].add_source(
    "M20 Sorcerer", 107
)
mf.add_ratings([-1])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Pacifist")[0].add_source("M20 Sorcerer", 107)
mf.add_ratings([-5])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Style Sleeper")[0].add_source(
    "M20 Sorcerer", 107
)
mf.add_ratings([2])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Twin Link")[0].add_source(
    "M20 Sorcerer", 107
)
mf.add_ratings([4, 6])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Wild Talent")[0].add_source(
    "M20 Sorcerer", 107
)
mf.add_ratings([4, 3, 2, 1, 0, -1, -2, -3, -4])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Path Natural")[0].add_source(
    "M20 Sorcerer", 108
)
mf.add_ratings([5])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Psychic Feedback")[0].add_source(
    "M20 Sorcerer", 108
)
mf.add_ratings([-1, -2, -6])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Psi Focus")[0].add_source(
    "M20 Sorcerer", 108
)
mf.add_ratings([-3, -4, -5])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Path Inept")[0].add_source(
    "M20 Sorcerer", 108
)
mf.add_ratings([-5])
mf.allowed_types.add(sorcerer)
mf = MeritFlaw.objects.get_or_create(name="Ritual Sleeper")[0].add_source(
    "M20 Sorcerer", 108
)
mf.add_ratings([-5])
mf.allowed_types.add(sorcerer)

mf = MeritFlaw.objects.get_or_create(name="Scarred Avatar")[0].add_source(
    "Lore of the Traditions", 97
)
mf.allowed_types.add(mage)
mf.add_ratings([-2, -4])


MeritFlaw.objects.get_or_create(name="Ability Deficit")[0].add_source(
    "Book of Secrets", 53
)
MeritFlaw.objects.get_or_create(name="Absent-Minded")[0].add_source(
    "Book of Secrets", 50
)
MeritFlaw.objects.get_or_create(name="Abyssal Lunatic")[0].add_source(
    "Book of the Fallen", 119
)
MeritFlaw.objects.get_or_create(name="Abyssal Mastery")[0].add_source(
    "Book of the Fallen", 117
)
MeritFlaw.objects.get_or_create(name="Acute Sense (Mage)")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 642
)
MeritFlaw.objects.get_or_create(name="Addiction (Mage)")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 646
)
MeritFlaw.objects.get_or_create(name="Aging")[0].add_source("Book of Secrets", 40)
MeritFlaw.objects.get_or_create(name="Alchohol/Drug Tolerance")[0].add_source(
    "Book of Secrets", 35
)
MeritFlaw.objects.get_or_create(name="Alien Impression")[0].add_source(
    "Gods and Monsters", 195
)
MeritFlaw.objects.get_or_create(name="Alpha")[0].add_source("Gods and Monsters", 195)
MeritFlaw.objects.get_or_create(name="Ambidextrous")[0].add_source(
    "Book of Secrets", 36
)
MeritFlaw.objects.get_or_create(name="Amnesia")[0].add_source("Book of Secrets", 48)
MeritFlaw.objects.get_or_create(name="Anachronism")[0].add_source("Book of Secrets", 81)
MeritFlaw.objects.get_or_create(name="Animal")[0].add_source("Gods and Monsters", 197)
MeritFlaw.objects.get_or_create(name="Animal Magnetism")[0].add_source(
    "Book of Secrets", 54
)
MeritFlaw.objects.get_or_create(name="Apprentice")[0].add_source("Book of Secrets", 81)
MeritFlaw.objects.get_or_create(name="Artistically Gifted")[0].add_source(
    "Book of Secrets", 43
)
MeritFlaw.objects.get_or_create(name="Aura")[0].add_source("Gods and Monsters", 202)
MeritFlaw.objects.get_or_create(name="Avatar Companion")[0].add_source(
    "Book of Secrets", 79
)
MeritFlaw.objects.get_or_create(name="Bard's Tongue")[0].add_source(
    "Book of Secrets", 82
)
MeritFlaw.objects.get_or_create(name="Bardic Gift")[0].add_source("Book of Secrets", 69)
MeritFlaw.objects.get_or_create(name="Beast Within")[0].add_source(
    "Book of Secrets", 92
)
MeritFlaw.objects.get_or_create(name="Bedeviled")[0].add_source("Book of Secrets", 94)
MeritFlaw.objects.get_or_create(name="Berserker (Mage)")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 644
)
MeritFlaw.objects.get_or_create(name="Beta")[0].add_source("Gods and Monsters", 197)
MeritFlaw.objects.get_or_create(name="Bigot")[0].add_source("Book of Secrets", 50)
MeritFlaw.objects.get_or_create(name="Bizarre Hunger")[0].add_source(
    "Book of Secrets", 87
)
MeritFlaw.objects.get_or_create(name="Black and White")[0].add_source(
    "M20 Sorcerer", 107
)
MeritFlaw.objects.get_or_create(name="Blacklisted")[0].add_source("Book of Secrets", 59)
MeritFlaw.objects.get_or_create(name="Blood Magick")[0].add_source(
    "Book of Secrets", 92
)
MeritFlaw.objects.get_or_create(name="Blood-Hungry Soul")[0].add_source(
    "Book of Secrets", 87
)
MeritFlaw.objects.get_or_create(name="Bound")[0].add_source("Book of Secrets", 92)
MeritFlaw.objects.get_or_create(name="Branded")[0].add_source("Book of Secrets", 89)
MeritFlaw.objects.get_or_create(name="Broken")[0].add_source("Gods and Monsters", 197)
MeritFlaw.objects.get_or_create(name="Burning Aura")[0].add_source(
    "Book of Secrets", 68
)
MeritFlaw.objects.get_or_create(name="Cast No Shadow Or Reflection")[0].add_source(
    "Book of Secrets", 82
)
MeritFlaw.objects.get_or_create(name="Cast-Iron Stomach")[0].add_source(
    "Book of Secrets", 36
)
MeritFlaw.objects.get_or_create(name="Catlike Balance")[0].add_source(
    "Book of Secrets", 36
)
MeritFlaw.objects.get_or_create(name="Catspaw")[0].add_source("Book of Secrets", 64)
MeritFlaw.objects.get_or_create(name="Celestial Affinity")[0].add_source(
    "Book of Secrets", 70
)
MeritFlaw.objects.get_or_create(name="Child")[0].add_source("Book of Secrets", 39)
MeritFlaw.objects.get_or_create(name="Chronic Depression")[0].add_source(
    "Book of Secrets", 51
)
MeritFlaw.objects.get_or_create(name="Circumspect Avatar")[0].add_source(
    "Book of Secrets", 69
)
MeritFlaw.objects.get_or_create(name="Clear Sighted")[0].add_source(
    "Book of Secrets", 75
)
MeritFlaw.objects.get_or_create(name="Cloak of the Seasons")[0].add_source(
    "Book of Secrets", 70
)
MeritFlaw.objects.get_or_create(name="Code of Honor")[0].add_source(
    "Book of Secrets", 44
)
MeritFlaw.objects.get_or_create(name="Common Sense")[0].add_source(
    "Book of Secrets", 43
)
MeritFlaw.objects.get_or_create(name="Compulsion")[0].add_source("Book of Secrets", 46)
MeritFlaw.objects.get_or_create(name="Compulsive Speech")[0].add_source(
    "Book of Secrets", 59
)
MeritFlaw.objects.get_or_create(name="Computer Aptitude")[0].add_source(
    "Book of Secrets", 43
)
MeritFlaw.objects.get_or_create(name="Concentration")[0].add_source(
    "Book of Secrets", 43
)
MeritFlaw.objects.get_or_create(name="Confidence")[0].add_source("Book of Secrets", 54)
MeritFlaw.objects.get_or_create(name="Conflicting Loyalties")[0].add_source(
    "Book of Secrets", 59
)
MeritFlaw.objects.get_or_create(name="Conniver")[0].add_source("Book of Secrets", 60)
MeritFlaw.objects.get_or_create(name="Construct")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 647
)
MeritFlaw.objects.get_or_create(name="Corrupted")[0].add_source("Sources of Magick", 22)
MeritFlaw.objects.get_or_create(name="Crucial Component")[0].add_source(
    "Book of Secrets", 87
)
MeritFlaw.objects.get_or_create(name="Cultural Other")[0].add_source(
    "Book of Secrets", 60
)
MeritFlaw.objects.get_or_create(name="Curiosity")[0].add_source("Book of Secrets", 48)
MeritFlaw.objects.get_or_create(name="Cursed")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 646
)
MeritFlaw.objects.get_or_create(name="Cyclic Magick")[0].add_source(
    "Book of Secrets", 70
)
MeritFlaw.objects.get_or_create(name="Cyclic Node")[0].add_source(
    "Sources of Magick", 20
)
MeritFlaw.objects.get_or_create(name="Danger Sense (Werewolf and Mage)")[0].add_source(
    "Book of Secrets", 70
)
MeritFlaw.objects.get_or_create(name="Dangerous Energies")[0].add_source(
    "Sources of Magick", 22
)
MeritFlaw.objects.get_or_create(name="Daredevil")[0].add_source("Book of Secrets", 38)
MeritFlaw.objects.get_or_create(name="Dark Fate")[0].add_source("Book of Secrets", 92)
MeritFlaw.objects.get_or_create(name="Dark Secret")[0].add_source("Book of Secrets", 61)
MeritFlaw.objects.get_or_create(name="Dark Triad")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 643
)
MeritFlaw.objects.get_or_create(name="Deathwalker")[0].add_source("Book of Secrets", 74)
MeritFlaw.objects.get_or_create(name="Debts")[0].add_source("Book of Secrets", 61)
MeritFlaw.objects.get_or_create(name="Degeneration")[0].add_source(
    "Book of Secrets", 41
)
MeritFlaw.objects.get_or_create(name="Demented Eidolon")[0].add_source(
    "Book of Secrets", 89
)
MeritFlaw.objects.get_or_create(name="Deranged (Mage)")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 648
)
MeritFlaw.objects.get_or_create(name="Detached")[0].add_source("M20 Sorcerer", 107)
MeritFlaw.objects.get_or_create(name="Devil's Mark")[0].add_source(
    "Book of Secrets", 83
)
MeritFlaw.objects.get_or_create(name="Diabolical Mentor")[0].add_source(
    "Book of Secrets", 64
)
x = MeritFlaw.objects.get_or_create(name="Dilettante")[0].add_source(
    "The Rich Bastard's Guide to Magick", 44
)
x.add_ratings([1, 3])
x.allowed_types.add(mage)
x.allowed_types.add(human)
x.allowed_types.add(sorcerer)
MeritFlaw.objects.get_or_create(name="Discredited")[0].add_source("Book of Secrets", 62)
MeritFlaw.objects.get_or_create(name="Dogmatic")[0].add_source("Book of Secrets", 64)
MeritFlaw.objects.get_or_create(name="Double Agent")[0].add_source(
    "Book of Secrets", 65
)
MeritFlaw.objects.get_or_create(name="Driving Goal")[0].add_source(
    "Book of Secrets", 51
)
MeritFlaw.objects.get_or_create(name="Dual Affiliation")[0].add_source(
    "Book of Secrets", 79
)
MeritFlaw.objects.get_or_create(name="Easily Intoxicated")[0].add_source(
    "Book of Secrets", 40
)
x = MeritFlaw.objects.get_or_create(name="Eccentric")[0].add_source(
    "The Rich Bastard's Guide to Magick", 44
)
x.add_ratings([-1, -2])
x.allowed_types.add(mage)
x.allowed_types.add(human)
x.allowed_types.add(sorcerer)
MeritFlaw.objects.get_or_create(name="Echo Chamber")[0].add_source(
    "Book of Secrets", 66
)
MeritFlaw.objects.get_or_create(name="Echoes (Mage)")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 646
)
MeritFlaw.objects.get_or_create(name="Eidetic Memory")[0].add_source(
    "Book of Secrets", 44
)
MeritFlaw.objects.get_or_create(name="Enchanting Feature")[0].add_source(
    "Book of Secrets", 37
)
MeritFlaw.objects.get_or_create(name="Enemy")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 647
)
MeritFlaw.objects.get_or_create(name="Esoteric Discourse/Technobabbler")[0].add_source(
    "Book of Secrets", 62
)
MeritFlaw.objects.get_or_create(name="Expendable")[0].add_source("Book of Secrets", 65)
MeritFlaw.objects.get_or_create(name="Expert Driver")[0].add_source(
    "Book of Secrets", 44
)
MeritFlaw.objects.get_or_create(name="Extreme Kink")[0].add_source(
    "Book of Secrets", 51
)
MeritFlaw.objects.get_or_create(name="Fae Blood")[0].add_source("Book of Secrets", 74)
MeritFlaw.objects.get_or_create(name="Faerie Affinity")[0].add_source(
    "Book of Secrets", 69
)
MeritFlaw.objects.get_or_create(name="Failure")[0].add_source("Book of Secrets", 65)
MeritFlaw.objects.get_or_create(name="Faithless")[0].add_source("Book of Secrets", 93)
MeritFlaw.objects.get_or_create(name="Family Issues")[0].add_source(
    "Book of Secrets", 62
)
MeritFlaw.objects.get_or_create(name="Family Support (Mage)")[0].add_source(
    "Book of Secrets", 53
)
MeritFlaw.objects.get_or_create(name="Famous Node")[0].add_source(
    "Sources of Magick", 20
)
MeritFlaw.objects.get_or_create(name="Faulty Enhancements")[0].add_source(
    "Book of Secrets", 88
)
MeritFlaw.objects.get_or_create(name="Favor")[0].add_source("Book of Secrets", 54)
MeritFlaw.objects.get_or_create(name="Feral Mind")[0].add_source("Book of Secrets", 52)
MeritFlaw.objects.get_or_create(name="Fifth Degree")[0].add_source(
    "Book of Secrets", 68
)
x = MeritFlaw.objects.get_or_create(name="Financial Partner")[0].add_source(
    "The Rich Bastard's Guide to Magick", 45
)
x.add_ratings([-2, -3, -4])
x.allowed_types.add(mage)
x.allowed_types.add(human)
x.allowed_types.add(sorcerer)

MeritFlaw.objects.get_or_create(name="Flashbacks (Mage and Changeling)")[0].add_source(
    "Book of Secrets", 52
)
MeritFlaw.objects.get_or_create(name="Flow of Ki")[0].add_source("M20 Sorcerer", 106)
MeritFlaw.objects.get_or_create(name="Focus Locked")[0].add_source(
    "Sources of Magick", 20
)
MeritFlaw.objects.get_or_create(name="Former Caern")[0].add_source(
    "Sources of Magick", 23
)
MeritFlaw.objects.get_or_create(name="Former Freehold")[0].add_source(
    "Sources of Magick", 23
)
MeritFlaw.objects.get_or_create(name="Former Haunt")[0].add_source(
    "Sources of Magick", 23
)
MeritFlaw.objects.get_or_create(name="Functioning Caern")[0].add_source(
    "Sources of Magick", 21
)
MeritFlaw.objects.get_or_create(name="Functioning Freehold")[0].add_source(
    "Sources of Magick", 21
)
MeritFlaw.objects.get_or_create(name="Functioning Haunt")[0].add_source(
    "Sources of Magick", 21
)
MeritFlaw.objects.get_or_create(name="Geas")[0].add_source("Book of Secrets", 83)
MeritFlaw.objects.get_or_create(name="Genius Locus")[0].add_source(
    "Sources of Magick", 21
)
MeritFlaw.objects.get_or_create(name="Ghoul")[0].add_source("Book of Secrets", 75)
MeritFlaw.objects.get_or_create(name="Green Thumb")[0].add_source("Book of Secrets", 68)
MeritFlaw.objects.get_or_create(name="Gremlin")[0].add_source("Book of Secrets", 84)
MeritFlaw.objects.get_or_create(name="Guardian Angel")[0].add_source(
    "Book of Secrets", 78
)
MeritFlaw.objects.get_or_create(name="Gullible")[0].add_source("Book of Secrets", 65)
MeritFlaw.objects.get_or_create(name="Hands of Daedalus")[0].add_source(
    "Book of Secrets", 70
)
MeritFlaw.objects.get_or_create(name="Hatred")[0].add_source("Book of Secrets", 52)
MeritFlaw.objects.get_or_create(name="Haunted")[0].add_source("Book of Secrets", 90)
MeritFlaw.objects.get_or_create(name="Hero Worship")[0].add_source(
    "Book of Secrets", 46
)
MeritFlaw.objects.get_or_create(name="Hideaway/Safehouse")[0].add_source(
    "Book of Secrets", 55
)
MeritFlaw.objects.get_or_create(name="Hit List")[0].add_source("Book of Secrets", 67)
MeritFlaw.objects.get_or_create(name="Horrific")[0].add_source("Book of Secrets", 41)
MeritFlaw.objects.get_or_create(name="Huge Size")[0].add_source("Book of Secrets", 38)
MeritFlaw.objects.get_or_create(name="Hyperflexible")[0].add_source(
    "Book of Secrets", 36
)
MeritFlaw.objects.get_or_create(name="Hyperfocus")[0].add_source("Book of Secrets", 45)
MeritFlaw.objects.get_or_create(name="Hypersensitivity")[0].add_source(
    "Book of Secrets", 38
)
MeritFlaw.objects.get_or_create(name="Icy")[0].add_source("Book of Secrets", 48)
MeritFlaw.objects.get_or_create(name="Immortal")[0].add_source("Book of Secrets", 76)
MeritFlaw.objects.get_or_create(name="Immortal Enemy")[0].add_source(
    "Book of Secrets", 93
)
MeritFlaw.objects.get_or_create(name="Impatient")[0].add_source("Book of Secrets", 46)
MeritFlaw.objects.get_or_create(name="Impediment")[0].add_source("Book of Secrets", 39)
MeritFlaw.objects.get_or_create(name="Inappropriate")[0].add_source(
    "Book of Secrets", 46
)
MeritFlaw.objects.get_or_create(name="Infamous Node")[0].add_source(
    "Sources of Magick", 23
)
MeritFlaw.objects.get_or_create(name="Infamy")[0].add_source("Book of Secrets", 62)
MeritFlaw.objects.get_or_create(name="Inner Knight")[0].add_source(
    "Book of Secrets", 77
)
MeritFlaw.objects.get_or_create(name="Inner Strength")[0].add_source(
    "Book of Secrets", 45
)
MeritFlaw.objects.get_or_create(name="Innocent")[0].add_source("M20 Sorcerer", 106)
MeritFlaw.objects.get_or_create(name="Innocuous Aura")[0].add_source(
    "Book of the Fallen", 117
)
MeritFlaw.objects.get_or_create(name="Insane/Infamous Mentor")[0].add_source(
    "Book of Secrets", 63
)
MeritFlaw.objects.get_or_create(name="Insensate to Pain")[0].add_source(
    "Book of Secrets", 38
)
MeritFlaw.objects.get_or_create(name="Intemperate")[0].add_source("Book of Secrets", 49)
MeritFlaw.objects.get_or_create(name="Iron Will")[0].add_source("Book of Secrets", 45)
MeritFlaw.objects.get_or_create(name="Isolated Node")[0].add_source(
    "Sources of Magick", 23
)
MeritFlaw.objects.get_or_create(name="Isolated Upbringing")[0].add_source(
    "M20 Sorcerer", 106
)
MeritFlaw.objects.get_or_create(name="Jack-of-all-Trades (Mage and Werewolf)")[
    0
].add_source("Book of Secrets", 45)
MeritFlaw.objects.get_or_create(name="Jinx/Infernal Contraption")[0].add_source(
    "Book of Secrets", 88
)
MeritFlaw.objects.get_or_create(name="Judge's Wisdom")[0].add_source(
    "Book of Secrets", 46
)
MeritFlaw.objects.get_or_create(name="Language")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 643
)
MeritFlaw.objects.get_or_create(name="Legendary Attributes - Appearance")[0].add_source(
    "Book of Secrets", 77
)
MeritFlaw.objects.get_or_create(name="Legendary Attributes - Charisma")[0].add_source(
    "Book of Secrets", 77
)
MeritFlaw.objects.get_or_create(name="Legendary Attributes - Dexterity")[0].add_source(
    "Book of Secrets", 77
)
MeritFlaw.objects.get_or_create(name="Legendary Attributes - Intelligence")[
    0
].add_source("Book of Secrets", 77)
MeritFlaw.objects.get_or_create(name="Legendary Attributes - Manipulation")[
    0
].add_source("Book of Secrets", 77)
MeritFlaw.objects.get_or_create(name="Legendary Attributes - Perception")[0].add_source(
    "Book of Secrets", 77
)
MeritFlaw.objects.get_or_create(name="Legendary Attributes - Stamina")[0].add_source(
    "Book of Secrets", 77
)
MeritFlaw.objects.get_or_create(name="Legendary Attributes - Strength")[0].add_source(
    "Book of Secrets", 77
)
MeritFlaw.objects.get_or_create(name="Legendary Attributes - Wits")[0].add_source(
    "Book of Secrets", 77
)
MeritFlaw.objects.get_or_create(name="Lifesaver")[0].add_source("Book of Secrets", 52)
MeritFlaw.objects.get_or_create(name="Light Sleeper")[0].add_source(
    "Book of Secrets", 36
)
MeritFlaw.objects.get_or_create(name="Lightning Calculator")[0].add_source(
    "Book of Secrets", 44
)
MeritFlaw.objects.get_or_create(name="Limbless")[0].add_source("Gods and Monsters", 197)
MeritFlaw.objects.get_or_create(name="Local Hero")[0].add_source("Book of Secrets", 58)
MeritFlaw.objects.get_or_create(name="Locked Vidare")[0].add_source(
    "Book of Secrets", 85
)
MeritFlaw.objects.get_or_create(name="Loyalty")[0].add_source("Book of Secrets", 53)
MeritFlaw.objects.get_or_create(name="Lucky")[0].add_source("Book of Secrets", 71)
MeritFlaw.objects.get_or_create(name="Manifest Avatar")[0].add_source(
    "Book of Secrets", 71
)
MeritFlaw.objects.get_or_create(name="Manifestation")[0].add_source(
    "Sources of Magick", 22
)
MeritFlaw.objects.get_or_create(name="Mark of Favor")[0].add_source(
    "Book of Secrets", 71
)
MeritFlaw.objects.get_or_create(name="Master of Red Tape")[0].add_source(
    "Book of Secrets", 58
)
MeritFlaw.objects.get_or_create(name="Mayfly Curse")[0].add_source(
    "Book of Secrets", 42
)
MeritFlaw.objects.get_or_create(name="Mechanical Aptitude")[0].add_source(
    "Book of Secrets", 44
)
MeritFlaw.objects.get_or_create(name="Medium")[0].add_source("Book of Secrets", 69)
MeritFlaw.objects.get_or_create(name="Mental Lock")[0].add_source("Book of Secrets", 47)
MeritFlaw.objects.get_or_create(name="Mistaken Identity")[0].add_source(
    "Book of Secrets", 63
)
MeritFlaw.objects.get_or_create(name="Monstrous")[0].add_source("Book of Secrets", 41)
MeritFlaw.objects.get_or_create(name="Mr. Red Tape")[0].add_source(
    "Book of Secrets", 67
)
MeritFlaw.objects.get_or_create(name="My Master is My Slave")[0].add_source(
    "Gods and Monsters", 195
)
MeritFlaw.objects.get_or_create(name="Naive")[0].add_source("Book of Secrets", 63)
MeritFlaw.objects.get_or_create(name="Narc")[0].add_source("Book of Secrets", 65)
MeritFlaw.objects.get_or_create(name="Natural Channel")[0].add_source(
    "Book of Secrets", 72
)
MeritFlaw.objects.get_or_create(name="Natural Leader (Mage)")[0].add_source(
    "Book of Secrets", 56
)
MeritFlaw.objects.get_or_create(name="Natural Linguist")[0].add_source(
    "Book of Secrets", 45
)
MeritFlaw.objects.get_or_create(name="Natural Shapeshifter")[0].add_source(
    "Book of Secrets", 72
)
MeritFlaw.objects.get_or_create(name="Nephilim/Laham")[0].add_source(
    "Book of Secrets", 80
)
MeritFlaw.objects.get_or_create(name="New Kid")[0].add_source("Book of Secrets", 63)
MeritFlaw.objects.get_or_create(name="Nightmares (Mage)")[0].add_source(
    "Book of Secrets", 47
)
MeritFlaw.objects.get_or_create(name="Nightsight (Mage)")[0].add_source(
    "Book of Secrets", 38
)
MeritFlaw.objects.get_or_create(name="Nine Lives")[0].add_source("Book of Secrets", 79)
MeritFlaw.objects.get_or_create(name="No Dextrous Limbs")[0].add_source(
    "Gods and Monsters", 197
)
MeritFlaw.objects.get_or_create(name="Noble Blood")[0].add_source("Book of Secrets", 36)
MeritFlaw.objects.get_or_create(name="Noted Messenger")[0].add_source(
    "Book of Secrets", 58
)
MeritFlaw.objects.get_or_create(name="Notoriety")[0].add_source("Book of Secrets", 65)
MeritFlaw.objects.get_or_create(name="Oathbreaker")[0].add_source("Book of Secrets", 90)
MeritFlaw.objects.get_or_create(name="Obsession")[0].add_source("Book of Secrets", 49)
MeritFlaw.objects.get_or_create(name="OCPD")[0].add_source("Book of Secrets", 53)
MeritFlaw.objects.get_or_create(name="Officially Dead")[0].add_source(
    "Book of Secrets", 56
)
MeritFlaw.objects.get_or_create(name="Offline")[0].add_source("Book of Secrets", 63)
MeritFlaw.objects.get_or_create(name="Old Flame")[0].add_source("Book of Secrets", 65)
MeritFlaw.objects.get_or_create(name="Omega")[0].add_source("Gods and Monsters", 197)
MeritFlaw.objects.get_or_create(name="Oracular Ability")[0].add_source(
    "Book of Secrets", 72
)
MeritFlaw.objects.get_or_create(name="Overconfident")[0].add_source(
    "Book of Secrets", 48
)
MeritFlaw.objects.get_or_create(name="Overextended")[0].add_source(
    "Book of Secrets", 67
)
MeritFlaw.objects.get_or_create(name="Pacifist")[0].add_source("M20 Sorcerer", 107)
MeritFlaw.objects.get_or_create(name="Paranormal Prohibition or Imperative")[
    0
].add_source("Book of Secrets", 83)
MeritFlaw.objects.get_or_create(name="Parlor Trick")[0].add_source(
    "Book of Secrets", 73
)
MeritFlaw.objects.get_or_create(name="Path Inept")[0].add_source("M20 Sorcerer", 108)
MeritFlaw.objects.get_or_create(name="Path Natural")[0].add_source("M20 Sorcerer", 108)
MeritFlaw.objects.get_or_create(name="Perfect Liar")[0].add_source(
    "Book of Secrets", 56
)
MeritFlaw.objects.get_or_create(name="Permanent Paradox Flaw")[0].add_source(
    "Book of Secrets", 89
)
MeritFlaw.objects.get_or_create(name="Permanent Wound")[0].add_source(
    "Book of Secrets", 41
)
MeritFlaw.objects.get_or_create(name="Phobia (Werewolf and Mage)")[0].add_source(
    "Book of Secrets", 50
)
MeritFlaw.objects.get_or_create(name="Phylactery")[0].add_source("Book of Secrets", 94)
MeritFlaw.objects.get_or_create(name="Physically Impressive")[0].add_source(
    "Book of Secrets", 37
)
MeritFlaw.objects.get_or_create(name="Pitiable")[0].add_source("Book of Secrets", 54)
MeritFlaw.objects.get_or_create(name="Poison Resistance (Mage)")[0].add_source(
    "Book of Secrets", 37
)
MeritFlaw.objects.get_or_create(name="Poker Face")[0].add_source("Book of Secrets", 38)
MeritFlaw.objects.get_or_create(name="Power Source")[0].add_source(
    "Gods and Monsters", 198
)
MeritFlaw.objects.get_or_create(name="Powerful Ally")[0].add_source(
    "Book of Secrets", 77
)
MeritFlaw.objects.get_or_create(name="Prestige")[0].add_source("Book of Secrets", 56)
x = MeritFlaw.objects.get_or_create(name="Prestigious Mentor")[0].add_source(
    "Book of Secrets", 54
)
x.add_ratings([1])
x.allowed_types.add(mage)
x.allowed_types.add(human)
x.allowed_types.add(sorcerer)

MeritFlaw.objects.get_or_create(name="Primal Marks")[0].add_source(
    "Book of Secrets", 90
)
MeritFlaw.objects.get_or_create(name="Probationary Member")[0].add_source(
    "Book of Secrets", 68
)
MeritFlaw.objects.get_or_create(name="Profiled Appearance")[0].add_source(
    "Book of Secrets", 40
)
MeritFlaw.objects.get_or_create(name="Prone to Quiet")[0].add_source(
    "Book of Secrets", 91
)
MeritFlaw.objects.get_or_create(name="Property")[0].add_source("Book of Secrets", 56)
MeritFlaw.objects.get_or_create(name="Psi Focus")[0].add_source("M20 Sorcerer", 108)
MeritFlaw.objects.get_or_create(name="Psychic Awareness")[0].add_source(
    "M20 Sorcerer", 106
)
MeritFlaw.objects.get_or_create(name="Psychic Feedback")[0].add_source(
    "M20 Sorcerer", 108
)
MeritFlaw.objects.get_or_create(name="Psychic Vampire")[0].add_source(
    "Book of Secrets", 93
)
MeritFlaw.objects.get_or_create(name="PTSD")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 647
)
MeritFlaw.objects.get_or_create(name="Qlippothic Radiance")[0].add_source(
    "Book of the Fallen", 119
)
MeritFlaw.objects.get_or_create(name="Regal Bearing")[0].add_source(
    "Book of Secrets", 54
)
MeritFlaw.objects.get_or_create(name="Repulsive Feature")[0].add_source(
    "Book of Secrets", 40
)
MeritFlaw.objects.get_or_create(name="Research Grant")[0].add_source(
    "Book of Secrets", 57
)
MeritFlaw.objects.get_or_create(name="Rising Star")[0].add_source("Book of Secrets", 58)
MeritFlaw.objects.get_or_create(name="Ritual Sleeper")[0].add_source(
    "M20 Sorcerer", 108
)
MeritFlaw.objects.get_or_create(name="Rival House")[0].add_source("Book of Secrets", 63)
MeritFlaw.objects.get_or_create(name="Rivalry")[0].add_source("Book of Secrets", 66)
MeritFlaw.objects.get_or_create(name="Rogue")[0].add_source("Book of Secrets", 68)
MeritFlaw.objects.get_or_create(name="Rose-Colored Glasses")[0].add_source(
    "Book of Secrets", 50
)
MeritFlaw.objects.get_or_create(name="Rotten Liar")[0].add_source("Book of Secrets", 66)
MeritFlaw.objects.get_or_create(name="Saint of the Pit")[0].add_source(
    "Book of the Fallen", 118
)
MeritFlaw.objects.get_or_create(name="Sanctity")[0].add_source("Book of Secrets", 57)
MeritFlaw.objects.get_or_create(name="Scientific Mystic/Techgnosi")[0].add_source(
    "Book of Secrets", 45
)
x = MeritFlaw.objects.get_or_create(name="Screw the Rules")[0].add_source(
    "The Rich Bastard's Guide to Magick", 44
)
x.add_ratings([4])
x.allowed_types.add(mage)
x.allowed_types.add(human)
x.allowed_types.add(sorcerer)

MeritFlaw.objects.get_or_create(name="Secret Code Language")[0].add_source(
    "Book of Secrets", 57
)
MeritFlaw.objects.get_or_create(name="Sect Enmity")[0].add_source("Book of Secrets", 64)
MeritFlaw.objects.get_or_create(name="Self-Confident")[0].add_source(
    "Book of Secrets", 46
)
MeritFlaw.objects.get_or_create(name="Shadow Appeal")[0].add_source(
    "Book of the Fallen", 117
)
MeritFlaw.objects.get_or_create(name="Shallowing")[0].add_source(
    "Sources of Magick", 22
)
MeritFlaw.objects.get_or_create(name="Shapechanger Kin")[0].add_source(
    "Book of Secrets", 74
)
MeritFlaw.objects.get_or_create(name="Shattered Avatar")[0].add_source(
    "Book of Secrets", 77
)
MeritFlaw.objects.get_or_create(name="Short (Mage)")[0].add_source(
    "Book of Secrets", 50
)
MeritFlaw.objects.get_or_create(name="Short Fuse")[0].add_source("Book of Secrets", 50)
MeritFlaw.objects.get_or_create(name="Shy")[0].add_source("Book of Secrets", 48)
MeritFlaw.objects.get_or_create(name="Sleeping with the Enemy")[0].add_source(
    "Book of Secrets", 66
)
MeritFlaw.objects.get_or_create(name="Socially Networked")[0].add_source(
    "Book of Secrets", 57
)
MeritFlaw.objects.get_or_create(name="Soft-Hearted (Werewolf and Mage)")[0].add_source(
    "Book of Secrets", 48
)
MeritFlaw.objects.get_or_create(name="Spark of Life")[0].add_source(
    "Book of Secrets", 78
)
MeritFlaw.objects.get_or_create(name="Special Responsibility")[0].add_source(
    "Book of Secrets", 64
)
MeritFlaw.objects.get_or_create(name="Spectral Presence")[0].add_source(
    "Book of the Fallen", 119
)
MeritFlaw.objects.get_or_create(name="Speech Impediment")[0].add_source(
    "Book of Secrets", 48
)
MeritFlaw.objects.get_or_create(name="Sphere Attuned (Entropy)")[0].add_source(
    "Sources of Magick", 22
)
MeritFlaw.objects.get_or_create(name="Sphere Attuned (Forces)")[0].add_source(
    "Sources of Magick", 22
)
MeritFlaw.objects.get_or_create(name="Sphere Attuned (Life)")[0].add_source(
    "Sources of Magick", 22
)
MeritFlaw.objects.get_or_create(name="Sphere Attuned (Matter)")[0].add_source(
    "Sources of Magick", 22
)
MeritFlaw.objects.get_or_create(name="Sphere Attuned (Mind)")[0].add_source(
    "Sources of Magick", 22
)
MeritFlaw.objects.get_or_create(name="Sphere Attuned (Prime)")[0].add_source(
    "Sources of Magick", 22
)
MeritFlaw.objects.get_or_create(name="Sphere Attuned (Spirit)")[0].add_source(
    "Sources of Magick", 22
)
MeritFlaw.objects.get_or_create(name="Sphere Attuned (Time)")[0].add_source(
    "Sources of Magick", 22
)
MeritFlaw.objects.get_or_create(name="Sphere Inept - Correspondence")[0].add_source(
    "Book of Secrets", 94
)
MeritFlaw.objects.get_or_create(name="Sphere Inept - Entropy")[0].add_source(
    "Book of Secrets", 94
)
MeritFlaw.objects.get_or_create(name="Sphere Inept - Forces")[0].add_source(
    "Book of Secrets", 94
)
MeritFlaw.objects.get_or_create(name="Sphere Inept - Life")[0].add_source(
    "Book of Secrets", 94
)
MeritFlaw.objects.get_or_create(name="Sphere Inept - Matter")[0].add_source(
    "Book of Secrets", 94
)
MeritFlaw.objects.get_or_create(name="Sphere Inept - Mind")[0].add_source(
    "Book of Secrets", 94
)
MeritFlaw.objects.get_or_create(name="Sphere Inept - Prime")[0].add_source(
    "Book of Secrets", 94
)
MeritFlaw.objects.get_or_create(name="Sphere Inept - Spirit")[0].add_source(
    "Book of Secrets", 94
)
MeritFlaw.objects.get_or_create(name="Sphere Inept - Time")[0].add_source(
    "Book of Secrets", 94
)
MeritFlaw.objects.get_or_create(name="Sphere Natural - Correspondence")[0].add_source(
    "Book of Secrets", 79
)
MeritFlaw.objects.get_or_create(name="Sphere Natural - Entropy")[0].add_source(
    "Book of Secrets", 79
)
MeritFlaw.objects.get_or_create(name="Sphere Natural - Forces")[0].add_source(
    "Book of Secrets", 79
)
MeritFlaw.objects.get_or_create(name="Sphere Natural - Life")[0].add_source(
    "Book of Secrets", 79
)
MeritFlaw.objects.get_or_create(name="Sphere Natural - Matter")[0].add_source(
    "Book of Secrets", 79
)
MeritFlaw.objects.get_or_create(name="Sphere Natural - Mind")[0].add_source(
    "Book of Secrets", 79
)
MeritFlaw.objects.get_or_create(name="Sphere Natural - Prime")[0].add_source(
    "Book of Secrets", 79
)
MeritFlaw.objects.get_or_create(name="Sphere Natural - Spirit")[0].add_source(
    "Book of Secrets", 79
)
MeritFlaw.objects.get_or_create(name="Sphere Natural - Time")[0].add_source(
    "Book of Secrets", 79
)
MeritFlaw.objects.get_or_create(name="Spirit Guardian")[0].add_source(
    "Sources of Magick", 22
)
MeritFlaw.objects.get_or_create(name="Spirit Magnet (Mage)")[0].add_source(
    "Book of Secrets", 73
)
MeritFlaw.objects.get_or_create(name="Spirit Mentor")[0].add_source(
    "Book of Secrets", 73
)
MeritFlaw.objects.get_or_create(name="Sterile")[0].add_source("Book of Secrets", 36)
MeritFlaw.objects.get_or_create(name="Stormwarden/Quantum Voyager")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 643
)
MeritFlaw.objects.get_or_create(name="Strangeness")[0].add_source("Book of Secrets", 85)
MeritFlaw.objects.get_or_create(name="Strength of Psyche")[0].add_source(
    "M20 Sorcerer", 107
)
MeritFlaw.objects.get_or_create(name="Stress Atavism")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 644
)
MeritFlaw.objects.get_or_create(name="Style Sleeper")[0].add_source("M20 Sorcerer", 107)
MeritFlaw.objects.get_or_create(name="Subculture Insider")[0].add_source(
    "Book of Secrets", 58
)
MeritFlaw.objects.get_or_create(name="Supernatural Companion")[0].add_source(
    "Book of Secrets", 74
)
MeritFlaw.objects.get_or_create(name="Sympathizer")[0].add_source("Book of Secrets", 64)
MeritFlaw.objects.get_or_create(name="Taint of Corruption")[0].add_source(
    "Book of Secrets", 96
)
MeritFlaw.objects.get_or_create(name="Thaumivore")[0].add_source(
    "Gods and Monsters", 199
)
MeritFlaw.objects.get_or_create(name="Throwback")[0].add_source("Book of Secrets", 85)
MeritFlaw.objects.get_or_create(name="Ties")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 643
)
MeritFlaw.objects.get_or_create(name="Time Sense")[0].add_source("Book of Secrets", 44)
MeritFlaw.objects.get_or_create(name="Too Tough To Die")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 644
)
MeritFlaw.objects.get_or_create(name="Troublemaker")[0].add_source(
    "Book of Secrets", 65
)
MeritFlaw.objects.get_or_create(name="True Faith")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 644
)
MeritFlaw.objects.get_or_create(name="True Love (Werewolf and Mage)")[0].add_source(
    "Book of Secrets", 59
)
MeritFlaw.objects.get_or_create(name="Twin Link")[0].add_source("M20 Sorcerer", 107)
MeritFlaw.objects.get_or_create(name="Twin Souls")[0].add_source("Book of Secrets", 74)
MeritFlaw.objects.get_or_create(name="Twisted Apprenticeship")[0].add_source(
    "Book of Secrets", 64
)
MeritFlaw.objects.get_or_create(name="Umbral Affinity")[0].add_source(
    "Mage: the Ascension 20th Anniversary Edition", 644
)
MeritFlaw.objects.get_or_create(name="Unaging")[0].add_source("Book of Secrets", 69)
MeritFlaw.objects.get_or_create(name="Unbelief")[0].add_source("Gods and Monsters", 199)
MeritFlaw.objects.get_or_create(name="Unbondable")[0].add_source("Book of Secrets", 75)
MeritFlaw.objects.get_or_create(name="Uncanny")[0].add_source("Book of Secrets", 85)
MeritFlaw.objects.get_or_create(name="Ungainly Fingers")[0].add_source(
    "Gods and Monsters", 200
)
MeritFlaw.objects.get_or_create(name="Unobtrusive")[0].add_source("Book of Secrets", 54)
MeritFlaw.objects.get_or_create(name="Vanilla")[0].add_source("Book of Secrets", 48)
MeritFlaw.objects.get_or_create(name="Vengeful")[0].add_source("Book of Secrets", 50)
MeritFlaw.objects.get_or_create(name="Vulnerability")[0].add_source(
    "Book of Secrets", 86
)
MeritFlaw.objects.get_or_create(name="Ward")[0].add_source("Book of Secrets", 66)
MeritFlaw.objects.get_or_create(name="Weak Spot")[0].add_source(
    "Gods and Monsters", 200
)
MeritFlaw.objects.get_or_create(name="Whimsy")[0].add_source("Book of Secrets", 48)
MeritFlaw.objects.get_or_create(name="Widderslainte")[0].add_source(
    "Book of the Fallen", 120
)
MeritFlaw.objects.get_or_create(name="Wild Talent")[0].add_source("M20 Sorcerer", 107)
MeritFlaw.objects.get_or_create(name="Witch-Hunted")[0].add_source(
    "Book of Secrets", 68
)

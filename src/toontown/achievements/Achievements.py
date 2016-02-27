from toontown.toonbase import ToontownGlobals
from toontown.quest import Quests

import collections


BRONZE = 0
SILVER = 1
GOLD = 2
PLATINUM = 3

HIDDEN = 0
VISIBLE = 1

ANY = -1

BOOST_LEVEL = 5
BASE_XP = 250
GROWTH_FACTOR = 0.12

achievementScore = {
    BRONZE: 200,
    SILVER: 500,
    GOLD: 1250,
    PLATINUM: 3000
}


class Achievement:
    NEEDS_STATS = True

    def __init__(self, id):
        self.id = id

    def doAchievement(self, av):
        if self.id in av.getAchievements()[0]:
            return

        accountStats = None

        if self.NEEDS_STATS:
            accountStats = simbase.air.achievementsManager.statsCache.getStats(av.doId)

        self.handleAccountStats(av, accountStats)

    def handleAccountStats(self, av, accountStats):
        if self.hasComplete(av, accountStats):
            self.handleComplete(av)

    def hasComplete(self, av, accountStats):
        return False

    def handleComplete(self, av):
        simbase.air.achievementsManager.toonCompletedAchievement(av, self.id)


class MeetsFieldAchievement(Achievement):
    def __init__(self, id, field, needed=ANY):
        Achievement.__init__(self, id)

        self.field = field
        self.needed = needed

    def meetsNeeded(self, field):
        return field >= self.needed

    def hasComplete(self, av, accountStats):
        return self.meetsNeeded(accountStats[self.field])


class HasRequiredAchievements(Achievement):
    def __init__(self, id, achievementIds):
        Achievement.__init__(self, id)

        self.achievementIds = achievementIds

    def meetsNeededAchievementIds(self, avAchievements):
        for achievementId in self.achievementIds:
            if achievementId not in avAchievements:
                return False

        return True

    def hasComplete(self, av, accountStats):
        return self.meetsNeededAchievementIds(accountStats['ACHIEVEMENTS'])


class FriendAchievement(Achievement):
    NEEDS_STATS = False

    def __init__(self, id, neededFriends=ANY):
        Achievement.__init__(self, id)

        self.neededFriends = neededFriends

    def meetsNeededFriends(self, avFriends):
        if self.neededFriends == ANY:
            return True

        return len(avFriends) >= self.neededFriends

    def hasComplete(self, av, accountStats):
        return self.meetsNeededFriends(av.getFriendsList())


class SuitAchievement(Achievement):
    def __init__(self, id, dbEntry, needed=ANY):
        Achievement.__init__(self, id)

        self.needed = needed
        self.dbEntry = dbEntry

    def meetsNeeded(self, cogsDefeated):
        if self.needed == ANY:
            return True

        return cogsDefeated >= self.needed

    def hasComplete(self, av, accountStats):
        return self.meetsNeeded(accountStats[self.dbEntry])


class BuildingAchievement(Achievement):
    def __init__(self, id, track=None, floor=ANY, needed=ANY, floors=ANY):
        Achievement.__init__(self, id)

        self.track = ToontownGlobals.cogDept2index[track] if track is not None else ANY
        self.floor = floor
        self.needed = needed
        self.floors = floors

    def hasComplete(self, av, accountStats):
        # Check if we are only checking for total floor count.
        if self.floors != ANY:
            return accountStats['BUILDING_FLOORS_COMPLETED'] >= self.floors

        # Check if we are checking for a total for a specific track.
        if self.track != ANY and self.floor == ANY:
            return sum(accountStats['BUILDINGS_COMPLETED'][self.track*5:(self.track*5)+5]) >= self.needed

        # Check if we are checking for a specific track and floor.
        if self.track != ANY and self.floor != ANY:
            return sum(accountStats['BUILDINGS_COMPLETED'][(self.track*5)+self.floor]) >= self.needed

        # Check if we are checking for a specific floor any track.
        if self.track == ANY and self.floor != ANY:
            return sum([accountStats['BUILDINGS_COMPLETED'][(x*5)+self.floor] for x in xrange(4)]) >= self.needed

        # Check if we are checking for overall buildings.
        if self.track == ANY and self.floor == ANY:
            return sum(accountStats['BUILDINGS_COMPLETED']) >= self.needed

        # This achievement isn't possible to complete.
        return False


class BossCogAchievement(SuitAchievement):
    def __init__(self, id, dbEntry, needed=ANY, players=ANY):
        SuitAchievement.__init__(self, id, dbEntry, needed)

        self.players = players

    def meetsNeeded(self, bossStats):
        if self.needed == ANY:
            return True

        progress = sum(bossStats) if self.players == ANY else bossStats[self.players-1]
        return progress >= self.needed


class VPAchievement(BossCogAchievement):
    def __init__(self, id, needed=ANY, players=ANY):
        BossCogAchievement.__init__(self, id, 'VPS_DEFEATED', needed, players)


class VPStunAchievement(MeetsFieldAchievement):
    def __init__(self, id, needed=ANY):
        MeetsFieldAchievement.__init__(self, id, 'VP_STUNS', needed)


class CFOAchievement(BossCogAchievement):
    def __init__(self, id, needed=ANY, players=ANY):
        BossCogAchievement.__init__(self, id, 'CFOS_DEFEATED', needed, players)


class CJAchievement(BossCogAchievement):
    def __init__(self, id, needed=ANY, players=ANY):
        BossCogAchievement.__init__(self, id, 'CJS_DEFEATED', needed, players)


class CJJurorAchievement(MeetsFieldAchievement):
    def __init__(self, id, needed=ANY):
        MeetsFieldAchievement.__init__(self, id, 'CJ_JURORS_SEATED', needed)


class CEOAchievement(BossCogAchievement):
    def __init__(self, id, needed=ANY, players=ANY):
        BossCogAchievement.__init__(self, id, 'CEOS_DEFEATED', needed, players)


class CEOSnackAchievement(MeetsFieldAchievement):
    def __init__(self, id, needed=ANY):
        MeetsFieldAchievement.__init__(self, id, 'CEO_SNACKS_EATEN', needed)


class QuestCountAchievement(MeetsFieldAchievement):
    def __init__(self, id, needed=ANY):
        MeetsFieldAchievement.__init__(self, id, 'QUESTS_COMPLETED', needed)


class QuestTierAchievement(Achievement):
    NEEDS_STATS = False

    def __init__(self, id, tier=ANY):
        Achievement.__init__(self, id)

        self.tier = tier

    def meetsTier(self, tier):
        if tier == ANY:
            return True

        return tier >= self.tier

    def hasComplete(self, av, accountStats):
        return self.meetsTier(av.getRewardTier())


# Next available achievement id: 38
AchievementsDict = {
    # Misc Achievements

    0: (FriendAchievement(0, neededFriends=1), BRONZE, VISIBLE),  # Make 1 friend

    # Cog Achievements

    17: (BuildingAchievement(17, needed=1), BRONZE, VISIBLE),  # Complete 1 building
    18: (BuildingAchievement(18, track='s', needed=1), BRONZE, VISIBLE),  # Complete 1 Sellbot building
    19: (BuildingAchievement(19, track='m', needed=1), BRONZE, VISIBLE),  # Complete 1 Cashbot building
    20: (BuildingAchievement(20, track='l', needed=1), BRONZE, VISIBLE),  # Complete 1 Lawbot building
    21: (BuildingAchievement(21, track='c', needed=1), BRONZE, VISIBLE),  # Complete 1 Bossbot building

    1: (VPAchievement(1, needed=1), BRONZE, VISIBLE),  # Defeat 1 VP
    12: (VPAchievement(12, needed=1, players=1), SILVER, VISIBLE),  # Solo the VP once
    23: (VPStunAchievement(23, needed=100), SILVER, VISIBLE),  # Stun the VP 100 times
    30: (VPStunAchievement(30, needed=1000), GOLD, VISIBLE),  # Stun the VP 1000 times
    31: (VPStunAchievement(31, needed=2000), PLATINUM, VISIBLE),  # Stun the VP 2000 times
    25: (HasRequiredAchievements(25, [1, 12, 31]), PLATINUM, HIDDEN),  # Get all of the VP achievements

    2: (CFOAchievement(2, needed=1), BRONZE, VISIBLE),  # Defeat 1 CFO
    13: (CFOAchievement(13, needed=1, players=1), GOLD, VISIBLE),  # Solo the CFO once
    26: (HasRequiredAchievements(26, [2, 13]), PLATINUM, HIDDEN),  # Get all of the CFO achievements

    3: (CJAchievement(3, needed=1), BRONZE, VISIBLE),  # Defeat 1 CJ
    14: (CJAchievement(14, needed=1, players=1), GOLD, VISIBLE),  # Solo the CJ once
    24: (CJJurorAchievement(24, needed=50), SILVER, VISIBLE),  # Seat 50 jurors in the CJ
    27: (HasRequiredAchievements(27, [3, 14, 24]), PLATINUM, HIDDEN),  # Get all of the CJ achievements

    4: (CEOAchievement(4, needed=1), BRONZE, VISIBLE),  # Defeat 1 CEO
    15: (CEOAchievement(15, needed=1, players=1), GOLD, VISIBLE),  # Solo the CEO once
    22: (CEOSnackAchievement(22, needed=50), BRONZE, HIDDEN),  # Eat 50 snacks in the CEO
    28: (HasRequiredAchievements(28, [4, 15, 22]), PLATINUM, HIDDEN),  # Get all of the CEO achievements

    16: (HasRequiredAchievements(16, [12, 13, 14, 15]), PLATINUM, VISIBLE),  # Solo all the cog bosses

    29: (HasRequiredAchievements(29, [25, 26, 27, 28, 16]), PLATINUM, VISIBLE),  # Get all of the cog boss achievements

    # Quest Achievements

    32: (QuestCountAchievement(32, needed=1), BRONZE, VISIBLE),  # Complete your first ToonTask
    33: (QuestCountAchievement(33, needed=10), BRONZE, VISIBLE),  # Complete 10 ToonTasks
    34: (QuestCountAchievement(34, needed=100), SILVER, VISIBLE),  # Complete 100 ToonTasks
    35: (QuestCountAchievement(35, needed=250), SILVER, VISIBLE),  # Complete 250 ToonTasks
    36: (QuestCountAchievement(36, needed=500), GOLD, VISIBLE),  # Complete 500 ToonTasks

    5: (QuestTierAchievement(5, tier=Quests.DD_TIER), BRONZE, VISIBLE),  # Complete TTC
    6: (QuestTierAchievement(6, tier=Quests.DG_TIER), BRONZE, VISIBLE),  # Complete DD
    7: (QuestTierAchievement(7, tier=Quests.MM_TIER), BRONZE, VISIBLE),  # Complete DG
    8: (QuestTierAchievement(8, tier=Quests.BR_TIER), SILVER, VISIBLE),  # Complete MML
    9: (QuestTierAchievement(9, tier=Quests.DL_TIER), SILVER, VISIBLE),  # Complete TB
    10: (QuestTierAchievement(10, tier=Quests.ELDER_TIER), GOLD, VISIBLE),  # Complete DDL
    11: (QuestTierAchievement(11, tier=Quests.ELDER_TIER), PLATINUM, VISIBLE),  # Complete all tasks

    37: (HasRequiredAchievements(37, [36, 11]), PLATINUM, HIDDEN)  # Get all Quest achievements
}

classifier2AchievementIds = collections.OrderedDict()
classifier2AchievementIds['misc'] = [0]
classifier2AchievementIds['quest'] = [32, 33, 34, 35, 36, 5, 6, 7, 8, 9, 10, 11, 37]
classifier2AchievementIds['suit'] = [17, 18, 19, 20, 21, 1, 12, 23, 30, 31, 25, 2, 13, 26, 3, 14, 24, 27, 4, 15, 22,
                                     28, 16, 29]

achievementId2Classifier = {}

for category in classifier2AchievementIds:
    achievementIds = classifier2AchievementIds[category]
    for achievementId in achievementIds:
        achievementId2Classifier[achievementId] = category

type2Achievements = {}

for achievementId in AchievementsDict:
    achievementClass = AchievementsDict[achievementId][0].__class__.__name__

    if achievementClass not in type2Achievements:
        type2Achievements[achievementClass] = []

    type2Achievements[achievementClass].append(achievementId)


def getLevelFromPoints(xp):
    i = 0
    while True:
        points = getPointsForLevel(i)
        if points >= xp:
            return i
        i += 1


def getPointsForLevel(level):
    if level == 0:
        return BASE_XP
    return int((BASE_XP * level+1) * (GROWTH_FACTOR * level+1))


def getAchievementClassifier(achievementId):
    return achievementId2Classifier[achievementId]


def getClassifierAchievements(classifier):
    return classifier2AchievementIds[classifier]


def getAchievementsOfType(type):
    return type2Achievements.get(type, [])


def getAchievementVisibility(achievementId):
    return AchievementsDict[achievementId][2]


def getAchievementScore(achievementId):
    achievementType = AchievementsDict[achievementId][1]
    return achievementScore[achievementType]


def getAchievementClass(achievementId):
    return AchievementsDict[achievementId][0]


def getAchievementCategory(achievementId):
    return AchievementsDict[achievementId][1]


def doAchievement(achievementId, args):
    AchievementsDict[achievementId][0].doAchievement(*args)

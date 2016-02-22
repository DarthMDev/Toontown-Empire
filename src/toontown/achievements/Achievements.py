from toontown.quest import Quests


BRONZE = 0
SILVER = 1
GOLD = 2
PLATINUM = 3

HIDDEN = 0
VISIBLE = 1

ANY = 0

MAX_LEVEL = 20

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


class BossCogAchievement(SuitAchievement):
    def __init__(self, id, dbEntry, needed=ANY, players=ANY):
        SuitAchievement.__init__(self, id, dbEntry, needed)

        self.players = players

    def meetsNeeded(self, bossStats):
        if self.needed == ANY:
            return True

        progress = 0

        if self.players == ANY:
            for x in bossStats:
                progress += x
        else:
            progress = bossStats[self.players-1]

        return progress >= self.needed

    def hasComplete(self, av, accountStats):
        return self.meetsNeeded(accountStats[self.dbEntry])


class VPAchievement(BossCogAchievement):
    def __init__(self, id, needed=ANY, players=ANY):
        BossCogAchievement.__init__(self, id, 'VPS_DEFEATED', needed, players)


class CFOAchievement(BossCogAchievement):
    def __init__(self, id, needed=ANY, players=ANY):
        BossCogAchievement.__init__(self, id, 'CFOS_DEFEATED', needed, players)


class CJAchievement(BossCogAchievement):
    def __init__(self, id, needed=ANY, players=ANY):
        BossCogAchievement.__init__(self, id, 'CJS_DEFEATED', needed, players)


class CEOAchievement(BossCogAchievement):
    def __init__(self, id, needed=ANY, players=ANY):
        BossCogAchievement.__init__(self, id, 'CEOS_DEFEATED', needed, players)


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


# Next available achievement id: 17
AchievementsDict = {
    0: (FriendAchievement(0, neededFriends=1), BRONZE, VISIBLE),  # Make 1 friend

    1: (VPAchievement(1, needed=1), BRONZE, VISIBLE),  # Defeat 1 VP
    12: (VPAchievement(12, needed=1, players=1), SILVER, VISIBLE),  # Solo the VP once

    2: (CFOAchievement(2, needed=1), BRONZE, VISIBLE),  # Defeat 1 CFO
    13: (CFOAchievement(13, needed=1, players=1), GOLD, VISIBLE),  # Solo the CFO once

    3: (CJAchievement(3, needed=1), BRONZE, VISIBLE),  # Defeat 1 CJ
    14: (CJAchievement(14, needed=1, players=1), GOLD, VISIBLE),  # Solo the CJ once

    4: (CEOAchievement(4, needed=1), BRONZE, VISIBLE),  # Defeat 1 CEO
    15: (CEOAchievement(15, needed=1, players=1), GOLD, VISIBLE),  # Solo the CEO once

    16: (HasRequiredAchievements(16, [12, 13, 14, 15]), PLATINUM, VISIBLE),  # Solo all the cog bosses

    5: (QuestTierAchievement(5, tier=Quests.DD_TIER), BRONZE, VISIBLE),  # Complete TTC
    6: (QuestTierAchievement(6, tier=Quests.DG_TIER), BRONZE, VISIBLE),  # Complete DD
    7: (QuestTierAchievement(7, tier=Quests.MM_TIER), BRONZE, VISIBLE),  # Complete DG
    8: (QuestTierAchievement(8, tier=Quests.BR_TIER), SILVER, VISIBLE),  # Complete MML
    9: (QuestTierAchievement(9, tier=Quests.DL_TIER), SILVER, VISIBLE),  # Complete TB
    10: (QuestTierAchievement(10, tier=Quests.ELDER_TIER), GOLD, VISIBLE),  # Complete DDL
    11: (QuestTierAchievement(11, tier=Quests.ELDER_TIER), PLATINUM, VISIBLE)  # Complete all tasks
}

category2AchievementIds = {
    'misc': [0, 5, 6, 7, 8, 9, 10, 11],
    'suit': [1, 2, 3, 4, 12, 13, 14, 15, 16]
}

type2Achievements = {}
levels = []
totalPoints = 0

for achievementId in AchievementsDict:
    achievementClass = AchievementsDict[achievementId][0].__class__.__name__

    if achievementClass not in type2Achievements:
        type2Achievements[achievementClass] = []

    type2Achievements[achievementClass].append(achievementId)
    totalPoints += achievementScore[AchievementsDict[achievementId][1]]

averagePoints = totalPoints / MAX_LEVEL
for i in xrange(MAX_LEVEL):
    levels.append(averagePoints * (i + 1))


def getLevelFromPoints(points):
    # Check if they are the max level.
    if points == levels[len(levels)-1]:
        return len(levels) - 1

    # Iterate through all of the levels and determine what level they are.
    for level, levelPoints in enumerate(levels):
        if points < levelPoints:
            return level


def getPointsForLevel(level):
    return levels[level]


def getAchievementsOfType(type):
    return type2Achievements.get(type, [])


def getAchievementScore(achievementId):
    achievementType = AchievementsDict[achievementId][1]
    return achievementScore[achievementType]


def getAchievementClass(achievementId):
    return AchievementsDict[achievementId][0]


def getAchievementCategory(achievementId):
    return AchievementsDict[achievementId][1]


def doAchievement(achievementId, args):
    AchievementsDict[achievementId][0].doAchievement(*args)

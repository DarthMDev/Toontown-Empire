from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM

from toontown.achievements.AccountStatsFSM import FetchAccountStatsFSM
from toontown.achievements import Achievements
from toontown.toonbase import ToontownGlobals


class AchievementOperationQueue:
    def __init__(self):
        self.operations = {}

    def addOperation(self, av, operation):
        if av.doId not in self.operations:
            self.operations[av.doId] = [operation]
            self.doOperation(av)
            return

        self.operations[av.doId].append(operation)

    def doOperation(self, av):
        if len(self.operations[av.doId]) == 0:
            del self.operations[av.doId]
            return

        operation = self.operations[av.doId].pop(0)
        operation.setCallback(self.doOperation)
        operation.request('Start')


class AchievementOperationFSM(FSM):
    def __init__(self, air, av):
        FSM.__init__(self, self.__class__.__name__)

        self.air = air
        self.av = av

        self.callback = None

    def setCallback(self, callback):
        self.callback = callback

    def enterStart(self):
        accountStats = self.air.achievementsManager.statsCache.getStats(self.av.doId)
        self.handleAccountStatsRecieved(accountStats)

    def handleAccountStatsRecieved(self, accountStats):
        pass

    def enterDone(self):
        if self.callback:
            self.callback(self.av)


class AddAchievementFSM(AchievementOperationFSM):
    notify = directNotify.newCategory('AddAchievementFSM')

    def __init__(self, air, av, achievementId):
        AchievementOperationFSM.__init__(self, air, av)

        self.achievementId = achievementId

    def handleAccountStatsRecieved(self, accountStats):
        accountStats['ACHIEVEMENTS'].append(self.achievementId)
        accountStats['ACHIEVEMENT_POINTS'] += Achievements.getAchievementScore(self.achievementId)

        # Update the account stats:
        self.air.dbInterface.updateObject(
            self.air.dbId,
            self.av.getStatsId(),
            self.air.dclassesByName['AccountStats'],
            {'ACHIEVEMENTS': accountStats['ACHIEVEMENTS'],
             'ACHIEVEMENT_POINTS': accountStats['ACHIEVEMENT_POINTS']})

        # Set the av's achievements:
        self.av.b_setAchievements(accountStats['ACHIEVEMENTS'], accountStats['ACHIEVEMENT_POINTS'])
        self.demand('Done')


class AccountStatsCache(DirectObject):
    notify = directNotify.newCategory('AccountStatsCache')

    def __init__(self, air):
        DirectObject.__init__(self)

        self.air = air
        self.stats = {}

    def getStats(self, avId):
        if avId not in self.stats:
            self.notify.warning('Tried to get stats for unknown avId %s' % avId)
            return

        return self.stats[avId]

    def __handleAccountStatsRecieved(self, av, accountStats):
        if av.doId in self.stats:
            self.notify.warning('Tried to create stats cache for existing avId %s' % av.doId)
            del self.stats[av.doId]
            return

        self.acceptOnce(av.getDeleteEvent(), self.toonDeleted, extraArgs=[av.doId])
        self.stats[av.doId] = accountStats

    def toonGenerated(self, av):
        fsm = FetchAccountStatsFSM(self.air, av, self.__handleAccountStatsRecieved)
        fsm.request('Start')

    def toonDeleted(self, avId):
        if avId not in self.stats:
            self.notify.warning('Tried to clear stats cache for unknown avId %s' % avId)
            return

        del self.stats[avId]


class AchievementsManagerAI:
    def __init__(self, air):
        self.air = air
        self.operationsQueue = AchievementOperationQueue()
        self.statsCache = AccountStatsCache(self.air)

    """
    Utility Functions
    """

    def toonCompletedAchievement(self, av, achievementId):
        fsm = AddAchievementFSM(self.air, av, achievementId)
        self.operationsQueue.addOperation(av, fsm)

    def modifyAccountStats(self, statsId, modified):
        self.air.dbInterface.updateObject(
            self.air.dbId,
            statsId,
            self.air.dclassesByName['AccountStats'],
            modified)

    """
    Friend Achievements
    """

    def toonMadeFriend(self, avId):
        av = self.air.doId2do.get(avId)
        if av is None:
            return

        # Update the account stats
        accountStats = self.statsCache.getStats(avId)
        accountStats['FRIENDS_MADE'] += 1

        self.modifyAccountStats(av.getStatsId(), {'FRIENDS_MADE': accountStats['FRIENDS_MADE']})

        possibleAchievements = Achievements.getAchievementsOfType('FriendAchievement')
        for achievementId in possibleAchievements:
            Achievements.doAchievement(achievementId, [av])

    def toonPlayedMinigame(self, avId):
        pass

    """
    Building Achievements
    """

    def toonDefeatedBuilding(self, avId, track, floorCount):
        av = self.air.doId2do.get(avId)
        if av is None:
            return

        index = (ToontownGlobals.cogDept2index[track] * 5) + floorCount

        # Update the account stats
        accountStats = self.statsCache.getStats(avId)
        accountStats['BUILDINGS_COMPLETED'][index] += 1
        accountStats['BUILDING_FLOORS_COMPLETED'] += floorCount + 1

        self.modifyAccountStats(av.getStatsId(), {'BUILDINGS_COMPLETED': accountStats['BUILDINGS_COMPLETED'],
                                                  'BUILDING_FLOORS_COMPLETED': accountStats['BUILDING_FLOORS_COMPLETED']})

        possibleAchievements = Achievements.getAchievementsOfType('BuildingAchievement')
        for achievementId in possibleAchievements:
            Achievements.doAchievement(achievementId, [av])

    """
    Boss Cog Achievements
    """

    def toonDefeatedBossCog(self, avId, bossDept, infoDict):
        av = self.air.doId2do.get(avId)
        if av is None:
            return

        if bossDept == 's':
            self.toonDefeatedVP(av, infoDict)
        elif bossDept == 'm':
            self.toonDefeatedCFO(av, infoDict)
        elif bossDept == 'l':
            self.toonDefeatedCJ(av, infoDict)
        elif bossDept == 'c':
            self.toonDefeatedCEO(av, infoDict)
        else:
            self.notify.warning('Avatar %s defeated unknown boss: %s' % (avId, bossDept))
            return

        possibleAchievements = Achievements.getAchievementsOfType('HasRequiredAchievements')
        for achievementId in possibleAchievements:
            Achievements.doAchievement(achievementId, [av])

    def toonLostBossCog(self, avId, bossDept):
        av = self.air.doId2do.get(avId)
        if av is None:
            return

        accountStats = self.statsCache.getStats(avId)

        if bossDept == 's':
            accountStats['VPS_LOST'] += 1
            self.modifyAccountStats(av.getStatsId(), {'VPS_LOST': accountStats['VPS_LOST']})
        elif bossDept == 'm':
            accountStats['CFOS_LOST'] += 1
            self.modifyAccountStats(av.getStatsId(), {'CFOS_LOST': accountStats['CFOS_LOST']})
        elif bossDept == 'l':
            accountStats['CJS_LOST'] += 1
            self.modifyAccountStats(av.getStatsId(), {'CJS_LOST': accountStats['CJS_LOST']})
        elif bossDept == 'c':
            accountStats['CEOS_LOST'] += 1
            self.modifyAccountStats(av.getStatsId(), {'CEOS_LOST': accountStats['CEOS_LOST']})
        else:
            self.notify.warning('Avatar %s lost unknown boss: %s' % (avId, bossDept))

    def toonDefeatedVP(self, av, infoDict):
        # Update the account stats
        accountStats = self.statsCache.getStats(av.doId)

        accountStats['VPS_DEFEATED'][infoDict['toonCount']] += 1
        if infoDict['finalHit']:
            accountStats['VP_FINAL_HITS'] += 1
        accountStats['VP_STUNS'] += infoDict['stuns']
        accountStats['VP_DAMAGE_DEALT'] += infoDict['damageDealt']

        previousTime = accountStats['VP_TIMES'][infoDict['toonCount']]
        if previousTime > infoDict['time'] or previousTime == 0:
            accountStats['VP_TIMES'][infoDict['toonCount']] = infoDict['time']

        self.modifyAccountStats(av.getStatsId(), {'VPS_DEFEATED': accountStats['VPS_DEFEATED'],
                                                  'VP_FINAL_HITS': accountStats['VP_FINAL_HITS'],
                                                  'VP_STUNS': accountStats['VP_STUNS'],
                                                  'VP_DAMAGE_DEALT': accountStats['VP_DAMAGE_DEALT'],
                                                  'VP_TIMES': accountStats['VP_TIMES']})

        possibleAchievements = Achievements.getAchievementsOfType('VPAchievement')
        possibleAchievements.extend(Achievements.getAchievementsOfType('VPStunAchievement'))
        for achievementId in possibleAchievements:
            Achievements.doAchievement(achievementId, [av])

    def toonDefeatedCFO(self, av, infoDict):
        # Update the account stats
        accountStats = self.statsCache.getStats(av.doId)

        accountStats['CFOS_DEFEATED'][infoDict['toonCount']] += 1
        if infoDict['finalHit']:
            accountStats['CFO_FINAL_HITS'] += 1
        accountStats['CFO_STUNS'] += infoDict['stuns']
        accountStats['CFO_DAMAGE_DEALT'] += infoDict['damageDealt']
        accountStats['CFO_GOONS_HIT'] += infoDict['goonsHit']
        accountStats['CFO_SAFES_HIT'] += infoDict['safesHit']
        accountStats['CFO_HELMETS_REMOVED'] += infoDict['helmetsRemoved']

        previousTime = accountStats['CFO_TIMES'][infoDict['toonCount']]
        if previousTime > infoDict['time'] or previousTime == 0:
            accountStats['CFO_TIMES'][infoDict['toonCount']] = infoDict['time']

        self.modifyAccountStats(av.getStatsId(), {'CFOS_DEFEATED': accountStats['CFOS_DEFEATED'],
                                                  'CFO_FINAL_HITS': accountStats['CFO_FINAL_HITS'],
                                                  'CFO_STUNS': accountStats['CFO_STUNS'],
                                                  'CFO_DAMAGE_DEALT': accountStats['CFO_DAMAGE_DEALT'],
                                                  'CFO_GOONS_HIT': accountStats['CFO_GOONS_HIT'],
                                                  'CFO_SAFES_HIT': accountStats['CFO_SAFES_HIT'],
                                                  'CFO_HELMETS_REMOVED': accountStats['CFO_HELMETS_REMOVED'],
                                                  'CFO_TIMES': accountStats['CFO_TIMES']})

        possibleAchievements = Achievements.getAchievementsOfType('CFOAchievement')
        for achievementId in possibleAchievements:
            Achievements.doAchievement(achievementId, [av])

    def toonDefeatedCJ(self, av, infoDict):
        # Update the account stats
        accountStats = self.statsCache.getStats(av.doId)

        accountStats['CJS_DEFEATED'][infoDict['toonCount']] += 1
        if infoDict['finalHit']:
            accountStats['CJ_FINAL_HITS'] += 1
        accountStats['CJ_DAMAGE_DEALT'] += infoDict['damageDealt']
        accountStats['CJ_COGS_STUNNED'] += infoDict['cogsStunned']
        accountStats['CJ_JURORS_SEATED'] += infoDict['jurorsSeated']

        previousTime = accountStats['CJ_TIMES'][infoDict['toonCount']]
        if previousTime > infoDict['time'] or previousTime == 0:
            accountStats['CJ_TIMES'][infoDict['toonCount']] = infoDict['time']

        self.modifyAccountStats(av.getStatsId(), {'CJS_DEFEATED': accountStats['CJS_DEFEATED'],
                                                  'CJ_FINAL_HITS': accountStats['CJ_FINAL_HITS'],
                                                  'CJ_DAMAGE_DEALT': accountStats['CJ_DAMAGE_DEALT'],
                                                  'CJ_COGS_STUNNED': accountStats['CJ_COGS_STUNNED'],
                                                  'CJ_JURORS_SEATED': accountStats['CJ_JURORS_SEATED'],
                                                  'CJ_TIMES': accountStats['CJ_TIMES']})

        possibleAchievements = Achievements.getAchievementsOfType('CJAchievement')
        possibleAchievements.extend(Achievements.getAchievementsOfType('CJJurorAchievement'))
        for achievementId in possibleAchievements:
            Achievements.doAchievement(achievementId, [av])

    def toonDefeatedCEO(self, av, infoDict):
        # Update the account stats
        accountStats = self.statsCache.getStats(av.doId)

        accountStats['CEOS_DEFEATED'][infoDict['toonCount']] += 1
        if infoDict['finalHit']:
            accountStats['CEO_FINAL_HITS'] += 1
        accountStats['CEO_DAMAGE_DEALT'] += infoDict['damageDealt']
        accountStats['CEO_GOLF_HITS'] += infoDict['golfHits']
        accountStats['CEO_SNACKS_EATEN'] += infoDict['snacksEaten']
        accountStats['CEO_COGS_SERVED'] += infoDict['cogsServed']
        accountStats['FIRES_EARNED'] += infoDict['fires']

        previousTime = accountStats['CEO_TIMES'][infoDict['toonCount']]
        if previousTime > infoDict['time'] or previousTime == 0:
            accountStats['CEO_TIMES'][infoDict['toonCount']] = infoDict['time']

        self.modifyAccountStats(av.getStatsId(), {'CEOS_DEFEATED': accountStats['CEOS_DEFEATED'],
                                                  'CEO_FINAL_HITS': accountStats['CEO_FINAL_HITS'],
                                                  'CEO_DAMAGE_DEALT': accountStats['CEO_DAMAGE_DEALT'],
                                                  'CEO_GOLF_HITS': accountStats['CEO_GOLD_HITS'],
                                                  'CEO_SNACKS_EATEN': accountStats['CEO_SNACKS_EATEN'],
                                                  'CEO_COGS_SERVED': accountStats['CEO_COGS_SERVED'],
                                                  'FIRES_EARNED': accountStats['FIRES_EARNED'],
                                                  'CEO_TIMES': accountStats['CEO_TIMES']})

        possibleAchievements = Achievements.getAchievementsOfType('CEOAchievement')
        possibleAchievements.extend(Achievements.getAchievementsOfType('CEOSnackAchievement'))
        for achievementId in possibleAchievements:
            Achievements.doAchievement(achievementId, [av])

    """
    Quest Achievements
    """

    def toonCompletedQuest(self, avId):
        av = self.air.doId2do.get(avId)
        if av is None:
            return

        # Update the account stats
        accountStats = self.statsCache.getStats(avId)
        accountStats['QUESTS_COMPLETED'] += 1

        self.modifyAccountStats(av.getStatsId(), {'QUESTS_COMPLETED': accountStats['QUESTS_COMPLETED']})

        possibleAchievements = Achievements.getAchievementsOfType('QuestTierAchievement')
        possibleAchievements.extend(Achievements.getAchievementsOfType('QuestCountAchievement'))
        for achievementId in possibleAchievements:
            Achievements.doAchievement(achievementId, [av])

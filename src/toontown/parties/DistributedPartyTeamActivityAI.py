from direct.distributed.ClockDelta import globalClockDelta

from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.parties import PartyGlobals

import random


class DistributedPartyTeamActivityAI(DistributedPartyActivityAI):
    notify = directNotify.newCategory('DistributedPartyTeamActivityAI')

    MAX_PLAYERS = 8
    MIN_PLAYERS_PER_TEAM = 1
    MAX_PLAYERS_PER_TEAM = 4

    CAN_SWITCH_TEAMS = True

    COUNTDOWN_TIME = 15
    DURATION = 90

    def __init__(self, air, party, activityInfo):
        DistributedPartyActivityAI.__init__(self, air, party, activityInfo)

        self.leftTeam = []
        self.rightTeam = []

        self.teamDict = {
            PartyGlobals.TeamActivityTeams.LeftTeam: self.leftTeam,
            PartyGlobals.TeamActivityTeams.RightTeam: self.rightTeam
        }

    def generate(self):
        DistributedPartyActivityAI.generate(self)

        self.setState('WaitForEnough')

    def toonJoinRequest(self, team):
        av = self._getCaller()
        if not av:
            return
            
        if not self.fsm.state in ('WaitForEnough', 'WaitToStart'):
            self.sendUpdateToAvatarId(av.doId, 'joinTeamRequestDenied', [PartyGlobals.DenialReasons.Default])
            return
            
        if len(self.toonIds[team]) >= self.getPlayersPerTeam()[1]:
            self.sendUpdateToAvatarId(av.doId, 'joinTeamRequestDenied', [PartyGlobals.DenialReasons.Full])
            return
            
        if av.doId in self.toonsPlaying:
            self.air.writeServerEvent('suspicious', av.doId, 'tried to join party team activity again!')
            self.sendUpdateToAvatarId(av.doId, 'joinTeamRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        # idgaf if they exit unexpectedly in this case
        self.toonIds[team].append(av.doId)
        DistributedPartyActivityAI.toonJoinRequest(self)
        self.__update()

    def __update(self):
        self.updateToonsPlaying()
        
        if self.fsm.state == 'WaitForEnough':
            if self.__areTeamsCorrect():
                self.b_setState('WaitToStart')
        
        elif self.fsm.state == 'WaitToStart':
            if not self.__areTeamsCorrect():
                self.b_setState('WaitForEnough')
        
    def handleUnexpectedExit(self, avId, team):
        DistributedPartyActivityAI.handleUnexpectedExit(self, avId)
        if avId in self.teamDict[team]:
            del self.teamDict[team]
        if avId in self.leftTeam:
            self.leftTeam.remove(avId)
        if avId in self.rightTeam:
            self.rightTeam.remove(avId)
        self.updateToonsPlaying()

    def toonExitRequest(self, team):
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.air.doId2do:
            self.notify.warning('Unknown avatar %s tried to exit!' % avId)
            return

        if not self.isValidTeam(team):
            self.notify.warning('Avatar %s tried to exit an invalid team!' % avId)
            return

        if avId not in self.toonsPlaying:
            self.notify.warning('Avatar %s tried to leave a game he wasnt playing!' % avId)
            return

        if avId not in self.teamDict[team]:
            self.notify.warning('Avatar %s tried to leave a team he wasnt on!' % avId)
            return

        self.teamDict[team].remove(avId)
        del self.toonsPlaying[avId]

        self.updateToonsPlaying()

        if not self.areEnoughPlayers():
            self.setState('WaitForEnough')
            self.cancelCountdown()

    def toonSwitchTeamRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not self.CAN_SWITCH_TEAMS:
            self.notify.warning('Avatar %s tried to switch teams when it was disabled!' % avId)
            return

        if avId not in self.toonsPlaying:
            self.notify.warning('Unknown avatar %s tried to switch teams!' % avId)
            return

        if avId in self.leftTeam:
            if self.isTeamFull(self.rightTeam):
                self.switchTeamRequestDenied(avId, PartyGlobals.DenialReasons.Full)
                return

            self.leftTeam.remove(avId)
            self.rightTeam.append(avId)

        if avId in self.rightTeam:
            if self.isTeamFull(self.leftTeam):
                self.switchTeamRequestDenied(avId, PartyGlobals.DenialReasons.Full)
                return

            self.rightTeam.remove(avId)
            self.leftTeam.append(avId)

        self.updateToonsPlaying()

    def getPlayersPerTeam(self):
        return self.MIN_PLAYERS_PER_TEAM, self.MAX_PLAYERS_PER_TEAM

    def getDuration(self):
        return self.DURATION

    def getCanSwitchTeams(self):
        return self.CAN_SWITCH_TEAMS

    def setState(self, state, data=[0]):
        self.state = state
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime(), data])

    def getToonsPlaying(self):
        return self.leftTeam, self.rightTeam

    def setAdvantage(self, todo0):
        pass

    def switchTeamRequestDenied(self, avId, reason):
        self.sendUpdateToAvatarId(avId, 'switchTeamRequestDenied', [reason])

    def updateToonsPlaying(self):
        self.sendUpdate('setToonsPlaying', [self.leftTeam, self.rightTeam])

    def balancePlayers(self):
        lowTeam = self.leftTeam if len(self.leftTeam) < len(self.rightTeam) else self.rightTeam
        highTeam = self.rightTeam if len(self.leftTeam) < len(self.rightTeam) else self.leftTeam

        while len(highTeam) >= len(lowTeam) + 2:
            avId = random.choice(highTeam)

            highTeam.remove(avId)
            lowTeam.append(avId)

        self.updateToonsPlaying()

    def areEnoughPlayers(self):
        return len(self.leftTeam) + len(self.rightTeam) >= 2

    def isTeamFull(self, team):
        return len(team) >= self.MAX_PLAYERS_PER_TEAM

    def startCountdown(self):
        taskMgr.doMethodLater(self.COUNTDOWN_TIME, self.countdownFinished, self.uniqueName('countdown'))

    def cancelCountdown(self):
        taskMgr.remove(self.uniqueName('countdown'))

    def countdownFinished(self, task):
        self.setState('Rules')

    def clearGame(self):
        self.leftTeam = []
        self.rightTeam = []

        self.teamDict = {
            PartyGlobals.TeamActivityTeams.LeftTeam: self.leftTeam,
            PartyGlobals.TeamActivityTeams.RightTeam: self.rightTeam
        }

        self.toonsPlaying = {}

        self.updateToonsPlaying()

        self.setState('WaitForEnough')

    def isValidTeam(self, team):
        return (team == PartyGlobals.TeamActivityTeams.LeftTeam) or (team == PartyGlobals.TeamActivityTeams.RightTeam)

from otp.uberdog.GlobalOtpObjectUD import GlobalOtpObjectUD
from GroupTrackerGlobals import *


class GlobalGroupTrackerUD(GlobalOtpObjectUD):

    def announceGenerate(self):
        GlobalOtpObjectUD.announceGenerate(self)
        self.leader2Group = {1000001: ['Flippy', 'Nuttyboro', 0, 3]}
        self.listeners = []

    def addGroup(self, leaderId, groupStruct):
        self.leader2Group[leaderId] = list(groupStruct)

    def updateGroup(self, leaderId, category, currAvs):
        self.leader2Group[leaderId][CATEGORY] = category
        self.leader2Group[leaderId][CURR_AVS] = currAvs

        for avId in self.listeners:
            self.sendToAvatar(avId, 'updateGroup', [leaderId, category, currAvs])

    def removeGroup(self, leaderId):
        del self.leader2Group[leaderId]

    def requestGroups(self, avId):
        self.requestGroupsResponse(avId)
        if avId not in self.listeners:
            self.accept('distObjDelete-%d' % avId, self.doneRequesting, extraArgs=[avId])
            self.listeners.append(avId)

    def requestGroupsResponse(self, avId):
        if not self.leader2Group:
            return

        self.sendToAvatar(avId, 'requestGroupsResponse', [self.leader2Group.keys(), self.leader2Group.values()])

    def doneRequesting(self, avId):
        self.ignore('distObjDelete-%d' % avId)
        if avId in self.listeners:
            self.listeners.remove(avId)

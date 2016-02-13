from otp.uberdog.GlobalOtpObjectUD import GlobalOtpObjectUD
from GroupTrackerGlobals import *


class GlobalGroupTrackerUD(GlobalOtpObjectUD):

    def announceGenerate(self):
        GlobalOtpObjectUD.announceGenerate(self)

        # Maps a leaderId to the corresponding BoardingGroup.
        self.leader2Group = {}

        # Listeners recieve updates to their GroupTracker page.
        self.listeners = []

    def addGroup(self, leaderId, groupStruct):
        self.leader2Group[leaderId] = list(groupStruct)

    def updateGroup(self, leaderId, category, currAvs, memberNames):
        if leaderId not in self.leader2Group:
            return
        self.leader2Group[leaderId][CATEGORY] = category
        self.leader2Group[leaderId][CURR_AVS] = currAvs
        self.leader2Group[leaderId][MEMBER_NAMES] = memberNames

        for avId in self.listeners:
            self.sendToAvatar(avId, 'updateGroup', [leaderId, category, currAvs, memberNames])

    def removeGroup(self, leaderId):
        if leaderId not in self.leader2Group:
            return
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

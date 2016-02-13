from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from GroupTrackerGlobals import *

class GlobalGroupTracker(DistributedObjectGlobal):
    def announceGenerate(self):
        DistributedObjectGlobal.announceGenerate(self)
        self.leader2Group = {}

    def requestGroups(self):
        self.sendUpdate('requestGroups', [base.localAvatar.doId])

    def doneRequesting(self):
        self.sendUpdate('doneRequesting', [base.localAvatar.doId])

    def setGroupInfo(self, leaderIds, groups):
        for leaderId, group in zip(leaderIds, groups):
            self.leader2Group[leaderId] = group

    def getGroupInfo(self):
        return self.leader2Group.values()

    def updateGroup(self, leaderId, category, currAvs):
        self.leader2Group[leaderId][CATEGORY] = category
        self.leader2Group[leaderId][CURR_AVS] = currAvs
        messenger.send('GroupTrackerResponse')
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from GroupTrackerGlobals import *
from itertools import izip


class GlobalGroupTracker(DistributedObjectGlobal):
    def announceGenerate(self):
        DistributedObjectGlobal.announceGenerate(self)
        self.leader2Group = {}

    def requestGroups(self):
        self.sendUpdate('requestGroups', [base.localAvatar.doId])

    def doneRequesting(self):
        self.sendUpdate('doneRequesting', [base.localAvatar.doId])

    def setGroupInfo(self, leaderIds, groups):
        self.leader2Group = dict(izip(leaderIds, [list(group) for group in groups]))
        messenger.send('GroupTrackerResponse')

    def getGroupInfo(self):
        return self.leader2Group.values()

    def updateGroup(self, leaderId, category, memberIds, memberNames, show):
        if leaderId not in self.leader2Group:
            return
        self.leader2Group[leaderId][CATEGORY] = category
        self.leader2Group[leaderId][MEMBER_IDS] = memberIds
        self.leader2Group[leaderId][MEMBER_NAMES] = memberNames
        self.leader2Group[leaderId][SHOW] = show
        messenger.send('GroupTrackerResponse')
        
    def showMe(self, show):
        self.sendUpdate('showMe', [show])
    

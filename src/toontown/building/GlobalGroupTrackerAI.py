from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI


class GlobalGroupTrackerAI(DistributedObjectGlobalAI):

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)

    def addGroupAI(self, leaderId, leaderName, shardName, category, memberIds, memberNames, show):
        self.sendUpdate('addGroup', [leaderId, [leaderName, shardName, category, memberIds, memberNames, show]])

    def updateGroupAI(self, leaderId, category, memberIds, memberNames, show):
        self.sendUpdate('updateGroup', [leaderId, category, memberIds, memberNames, show])
    
    def showMe(self, show):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdate('showGroup', [avId, show])

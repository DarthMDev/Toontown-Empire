from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI


class GlobalGroupTrackerAI(DistributedObjectGlobalAI):

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)

    def addGroup(self, leaderId, leaderName, shardName, category, currAvs):
        self.sendUpdate('addGroup', [leaderId, [leaderName, shardName, category, currAvs]])

    def updateGroup(self, leaderId, category, currAvs):
        self.sendUpdate('updateGroup', [leaderId, category, currAvs])

    def removeGroup(self, leaderId):
        self.sendUpdate('removeGroup', [leaderId])

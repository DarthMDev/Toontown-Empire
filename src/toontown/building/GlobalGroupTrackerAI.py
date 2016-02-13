from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI


class GlobalGroupTrackerAI(DistributedObjectGlobalAI):

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)

    def addGroup(self, leaderId, leaderName, shardName, category, currAvs, memberNames):
        self.sendUpdate('addGroup', [leaderId, [leaderName, shardName, category, currAvs, memberNames]])

    def updateGroup(self, leaderId, category, currAvs, memberNames):
        self.sendUpdate('updateGroup', [leaderId, category, currAvs, memberNames])

    def removeGroup(self, leaderId):
        self.sendUpdate('removeGroup', [leaderId])

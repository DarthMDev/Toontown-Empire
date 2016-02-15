from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.hood import ZoneUtil

class WelcomeValleyManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("WelcomeValleyManagerAI")

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.avId2Zone = {}

    def clientSetZone(self, todo0):
        pass

    def toonSetZone(self, doId, newZoneId):
        pass #TODO
        
    def requestZoneIdMessage(self, origZoneId, context):
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.avId2Zone:
            newZone = 22000
            self.avId2Zone[avId] = newZone
        elif origZoneId == 0:
            newZone = 22000
            self.avId2Zone[avId] = newZone
        else:
            newZone = ZoneUtil.getTrueZoneId(origZoneId, self.avId2Zone[avId])
        self.sendUpdateToAvatarId(avId,
            'requestZoneIdResponse', [newZone, context])

    def requestZoneIdResponse(self, todo0, todo1):
        pass


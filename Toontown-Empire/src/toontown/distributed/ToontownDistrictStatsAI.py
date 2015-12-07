from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI


class ToontownDistrictStatsAI(DistributedObjectAI):
    notify = directNotify.newCategory('ToontownDistrictStatsAI')

    districtId = 0
    avatarCount = 0
    newAvatarCount = 0
    invasionStatus = 0

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)



    def handleShardStatusQuery(self):
        # Send a shard status update containing our population:
        status = {'population': self.avatarCount}


    def setDistrictId(self, districtId):
        self.districtId = districtId

    def d_setDistrictId(self, districtId):
        self.sendUpdate('setDistrictId', [districtId])

    def b_setDistrictId(self, districtId):
        self.setDistrictId(districtId)
        self.d_setDistrictId(districtId)

    def getDistrictId(self):
        return self.districtId

    def setAvatarCount(self, avatarCount):
        self.avatarCount = avatarCount

        # Send a shard status update containing our population:
        status = {'population': self.avatarCount}


    def d_setAvatarCount(self, avatarCount):
        self.sendUpdate('setAvatarCount', [avatarCount])

    def b_setAvatarCount(self, avatarCount):
        self.d_setAvatarCount(avatarCount)
        self.setAvatarCount(avatarCount)

    def getAvatarCount(self):
        return self.avatarCount

    def setNewAvatarCount(self, newAvatarCount):
        self.newAvatarCount = newAvatarCount

    def d_setNewAvatarCount(self, newAvatarCount):
        self.sendUpdate('setNewAvatarCount', [newAvatarCount])

    def b_setNewAvatarCount(self, newAvatarCount):
        self.setNewAvatarCount(newAvatarCount)
        self.d_setNewAvatarCount(newAvatarCount)

    def getNewAvatarCount(self):
        return self.newAvatarCount

    def setInvasionStatus(self, invasionStatus):
        self.invasionStatus = invasionStatus

    def d_setInvasionStatus(self, invasionStatus):
        self.sendUpdate('setInvasionStatus', [invasionStatus])

    def b_setInvasionStatus(self, invasionStatus):
        self.setInvasionStatus(invasionStatus)
        self.d_setInvasionStatus(invasionStatus)

    def getInvasionStatus(self):
        return self.invasionStatus

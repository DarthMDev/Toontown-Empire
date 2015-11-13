from direct.directnotify.DirectNotifyGlobal import directNotify
from src.otp.avatar import AvatarDetail
from src.toontown.toon import DistributedToon

class ToonDetail(AvatarDetail.AvatarDetail):
    notify = directNotify.newCategory('ToonDetail')

    def getDClass(self):
        return 'DistributedToon'

    def createHolder(self):
        toon = DistributedToon.DistributedToon(base.cr, bFake=True)
        toon.forceAllowDelayDelete()
        return toon

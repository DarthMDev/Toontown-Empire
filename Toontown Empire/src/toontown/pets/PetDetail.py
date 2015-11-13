from direct.directnotify import DirectNotifyGlobal
from src.otp.avatar import AvatarDetail
from src.toontown.pets import DistributedPet

class PetDetail(AvatarDetail.AvatarDetail):
    notify = DirectNotifyGlobal.directNotify.newCategory('PetDetail')

    def getDClass(self):
        return 'DistributedPet'

    def createHolder(self):
        pet = DistributedPet.DistributedPet(base.cr, bFake=True)
        pet.forceAllowDelayDelete()
        pet.generateInit()
        pet.generate()
        return pet

from toontown.toonbase import ToontownGlobals
import SosShopGlobals, DistributedNPCToonBaseAI

class DistributedNPCSosAI(DistributedNPCToonBaseAI.DistributedNPCToonBaseAI):

    def restock(self, sos, amount):
        av = simbase.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not av:
            return

        newSos = av.getHp() + laff

        if newSos > av.getMaxHp():
            self.sendUpdate('rollResult', [SosShopGlobals.FULL_SOS])
            return

        cost = SosShopGlobals.CostPerSOS

        if cost > av.getTotalMoney():
            self.sendUpdate('rollResult', [SosShopGlobals.NOT_ENOUGH_MONEY])
            return

        av.takeMoney(cost)
        av.toonUp(laff)
        self.sendUpdate('rollResult', [SosShopGlobals.RESTOCK_SUCCESSFUL])
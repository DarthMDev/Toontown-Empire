from toontown.toonbase import ToontownGlobals
import SosShopGlobals, DistributedNPCToonBaseAI, random, math, NPCToons

class DistributedNPCSosAI(DistributedNPCToonBaseAI.DistributedNPCToonBaseAI):

    def roll(self, amount):
        av = simbase.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not av:
            return
        
        #Todo: Add all the Sos Card IDs to this list. It'll take a while.
        NPCIdList = [2001, 2132, 2121, 2011, 3007, 1001, 3112, 1323, 2308, 4119, 4219, 4115, 1116, 2311, 4140, 3137]
        
        count = amount
        npcIdList = list(NPCIdList)
        npcId = random.choice(npcIdList)
                  
        if npcId not in NPCToons.npcFriends:
          pass

        av.NPCFriendsDict[npcId] = count

        if count > 100:
            self.sendUpdate('rollResult', [SosShopGlobals.FULL_SOS])
            return

        cost = SosShopGlobals.CostPerSOS

        if cost > av.getTotalMoney():
            self.sendUpdate('rollResult', [SosShopGlobals.NOT_ENOUGH_MONEY])
            return

        av.takeMoney(cost)
        av.d_setNPCFriendsDict(av.NPCFriendsDict)
        self.sendUpdate('rollResult', [SosShopGlobals.ROLL_SUCCESSFUL])
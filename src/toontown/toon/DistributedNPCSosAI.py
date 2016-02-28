from toontown.toonbase import ToontownGlobals
import SosShopGlobals, DistributedNPCToonBaseAI, random, NPCToons

class DistributedNPCSosAI(DistributedNPCToonBaseAI.DistributedNPCToonBaseAI):

    def restock(self, sos, amount):
        av = simbase.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not av:
            return
        
        #Todo: Add all the Sos Card IDs to this list. It'll take a while.
        NPCIdList = [2001, 2132, 2121, 2011, 3007, 1001, 3112, 1323, 2308, 4119, 4219, 4115, 1116, 2311, 4140, 3137]
        
        count = random.randint(1, 5)
        npcIdList = list(NPCIdList)
        npcId = random.choice(npcIdList)
                  

        if npcId not in NPCToons.npcFriends:
          continue
         break

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
        self.sendUpdate('rollResult', [SosShopGlobals.RESTOCK_SUCCESSFUL])
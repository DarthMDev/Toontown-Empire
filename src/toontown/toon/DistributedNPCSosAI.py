from toontown.toonbase import ToontownGlobals
import SosShopGlobals, DistributedNPCToonBaseAI, random, math, NPCToons

class DistributedNPCSosAI(DistributedNPCToonBaseAI.DistributedNPCToonBaseAI):

    def roll(self, amount):
        av = simbase.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not av:
            return
            
        #This does not include FO sos cards.
        NPCIdList = [2001, 2132, 2121, 2011, 3007, 1001, 3112, 1323, 2308, 4119, 4219, 4115, 1116, 2311, 4140, 3137, 4327, 4230, 3135, 2208, 5124, 2003, 2126, 4007, 1315, 5207, 3129, 4125, 1329]
        
        count = amount
        npcIdList = list(NPCIdList)
        npcId = random.choice(npcIdList)
                  
        if npcId not in NPCToons.npcFriends:
          npcId = 2001

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
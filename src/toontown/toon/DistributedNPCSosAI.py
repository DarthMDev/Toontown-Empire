from toontown.toonbase import ToontownGlobals
import SosShopGlobals, DistributedNPCToonBaseAI, random, math, NPCToons

class DistributedNPCSosAI(DistributedNPCToonBaseAI.DistributedNPCToonBaseAI):

    def roll(self, amount, cost, type):
        av = simbase.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not av:
            return
            
        #This does not include FO sos cards.
        FullNPCIdList = [2001, 2132, 2121, 2011, 3007, 1001, 3112, 1323, 2308, 4119, 4219, 4115, 1116, 2311, 4140, 3137, 4327, 4230, 3135, 2208, 5124, 2003, 2126, 4007, 1315, 5207, 3129, 4125, 1329]
        #Only 3 Star Sos Cards
        ThreeStarNPCIdList = [2121, 1001, 1323, 2308, 4115, 4140, 2126, 4007, 1315, 5207, 3129, 4125, 1329]
        #Only 4 Star Sos Cards
        FourStarNPCIdList = [2132, 3007, 4219, 2311, 3137, 4327, 4230, 3135, 2208, 5124]
        #Only 5 Star Sos Cards
        FiveStarNPCIdList = [2001, 2011, 4119, 1116, 3112, 2003]
        
        count = amount
        cost = cost
        type = type
        
        if type == 2:
         npcIdList = list(FullNPCIdList)
        elif type == 3:
         npcIdList = list(ThreeStarNPCIdList)
        elif type == 4:
         npcIdList = list(FourStarNPCIdList)
        elif type == 5:
         npcIdList = list(FiveStarNPCIdList)
        else:
         npcIdList = list(FullNPCIdList)
        
        npcId = random.choice(npcIdList)
                  
        if npcId not in NPCToons.npcFriends:
          npcId = 2001

        av.NPCFriendsDict[npcId] = count

        if count > 100:
            self.sendUpdate('rollResult', [SosShopGlobals.FULL_SOS])
            return


        if cost > av.getTotalMoney():
            self.sendUpdate('rollResult', [SosShopGlobals.NOT_ENOUGH_MONEY])
            return

        av.takeMoney(cost)
        av.d_setNPCFriendsDict(av.NPCFriendsDict)
        self.sendUpdate('rollResult', [SosShopGlobals.ROLL_SUCCESSFUL])
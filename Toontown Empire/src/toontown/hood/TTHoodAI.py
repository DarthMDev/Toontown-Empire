from src.toontown.hood import HoodAI
from src.toontown.safezone import ButterflyGlobals
from src.toontown.safezone import DistributedButterflyAI
from src.toontown.safezone import DistributedTrolleyAI
from src.toontown.toon import NPCToons
from src.toontown.toonbase import TTLocalizer
from src.toontown.toonbase import ToontownGlobals
from src.toontown.ai import DistributedEffectMgrAI

class TTHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.ToontownCentral,
                               ToontownGlobals.ToontownCentral)

        self.trolley = None

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()
        if simbase.config.GetBool('want-butterflies', True):
            self.createButterflies()

        NPCToons.createNPC(
            simbase.air, 2021,
            (ToontownGlobals.ToontownCentral, TTLocalizer.NPCToonNames[2021], ('rls', 'ls', 'l', 'm', 26, 0, 26, 26, 152, 27, 139, 27, 58, 27, 0), 'm', 1, NPCToons.NPC_GLOVE),
             ToontownGlobals.ToontownCentral, posIndex=0)

        self.trickOrTreatMgr = DistributedEffectMgrAI.DistributedEffectMgrAI(self.air, ToontownGlobals.HALLOWEEN, 12)
        self.trickOrTreatMgr.generateWithRequired(2649) # All Fun and Games Shop, Silly Street

        self.winterCarolingMgr = DistributedEffectMgrAI.DistributedEffectMgrAI(self.air, ToontownGlobals.CHRISTMAS, 14)
        self.winterCarolingMgr.generateWithRequired(2659) # Joy Buzzers to the World, Silly Street

    def shutdown(self):
        HoodAI.HoodAI.shutdown(self)
        ButterflyGlobals.clearIndexes(self.zoneId)

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()

    def createButterflies(self):
        playground = ButterflyGlobals.TTC
        ButterflyGlobals.generateIndexes(self.zoneId, ButterflyGlobals.TTC)

        for i in xrange(0, ButterflyGlobals.NUM_BUTTERFLY_AREAS[ButterflyGlobals.TTC]):
            for _ in xrange(0, ButterflyGlobals.NUM_BUTTERFLIES[ButterflyGlobals.TTC]):
                butterfly = DistributedButterflyAI.DistributedButterflyAI(self.air, playground, i, self.zoneId)
                butterfly.generateWithRequired(self.zoneId)
                butterfly.start()

from src.otp.nametag.NametagConstants import CFSpeech, CFTimeout
from src.toontown.toonbase import TTLocalizer, ToontownGlobals
from src.toontown.toon import NPCToons
from DistributedNPCToonBase import DistributedNPCToonBase
import LaffRestockGlobals, LaffShopGui, time

class DistributedNPCLaffRestock(DistributedNPCToonBase):

    #zone2id = {
        #10000: 0,
        #13000: 1,
        #12000: 2,
        #11000: 3,
    #} - Storm Sellbot

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.lastCollision = 0
        self.laffDialog = None

    def disable(self):
        self.ignoreAll()
        self.destroyDialog()
        DistributedNPCToonBase.disable(self)

    #def initToonState(self): - Storm Sellbot
        #self.setAnimState('neutral', 0.9, None, None)
        #if self.name in NPCToons.LaffRestockPositions:
            #pos = NPCToons.LaffRestockPositions[self.name]
            #self.setPos(*pos[0])
            #self.setH(pos[1])
        #self.putOnSuit(self.zone2id.get(self.zoneId, -1), rental=True)

    def getCollSphereRadius(self):
        return 1.25

    def handleCollisionSphereEnter(self, collEntry):
        if self.lastCollision > time.time():
            return
        
        self.lastCollision = time.time() + ToontownGlobals.NPCCollisionDelay
        self.lookAt(base.localAvatar)
        
        if base.localAvatar.getHp() >= base.localAvatar.getMaxHp():
            self.setChatAbsolute(TTLocalizer.RestockFullLaffMessage, CFSpeech | CFTimeout)
            return
        
        base.cr.playGame.getPlace().fsm.request('stopped')
        base.setCellsAvailable(base.bottomCells, 0)
        self.destroyDialog()
        self.acceptOnce('laffShopDone', self.__laffShopDone)
        self.laffDialog = LaffShopGui.LaffShopGui()
    
    def freeAvatar(self):
        base.cr.playGame.getPlace().fsm.request('walk')
        base.setCellsAvailable(base.bottomCells, 1)
    
    def __laffShopDone(self, state, laff):
        self.freeAvatar()

        if state == LaffRestockGlobals.TIMER_END:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech|CFTimeout)
        elif state == LaffRestockGlobals.USER_CANCEL:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE, CFSpeech|CFTimeout)
        elif state == LaffRestockGlobals.RESTOCK:
            self.sendUpdate('restock', [laff])

    def restockResult(self, state):
        if state in LaffRestockGlobals.RestockMessages:
            self.setChatAbsolute(LaffRestockGlobals.RestockMessages[state], CFSpeech | CFTimeout)
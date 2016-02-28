from otp.nametag.NametagConstants import CFSpeech, CFTimeout
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toon import NPCToons
from DistributedNPCToonBase import DistributedNPCToonBase
import SosShopGlobals, SosShopGui, time, random, math

class DistributedNPCSos(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.lastCollision = 0
        self.sosDialog = None

    def disable(self):
        self.ignoreAll()
        self.destroyDialog()
        DistributedNPCToonBase.disable(self)

    def destroyDialog(self):
        self.clearChat()

        if self.sosDialog:
            self.sosDialog.destroy()
            self.sosDialog = None
    
    def initToonState(self):
        self.setAnimState('neutral', 0.9, None, None)
        self.putOnSuit(ToontownGlobals.cogHQZoneId2deptIndex(self.zoneId), rental=True)

        if self.name in NPCToons.SosShopPositions:
            pos = NPCToons.SosShopPositions[self.name]
            self.setPos(*pos[0])
            self.setH(pos[1])

    def getCollSphereRadius(self):
        return 1.25

    def handleCollisionSphereEnter(self, collEntry):
        if self.lastCollision > time.time():
            return
        
        self.lastCollision = time.time() + ToontownGlobals.NPCCollisionDelay
        self.lookAt(base.localAvatar)
        
        base.cr.playGame.getPlace().fsm.request('stopped')
        base.setCellsAvailable(base.bottomCells, 0)
        self.destroyDialog()
        self.acceptOnce('sosShopDone', self.__sosShopDone)
        self.sosDialog = SosShopGui.SosShopGui()
    
    def freeAvatar(self):
        base.cr.playGame.getPlace().fsm.request('walk')
        base.setCellsAvailable(base.bottomCells, 1)
    
    def __sosShopDone(self, state):
        self.freeAvatar()

        if state == SosShopGlobals.TIMER_END:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech|CFTimeout)
        elif state == SosShopGlobals.USER_CANCEL:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE, CFSpeech|CFTimeout)
        elif state == SosShopGlobals.ROLL:
            count = random.randint(1, 5)
            self.sendUpdate('roll', [count])

    def rollResult(self, state):
        if state in SosShopGlobals.RollMessages:
            self.setChatAbsolute(SosShopGlobals.RollMessages[state], CFSpeech | CFTimeout)
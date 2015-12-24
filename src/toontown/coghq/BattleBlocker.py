from panda3d.core import CollisionSphere
from panda3d.core import CollisionNode
from direct.interval.IntervalGlobal import Sequence
from direct.interval.IntervalGlobal import Func
from otp.level import BasicEntities
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal

class BattleBlocker(BasicEntities.DistributedNodePathEntity):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleBlocker')

    def __init__(self, cr):
        BasicEntities.DistributedNodePathEntity.__init__(self, cr)
        self.suitIds = []
        self.battleId = None
        self.in_battle = False
        self.cSphere = CollisionSphere(0, 0, 0, self.radius)
        self.cSphereNode = CollisionNode('battleBlocker-{0}-{1}'.format(self.level.getLevelId(), self.entId))
        self.cSphereNodePath = self.attachNewNode(self.cSphereNode)
        self.enterEvent = 'enter' + self.cSphereNode.getName()
        return

    def setActive(self, active):
        self.active = active

    def announceGenerate(self):
        BasicEntities.DistributedNodePathEntity.announceGenerate(self)
        self.initCollisionGeom()

    def disable(self):
        self.ignoreAll()
        self.unloadCollisionGeom()
        BasicEntities.DistributedNodePathEntity.disable(self)

    def destroy(self):
        BasicEntities.DistributedNodePathEntity.destroy(self)

    def setSuits(self, suitIds):
        self.suitIds = suitIds

    def setBattle(self, battleId):
        self.battleId = battleId

    def setBattleFinished(self):
        self.in_battle = False
        self.ignoreAll()

    def initCollisionGeom(self):
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.cSphere.setTangible(0)
        self.accept(self.enterEvent, self.__handleToonEnter)

    def unloadCollisionGeom(self):
        if hasattr(self, 'cSphereNodePath'):
            self.ignore(self.enterEvent)
            del self.cSphere
            del self.cSphereNode
            self.cSphereNodePath.removeNode()
            self.cSphereNodePath.cleanup()
            del self.cSphereNodePath

    def __handleToonEnter(self, *args):
        self.notify.debug('__handleToonEnter, {0}'.format(self.entId))
        self.in_battle = True
        self.startBattle(self.in_battle)

    def startBattle(self, in_battle = False):
        if not self.active:
            return
        callback = None
        self.in_battle = in_battle
        if self.battleId != None and self.battleId in base.cr.doId2do and not self.in_battle:
            battle = base.cr.doId2do.get(self.battleId)
            self.in_battle = True
            if battle:
                self.notify.debug('act like we collided with battle {0:d}'.format(self.battleId))
                callback = battle.handleBattleBlockerCollision
        elif self.suitIds > 0:
            for suitId in self.suitIds:
                suit = base.cr.doId2do.get(suitId)
                if suit:
                    self.notify.debug('act like we collided with Suit {0:d} ( in state {1} )'.format(suitId, suit.fsm.getCurrentState().getName()))
                    callback = suit.handleBattleBlockerCollision
                    break

        self.showReaction(callback)
        return

    @staticmethod
    def showReaction(callback = None):
        if not base.localAvatar.wantBattles:
            return
        track = Sequence()
        if callback:
            track.append(Func(callback))
        track.start()

from direct.directnotify import DirectNotifyGlobal
from src.toontown.battle.DistributedBattleBldgAI import DistributedBattleBldgAI

class DistributedCogdoBattleBldgAI(DistributedBattleBldgAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCogdoBattleBldgAI")

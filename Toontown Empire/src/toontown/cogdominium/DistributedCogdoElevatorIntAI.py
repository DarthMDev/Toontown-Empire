from direct.directnotify import DirectNotifyGlobal
from src.toontown.building.DistributedElevatorIntAI import DistributedElevatorIntAI

class DistributedCogdoElevatorIntAI(DistributedElevatorIntAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCogdoElevatorIntAI")

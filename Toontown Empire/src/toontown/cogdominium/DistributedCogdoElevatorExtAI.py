from direct.directnotify import DirectNotifyGlobal
from src.toontown.building.DistributedElevatorExtAI import DistributedElevatorExtAI

class DistributedCogdoElevatorExtAI(DistributedElevatorExtAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCogdoElevatorExtAI')

    def _createInterior(self):
        self.bldg.createCogdoInterior()

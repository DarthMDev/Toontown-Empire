from src.toontown.building.DistributedElevatorExt import DistributedElevatorExt
from src.toontown.building.ElevatorConstants import *
from src.toontown.building.ElevatorUtils import *
from src.toontown.toonbase import ToontownGlobals

class DistributedCogdoElevatorExt(DistributedElevatorExt):
    def __init__(self, cr):
        DistributedElevatorExt.__init__(self, cr)
        self.type = ELEVATOR_FIELD

    def getElevatorModel(self):
        return self.bldg.getCogdoElevatorNodePath()

    def getBldgDoorOrigin(self):
        return self.bldg.getCogdoDoorOrigin()

    def _getDoorsClosedInfo(self):
        return ('cogdoInterior', 'cogdoInterior')

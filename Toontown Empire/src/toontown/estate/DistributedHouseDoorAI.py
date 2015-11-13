from direct.directnotify import DirectNotifyGlobal
from src.toontown.building.DistributedDoorAI import DistributedDoorAI

class DistributedHouseDoorAI(DistributedDoorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedHouseDoorAI")

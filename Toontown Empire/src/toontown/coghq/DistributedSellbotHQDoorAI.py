from direct.directnotify import DirectNotifyGlobal
from src.toontown.coghq.DistributedCogHQDoorAI import DistributedCogHQDoorAI

class DistributedSellbotHQDoorAI(DistributedCogHQDoorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSellbotHQDoorAI")

    def informPlayer(self, todo0):
        pass

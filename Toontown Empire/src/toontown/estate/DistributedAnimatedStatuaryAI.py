from direct.directnotify import DirectNotifyGlobal
from src.toontown.estate.DistributedStatuaryAI import DistributedStatuaryAI

class DistributedAnimatedStatuaryAI(DistributedStatuaryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedAnimatedStatuaryAI")


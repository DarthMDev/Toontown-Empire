from direct.directnotify import DirectNotifyGlobal
from src.toontown.cogdominium.DistCogdoLevelGameAI import DistCogdoLevelGameAI

class DistCogdoBoardroomGameAI(DistCogdoLevelGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistCogdoBoardroomGameAI")

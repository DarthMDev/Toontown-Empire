from direct.directnotify import DirectNotifyGlobal
from src.toontown.parties.DistributedPartyDanceActivityBaseAI import DistributedPartyDanceActivityBaseAI

class DistributedPartyDanceActivityAI(DistributedPartyDanceActivityBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyDanceActivityAI")


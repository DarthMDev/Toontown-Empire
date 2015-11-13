from src.toontown.coghq.LawbotCogHQLoader import LawbotCogHQLoader
from src.toontown.toonbase import ToontownGlobals
from src.toontown.hood.CogHood import CogHood


class LawbotHQ(CogHood):
    notify = directNotify.newCategory('LawbotHQ')

    ID = ToontownGlobals.LawbotHQ
    LOADER_CLASS = LawbotCogHQLoader

    def load(self):
        CogHood.load(self)

        self.sky.hide()

    def enter(self, requestStatus):
        CogHood.enter(self, requestStatus)

        base.localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.LawbotHQCameraNear, ToontownGlobals.LawbotHQCameraFar)

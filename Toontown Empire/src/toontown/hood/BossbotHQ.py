from src.toontown.coghq.BossbotCogHQLoader import BossbotCogHQLoader
from src.toontown.toonbase import ToontownGlobals
from src.toontown.hood.CogHood import CogHood


class BossbotHQ(CogHood):
    notify = directNotify.newCategory('BossbotHQ')

    ID = ToontownGlobals.BossbotHQ
    LOADER_CLASS = BossbotCogHQLoader
    
    def enter(self, requestStatus):
        CogHood.enter(self, requestStatus)

        base.localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.BossbotHQCameraNear, ToontownGlobals.BossbotHQCameraFar)
        
	
    def load(self):
        CogHood.load(self)

        self.fog = Fog('BBHQFog')

    def setFog(self):
        if base.wantFog:
            self.fog.setColor(0.640625, 0.355469, 0.269531, 1.0)
            self.fog.setExpDensity(0.012)
            render.clearFog()
            render.setFog(self.fog)
            self.sky.clearFog()
            self.sky.setFog(self.fog)

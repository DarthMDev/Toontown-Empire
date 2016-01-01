from direct.directnotify import DirectNotifyGlobal
from otp.avatar.ShadowPlacer import ShadowPlacer
from panda3d.core import NodePath
from otp.otpbase import OTPGlobals
def setGlobalDropShadowFlag(flag):
    globalDropShadowFlag = 1
    if flag != globalDropShadowFlag:
        globalDropShadowFlag = flag
        messenger.send('globalDropShadowFlagChanged')

def setGlobalDropShadowGrayLevel(grayLevel):
    globalDropShadowGrayLevel = 0.5
    if grayLevel != globalDropShadowGrayLevel:
        globalDropShadowGrayLevel = grayLevel
        messenger.send('globalDropShadowGrayLevelChanged')


class ShadowCaster(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShadowCaster')

    def __init__(self, squareShadow=False):
        if squareShadow:
            self.shadowFileName = 'phase_3/models/props/square_drop_shadow'
        else:
            self.shadowFileName = 'phase_3/models/props/drop_shadow'
        self.dropShadow = None
        self.shadowPlacer = None
        self.activeShadow = 0
        self.globalDropShadowFlag = 1
        self.globalDropShadowGrayLevel = 0.5
        self.wantsActive = 1
        self.storedActiveState = 0
        if hasattr(base, 'wantDynamicShadows') and base.wantDynamicShadows:
            messenger.accept('globalDropShadowFlagChanged', self, self.__globalDropShadowFlagChanged)
            messenger.accept('globalDropShadowGrayLevelChanged', self, self.__globalDropShadowGrayLevelChanged)

    def delete(self):
        if hasattr(base, 'wantDynamicShadows') and base.wantDynamicShadows:
            messenger.ignore('globalDropShadowFlagChanged', self)
            messenger.ignore('globalDropShadowGrayLevelChanged', self)
        self.deleteDropShadow()
        self.shadowJoint = None

    def initializeDropShadow(self, hasGeomNode=True):
        self.deleteDropShadow()
        if hasGeomNode:
            self.getGeomNode().setTag('cam', 'caster')
        dropShadow = loader.loadModel(self.shadowFileName)
        dropShadow.setScale(0.4)
        dropShadow.flattenMedium()
        dropShadow.setBillboardAxis(2)
        dropShadow.setColor(0.0, 0.0, 0.0, self.globalDropShadowGrayLevel, 1)
        self.shadowPlacer = ShadowPlacer(dropShadow)#(base.shadowTrav, dropShadow, OTPGlobals.WallBitmask, OTPGlobals.FloorBitmask)
        self.dropShadow = dropShadow
        if not self.globalDropShadowFlag:
            self.dropShadow.hide()
        if self.getShadowJoint():
            dropShadow.reparentTo(self.getShadowJoint())
        else:
            self.dropShadow.hide()
        self.setActiveShadow(self.wantsActive)
        self.__globalDropShadowFlagChanged()
        self.__globalDropShadowGrayLevelChanged()

    def update(self):
        pass

    def deleteDropShadow(self):
        if self.shadowPlacer:
            self.shadowPlacer.delete()
            self.shadowPlacer = None
        if self.dropShadow:
            self.dropShadow.removeNode()
            self.dropShadow = None

    def setActiveShadow(self, isActive=1):
        isActive = isActive and self.wantsActive
        if not self.globalDropShadowFlag:
            self.storedActiveState = isActive
        if self.shadowPlacer != None:
            isActive = isActive and self.globalDropShadowFlag
            if self.activeShadow != isActive:
                self.activeShadow = isActive
                if isActive:
                    self.shadowPlacer.on()
                else:
                    self.shadowPlacer.off()

    def setShadowHeight(self, shadowHeight):
        if self.dropShadow:
            self.dropShadow.setZ(-shadowHeight)

    def getShadowJoint(self):
        if hasattr(self, 'shadowJoint'):
            return self.shadowJoint
        shadowJoint = self.find('**/attachShadow')
        if shadowJoint.isEmpty():
            self.shadowJoint = NodePath(self)
        else:
            self.shadowJoint = shadowJoint
        return self.shadowJoint

    def hideShadow(self):
        self.dropShadow.hide()

    def showShadow(self):
        if not self.globalDropShadowFlag:
            self.dropShadow.hide()
        else:
            self.dropShadow.show()

    def __globalDropShadowFlagChanged(self):
        if self.dropShadow != None:
            if self.globalDropShadowFlag == 0:
                if self.activeShadow == 1:
                    self.storedActiveState = 1
                    self.setActiveShadow(0)
            elif self.activeShadow == 0:
                self.setActiveShadow(1)
            self.showShadow()

    def __globalDropShadowGrayLevelChanged(self):
        if self.dropShadow != None:
            self.dropShadow.setColor(0.0, 0.0, 0.0, self.globalDropShadowGrayLevel, 1)

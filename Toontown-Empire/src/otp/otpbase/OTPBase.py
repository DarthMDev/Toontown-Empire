from direct.showbase.ShowBase import ShowBase
from otp.ai.MagicWordGlobal import *
from otp.chat import WhiteList, WhiteListData, SequenceListData
from panda3d.core import Camera, TPLow, VBase4, ColorWriteAttrib, Filename, getModelPath, NodePath, Vec4
import OTPGlobals, OTPRender, math

class OTPBase(ShowBase):

    def __init__(self, windowType = None):
        ShowBase.__init__(self, windowType=windowType)
        self.idTags = config.GetBool('want-id-tags', 0)
        if not self.idTags:
            del self.idTags
        self.wantNametags = self.config.GetBool('want-nametags', 1)
        self.wantDynamicShadows = 1
        self.stereoEnabled = False
        self.whiteList = None
        if config.GetBool('want-whitelist', True):
            self.whiteList = WhiteList.WhiteList()
            self.whiteList.setWords(WhiteListData.WHITELIST)

            if config.GetBool('want-sequence-list', True):
                self.whiteList.setSequenceList(SequenceListData.SEQUENCES)
        
        base.cam.node().setCameraMask(OTPRender.MainCameraBitmask)
        taskMgr.setupTaskChain('net', numThreads=1, frameBudget=0.001, threadPriority=TPLow)

    def getRepository(self):
        return self.cr

    def run(self):
        try:
            taskMgr.run()
        except SystemExit:
            self.notify.info('Normal exit.')
            self.destroy()
            raise
        except:
            self.notify.warning('Handling Python exception.')
            if getattr(self, 'cr', None):
                if self.cr.timeManager:
                    from otp.otpbase import OTPGlobals
                    self.cr.timeManager.setDisconnectReason(OTPGlobals.DisconnectPythonError)
                    self.cr.timeManager.setExceptionInfo()
                self.cr.sendDisconnect()
            self.notify.info('Exception exit.\n')
            self.destroy()
            import traceback
            traceback.print_exc()


@magicWord(category=CATEGORY_STAFF)
def oobe():
    """
    Toggle the 'out of body experience' view.
    """
    base.oobe()

@magicWord(category=CATEGORY_STAFF)
def oobeCull():
    """
    Toggle the 'out of body experience' view with culling debugging.
    """
    base.oobeCull()

@magicWord(category=CATEGORY_LEADER)
def wire():
    """
    Toggle the 'wireframe' view.
    """
    base.toggleWireframe()

@magicWord(category=CATEGORY_LEADER)
def idNametags():
    """
    Display avatar IDs inside nametags.
    """
    messenger.send('nameTagShowAvId')

@magicWord(category=CATEGORY_LEADER)
def nameNametags():
    """
    Display only avatar names inside nametags.
    """
    messenger.send('nameTagShowName')

@magicWord(category=CATEGORY_LEADER)
def a2d():
    """
    Toggle aspect2d.
    """
    if aspect2d.isHidden():
        aspect2d.show()
    else:
        aspect2d.hide()

@magicWord(category=CATEGORY_LEADER)
def placer():
    """
    Toggle the camera placer.
    """
    base.camera.place()

@magicWord(category=CATEGORY_LEADER)
def explorer():
    """
    Toggle the scene graph explorer.
    """
    base.render.explore()


@magicWord(category=CATEGORY_LEADER)
def neglect():
    """
    toggle the neglection of network updates on the invoker's client.
    """
    if base.cr.networkPlugPulled():
        base.cr.restoreNetworkPlug()
        return 'You are no longer neglecting network updates.'
    else:
        base.cr.pullNetworkPlug()
        return 'You are now neglecting network updates.'


@magicWord(category=CATEGORY_LEADER, types=[float, float, float, float])
def backgroundColor(r=None, g=1, b=1, a=1):
    """
    set the background color. Specify no arguments for the default background
    color.
    """
    if r is None:
        r, g, b, a = OTPGlobals.DefaultBackgroundColor
    base.setBackgroundColor(Vec4(r, g, b, a))
    return 'The background color has been changed.'

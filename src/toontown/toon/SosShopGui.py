from direct.gui.DirectGui import *
from direct.task.Task import Task
from otp.otpbase import OTPLocalizer
from toontown.toonbase import ToontownGlobals, TTLocalizer, ToontownTimer
import SosShopGlobals

try:
 from panda3d.core import *
except:
 pass

#TODO: Fix Text Color For The Gui.

class SosShopGui(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, parent=aspect2d, relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(1.33, 1, 1.3), pos=(0, 0, 0), text='', text_scale=0.07, text_pos=(0, 0.475))
        self.initialiseoptions(SosShopGui)
        
        self.extraState = 0
        self.buyState = 0
        self.cost = 5000
        self.ok = True
        self.holdState = SosShopGlobals.MinimumState
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(aspect2d)
        self.timer.posInTopRightCorner()
        self.timer.countdown(SosShopGlobals.TIMER_SECONDS, self.__cancel, [SosShopGlobals.TIMER_END])
        self.setupButtons()
        self.bindButtons()
        self.setupText()
        self.__updateRollInfo(0)
        self.__updateStatusText(SosShopGlobals.MinimumState)

    def setupText(self):
        self.info = DirectLabel(guiId='SosKeeperInfo', parent=self, relief=None, text="", text_align=TextNode.ALeft, text_scale=TTLocalizer.SRIStip, textMayChange=1, pos=(-0.6, 0.6, 0.5), text_wordwrap=15)
        self.status = DirectLabel(guiId='SosKeeperStatus', parent=self, relief=None, text="", text_align=TextNode.ALeft, text_scale=TTLocalizer.SREStip, textMayChange=1, pos=(-0.6, 0, -0.5), text_wordwrap=15)
    
    def setupButtons(self):
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        arrowGui = loader.loadModel('phase_3/models/gui/create_a_toon_gui')
        arrowImageList = (arrowGui.find('**/CrtATn_R_Arrow_UP'), arrowGui.find('**/CrtATn_R_Arrow_DN'), arrowGui.find('**/CrtATn_R_Arrow_RLVR'), arrowGui.find('**/CrtATn_R_Arrow_UP'))

        
        self.cancelButton = DirectButton(parent=self, relief=None, image=(buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), pos=(-0.2, 0, -0.5), text=OTPLocalizer.lCancel, text_scale=0.06, text_pos=(0, -0.1), command=self.__cancel, extraArgs=[SosShopGlobals.USER_CANCEL])
        self.okButton = DirectButton(parent=self, relief=None, image=(buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr')), pos=(0.2, 0, -0.5), text=OTPLocalizer.lOK, text_scale=0.06, text_pos=(0, -0.1), command=self.__roll)
        self.upArrow = DirectButton(parent=self, relief=None, image=arrowImageList, image_scale=(1, 1, 1), image3_color=Vec4(0.6, 0.6, 0.6, 0.25), pos=(0.2, 0, -0.265))
        self.downArrow = DirectButton(parent=self, relief=None, image=arrowImageList, image_scale=(-1, 1, 1), image3_color=Vec4(0.6, 0.6, 0.6, 0.25), pos=(-0.2, 0, -0.265))
        
        buttons.removeNode()
        arrowGui.removeNode()

    def bindButtons(self):
        self.downArrow.bind(DGG.B1PRESS, self.__taskUpdate, extraArgs=[-1])
        self.downArrow.bind(DGG.B1RELEASE, self.__taskDone)
        self.upArrow.bind(DGG.B1PRESS, self.__taskUpdate, extraArgs=[1])
        self.upArrow.bind(DGG.B1RELEASE, self.__taskDone)
        
      
    def destroy(self):
        self.ignoreAll()

        if self.timer:
            self.timer.destroy()
            self.timer = None
        if self.info:
            self.info.remove()
            self.info = None
        if self.status:
            self.status.remove()
            self.status = None 

        taskMgr.remove(self.taskName('runRollCounter'))
        DirectFrame.destroy(self)
        
    def __updateStatusText(self, newState):
     if newState == 2:
      self.info['text'] = SosShopGlobals.AnyInfoText
      self.status['text'] = SosShopGlobals.AnySosText
      self.cost = 5000
     elif newState == 3:
      self.info['text'] = SosShopGlobals.ThreeStarInfoText
      self.status['text'] = SosShopGlobals.ThreeStarSosText
      self.cost = 7000
     elif newState == 4:
      self.info['text'] = SosShopGlobals.FourStarInfoText     
      self.status['text'] = SosShopGlobals.FourStarSosText
      self.cost = 9000
     elif newState == 5:
      self.info['text'] = SosShopGlobals.FiveStarInfoText
      self.status['text'] = SosShopGlobals.FiveStarSosText
      self.cost = 12000
     else:
      self.info['text'] = "Please consult an admin or staff member on the game or website as an error has occured!"
      self.status['text'] = "An error has occured!"
      self.ok = False
      self.cost = 99999
     #Money Check
     if self.cost > base.localAvatar.getTotalMoney() and self.ok:
        print("SosShopGui: LocalToon is out of money!")
     elif self.cost < base.localAvatar.getTotalMoney() and self.ok:
        self.okButton['state'] = DGG.NORMAL
     elif not self.ok:
        self.okButton['state'] = DGG.DISABLED    
     else:
       self.okButton['state'] = DGG.DISABLED

    def __cancel(self, state):
        self.destroy()
        cost = 0
        type = 0
        messenger.send('sosShopDone', [state, cost, type])

    def __roll(self):
        cost = self.cost
        type = self.buyState
        self.destroy()
        messenger.send('sosShopDone', [SosShopGlobals.ROLL, cost, type])

    def __updateRollInfo(self, rollState):
        self.extraState += rollState
        hitLimit = 0
        newState = self.holdState + self.extraState
        

        if newState <= SosShopGlobals.ResetState:
         newState == 5
        else: 
         pass
        
        if newState <= SosShopGlobals.UnderState:
         newState == 2
        else: 
         pass
        
        if newState <= SosShopGlobals.MinimumState:
            self.downArrow['state'] = DGG.DISABLED
            hitLimit = 1
        else:
            self.downArrow['state'] = DGG.NORMAL
            
        if newState >= SosShopGlobals.MaximumState:
            self.upArrow['state'] = DGG.DISABLED
            hitLimit = 1
        else:
            self.upArrow['state'] = DGG.NORMAL 
            
        self.__updateStatusText(newState)
        self.buyState = newState

        return hitLimit

    def __runTask(self, task):
        if task.time - task.prevTime < task.delayTime:
            return Task.cont
        else:
            task.delayTime = max(0.05, task.delayTime * 0.75)
            task.prevTime = task.time
            updateLimit = self.__updateRollInfo(task.delta)

            return Task.done if updateLimit else Task.cont

    def __taskDone(self, event):
        messenger.send('wakeup')
        taskMgr.remove(self.taskName('runRollCounter'))

    def __taskUpdate(self, delta, event):
        messenger.send('wakeup')

        task = Task(self.__runTask)
        task.delayTime = 0.4
        task.prevTime = 0.0
        task.delta = delta
        updateLimit = self.__updateRollInfo(delta)

        if not updateLimit:
            taskMgr.add(task, self.taskName('runRollCounter'))
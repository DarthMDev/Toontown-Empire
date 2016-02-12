from direct.interval.IntervalGlobal import *
from direct.gui import OnscreenText, OnscreenImage
from otp.nametag import NametagGlobals
from toontown.toonbase import ToontownGlobals, TTLocalizer
import TTStreet

class TutorialStreet(TTStreet.TTStreet):

    def enter(self, requestStatus):
        TTStreet.TTStreet.enter(self, requestStatus, visibilityFlag=0, arrowsOn=0)
        print('TutorialStreet(debug): %s' % requestStatus['how'])
        if requestStatus['how'] == 'teleportIn':
            self.startWelcomeCutscene()
    
    def startWelcomeCutscene(self):
        cells = base.bottomCells + base.leftCells + base.rightCells
        
        base.localAvatar.initCameraPositions()
        base.cam.setPosHpr(-79.5, 160, 105, 60, 0, 0)
        base.cam.reparentTo(render)
        base.setCellsAvailable(cells, 0)
        
        welcomeText = OnscreenText.OnscreenText(TTLocalizer.TutorialWelcome, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1), font=ToontownGlobals.getToonFont(), pos=(0, 0.8), scale=0.16, mayChange=1, wordwrap=16)
        gameLogo = OnscreenImage.OnscreenImage('phase_3/maps/toontown-logo.png', scale=(1.2, 0, 0.6), pos=(-0.05, 0, -0.15))
        gameLogo.setTransparency(TransparencyAttrib.MAlpha)
        gameLogo.setBin('fixed', 20)
        gameLogo.hide()
        
        cutscene = Sequence(
            Wait(0.1),
            Func(self.fsm.request, 'stopped'),
            Func(base.localAvatar.setPosHpr, 49.5, 16.5, -0.475, 90, 0, 0),
            welcomeText.colorScaleInterval(1.5, (1, 1, 1, 1), (1, 1, 1, 0)),
            Wait(2),
            Func(gameLogo.show),
            gameLogo.colorScaleInterval(1.5, (1, 1, 1, 1), (1, 1, 1, 0)),
            Wait(2),
            Parallel(welcomeText.colorScaleInterval(1.5, (1, 1, 1, 0)), gameLogo.colorScaleInterval(1.5, (1, 1, 1, 0))),
            Func(welcomeText.removeNode),
            Func(gameLogo.removeNode),
            Wait(1),
            Func(base.transitions.irisOut, 0.5),
            Wait(0.6),
            Func(base.cam.setPosHpr, base.localAvatar.cameraPositions[0][0], (0, 0, 0)),
            Func(base.cam.reparentTo, base.localAvatar),
            Wait(0.4),
            Func(base.transitions.irisIn, 0.5),
            Wait(0.5),
            Func(base.setCellsAvailable, cells, 1),
            Func(self.fsm.request, 'walk'))
        
        cutscene.start()

    def exit(self):
        TTStreet.TTStreet.exit(self, visibilityFlag=0)

    def enterTeleportIn(self, requestStatus):
        TTStreet.TTStreet.enterTeleportIn(self, requestStatus)

    def enterTownBattle(self, event):
        self.loader.townBattle.enter(event, self.fsm.getStateNamed('battle'), tutorialFlag=1)

    def handleEnterTunnel(self, requestStatus, collEntry):
        messenger.send('stopTutorial')
        TTStreet.TTStreet.handleEnterTunnel(self, requestStatus, collEntry)

    def exitDoorIn(self):
        base.localAvatar.obscureMoveFurnitureButton(0)

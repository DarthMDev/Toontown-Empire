from direct.interval.IntervalGlobal import *
from direct.gui import OnscreenText, OnscreenImage
from otp.nametag import NametagGlobals
from toontown.toonbase import ToontownGlobals, TTLocalizer
import TTStreet

class TutorialStreet(TTStreet.TTStreet):

    def enter(self, requestStatus):
        TTStreet.TTStreet.enter(self, requestStatus, visibilityFlag=0, arrowsOn=0)


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

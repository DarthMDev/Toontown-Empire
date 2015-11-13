from panda3d.core import *
from direct.gui.DirectGui import *
from src.toontown.toonbase import ToontownGlobals
from src.toontown.toonbase import TTLocalizer
from src.toontown.hood import ZoneUtil
import random

LOADING_SCREEN_SORT_INDEX = 4000

class ToontownLoadingScreen:

    def __init__(self):
        self.__expectedCount = 0
        self.__count = 0
        self.gui = loader.loadModel('phase_3/models/gui/progress-background.bam')
        self.title = DirectLabel(guiId='ToontownLoadingScreenTitle', parent=self.gui, relief=None, pos=(base.a2dRight/5, 0, 0.235), text='', textMayChange=1, text_scale=0.08, text_fg=(0, 0, 0.5, 1), text_align=TextNode.ALeft, text_font=ToontownGlobals.getInterfaceFont())
        self.tip = DirectLabel(guiId='ToontownLoadingScreenTip', parent=self.gui, relief=None, pos=(0, 0, 0.045), text='', textMayChange=1, text_scale=0.05, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_align=TextNode.ACenter)
        self.waitBar = DirectWaitBar(guiId='ToontownLoadingScreenWaitBar', parent=self.gui, frameSize=(base.a2dLeft+(base.a2dRight/4.95), base.a2dRight-(base.a2dRight/4.95), -0.03, 0.03), pos=(0, 0, 0.15), text='')
        logoScale = 0.5625  # Scale for our locked aspect ratio (2:1).
        self.logo = OnscreenImage(
            image='phase_3/maps/toontown-logo.png',
            scale=(logoScale * 2.0, 1, logoScale))
        self.logo.reparentTo(hidden)
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        scale = self.logo.getScale()
        self.logo.setPos(0, 0, -scale[2])
        self.toon = None

    def destroy(self):
        self.tip.destroy()
        self.title.destroy()
        self.gui.removeNode()
        self.logo.removeNode()

    def getTip(self, tipCategory):
        return TTLocalizer.TipTitle + ' ' + random.choice(TTLocalizer.TipDict.get(tipCategory))

    def begin(self, range, label, gui, tipCategory, zoneId):
        self.defaultTex = 'phase_3.5/maps/loading/default.jpg'
        self.defaultFont = ToontownGlobals.getInterfaceFont()
        self.defaultFontColor = (0, 0, 0.5, 1)
        self.zone2picture = {
            ToontownGlobals.GoofySpeedway : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.ToontownCentral : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.SillyStreet : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.LoopyLane : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.PunchlinePlace : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.DonaldsDock : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.BarnacleBoulevard : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.SeaweedStreet : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.LighthouseLane : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.DaisyGardens : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.ElmStreet : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.MapleStreet : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.OakStreet : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.MinniesMelodyland : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.AltoAvenue : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.BaritoneBoulevard : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.TenorTerrace : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.TheBrrrgh : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.WalrusWay : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.SleetStreet : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.PolarPlace : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.DonaldsDreamland : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.LullabyLane : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.PajamaPlace : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.OutdoorZone : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.GolfZone : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.SellbotHQ : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.SellbotFactoryExt : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.SellbotFactoryInt : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.SellbotMegaCorpInt : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.CashbotHQ : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.LawbotHQ : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.BossbotHQ : 'phase_3.5/maps/loading/toon.jpg'
        }
        self.zone2font = {
            #Toontown Central Loader Fonts 
            ToontownGlobals.GoofySpeedway : ToontownGlobals.getSignFont(),
            ToontownGlobals.ToontownCentral : ToontownGlobals.getCentralFont(),
            ToontownGlobals.SillyStreet : ToontownGlobals.getCentralFont(),
            ToontownGlobals.LoopyLane : ToontownGlobals.getCentralFont(),
            ToontownGlobals.PunchlinePlace : ToontownGlobals.getCentralFont(),
            #Donalds Dock Loader Fonts
            ToontownGlobals.DonaldsDock : ToontownGlobals.getDockFont(),
            ToontownGlobals.BarnacleBoulevard : ToontownGlobals.getDockFont(),
            ToontownGlobals.SeaweedStreet : ToontownGlobals.getDockFont(),
            ToontownGlobals.LighthouseLane : ToontownGlobals.getDockFont(),
            #Daisys Gardens Loader Fonts
            ToontownGlobals.DaisyGardens : ToontownGlobals.getGardenFont(),
            ToontownGlobals.ElmStreet : ToontownGlobals.getGardenFont(),
            ToontownGlobals.MapleStreet : ToontownGlobals.getGardenFont(),
            ToontownGlobals.OakStreet : ToontownGlobals.getGardenFont(),
            #Minnies Melodyland Loader Fonts
            ToontownGlobals.MinniesMelodyland : ToontownGlobals.getMelodyFont(),
            ToontownGlobals.AltoAvenue : ToontownGlobals.getMelodyFont(),
            ToontownGlobals.BaritoneBoulevard : ToontownGlobals.getMelodyFont(),
            ToontownGlobals.TenorTerrace : ToontownGlobals.getMelodyFont(),
            #Brghhh Loader Fonts
            ToontownGlobals.TheBrrrgh : ToontownGlobals.getFrostFont(),
            ToontownGlobals.WalrusWay : ToontownGlobals.getFrostFont(),
            ToontownGlobals.SleetStreet : ToontownGlobals.getFrostFont(),
            ToontownGlobals.PolarPlace : ToontownGlobals.getFrostFont(),
            #Donalds Dreamland Loader Fonts
            ToontownGlobals.DonaldsDreamland : ToontownGlobals.getDreamFont(),
            ToontownGlobals.LullabyLane : ToontownGlobals.getDreamFont(),
            ToontownGlobals.PajamaPlace : ToontownGlobals.getDreamFont(),
            #Other Zone Fonts
            ToontownGlobals.OutdoorZone : ToontownGlobals.getSignFont(),
            ToontownGlobals.GolfZone : ToontownGlobals.getSignFont(),
            #Cog Loader Fonts (Never edit, they are good as they currently are)
            ToontownGlobals.SellbotHQ : ToontownGlobals.getSuitFont(),
            ToontownGlobals.SellbotFactoryExt : ToontownGlobals.getSuitFont(),
            ToontownGlobals.SellbotFactoryInt : ToontownGlobals.getSuitFont(),
            ToontownGlobals.SellbotMegaCorpInt : ToontownGlobals.getSuitFont(),
            ToontownGlobals.CashbotHQ : ToontownGlobals.getSuitFont(),
            ToontownGlobals.LawbotHQ : ToontownGlobals.getSuitFont(),
            ToontownGlobals.BossbotHQ : ToontownGlobals.getSuitFont()
        }
        self.zone2fontcolor = {
            ToontownGlobals.GoofySpeedway : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.ToontownCentral : VBase4(0.9803921568627451, 0.8235294117647059, 0.0392156862745098, 1.0),
            ToontownGlobals.SillyStreet : VBase4(0.9803921568627451, 0.8235294117647059, 0.0392156862745098, 1.0),
            ToontownGlobals.LoopyLane : VBase4(0.9803921568627451, 0.8235294117647059, 0.0392156862745098, 1.0),
            ToontownGlobals.PunchlinePlace : VBase4(0.9803921568627451, 0.8235294117647059, 0.0392156862745098, 1.0),
            ToontownGlobals.DonaldsDock : VBase4(0.6901960784313725, 0.4274509803921569, 0.0549019607843137, 1.0),
            ToontownGlobals.BarnacleBoulevard : VBase4(0.6901960784313725, 0.4274509803921569, 0.0549019607843137, 1.0),
            ToontownGlobals.SeaweedStreet : VBase4(0.6901960784313725, 0.4274509803921569, 0.0549019607843137, 1.0),
            ToontownGlobals.LighthouseLane : VBase4(0.6901960784313725, 0.4274509803921569, 0.0549019607843137, 1.0),
            ToontownGlobals.DaisyGardens : VBase4(0.1647058823529412, 0.7490196078431373, 0.4509803921568627, 1.0),
            ToontownGlobals.ElmStreet : VBase4(0.1647058823529412, 0.7490196078431373, 0.4509803921568627, 1.0),
            ToontownGlobals.MapleStreet : VBase4(0.1647058823529412, 0.7490196078431373, 0.4509803921568627, 1.0),
            ToontownGlobals.OakStreet : VBase4(0.1647058823529412, 0.7490196078431373, 0.4509803921568627, 1.0),
            ToontownGlobals.MinniesMelodyland : VBase4(0.9294117647058824, 0.0196078431372549, 0.7333333333333333, 1.0),
            ToontownGlobals.AltoAvenue : VBase4(0.9294117647058824, 0.0196078431372549, 0.7333333333333333, 1.00),
            ToontownGlobals.BaritoneBoulevard : VBase4(0.9294117647058824, 0.0196078431372549, 0.7333333333333333, 1.0),
            ToontownGlobals.TenorTerrace : VBase4(0.9294117647058824, 0.0196078431372549, 0.7333333333333333, 1.0),
            ToontownGlobals.TheBrrrgh : VBase4(0.792156862745098, 0.8823529411764706, 1.0, 1.0),
            ToontownGlobals.WalrusWay : VBase4(0.792156862745098, 0.8823529411764706, 1.0, 1.0),
            ToontownGlobals.SleetStreet : VBase4(0.792156862745098, 0.8823529411764706, 1.0, 1.0),
            ToontownGlobals.PolarPlace : VBase4(0.792156862745098, 0.8823529411764706, 1.0, 1.0),
            ToontownGlobals.DonaldsDreamland : VBase4(0.4313725490196078, 0.196078431372549, 0.7607843137254902, 1.0),
            ToontownGlobals.LullabyLane : VBase4(0.4313725490196078, 0.196078431372549, 0.7607843137254902, 1.0),
            ToontownGlobals.PajamaPlace : VBase4(0.4313725490196078, 0.196078431372549, 0.7607843137254902, 1.0),
            ToontownGlobals.OutdoorZone : VBase4(0.4313725490196078, 0.196078431372549, 0.7607843137254902, 1.0),
            ToontownGlobals.GolfZone : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.SellbotHQ : (0.0056754360035471, 0.0666666666666667, 0.9607843137254902, 1.0),
            ToontownGlobals.SellbotFactoryExt : (0.0056754360035471, 0.0666666666666667, 0.9607843137254902, 1.0),
            ToontownGlobals.SellbotFactoryInt : (0.0056754360035471, 0.0666666666666667, 0.9607843137254902, 1.0),
            ToontownGlobals.SellbotMegaCorpInt : ((0.0056754360035471, 0.0666666666666667, 0.9607843137254902, 1.0)),
            ToontownGlobals.CashbotHQ : (0.2274509803921569, 0.7215686274509804, 0.0509803921568627, 1.0),
            ToontownGlobals.LawbotHQ : (0.1294117647058824, 0.2549019607843137, 0.8705882352941176, 1.0),
            ToontownGlobals.BossbotHQ : (0.7215686274509804, 0.5098039215686275, 0.2509803921568627, 1.0)
        }

        self.waitBar['range'] = range
        self.title['text'] = label
        self.loadingScreenTex = self.zone2picture.get(ZoneUtil.getBranchZone(zoneId), self.defaultTex)
        self.loadingScreenFont = self.zone2font.get(ZoneUtil.getBranchZone(zoneId), self.defaultFont)
        self.loadingScreenFontColor = self.zone2fontcolor.get(ZoneUtil.getBranchZone(zoneId), self.defaultFontColor)
        self.background = loader.loadTexture(self.loadingScreenTex)
        self.__count = 0
        self.__expectedCount = range
        if gui:
            if base.localAvatarStyle:
                from src.toontown.toon import Toon 
                wave = {'emote': 'wave', 'frame':25}
                shrug = {'emote':'shrug', 'frame':30}
                duck = {'emote':'duck', 'frame':40}
                up = {'emote':'up', 'frame':60}
                pushup = {'emote':'down', 'frame':23}
                bow = {'emote':'bow', 'frame':45}
                bored = {'emote':'bored', 'frame':135} 
                run = {'emote':'run', 'frame':7}
                victory = {'emote':'victory', 'frame':10}
                applause = {'emote':'applause', 'frame':23}
                dust = {'emote':'sprinkle-dust', 'frame':40}
                hypno = {'emote':'hypnotize', 'frame':25}
                cringe = {'emote':'cringe', 'frame':25}
                emotelist = [wave, shrug, duck, up, pushup, bow, 
                            bored, run, victory, applause, dust, hypno, cringe]
                emotechosen = random.choice(emotelist)
                self.toon = Toon.Toon()
                self.toon.setDNA(base.localAvatarStyle)
                self.toon.pose(emotechosen['emote'], emotechosen['frame'])
                self.toon.getGeomNode().setDepthWrite(1)
                self.toon.getGeomNode().setDepthTest(1)
                self.toon.setHpr(205, 0, 0)
                self.toon.setScale(0.18)
                self.toon.setPos(base.a2dBottomRight.getX()/1.25, 0, -0.034)
                self.toon.reparentTo(self.waitBar)
            self.waitBar['frameSize'] = (base.a2dLeft+(base.a2dRight/4.95), base.a2dRight-(base.a2dRight/4.95), -0.03, 0.03)
            self.title['text_font'] = self.loadingScreenFont
            self.title['text_fg'] = self.loadingScreenFontColor
            self.title.reparentTo(base.a2dpBottomLeft, LOADING_SCREEN_SORT_INDEX)
            self.title.setPos(base.a2dRight/5, 0, 0.235)
            self.tip['text'] = self.getTip(tipCategory)
            self.gui.setPos(0, -0.1, 0)
            self.gui.reparentTo(aspect2d, LOADING_SCREEN_SORT_INDEX)
            self.gui.setTexture(self.background, 1)
            #if self.loadingScreenTex == self.defaultTex:
            #    self.logo.reparentTo(base.a2dpTopCenter, LOADING_SCREEN_SORT_INDEX)
            self.logo.reparentTo(base.a2dpTopCenter, LOADING_SCREEN_SORT_INDEX)
        else:
            self.title.reparentTo(base.a2dpBottomLeft, LOADING_SCREEN_SORT_INDEX)
            self.gui.reparentTo(hidden)
            self.logo.reparentTo(hidden)
        self.tip.reparentTo(base.a2dpBottomCenter, LOADING_SCREEN_SORT_INDEX)
        self.waitBar.reparentTo(base.a2dpBottomCenter, LOADING_SCREEN_SORT_INDEX)
        self.waitBar.update(self.__count)

    def end(self):
        self.waitBar.finish()
        self.waitBar.reparentTo(self.gui)
        self.title.reparentTo(self.gui)
        self.tip.reparentTo(self.gui)
        self.gui.reparentTo(hidden)
        if self.toon:
            self.toon.reparentTo(hidden)
        self.logo.reparentTo(hidden)
        return (self.__expectedCount, self.__count)

    def abort(self):
        self.gui.reparentTo(hidden)

    def tick(self):
        self.__count = self.__count + 1
        self.waitBar.update(self.__count)

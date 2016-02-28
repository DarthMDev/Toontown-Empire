from panda3d.core import NodePath, Vec4, TextNode, CardMaker, TransparencyAttrib

from direct.interval.IntervalGlobal import LerpColorScaleInterval, Sequence, Func, Wait, Parallel

from toontown.achievements import Achievements
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer


achievementModel = loader.loadModel('phase_3.5/models/gui/achievement_set.bam')
achievementSfx = base.loadSfx('phase_3.5/audio/sfx/poof_in.ogg')
lockTexture = loader.loadTexture('phase_3.5/maps/achievement_lock.png')

CategoryModels = {
    Achievements.BRONZE: achievementModel.find('**/achievement1'),
    Achievements.SILVER: achievementModel.find('**/achievement2'),
    Achievements.GOLD: achievementModel.find('**/achievement3'),
    Achievements.PLATINUM: achievementModel.find('**/achievement4')
}


class AchievementNode(NodePath):
    def __init__(self, achievementId, faded=False, locked=False):
        NodePath.__init__(self, hidden.attachNewNode('achievement-%s-%s' % (achievementId, id(self))))

        self.achievementId = achievementId
        self.category = Achievements.getAchievementCategory(self.achievementId)

        CategoryModels[self.category].copyTo(self)

        if not faded:
            self.generateAchievementInfo()

            if locked:
                cm = CardMaker('lock')
                lock = self.attachNewNode(cm.generate())
                lock.setTransparency(TransparencyAttrib.MAlpha)
                lock.setTexture(lockTexture)
                lock.setScale(0.35)
                lock.setPos(1.5, 0, -0.025)
                lock.setColorScale(0, 0, 0, 0.6)

        if faded:
            self.setColorScale(0, 0, 0, 0.1)

        self.flattenStrong()

    def generateAchievementInfo(self):
        acievementInfo = TTLocalizer.getAchievementInfo(self.achievementId)

        title = TextNode('title')
        title.setText(acievementInfo[0])
        title.setFont(ToontownGlobals.getSignFont())
        title.setTextColor(1, 1, 1, 1)
        title.setAlign(TextNode.ACenter)

        titleNode = self.attachNewNode(title)
        titleNode.setScale(0.2)
        titleNode.setZ(0.2)

        description = TextNode('description')
        description.setText(acievementInfo[1])
        description.setFont(ToontownGlobals.getSignFont())
        description.setTextColor(1, 1, 1, 1)
        description.setAlign(TextNode.ACenter)

        descriptionNode = self.attachNewNode(description)
        descriptionNode.setScale(0.15)
        descriptionNode.setZ(-0.14)


class AchievementPopup(NodePath):
    def __init__(self, achievementId):
        NodePath.__init__(self, hidden.attachNewNode('achievement-popup-%s' % id(self)))

        AchievementNode(achievementId).reparentTo(self)

        self.reparentTo(base.a2dTopCenter, 4000)
        self.stash()

        self.setScale(0.3)
        self.setZ(-0.18)

        self.callback = None

    def setCallback(self, callback):
        self.callback = callback

    def doCallback(self):
        if self.callback is not None:
            self.callback()

    def cleanup(self):
        self.removeNode()

    def play(self):
        Sequence(
            Parallel(
                Sequence(
                    Func(self.unstash),
                    Func(self.setTransparency, 1),
                    LerpColorScaleInterval(self, 1.2, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0)),
                    Func(self.clearColorScale),
                    Func(self.clearTransparency)
                ),
                Func(base.playSfx, achievementSfx)
            ),
            Wait(2.5),
            Sequence(
                Func(self.setTransparency, 1),
                LerpColorScaleInterval(self, 0.4, Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1)),
                Func(self.clearColorScale),
                Func(self.clearTransparency),
                Func(self.stash)
            ),
            Func(self.cleanup),
            Func(self.doCallback)
        ).start()


class AchievementsGUI:
    def __init__(self):
        self.queue = []
        self.playing = False

    def showAchievement(self, achievementId):
        popup = AchievementPopup(achievementId)
        self.queue.append(popup)

        if self.playing is False:
            self.playing = True
            self.showNext()

    def showNext(self):
        if len(self.queue) == 0:
            self.playing = False
            return

        popup = self.queue.pop(0)
        popup.setCallback(self.showNext)
        popup.play()

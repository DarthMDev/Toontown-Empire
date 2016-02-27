from panda3d.core import NodePath
from panda3d.core import TextNode

from direct.gui.DirectWaitBar import DirectWaitBar
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from direct.gui import DirectGuiGlobals as DGG

from toontown.shtiker.ShtikerPage import ShtikerPage
from toontown.achievements.AchievementsGUI import AchievementNode
from toontown.achievements import Achievements
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

from collections import OrderedDict


gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
arrowUp = gui.find('**/tt_t_gui_mat_shuffleArrowUp')
arrowDown = gui.find('**/tt_t_gui_mat_shuffleArrowDown')
arrowRollover = gui.find('**/tt_t_gui_mat_shuffleArrowUp')
arrowDisabled = gui.find('**/tt_t_gui_mat_shuffleArrowDisabled')
gui.removeNode()

halfButtonScale = (0.6, 0.6, 0.6)
halfButtonHoverScale = (0.7, 0.7, 0.7)
halfButtonInvertScale = (-0.6, 0.6, 0.6)
halfButtonInvertHoverScale = (-0.7, 0.7, 0.7)


class PageArrow(DirectButton):
    def __init__(self, page, inverted=False, **kwargs):
        self.page = page

        if not inverted:
            scales = (halfButtonScale, halfButtonHoverScale)
            extraArgs = [-1]
            pos = (-0.6, 0, 0.62)
        else:
            scales = (halfButtonInvertScale, halfButtonInvertHoverScale)
            extraArgs = [1]
            pos = (0.6, 0, 0.62)

        optiondefs = (
            ('relief', None, None),
            ('image', (
                arrowUp,
                arrowDown,
                arrowRollover,
                arrowDisabled
            ), None),
            ('image_scale', scales[0], None),
            ('image1_scale', scales[1], None),
            ('image2_scale', scales[1], None),
            ('extraArgs', extraArgs, None),
            ('pos', kwargs.get('pos') or pos, None),
        )

        self.defineoptions(kwargs, optiondefs)
        DirectButton.__init__(self, page)
        self.initialiseoptions(PageArrow)


class AchievementGroup(NodePath):
    POS_LIST = [
        (-0.435, 0, 0.41),
        (0.435, 0, 0.41),
        (-0.435, 0, 0.16),
        (0.435, 0, 0.16),
        (-0.435, 0, -0.09),
        (0.435, 0, -0.09),
        (-0.435, 0, -0.34),
        (0.435, 0, -0.34)
    ]

    def __init__(self, parent, achievementIds):
        NodePath.__init__(self, parent.attachNewNode('achievement-group-%s' % id(self)))

        self.achievementIds = achievementIds
        self.achievements = {}

    def load(self):
        for i, achievementId in enumerate(self.achievementIds):
            node = self.drawAchievement(achievementId, i)
            self.achievements[achievementId] = (i, node)

    def unload(self):
        self.removeNode()

    def update(self, achievementId):
        index = self.achievements[achievementId][0]
        self.achievements[achievementId][1].removeNode()

        node = self.drawAchievement(achievementId, index, forceUnlocked=True)
        self.achievements[achievementId] = (index, node)

    def drawAchievement(self, achievementId, index, forceUnlocked=False):
        locked = not base.localAvatar.hasAchievement(achievementId) if not forceUnlocked else False
        faded = Achievements.getAchievementVisibility(achievementId) == Achievements.HIDDEN and locked

        node = AchievementNode(achievementId, faded=faded, locked=locked)
        node.setScale(0.2)
        node.setPos(*self.POS_LIST[index])
        node.reparentTo(self)
        return node

    def hasAchievement(self, achievementId):
        return achievementId in self.achievementIds


class AchievementGroupList:
    def __init__(self, parent, achievementIds):
        self.parent = parent
        self.achievementIds = achievementIds

        self.groups = []
        self.currentGroupIndex = None

        self.groupLabel = None

        self.leftArrow = None
        self.rightArrow = None

    def load(self):
        self.groupLabel = DirectLabel(parent=self.parent, relief=None, text='0/0', text_scale=0.05,
                                      textMayChange=1, pos=(0, 0, -0.555))

        self.leftArrow = PageArrow(self.parent, command=self.arrowPressed, pos=(-0.105, 0, -0.54), scale=0.7)
        self.rightArrow = PageArrow(self.parent, inverted=True, command=self.arrowPressed,
                                    pos=(0.105, 0, -0.54), scale=0.7)

        for achievementIds in [self.achievementIds[i:i+8] for i in xrange(0, len(self.achievementIds), 8)]:
            group = AchievementGroup(self.parent, achievementIds)
            group.load()
            group.hide()
            self.groups.append(group)

        self.showGroup(0)

    def unload(self):
        for group in self.groups:
            group.unload()

        self.groups = []

        self.groupLabel.destroy()
        self.groupLabel = None

        self.leftArrow.destroy()
        self.leftArrow = None

        self.rightArrow.destroy()
        self.rightArrow = None

    def update(self, achievementId):
        for group in self.groups:
            if group.hasAchievement(achievementId):
                group.update(achievementId)
                break

    def showGroup(self, groupIndex):
        if self.currentGroupIndex is not None:
            self.groups[self.currentGroupIndex].hide()

        if groupIndex == 0:
            self.leftArrow['state'] = DGG.DISABLED
        else:
            self.leftArrow['state'] = DGG.NORMAL

        if groupIndex == len(self.groups) - 1:
            self.rightArrow['state'] = DGG.DISABLED
        else:
            self.rightArrow['state'] = DGG.NORMAL

        self.groups[groupIndex].show()
        self.currentGroupIndex = groupIndex

        self.groupLabel['text'] = '%s/%s' % (groupIndex+1, len(self.groups))

    def arrowPressed(self, direction):
        self.showGroup(self.currentGroupIndex + direction)


class AchievementClassifier(NodePath):
    def __init__(self, page, classifier):
        NodePath.__init__(self, page.attachNewNode('achievement-classifier-%s' % classifier))

        self.page = page
        self.classifier = classifier

        self.label = None
        self.achievementGroupList = None

    def update(self, achievementId):
        self.achievementGroupList.update(achievementId)

    def load(self):
        self.label = DirectLabel(parent=self, relief=None, text=TTLocalizer.getAchievementClassifier(self.classifier),
                                 text_scale=0.08, textMayChange=0, pos=(0, 0, 0.6))

        self.achievementGroupList = AchievementGroupList(self, Achievements.getClassifierAchievements(self.classifier))
        self.achievementGroupList.load()

    def unload(self):
        self.label.destroy()
        self.label = None

        self.achievementGroupList.unload()
        self.achievementGroupList = None


class AchievementsPage(ShtikerPage):
    def __init__(self):
        ShtikerPage.__init__(self)

        self.classifiers = OrderedDict()
        self.currentClassifierIndex = None

        self.achievementIds = []
        self.achievementPoints = None

        self.leftArrow = None
        self.rightArrow = None

        self.pointsBar = None
        self.levelText = None

    def load(self):
        self.leftArrow = PageArrow(self, command=self.arrowPressed)
        self.rightArrow = PageArrow(self, inverted=True, command=self.arrowPressed)

        self.pointsBar = DirectWaitBar(parent=self, text='0/0', textMayChange=1, text_fg=(1, 1, 1, 0.75),
                                       pos=(-0.05, 0, -0.62), scale=0.5, frameSize=(-1.46, 1.46, -0.06, 0.06),
                                       frameColor=(77.0/255.0, 77.0/255.0, 77.0/255.0, 0.55),
                                       barColor=(0.0/255.0, 162.0/255.0, 232.0/255.0, 1.0),
                                       range=0, value=0)

        self.levelText = DirectLabel(parent=self, relief=None, pos=(0.75, 0, -0.656), text='0', textMayChange=True,
                                     text_fg=(1, 1, 2, 0.85), text_shadow=(0, 0, 0, 5), text_align=TextNode.ACenter,
                                     text_scale=0.1, text_font=ToontownGlobals.getSignFont())

        for classifier in Achievements.classifier2AchievementIds:
            achievementClassifier = AchievementClassifier(self, classifier)
            achievementClassifier.load()
            achievementClassifier.hide()
            self.classifiers[classifier] = achievementClassifier

    def showClassifier(self, classifierIndex):
        if self.currentClassifierIndex is not None:
            self.classifiers[self.classifiers.keys()[self.currentClassifierIndex]].hide()

        if classifierIndex == 0:
            self.leftArrow['state'] = DGG.DISABLED
        else:
            self.leftArrow['state'] = DGG.NORMAL

        if classifierIndex == len(self.classifiers) - 1:
            self.rightArrow['state'] = DGG.DISABLED
        else:
            self.rightArrow['state'] = DGG.NORMAL

        self.currentClassifierIndex = classifierIndex
        self.classifiers[self.classifiers.keys()[classifierIndex]].show()

    def unload(self):
        for classifier in self.classifiers:
            self.classifiers[classifier].unload()

        self.classifiers = OrderedDict()
        self.currentClassifierIndex = None

        self.achievementIds = []
        self.achievementPoints = None

        self.leftArrow.destroy()
        self.leftArrow = None

        self.rightArrow.destroy()
        self.rightArrow = None

        self.pointsBar.destroy()
        self.pointsBar = None

        self.levelText.destroy()
        self.levelText = None

        ShtikerPage.unload(self)

    def enter(self):
        if self.currentClassifierIndex is None:
            self.showClassifier(0)

        ShtikerPage.enter(self)

    def update(self, achievements, achievementPoints):
        if self.achievementIds:
            newAchievementIds = [x for x in achievements if x not in self.achievementIds]
            for achievementId in newAchievementIds:
                classifier = Achievements.getAchievementClassifier(achievementId)
                self.classifiers[classifier].update(achievementId)

        self.achievementIds = achievements
        self.achievementPoints = achievementPoints

        level = Achievements.getLevelFromPoints(achievementPoints)
        self.levelText['text'] = str(level + 1)
        
        neededPoints = Achievements.getPointsForLevel(level)
        previousPoints = Achievements.getPointsForLevel(level-1) if level > 0 else 0

        self.pointsBar['text'] = '%s/%s' % (achievementPoints, neededPoints)
        self.pointsBar['range'] = neededPoints - previousPoints
        self.pointsBar['value'] = achievementPoints - previousPoints

    def arrowPressed(self, direction):
        self.showClassifier(self.currentClassifierIndex + direction)

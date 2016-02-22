from panda3d.core import NodePath
from panda3d.core import TextNode

from direct.gui.DirectWaitBar import DirectWaitBar
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from direct.gui import DirectGuiGlobals as DGG

from toontown.shtiker.ShtikerPage import ShtikerPage
from toontown.achievements import Achievements
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer


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
            ('pos', pos, None),
        )

        self.defineoptions(kwargs, optiondefs)
        DirectButton.__init__(self, page)
        self.initialiseoptions(PageArrow)


class AchievementList(DirectFrame):
    def __init__(self, parent, **kwargs):
        optiondefs = (
            ('image', None, None),
            ('relief', None, None),
            ('frameColor', (1, 1, 1, 1), None),
            ('image_scale', halfButtonInvertScale, None),
            ('text_fg', (1, 1, 1, 1), None),
        )

        self.defineoptions(kwargs, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(AchievementList)

        self.achievements = {}

    def addAchievement(self, achievementId):
        pass

    def hasAchievement(self, achievementId):
        return achievementId in self.achievements


class AchievementCategory(NodePath):
    def __init__(self, page, category):
        NodePath.__init__(self, page.attachNewNode('achievement-category-%s' % category))

        self.page = page
        self.category = category
        self.activeIds = []

        self.label = None
        self.achievementList = None

    def update(self):
        pass

    def load(self):
        self.label = DirectLabel(parent=self, relief=None, text=TTLocalizer.getAchievementCategory(self.category),
                                 text_scale=0.08, textMayChange=0, pos=(0, 0, 0.6))

        self.achievementList = AchievementList(self)

    def unload(self):
        self.label.destroy()
        self.label = None

        self.achievementList.destroy()
        self.achievementList = None


class AchievementsPage(ShtikerPage):
    def __init__(self):
        ShtikerPage.__init__(self)

        self.categories = []
        self.currentCategoryIndex = None

        self.achievements = []
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

        for category in Achievements.category2AchievementIds:
            achievementCategory = AchievementCategory(self, category)
            achievementCategory.load()
            achievementCategory.hide()
            self.categories.append(achievementCategory)

    def showCategory(self, categoryIndex):
        if self.currentCategoryIndex is not None:
            self.categories[self.currentCategoryIndex].hide()

        if categoryIndex == 0:
            self.leftArrow['state'] = DGG.DISABLED
        else:
            self.leftArrow['state'] = DGG.NORMAL

        if categoryIndex == len(self.categories) - 1:
            self.rightArrow['state'] = DGG.DISABLED
        else:
            self.rightArrow['state'] = DGG.NORMAL

        self.currentCategoryIndex = categoryIndex
        self.categories[categoryIndex].show()

    def unload(self):
        for category in self.categories:
            category.unload()

        self.categories = []
        self.currentCategoryIndex = None

        self.achievements = []
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
        if self.currentCategoryIndex is None:
            self.showCategory(0)

        ShtikerPage.enter(self)

    def update(self, achievements, achievementPoints):
        self.achievements = achievements
        self.achievementPoints = achievementPoints

        level = Achievements.getLevelFromPoints(achievementPoints)
        self.levelText['text'] = str(level + 1)
        
        neededPoints = Achievements.getPointsForLevel(level)
        self.pointsBar['text'] = '%s/%s' % (achievementPoints, neededPoints)
        self.pointsBar['range'] = neededPoints
        self.pointsBar['value'] = achievementPoints

    def arrowPressed(self, direction):
        self.showCategory(self.currentCategoryIndex + direction)

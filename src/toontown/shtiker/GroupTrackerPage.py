from toontown.shtiker import ShtikerPage
from panda3d.core import TextNode, Vec4
from direct.gui.DirectGui import DirectLabel, DirectFrame, DirectButton, DirectScrolledList, DGG
from toontown.toonbase import TTLocalizer

SUIT_ICON_COLORS = (Vec4(0.863, 0.776, 0.769, 1.0), Vec4(0.749, 0.776, 0.824, 1.0),
                    Vec4(0.749, 0.769, 0.749, 1.0), Vec4(0.843, 0.745, 0.745, 1.0))


class GroupTrackerPage(ShtikerPage.ShtikerPage):
    notify = directNotify.newCategory('GroupTrackerPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.groups = []
        self.groupinfo = {}

    def load(self):
        self.listXorigin = -0.02
        self.listFrameSizeX = 0.67
        self.listZorigin = -0.96
        self.listFrameSizeZ = 1.04
        self.arrowButtonScale = 1.3
        self.itemFrameXorigin = -0.237
        self.itemFrameZorigin = 0.365
        self.buttonXstart = self.itemFrameXorigin + 0.293
        self.gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.scrollList = DirectScrolledList(parent=self, 
                                            relief=None, 
                                            pos=(-0.5, 0, 0), 
                                            incButton_image=(self.gui.find('**/FndsLst_ScrollUp'), 
                                                             self.gui.find('**/FndsLst_ScrollDN'),
                                                             self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
                                                             self.gui.find('**/FndsLst_ScrollUp')
                                                             ), 
                                            incButton_relief=None, 
                                            incButton_scale=(self.arrowButtonScale, self.arrowButtonScale, -self.arrowButtonScale), 
                                            incButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin - 0.999), 
                                            incButton_image3_color=Vec4(1, 1, 1, 0.2), 
                                            decButton_image=(self.gui.find('**/FndsLst_ScrollUp'), 
                                                             self.gui.find('**/FndsLst_ScrollDN'),
                                                             self.gui.find('**/FndsLst_ScrollUp_Rllvr'), 
                                                             self.gui.find('**/FndsLst_ScrollUp')
                                                             ), 
                                            decButton_relief=None, 
                                            decButton_scale=(self.arrowButtonScale, self.arrowButtonScale, self.arrowButtonScale), 
                                            decButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.227), 
                                            decButton_image3_color=Vec4(1, 1, 1, 0.2), 
                                            itemFrame_pos=(self.itemFrameXorigin, 0, self.itemFrameZorigin), 
                                            itemFrame_scale=1.0,
                                            itemFrame_relief=DGG.SUNKEN, 
                                            itemFrame_frameSize=(self.listXorigin, 
                                                                 self.listXorigin + self.listFrameSizeX,
                                                                 self.listZorigin,
                                                                 self.listZorigin + self.listFrameSizeZ
                                                                 ), 
                                            itemFrame_frameColor=(0.85, 0.95, 1, 1), 
                                            itemFrame_borderWidth=(0.01, 0.01), 
                                            numItemsVisible=15, 
                                            forceHeight=0.065, 
                                            items=self.groups
                                            )
                                            
        self.scrollTitle = DirectFrame(parent=self.scrollList, 
                                       text='Groups', 
                                       text_scale=0.06, 
                                       text_align=TextNode.ACenter, 
                                       relief=None,
                                       pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.127)
                                       )
        
        text = TTLocalizer.BoardingGroupInformation % {
             'district': 'The Longest Name Ever',
             'currentPlayers': '2',
             'maxPlayers' : '4'}
        title = 'Cashbot Bullion Mint' #The text here will be the current selected place to teleport from boarding groups ex. Side Entrance, Bullion Mint
        self.groupInfoTitle = DirectLabel(parent=self, text=title, 
                                          text_scale=0.080, text_align=TextNode.ACenter,
                                          text_wordwrap=15, relief=None, pos=(0.45, 0, 0.5))
        self.groupInfo = DirectLabel(parent=self,
                                     text=text,
                                     text_scale=0.050,
                                     text_align=TextNode.ACenter, 
                                     text_wordwrap=15, 
                                     relief=None, 
                                     pos=(0.45, 0, 0.35)
                                     )

        # Loading group icons
        suitIcons = loader.loadModel('phase_3/models/gui/cog_icons')
        # All suit icons
        self.bossbotIcon = suitIcons.find('**/CorpIcon')
        self.bossbotIcon.setColor(SUIT_ICON_COLORS[0])
        
        self.lawbotIcon = suitIcons.find('**/LegalIcon')
        self.lawbotIcon.setColor(SUIT_ICON_COLORS[1])
        
        self.cashbotIcon = suitIcons.find('**/MoneyIcon')
        self.cashbotIcon.setColor(SUIT_ICON_COLORS[2])
        
        self.sellbotIcon = suitIcons.find('**/SalesIcon')
        self.sellbotIcon.setColor(SUIT_ICON_COLORS[3])
        
        # Group Image:
        self.groupIcon = DirectButton(parent=self, relief=None, state=DGG.DISABLED, image=(self.cashbotIcon, self.cashbotIcon, self.cashbotIcon), image_scale=(0.4, 1, 0.4), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(0.45, 10, -0.3), command=self.doNothing)
        
        suitIcons.removeNode()
        self.gui.removeNode()
        self.accept('GroupTrackerResponse', self.updatePage)

    def unload(self):
        self.scrollList.destroy()
        self.groupInfo.destroy()
        self.groupInfoTitle.destroy()
        self.groupIcon.destroy()
        del self.scrollList
        del self.groupInfo
        del self.groupInfoTitle
        del self.groupIcon
        ShtikerPage.ShtikerPage.unload(self)

    def enter(self):
        ShtikerPage.ShtikerPage.enter(self)
        base.cr.globalGroupTracker.requestGroups()

    def updatePage(self):
        groups = base.cr.globalGroupTracker.getGroupInfo()

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)
        base.cr.globalGroupTracker.doneRequesting()

    def doNothing(self):
        pass
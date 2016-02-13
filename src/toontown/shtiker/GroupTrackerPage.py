from toontown.shtiker import ShtikerPage
from panda3d.core import TextNode, Vec4
from direct.gui.DirectGui import DirectLabel, DirectFrame, DirectButton, DirectScrolledList, DGG
from toontown.toonbase import TTLocalizer

SUIT_ICON_COLORS = (Vec4(0.863, 0.776, 0.769, 1.0), Vec4(0.749, 0.776, 0.824, 1.0),
                    Vec4(0.749, 0.769, 0.749, 1.0), Vec4(0.843, 0.745, 0.745, 1.0))

class GroupTrackerPlayer(DirectButton):
    def __init__(self, parent, avId, name, isLeader, **kw):
        self.avId = avId
        self.name = name
        self.leader = isLeader
        self.leaderImage = None

        if parent is None:
            parent = aspect2d

        optiondefs = (
            ('text', self.name, None),
            ('text_fg', (0.0, 0.0, 0.0, 1.0), None),
            ('text_align', TextNode.ALeft, None),
            ('text_pos', (-0.2, 0.0, 0.0), None),
            ('relief', None, None),
            ('text_scale', 0.05, None),
            ('command', self.loadPlayerDetails, None)
        )

        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent)
        self.initialiseoptions(GroupTrackerPlayer)
        
        boardingGroupIcons = loader.loadModel('phase_9/models/gui/tt_m_gui_brd_status')
        self.leaderButtonImage = boardingGroupIcons.find('**/tt_t_gui_brd_statusLeader')
        self.leaderImage = DirectButton(parent=self, relief=None, state=DGG.DISABLED, image=(self.leaderButtonImage), image_scale=(0.06, 1.0, 0.06), pos=(-0.26, 0, 0.02), command=None)
        if(self.name == 'Necromoni'):
            self.setLeaderStatus(True)
        else:
            self.setLeaderStatus(False)
        boardingGroupIcons.removeNode()
    
    def destroy(self):
        if self.leaderImage:
            self.leaderImage.destroy()
            del self.leaderImage
        
        DirectButton.destroy(self)
    
    def setLeaderStatus(self, isLeader):
        self.leader = isLeader
        
        if self.leader and self.leaderImage is None:
            self.leaderImage = DirectButton(parent=self, relief=None, state=DGG.DISABLED, image=(self.leaderButtonImage), image_scale=(0.06, 1.0, 0.06), pos=(-0.26, 0, 0.02), command=None)
        if self.leader == False and self.leaderImage is not None:
            self.leaderImage.destroy()
            del self.leaderImage
    
    def loadPlayerDetails(self):
        # TODO: Load player details based off avId for localAvatar
        pass

class GroupTrackerPage(ShtikerPage.ShtikerPage):
    notify = directNotify.newCategory('GroupTrackerPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.groups = []
        self.groupinfo = {}
        self.players = []
        self.playerWidgets = []

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
        
        districtText = TTLocalizer.BoardingGroupDistrictInformation % {
             'district': 'Gravity Falls'}
        
        self.players.append('Craig')
        self.players.append('Craigy')
        self.players.append('Malverde')
        self.players.append('Maverdeee')
        self.players.append('Bob')
             
        title = 'Cashbot Bullion Mint' #The text here will be the current selected place to teleport from boarding groups ex. Side Entrance, Bullion Mint
        self.playerList = DirectScrolledList(parent=self, 
                                            relief=None, 
                                            pos=(0.45, 0, 0.1), 
                                            
                                            incButton_image=(self.gui.find('**/FndsLst_ScrollUp'), 
                                                             self.gui.find('**/FndsLst_ScrollDN'),
                                                             self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
                                                             self.gui.find('**/FndsLst_ScrollUp')
                                                             ), 
                                            incButton_relief=None, 
                                            incButton_scale=(1.0, 1.0, -1.0), 
                                            incButton_pos=(0, 0, -0.28), 
                                            incButton_image3_color=Vec4(1, 1, 1, 0.05),
                                            
                                            decButton_image=(self.gui.find('**/FndsLst_ScrollUp'), 
                                                             self.gui.find('**/FndsLst_ScrollDN'),
                                                             self.gui.find('**/FndsLst_ScrollUp_Rllvr'), 
                                                             self.gui.find('**/FndsLst_ScrollUp')
                                                             ), 
                                            decButton_relief=None, 
                                            decButton_scale=(1.0, 1.0, 1.0),
                                            decButton_pos=(0.0, 0, 0.04), 
                                            decButton_image3_color=Vec4(1, 1, 1, 0.25), 
                                            
                                            itemFrame_pos=(0, 0, -0.05), 
                                            itemFrame_scale=1.0,
                                            itemFrame_relief=DGG.SUNKEN, 
                                            itemFrame_frameSize=(-0.3, 0.3,  #x
                                                                 -0.2, 0.06),  #z
                                            itemFrame_frameColor=(0.85, 0.95, 1, 1), 
                                            itemFrame_borderWidth=(0.01, 0.01), 
                                            numItemsVisible=4,
                                            forceHeight=0.05, 
                                            items=self.playerWidgets
                                            )
                                            
        self.playerListTitle = DirectFrame(parent=self.playerList, 
                                       text='Players [2/4]', 
                                       text_scale=0.05, 
                                       text_align=TextNode.ACenter, 
                                       relief=None,
                                       pos=(0, 0, 0.08)
                                       )
        self.groupInfoTitle = DirectLabel(parent=self, text=title, 
                                          text_scale=0.080, text_align=TextNode.ACenter,
                                          text_wordwrap=15, relief=None, pos=(0.45, 0, 0.5))
        self.groupInfoDistrict = DirectLabel(parent=self,
                                     text=districtText,
                                     text_scale=0.050,
                                     text_align=TextNode.ACenter, 
                                     text_wordwrap=15, 
                                     relief=None, 
                                     pos=(0.45, 0, 0.4)
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

        boardingGroupIcons = loader.loadModel('phase_9/models/gui/tt_m_gui_brd_status')
        self.leaderButtonImage = boardingGroupIcons.find('**/tt_t_gui_brd_statusLeader')

        # Group Image:
        self.groupIcon = DirectButton(parent=self, relief=None, state=DGG.DISABLED, image=(self.cashbotIcon, self.cashbotIcon, self.cashbotIcon), image_scale=(0.4, 1, 0.4), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(0.45, 10, -0.5), command=self.doNothing)
        
        self.updatePlayerList()
        
        boardingGroupIcons.removeNode()
        suitIcons.removeNode()
        self.gui.removeNode()
        self.accept('GroupTrackerResponse', self.updatePage)

    def unload(self):
        self.scrollList.destroy()
        self.groupInfo.destroy()
        self.groupInfoDistrict.destroy()
        self.playerList.destroy()
        self.groupInfoTitle.destroy()
        self.groupIcon.destroy()
        for widget in self.playerWidgets:
            widget.destroy()
        self.playerWidgets = []
        del self.scrollList
        del self.groupInfo
        del self.groupInfoDistrict
        del self.playerList
        del self.groupInfoTitle
        del self.groupIcon
        ShtikerPage.ShtikerPage.unload(self)

    def enter(self):
        ShtikerPage.ShtikerPage.enter(self)
        base.cr.globalGroupTracker.requestGroups()

    def updatePage(self):
        groups = base.cr.globalGroupTracker.getGroupInfo()
        print(groups)

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)
        base.cr.globalGroupTracker.doneRequesting()

    def doNothing(self):
        pass
    
    def setPlayers(self, players):
        self.players = players
        self.updatePlayerList()
    
    def updatePlayerList(self):
        if self.playerList is None:
            return
            
        # Clear the List
        for item in self.playerList['items']:
            self.playerList.removeItem(item, refresh=False)
        
        # Clear the widgets
        self.playerWidgets = []
        
        # Make a player widget for each player
        for player in self.players:
            self.playerWidgets.append(GroupTrackerPlayer(parent=self, avId=1, name=player, isLeader=False))
        
        # Re-Populate the List
        for player in self.playerWidgets:
            self.playerList.addItem(player)
        
        # Update the Player List Title
        self.playerListTitle['text'] = ('Players ' + str(len(self.players)) + '/' + '8' + ':')
            
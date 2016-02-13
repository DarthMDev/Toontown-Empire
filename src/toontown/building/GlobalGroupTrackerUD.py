from otp.uberdog.GlobalOtpObjectUD import GlobalOtpObjectUD
from GroupTrackerGlobals import *


class GlobalGroupTrackerUD(GlobalOtpObjectUD):

    def announceGenerate(self):
        GlobalOtpObjectUD.announceGenerate(self)

        # Maps a leaderId to the corresponding BoardingGroup struct.
        self.leader2Group = {}

        # Listeners are people who want to recieve updates to their GroupTracker page.
        self.listeners = []

    def addGroup(self, leaderId, groupStruct):
        self.leader2Group[leaderId] = list(groupStruct)  
        
        category = self.leader2Group[leaderId][CATEGORY]
        memberIds = self.leader2Group[leaderId][MEMBER_IDS]
        memberNames = self.leader2Group[leaderId][MEMBER_NAMES]
        show = self.leader2Group[leaderId][SHOW]
        
        for avId in self.listeners:
            self.sendToAvatar(avId, 'updateGroup', [leaderId, category, memberIds, memberNames, show])

    def updateGroup(self, leaderId, category, memberIds, memberNames, show):
        if leaderId not in self.leader2Group:
            return
        self.leader2Group[leaderId][CATEGORY] = category
        self.leader2Group[leaderId][MEMBER_IDS] = memberIds
        self.leader2Group[leaderId][MEMBER_NAMES] = memberNames
        self.leader2Group[leaderId][SHOW] = show
        
        for avId in self.listeners:
            self.sendToAvatar(avId, 'updateGroup', [leaderId, category, memberIds, memberNames, show])

    def requestGroups(self, avId):
        self.requestGroupsResponse(avId)
        if avId not in self.listeners:
            # Accept this event incase of a unexpected exit from the client.
            self.accept('distObjDelete-%d' % avId, self.doneRequesting, extraArgs=[avId])
            self.listeners.append(avId)

    def requestGroupsResponse(self, avId):
        if not self.leader2Group:
            # We have no info to display. The client should be notified by the timeout task.
            return
            
        self.sendToAvatar(avId, 'requestGroupsResponse', [self.leader2Group.keys(), self.leader2Group.values()])

    def doneRequesting(self, avId):
        self.ignore('distObjDelete-%d' % avId)
        if avId in self.listeners:
            self.listeners.remove(avId)
    
    def showGroup(self, leaderId, show):
        if leaderId not in self.leader2Group:
            return
        
        category = self.leader2Group[leaderId][CATEGORY]
        memberIds = self.leader2Group[leaderId][MEMBER_IDS]
        memberNames = self.leader2Group[leaderId][MEMBER_NAMES]
        self.leader2Group[leaderId][SHOW] = show

        for avId in self.listeners:
            self.sendToAvatar(avId, 'updateGroup', [leaderId, category, memberIds, memberNames, show])


from otp.ai.MagicWordGlobal import *
from otp.avatar.Avatar import teleportNotify
from toontown.chat import ToonChatGarbler
from toontown.toonbase import ToontownGlobals

class FriendHandle:
    def __init__(self, doId, name, style, adminAccess, petId, isAPet = False):
        self.doId = doId
        self.style = style
        self.petId = petId
        self.adminAccess = adminAccess
        self.isAPet = isAPet
        self.chatGarbler = ToonChatGarbler.ToonChatGarbler()
        self.name = name

    def getDoId(self):
        return self.doId

    def getAdminAccess(self):
        return self.adminAccess

    def isAdmin(self):
        return self.adminAccess >= MINIMUM_MAGICWORD_ACCESS

    def getPetId(self):
        return self.petId

    def hasPet(self):
        return self.getPetId() != 0

    def isPet(self):
        return self.isAPet

    def getName(self):
        return self.name

    def getFont(self):
        return ToontownGlobals.getToonFont()

    def getStyle(self):
        return self.style

    def uniqueName(self, idString):
        return idString + '-' + str(self.getDoId())

    def d_battleSOS(self, sendToId):
        base.cr.tteFriendsManager.d_battleSOS(self.doId)

    def d_teleportQuery(self, requesterId):
        teleportNotify.debug('sending d_teleportQuery(%s)' % (requesterId,))

        base.cr.tteFriendsManager.d_teleportQuery(self.doId)

    def d_teleportResponse(self, avId, available, shardId, hoodId, zoneId):
        teleportNotify.debug('sending teleportResponse%s' % ((avId, available,
            shardId, hoodId, zoneId),)
        )

        base.cr.tteFriendsManager.d_teleportResponse(self.doId, available,
            shardId, hoodId, zoneId
        )

    def d_teleportGiveup(self, requesterId):
        teleportNotify.debug('sending d_teleportGiveup(%s)' % (requesterId,))

        base.cr.tteFriendsManager.d_teleportGiveup(self.doId)

    def isUnderstandable(self):
        if self.commonChatFlags & base.localAvatar.commonChatFlags & ToontownGlobals.CommonChat:
            understandable = 1
        elif self.commonChatFlags & ToontownGlobals.SuperChat:
            understandable = 1
        elif base.localAvatar.commonChatFlags & ToontownGlobals.SuperChat:
            understandable = 1
        elif base.cr.getFriendFlags(self.doId) & ToontownGlobals.FriendChat:
            understandable = 1
        elif self.whitelistChatFlags & base.localAvatar.whitelistChatFlags:
            understandable = 1
        else:
            understandable = 0
        return understandable

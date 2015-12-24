

class AvatarHandle(object):
    dclassName = 'AvatarHandle'

    @staticmethod
    def getName():
        if __dev__:
            pass
        return ''

    @staticmethod
    def isOnline():
        if __dev__:
            pass
        return False

    @staticmethod
    def isUnderstandable():
        if __dev__:
            pass
        return True

    def setTalkWhisper(self, fromAV, fromAC, avatarName, chat, mods, flags):
        newText, scrubbed = localAvatar.scrubTalk(chat, mods)
        base.talkAssistant.receiveWhisperTalk(fromAV, avatarName, fromAC, None, self.avatarId, self.getName(), newText, scrubbed)
        return

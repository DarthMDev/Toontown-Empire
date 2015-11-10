from direct.directnotify import DirectNotifyGlobal
from src.otp.chat.TalkAssistant import TalkAssistant
from src.otp.chat.ChatGlobals import *

class TTTalkAssistant(TalkAssistant):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTTalkAssistant')

    def sendToonTaskSpeedChat(self, taskId, toNpcId, toonProgress, msgIndex):
        messenger.send(SCChatEvent)
        messenger.send('chatUpdateSCToontask', [taskId, toNpcId, toonProgress, msgIndex])

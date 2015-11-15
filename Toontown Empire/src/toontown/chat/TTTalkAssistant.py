import string
import sys
from direct.showbase import DirectObject
from src.otp.otpbase import OTPLocalizer
from src.toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
from src.otp.otpbase import OTPGlobals
from src.otp.speedchat import SCDecoders
from pandac.PandaModules import *
from src.otp.chat.ChatGlobals import *
from src.otp.chat.TalkGlobals import *
from src.otp.speedchat import SpeedChatGlobals
from src.otp.chat.TalkMessage import TalkMessage
from src.otp.chat.TalkAssistant import TalkAssistant
from src.toontown.speedchat import TTSCDecoders
import time

class TTTalkAssistant(TalkAssistant):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTTalkAssistant')

    def __init__(self):
        TalkAssistant.__init__(self)

    def clearHistory(self):
        TalkAssistant.clearHistory(self)

    def sendToonTaskSpeedChat(self, taskId, toNpcId, toonProgress, msgIndex):
        error = None
        messenger.send(SCChatEvent)
        messenger.send('chatUpdateSCToontask', [taskId,
         toNpcId,
         toonProgress,
         msgIndex])
        return error

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from otp.distributed import OtpDoGlobals
from toontown.toonbase import TTLocalizer
import time

BLACKLIST = TTLocalizer.Blacklist
OFFENSE_MSGS = ('-- DEV CHAT -- word blocked: %s', 'Watch your language! This is your first offense. You said "%s".',
                'Watch your language! This is your second offense. Next offense you\'ll get banned for 24 hours. You said "%s".')
 
class ChatAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('ChatAgentUD')
    wantWhitelist = config.GetBool('want-whitelist', True)
   
    chatMode2channel = {
            1 : OtpDoGlobals.OTP_STAFF_CHANNEL,
            2 : OtpDoGlobals.OTP_LEAD_STAFF_CHANNEL,
            3 : OtpDoGlobals.OTP_DEVELOPER_CHANNEL,
            4 : OtpDoGlobals.OTP_LEADER_CHANNEL,            
    }
    chatMode2prefix = {
            1 : "[STAFF] ",
            2 : "[LEADSTAFF] ",
            3 : "[DEVELOPER] ",
            4 : "[LEADER] ",
    }
   
    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
 
        self.offenses = {}
        self.muted = {}

    def muteAccount(self, account, howLong):
         print ['muteAccount', account, howLong]
         self.muted[account] = True
 
     def unmuteAccount(self, account):
         print ['unuteAccount', account]
         self.muted[account] = False

    def chatMessage(self, message, chatMode):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', self.air.getAccountIdFromSender(),
                                      'Account sent chat without an avatar', message)
            return
 
        if chatMode == 0 and self.wantWhitelist:
            if self.detectBadWords(self.air.getMsgSender(), message):
                return
 
        self.air.writeServerEvent('chat-said', sender, message)
        self.air.send(self.air.dclassesByName['DistributedAvatarUD'].aiFormatUpdate('setTalk', sender, sender, self.air.ourChannel, [message]))

# ~Mute command stuff

        if sender in self.muted and int(time.time()/60) < self.muted[sender]:
             return

# ends here
 
    def detectBadWords(self, sender, message):
        words = message.split()
        print words
        for word in words:
            if word.lower() in BLACKLIST:
                accountId = (sender >> 32) & 0xFFFFFFFF
                avId = sender & 0xFFFFFFFF
               
                if not sender in self.offenses:
                    self.offenses[sender] = 0
                   
                if self.air.friendsManager.getToonAccess(avId) < 300:
                    self.offenses[sender] += 1
               
                if self.offenses[sender] >= 3:
                    msg = 'Banned'    
                   
                else:
                    msg = OFFENSE_MSGS[self.offenses[sender]] % word
                    dclass = self.air.dclassesByName['ClientServicesManagerUD']
                    dg = dclass.aiFormatUpdate('systemMessage',
                               OtpDoGlobals.OTP_DO_ID_CLIENT_SERVICES_MANAGER,
                               sender, 1000000, [msg])
                    self.air.send(dg)
                   
                self.air.writeServerEvent('chat-offense', accountId, word=word, num=self.offenses[sender], msg=msg)
                if self.offenses[sender] >= 3:
                    del self.offenses[sender]
                   
                return 1
               
        return 0

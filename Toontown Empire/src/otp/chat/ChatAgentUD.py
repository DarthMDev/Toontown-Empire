from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from src.toontown.chat.TTWhiteList import TTWhiteList
from src.otp.distributed import OtpDoGlobals
import SequenceList

class ChatAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("ChatAgentUD")

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.wantBlacklistSequence = config.GetBool('want-blacklist-sequence', True)
        self.wantWhitelist = config.GetBool('want-whitelist', True)
        if self.wantWhitelist:
            self.whiteList = TTWhiteList()
            if self.wantBlacklistSequence:
                self.sequenceList = SequenceList.SequenceList()
        self.chatMode2channel = {
            1 : OtpDoGlobals.OTP_MOD_CHANNEL,
            2 : OtpDoGlobals.OTP_ADMIN_CHANNEL,
            3 : OtpDoGlobals.OTP_SYSADMIN_CHANNEL,
        }
        self.chatMode2prefix = {
            1 : "[MOD] ",
            2 : "[ADMIN] ",
            3 : "[SYSADMIN] ",
        }
    def chatMessage(self, message, chatMode):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', accId=self.air.getAccountIdFromSender(),
                                         issue='Account sent chat without an avatar', message=message)
            return

        if self.wantWhitelist:
            cleanMessage, modifications = self.cleanWhitelist(message)
        else:
            cleanMessage, modifications = message, []
        self.air.writeServerEvent('chat-said', avId=sender, chatMode=chatMode, msg=message, cleanMsg=cleanMessage)

        if chatMode != 0:
            # Staff messages do not need to be cleaned. [TODO: Blacklist this?]
            if message.startswith('.'):
                cleanMessage = '.' + self.chatMode2prefix.get(chatMode, "") + message[1:]
            else:
                cleanMessage = self.chatMode2prefix.get(chatMode, "") + message
            modifications = []
        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalk', sender, self.chatMode2channel.get(chatMode, sender),
                                              self.air.ourChannel,
                                              [0, 0, '', cleanMessage, modifications, 0])
        self.air.send(dg)

    def whisperMessage(self, receiverAvId, message):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', accId=self.air.getAccountIdFromSender(),
                                         issue='Account sent chat without an avatar', message=message)
            return

        cleanMessage, modifications = self.cleanWhitelist(message)
        self.air.writeServerEvent('whisper-said', avId=sender, reciever=receiverAvId, msg=message, cleanMsg=cleanMessage)
        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalkWhisper', receiverAvId, receiverAvId, self.air.ourChannel,
                                            [sender, sender, '', cleanMessage, modifications, 0])
        self.air.send(dg)

    # True friend unfiltered chat
    def sfWhisperMessage(self, receiverAvId, message):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', accId=self.air.getAccountIdFromSender(),
                                         issue='Account sent chat without an avatar', message=message)
            return

        cleanMessage = self.cleanBlacklist(message)

        self.air.writeServerEvent('sf-whisper-said', avId=sender, reciever=receiverAvId, msg=message, cleanMsg=cleanMessage)
        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalkWhisper', receiverAvId, receiverAvId, self.air.ourChannel,
                                            [sender, sender, '', cleanMessage, [], 0])
        self.air.send(dg)

    def cleanWhitelist(self, message):
        modifications = []
        words = message.split(' ')
        offset = 0
        for word in words:
            if word and not self.whiteList.isWord(word):
                modifications.append((offset, offset+len(word)-1))
            offset += len(word) + 1

        cleanMessage = message
        if self.wantBlacklistSequence:
            modifications += self.cleanSequences(cleanMessage)

        for modStart, modStop in modifications:
            cleanMessage = cleanMessage[:modStart] + '*' * (modStop - modStart + 1) + cleanMessage[modStop + 1:]

        return (cleanMessage, modifications)

    def cleanBlacklist(self, message):
        # We don't have a black list so we just return the full message
        return message

    def cleanSequences(self, message):
        modifications = []
        offset = 0
        words = message.split()
        for wordit in xrange(len(words)):
            word = words[wordit].lower()
            seqlist = self.sequenceList.getList(word)
            if len(seqlist) > 0:
                for seqit in xrange(len(seqlist)):
                    sequence = seqlist[seqit]
                    splitseq = sequence.split()
                    if len(words) - (wordit + 1) >= len(splitseq):
                        cmplist = words[wordit + 1:]
                        del cmplist[len(splitseq):]
                        cmplist = [word.lower() for word in cmplist]
                        if cmp(cmplist, splitseq) == 0:
                            modifications.append((offset, offset + len(word) + len(sequence) - 1))
            offset += len(word) + 1

        return modifications




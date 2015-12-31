from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from otp.ai.MagicWordGlobal import *
from otp.avatar import Avatar

class ChatAgent(DistributedObjectGlobal):

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        self.cr.chatAgent = self
        self.chatMode = 0

    def delete(self):
        self.ignoreAll()
        self.cr.chatAgent = None
        DistributedObjectGlobal.delete(self)

    def verifyMessage(self, message):
        try:
            message.decode('ascii')
            return True
        except:
            return False

    def sendChatMessage(self, message):
        if not self.verifyMessage(message):
            return
        self.sendUpdate('chatMessage', [message, self.chatMode])

# ~Mute stuff

    def sendMuteAccount(self, account, howLong):
        self.sendUpdate('muteAccount', [account, howLong])

    def sendUnmuteAccount(self, account):
        self.sendUpdate('unmuteAccount', [account])

@magicWord(category=CATEGORY_TRIAL, types=[int])
def chatmode(mode=-1):
    """ Set the chat mode of the current avatar. """
    mode2name = {
        0 : "user",
        1 : "staff",
        2 : "lead staff",
        3 : "leader",
    }
    if base.cr.chatAgent is None:
        return "No ChatAgent found."
    if mode == -1:
        return "You are currently talking in the %s chat mode." % mode2name.get(base.cr.chatAgent.chatMode, "N/A")
    if not 0 <= mode <= 3:
        return "Invalid chat mode specified."
    if mode == 3 and spellbook.getInvoker().getAdminAccess() < 701:
        return "Chat mode 3 is reserved for leader."
    if mode == 2 and spellbook.getInvoker().getAdminAccess() < 502:
        return "Chat mode 2 is reserved for lead staff."
    if mode == 1 and spellbook.getInvoker().getAdminAccess() < 701:
        return "Chat mode 1 is reserved for staff."
    base.cr.chatAgent.chatMode = mode
    return "You are now talking in the %s chat mode." % mode2name.get(mode, "N/A")

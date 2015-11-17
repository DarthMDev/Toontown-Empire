from direct.distributed.PyDatagram import *
import urlparse
from src.otp.distributed.OtpDoGlobals import *
from src.otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from src.toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
import src.toontown.minigame.MinigameCreatorAI
from src.otp.otpbase import BackupManager

if config.GetBool('want-rpc-server', False):
    from src.toontown.rpc.ToontownRPCServer import ToontownRPCServer
    from src.toontown.rpc.ToontownRPCHandler import ToontownRPCHandler

class ToontownUberRepository(ToontownInternalRepository):
    def __init__(self, baseChannel, serverId):
        ToontownInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')

        self.notify.setInfo(True)

    def handleConnected(self):
        ToontownInternalRepository.handleConnected(self)
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)

        if config.GetBool('want-rpc-server', False):
            endpoint = config.GetString('rpc-server-endpoint', 'http://localhost:8080/')
            self.rpcServer = ToontownRPCServer(endpoint, ToontownRPCHandler(self))
            self.rpcServer.start(useTaskChain=True)

        self.backups = BackupManager.BackupManager(
            filepath=self.config.GetString('backups-filepath', 'backups/'),
            extension=self.config.GetString('backups-extension', '.json'))

        self.createGlobals()
        self.notify.info('Done.')

    def createGlobals(self):
        """
        Create "global" objects.
        """

        self.csm = simbase.air.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')
        self.chatAgent = simbase.air.generateGlobalObject(OTP_DO_ID_CHAT_MANAGER, 'ChatAgent')
        self.friendsManager = simbase.air.generateGlobalObject(OTP_DO_ID_tte_FRIENDS_MANAGER, 'tteFriendsManager')
        self.globalPartyMgr = simbase.air.generateGlobalObject(OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')
        self.groupManager = simbase.air.generateGlobalObject(OPT_DO_ID_GROUP_MANAGER, 'GroupManager')
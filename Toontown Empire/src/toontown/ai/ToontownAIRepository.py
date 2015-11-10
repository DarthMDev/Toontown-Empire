from direct.distributed.PyDatagram import *
from panda3d.core import *

from src.otp.ai.AIZoneData import AIZoneDataStore
from src.otp.ai.MagicWordManagerAI import MagicWordManagerAI
from src.otp.ai.TimeManagerAI import TimeManagerAI
from src.otp.ai import BanManagerAI
from src.otp.distributed.OtpDoGlobals import *
from src.otp.friends.FriendManagerAI import FriendManagerAI
from src.toontown.ai import CogPageManagerAI
from src.toontown.ai import CogSuitManagerAI
from src.toontown.ai import PromotionManagerAI
from src.toontown.ai.FishManagerAI import FishManagerAI
from src.toontown.ai.NewsManagerAI import NewsManagerAI
from src.toontown.ai.QuestManagerAI import QuestManagerAI
from src.toontown.ai.DistributedBlackCatMgrAI import DistributedBlackCatMgrAI
from src.toontown.ai.DistributedReportMgrAI import DistributedReportMgrAI
from src.toontown.building.DistributedBuildingQueryMgrAI import DistributedBuildingQueryMgrAI
from src.toontown.building.DistributedTrophyMgrAI import DistributedTrophyMgrAI
from src.toontown.catalog.CatalogManagerAI import CatalogManagerAI
from src.toontown.coghq import CountryClubManagerAI
from src.toontown.coghq import FactoryManagerAI
from src.toontown.coghq import LawOfficeManagerAI
from src.toontown.coghq import MintManagerAI
from src.toontown.distributed.ToontownDistrictAI import ToontownDistrictAI
from src.toontown.distributed.ToontownDistrictStatsAI import ToontownDistrictStatsAI
from src.toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from src.toontown.coderedemption.TTCodeRedemptionMgrAI import TTCodeRedemptionMgrAI
from src.toontown.dna.DNAParser import loadDNAFileAI
from src.toontown.estate.EstateManagerAI import EstateManagerAI
from src.toontown.hood import BRHoodAI
from src.toontown.hood import BossbotHQAI
from src.toontown.hood import CashbotHQAI
from src.toontown.hood import DDHoodAI
from src.toontown.hood import DGHoodAI
from src.toontown.hood import DLHoodAI
from src.toontown.hood import GSHoodAI
from src.toontown.hood import GZHoodAI
from src.toontown.hood import LawbotHQAI
from src.toontown.hood import MMHoodAI
from src.toontown.hood import OZHoodAI
from src.toontown.hood import SellbotHQAI
from src.toontown.hood import TTHoodAI
from src.toontown.hood import ZoneUtil
from src.toontown.racing.LeaderboardMgrAI import LeaderboardMgrAI
from src.toontown.parties.ToontownTimeManagerAI import ToontownTimeManagerAI
from src.toontown.pets.PetManagerAI import PetManagerAI
from src.toontown.safezone.SafeZoneManagerAI import SafeZoneManagerAI
from src.toontown.suit.SuitInvasionManagerAI import SuitInvasionManagerAI
from src.toontown.groups.GroupManagerAI import GroupManagerAI
from src.toontown.toon import NPCToons
from src.toontown.toonbase import ToontownGlobals
from src.toontown.tutorial.TutorialManagerAI import TutorialManagerAI
from src.toontown.uberdog.DistributedPartyManagerAI import DistributedPartyManagerAI
#from src.toontown.uberdog.DistributedLobbyManagerAI import DistributedLobbyManagerAI

class ToontownAIRepository(ToontownInternalRepository):
    def __init__(self, baseChannel, stateServerChannel, districtName):
        ToontownInternalRepository.__init__(
            self, baseChannel, stateServerChannel, dcSuffix='AI')

        self.districtName = districtName

        self.notify.setInfo(True)  # Our AI repository should always log info.
        self.hoods = []
        self.cogHeadquarters = []
        self.dnaStoreMap = {}
        self.dnaDataMap = {}
        self.suitPlanners = {}
        self.buildingManagers = {}
        self.disconnectedToons = {}
        self.factoryMgr = None
        self.mintMgr = None
        self.lawOfficeMgr = None
        self.countryClubMgr = None
        self.groupManager = GroupManagerAI(self)

        self.zoneAllocator = UniqueIdAllocator(ToontownGlobals.DynamicZonesBegin,
                                               ToontownGlobals.DynamicZonesEnd)
        self.zoneDataStore = AIZoneDataStore()

        self.wantFishing = self.config.GetBool('want-fishing', True)
        self.wantHousing = self.config.GetBool('want-housing', True)
        self.wantPets = self.config.GetBool('want-pets', True)
        self.wantKarts = self.config.GetBool('want-karts', True)
        self.wantParties = self.config.GetBool('want-parties', True)
        self.wantEmblems = self.config.GetBool('want-emblems', True)
        self.wantCogbuildings = self.config.GetBool('want-cogbuildings', True)
        self.wantCogdominiums = self.config.GetBool('want-cogdominiums', True)
        self.wantTrackClsends = self.config.GetBool('want-track-clsends', False)
        self.baseXpMultiplier = self.config.GetFloat('base-xp-multiplier', 1.0)

        self.cogSuitMessageSent = False

    def createManagers(self):
        self.timeManager = TimeManagerAI(self)
        self.timeManager.generateWithRequired(2)
        self.toontownTimeManager = ToontownTimeManagerAI()
        self.magicWordManager = MagicWordManagerAI(self)
        self.magicWordManager.generateWithRequired(2)
        self.newsManager = NewsManagerAI(self)
        self.newsManager.generateWithRequired(2)
        self.safeZoneManager = SafeZoneManagerAI(self)
        self.safeZoneManager.generateWithRequired(2)
        self.tutorialManager = TutorialManagerAI(self)
        self.tutorialManager.generateWithRequired(2)
        self.friendManager = FriendManagerAI(self)
        self.friendManager.generateWithRequired(2)
        self.questManager = QuestManagerAI(self)       
        self.banManager = BanManagerAI.BanManagerAI(self)
        self.suitInvasionManager = SuitInvasionManagerAI(self)
        self.blackCatMgr = DistributedBlackCatMgrAI(self)
        self.blackCatMgr.generateWithRequired(2)
        self.reportMgr = DistributedReportMgrAI(self)
        self.reportMgr.generateWithRequired(2)
        self.trophyMgr = DistributedTrophyMgrAI(self)
        self.trophyMgr.generateWithRequired(2)
        self.cogSuitMgr = CogSuitManagerAI.CogSuitManagerAI()
        self.promotionMgr = PromotionManagerAI.PromotionManagerAI(self)
        self.cogPageManager = CogPageManagerAI.CogPageManagerAI()
        self.codeRedemptionMgr = TTCodeRedemptionMgrAI(self)
        self.codeRedemptionMgr.generateWithRequired(2)
        self.buildingQueryMgr = DistributedBuildingQueryMgrAI(self)
        self.buildingQueryMgr.generateWithRequired(2)
        self.groupManager.generateWithRequired(2)
        if self.wantKarts:
            self.leaderboardMgr = LeaderboardMgrAI(self)
        if self.wantFishing:
            self.fishManager = FishManagerAI(self)
        if self.wantHousing:
            self.estateManager = EstateManagerAI(self)
            self.estateManager.generateWithRequired(2)
            self.catalogManager = CatalogManagerAI(self)
            self.catalogManager.generateWithRequired(2)
        if self.wantPets:
            self.petMgr = PetManagerAI(self)
        if self.wantParties:
            self.partyManager = DistributedPartyManagerAI(self)
            self.partyManager.generateWithRequired(2)
            self.globalPartyMgr = self.generateGlobalObject(
                OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')
        #self.lobbyManager = DistributedLobbyManagerAI(self)
        #self.lobbyManager.generateWithRequired(2)
        #self.globalLobbyMgr = self.generateGlobalObject(
        #    OTP_DO_ID_GLOBAL_LOBBY_MANAGER, 'GlobalLobbyManager')
        self.megaInvasionManager = simbase.air.generateGlobalObject(
            OTP_DO_ID_MEGA_INVASION_MANAGER, 'MegaInvasionManager')

    def createSafeZones(self):
        NPCToons.generateZone2NpcDict()
        if self.config.GetBool('want-toontown-central', True):
            self.hoods.append(TTHoodAI.TTHoodAI(self))
        if self.config.GetBool('want-donalds-dock', True):
            self.hoods.append(DDHoodAI.DDHoodAI(self))
        if self.config.GetBool('want-daisys-garden', True):
            self.hoods.append(DGHoodAI.DGHoodAI(self))
        if self.config.GetBool('want-minnies-melodyland', True):
            self.hoods.append(MMHoodAI.MMHoodAI(self))
        if self.config.GetBool('want-the-brrrgh', True):
            self.hoods.append(BRHoodAI.BRHoodAI(self))
        if self.config.GetBool('want-donalds-dreamland', True):
            self.hoods.append(DLHoodAI.DLHoodAI(self))
        if self.config.GetBool('want-goofy-speedway', True):
            self.hoods.append(GSHoodAI.GSHoodAI(self))
        if self.config.GetBool('want-outdoor-zone', True):
            self.hoods.append(OZHoodAI.OZHoodAI(self))
        if self.config.GetBool('want-golf-zone', True):
            self.hoods.append(GZHoodAI.GZHoodAI(self))

    def createCogHeadquarters(self):
        NPCToons.generateZone2NpcDict()
        if self.config.GetBool('want-sellbot-headquarters', True):
            self.factoryMgr = FactoryManagerAI.FactoryManagerAI(self)
            self.cogHeadquarters.append(SellbotHQAI.SellbotHQAI(self))
        if self.config.GetBool('want-cashbot-headquarters', True):
            self.mintMgr = MintManagerAI.MintManagerAI(self)
            self.cogHeadquarters.append(CashbotHQAI.CashbotHQAI(self))
        if self.config.GetBool('want-lawbot-headquarters', True):
            self.lawOfficeMgr = LawOfficeManagerAI.LawOfficeManagerAI(self)
            self.cogHeadquarters.append(LawbotHQAI.LawbotHQAI(self))
        if self.config.GetBool('want-bossbot-headquarters', True):
            self.countryClubMgr = CountryClubManagerAI.CountryClubManagerAI(self)
            self.cogHeadquarters.append(BossbotHQAI.BossbotHQAI(self))

    def handleConnected(self):
        ToontownInternalRepository.handleConnected(self)
        self.districtId = self.allocateChannel()
        self.notify.info('Creating ToontownDistrictAI(%d)...' % self.districtId)
        self.distributedDistrict = ToontownDistrictAI(self)
        self.distributedDistrict.setName(self.districtName)
        self.distributedDistrict.generateWithRequiredAndId(
            self.districtId, self.getGameDoId(), 2)
        self.notify.info('Claiming ownership of channel ID: %d...' % self.districtId)
        self.claimOwnership(self.districtId)

        self.districtStats = ToontownDistrictStatsAI(self)
        self.districtStats.setDistrictId(self.districtId)
        self.districtStats.generateWithRequiredAndId(
            self.allocateChannel(), self.getGameDoId(), 3)
        self.notify.info('Created ToontownDistrictStats(%d)' % self.districtStats.doId)

        self.notify.info('Creating managers...')
        self.createManagers()
        if self.config.GetBool('want-safe-zones', True):
            self.notify.info('Creating safe zones...')
            self.createSafeZones()
        if self.config.GetBool('want-cog-headquarters', True):
            self.notify.info('Creating Cog headquarters...')
            self.createCogHeadquarters()

        self.notify.info('Making district available...')
        self.distributedDistrict.b_setAvailable(1)
        self.notify.info('Done.')

    def claimOwnership(self, channelId):
        datagram = PyDatagram()
        datagram.addServerHeader(channelId, self.ourChannel, STATESERVER_OBJECT_SET_AI)
        datagram.addChannel(self.ourChannel)
        self.send(datagram)

    def lookupDNAFileName(self, zoneId):
        zoneId = ZoneUtil.getCanonicalZoneId(zoneId)
        hoodId = ZoneUtil.getCanonicalHoodId(zoneId)
        hood = ToontownGlobals.dnaMap[hoodId]
        if hoodId == zoneId:
            zoneId = 'sz'
            phaseNum = ToontownGlobals.phaseMap[hoodId]
        else:
            phaseNum = ToontownGlobals.streetPhaseMap[hoodId]
        return 'phase_%s/dna/%s_%s.pdna' % (phaseNum, hood, zoneId)

    def loadDNAFileAI(self, dnastore, filename):
        return loadDNAFileAI(dnastore, filename)

    def incrementPopulation(self):
        self.districtStats.b_setAvatarCount(self.districtStats.getAvatarCount() + 1)

    def decrementPopulation(self):
        self.districtStats.b_setAvatarCount(self.districtStats.getAvatarCount() - 1)

    def allocateZone(self):
        return self.zoneAllocator.allocate()

    def deallocateZone(self, zone):
        self.zoneAllocator.free(zone)

    def getZoneDataStore(self):
        return self.zoneDataStore

    def getTrackClsends(self):
        return self.wantTrackClsends

    def getAvatarExitEvent(self, avId):
        return 'distObjDelete-%d' % avId

    def trueUniqueName(self, name):
        return self.uniqueName(name)

    def setAvatarDisconnectReason(self, avId, reason):
        self.disconnectedToons[avId] = reason

    def getAvatarDisconnectReason(self, avId):
        reason = self.disconnectedToons[avId]
        del self.disconnectedToons[avId]
        return reason
from src.toontown.building import DistributedCFOElevatorAI
from src.toontown.building import FADoorCodes
from src.toontown.building.DistributedBoardingPartyAI import DistributedBoardingPartyAI
from src.toontown.coghq.DistributedMintElevatorExtAI import DistributedMintElevatorExtAI
from src.toontown.hood import CogHQAI
from src.toontown.suit import DistributedCashbotBossAI
from src.toontown.suit import DistributedSuitPlannerAI
from src.toontown.toonbase import ToontownGlobals


class CashbotHQAI(CogHQAI.CogHQAI):
    def __init__(self, air):
        CogHQAI.CogHQAI.__init__(
            self, air, ToontownGlobals.CashbotHQ, ToontownGlobals.CashbotLobby,
            FADoorCodes.CB_DISGUISE_INCOMPLETE,
            DistributedCFOElevatorAI.DistributedCFOElevatorAI,
            DistributedCashbotBossAI.DistributedCashbotBossAI)

        self.mintElevators = []
        self.mintBoardingParty = None
        self.suitPlanners = []

        self.startup()

    def startup(self):
        CogHQAI.CogHQAI.startup(self)

        self.createMintElevators()
        if simbase.config.GetBool('want-boarding-groups', True):
            self.createMintBoardingParty()
        if simbase.config.GetBool('want-suit-planners', True):
            self.createSuitPlanners()

    def createMintElevators(self):
        destZones = (
            ToontownGlobals.CashbotMintIntA,
            ToontownGlobals.CashbotMintIntB,
            ToontownGlobals.CashbotMintIntC
        )
        mins = ToontownGlobals.FactoryLaffMinimums[1]
        for i in xrange(len(destZones)):
            mintElevator = DistributedMintElevatorExtAI(
                self.air, self.air.mintMgr, destZones[i],
                antiShuffle=0, minLaff=mins[i])
            mintElevator.generateWithRequired(self.zoneId)
            self.mintElevators.append(mintElevator)

    def createMintBoardingParty(self):
        mintIdList = []
        for mintElevator in self.mintElevators:
            mintIdList.append(mintElevator.doId)
        self.mintBoardingParty = DistributedBoardingPartyAI(self.air, mintIdList, 4)
        self.mintBoardingParty.generateWithRequired(self.zoneId)

    def createSuitPlanners(self):
        suitPlanner = DistributedSuitPlannerAI.DistributedSuitPlannerAI(self.air, self.zoneId)
        suitPlanner.generateWithRequired(self.zoneId)
        suitPlanner.d_setZoneId(self.zoneId)
        suitPlanner.initTasks()
        self.suitPlanners.append(suitPlanner)
        self.air.suitPlanners[self.zoneId] = suitPlanner

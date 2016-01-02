from panda3d.core import *
from direct.interval.IntervalGlobal import *
from src.toontown.battle.BattleBase import *
from src.toontown.coghq import DistributedLevelBattle
from direct.directnotify import DirectNotifyGlobal
from src.toontown.toon import TTEmote
from src.otp.avatar import Emote
from src.toontown.battle import SuitBattleGlobals
import random
from src.toontown.suit import SuitDNA
from direct.fsm import State
from direct.fsm import ClassicFSM, State
from src.toontown.toonbase import ToontownGlobals
from src.otp.nametag import NametagGlobals

class DistributedMintBattle(DistributedLevelBattle.DistributedLevelBattle):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMintBattle')

    def __init__(self, cr):
        DistributedLevelBattle.DistributedLevelBattle.__init__(self, cr)
        self.fsm.addState(State.State('MintReward', self.enterMintReward, self.exitMintReward, ['Resume']))
        offState = self.fsm.getStateNamed('Off')
        offState.addTransition('MintReward')
        playMovieState = self.fsm.getStateNamed('PlayMovie')
        playMovieState.addTransition('MintReward')

    def enterMintReward(self, ts):
        self.notify.debug('enterMintReward()')
        self.disableCollision()
        self.delayDeleteMembers()
        if self.hasLocalToon():
            NametagGlobals.setMasterArrowsOn(0)
            if self.bossBattle:
                messenger.send('localToonConfrontedMintBoss')
        self.movie.playReward(ts, self.uniqueName('building-reward'), self.__handleMintRewardDone, noSkip=True)

    def __handleMintRewardDone(self):
        self.notify.debug('mint reward done')
        if self.hasLocalToon():
            self.d_rewardDone(base.localAvatar.doId)
        self.movie.resetReward()
        self.fsm.request('Resume')

    def exitMintReward(self):
        self.notify.debug('exitMintReward()')
        self.movie.resetReward(finish=1)
        self._removeMembersKeep()
        NametagGlobals.setMasterArrowsOn(1)

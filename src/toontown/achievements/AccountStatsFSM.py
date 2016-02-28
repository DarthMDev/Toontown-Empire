from direct.fsm.FSM import FSM


class FetchAccountStatsFSM(FSM):
    def __init__(self, air, av, callback):
        FSM.__init__(self, 'AccountStatsFSM')

        self.air = air
        self.av = av
        self.callback = callback

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.av.getStatsId(),
                                         self.handleAccountStatsRecieved)

    def handleAccountStatsRecieved(self, dclass, fields):
        if dclass != self.air.dclassesByName['AccountStats']:
            self.notify.warning('Got %s dclass instead of AccountStats!' % dclass.getName())
            self.demand('Done', {})
            return

        self.demand('Done', fields)

    def enterDone(self, accountStats):
        if self.callback is not None:
            self.callback(self.av, accountStats)

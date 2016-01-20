class PlayerBase(object):

    def __init__(self):
        self.badgeState = False

    def atLocation(self, locationId):
        return True

    def getLocation(self):
        return []

    def setAsBadge(self, state):
        self.badgeState = state

    def isBadge(self):
        return self.badgeState

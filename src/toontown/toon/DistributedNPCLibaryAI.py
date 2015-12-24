# Work on this for like 15 minutes and will stay here until me or someone finishes it.
from DistributedNPCToonBaseAI import DistributedNPCToonBaseAI
from ToonDNA import ToonDNA
from toontown.toonbase import ToontownGlobals


class DistributedNPCLibaryAI(DistributedNPCToonBaseAI):

def HttpNameChangeRequest(self, url, **extras):
    signature = hashlib.sha512(json.dumps(_data) + apiSecret).hexdigest()
    data = urllib.urlencode({'data': json.dumps(_data), 'hmac': signature})
    req = urllib2.Request('http://www.toontownempire.com/ToonCouncilApproval/' + url, data)

    def addNameRequest(self, avId, name, accountID = None):
        return True

    def getNameStatus(self, accountId, callback = None):
        return 'APPROVED'

    def removeNameRequest(self, avId):
        pass

    def lookup(self, data, callback):
        userId = data['userId']

        data['success'] = True

        if str(userId) not in self.dbm:
            data['accountId'] = 0

        else:
            data['accountId'] = int(self.dbm[str(userId)])

        callback(data)
        return data

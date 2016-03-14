from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.fsm.FSM import FSM

from otp.ai.MagicWordGlobal import *
from otp.distributed import OtpDoGlobals

from toontown.makeatoon.NameGenerator import NameGenerator
from toontown.toon.ToonDNA import ToonDNA
from toontown.toonbase import TTLocalizer
from toontown.uberdog import NameJudgeBlacklist

from panda3d.core import *

import hashlib, hmac, json
import anydbm, math, os
import urllib2, time, urllib
import cookielib, socket

def rejectConfig(issue, securityIssue=True, retarded=True):
    print
    print
    print 'Lemme get this straight....'
    print 'You are trying to use remote account database type...'
    print 'However,', issue + '!!!!'
    if securityIssue:
        print 'Do you want this server to get hacked?'
    if retarded:
        print '"Either down\'s or autism"\n  - JohnnyDaPirate, 2015'
    print 'Go fix that!'
    exit()

def entropy(string):
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy

def entropyIdeal(length):
    prob = 1.0 / length
    return -length * prob * math.log(prob) / math.log(2.0)

accountDBType = config.GetString('accountdb-type', 'developer')
accountServerSecret = config.GetString('account-server-secret', 'dev')
accountServerHashAlgo = config.GetString('account-server-hash-algo', 'sha512')
apiSecret = accountServerSecret = config.GetString('api-key', 'dev')
if accountDBType == 'mongodb':
    import pymongo
    import bcrypt
    from pymongo import MongoClient

if accountDBType == 'mysqldb':
    from passlib.hash import bcrypt
    import mysql.connector

if accountDBType == 'remote':
    if accountServerSecret == 'dev':
        rejectConfig('you have not changed the secret in config/local.prc')

    if apiSecret == 'dev':
        rejectConfig('you have not changed the api key in config/local.prc')

    if len(accountServerSecret) < 16:
        rejectConfig('the secret is too small! Make it 16+ bytes', retarded=False)

    secretLength = len(accountServerSecret)
    ideal = entropyIdeal(secretLength) / 2
    entropy = entropy(accountServerSecret)
    if entropy < ideal:
        rejectConfig('the secret entropy is too low! For %d bytes,'
                     ' it should be %d. Currently it is %d' % (secretLength, ideal, entropy),
                     retarded=False)

    hashAlgo = getattr(hashlib, accountServerHashAlgo, None)
    if not hashAlgo:
        rejectConfig('%s is not a valid hash algo' % accountServerHashAlgo, securityIssue=False)

    hashSize = len(hashAlgo('').digest())

minAccessLevel = config.GetInt('min-access-level', 0)

def executeHttpRequest(url, **extras):
    print "executeHttpRequest: ", accountDBType, url, extras

    if accountDBType == 'remote':
        timestamp = str(int(time.time()))
        signature = hmac.new(accountServerSecret, timestamp, hashlib.sha256)
        request = urllib2.Request(accountServerEndpoint + url)
        request.add_header('User-Agent', 'TTI-CSM')
        request.add_header('X-CSM-Timestamp', timestamp)
        request.add_header('X-CSM-Signature', signature.hexdigest())
        for k, v in extras.items():
            request.add_header('X-CSM-' + k, v)
        try:
            return urllib2.urlopen(request).read()
        except:
            return None

    if accountDBType == 'mysqldb':
        if url == 'accounts/ban/':
            print [extras['Id'], extras['Release'], extras['Reason']]
        return None;

    return None;

def executeHttpRequestAndLog(url, **extras):
    # SEE ABOVE
    response = executeHttpRequest(url, extras)

    if response is None:
        notify.error('A request to ' + url + ' went wrong.')
        return None

    try:
        data = json.loads(response)
    except:
        notify.error('Malformed response from ' + url + '.')
        return None

    if 'error' in data:
        notify.warning('Error from ' + url + ':' + data['error'])

    return data

#blacklist = executeHttpRequest('names/blacklist.json') # todo; create a better system for this
blacklist = json.dumps(["none"])
if blacklist:
    blacklist = json.loads(blacklist)

def judgeName(name):
    if not name:
        return False
    if blacklist:
        for namePart in name.split(' '):
            namePart = namePart.lower()
            if len(namePart) < 1:
                return False
            for banned in blacklist:
                if banned in namePart:
                    return False
    return True

# --- ACCOUNT DATABASES ---
# These classes make up the available account databases for Toontown Stride.
# DeveloperAccountDB is a special database that accepts a username, and assigns
# each user with 700 access automatically upon login.

class AccountDB:
    notify = directNotify.newCategory('AccountDB')

    def __init__(self, csm):
        self.csm = csm

        filename = config.GetString('account-bridge-filename', 'account-bridge.db')
        filename = os.path.join('dependencies', filename)

        self.dbm = anydbm.open(filename, 'c')

    def addNameRequest(self, avId, name, accountID = None):
        return True

    def getNameStatus(self, accountId, callback = None):
        return 'APPROVED'

    def removeNameRequest(self, avId):
        pass

    def lookup(self, data, callback):
        userId = data['userId']

        data['success'] = True
        data['accessLevel'] = max(data['accessLevel'], minAccessLevel)

        if str(userId) not in self.dbm:
            data['accountId'] = 0

        else:
            data['accountId'] = int(self.dbm[str(userId)])

        callback(data)
        return data

    def storeAccountID(self, userId, accountId, callback):
        self.dbm[str(userId)] = str(accountId)  # anydbm only allows strings.
        if getattr(self.dbm, 'sync', None):
            self.dbm.sync()
            callback(True)
        else:
            self.notify.warning('Unable to associate user %s with account %d!' % (userId, accountId))
            callback(False)

class DeveloperAccountDB(AccountDB):
    notify = directNotify.newCategory('DeveloperAccountDB')

    def lookup(self, userId, callback):
        return AccountDB.lookup(self, {'userId': userId,
                                       'accessLevel': 0,
                                       'notAfter': 0},
                                callback)

# Mongo implementation of the AccountDB
#
# This was never used in production and might possibly not work.
# Still, it is a good starting point.  This has a similar behavior to
# DeveloperAccountDB and LocalAccountDB in that it automatically
# registers new users, the first user that is created
# gets 700 access, and every user created afterwards gets 100 access.
#
# params:
#    mongodb-url   how to connect to the mongodb
#    mongodb-name  What db to use
#
# dependencies:
#    pip install py-bcrypt PyMongo

class MongoAccountDB(AccountDB):
    notify = directNotify.newCategory('MongoAccountDB')

    def get_hashed_password(self, plain_text_password):
        newpass = bcrypt.encrypt(plain_text_password)
        return newpass
 
    def check_password(self, plain_text_password, hashed_password):
        return bcrypt.verify(plain_text_password, hashed_password)

    def __init__(self, csm):
        self.csm = csm

        dburl = simbase.config.GetString('mongodb-url', 'mongodb://localhost:21021')
        self.client = MongoClient(dburl)

        dbname = simbase.config.GetString('mongodb-name', 'test')
        self.db = self.client[dbname]

        self.accounts = self.db.accountdb
        self.nameStatus = self.db.nameStatus

    def addNameRequest(self, avId, name):
        self.nameStatus.insert( { "avId": avId, "name": name, "status": "PENDING" } )
        return 'Success'

    def getNameStatus(self, avId):
        stat = self.nameStatus[avId]
        if stat:
            return stat["status"]
        return 'REJECTED'

    def removeNameRequest(self, avId):
        self.nameStatus.remove( { "avId": avId } )
        return 'Success'

    def lookup(self, token, callback):
        try:
            tokenList = token.split(':')
    
            if len(tokenList) != 2:
                response = {
                  'success': False,
                  'reason': "invalid password format"
                }
                callback(response)
                return response

            username = tokenList[0]
            password = tokenList[1]

            # special case for first user
            if accounts.count() == 0:
                account = { "username": username, "password": self.get_hashed_password(password), "accountId": 0, "accessLevel": 700}
                accounts.insert(account)
                response = {
                  'success': True,
                  'userId': username,
                  'accountId': 0,
                  'accessLevel': 700
                }
                callback(response)
                return response

            account = accounts.find_one({"username": username})

            if account:
                if not self.check_password(password, account["password"]):
                    response = {
                      'success': False,
                      'reason': "invalid password"
                    }
                    callback(response)
                    return response

                response = {
                    'success': True,
                    'userId': username,
                    'accountId': int(account["accountId"]),
                    'accessLevel': int(account["accessLevel"])
                }
                callback(response)
                return response

            account = { "username": username, "password": self.get_hashed_password(password), "accountId": 0, "accessLevel": max(100, minAccessLevel)}
            accounts.insert(account)

            response = {
              'success': True,
              'userId': username,
              'accountId': 0,
              'accessLevel': int(account["accessLevel"])
            }

            callback(response)
            return response
                
        except:
            self.notify.warning('Could not decode the provided token!')
            response = {
                'success': False,
                'reason': "Can't decode this token."
            }
            callback(response)
            return response

    def storeAccountID(self, userId, accountId, callback):
        account = accounts.find_one({"username": userId})
        if account:
            accounts.update({"username": userId}, {"$set": {"accountId": accountId}})
            callback(True)
        else:
            self.notify.warning('Unable to associate user %s with account %d!' % (userId, accountId))
            callback(False)

# MySQL implementation of the AccountDB
#
# params:
#        'mysql-username' =>  'toontown'
#        'mysql-password' =>  'password'
#        'mysql-db' =>  'toontown'
#        'mysql-host' =>  '127.0.0.1'
#        'mysql-port' =>  3306
#        'mysql-ssl' =>  False
#        'mysql-ssl-ca' =>  ''
#        'mysql-ssl-cert' =>  ''
#        'mysql-ssl-key' =>  ''
#        'mysql-ssl-verify-cert' =>  False
#        'mysql-auto-new-account' =>  True

# dependencies:
#    apt-get install python-mysqldb
#    pip install passlib

class MySQLAccountDB(AccountDB):
    notify = directNotify.newCategory('MySQLAccountDB')

    def get_hashed_password(self, plain_text_password):
        return bcrypt.encrypt(plain_text_password)

    def check_password(self, plain_text_password, hashed_password):
        try:
            return bcrypt.verify(plain_text_password, hashed_password)
        except:
            print ("bad hash: ", (plain_text_password, hashed_password))
            return False

    def create_database(self, cursor):
      try:
          cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.db))
      except mysql.connector.Error as err:
          print("Failed creating database: {}".format(err))
          exit(1)


    def auto_migrate_semidbm(self):
        self.cur.execute(self.count_account)
        row = self.cur.fetchone()
        if row[0] != 0:
            return

        filename = simbase.config.GetString(
            'account-bridge-filename', 'account-bridge')
        dbm = semidbm.open(filename, 'c')

        for account in dbm.keys():
            accountid = dbm[account]
            print "%s maps to %s"%(account, accountid)
            self.cur.execute(self.add_account, (account,  "", accountid, 0, 0))
        self.cnx.commit()
        dbm.close()

    def __init__(self, csm):
        self.csm = csm

        # Just a few configuration options
        self.username = simbase.config.GetString('mysql-username', 'toontown')
        self.password = simbase.config.GetString('mysql-password', 'password')
        self.db = simbase.config.GetString('mysql-db', 'toontown')
        self.host = simbase.config.GetString('mysql-host', '127.0.0.1')
        self.port = simbase.config.GetInt('mysql-port', 3306)
        self.ssl = simbase.config.GetBool('mysql-ssl', False)
        self.ssl_ca = simbase.config.GetString('mysql-ssl-ca', '')
        self.ssl_cert = simbase.config.GetString('mysql-ssl-cert', '')
        self.ssl_key = simbase.config.GetString('mysql-ssl-key', '')
        self.ssl_verify_cert = simbase.config.GetBool('mysql-ssl-verify-cert', False)
        self.auto_migrate = True

        # Lets try connection to the db
        if self.ssl:
            self.config = {
              'user': self.username,
              'password': self.password,
              'db': self.db,
              'host': self.host,
              'port': self.port,
              'client_flags': [ClientFlag.SSL],
              'ssl_ca': self.ssl_ca,
              'ssl_cert': self.ssl_cert,
              'ssl_key': self.ssl_key,
              'ssl_verify_cert': self.ssl_verify_cert
            }
        else:
            self.config = {
              'user': self.username,
              'password': self.password,
              'db': self.db,
              'host': self.host,
              'port': self.port,
            }

        self.cnx = mysql.connector.connect(**self.config)
        self.cur = self.cnx.cursor(buffered=True)

        # First we try to change the the particular db using the
        # database property.  If there is an error, we try to
        # create the database and then switch to it.

        try:
            self.cnx.database = self.db
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.create_database(self.cur)
                self.cnx.database = self.db
            else:
                print(err)
                exit(1)


        self.count_account = ("SELECT COUNT(*) from Accounts")
        self.select_account = ("SELECT password,accountId,accessLevel,status,rawPassword FROM Accounts where username = %s")
        self.add_account = ("REPLACE INTO Accounts (username, password, accountId, accessLevel, rawPassword) VALUES (%s, %s, %s, %s, %s)")
        self.update_avid = ("UPDATE Accounts SET accountId = %s where username = %s")
        self.update_password = ("UPDATE Accounts SET password = %s, rawPassword = '1' where username = %s")
        self.count_avid = ("SELECT COUNT(*) from Accounts WHERE username = %s")


        self.select_name = ("SELECT status FROM NameApprovals where avId = %s")
        self.add_name_request = ("REPLACE INTO NameApprovals (avId, name, status) VALUES (%s, %s, %s)")
        self.delete_name_query = ("DELETE FROM NameApprovals where avId = %s")


        if self.auto_migrate:
            self.auto_migrate_semidbm()

    def __del__(self):
        try:
            this.cur.close()
        except:
            pass

        try:
            this.cnx.close()
        except:
            pass


    def addNameRequest(self, avId, name):
       self.cur.execute(self.add_name_request, (avId, name, "PENDING"))
       self.cnx.commit()
       return 'Success'
        
    def getNameStatus(self, avId):
        self.cur.execute(self.select_name, (avId,))
        row = self.cur.fetchone()
        if row:
            return row[0]
        return "REJECTED"

    def removeNameRequest(self, avId):
        self.cur.execute(self.delete_name_query, (avId,))
        return 'Success'

    def lookup(self, token, callback):
        try:
            tokenList = token.split(':')

            if len(tokenList) != 2:
                response = {
                  'success': False,
                  'reason': "invalid password format"
                }
                print response
                callback(response)
                return response

            username = tokenList[0]
            password = tokenList[1]


            self.cur.execute(self.select_account, (username,))
            row = self.cur.fetchone()
            self.cnx.commit()

            if row:
                if not self.check_password(password, row[0]):
                    response = {
                      'success': False,
                      'reason': "invalid password"
                    }
                    callback(response)
                    return response

                response = {
                    'success': True,
                    'userId': username,
                    'accessLevel': int(row[2]),
                    'accountId': row[1]
                }

                print response
                callback(response)
                return response

            response = {
              'success': False,
              'reason': "unknown user"
            }
            print response
            callback(response)
            return response

        except mysql.connector.Error as err:
            print("mysql exception {}".format(err))
            response = {
                'success': False,
                'reason': "Can't decode this token."
            }
            print response
            callback(response)
            return response
#        except:
#            print "exception..."
#            self.notify.warning('Could not decode the provided token!')
#            response = {
#                'success': False,
#                'reason': "Can't decode this token."
#            }
#            print response
#            callback(response)
#            return response

    def storeAccountID(self, userId, accountId, callback):
        self.cur.execute(self.count_avid, (userId,))
        row = self.cur.fetchone()
    
        if row[0] >= 1:
            self.cur.execute(self.update_avid, (accountId, userId))
            self.cnx.commit()
            callback(True)
        else:
            print ("storeAccountId", self.update_avid, (accountId, userId))
            self.notify.warning('Unable to associate user %s with account %d!' % (userId, accountId))
            callback(False)

class RemoteAccountDB:
    # TO DO FOR NAMES:
    # CURRENTLY IT MAKES n REQUESTS FOR EACH AVATAR
    # IN THE FUTURE, MAKE ONLY 1 REQUEST
    # WHICH RETURNS ALL PENDING AVS
    # ^ done, check before removing todo note
    notify = directNotify.newCategory('RemoteAccountDB')

    def __init__(self, csm):
        self.csm = csm

    def addNameRequest(self, avId, name, accountID = None):
        username = avId
        if accountID is not None:
            username = accountID

        res = executeHttpRequest('names', action='set', username=str(username),
                                  avId=str(avId), wantedName=name)
        if res is not None:
            return True
        return False

    def getNameStatus(self, accountId, callback = None):
        r = executeHttpRequest('names', action='get', username=str(accountId))
        try:
            r = json.loads(r)
            if callback is not None:
                callback(r)
            return True
        except:
            return False

    def removeNameRequest(self, avId):
        r = executeHttpRequest('names', action='del', avId=str(avId))
        if r:
            return 'SUCCESS'
        return 'FAILURE'

    def lookup(self, token, callback):
        '''
        Token format:
        The token is obfuscated a bit, but nothing too hard to read.
        Most of the security is based on the hash.

        I. Data contained in a token:
            A json-encoded dict, which contains timestamp, userid and extra info

        II. Token format
            X = BASE64(ROT13(DATA)[::-1])
            H = HASH(X)[::-1]
            Token = BASE64(H + X)
        '''

        cookie_check = executeHttpRequest('cookie', cookie=token)

        try:
            check = json.loads(cookie_check)
            if check['success'] is not True:
                raise ValueError(check['error'])
            token = token.decode('base64')
            hash, token = token[:hashSize], token[hashSize:]
            correctHash = hashAlgo(token + accountServerSecret).digest()
            if len(hash) != len(correctHash):
                raise ValueError('Invalid hash.')

            value = 0
            for x, y in zip(hash[::-1], correctHash):
                value |= ord(x) ^ ord(y)

            if value:
                raise ValueError('Invalid hash.')

            token = json.loads(token.decode('base64')[::-1].decode('rot13'))

            if token['notAfter'] < int(time.time()):
                raise ValueError('Expired token.')
        except:
            resp = {'success': False}
            callback(resp)
            return resp

        return self.account_lookup(token, callback)

    def account_lookup(self, data, callback):
        data['success'] = True
        data['accessLevel'] = max(data['accessLevel'], minAccessLevel)
        data['accountId'] = int(data['accountId'])

        callback(data)
        return data

    def storeAccountID(self, userId, accountId, callback):
        r = executeHttpRequest('associateuser', username=str(userId), accountId=str(accountId))
        try:
            r = json.loads(r)
            if r['success']:
                callback(True)
            else:
                self.notify.warning('Unable to associate user %s with account %d, got the return message of %s!' % (userId, accountId, r['error']))
                callback(False)
        except:
            self.notify.warning('Unable to associate user %s with account %d!' % (userId, accountId))
            callback(False)


# --- FSMs ---
class OperationFSM(FSM):
    TARGET_CONNECTION = False

    def __init__(self, csm, target):
        self.csm = csm
        self.target = target

        FSM.__init__(self, self.__class__.__name__)

    def enterKill(self, reason=''):
        if self.TARGET_CONNECTION:
            self.csm.killConnection(self.target, reason)
        else:
            self.csm.killAccount(self.target, reason)
        self.demand('Off')

    def enterOff(self):
        if self.TARGET_CONNECTION:
            del self.csm.connection2fsm[self.target]
        else:
            del self.csm.account2fsm[self.target]

class LoginAccountFSM(OperationFSM):
    notify = directNotify.newCategory('LoginAccountFSM')
    TARGET_CONNECTION = True

    def enterStart(self, token):
        self.token = token
        self.demand('QueryAccountDB')

    def enterQueryAccountDB(self):
        self.csm.accountDB.lookup(self.token, self.__handleLookup)

    def __handleLookup(self, result):
        if not result.get('success'):
            self.csm.air.writeServerEvent('tokenRejected', self.target, self.token)
            self.demand('Kill', result.get('reason', 'The account server rejected your token.'))
            return

        self.userId = result.get('userId', 0)
        self.accountId = result.get('accountId', 0)
        self.accessLevel = result.get('accessLevel', 0)
        self.notAfter = result.get('notAfter', 0)
        if self.accountId:
            self.demand('RetrieveAccount')
        else:
            self.demand('CreateAccount')

    def enterRetrieveAccount(self):
        self.csm.air.dbInterface.queryObject(
            self.csm.air.dbId, self.accountId, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields

        if self.notAfter:
            if self.account.get('LAST_LOGIN_TS', 0) > self.notAfter:
                self.notify.debug('Rejecting old token: %d, notAfter=%d' % (self.account.get('LAST_LOGIN_TS', 0), self.notAfter))
                return self.__handleLookup({'success': False})

        self.demand('SetAccount')

    def enterCreateAccount(self):
        self.account = {
            'ACCOUNT_AV_SET': [0] * 6,
            'ESTATE_ID': 0,
            'ACCOUNT_AV_SET_DEL': [],
            'CREATED': time.ctime(),
            'LAST_LOGIN': time.ctime(),
            'LAST_LOGIN_TS': time.time(),
            'ACCOUNT_ID': str(self.userId),
            'ACCESS_LEVEL': self.accessLevel,
            'CHAT_SETTINGS': [1, 1]
        }
        self.csm.air.dbInterface.createObject(
            self.csm.air.dbId,
            self.csm.air.dclassesByName['AccountUD'],
            self.account,
            self.__handleCreate)

    def __handleCreate(self, accountId):
        if self.state != 'CreateAccount':
            self.notify.warning('Received a create account response outside of the CreateAccount state.')
            return

        if not accountId:
            self.notify.warning('Database failed to construct an account object!')
            self.demand('Kill', 'Your account object could not be created in the game database.')
            return

        self.accountId = accountId
        self.csm.air.writeServerEvent('accountCreated', accountId)
        self.demand('StoreAccountID')

    def enterStoreAccountID(self):
        self.csm.accountDB.storeAccountID(
            self.userId,
            self.accountId,
            self.__handleStored)

    def __handleStored(self, success=True):
        if not success:
            self.demand('Kill', 'The account server could not save your user ID!')
            return

        self.demand('SetAccount')

    def enterSetAccount(self):
        # If necessary, update their account information:
        if self.accessLevel:
            self.csm.air.dbInterface.updateObject(
                self.csm.air.dbId,
                self.accountId,
                self.csm.air.dclassesByName['AccountUD'],
                {'ACCESS_LEVEL': self.accessLevel})

        # If there's anybody on the account, kill them for redundant login:
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.csm.GetAccountConnectionChannel(self.accountId),
            self.csm.air.ourChannel,
            CLIENTAGENT_EJECT)
        datagram.addUint16(100)
        datagram.addString('This account has been logged in from elsewhere.')
        self.csm.air.send(datagram)

        # Next, add this connection to the account channel.
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.target,
            self.csm.air.ourChannel,
            CLIENTAGENT_OPEN_CHANNEL)
        datagram.addChannel(self.csm.GetAccountConnectionChannel(self.accountId))
        self.csm.air.send(datagram)

        # Subscribe to any "staff" channels that the account has access to.
        access = self.account.get('ADMIN_ACCESS', 0)
        if access >= 200:
            # Subscribe to the moderator channel.
            dg = PyDatagram()
            dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
            dg.addChannel(OtpDoGlobals.OTP_MOD_CHANNEL)
            self.csm.air.send(dg)
        if access >= 400:
            # Subscribe to the administrator channel.
            dg = PyDatagram()
            dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
            dg.addChannel(OtpDoGlobals.OTP_ADMIN_CHANNEL)
            self.csm.air.send(dg)
        if access >= 500:
            # Subscribe to the system administrator channel.
            dg = PyDatagram()
            dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
            dg.addChannel(OtpDoGlobals.OTP_SYSADMIN_CHANNEL)
            self.csm.air.send(dg)

        # Now set their sender channel to represent their account affiliation:
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.target,
            self.csm.air.ourChannel,
            CLIENTAGENT_SET_CLIENT_ID)
        # Account ID in high 32 bits, 0 in low (no avatar):
        datagram.addChannel(self.accountId << 32)
        self.csm.air.send(datagram)

        # Un-sandbox them!
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.target,
            self.csm.air.ourChannel,
            CLIENTAGENT_SET_STATE)
        datagram.addUint16(2)  # ESTABLISHED
        self.csm.air.send(datagram)

        # Update the last login timestamp:
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.accountId,
            self.csm.air.dclassesByName['AccountUD'],
            {'LAST_LOGIN': time.ctime(),
             'LAST_LOGIN_TS': time.time(),
             'ACCOUNT_ID': str(self.userId)})

        # We're done.
        self.csm.air.writeServerEvent('accountLogin', self.target, self.accountId, self.userId)
        self.csm.sendUpdateToChannel(self.target, 'acceptLogin', [int(time.time())])
        self.demand('Off')

class CreateAvatarFSM(OperationFSM):
    notify = directNotify.newCategory('CreateAvatarFSM')

    def enterStart(self, dna, thirdTrack, index):
        # Basic sanity-checking:
        if index < 0 or index >= 6:
            self.demand('Kill', 'Invalid index specified!')
            return

        if not ToonDNA().isValidNetString(dna):
            self.demand('Kill', 'Invalid DNA specified!')
            return

        if thirdTrack < 0 or thirdTrack == 4 or thirdTrack == 5 or thirdTrack >= 7:
            self.demand('Kill', 'Invalid third track specified!')
            return

        self.index = index
        self.dna = dna
        self.thirdTrack = thirdTrack

        # Okay, we're good to go, let's query their account.
        self.demand('RetrieveAccount')

    def enterRetrieveAccount(self):
        self.csm.air.dbInterface.queryObject(
            self.csm.air.dbId, self.target, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields

        # For use in calling name requests:
        self.accountID = self.account['ACCOUNT_ID']

        self.avList = self.account['ACCOUNT_AV_SET']
        # Sanitize:
        self.avList = self.avList[:6]
        self.avList += [0] * (6-len(self.avList))

        # Make sure the index is open:
        if self.avList[self.index]:
            self.demand('Kill', 'This avatar slot is already taken by another avatar!')
            return

        # Okay, there's space. Let's create the avatar!
        self.demand('CreateAvatar')

    def enterCreateAvatar(self):
        dna = ToonDNA()
        dna.makeFromNetString(self.dna)
        colorString = TTLocalizer.ColorfulToon
        animalType = TTLocalizer.AnimalToSpecies[dna.getAnimal()]
        name = ' '.join((colorString, animalType))
        trackAccess = [0, 0, 0, 0, 1, 1, 0]
        trackAccess[self.thirdTrack] = 1
        toonFields = {
            'setName': (name,),
            'setWishNameState': ('OPEN',),
            'setWishName': ('',),
            'setDNAString': (self.dna,),
            'setDISLid': (self.target,),
            'setTrackAccess': (trackAccess,)
        }
        self.csm.air.dbInterface.createObject(
            self.csm.air.dbId,
            self.csm.air.dclassesByName['DistributedToonUD'],
            toonFields,
            self.__handleCreate)

    def __handleCreate(self, avId):
        if not avId:
            self.demand('Kill', 'Database failed to create the new avatar object!')
            return

        self.avId = avId
        self.demand('StoreAvatar')

    def enterStoreAvatar(self):
        # Associate the avatar with the account...
        self.avList[self.index] = self.avId
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.target,
            self.csm.air.dclassesByName['AccountUD'],
            {'ACCOUNT_AV_SET': self.avList},
            {'ACCOUNT_AV_SET': self.account['ACCOUNT_AV_SET']},
            self.__handleStoreAvatar)

        self.accountID = self.account['ACCOUNT_ID']

    def __handleStoreAvatar(self, fields):
        if fields:
            self.demand('Kill', 'Database failed to associate the new avatar to your account!')
            return

        # Otherwise, we're done!
        self.csm.air.writeServerEvent('avatarCreated', self.avId, self.target, self.dna.encode('hex'), self.index)
        self.csm.sendUpdateToAccountId(self.target, 'createAvatarResp', [self.avId])
        self.demand('Off')

class AvatarOperationFSM(OperationFSM):
    POST_ACCOUNT_STATE = 'Off'  # This needs to be overridden.

    def enterRetrieveAccount(self):
        # Query the account:
        self.csm.air.dbInterface.queryObject(
            self.csm.air.dbId, self.target, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields

        # For use in calling name requests:
        self.accountID = self.account['ACCOUNT_ID']

        self.avList = self.account['ACCOUNT_AV_SET']
        # Sanitize:
        self.avList = self.avList[:6]
        self.avList += [0] * (6-len(self.avList))

        self.demand(self.POST_ACCOUNT_STATE)

class GetAvatarsFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('GetAvatarsFSM')
    POST_ACCOUNT_STATE = 'QueryAvatars'

    def enterStart(self):
        self.demand('RetrieveAccount')
        self.nameStateData = None

    def enterQueryAvatars(self):
        self.pendingAvatars = set()
        self.avatarFields = {}
        for avId in self.avList:
            if avId:
                self.pendingAvatars.add(avId)

                def response(dclass, fields, avId=avId):
                    if self.state != 'QueryAvatars':
                        return
                    if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
                        self.demand('Kill', "One of the account's avatars is invalid!")
                        return
                    self.avatarFields[avId] = fields
                    self.pendingAvatars.remove(avId)
                    if not self.pendingAvatars:
                        self.demand('SendAvatars')

                self.csm.air.dbInterface.queryObject(
                    self.csm.air.dbId,
                    avId,
                    response)

        if not self.pendingAvatars:
            self.demand('SendAvatars')

    def enterSendAvatars(self):
        potentialAvs = []

        for avId, fields in self.avatarFields.items():
            index = self.avList.index(avId)
            wishNameState = fields.get('setWishNameState', [''])[0]
            name = fields['setName'][0]
            nameState = 0

            if wishNameState == 'OPEN':
                nameState = 1
            elif wishNameState == 'PENDING':
                if accountDBType == 'remote':
                    if self.nameStateData is None:
                        self.demand('QueryNameState')
                        return
                    actualNameState = self.nameStateData[str(avId)]
                else:
                    actualNameState = self.csm.accountDB.getNameStatus(self.account['ACCOUNT_ID'])
                self.csm.air.dbInterface.updateObject(
                    self.csm.air.dbId,
                    avId,
                    self.csm.air.dclassesByName['DistributedToonUD'],
                    {'setWishNameState': [actualNameState]}
                )
                if actualNameState == 'PENDING':
                    nameState = 2
                if actualNameState == 'APPROVED':
                    nameState = 3
                    name = fields['setWishName'][0]
                elif actualNameState == 'REJECTED':
                    nameState = 4
            elif wishNameState == 'APPROVED':
                nameState = 3
            elif wishNameState == 'REJECTED':
                nameState = 4

            potentialAvs.append([avId, name, fields['setDNAString'][0],
                                 index, nameState])

        self.csm.sendUpdateToAccountId(self.target, 'setAvatars', [self.account['CHAT_SETTINGS'], potentialAvs])
        self.demand('Off')

    def enterQueryNameState(self):
        def gotStates(data):
            self.nameStateData = data
            taskMgr.doMethodLater(0, GetAvatarsFSM.demand, 'demand-QueryAvatars',
                                  extraArgs=[self, 'QueryAvatars'])

        self.csm.accountDB.getNameStatus(self.account['ACCOUNT_ID'], gotStates)
        # We should've called the taskMgr action by now.


# This inherits from GetAvatarsFSM, because the delete operation ends in a
# setAvatars message being sent to the client.
class DeleteAvatarFSM(GetAvatarsFSM):
    notify = directNotify.newCategory('DeleteAvatarFSM')
    POST_ACCOUNT_STATE = 'ProcessDelete'

    def enterStart(self, avId):
        self.avId = avId
        GetAvatarsFSM.enterStart(self)

    def enterProcessDelete(self):
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to delete an avatar not in the account!')
            return

        index = self.avList.index(self.avId)
        self.avList[index] = 0

        avsDeleted = list(self.account.get('ACCOUNT_AV_SET_DEL', []))
        avsDeleted.append([self.avId, int(time.time())])

        estateId = self.account.get('ESTATE_ID', 0)

        if estateId != 0:
            # This assumes that the house already exists, but it shouldn't
            # be a problem if it doesn't.
            self.csm.air.dbInterface.updateObject(
                self.csm.air.dbId,
                estateId,
                self.csm.air.dclassesByName['DistributedEstateAI'],
                {'setSlot%dToonId' % index: [0],
                 'setSlot%dGarden' % index: [[]]}
            )

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.target,
            self.csm.air.dclassesByName['AccountUD'],
            {'ACCOUNT_AV_SET': self.avList,
             'ACCOUNT_AV_SET_DEL': avsDeleted},
            {'ACCOUNT_AV_SET': self.account['ACCOUNT_AV_SET'],
             'ACCOUNT_AV_SET_DEL': self.account['ACCOUNT_AV_SET_DEL']},
            self.__handleDelete)
        self.csm.accountDB.removeNameRequest(self.avId)

    def __handleDelete(self, fields):
        if fields:
            self.demand('Kill', 'Database failed to mark the avatar as deleted!')
            return

        self.csm.air.friendsManager.clearList(self.avId)
        self.csm.air.writeServerEvent('avatarDeleted', self.avId, self.target)
        self.demand('QueryAvatars')

class SetNameTypedFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('SetNameTypedFSM')
    POST_ACCOUNT_STATE = 'RetrieveAvatar'

    def enterStart(self, avId, name):
        self.avId = avId
        self.name = name
        self.set_account_id = None

        if self.avId:
            self.demand('RetrieveAccount')
            return

        # Hmm, self.avId was 0. Okay, let's just cut to the judging:
        self.demand('JudgeName')

    def enterRetrieveAvatar(self):
        if self.accountID:
            self.set_account_id = self.accountID
        if self.avId and self.avId not in self.avList:
            self.demand('Kill', 'Tried to name an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        if fields['setWishNameState'][0] != 'OPEN':
            self.demand('Kill', 'Avatar is not in a namable state!')
            return

        self.demand('JudgeName')

    def enterJudgeName(self):
        # Let's see if the name is valid:
        status = judgeName(self.name)

        if self.avId and status:
            if self.csm.accountDB.addNameRequest(self.avId, self.name, accountID=self.set_account_id):
                self.csm.air.dbInterface.updateObject(
                    self.csm.air.dbId,
                    self.avId,
                    self.csm.air.dclassesByName['DistributedToonUD'],
                    {'setWishNameState': ('PENDING',),
                     'setWishName': (self.name,)})
            else:
                status = False

        if self.avId:
            self.csm.air.writeServerEvent('avatarWishname', self.avId, self.name)

        self.csm.sendUpdateToAccountId(self.target, 'setNameTypedResp', [self.avId, status])
        self.demand('Off')

class SetNamePatternFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('SetNamePatternFSM')
    POST_ACCOUNT_STATE = 'RetrieveAvatar'

    def enterStart(self, avId, pattern):
        self.avId = avId
        self.pattern = pattern

        self.demand('RetrieveAccount')

    def enterRetrieveAvatar(self):
        if self.avId and self.avId not in self.avList:
            self.demand('Kill', 'Tried to name an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        if fields['setWishNameState'][0] != 'OPEN':
            self.demand('Kill', 'Avatar is not in a namable state!')
            return

        self.demand('SetName')

    def enterSetName(self):
        # Render the pattern into a string:
        parts = []
        for p, f in self.pattern:
            part = self.csm.nameGenerator.nameDictionary.get(p, ('', ''))[1]
            if f:
                part = part[:1].upper() + part[1:]
            else:
                part = part.lower()
            parts.append(part)

        parts[2] += parts.pop(3) # Merge 2&3 (the last name) as there should be no space.
        while '' in parts:
            parts.remove('')
        name = ' '.join(parts)

        if name == '':
            name = 'Toon'

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.avId,
            self.csm.air.dclassesByName['DistributedToonUD'],
            {'setWishNameState': ('',),
             'setWishName': ('',),
             'setName': (name,)})

        self.csm.air.writeServerEvent('avatarNamed', self.avId, name)
        self.csm.sendUpdateToAccountId(self.target, 'setNamePatternResp', [self.avId, 1])
        self.demand('Off')

class AcknowledgeNameFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('AcknowledgeNameFSM')
    POST_ACCOUNT_STATE = 'GetTargetAvatar'

    def enterStart(self, avId):
        self.avId = avId
        self.demand('RetrieveAccount')

    def enterGetTargetAvatar(self):
        # Make sure the target avatar is part of the account:
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to acknowledge name on an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        # Process the WishNameState change.
        wishNameState = fields['setWishNameState'][0]
        wishName = fields['setWishName'][0]
        name = fields['setName'][0]

        if wishNameState == 'APPROVED':
            wishNameState = ''
            name = wishName
            wishName = ''
            self.csm.accountDB.removeNameRequest(self.avId)
        elif wishNameState == 'REJECTED':
            wishNameState = 'OPEN'
            wishName = ''
            self.csm.accountDB.removeNameRequest(self.avId)
        else:
            self.demand('Kill', "Tried to acknowledge name on an avatar in %s state!" % wishNameState)
            return

        # Push the change back through:
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.avId,
            self.csm.air.dclassesByName['DistributedToonUD'],
            {'setWishNameState': (wishNameState,),
             'setWishName': (wishName,),
             'setName': (name,)},
            {'setWishNameState': fields['setWishNameState'],
             'setWishName': fields['setWishName'],
             'setName': fields['setName']})

        self.csm.sendUpdateToAccountId(self.target, 'acknowledgeAvatarNameResp', [])
        self.demand('Off')

class LoadAvatarFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('LoadAvatarFSM')
    POST_ACCOUNT_STATE = 'GetTargetAvatar'

    def enterStart(self, avId):
        self.avId = avId
        self.demand('RetrieveAccount')

    def enterGetTargetAvatar(self):
        # Make sure the target avatar is part of the account:
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to play an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        self.avatar = fields
        self.demand('SetAvatar')

    def enterSetAvatarTask(self, channel, task):
        # Finally, grant ownership and shut down.
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.avId,
            self.csm.air.ourChannel,
            STATESERVER_OBJECT_SET_OWNER)
        datagram.addChannel(self.target<<32 | self.avId)
        self.csm.air.send(datagram)

        # Tell the GlobalPartyManager as well:
        self.csm.air.globalPartyMgr.avatarJoined(self.avId)
        
        fields = self.avatar
        fields.update({'setAdminAccess': [self.account.get('ACCESS_LEVEL', 0)]})
        self.csm.air.friendsManager.addToonData(self.avId, fields)        

        self.csm.air.writeServerEvent('avatarChosen', self.avId, self.target)
        self.demand('Off')
        return task.done

    def enterSetAvatar(self):
        channel = self.csm.GetAccountConnectionChannel(self.target)

        # First, give them a POSTREMOVE to unload the avatar, just in case they
        # disconnect while we're working.
        datagramCleanup = PyDatagram()
        datagramCleanup.addServerHeader(
            self.avId,
            channel,
            STATESERVER_OBJECT_DELETE_RAM)
        datagramCleanup.addUint32(self.avId)
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_ADD_POST_REMOVE)
        datagram.addString(datagramCleanup.getMessage())
        self.csm.air.send(datagram)

        # Activate the avatar on the DBSS:
        self.csm.air.sendActivate(
            self.avId, 0, 0, self.csm.air.dclassesByName['DistributedToonUD'],
            {'setAdminAccess': [self.account.get('ACCESS_LEVEL', 0)]})

        # Next, add them to the avatar channel:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_OPEN_CHANNEL)
        datagram.addChannel(self.csm.GetPuppetConnectionChannel(self.avId))
        self.csm.air.send(datagram)

        # Now set their sender channel to represent their account affiliation:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_SET_CLIENT_ID)
        datagram.addChannel(self.target<<32 | self.avId)
        self.csm.air.send(datagram)

        # Eliminate race conditions.
        taskMgr.doMethodLater(0.2, self.enterSetAvatarTask,
                              'avatarTask-%s' % self.avId, extraArgs=[channel],
                              appendTask=True)                         

class UnloadAvatarFSM(OperationFSM):
    notify = directNotify.newCategory('UnloadAvatarFSM')

    def enterStart(self, avId):
        self.avId = avId

        # We don't even need to query the account, we know the avatar is being played!
        self.demand('UnloadAvatar')

    def enterUnloadAvatar(self):
        channel = self.csm.GetAccountConnectionChannel(self.target)

        # Tell TTSFriendsManager somebody is logging off:
        self.csm.air.friendsManager.toonOffline(self.avId)

        # Clear off POSTREMOVE:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_CLEAR_POST_REMOVES)
        self.csm.air.send(datagram)

        # Remove avatar channel:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_CLOSE_CHANNEL)
        datagram.addChannel(self.csm.GetPuppetConnectionChannel(self.avId))
        self.csm.air.send(datagram)

        # Reset sender channel:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_SET_CLIENT_ID)
        datagram.addChannel(self.target<<32)
        self.csm.air.send(datagram)

        # Unload avatar object:
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.avId,
            channel,
            STATESERVER_OBJECT_DELETE_RAM)
        datagram.addUint32(self.avId)
        self.csm.air.send(datagram)

        # Done!
        self.csm.air.writeServerEvent('avatarUnload', self.avId)
        self.demand('Off')

# --- CLIENT SERVICES MANAGER UBERDOG ---
class ClientServicesManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('ClientServicesManagerUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        # These keep track of the connection/account IDs currently undergoing an
        # operation on the CSM. This is to prevent (hacked) clients from firing up more
        # than one operation at a time, which could potentially lead to exploitation
        # of race conditions.
        self.connection2fsm = {}
        self.account2fsm = {}

        # For processing name patterns.
        self.nameGenerator = NameGenerator()

        # Temporary HMAC key:
        self.key = 'c603c5833021ce79f734943f6e662250fd4ecf7432bf85905f71707dc4a9370c6ae15a8716302ead43810e5fba3cf0876bbbfce658e2767b88d916f5d89fd31'

        # Instantiate our account DB interface:
        if accountDBType == 'developer':
            self.accountDB = DeveloperAccountDB(self)
        elif accountDBType == 'mongodb':
            self.accountDB = MongoAccountDB(self)
        elif accountDBType == 'mysqldb':
            self.accountDB = MySQLAccountDB(self)
        elif accountDBType == 'remote':
            self.accountDB = RemoteAccountDB(self)
        else:
            self.notify.error('Invalid accountdb-type: ' + accountDBType)

    def killConnection(self, connId, reason):
        datagram = PyDatagram()
        datagram.addServerHeader(
            connId,
            self.air.ourChannel,
            CLIENTAGENT_EJECT)
        datagram.addUint16(101)
        datagram.addString(reason)
        self.air.send(datagram)

    def killConnectionFSM(self, connId):
        fsm = self.connection2fsm.get(connId)

        if not fsm:
            self.notify.warning('Tried to kill connection %d for duplicate FSM, but none exists!' % connId)
            return

        self.killConnection(connId, 'An operation is already underway: ' + fsm.name)

    def killAccount(self, accountId, reason):
        self.killConnection(self.GetAccountConnectionChannel(accountId), reason)

    def killAccountFSM(self, accountId):
        fsm = self.account2fsm.get(accountId)
        if not fsm:

            self.notify.warning('Tried to kill account %d for duplicate FSM, but none exists!' % accountId)
            return

        self.killAccount(accountId, 'An operation is already underway: ' + fsm.name)

    def runAccountFSM(self, fsmtype, *args):
        sender = self.air.getAccountIdFromSender()

        if not sender:
            self.killAccount(sender, 'Client is not logged in.')

        if sender in self.account2fsm:
            self.killAccountFSM(sender)
            return

        self.account2fsm[sender] = fsmtype(self, sender)
        self.account2fsm[sender].request('Start', *args)

    def login(self, cookie, authKey):
        self.notify.debug('Received login cookie %r from %d' % (cookie, self.air.getMsgSender()))

        sender = self.air.getMsgSender()

        # Time to check this login to see if its authentic
        digest_maker = hmac.new(self.key)
        digest_maker.update(cookie)
        serverKey = digest_maker.hexdigest()
        if serverKey == authKey:
            # This login is authentic!
            pass
        else:
            # This login is not authentic.
            self.killConnection(sender, ' ')

        if sender >> 32:
            self.killConnection(sender, 'Client is already logged in.')
            return

        if sender in self.connection2fsm:
            self.killConnectionFSM(sender)
            return

        self.connection2fsm[sender] = LoginAccountFSM(self, sender)
        self.connection2fsm[sender].request('Start', cookie)

    def requestAvatars(self):
        self.notify.debug('Received avatar list request from %d' % (self.air.getMsgSender()))
        self.runAccountFSM(GetAvatarsFSM)

    def createAvatar(self, dna, thirdTrack, index):
        self.runAccountFSM(CreateAvatarFSM, dna, thirdTrack, index)

    def deleteAvatar(self, avId):
        self.runAccountFSM(DeleteAvatarFSM, avId)

    def setNameTyped(self, avId, name):
        self.runAccountFSM(SetNameTypedFSM, avId, name)

    def setNamePattern(self, avId, p1, f1, p2, f2, p3, f3, p4, f4):
        self.runAccountFSM(SetNamePatternFSM, avId, [(p1, f1), (p2, f2),
                                                     (p3, f3), (p4, f4)])

    def acknowledgeAvatarName(self, avId):
        self.runAccountFSM(AcknowledgeNameFSM, avId)

    def chooseAvatar(self, avId):
        currentAvId = self.air.getAvatarIdFromSender()
        accountId = self.air.getAccountIdFromSender()
        if currentAvId and avId:
            self.killAccount(accountId, 'A Toon is already chosen!')
            return
        elif not currentAvId and not avId:
            # This isn't really an error, the client is probably just making sure
            # none of its Toons are active.
            return

        if avId:
            self.runAccountFSM(LoadAvatarFSM, avId)
        else:
            self.runAccountFSM(UnloadAvatarFSM, currentAvId)

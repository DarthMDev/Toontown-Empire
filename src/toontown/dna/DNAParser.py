from direct.stdpy import threading

from libpandadna import *

class DNABulkLoader:
    def __init__(self, storage, files):
        self.dnaStorage = storage
        self.dnaFiles = files

    def loadDNAFiles(self):
        for file in self.dnaFiles:
            print 'Reading DNA file...', file
            loadDNABulk(self.dnaStorage, file)
        del self.dnaStorage
        del self.dnaFiles

def loadDNABulk(dnaStorage, file):
    dnaLoader = DNALoader()
    if __debug__:
        file = 'resources/' + file
    else:
        file = '/' + file
    dnaLoader.loadDNAFile(dnaStorage, file)

def loadDNAFile(dnaStorage, file):
    print 'Reading DNA file...', file
    dnaLoader = DNALoader()
    if __debug__:
        file = 'resources/' + file
    else:
        file = '/' + file
    node = dnaLoader.loadDNAFile(dnaStorage, file)
    if node.node().getNumChildren() > 0:
        return node.node()

def loadDNAFileAI(dnaStorage, file):
    dnaLoader = DNALoader()
    if __debug__:
        file = 'resources/' + file
    else:
        file = '/' + file
    data = dnaLoader.loadDNAFileAI(dnaStorage, file)
    return data

def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
    try:
        block = int(str(block).split('_')[0])
    except:
        print 'setupDoor: error parsing', block
        block = 9999

    DNADoor.setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color)

from direct.stdpy import threading

import DNALoader
from DNAStorage import DNAStorage
from DNASuitPoint import DNASuitPoint
from DNAGroup import DNAGroup
from DNAVisGroup import DNAVisGroup
from DNADoor import DNADoor
import sys
if sys.platform == 'darwin' or sys.platform == 'linux2':
	from toontown.libpandadna import *
else:
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
    file = '/' + file
    dnaLoader.loadDNAFile(dnaStorage, file)

def loadDNAFile(dnaStorage, file):
    print 'Reading DNA file...', file
    dnaLoader = DNALoader()
    file = '/' + file
    node = dnaLoader.loadDNAFile(dnaStorage, file)
    if node.node().getNumChildren() > 0:
        return node.node()

def loadDNAFileAI(dnaStorage, file):
    dnaLoader = DNALoader()
    file = '/' + file
    data = dnaLoader.loadDNAFileAI(dnaStorage, file)
    return data

def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
    DNADoor.setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color)

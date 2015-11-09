from direct.stdpy import threading
from toontown.libpandadna import *
from toontown.libpandadna.DNAAnimBuilding import *
from toontown.libpandadna.DNAAnimProp import *
from toontown.libpandadna.DNACornice import *
from toontown.libpandadna.DNADoor import *
from toontown.libpandadna.DNAFlatBuilding import *
from toontown.libpandadna.DNAFlatDoor import *
from toontown.libpandadna.DNAGroup import *
from toontown.libpandadna.DNAInteractiveProp import *
from toontown.libpandadna.DNALandmarkBuilding import *
from toontown.libpandadna.DNANode import *
from toontown.libpandadna.DNAProp import *
from toontown.libpandadna.DNASign import *
from toontown.libpandadna.DNASignBaseline import *
from toontown.libpandadna.DNASignGraphic import *
from toontown.libpandadna.DNASignText import *
from toontown.libpandadna.DNAStreet import *
from toontown.libpandadna.DNAWall import *
from toontown.libpandadna.DNAWindows import *
from toontown.libpandadna.DNAStorage import *
from toontown.libpandadna.DNALoader import *
from toontown.libpandadna.DNASuitEdge import *
from toontown.libpandadna.DNASuitPoint import *
from toontown.libpandadna.DNASuitPath import * 
from toontown.libpandadna.DNABattleCell import *

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
    fileu = '../resources/' + file
    dnaLoader.loadDNAFile(dnaStorage, fileu)

def loadDNAFile(dnaStorage, file):
    print 'Reading DNA file...', file
    dnaLoader = DNALoader()
    fileu = '../resources/' + file
    node = dnaLoader.loadDNAFile(dnaStorage, fileu)
    if node.node().getNumChildren() > 0:
        return node.node()

def loadDNAFileAI(dnaStorage, file):
    dnaLoader = DNALoader()
    fileu = '../resources/' + file
    data = dnaLoader.loadDNAFileAI(dnaStorage, fileu)
    return data

def setupDoor(a, b, c, d, e, f):
    try:
        e = int(str(e).split('_')[0])
    except:
        print 'setupDoor: error parsing', e
        e = 9999

    DNADoor.setupDoor(a, b, c, d, e, f)

from panda3d.core import *
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram
from direct.stdpy.file import *

import DNAStorage
import DNANode
import DNAParser
import DNALoader
import DNAGroup
import DNAVisGroup

class DNAData(DNAGroup):
    def __init__(self, name):
        DNAGroup.__init__(self, name)
        self.coordSystem = 0
        self.dnaFilename = ''
        self.dnaStorage = None

    def getCoordSystem(self):
        return self.coordSystem

    def getDnaFilename(self):
        return self.dnaFilename

    def getDnaStorage(self):
        if self.dnaStorage is None:
            self.dnaStorage = DNAStorage()
        return self.dnaStorage

    def setCoordSystem(self, system):
        self.coordSystem = system

    def setDnaFilename(self, filename):
        self.dnaFilename = filename

    def setDnaStorage(self, storage):
        self.dnaStorage = storage

    def read(self, stream):
        parser = yacc.yacc(debug=0, optimize=0)
        parser.dnaData = self
        parser.parentGroup = parser.dnaData
        parser.dnaStore = self.getDnaStorage()
        parser.nodePath = None
        parser.parse(stream.read())

from pandac.PandaModules import Vec3, Vec4, Point3, TextNode, VBase4
from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel, DirectScrolledList, DirectCheckButton
from direct.gui import DirectGuiGlobals
from direct.showbase.DirectObject import DirectObject
from direct.showbase import PythonUtil
from src.toontown.toonbase import ToontownGlobals
from src.toontown.toonbase import TTLocalizer
from src.toontown.parties import PartyGlobals
from src.toontown.parties.PartyInfo import PartyInfo
from src.toontown.parties import PartyUtils

class PartyEditorGridSquare(DirectObject):
    notify = directNotify.newCategory('PartyEditorGridSquare')

    def __init__(self, partyEditor, x, y):
        self.partyEditor = partyEditor
        self.x = x
        self.y = y
        self.gridElement = None
        return

    def getPos(self):
        return Point3(PartyGlobals.PartyEditorGridBounds[0][0] + self.x * PartyGlobals.PartyEditorGridSquareSize[0] + PartyGlobals.PartyEditorGridSquareSize[0] / 2.0, 0.0, PartyGlobals.PartyEditorGridBounds[1][1] + (PartyGlobals.PartyEditorGridSize[1] - 1 - self.y) * PartyGlobals.PartyEditorGridSquareSize[1] + PartyGlobals.PartyEditorGridSquareSize[1] / 2.0)

    def destroy(self):
        del self.gridElement

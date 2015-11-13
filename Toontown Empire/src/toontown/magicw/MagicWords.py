#This is for testing purposes. May not work or be present in final version.
import src.toontown
import src.otp
import direct
import random
import math
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.gui import DirectGuiGlobals
from src.toontown.toonbase import TTLocalizer
from src.toontown.toonbase import ToontownGlobals
from src.toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase import PythonUtil
from direct.showbase.PythonUtil import *
from direct.task import Task
from src.toontown.toon import ToonDNA
#from src.toontown.toon import LocalToon
from src.otp.ai.MagicWordGlobal import *

#Codes Below is for Testing
@magicWord(category=CATEGORY_MODERATOR)
def magicHead():
 from src.toontown.toon import LaughingManGlobals
 invoker = spellbook.getTarget()
 LaughingManGlobals.addToonEffect(invoker)
 
@magicWord(category=CATEGORY_MODERATOR)
def noName():
    #from src.otp.avatar import LocalAvatar
    invoker = spellbook.getTarget()
    invoker.setNameVisible(False)
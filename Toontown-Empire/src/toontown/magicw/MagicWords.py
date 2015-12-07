#This is for testing purposes. May not work or be present in final version.
import toontown
import otp
import direct
import random
import math
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.gui import DirectGuiGlobals
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase import PythonUtil
from direct.showbase.PythonUtil import *
from direct.task import Task
from toontown.toon import ToonDNA
#from toontown.toon import LocalToon
from otp.ai.MagicWordGlobal import *

#Codes Below is for Testing
@magicWord(category=CATEGORY_MODERATOR)
def magicHead():
 from toontown.toon import LaughingManGlobals
 invoker = spellbook.getTarget()
 LaughingManGlobals.addToonEffect(invoker)
 
@magicWord(category=CATEGORY_MODERATOR)
def noName():
    #from otp.avatar import LocalAvatar
    invoker = spellbook.getTarget()
    invoker.setNameVisible(False)
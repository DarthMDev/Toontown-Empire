# TODO: Fix Error with the updater not loading the path files!! ~Dan
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from panda3d.core import *
import os, sys, math, random, time, __builtin__
from direct.task import Task
from direct.fsm import FSM
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
data = []
WaitTime = 1



def OpenFileQA():
 with open('dependencies/config/release/qa.prc', "a+") as newfile:
	newfile.writelines(data)		
	print(ver)
        
def OpenFileDevQA():
 with open('dependencies/config/release/dev.prc', "a+") as newfile:
	newfile.writelines(data)		
	print(ver)
        
def RemoveQAFile():
 os.remove('dependencies/config/release/qa.prc')

def RemoveDevQAFile():
 os.remove('dependencies/config/release/dev.prc')
  
def ResetData():
 data = None
 
def NewData():
 data = []

def ReleaseQA():
 with open('dependencies/config/release/qa.prc', 'r+') as config:
	data = config.readlines()
	line = data[7].split()
	x = line[1]
	y = x.split("-")
	ver = y[2]
	ver = ver.split(".")
	if str(ver[2]) == "9":
		ver[1] = int(ver[1]) + 1
		ver[2] = 0
	if str(ver[1]) == "9":
		ver[0] = int(ver[0]) + 1
		ver[1] = 0
	else:
		ver[2] = int(ver[2]) + 1
		data[7] = "server-version TTE-Alpha-"+ str(ver[0]) + "." + str(ver[1]) + "." + str(ver[2]) + "\n"
		
def DevQA():
 with open('dependencies/config/release/dev.prc', 'r+') as config:
	data = config.readlines()
	line = data[21].split()
	x = line[1]
	y = x.split("-")
	ver = y[2]
	ver = ver.split(".")
	if str(ver[2]) == "9":
		ver[1] = int(ver[1]) + 1
		ver[2] = 0
	if str(ver[1]) == "9":
		ver[0] = int(ver[0]) + 1
		ver[1] = 0
	else:
		ver[2] = int(ver[2]) + 1
		data[21] = "server-version TTE-Alpha-"+ str(ver[0]) + "." + str(ver[1]) + "." + str(ver[2]) + "\n"
                
                
class Update(ShowBase):
 def __init__(self):
  ShowBase.__init__(self)
  os.chdir('../../../')
  seq = Sequence()
  seq.append(Func(ReleaseQA))
  seq.append(Wait(WaitTime))
  seq.append(Func(RemoveQAFile))
  seq.append(Wait(WaitTime))
  seq.append(Func(OpenFileQA))
  seq.append(Wait(WaitTime))
  seq.append(Func(ResetData))
  seq.append(Wait(WaitTime))
  seq.append(Func(NewData))
  seq.append(Wait(WaitTime))
  seq.append(Func(DevQA))
  seq.append(Wait(WaitTime))
  seq.append(Func(RemoveDevQAFile))
  seq.append(Wait(WaitTime))
  seq.append(Func(OpenFileDevQA))
  seq.append(Wait(WaitTime))
  seq.start()

start = Update()
start.run()
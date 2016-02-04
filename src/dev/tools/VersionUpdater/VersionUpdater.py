# TODO: Add correct paths + add astron cluster files! ~FordTheWriter
import os, sys, math, random
from direct.interval.IntervalGlobal import *
os.chdir('../../../')
data = []


class VersionUpdater(self):

 def OpenFileQA(self):
  with open('dependencies/config/release/qa.prc', "a+") as newfile:
	newfile.writelines(data)		
	print(ver)
        
 def OpenFileDevQA(self):
  with open('dependencies/config/release/dev.prc', "a+") as newfile:
	newfile.writelines(data)		
	print(ver)
        
 def RemoveQAFile(self):
  os.remove('dependencies/config/release/qa.prc')

 def RemoveDevQAFile(self):
  os.remove('dependencies/config/release/dev.prc')
  
 def ResetData(self):
  data = None
 
 def NewData(self):
  data = []

 def ReleaseQA(self):
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
		
 
 def DevQA(self):
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
		data[7] = "server-version TTE-Alpha-"+ str(ver[0]) + "." + str(ver[1]) + "." + str(ver[2]) + "\n"


   
def update():
 seq = Sequence()
 seq.append(Func(VersionUpdater.ReleaseQA))
 seq.append(Wait(0.1))
 seq.append(Func(VersionUpdater.RemoveQAFile)
 seq.append(Wait(0.1))
 seq.append(Func(VersionUpdater.OpenFileQA)
 seq.append(Wait(0.1))
 seq.append(Func(VersionUpdater.ResetData)
 seq.append(Wait(0.1))
 seq.append(Func(VersionUpdater.NewData)
 seq.append(Wait(0.1))
 seq.append(Func(VersionUpdater.DevQA))
 seq.start()
update()
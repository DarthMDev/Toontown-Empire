import subprocess
import os 
import sys

#TODO move the enviornment variables into the launcher and remove the raw_inputs
username = raw_input("> ")
password = raw_input("> ") 

os.environ["TTE_GAMESERVER"] = "server.toontownempire.com"
os.environ["tteUsername"] = username
os.environ["ttePassword"] = password
import GameData
if sys.platform == 'win32':
	subprocess.call(['dependencies\panda\python\ppython.exe', '-m', 'toontown.toonbase.ToontownStartDist'])
elif sys.platform == 'darwin':
	subprocess.call(['ppython', '-m', 'toontown.toonbase.ToontownStartDist'])
else:
	subprocess.call(['python2', '-m', 'toontown.toonbase.ToontownStartDist'])


import subprocess, os, sys

username = raw_input("> ")
password = raw_input("> ") 

os.environ["TTE_GAMESERVER"] = "server.toontownempire.com"
os.environ["tteUsername"] = username
os.environ["ttePassword"] = password

subprocess.call(['dependencies\panda\python\ppython.exe', '-m', 'toontown.toonbase.ToontownStart'])

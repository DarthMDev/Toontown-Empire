import subprocess, os, sys, runpy

username = raw_input("> ")
password = raw_input("> ") 

os.environ["TTE_GAMESERVER"] = "server.toontownempire.com"
os.environ["tteUsername"] = username
os.environ["ttePassword"] = password

runpy.run_module('toontown.toonbase.ToontownStart', run_name='__main__', alter_sys=True)

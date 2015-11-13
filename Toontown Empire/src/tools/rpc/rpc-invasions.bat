@echo off
cd ../../../
set /P serv=RPC Server:
"src/src/dependencies/panda/python/ppython.exe" "src/tools/rpc/rpc-invasions.py" 6163636f756e7473 %serv%
pause
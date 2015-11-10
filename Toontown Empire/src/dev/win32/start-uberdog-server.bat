@echo off

title TTE Uberdog
rem Define some constants for our UberDOG server:
set MAX_CHANNELS=999999
set STATESERVER=4002
set ASTRON_IP=127.0.0.1:7100
set EVENTLOGGER_IP=127.0.0.1:7198
set BASE_CHANNEL=1000000

echo ===============================
echo Starting Toontown Empire UberDOG server...
echo ppython: "src/dependencies/panda/python/ppython.exe"
echo Base channel: %BASE_CHANNEL%
echo Max channels: %MAX_CHANNELS%
echo State Server: %STATESERVER%
echo Astron IP: %ASTRON_IP%
echo Event Logger IP: %EVENTLOGGER_IP%
echo ===============================

cd ../../../


:main
"src/dependencies/panda/python/ppython.exe" ^
	-m src.toontown.uberdog.ServiceStart ^
	--base-channel %BASE_CHANNEL% ^
	--max-channels %MAX_CHANNELS% ^
	--stateserver %STATESERVER% ^
	--astron-ip %ASTRON_IP% ^
	--eventlogger-ip %EVENTLOGGER_IP%
goto main


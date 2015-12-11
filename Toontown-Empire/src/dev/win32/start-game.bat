@echo off

title TTE Alpha Lancher

echo Choose your connection method!
echo.
echo #1 - Localhost
echo #2 - Toontown Empire Dev Server
echo #3 - Custom
echo #4 - Local RemoteDB
echo #5 - Production Server
echo.

:selection

set INPUT=-1
set /P INPUT=Selection: 

if %INPUT%==1 (
    set TTE_GAMESERVER=127.0.0.1
) else if %INPUT%==2 (
    set TTE_GAMESERVER=45.55.208.151
)
else if %INPUT == 5 (
    set TTE_GAMESERVER = gameserver.toontownempire.com
    )
 else if %INPUT%==4 (
    set TTE_GAMESERVER=127.0.0.1
) else if %INPUT%==3 (
    echo.
    set /P TTE_GAMESERVER=Gameserver: 
) else (
	goto selection
)

echo.

if %INPUT%==2 (
    set /P tteUsername="Username: "
    set /P ttePassword="Password: "
) else if %INPUT%==4 (
    set /P tteUsername="Username: "
    set /P ttePassword="Password: "
) else (
    set /P TTE_PLAYCOOKIE=Username: 
)

echo.

echo ===============================
echo Starting Toontown Empire...
echo ppython: "dependencies/panda/python/ppython.exe"

if %INPUT%==2 (
    echo Username: %tteUsername%
) else if %INPUT%==4 (
    echo Username: %tteUsername%
) else (
    echo Username: %TTE_PLAYCOOKIE%
)

echo Gameserver: %TTE_GAMESERVER%
echo ===============================

cd ../../

if %INPUT%==2 (
    "dependencies/panda/python/ppython.exe" -m toontown.toonbase.ToontownStartRemoteDB
) else if %INPUT%==4 (
    "dependencies/panda/python/ppython.exe" -m toontown.toonbase.ToontownStartRemoteDB
) else (
    "dependencies/panda/python/ppython.exe" -m toontown.toonbase.ToontownStart
)

pause

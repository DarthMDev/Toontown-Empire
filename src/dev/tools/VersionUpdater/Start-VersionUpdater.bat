@echo off

cd ../../../
title Version Updater

:selection
echo Choose your Version Updater!
echo.
echo #1 - Dan's Version Updater [Broken]
echo #2 - Ford's Version Updater
echo.

set INPUT=-1
set /P INPUT=Selection: 

if %INPUT%==1 (
    echo You chose Dan's Version Updater!
) else if %INPUT%==2 (
    echo You chose Ford's Version Updater!
) else (
	goto selection
)

:start
echo --------------------------------------------
echo Starting Version Updater...
echo ppython: "dependencies/panda/python/ppython.exe"
echo --------------------------------------------

if %INPUT%==1 (
    "dependencies/panda/python/ppython.exe" -m dev.tools.VersionUpdater.DansVersionUpdater
) else if %INPUT%==2 (
    "dependencies/panda/python/ppython.exe" -m dev.tools.VersionUpdater.FordsVersionUpdater
) else (
    ""dependencies/panda/python/ppython.exe" -m dev.tools.VersionUpdater.FordsVersionUpdater
)

pause
goto start
@echo off

cd ../../../
title Version Updater

echo Starting Version Updater...
echo ppython: "dependencies/panda/python/ppython.exe"

:start
echo --------------------------------------------
"dependencies/panda/python/ppython.exe" -m dev.tools.VersionUpdater.DansVersionUpdater

pause
goto start
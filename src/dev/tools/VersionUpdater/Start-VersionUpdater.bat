@echo off

title Version Updater

echo Starting Version Updater...
echo ppython: "dependencies/panda/python/ppython.exe"

:start


cd ../../../
"dependencies/panda/python/ppython.exe" -m dev.tools.VersionUpdater.VersionUpdater

pause
goto start
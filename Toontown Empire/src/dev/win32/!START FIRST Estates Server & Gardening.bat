@echo off
title TTE MongoDB

cd ../../

:main
"src/dependencies/MongoDB\Server\3.0\bin\mongod.exe" --dbpath dependencies/MongoDB/GardeningDatabase


pause

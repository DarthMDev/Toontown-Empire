@echo off
title TTE MongoDB

cd ../../dependencies/MongoDB/Server/3.0/mongodb

:main
"C:\Program Files\MongoDB\Server\3.4\bin\mongod.exe" --dbpath .\


pause
goto main

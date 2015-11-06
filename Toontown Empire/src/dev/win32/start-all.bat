@echo off
start "!START FIRST Estates Server & Gardening.bat"
start start-astron-cluster.bat
TIMEOUT 1
start start-uberdog-server.bat
TIMEOUT 7
start start-ai-server.bat
start start-game.bat

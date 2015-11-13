@echo off
cd "../../dependencies/astron/"

title TTE Astron
astrond --loglevel info config/cluster.yml
pause

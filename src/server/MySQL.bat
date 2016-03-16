@echo off
ECHO ------------------------------------------------------------------------------------------
ECHO ******************************************************************************************
ECHO Toontown
ECHO Empire
ECHO SQL
ECHO Server   		BY Malverde
ECHO ******************************************************************************************
echo ------------------------------------------------------------------------------------------
echo Please dont close Window while MySQL is running
echo MySQL is trying to start
echo Please wait  ...
echo MySQL is starting with mysql\bin\my.cnf (console)

mysql\bin\mysqld --defaults-file=mysql\bin\my.cnf --standalone --console

if errorlevel 1 goto error
goto finish

:error
echo.
echo MySQL could not be started
pause

:finish

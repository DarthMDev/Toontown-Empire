#!/bin/sh
cd ..
export PYTHONPATH=dependencies/linux:$PYTHONPATH
# Get the user input:
read -p "Username: " tteUsername
read -p "Gameserver (DEFAULT:  127.0.0.1): " TTE_GAMESERVER
TTI_GAMESERVER=${TTE_GAMESERVER:-"167.114.28.238"}

# Export the environment variables:
export tteUsername=$tteUsername
export ttePassword="password"
export TTE_PLAYCOOKIE=$tteUsername
export TTE_GAMESERVER=$TTE_GAMESERVER

echo "==============================="
echo "Starting Toontown Empire"
echo "Username: $tteUsername"
echo "Gameserver: $TTE_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ClientStart

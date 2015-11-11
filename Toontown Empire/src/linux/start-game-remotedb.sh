#!/bin/bash
cd ..

# Get the user input:
read -p "Username: " tteUsername
read -s -p "Password: " ttePassword
echo
read -p "Gameserver (DEFAULT: 127.0.0.1): " TTE_GAMESERVER
TTE_GAMESERVER=${TTE_GAMESERVER:-"127.0.0.2"}

# Export the environment variables:
export ttiUsername=$tteUsername
export ttiPassword=$ttePassword
export TTE_PLAYCOOKIE=$tteUsername
export TTE_GAMESERVER=$TTE_GAMESERVER

echo "==============================="
echo "Starting Toontown Empire"
echo "Username: $tteUsername"
echo "Gameserver: $TTE_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ClientStartRemoteDB

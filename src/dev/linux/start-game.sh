#!/bin/sh
cd ../../../

# Get the user input:
read -p "Username: " tteUsername
read -p "Gameserver (DEFAULT:  104.131.65.72): " TTE_GAMESERVER
TTI_GAMESERVER=${TTE_GAMESERVER:-"104.131.65.72"}

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

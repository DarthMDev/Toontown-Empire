#!/bin/sh
cd ..
cd ..
# Get the user input:
read -p "Username: " tteUsername

# Export the environment variables:
export tteUsername=$tteUsername
export ttePassword="password"
export TTE_PLAYCOOKIE=$tteUsername
export TTE_GAMESERVER="127.0.0.1"

echo "==============================="
echo "Starting Toontown Empire"
echo "Username: $tteUsername"
echo "Gameserver: $TTE_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ClientStart

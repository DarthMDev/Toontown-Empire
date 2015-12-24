#!/bin/sh
cd ../..

export DYLD_LIBRARY_PATH=`pwd`/Libraries.bundle
export DYLD_FRAMEWORK_PATH="Frameworks"

# Get the user input:
read -p "Username: " tteUsername
read -p "Gameserver (DEFAULT:  167.114.28.238): " TTE_GAMESERVER
TTE_GAMESERVER=${TTE_GAMESERVER:-"167.114.28.238"}

# Export the environment variables:
export tteUsername=$tteUsername
export ttePassword="password"
export TTE_PLAYCOOKIE=$tteUsername
export TTE_GAMESERVER=$TTE_GAMESERVER

echo "==============================="
echo "Starting Toontown Empire..."
echo "Username: $tteUsername"
echo "Gameserver: $TTE_GAMESERVER"
echo "==============================="

ppython -m toontown.toonbase.ToontownStart
#!/bin/sh
cd ../../../

export DYLD_LIBRARY_PATH=`pwd`/Libraries.bundle
export DYLD_FRAMEWORK_PATH="Frameworks"

# Get the user input:
read -p "Username: " tteUsername
read -p "Gameserver (DEFAULT:  167.114.28.238): " tte_GAMESERVER
tte_GAMESERVER=${tte_GAMESERVER:-"167.114.28.238"}

# Export the environment variables:
export tteUsername=$tteUsername
export ttePassword="password"
export tte_PLAYCOOKIE=$tteUsername
export tte_GAMESERVER=$tte_GAMESERVER

echo "==============================="
echo "Starting Toontown Empire..."
echo "Username: $tteUsername"
echo "Gameserver: $tte_GAMESERVER"
echo "==============================="

ppython -m src.toontown.toonbase.ToontownStart
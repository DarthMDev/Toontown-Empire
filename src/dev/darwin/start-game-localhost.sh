#!/bin/sh
cd ..
cd ..
export DYLD_LIBRARY_PATH=`pwd`/Libraries.bundle
export PYTHONPATH=/Developer/Panda3D/lib:$PYTHONPATH
export DYLD_FRAMEWORK_PATH="Frameworks"
export PYTHONPATH=dependencies/mac:$PYTHONPATH
# Get the user input:
read -p "Username: " tteUsername

# Export the environment variables:
export tteUsername=$tteUsername
export ttePassword="password"
export TTE_PLAYCOOKIE=$tteUsername
export TTE_GAMESERVER="127.0.0.1"

echo "==============================="
echo "Starting Toontown Empire..."
echo "Username: $tteUsername"
echo "Gameserver: $TTE_GAMESERVER"
echo "==============================="

ppython -m toontown.toonbase.ToontownStart

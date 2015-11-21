# Toontown Empire 

[![Build Status](https://magnum.travis-ci.com/mgracer48/toontown-empire.svg?token=nwGfbyDzkuRBAHQGp16L&branch=master)](https://magnum.travis-ci.com/mgracer48/toontown-empire)

[![Codacy Badge](https://api.codacy.com/project/badge/grade/a71bcbed1f8c4cd59d7f1fa131c7114d)](https://www.codacy.com)

[![Code Issues](https://www.quantifiedcode.com/api/v1/project/ace720abeb544fbcb8dc1c9aff3a6241/badge.svg)](https://www.quantifiedcode.com/app/project/ace720abeb544fbcb8dc1c9aff3a6241)

Official Repo for Toontown Empire, a new Toontown game based on Disney's Toontown Online.

# Staff Positions:

1. Dynamite- Leader and Game Developer
2. Dubito: Leader, Server Administrator and Launcher Developer
3. Josh Zimmer- Leader and Game Developer
4. Xikyl- Texture and Graphic Artist
5. MGRacer48- Game Developer
6. Craigy- Malv: Game Developer
7. Spike- Community Manager
8. Trevor- Composor 
9. EpicrockersMC- Moderator

# Repo:

We make dev changes to master but before we release if the master branch is stable merge it into the production branch. This is the branch used for hosting the game on the server and the branch used for deploying to the server with a stable game. 

Do not push broken code to the master branch, because it messes up the game and makes it harder for the developers to add features, and fix bugs in the game! When you revert something broken, please post the crash to make life easier for the coders.

# requirements:
In order to run game you need to install this
pip install -U airbrake pymongo bson raven
if on mac or linux:
sudo pip install -U rollbar pymongo bson  raven 

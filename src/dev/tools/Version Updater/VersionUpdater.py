import os
os.chdir('../../../')

from dependencies.astron.config import *
#TODO make version equal to end of TTE- try using indexes
if version is None:
    version = 1.0
ask = raw_input('Are you sure you want to change version number by .1? Type yes or no: '
ask = str(ask)
ask = ask.lower()
if ask == 'yes':
    version += 0.1
elif ask == 'no':
    exit()

import os
os.chdir('../../../')

#from dependencies.astron.config import * - this doesnt have any python files so removing import
#TODO make version equal to end of TTE- try using indexes we also need to get it from qa.prc. We also need to use write so it doesnt add new line more like overwrites version at end of tte prefix
if version is None:
    version = 1.0
ask = raw_input('Are you sure you want to change version number by .1? Type yes or no: ')
ask = str(ask)
ask = ask.lower()
if ask == 'yes':
    version += 0.1
    os.chdir('dependencies/config/release')
    with open('qa.prc', 'w') as config:
         config.write(version)
elif ask == 'no':
    exit()

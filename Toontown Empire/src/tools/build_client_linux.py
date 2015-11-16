import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--main-module', default='toontown.toonbase.ToontownStartRemoteDB',
                    help='The path to the main module.')
parser.add_argument('modules', nargs='*', default=['otp', 'toontown', 'pymongo', 'bson', 'dependencies', 'user'],
                    help='The Toontown Offline modules to be included in the build.')
args = parser.parse_args()

print 'Building the client...'

os.chdir('build')

cmd = ('/usr/bin/python2')
cmd += ' -m direct.showutil.pfreeze'
args.modules.extend(['direct', 'pandac', 'panda3d'])
for module in args.modules:
    cmd += ' -i {0}.*.*'.format(module)
cmd += ' -i {0}.*'.format('encodings')
cmd += ' -i {0}'.format('base64')
cmd += ' -i {0}'.format('site')
cmd += ' -o empire.so'
cmd += ' {0}'.format(args.main_module)

os.system(cmd)

print 'Done building the client.'

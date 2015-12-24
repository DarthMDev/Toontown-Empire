import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--panda3d-dir', default='/Developer/Panda3D',
                    help='The path to the Panda3D build to use for this distribution.')
parser.add_argument('--main-module', default='toontown.toonbase.ToontownStart',
                    help='The path to the main module.')
parser.add_argument('modules', nargs='*', default=['otp', 'toontown'],
                    help='The Toontown Offline modules to be included in the build.')
args = parser.parse_args()

print 'Building the client...'

os.chdir('build')

cmd = ('ppython')
cmd += ' -m direct.showutil.pfreeze'
args.modules.extend(['direct', 'pandac'])
for module in args.modules:
    cmd += ' -i {0}.*.*'.format(module)
cmd += ' -i {0}.*'.format('encodings')
cmd += ' -i {0}'.format('base64')
cmd += ' -i {0}'.format('site')
cmd += ' -o TTE.so'
cmd += ' {0}'.format(args.main_module)

os.system(cmd)

print 'Done building the client.'

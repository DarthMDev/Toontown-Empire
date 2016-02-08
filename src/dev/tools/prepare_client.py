from pandac.PandaModules import *
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--build-dir', default='build',
                    help='The directory in which to store the build files.')
parser.add_argument('--src-dir', default='..',
                    help='The directory of the Toontown Empire source code.')
parser.add_argument('modules', nargs='*', default=['otp', 'toontown'],
                    help='The Toontown Empire modules to be included in the build.')
args = parser.parse_args()

os.chdir('../../../')
print 'Preparing the client...'

# Create a clean build directory for us to store our build material:
if not os.path.exists(args.build_dir):
    os.mkdir(args.build_dir)
print 'Build directory = {0}'.format(args.build_dir)

# Set the build version.
buildVersion = ''
buildVer = raw_input('Build Version: TTE.')
if buildVer:
    buildVersion = buildVer
else:
    buildVersion = 'dev'
print 'buildVersion = {0}'.format(buildVersion)

# Copy the provided Toontown modules:

# All client and server files are included by default.
includes = ('')

# This is a list of explicitly excluded files.
excludes = ('')

def minify(f):
    """
    Returns the "minified" file data with removed __debug__ code blocks.
    """

    data = ''

    debugBlock = False  # Marks when we're in a __debug__ code block.
    elseBlock = False  # Marks when we're in an else code block.

    # The number of spaces in which the __debug__ condition is indented:
    indentLevel = 0

    for line in f:
        thisIndentLevel = len(line) - len(line.lstrip())
        if ('if __debug__:' not in line) and (not debugBlock):
            data += line
            continue
        elif 'if __debug__:' in line:
            debugBlock = True
            indentLevel = thisIndentLevel
            continue
        if thisIndentLevel <= indentLevel:
            if 'else' in line:
                elseBlock = True
                continue
            if 'elif' in line:
                line = line[:thisIndentLevel] + line[thisIndentLevel+2:]
            data += line
            debugBlock = False
            elseBlock = False
            indentLevel = 0
            continue
        if elseBlock:
            data += line[4:]

    return data

for module in args.modules:
    print 'Writing module...', module
    for root, folders, files in os.walk(os.path.join(args.src_dir, module)):
        outputDir = root.replace(args.src_dir, args.build_dir)
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        for filename in files:
            if filename in includes:
                if not filename.endswith('.py'):
                    continue
                if not filename.endswith('UD.py'):
                    continue
                if not filename.endswith('AI.py'):
                    continue
                if not filename in excludes:
                    continue
            with open(os.path.join(root, filename), 'r') as f:
                data = minify(f)
            with open(os.path.join(outputDir, filename), 'w') as f:
                f.write(data)

# Let's write _gamedata.py now. _gamedata is a compiled collection
# of data that will be used by the game at runtime. It contains
# the PRC file data and the stripped DC file for the client side.

# First, we need the PRC file data:
configFileName = 'public_client.prc'
configData = []
with open(os.path.join(args.src_dir, 'dependencies/config/release', configFileName)) as f:
    data = f.read()
    configData.append(data.replace('BUILD_VERSION', buildVersion))
print 'Using config file: {0}'.format(configFileName)

# Next, we need the (stripped) DC file:
dcFile = DCFile()
filepath = os.path.join(args.src_dir, 'dependencies/astron/dclass')
for filename in os.listdir(filepath):
    if filename.endswith('.dc'):
        dcFile.read(Filename.fromOsSpecific(os.path.join(filepath, filename)))
dcStream = StringStream()
dcFile.write(dcStream, True)
dcData = dcStream.getData()

# Finally, write our data to _gamedata.py:
print 'Writing _gamedata.py...'
gameData = '''\
CONFIG = %r
DC = %r'''
with open(os.path.join(args.build_dir, '_gamedata.py'), 'w') as f:
    f.write(gameData % (configData, dcData))

print 'Done preparing the client.'

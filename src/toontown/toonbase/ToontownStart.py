#!/usr/bin/env python2
import gc

gc.disable()

import __builtin__

__builtin__.process = 'client'

import sys, os
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../dependencies"
        )
    )
)

# Temporary hack patch:
__builtin__.__dict__.update(__import__('pandac.PandaModules', fromlist=['*']).__dict__)


from panda3d.core import loadPrcFile

if not os.path.exists('user/'):
    os.mkdir('user/')


	
	
if __debug__:
    import sys
    from direct.stdpy import threading

    loadPrcFile('dependencies/config/general.prc')
    loadPrcFile('dependencies/config/release/dev.prc')

    if os.path.isfile('dependencies/config/local.prc'):
        loadPrcFile('dependencies/config/local.prc')

from direct.directnotify.DirectNotifyGlobal import directNotify

notify = directNotify.newCategory('ToontownStart')
notify.setInfo(True)

if __debug__:
    # The VirtualFileSystem, which has already initialized, doesn't see the mount
    # directives in the config(s) yet. We have to force it to load those manually:
    from panda3d.core import VirtualFileSystem, ConfigVariableList, Filename
    vfs = VirtualFileSystem.getGlobalPtr()
    mounts = ConfigVariableList('vfs-mount')
    for mount in mounts:
        mountfile, mountpoint = (mount.split(' ', 2) + [None, None, None])[:2]
        vfs.mount(Filename(mountfile), Filename(mountpoint), 0)

from otp.settings.Settings import Settings
from otp.otpbase import OTPGlobals

preferencesFilename = ConfigVariableString(
    'preferences-filename',
    'user/preferences.json'
).getValue()

notify.info('Reading %s...' % preferencesFilename)

__builtin__.settings = Settings(preferencesFilename)
if 'res' not in settings:
    settings['res'] = (800, 600)
if 'fullscreen' not in settings:
    settings['fullscreen'] = False
if 'musicVol' not in settings:
    settings['musicVol'] = 1.0
if 'sfxVol' not in settings:
    settings['sfxVol'] = 1.0
if 'loadDisplay' not in settings:
    settings['loadDisplay'] = 'pandagl'
if 'toonChatSounds' not in settings:
    settings['toonChatSounds'] = True
if 'language' not in settings:
    settings['language'] = 'English'
if 'cogInterface' not in settings:
    settings['cogInterface'] = True
if 'speedchatPlus' not in settings:
    settings['speedchatPlus'] = True
if 'trueFriends' not in settings:
    settings['trueFriends'] = True
if 'tpTransition' not in settings:
    settings['tpTransition'] = True
if 'fov' not in settings:
    settings['fov'] = OTPGlobals.DefaultCameraFov
if 'talk2speech' not in settings:
    settings['talk2speech'] = False
if 'fpsMeter' not in settings:
    settings['fpsMeter'] = False

loadPrcFileData('Settings: res', 'win-size %d %d' % tuple(settings['res']))
loadPrcFileData('Settings: fullscreen', 'fullscreen %s' % settings['fullscreen'])
loadPrcFileData('Settings: musicVol', 'audio-master-music-volume %s' % settings['musicVol'])
loadPrcFileData('Settings: sfxVol', 'audio-master-sfx-volume %s' % settings['sfxVol'])
loadPrcFileData('Settings: loadDisplay', 'load-display %s' % settings['loadDisplay'])

import time
import sys
import random
import __builtin__
from toontown.launcher.TTELauncher import TTELauncher

__builtin__.launcher = TTELauncher()

notify.info('Starting the game...')
tempLoader = Loader()
backgroundNode = tempLoader.loadSync(Filename('phase_3/models/gui/loading-background'))
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
notify.info('Setting the default font...')
import ToontownGlobals
DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
import ToonBase
ToonBase.ToonBase()
from panda3d.core import *
if base.win is None:
    notify.error('Unable to open window; aborting.')
ConfigVariableDouble('decompressor-step-time').setValue(0.01)
ConfigVariableDouble('extractor-step-time').setValue(0.01)
backgroundNodePath = aspect2d.attachNewNode(backgroundNode, 0)
backgroundNodePath.setPos(0.0, 0.0, 0.0)
backgroundNodePath.setScale(render2d, VBase3(1))
backgroundNodePath.find('**/fg').hide()
logo = OnscreenImage(
    image='phase_3/maps/toontown-logo.jpg',
    scale=(1 / (4.0/3.0), 1, 1 / (4.0/3.0)),
    pos=backgroundNodePath.find('**/fg').getPos())
logo.setTransparency(TransparencyAttrib.MAlpha)
logo.setBin('fixed', 20)
logo.reparentTo(backgroundNodePath)
backgroundNodePath.find('**/bg').setBin('fixed', 10)
base.graphicsEngine.renderFrame()
DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))
import TTLocalizer
if base.musicManagerIsValid:
    music = base.loadMusic('phase_3/audio/bgm/tte_theme.ogg')
    if music:
        music.setLoop(1)
        music.play()
    notify.info('Loading the default GUI sounds...')
    DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
    DirectGuiGlobals.setDefaultClickSound(base.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
else:
    music = None
import ToontownLoader
from direct.gui.DirectGui import *
serverVersion = config.GetString('server-version', 'no_version_set')
buildVersion = 'tte.%s' % config.GetString('build-version', 'no_version_set')
print 'ToontownStart: Build Version:', buildVersion
credit = OnscreenText(text='Powered by Toontown Empire', pos=(1.3, 0.935), scale=0.06, fg=Vec4(0, 0, 1, 0.6), align=TextNode.ARight)
credit.setPos(-0.033,-0.065)
credit.reparentTo(base.a2dTopRight)
build = OnscreenText(buildVersion, pos=(-1.3, -0.975), scale=0.06, fg=Vec4(0, 0, 1, 0.6), align=TextNode.ALeft)
build.setPos(0.033,0.025)
build.reparentTo(base.a2dBottomLeft)
loader.beginBulkLoad('init', TTLocalizer.LoaderLabel, 138, 0, TTLocalizer.TIP_NONE)
from ToonBaseGlobal import *
from direct.showbase.MessengerGlobal import *
from toontown.distributed import ToontownClientRepository
cr = ToontownClientRepository.ToontownClientRepository(serverVersion)
cr.music = music
del music
base.initNametagGlobals()
base.setFrameRateMeter(settings['fpsMeter'])
base.cr = cr
loader.endBulkLoad('init')
from otp.friends import FriendManager
from otp.distributed.OtpDoGlobals import *
cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, 'FriendManager')
base.startShow(cr)
backgroundNodePath.reparentTo(hidden)
backgroundNodePath.removeNode()
del backgroundNodePath
del backgroundNode
del tempLoader
build.cleanup()
del build
base.loader = base.loader
__builtin__.loader = base.loader
autoRun = ConfigVariableBool('toontown-auto-run', 1)

gc.enable()
gc.collect()

if autoRun:
    try:
        base.run()
    except SystemExit:
        pass
    except:
        import traceback
        traceback.print_exc()

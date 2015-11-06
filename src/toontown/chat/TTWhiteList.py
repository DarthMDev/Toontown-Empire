import os
import datetime
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import AppRunnerGlobal
from otp.chat.WhiteList import WhiteList
from toontown.toonbase import TTLocalizer
from toontown.chat import WhiteListData

class TTWhiteList(WhiteList):
    notify = directNotify.newCategory('TTWhiteList')

    def __init__(self):
        WhiteList.__init__(self, WhiteListData.WHITELIST)

        self.defaultWord = TTLocalizer.ChatGarblerDefault[0]
		
    def loadingTextTask(self, task):
        timeIndex = int(globalClock.getFrameTime() - task.startTime) % 3
        timeStrs = (TTLocalizer.NewsPageDownloadingNews0, TTLocalizer.NewsPageDownloadingNews1, TTLocalizer.NewsPageDownloadingNews2)
        textToDisplay = timeStrs[timeIndex] % int(self.percentDownloaded * 100)
        return task.again

    def findWhitelistDir(self):
        if self.WhitelistOverHttp:
            return self.WhitelistStageDir
        searchPath = DSearchPath()
        if AppRunnerGlobal.appRunner:
            searchPath.appendDirectory(Filename.expandFrom('$TT_3_5_ROOT/phase_3.5/models/news'))
        else:
            basePath = os.path.expandvars('$TTMODELS') or './ttmodels'
            searchPath.appendDirectory(Filename.fromOsSpecific(basePath + '/built/' + self.NewsBaseDir))
            searchPath.appendDirectory(Filename(self.NewsBaseDir))
        pfile = Filename(self.WhitelistFileName)
        found = vfs.resolveFilename(pfile, searchPath)
        if not found:
            self.notify.warning('findWhitelistDir - no path: %s' % self.WhitelistFileName)
            self.setErrorMessage(TTLocalizer.NewsPageErrorDownloadingFile % self.WhitelistFileName)
            return None
        self.notify.debug('found whitelist file %s' % pfile)
        realDir = pfile.getDirname()
        return realDir

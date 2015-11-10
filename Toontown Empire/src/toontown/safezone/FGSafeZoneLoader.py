from src.toontown.safezone import FGPlayground
from src.toontown.safezone import SafeZoneLoader


class FGSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    def __init__(self,  hood, parentFSM, doneEvent):
	SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentSFM, doneEvent)
	self.playgroundClass = FGPlayground.FGPlayground
	self.musicFile = 'phase_8/audio/DG_nbrhood.ogg'
	self.activityMusicFile = 'phase_8/audio/bgm/DG_SZ.ogg'
	self.dnaFile = 'phase_2/dna/forest_grove.dna'
	self.safeZoneStorageDNAFile = 'phase_2/dna/storage_FG_sz.dna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.birdSound = map(base.loadSfx, ['phase_8/audio/sfx/SZ_DG_bird_01.ogg',
                                            'phase_8/audio/sfx/SZ_DG_bird_02.ogg',
                                            'phase_8/audio/sfx/SZ_DG_bird_03.ogg',
                                            'phase_8/audio/sfx/SZ_DG_bird_04.ogg'])

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)
        del self.birdSound

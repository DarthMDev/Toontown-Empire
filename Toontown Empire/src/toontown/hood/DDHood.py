from pandac.PandaModules import Vec4
from src.toontown.safezone.DDSafeZoneLoader import DDSafeZoneLoader
from src.toontown.town.DDTownLoader import DDTownLoader
from src.toontown.toonbase import ToontownGlobals
from src.toontown.hood.ToonHood import ToonHood

class DDHood(ToonHood):
    notify = directNotify.newCategory('DDHood')

    ID = ToontownGlobals.DonaldsDock
    TOWNLOADER_CLASS = DDTownLoader
    SAFEZONELOADER_CLASS = DDSafeZoneLoader
    STORAGE_DNA = 'phase_6/dna/storage_DD.pdna'
    SKY_FILE = 'phase_3.5/models/props/BR_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = ((0.803921568627451, 0.4, 0.0, 1.0))

    HOLIDAY_DNA = {
      ToontownGlobals.CHRISTMAS: ['phase_6/dna/winter_storage_DD.pdna'],
      ToontownGlobals.HALLOWEEN: ['phase_6/dna/halloween_props_storage_DD.pdna']}

    def load(self):
        ToonHood.load(self)

        self.fog = Fog('DDFog')

    def setFog(self):
        if base.wantFog:
            self.fog.setColor(0.640625, 0.355469, 0.269531, 1.0)
            self.fog.setExpDensity(0.009)
            render.clearFog()
            render.setFog(self.fog)
            self.sky.clearFog()
            self.sky.setFog(self.fog)

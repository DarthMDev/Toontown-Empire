from src.toontown.safezone.DGSafeZoneLoader import DGSafeZoneLoader
from src.toontown.town.DGTownLoader import DGTownLoader
from src.toontown.toonbase import ToontownGlobals
from src.toontown.hood.ToonHood import ToonHood

class DGHood(ToonHood):
    notify = directNotify.newCategory('DGHood')

    ID = ToontownGlobals.DaisyGardens
    TOWNLOADER_CLASS = DGTownLoader
    SAFEZONELOADER_CLASS = DGSafeZoneLoader
    STORAGE_DNA = 'phase_8/dna/storage_DG.pdna'
    SKY_FILE = 'phase_3.5/models/props/TT_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (0.0, 0.9333333333333333, 0.0, 1.0)

    HOLIDAY_DNA = {
      ToontownGlobals.CHRISTMAS: ['phase_8/dna/winter_storage_DG.pdna'],
      ToontownGlobals.HALLOWEEN: ['phase_8/dna/halloween_props_storage_DG.pdna']}

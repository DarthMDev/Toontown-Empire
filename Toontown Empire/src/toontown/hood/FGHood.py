from src.toontown.safezone.FGSafeZoneLoader import FGSafeZoneLoader
from src.toontown.town.FGTownLoader import FGTownLoader
from src.toontown.toonbase import ToontownGlobals
from src.toontown.hood.ToonHood import ToonHood

class DLHood(ToonHood):
    notify = directNotify.newCategory('FGHood')

    ID = ToontownGlobals.F
    TOWNLOADER_CLASS = DLTownLoader
    SAFEZONELOADER_CLASS = DLSafeZoneLoader
    STORAGE_DNA = 'phase_2/dna/storage_FG.pdna'
    SKY_FILE = 'phase_8/models/props/DL_sky'
    TITLE_COLOR = (0.2627, 0.8039, 0.5019, 1.0)

    HOLIDAY_DNA = {
      ToontownGlobals.CHRISTMAS: ['phase_8/dna/winter_storage_DL.pdna'],
      ToontownGlobals.HALLOWEEN: ['phase_8/dna/halloween_props_storage_DL.pdna']}

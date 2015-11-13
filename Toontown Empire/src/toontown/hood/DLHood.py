from src.toontown.safezone.DLSafeZoneLoader import DLSafeZoneLoader
from src.toontown.town.DLTownLoader import DLTownLoader
from src.toontown.toonbase import ToontownGlobals
from src.toontown.hood.ToonHood import ToonHood

class DLHood(ToonHood):
    notify = directNotify.newCategory('DLHood')

    ID = ToontownGlobals.DonaldsDreamland
    TOWNLOADER_CLASS = DLTownLoader
    SAFEZONELOADER_CLASS = DLSafeZoneLoader
    STORAGE_DNA = 'phase_8/dna/storage_DL.pdna'
    SKY_FILE = 'phase_8/models/props/DL_sky'
    TITLE_COLOR = (0.6, 0.9090909090909091, 0.8, 1.0)

    HOLIDAY_DNA = {
      ToontownGlobals.CHRISTMAS: ['phase_8/dna/winter_storage_DL.pdna'],
      ToontownGlobals.HALLOWEEN: ['phase_8/dna/halloween_props_storage_DL.pdna']}

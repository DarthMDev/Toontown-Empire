from src.toontown.safezone.MMSafeZoneLoader import MMSafeZoneLoader
from src.toontown.town.MMTownLoader import MMTownLoader
from src.toontown.toonbase import ToontownGlobals
from src.toontown.hood.ToonHood import ToonHood


class MMHood(ToonHood):
    notify = directNotify.newCategory('MMHood')

    ID = ToontownGlobals.MinniesMelodyland
    TOWNLOADER_CLASS = MMTownLoader
    SAFEZONELOADER_CLASS = MMSafeZoneLoader
    STORAGE_DNA = 'phase_6/dna/storage_MM.pdna'
    SKY_FILE = 'phase_6/models/props/MM_sky'
    SPOOKY_SKY_FILE = 'phase_6/models/props/MM_sky'
    TITLE_COLOR = (1.0, 0.4117647058823529, 0.7058823529411765, 1.0)

    HOLIDAY_DNA = {
      ToontownGlobals.CHRISTMAS: ['phase_6/dna/winter_storage_MM.pdna'],
      ToontownGlobals.HALLOWEEN: ['phase_6/dna/halloween_props_storage_MM.pdna']}

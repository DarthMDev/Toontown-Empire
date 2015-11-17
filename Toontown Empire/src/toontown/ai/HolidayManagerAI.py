from toontown.toonbase import ToontownGlobals
from datetime import datetime

class HolidayManagerAI:

    def __init__(self, air):
        self.air = air
        self.currentHolidays = []
        self.xpMultiplier = 1
        self.setup()

    def setup(self):
        holidays = config.GetString('active-holidays','')

        if holidays != '':
            for holiday in holidays.split(","):
                holiday = int(holiday)
                self.currentHolidays.append(holiday)

        date = datetime.now()

        if date.month == 10 and date.day == 31:
            # Halloween: Black Cat Day
            self.currentHolidays.append(ToontownGlobals.BLACK_CAT_DAY)

        if date.weekday() == 6:
            # Saturday: Fish Bingo
            self.currentHolidays.append(ToontownGlobals.SILLY_SATURDAY_BINGO)
		
        if date.month == 6 and date.day == 29:
		#mgracer48's  birthday
		    self.currentHolidays.append(ToontownGlobals.MGRACER48_BIRTHDAY)
		
        simbase.air.newsManager.setHolidayIdList([self.currentHolidays])

    def isHolidayRunning(self, holidayId):
        return holidayId in self.currentHolidays

    def isMoreXpHolidayRunning(self):
        if ToontownGlobals.MORE_XP_HOLIDAY in self.currentHolidays:
            self.xpMultiplier = 2
            return True
        return False

    def getXpMultiplier(self):
        return self.xpMultiplier

from toontown.toonbase import TTLocalizer

TIMER_SECONDS = 60

#Info Text
AnyInfoText = "Would you like to buy a Sos Card roll with all Sos Cards for 5000 jellybeans?"
ThreeStarInfoText = "Would you like to buy a Sos Card roll with 3 Star Sos Cards for 7000 jellybeans?"
FourStarInfoText = "Would you like to buy a Sos Card roll with 4 Star Sos Cards for 9000 jellybeans?"
FiveStarInfoText = "Would you like to buy a Sos Card roll with 5 Star Sos Cards for 12000 jellybeans?"

#Sos Text
AnySosText = "All SOS Cards"
ThreeStarSosText = "3 Star SOS Cards"
FourStarSosText = "4 Star SOS Cards"
FiveStarSosText = "5 Star SOS Cards"

# Sos Shop GUI
TIMER_END = 0
USER_CANCEL = 1
ROLL = 2

#States
UnderState = 1
MinimumState = 2
ResetState = 6
MaximumState = 5

#Sos Star States
AnyStarSos = MinimumState
ThreeStarSos = 3
FourStarSos = 4
FiveStarSos = 5

# Restock Results
FULL_SOS = 0
NOT_ENOUGH_MONEY = 1
ROLL_SUCCESSFUL = 2

RollMessages = {
 FULL_SOS: TTLocalizer.RollFullSosMessage,
 NOT_ENOUGH_MONEY: TTLocalizer.RollNoMoneyMessage,
 ROLL_SUCCESSFUL: TTLocalizer.RollSuccessfulMessage
}
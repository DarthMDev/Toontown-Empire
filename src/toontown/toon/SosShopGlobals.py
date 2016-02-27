from toontown.toonbase import TTLocalizer

TIMER_SECONDS = 60

#Sos Cost Amount
CostPerSOS = 5000

# Sos Shop GUI
TIMER_END = 0
USER_CANCEL = 1
ROLL = 2

# Restock Results
FULL_SOS = 0
NOT_ENOUGH_MONEY = 1
ROLL_SUCCESSFUL = 2

RestockMessages = {
 FULL_SOS: TTLocalizer.RollFullSosMessage,
 NOT_ENOUGH_MONEY: TTLocalizer.RollNoMoneyMessage,
 RESTOCK_SUCCESSFUL: TTLocalizer.RollSuccessfulMessage
}
from direct.fsm.StatePush import StateVar
from src.otp.level.EntityStateVarSet import EntityStateVarSet
from src.toontown.cogdominium.CogdoEntityTypes import CogdoBoardroomGameSettings
Settings = EntityStateVarSet(CogdoBoardroomGameSettings)
GameDuration = StateVar(60.0)
FinishDuration = StateVar(10.0)

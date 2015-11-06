from direct.controls import ControlManager
from direct.showbase.InputStateGlobal import inputState


class ToontownControlManager(ControlManager.ControlManager):
    wantWASD = base.wantWASD
    
    def __init__(self, enable=True, passMessagesThrough = False):
        self.passMessagesThrough = passMessagesThrough
        self.inputStateTokens = []
        self.WASDTurnTokens = []
        self.__WASDTurn = True
        self.controls = {}
        self.currentControls = None
        self.currentControlsName = None
        self.isEnabled = 0
        self.forceAvJumpToken = None
        self.inputToDisable = []
        self.forceTokens = None
        self.istWASD = []
        self.istNormal = []      
        if enable:
            self.enable()
    
    def enable(self):
        if self.isEnabled:
            assert self.notify.debug('already isEnabled')
            return
        
        self.isEnabled = 1

        
        #self.inputStateTokens = []
        ist = self.inputStateTokens
        ist.append(inputState.watch("run", 'runningEvent', "running-on", "running-off"))
        
        ist.append(inputState.watch("forward", "force-forward", "force-forward-stop"))
        
        
        ist.append(inputState.watchWithModifiers("reverse", "mouse4", inputSource=inputState.Mouse))
        
        if self.wantWASD:
            self.istWASD.append(inputState.watch("turnLeft", "mouse-look_left", "mouse-look_left-done"))
            self.istWASD.append(inputState.watch("turnLeft", "force-turnLeft", "force-turnLeft-stop"))

            self.istWASD.append(inputState.watch("turnRight", "mouse-look_right", "mouse-look_right-done"))
            self.istWASD.append(inputState.watch("turnRight", "force-turnRight", "force-turnRight-stop"))
            
            self.istWASD.append(inputState.watchWithModifiers("forward", "w", inputSource=inputState.WASD))
            self.istWASD.append(inputState.watchWithModifiers("reverse", "s", inputSource=inputState.WASD))
            self.setWASDTurn(self.__WASDTurn)
        else:
            self.istNormal.append(inputState.watchWithModifiers("forward", "arrow_up", inputSource=inputState.ArrowKeys))
            self.istNormal.append(inputState.watchWithModifiers("reverse", "arrow_down", inputSource=inputState.ArrowKeys))
            self.istNormal.append(inputState.watchWithModifiers("turnLeft", "arrow_left", inputSource=inputState.ArrowKeys))
            ist.append(inputState.watch("turnLeft", "mouse-look_left", "mouse-look_left-done"))
            ist.append(inputState.watch("turnLeft", "force-turnLeft", "force-turnLeft-stop"))
            
            self.istNormal.append(inputState.watchWithModifiers("turnRight", "arrow_right", inputSource=inputState.ArrowKeys))
            ist.append(inputState.watch("turnRight", "mouse-look_right", "mouse-look_right-done"))
            ist.append(inputState.watch("turnRight", "force-turnRight", "force-turnRight-stop"))

        
        if self.wantWASD:
            self.istWASD.append(inputState.watchWithModifiers("jump", "shift"))
        else:
            self.istNormal.append(inputState.watch("jump", "control", "control-up"))

        
        if self.currentControls:
            self.currentControls.enableAvatarControls()
            
            
            
    def setWASDTurn(self, turn):
        self.__WASDTurn = turn

        if not self.isEnabled:
            return
        
        turnLeftWASDSet = inputState.isSet("turnLeft", inputSource=inputState.WASD)
        turnRightWASDSet = inputState.isSet("turnRight", inputSource=inputState.WASD)
        slideLeftWASDSet = inputState.isSet("slideLeft", inputSource=inputState.WASD)
        slideRightWASDSet = inputState.isSet("slideRight", inputSource=inputState.WASD)

        for token in self.WASDTurnTokens:
            token.release()

        if turn:
            self.WASDTurnTokens = (
                inputState.watchWithModifiers("turnLeft", "a", inputSource=inputState.WASD),
                inputState.watchWithModifiers("turnRight", "d", inputSource=inputState.WASD),
                )

            inputState.set("turnLeft", slideLeftWASDSet, inputSource=inputState.WASD)
            inputState.set("turnRight", slideRightWASDSet, inputSource=inputState.WASD)

            inputState.set("slideLeft", False, inputSource=inputState.WASD)
            inputState.set("slideRight", False, inputSource=inputState.WASD)

        else:
            self.WASDTurnTokens = (
                inputState.watchWithModifiers("slideLeft", "a", inputSource=inputState.WASD),
                inputState.watchWithModifiers("slideRight", "d", inputSource=inputState.WASD),
                )

            inputState.set("slideLeft", turnLeftWASDSet, inputSource=inputState.WASD)
            inputState.set("slideRight", turnRightWASDSet, inputSource=inputState.WASD)
                
            inputState.set("turnLeft", False, inputSource=inputState.WASD)
            inputState.set("turnRight", False, inputSource=inputState.WASD)
            
    def disable(self):
        self.isEnabled = 0

        for token in self.inputStateTokens:
            token.release()
        self.inputStateTokens = []

        for token in self.WASDTurnTokens:
            token.release()
        self.WASDTurnTokens = []

        if self.currentControls:
            self.currentControls.disableAvatarControls()
            
        if self.passMessagesThrough: # for not breaking toontown          
            if self.wantWASD:
                print ':(ToontownControlManager) WASD support was enabled.'
                self.istWASD.append(inputState.watchWithModifiers("forward", "w", inputSource=inputState.WASD))
                self.istWASD.append(inputState.watchWithModifiers("reverse", "s", inputSource=inputState.WASD))
                self.istWASD.append(inputState.watchWithModifiers("turnLeft", "a", inputSource=inputState.WASD))
                self.istWASD.append(inputState.watchWithModifiers("turnRight", "d", inputSource=inputState.WASD))
            else:
                print ':(ToontownControlManager) WASD support was disabled.'
                self.istNormal.append(inputState.watchWithModifiers("forward", "arrow_up", inputSource=inputState.ArrowKeys))
                self.istNormal.append(inputState.watchWithModifiers("reverse", "arrow_down", inputSource=inputState.ArrowKeys))
                self.istNormal.append(inputState.watchWithModifiers("turnLeft", "arrow_left", inputSource=inputState.ArrowKeys))
                self.istNormal.append(inputState.watchWithModifiers("turnRight", "arrow_right", inputSource=inputState.ArrowKeys))
            
    def disableWASD(self):
        if self.wantWASD:
            self.forceTokens=[
                inputState.force(
                  "jump", 0, 'ControlManager.disableWASD'),
                inputState.force(
                  "forward", 0, 'ControlManager.disableWASD'),
                inputState.force(
                  "turnLeft", 0, 'ControlManager.disableWASD'),
                inputState.force(
                  "slideLeft", 0, 'ControlManager.disableWASD'),
                inputState.force(
                  "reverse", 0, 'ControlManager.disableWASD'),         
                inputState.force(
                  "turnRight", 0, 'ControlManager.disableWASD'),
                inputState.force(
                  "slideRight", 0, 'ControlManager.disableWASD')                  
            ]
            print 'disableWASD()'
                
                
    def enableWASD(self):
        if self.wantWASD:
            if self.forceTokens:
                for token in self.forceTokens:
                    token.release()
                self.forceTokens = []
                print 'enableWASD'
                
    def reload(self):
        self.wantWASD = base.wantWASD
        if self.wantWASD:       
            for token in self.istNormal:
                token.release()
            self.istNormal = []
            self.inputStateTokens = []
            self.disable()
            self.enable()
        else:
            for token in self.WASDTurnTokens:
                token.release()
            for token in self.istWASD:
                token.release()
            self.istWASD = []
            self.WASDTurnTokens = []
            self.disable()
            self.enable()
# This remains here until me or someone else finishes the code for buyable name change from libary.
# Link the libary npc number here  2005: 'Librarian Larry', to the code and finish the coding for
# name purchasing. ~ FordTheWriter
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.gui.DirectGui import DirectButton
from panda3d.core import aspect2d
from DistributedNPCToonBase import DistributedNPCToonBase
from toontown.chat.ChatGlobals import CFSpeech
from toontown.chat.ChatGlobals import CFTimeout
# from toontown.effects import DustCloud MIGHT BE USED IN THE FUTURE WE HAVE A WHITELIST FOR NAMES
# ~FordTheWriter
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
#from toontown.makeatoon import NameGenerator need this for names
from toontown.makeatoon import NameShop
#def getDustCloud(toon):
#    dustCloud = DustCloud.DustCloud(fBillboard=0)

#    dustCloud.setBillboardAxis(2.0)
#    dustCloud.setZ(3)
#    dustCloud.setScale(0.4)
#    dustCloud.createTrack()
#    return Sequence(Wait(0.5), Func(dustCloud.reparentTo, toon),
                                # dustCloud.track,
                                # Func(dustCloud.destroy))

class DistributedNPCLibary(DistributedNPCToonBase):
    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.next_collision = 0

        self.fsm = ClassicFSM.ClassicFSM(
            'NPCName',
            [
                State.State('off', self.enterOff, self.exitOff, ['pickName']),
                State.State('pickName', self.enter_pick_name, self.exit_name, ['off'])
            ], 'off', 'off')
        self.fsm.enterInitialState()

        self.title = None
        self.notice = None
        self.name = None
        self.buy_button = None
        self.cancel_button = None
        self.index = 0
        self.gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        self.shuffleArrowUp = self.gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        self.shuffleArrowDown = self.gui.find('**/tt_t_gui_mat_shuffleArrowDown')
        self.shuffleUp = self.gui.find('**/tt_t_gui_mat_shuffleUp')
        self.shuffleDown = self.gui.find('**/tt_t_gui_mat_shuffleDown')



    def leave(self, task=None):
        self.setChatAbsolute('', CFSpeech)
        self.setChatAbsolute(TTLocalizer.NameGoodbyeMessage, CFSpeech|CFTimeout)
        self.reset(task)

    def reset(self, task=None):
        self.fsm.request('off')
        base.cr.playGame.getPlace().setState('walk')
        base.setCellsActive(base.bottomCells, 1)
        self.destroy_gui()

        if task is not None:
            return task.done

    def disable(self):
        self.ignoreAll()
        self.destroy_gui()
        self.next_collision = 0
        DistributedNPCToonBase.disable(self)

# Use the make a toon type name gui for this
    def popup_Pick_Name_GUI(self):
        self.setChatAbsolute('', CFSpeech)
        self.setChatAbsolute(TTLocalizer.NameEnoughBeans, CFSpeech|CFTimeout)
        base.setCellsActive(base.bottomCells, 0)
        self.create_gui()

    def create_gui(self):
        NameShop.makeLabel()
        self.buybutton = DirectButton(aspect2d,
                                      relief=None,
                                      image=(self.shuffleUp,
                                             self.shuffleDown),
                                      text=TTLocalizer.NameGUIPurchase,
                                      text_font=ToontownGlobals.getInterfaceFont(),
                                      text_scale=0.11, text_pos=(0, -0.02),
                                      pos=(-0.60, 0, -0.90),
                                      text_fg=(1, 1, 1, 1),
                                      text_shadow=(0, 0, 0, 1),
                                      command=self.handle_buy)

        self.cancelbutton = DirectButton(aspect2d,
                                         relief=None,
                                         image=(self.shuffleUp,
                                                self.shuffleDown),
                                         text=TTLocalizer.NameGUICancel,
                                         text_font=ToontownGlobals.getInterfaceFont(),
                                         text_scale=0.11, text_pos=(0, -0.02),
                                         pos=(0.60, 0, -0.90),
                                         text_fg=(1, 1, 1, 1),
                                         text_shadow=(0, 0, 0, 1), command=self.leave)


        self.update_gui_by_index()

    def destroy_gui(self):
        for element in [self.buyButton, self.cancelButton]:
            if element:
                element.destroy()
                element = None

        self.index = 0
    def handle_buy(self):
        pass

    def enter_pick_name(self):
        pass

    def exit_name(self):
        pass

    def handle_set_index(self, offset):
        pass

    def update_gui_by_index(self):
        pass

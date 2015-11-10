if __debug__:
    import wx, sys
    from direct.stdpy import threading
    defaultText = ""

    def __inject_wx(_):
        code = textbox.GetValue()
        exec(code, globals())

    def openInjector_wx():
        app = wx.App(redirect=False)
        frame = wx.Frame(None, title="Injector", size=(640, 400), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX)
        panel = wx.Panel(frame)
        button = wx.Button(parent=panel, id=-1, label="Inject", size=(50, 20), pos=(295, 0))
        global textbox
        textbox = wx.TextCtrl(parent=panel, id=-1, pos=(20, 22), size=(600, 340), style=wx.TE_MULTILINE)
        frame.Bind(wx.EVT_BUTTON, __inject_wx, button)
        frame.Show()
        app.SetTopWindow(frame)
        textbox.AppendText(defaultText)
        threading.Thread(target=app.MainLoop).start()

    openInjector_wx()
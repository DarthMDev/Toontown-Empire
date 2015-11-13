if __debug__:
 from pandac.PandaModules import *
 import Tkinter as tk
 from direct.stdpy import thread
 from src.toontown.toonbase import PresetImports
 root = tk.Tk()
 frame = tk.Frame(root)
 text = tk.Text(frame,width=90,height=70)

 def runInjectorCode():
        global text
        exec (text.get(1.0, "end"),globals())

 def openInjector():
     print 'tte Injector Enabled'
     root.geometry('600x600')
     root.title('Toontown Empire Dev Injector')
     root.resizable(True,True)
     global text
     text.pack(side="left")
     tk.Button(root,text="Inject!",command=runInjectorCode).pack()
     scroll = tk.Scrollbar(frame)
     scroll.pack(fill="y",side="right")
     scroll.config(command=text.yview)
     text.config(yscrollcommand=scroll.set)
     frame.pack(fill="y")
     thread.start_new_thread(root.mainloop,())

openInjector()	

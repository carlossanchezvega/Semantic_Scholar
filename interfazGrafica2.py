from tkinter import*
import random
import time
from tkinter.messagebox import askokcancel

from PIL import Image, ImageTk

class Radiobar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.var = StringVar()
        for pick in picks:
            rad = Radiobutton(self, text=pick, value=pick, variable=self.var)
            rad.pack(side=side, anchor=anchor, expand=YES)
    def state(self):
        return self.var.get()


class Quitter(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(expand=YES, fill=BOTH, side=LEFT)
    def quit(self):
        ans = askokcancel('Title', "Really quit?")
        if ans: Frame.quit(self)


if __name__ == '__main__':
    root = Tk()
    root.geometry("1200x440+0+0")
    f1 = Frame(root,width = 900,height=100,relief=SUNKEN)
    f1.pack(side=LEFT)

    gui = Radiobar(f1, ['A', 'B', 'C'], side=TOP, anchor=NW)
    gui.pack(side=LEFT, fill=Y)
    gui.config(relief=RIDGE,  bd=2)

    def allstates(): print(gui.state())
    Quitter(root).pack(side=RIGHT)
    Button(root, text='Peek', command=allstates).pack(side=RIGHT)
    root.mainloop()


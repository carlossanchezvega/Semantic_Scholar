import itertools
import threading
import time
import sys
from tkinter import *

done = False
#here is the animation
def animate():
    # for c in itertools.cycle(['|', '/', '-', '\\']):
    #     if done:
    #         break
    #     sys.stdout.write('\rloading ' + c)
    #     sys.stdout.flush()
    #     time.sleep(0.1)
    frame2 = PhotoImage(file='/home/csanchez/Escritorio/giphy.gif', format="gif -index 2")

    sys.stdout.write('\rDone!     ')

t = threading.Thread(target=animate)
t.start()

#long process here
time.sleep(10)
done = True
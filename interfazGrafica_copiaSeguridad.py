from tkinter import*
import random
import time
from tkinter import messagebox
from tkinter.messagebox import askokcancel

import pymongo
from PIL import Image, ImageTk
from GetInfo import GetInfo
from Similarities_in_between_class import Similarities_in_between
from Graph_class import Graph_class

root = Tk()
root.geometry("1600x700+0+0")
root.title("Academic paper comparator")

Tops = Frame(root,bg="white",width = 1600,height=50,relief=SUNKEN)
Tops.pack(side=TOP)

f1 = Frame(root,width = 900,height=700,relief=SUNKEN)
f1.pack(side=LEFT)

f2 = Frame(root ,width = 400,height=700,relief=SUNKEN)
f2.pack(side=RIGHT)
#------------------TIME--------------
# localtime=time.asctime(time.localtime(time.time()))
#-----------------INFO TOP------------
lblinfo = Label(Tops, font=( 'aria' ,30, 'bold' ),text="Carlos Sánchez Vega",fg="steel blue",bd=10,anchor='w')
lblinfo.grid(row=0,column=0)
# lblinfo = Label(Tops, font=( 'aria' ,20, ),text=localtime,fg="steel blue",anchor=W)
# lblinfo.grid(row=1,column=0)

#---------------Calculator------------------
text_Input=StringVar()
operator =""

# txtdisplay = Entry(f2,font=('ariel' ,20,'bold'), textvariable=text_Input , bd=5 ,insertwidth=7 ,bg="white",justify='right')
# txtdisplay.grid(columnspan=4)


class Radiobar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.var = StringVar()
        for pick in picks:
            rad = Radiobutton(self, text=pick, value=pick, variable=self.var, font=( 'aria' ,16, 'bold' ),fg="steel blue")
            rad.pack(side=side, anchor=anchor, expand=YES)
        self.var.set("Grafo asociado")
    def state(self):
        return self.var.get()


def  btnclick(numbers):
    global operator
    operator=operator + str(numbers)
    text_Input.set(operator)

def clrdisplay():
    global operator
    operator=""
    text_Input.set("")

def eqals():
    global operator
    sumup=str(eval(operator))

    text_Input.set(sumup)
    operator = ""
def retrieve_author():
    return txtburger.get()



def qexit():
    ans = askokcancel('Title', "Really quit?")
    if ans:
        root.destroy()

def reset():
    Burger.set("")

Burger = StringVar()
lblburger = Label(f1, font=( 'aria' ,16, 'bold' ),text="Elija una funcionalidad",fg="steel blue",bd=10,anchor='w')
lblburger.grid(row=0,column=0, padx=(63, 0))
gui = Radiobar(f1, ['Grafo asociado','Comparador del autor con otros coautores', 'Comparador obras del autor', 'Comparador de obras entre autor y coautores'], side=TOP, anchor=NW)
gui.grid(row=0,column=1)
lblburger = Label(f1, font=( 'aria' ,16, 'bold' ),text="Nombre del autor",fg="steel blue",bd=10,anchor='w')
lblburger.grid(row=4,column=0,  pady=50)
txtburger = Entry(f1,font=('ariel' ,16,'bold'), textvariable=Burger , bd=6,insertwidth=4,bg="powder blue" ,justify='right')
txtburger.grid(row=4 ,column=1, pady=50)

#-----------------------------------------buttons------------------------------------------
lblTotal = Label(f1,text="---------------------",fg="white")
lblTotal.grid(row=6,columnspan=3)

btnreset=Button(f1,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,16,'bold'),width=10, text="RESET", bg="powder blue",command=reset)
btnreset.grid(row=7, column=1)

btnexit=Button(f1,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,16,'bold'),width=10, text="EXIT", bg="powder blue",command=qexit)
btnexit.grid(row=7, column=3)


def price():
    #root.geometry("1200x440+0+0")
    root.geometry("1200x440+0+0")
    root.title("Price List")
    load = Image.open("/home/csanchez/IdeaProjects/proyectoDePrueba/distances1.jpg")
    render = ImageTk.PhotoImage(load)
    window = Toplevel(root)
    window.minsize(width=100, height=100)
    window.geometry('1000x920+0+0')
    img = Label(window, image=render)
    img.image = render
    img.place(x=0, y=0)


    #get_info = GetInfo("mongodb://localhost","Alberto Fernández-Isabel" )
    #get_info.requestInfo()

    url_connection = "mongodb://localhost"
    connection = pymongo.MongoClient(url_connection)
    db = connection.authorAndPublicationData
    collection_authors = db.authors
    collection_publications = db.publications
    author = retrieve_author()


    getInfo = GetInfo(url_connection,author, collection_authors, collection_publications)
    result, best_similarity = getInfo.requestInfo()
    if result ==0 :

        option_selected = gui.state()
        if option_selected=='Grafo asociado':
            grafo = Graph_class("data/allInfo.json", best_similarity, collection_authors, collection_publications)
            grafo.create_graph()
        else:
            represent_similarities = Similarities_in_between(option_selected, best_similarity, url_connection,
                                                            collection_authors, collection_publications,6)
            represent_similarities.create_similarity_plot()
    else:
        messagebox.showerror("Error", "No existe ningún autor con ese nombre")

    root.mainloop()

btnprice=Button(f1,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,16,'bold'),width=10, text="PRICE", bg="powder blue",command=price)
btnprice.grid(row=7, column=0)

root.mainloop()


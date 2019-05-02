from tkinter import *
import random
import time
from tkinter import messagebox
from tkinter.messagebox import askokcancel

import pymongo
from PIL import Image
from GetInfo import GetInfo
from Similarities_in_between_class import Similarities_in_between
from Graph_class import Graph_class


class Radiobar( Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.var = StringVar()
        for pick in picks:
            rad = Radiobutton(self, text=pick, value=pick, variable=self.var, font=('aria', 16, 'bold'),
                              fg="steel blue")
            rad.pack(side=side, anchor=anchor, expand=YES)
        self.var.set("Grafo asociado")

    def state(self):
        return self.var.get()


class interfazGrafica_copiaSeguridad:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1600x700+0+0")
        self.master.wm_title("Academic paper comparator")
        self.master.title("Academic paper comparator")

        self.Tops = Frame(root, bg="white", width=1600, height=50, relief=SUNKEN)
        self.Tops.pack(side=TOP)

        self.f1 = Frame(root, width=900, height=700, relief=SUNKEN)
        self.f1.pack(side=LEFT)

        self.f2 = Frame(root, width=400, height=700, relief=SUNKEN)
        self.f2.pack(side=RIGHT)
        # ------------------TIME--------------
        # localtime=time.asctime(time.localtime(time.time()))
        # -----------------INFO TOP------------
        self.lblinfo = Label(self.Tops, font=('aria', 30, 'bold'), text="Carlos Sánchez Vega", fg="steel blue", bd=10, anchor='w')
        self.lblinfo.grid(row=0, column=0)
        # lblinfo = Label(Tops, font=( 'aria' ,20, ),text=localtime,fg="steel blue",anchor=W)
        # lblinfo.grid(row=1,column=0)

        # ---------------Calculator------------------
        self.text_Input = StringVar()
        self.operator = ""

        self.Burger = StringVar()
        self.lblburger = Label(self.f1, font=('aria', 16, 'bold'), text="Elija una funcionalidad", fg="steel blue", bd=10,
                          anchor='w')
        self.lblburger.grid(row=0, column=0, padx=(63, 0))
        self.gui = Radiobar(self.f1, ['Grafo asociado', 'Comparador del autor con otros coautores', 'Comparador obras del autor',
                            'Comparador de obras entre autor y coautores'], side=TOP, anchor=NW)
        self.gui.grid(row=0, column=1)
        self.lblburger = Label(self.f1, font=('aria', 16, 'bold'), text="Nombre del autor", fg="steel blue", bd=10, anchor='w')
        self.lblburger.grid(row=4, column=0, pady=50)
        self.txtburger = Entry(self.f1, font=('ariel', 16, 'bold'), textvariable=self.Burger, bd=6, insertwidth=4, bg="powder blue",
                          justify='right')
        self.txtburger.grid(row=4, column=1, pady=50)

        # -----------------------------------------buttons------------------------------------------
        self.lblTotal = Label(self.f1, text="---------------------", fg="white")
        self.lblTotal.grid(row=6, columnspan=3)

        self.btnreset = Button(self.f1, padx=16, pady=8, bd=10, fg="black", font=('ariel', 16, 'bold'), width=10, text="RESET",
                          bg="powder blue", command=self.reset)
        self.btnreset.grid(row=7, column=1)

        self.btnexit = Button(self.f1, padx=16, pady=8, bd=10, fg="black", font=('ariel', 16, 'bold'), width=10, text="EXIT",
                         bg="powder blue", command=self.qexit)
        self.btnexit.grid(row=7, column=3)

        self.btnprice = Button(self.f1, padx=16, pady=8, bd=10, fg="black", font=('ariel', 16, 'bold'), width=10, text="PRICE",
                          bg="powder blue", command=self.ejecutar)
        self.btnprice.grid(row=7, column=0)


    def greet(self):
        print("Greetings!")

    def  btnclick(self, numbers):
        global operator
        operator=operator + str(numbers)
        self.text_Input.set(operator)

    def clrdisplay(self):
        global operator
        operator=""
        self.text_Input.set("")


    def retrieve_author(self):
        return self.txtburger.get()



    def qexit(self):
        ans = askokcancel('Title', "Really quit?")
        if ans:
            root.destroy()

    def reset(self):
        self.Burger.set("")

    def ejecutar(self):
        # #root.geometry("1200x440+0+0")
        # root.geometry("1200x440+0+0")
        # root.title("Price List")
        # load = Image.open("/home/csanchez/IdeaProjects/proyectoDePrueba/distances1.jpg")
        # render = ImageTk.PhotoImage(load)
        # window = Toplevel(root)
        # window.minsize(width=100, height=100)
        # window.geometry('1000x920+0+0')
        # img = Label(window, image=render)
        # img.image = render
        # img.place(x=0, y=0)


        #get_info = GetInfo("mongodb://localhost","Alberto Fernández-Isabel" )
        #get_info.requestInfo()

        url_connection = "mongodb://localhost"
        connection = pymongo.MongoClient(url_connection)
        db = connection.authorAndPublicationData
        collection_authors = db.authors
        collection_publications = db.publications
        #db.authors.drop()
        #db.publications.drop()
        #db.authors.drop()
        author = self.retrieve_author()


        getInfo = GetInfo(url_connection,author, collection_authors, collection_publications)
        result, best_similarity = getInfo.requestInfo()
        if result ==0 :

            option_selected = self.gui.state()
            if option_selected=='Grafo asociado':
                grafo = Graph_class("data/allInfo.json", best_similarity, collection_authors, collection_publications)
                grafo.create_graph()
            else:
                represent_similarities = Similarities_in_between(option_selected, best_similarity, url_connection,
                                                                collection_authors, collection_publications,6)
                self.btnprice.config(relief=RAISED, state=ACTIVE)

                status_execution = represent_similarities.create_similarity_plot()
                print('LLEGA AQUI')

        else:
            messagebox.showerror("Error", "No existe ningún autor con ese nombre")
        #root.destroy()

root = Tk()
my_gui = interfazGrafica_copiaSeguridad(root)
root.mainloop()











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
        """
        Gets the value from a radiobar
        Args:
        Returns:
        """

        return self.var.get()


class Pantalla_presentacion:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1600x700+0+0")
        self.master.wm_title("Academic paper comparator")
        self.master.title("Academic paper comparator")

        self.Tops = Frame(master, bg="white", width=1600, height=50, relief=SUNKEN)
        self.Tops.pack(side=TOP)

        self.f1 = Frame(master, width=900, height=700, relief=SUNKEN)
        self.f1.pack(side=LEFT)

        self.f2 = Frame(master, width=400, height=700, relief=SUNKEN)
        self.f2.pack(side=RIGHT)
        self.lblinfo = Label(self.Tops, font=('aria', 30, 'bold'), text="Carlos Sánchez Vega", fg="steel blue", bd=10, anchor='w')
        self.lblinfo.grid(row=0, column=0)
        self.text_Input = StringVar()
        self.operator = ""

        self.Author = StringVar()
        self.lblfuncionalidad = Label(self.f1, font=('aria', 16, 'bold'), text="Elija una funcionalidad", fg="steel blue", bd=10,
                          anchor='w')
        self.lblfuncionalidad.grid(row=0, column=0, padx=(63, 0))
        self.gui = Radiobar(self.f1, ['Grafo asociado', 'Comparador del autor con otros coautores', 'Comparador obras del autor',
                            'Comparador de obras entre autor y coautores'], side=TOP, anchor=NW)
        self.gui.grid(row=0, column=1)
        self.lblfuncionalidad = Label(self.f1, font=('aria', 16, 'bold'), text="Nombre del autor", fg="steel blue", bd=10, anchor='w')
        self.lblfuncionalidad.grid(row=4, column=0, pady=50)
        self.txtauthor = Entry(self.f1, font=('ariel', 16, 'bold'), textvariable=self.Author, bd=6, insertwidth=4, bg="powder blue",
                          justify='right')
        self.txtauthor.grid(row=4, column=1, pady=50)
        self.btnEjecutar = Button(self.f1, padx=16, pady=8, bd=10, fg="black", font=('ariel', 16, 'bold'), width=10, text="EJECUTAR",
                                  bg="powder blue", command=self.ejecutar)
        self.btnEjecutar.grid(row=7, column=1)

        self.btnreset = Button(self.f1, padx=16, pady=8, bd=10, fg="black", font=('ariel', 16, 'bold'), width=10, text="RESET",
                          bg="powder blue", command=self.reset)
        self.btnreset.grid(row=7, column=2)

        self.btnexit = Button(self.f1, padx=16, pady=8, bd=10, fg="black", font=('ariel', 16, 'bold'), width=10, text="EXIT",
                         bg="powder blue", command=self.qexit)
        self.btnexit.grid(row=7, column=3)





    def clrdisplay(self):
        """
        Clear the textbox of the author
        Args:
        Returns:
        """
        global operator
        operator=""
        self.text_Input.set("")


    def retrieve_author(self):
        """
        Get the value from the textbox of the author
        Args:
        Returns:
        """
        return self.txtauthor.get()

    def qexit(self):
        """
        Exit the programn if confirmation is received
        Args:
        Returns:
        """
        ans = askokcancel('Title', "Really quit?")
        if ans:
            self.master.destroy()

    def reset(self):
        self.txtauthor.set("")

    def ejecutar(self):
        url_connection = "mongodb://localhost"
        connection = pymongo.MongoClient(url_connection)
        db = connection.authorAndPublicationData
        collection_authors = db.authors
        collection_publications = db.publications
        author = self.retrieve_author()

        getInfo = GetInfo(url_connection,author, collection_authors, collection_publications)
        result, best_similarity = getInfo.requestInfo()
        if result ==0:
            option_selected = self.gui.state()
            if option_selected=='Grafo asociado':
                grafo = Graph_class("data/allInfo.json", best_similarity, collection_authors, collection_publications)
                grafo.create_graph()
            else:
                represent_similarities = Similarities_in_between(option_selected, best_similarity, url_connection,
                                                                collection_authors, collection_publications,10)
                self.btnEjecutar.config(relief=RAISED, state=ACTIVE)

                status_execution = represent_similarities.create_similarity_plot()

        else:
            messagebox.showerror("Error", "No existe ningún autor con ese nombre")

def main():
    root = Tk()
    my_gui = Pantalla_presentacion(root)
    root.mainloop()


if __name__ == "__main__":
    main()
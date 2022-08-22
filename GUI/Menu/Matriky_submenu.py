import tkinter
from tkinter import Menu
from PIL import ImageTk, Image

#TODO> (main_menu, main_frame) + event handlers
def matrikaSubmenu(main_menu):
    #icons upload
    bookopen = ImageTk.PhotoImage(Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/bookopen.jpg"))
    arrowcircle = ImageTk.PhotoImage(Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/arrowcircle.jpg"))
    pohreb = ImageTk.PhotoImage(Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/pohreb.jpg"))
    krest = ImageTk.PhotoImage(Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/userplus.jpg"))
    sobas = ImageTk.PhotoImage(Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/sobas.jpg"))

    matriky = Menu(main_menu, tearoff=0)
    matriky.add_command(label="   Seznam členů", image=bookopen, compound=tkinter.LEFT)
    matriky.bookopen = bookopen
    matriky.add_command(label="   Pohyb členů", image=arrowcircle, compound=tkinter.LEFT )
    matriky.arrowcircle = arrowcircle
    matriky.add_separator()
    matriky.add_command(label="   Pohřební matrika", image=pohreb, compound=tkinter.LEFT)
    matriky.pohreb = pohreb
    matriky.add_command(label="   Křestní matrika", image=krest, compound=tkinter.LEFT)
    matriky.krest = krest
    matriky.add_command(label="   Sobášní matrika", image=sobas, compound=tkinter.LEFT)
    matriky.sobas = sobas
    main_menu.add_cascade(label="Matriky", menu=matriky)
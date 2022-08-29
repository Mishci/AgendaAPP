#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter
from tkinter import *
from PIL import ImageTk, Image
from bs4 import BeautifulSoup, SoupStrainer
import requests
import codecs


def texty(main_menu, main_frame):
    bookIcon = ImageTk.PhotoImage(Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/plus.jpg"))

    LitTexty = Menu(main_menu, tearoff=0)
    LitTexty.add_command(label="  Texty na neděli ", image=bookIcon, compound=tkinter.LEFT,
                         command=lambda: log_texts(main_frame)
                         )
    LitTexty.bookIcon = bookIcon
    main_menu.add_cascade(label="Liturgické texty", menu=LitTexty)


def log_texts(main_frame):
    widgetList = main_frame.winfo_children()
    # deleting the old treeview table from the screen before rendering a new one
    if len(widgetList) > 0:
        for widget in widgetList:
            widget.destroy()

    # getting the current url of the texty page
    BASE_URL = "https://www.ccsh.cz"
    base_response = requests.get(BASE_URL)
    base_content = base_response.content
    base_content = codecs.decode(base_content, 'utf-8')
    searched_center_tag = SoupStrainer(id="sloupek")
    base_soup = BeautifulSoup(base_content, 'html.parser', parse_only=searched_center_tag)
    center = base_soup.find("center")
    link = center.find('a').get("href")

    # using the current url to get soup
    response = requests.get(f"{BASE_URL + link}")
    response = response.content
    response = codecs.decode(response, 'utf-8')
    content = response
    searched_div = SoupStrainer(id="text")
    soup = BeautifulSoup(content, 'html.parser', parse_only=searched_div)
    print(f"soup = {soup} \n end of soup")

    text_frame = Frame(main_frame)
    text_frame.config(bg="#7bacc7", border=0, pady=20)
    text_frame.pack(fill=Y)

    #using the soup and strong tags filter selection for the output
    par_text = soup.getText()
    print(f'text = {par_text}')

    for item in soup.select(selector="p strong"):

        strong_label = tkinter.Label(text_frame, text=f"{item.text}", font=('Helvetica', 10, 'bold'))
        strong_label.config(border=0, bg="#7bacc7", wraplength=650)
        strong_label.pack()


        if "Tužby" in item.text:
            selection = item.parent.find_all_next("p")
            normal = selection[0].text + "\n" + selection[1].text + "\n \n"
            normal_label = tkinter.Label(text_frame, text=f"{normal} \n", font=('Helvetica', 10, 'normal'))
            normal_label.config(border=0, bg="#7bacc7", wraplength=600, anchor="e", justify=LEFT )
            normal_label.pack()


        elif item.text == "Modlitba před čtením ze sv. Písem:":
            normal = item.parent.find_next("p")
            normal_label = tkinter.Label(text_frame, text=f"{normal.text} \n", font=('Helvetica', 10, 'normal'))
            normal_label.config(border=2, bg="#7bacc7", wraplength=600, anchor="e", justify=LEFT)
            normal_label.pack()

        elif "požehnání:" in item.text:
            normal = item.parent.find_next("p")
            normal_label = tkinter.Label(text_frame, text=f"{normal.text} \n", font=('Helvetica', 10, 'normal'))
            normal_label.config(border=2, bg="#7bacc7", wraplength=600,  anchor="e", justify=LEFT,  )
            normal_label.pack()



        else:
            normal = item.parent.text.replace(f"{item.text}", "")
            normal_label = tkinter.Label(text_frame, text=f"{normal} \n", font=('Helvetica', 10, 'normal'))
            normal_label.config(border=2, bg="#7bacc7", anchor="e", justify=LEFT)
            normal_label.pack()




    text_frame.update()

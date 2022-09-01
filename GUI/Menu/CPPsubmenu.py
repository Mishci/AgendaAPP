#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter
from tkinter import *
from tkinter import ttk
from pandas import notna, isna
from IPython.display import display
from functools import reduce
import numpy as numpy
from PIL import ImageTk, Image
from LOGIC.readDataFromZippedExcel import readDataFromZippedExcel
from LOGIC.generate_archs import pop_up_gui
from GUI.Right_click_menu.Right_click_menu import RighClickMenu

i = 0
repetition = 0
iid = None
y_coord = 0


def cppSubmenu(main_menu, main_frame):
    """root = main= Main_Frame(root) is not the same widget as root = TK().
    root = self.ref in Menubar file which == main_frame widget
    main_menu parameter = Menubar, thus placing the submenu into Menubar widget"""

    # ICONS UPLOAD
    plusIcon = ImageTk.PhotoImage(Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/plus.jpg"))
    minusIcon = ImageTk.PhotoImage(Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/minus.jpg"))
    user_pay_check_icon = ImageTk.PhotoImage(
        Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/userPayCheck.jpg"))
    checkIcon = ImageTk.PhotoImage(
        Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/check.jpg"))
    krizek = ImageTk.PhotoImage(
        Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/krizek.jpg"))
    archArrow = ImageTk.PhotoImage(
        Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/arrow.jpg"))

    CPP = Menu(main_menu, tearoff=0)
    CPP.add_command(label="  Filtruj platící", image=checkIcon, compound=tkinter.LEFT,
                    command=lambda: searchComboBoxNP(main_frame, True))
    CPP.checkIcon = checkIcon
    CPP.add_command(label="  Filtruj neplatící", image=krizek, compound=tkinter.LEFT,
                    command=lambda: searchComboBoxNP(main_frame, False))
    CPP.krizek = krizek
    CPP.add_separator()
    CPP.add_command(label="  Přidej nový rok", image=plusIcon, compound=tkinter.LEFT, command=lambda: cities())
    CPP.plusIcon = plusIcon  # Holding the refference of the image / without it it wouldnt show
    CPP.add_command(label="  Vymaž celý rok", image=minusIcon, compound=tkinter.LEFT)
    CPP.minusIcon = minusIcon  # Holding the refference of the image / without it it wouldnt show
    CPP.add_separator()
    CPP.add_command(label="  Kontroluj platby člena", image=user_pay_check_icon, compound=tkinter.LEFT,
                    command=lambda: kontrolujPlatbyClena(main_frame))
    CPP.user_pay_check_icon = user_pay_check_icon

    CPP.add_separator()

    # vyberci archy submenu

    Archy = Menu(CPP)
    Archy.bind("<Leave>", lambda: abortArchyMenu(event=e, archy_widget=Archy))
    CPP.add_command(label="   Vytvoř výběrčí archy", image=archArrow, compound=tkinter.BOTTOM,
                    command=lambda: guiArchy(Archy, CPP, main_frame))
    CPP.archArrow = archArrow

    main_menu.add_cascade(label="CPP", menu=CPP, )


# ***************************************** ONCLICK FUNCTIONS TO TRIGGER ***********************************************

# ----------------------------------------- FILTRUJ PLATICI ---------------------------------------------------
def filtrujPlatici(main_frame, od, do, data, pay):
    """Tato funkce je volaná jako command v menubottonu FiltrujNelatící. Nejprve onclick zmaže obsah main_frame
        pak spustí funkci na načtení dat, a je načtení úspěšné, získá hodnoty labelů sloupců načínajících na CPP
        a tyto vykreslí do tabulky spolu s příměním a jménem"""

    selectedYearsTuple = (od, do)

    # getting know if main_frame exists
    widgetList = main_frame.winfo_children()
    # deleting the old treeview table from the screen before rendering a new one
    if len(widgetList) > 1:
        widgetList[1].destroy()

    if data is not None:

        columnList = data.columns.values
        displayCols = ["Přijmení", "Jméno"]

        # slicing the column starting with CPP based on the inputs from the combobox selection
        # default values are from: CPP 2020 to: CPP 2021
        CPPcols = [col for col in columnList if col.startswith('CPP')]

        if selectedYearsTuple[1] == CPPcols[0]:
            CPPcolsSlice = CPPcols[0]
        else:
            CPPcolsSlice = CPPcols[CPPcols.index(selectedYearsTuple[0]): CPPcols.index(selectedYearsTuple[1]) + 1]

        for col in CPPcolsSlice:
            displayCols.append(str(col))

        # getting the array of row filtering conditions
        filterCols = [notna(data[displayCols[displayCols.index(item)]]) for item in displayCols[2:]] if pay else [
            isna(data[displayCols[displayCols.index(item)]]) for item in displayCols[2:]]

        # joining all filtering conditions by AND/OR operator + gaining data for display
        # filtering out persons paying in each of the selected years vs not paying in at least in one of selected years
        selection = data.loc[reduce(numpy.logical_and, filterCols), displayCols] if pay else data.loc[
            reduce(numpy.logical_or, filterCols), displayCols]

        display(selection)

        for col in selection:
            if col != "Přijmení" and col != "Jméno":
                selection[col] = selection[col].fillna(0)
            else:
                pass

        createTreeview(main_frame, displayCols, selection)


# ---------------------------------- KONTROLUJ PLATBY CLENA ----------------------------------------------------
def kontrolujPlatbyClena(main_frame):
    # clearing the frame of all the previous widgets
    widgetList = main_frame.winfo_children()
    if len(widgetList) > 0:
        for widget in widgetList:
            widget.destroy()
    # creating the search interface only into absolutely empty frame / ee. just 1*
    widgetList = main_frame.winfo_children()
    if len(widgetList) == 0:

        formular = LabelFrame(main_frame, text="  Informace o platbách CPP člena:  ", width=400, bd=5, height=200,
                              padx=5,
                              pady=5, bg="lightblue")
        formular.pack()
        # ---------SURNAME
        surname = StringVar()
        surnameLabel = Label(formular, text="   Příjmení člena   ", bg="lightblue")
        surnameLabel.grid(row=0, column=0, padx=(15, 0), pady=(15, 10))
        surnameEntry = Entry(formular, textvariable=surname, )
        surnameEntry.grid(row=0, column=1, padx=15, pady=5)
        surnameEntry.focus_set()
        # ---------NAME
        name = StringVar()
        nameLabel = Label(formular, text="Jméno člena", bg="lightblue")
        nameLabel.grid(row=1, column=0, padx=(15, 0), pady=(15, 10))
        nameEntry = Entry(formular, textvariable=name, )
        nameEntry.grid(row=1, column=1, padx=15, pady=5)

        # refreshing the widget count list after adding the searchbar
        # running only if searchbar exists. rerenders just tne treeview after every selection
        widgetList = main_frame.winfo_children()
        if len(widgetList) >= 1:
            def vyhledejSearchBox(surname, name):
                # getting know if main_frame exists
                widgetList = main_frame.winfo_children()
                # deleting the old treeview table from the screen before rendering a new one
                if len(widgetList) > 1:
                    widgetList[1].destroy()

                data = readDataFromZippedExcel()

                surnameGet = surname.get()
                nameGet = name.get()
                print(data)

                # preparing a columns slice to display from the dataframe
                columnlist = data.columns.values
                displayCols = ["Přijmení", "Jméno", "Nar."]
                CPPcols = [col for col in columnlist if col.startswith('CPP')]
                for col in CPPcols:
                    displayCols.append(str(col))

                selByFirstName = data.loc[(data["Přijmení"] == surnameGet) & (data["Jméno"] == nameGet), displayCols]

                # changing all NaN in CPP columns with 0
                cols = list(selByFirstName.columns.values)

                for col in cols:
                    if col.startswith("CPP"):
                        selByFirstName[col] = selByFirstName[col].fillna(0)

                    else:
                        pass

                print(selByFirstName)

                createTreeview(main_frame, displayCols=displayCols, selection=selByFirstName)

                return selByFirstName

            # ----------BUTTON ---------------------------------------
            hledej = Button(formular, text=" Vyhledat ", command=lambda: vyhledejSearchBox(surname, name))
            hledej.grid(row=3, column=1)


        else:
            pass


# ---------------------------------------------------ARCHY-------------------------------------------------------------
# sorting out city names to be used by archy menu
def cities():
    """"converts the values of Adress column into list, sorting out just those that are not None, if pass -> converts
    the value to string -> then splits by empty space -> finally chosing out just the name if the city, i.e. the [0]"""
    data = readDataFromZippedExcel()

    places = [str(item) for item in list(data["Město"]) if
              item is not None]
    print(places)
    adresses = list(set(places))
    print(adresses)
    adresses.sort()
    return adresses


# creating the pop-up menu
def guiArchy(Archy, CPP, mainframe):
    """"creates the Archy.addcommands by looping in adressess, thus creating the pop-upo menu, triggered every time
    the user hovers the mouse over <Vyber mesto pro arch>. Binded on <Vytvor archy>, onlick on <Vytvor archy> adds
    another item into CPP menu (<Vyber mesto pro arch>). The repetitions of trigger is controlled bz global variable
    repetition + avoiding rewrite of adress variable in every repetition by lambda keyword parameter """
    global repetition
    if repetition == 0:
        adresses = cities()

        archon = ImageTk.PhotoImage(Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/archleft.jpg"))

        for adress in adresses:
            Archy.add_command(label=f"   {adress}", image=archon, compound=tkinter.LEFT,
                              command=lambda mesto=adress: pop_up_gui(mesto, mainframe))
            Archy.archon = archon

        CPP.add_cascade(label="   Vyber město pro arch", menu=Archy, compound=tkinter.RIGHT)
        repetition += 1


# deleting the pop-up menu when mouse left and resetting the repetition controller var
def abortArchyMenu(event, archy_widget):
    if event.widget == archy_widget:
        archy_widget.destroy()
        global repetition
        repetition = 0


# ********************************** GUI OUTPUT WIDGETS ***************************************************************

# -------------------------DISPLAY SELECTED DATA IN TREEVIEW TABLE ---------------------------
# TODO > try to separate the function into separate file
def createTreeview(main_frame, displayCols, selection):
    # resetting global checkers
    global iid
    iid = None
    global y_coord
    y_coord = 0

    # 1. creating a custom theme
    global i
    if i == 0:
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview", background="silver", foreground="black", rowheight=30,
                        fieldbackground="LightSeaGreen")
        style.map(
            "Treeview",
            bakcground=[("selected", "LightSeaGreen"), ("active", "red")]
        )
        style.configure("Treeview.Heading", background="LightSeaGreen", foreground="Black")
        i += 1
    else:
        pass

    # creating a container frame
    SearchBoxcontainer = Frame(main_frame)
    SearchBoxcontainer.config(bg="#7bacc7")
    SearchBoxcontainer.pack(pady=20)
    # 2. create Treeview Scrollbar
    scrollbar = Scrollbar(SearchBoxcontainer)
    scrollbar.pack(side=LEFT, fill=Y)

    # 3. creating a treeview table
    table = ttk.Treeview(SearchBoxcontainer, selectmode="browse", yscrollcommand=scrollbar.set)
    table["columns"] = displayCols
    table.column("#0", width=0, minwidth=0)
    table.column("#0", width=0, minwidth=0)
    table.heading("#0", text="Index", anchor=CENTER)

    # aligning cell labels and contents
    for column in table["columns"]:
        if column == "Přímění":
            anchor = W
        else:
            anchor = CENTER
        table.column(column, anchor=anchor, width=120, minwidth=80)
        table.heading(column, text=column, anchor=CENTER)

    # 4. setting styles for striped rows
    table.tag_configure("oddrow", background="white")
    table.tag_configure("evenrow", background="lightblue")

    # 5. populating the treeview rows with data from selection + striped rows generating
    row = 1
    for index in selection.index:
        if row % 2:
            table.insert(parent="", index="end", text="",
                         values=(tuple(selection.at[index, col] for col in table["columns"])),
                         tags="evenrow")
        else:
            table.insert(parent="", index="end", text="",
                         values=(tuple(selection.at[index, col] for col in table["columns"])),
                         tags="oddrow")
        row += 1

    table.pack()

    # 6. configuring the scrollbar
    scrollbar.config(command=table.yview)

    # 7. configuring the righ-click menu --> NESTED FUNCTION !!!

    def select(event):
        """"NESTED FUNCTION:
        function gets triggered on mouse click, getting the y coordinate of the clicked item of treeview widget.
        (focus action can be triggered only on mouse click)
        finally the cathed z coordinate of the click is stored it onto global variable y_coord,
        wchich is invoked bz import and used form displaying the context menu via Popup.shommenu function call"""
        global iid
        global y_coord

        region = table.identify_region(event.x, event.y)  # cathing the "header / cell" identifier

        # control for case the heading was focused on click --> reset ycoord to 0, and thus prohibit executing of
        # Popup.showMenu on headings
        # else set ycoord to the y value of the click event --> this gets imported to Popup.showMenu
        # and trigger the showing of popup Menu, but just on the same y coordinate as was the focus click (same line]
        if region == 'heading':
            y_coord = 0
            return
        elif region == "cell":
            iid = table.identify_row(event.y)
            if iid:
                y_coord = event.y_root
            else:
                return
        elif region == "nothing":
            return
            # END OF NESTED FUNCTION SELECT

    # NESTED WRAP FUNCTION for showing the popup menu /// see Righ_click_menu.py
    def manage_popup(event):
        Popup = RighClickMenu(table, tearoff=0)
        Popup.showMenu(event)

    # 8. binding the click to select , and right mouse click to show popup menu
    table.bind("<Button-1>", select)
    table.bind("<Button-3>", manage_popup)


# -------------------------COMBOBOX AND BUTTON FOR FILTERING THE PAYING PEOPLE -------------------------
def searchComboBoxNP(main_frame, condition):
    data = readDataFromZippedExcel()
    # clearing the screen after click
    i = 0
    if i == 0:
        for widgets in main_frame.winfo_children():
            widgets.destroy()

    if data is not None:
        columnList = data.columns.values
        CPPcols = [col for col in columnList if col.startswith('CPP')]

        values = CPPcols
        varOd = StringVar()
        varDo = StringVar()

        # container
        container = Frame(main_frame)
        container.pack(pady=20)

        # ------------------------OD PANE---------------------------
        odLabel = Label(container, text="CPP od: ", font=("Arial", 12))
        odLabel.grid(row=0, column=0, padx=(10, 10))
        searchFromBox = ttk.Combobox(container, textvariable=varOd, values=values)
        searchFromBox.set(values[len(values) - 2])

        # storing the selection, creating callback function and on selected binding
        def getOd(event):
            od = varOd.get()
            return od

        searchFromBox.grid(row=0, column=1)
        searchFromBox.bind("<<ComboboxSelected>>", getOd)

        # ------------------------DO PANE----------------------------
        doLabel = Label(container, text="CPP do: ", font=("Arial", 12))
        doLabel.grid(row=0, column=4, padx=(10, 10))
        searchToBox = ttk.Combobox(container, textvariable=varDo, values=values)

        # storing the selection, creating callback function and on selected binding
        def getDo(event):
            do = varDo.get()
            return do

        searchToBox.set(values[len(values) - 1])
        searchToBox.grid(row=0, column=5)
        searchFromBox.bind("<<ComboboxSelected>>", getDo)

        # Search Button
        searchButton = ttk.Button(container, text="Zobraz Výběr",
                                  command=lambda: filtrujPlatici(main_frame, searchFromBox.get(), searchToBox.get(),
                                                                 data, condition))
        searchButton.grid(row=0, column=3, padx=(20, 5))

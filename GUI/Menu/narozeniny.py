import tkinter
from tkinter import Menu
from GUI.Menu.CPPsubmenu import createTreeview
from GUI.Menu.CPPsubmenu import readDataFromZippedExcel
from PIL import ImageTk, Image


# -------------------- GIU MENU ITEMS ------------------------------------------------------------------
def narozeninySubmenu(main_menu, main_frame):
    # load icons
    this = ImageTk.PhotoImage(Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/archleft.jpg"))
    next = ImageTk.PhotoImage(Image.open("C:/Users/Michal/PycharmProjects/agenda/GUI/Menu/icons/doublearrow.jpg"))


    narozeniny = Menu(main_menu, tearoff=0)
    narozeniny.add_command(label="   Narozeniny v měsíci", command=lambda: searchBirthday(main_frame, 0, sort="Den"),
                           image=this, compound=tkinter.LEFT)
    narozeniny.this = this

    narozeniny.add_command(label="   Narozeniny v dalším měsíci",
                           command=lambda: searchBirthday(main_frame, 1, sort="Den"), image=next, compound=tkinter.LEFT)
    narozeniny.next = next
    narozeniny.add_separator()

    narozeniny.add_command(label="   Okrouhlá jubilea v měsíci", image=this, compound=tkinter.LEFT, command=lambda: searchBirthday(main_frame, 0, sort="Let",
                                                                                             isin_condition=[10, 20, 30,
                                                                                                             40, 50, 60,
                                                                                                             70, 80, 90,
                                                                                                             100]))
    narozeniny.add_command(label="   Okrouhlá jubilea v dalším měsíci", image=next, compound=tkinter.LEFT,
                           command=lambda: searchBirthday(main_frame, 1, sort="Let",
                                                          isin_condition=[10, 20, 30,
                                                                          40, 50, 60,
                                                                          70, 80, 90,
                                                                          100]))
    narozeniny.add_separator()

    narozeniny.add_command(label="   Pětková jubilea 55+ v měsíci", image=this, compound=tkinter.LEFT,
                           command=lambda: searchBirthday(main_frame, 0, sort="Let",
                                                          isin_condition=[55, 65, 75, 85,
                                                                          95, 105]))
    narozeniny.add_command(label="   Pětková jubilea 55+ v dalším měsíci", image=next, compound=tkinter.LEFT,
                           command=lambda: searchBirthday(main_frame, 1, sort="Let",
                                                          isin_condition=[55, 65, 75, 85,
                                                                          95, 105]))
    narozeniny.add_separator()

    narozeniny.add_command(label="   18 v tomto měsíci", image=this, compound=tkinter.LEFT,
                           command=lambda: searchBirthday(main_frame, 0, sort="Den", isin_condition=[18]))
    narozeniny.add_command(label="   18 v dalším měsíci", image=next, compound=tkinter.LEFT,
                           command=lambda: searchBirthday(main_frame, 1, sort="Den", isin_condition=[18]))

    main_menu.add_cascade(label="   Narozeniny a jubilea", menu=narozeniny)


# ---------------------------------------------------------------------------------------------------------

def naloadujData(modifier):
    from datetime import datetime
    data = readDataFromZippedExcel()

    # all Nar. column data selected
    monthCheck = list(data["Nar."].fillna(0))
    montchArray = monthCheck
    narChosen = []
    yearsCalc = []
    days = []
    print(montchArray)
    print(datetime.now().month)
    for item in montchArray:
        if item == 0:
            pass
        elif item != 0:
            # splitting every item into itemarray [year, month with zero, day with zero
            itemarray = str(item).split("-")
            # getting the current month but without zero, therefore the "0" replace with "" below
            currentMonth = datetime.now().month + modifier
            # getting rid of 0 in month description
            if itemarray[1][0] == "0":
                itemarray[1] = itemarray[1].replace("0", "")
            # getting rid of 0 in day description
            if itemarray[2][0] == "0":
                itemarray[2] = itemarray[2].replace("0", "")
            # comparing the item month with current month in no zero format + append the match to narchosen list
            if itemarray[1] == str(currentMonth):
                narChosen.append(item)
                yCalc = datetime.now().year - int(itemarray[0])
                yearsCalc.append(yCalc)
                days.append(int(itemarray[2]))  # dazs array for sorting bz day in the month
            itemarray.clear()
    # checking whether the value of [Nar.] matches some of the items of narchosen list
    selection = data.loc[data["Nar."].isin(narChosen)]

    selection.insert(loc=3, column="Let", value=yearsCalc)
    selection.insert(loc=4, column="Den", value=days)

    return selection


# VYHLEDAVACI FUNKCE : ARG : sloupec na trideni, podminka na filter
def searchBirthday(main_frame, modifier, sort, **kwargs):
    isin_condition = kwargs.get("isin_condition", None)
    # clearing the main-frame of all widgets
    widgetList = main_frame.winfo_children()
    # deleting the old treeview table from the screen before rendering a new one
    if len(widgetList) > 0:
        for widget in widgetList:
            widget.destroy()

    # getting the selection dataframe from naloadujData ()
    selection = naloadujData(modifier)
    # ----------------------------------------------------------------
    if isin_condition is not None:
        selection = selection.loc[selection["Let"].isin(isin_condition)]
    else:
        pass
    # sorting the output by date values in [Nar.] column
    selection = selection.sort_values(by=sort)
    # putting the output into  graphic by creating a treeview
    createTreeview(main_frame, ["Jméno", "Přijmení", "Adresa", "Nar.", "Let"], selection=selection) #TODO> pridat sloupec "Mesto"

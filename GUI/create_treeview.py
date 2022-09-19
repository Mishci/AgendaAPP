#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from GUI.Right_click_menu.Right_click_menu import RighClickMenu

iid = None
y_coord = 0
i = 0


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
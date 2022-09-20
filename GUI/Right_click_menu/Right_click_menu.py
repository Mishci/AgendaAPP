#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import Menu, LEFT
from GUI.Right_click_menu.Edit_pane import Edit_Pane


class RighClickMenu(Menu):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.tree = master

        self.add_items()

    def add_items(self):
        self.add_command(label="Edituj", compound=LEFT, command=self.edit)
        self.add_command(label="Vymaž", compound=LEFT, command=self.delete_item)
        self.add_separator()

    def edit(self):
        from GUI.create_treeview import iid
        from LOGIC.readDataFromZippedExcel import readDataFromZippedExcel
        select = self.tree.item(iid, "values")  # VALUES FROM SELECTION
        data = readDataFromZippedExcel()
        # SEARCHING ALL THE COLUMNS BELONGING TO A PERSON WITH A NAME AND SURNAME SELECTED
        personal = data.loc[(data["Přijmení"] == select[0]) & (data["Jméno"] == select[1])]

        # GETTING THE COLUMN NAMES + COLUMN VALUES INTO TWO LISTS
        columns = personal.columns.values
        personal_data = personal.iloc[0, :].tolist()

        # JOINING THE LISTS INTO TUPLE BY LIST COMPREHENSION
        output = tuple([(columns[index], personal_data[index]) for index in range(len(columns) - 1)])

        # SENDING THE TUPLE OVER TO EDIT_PANE , THUS CREATING THE EDIT PANE
        EditPane = Edit_Pane(column_data_tuples_list=output)

    def delete_item(self):
        print("Vymaž!")

    def showMenu(self, event):
        try:
            from GUI.create_treeview import y_coord, iid
            if y_coord > 0 and iid is not None:
                self.post(event.x_root, y_coord)
                print(y_coord)

        finally:
            self.grab_release()
